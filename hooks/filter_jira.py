#!/usr/bin/env python3
"""
PostToolUse 훅 - Jira MCP 툴 응답 필터링
불필요한 필드를 제거해 Claude 컨텍스트 토큰을 절약합니다.
"""
import json
import sys


def filter_issue(issue: dict) -> dict:
    f = issue.get("fields", {})
    return {
        "key": issue.get("key"),
        "summary": f.get("summary"),
        "status": f.get("status", {}).get("name"),
        "issuetype": f.get("issuetype", {}).get("name"),
        "priority": f.get("priority", {}).get("name") if f.get("priority") else None,
        "assignee": f.get("assignee", {}).get("displayName") if f.get("assignee") else None,
        "updated": (f.get("updated") or "")[:10],
        "duedate": f.get("duedate"),
        "description": _truncate_adf(f.get("description")),
        "comments": [
            {
                "author": c.get("author", {}).get("displayName"),
                "body": _truncate_adf(c.get("body")),
            }
            for c in (f.get("comment", {}).get("comments") or [])[-3:]
        ],
        "subtasks": [
            {
                "key": s.get("key"),
                "summary": s.get("fields", {}).get("summary"),
                "status": s.get("fields", {}).get("status", {}).get("name"),
            }
            for s in (f.get("subtasks") or [])
        ],
    }


def _truncate_adf(node, max_chars: int = 500) -> str:
    """Atlassian Document Format을 plain text로 변환 후 max_chars로 자름."""
    text = _adf_to_text(node)
    if len(text) > max_chars:
        return text[:max_chars] + "... (truncated)"
    return text


def _adf_to_text(node) -> str:
    if node is None:
        return ""
    if isinstance(node, str):
        return node
    if isinstance(node, list):
        return "".join(_adf_to_text(n) for n in node)
    if isinstance(node, dict):
        t = node.get("type", "")
        if t == "text":
            return node.get("text", "")
        if t == "hardBreak":
            return "\n"
        inner = "".join(_adf_to_text(c) for c in node.get("content", []))
        if t in ("paragraph", "heading", "listItem", "blockquote", "codeBlock"):
            return inner + "\n"
        return inner
    return ""


def main():
    raw = sys.stdin.read()
    if not raw.strip():
        sys.exit(0)

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = payload.get("tool_name", "")
    response = payload.get("tool_response", payload)

    # jira_ticket_detail: 단일 이슈
    if "ticket_detail" in tool_name:
        if isinstance(response, dict) and "fields" in response:
            filtered = filter_issue(response)
            print(json.dumps(filtered, ensure_ascii=False))
            return

    # jira_my_tickets / jira_sprint_tickets: 이슈 목록
    if "tickets" in tool_name or "sprint" in tool_name:
        if isinstance(response, list):
            # 목록은 이미 jira_tools.py에서 필터링됨, description만 추가 자름
            filtered = []
            for item in response:
                item["description"] = (item.get("description") or "")[:200]
                filtered.append(item)
            print(json.dumps(filtered, ensure_ascii=False))
            return

    # 해당 없는 툴은 그대로 통과
    sys.exit(0)


if __name__ == "__main__":
    main()
