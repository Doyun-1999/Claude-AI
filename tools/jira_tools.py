import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()

_story_points_field: str | None = None


@lru_cache(maxsize=1)
def _get_jira():
    try:
        from jira import JIRA
    except ImportError:
        raise ImportError("jira 패키지 없음: pip install jira")

    server = os.environ.get("JIRA_SERVER")
    email = os.environ.get("JIRA_EMAIL")
    token = os.environ.get("JIRA_API_TOKEN")

    missing = [k for k, v in {"JIRA_SERVER": server, "JIRA_EMAIL": email, "JIRA_API_TOKEN": token}.items() if not v]
    if missing:
        raise EnvironmentError(f".env에 없는 값: {', '.join(missing)}")

    return JIRA(server=server, basic_auth=(email, token))


def _story_points(jira) -> str | None:
    global _story_points_field
    if _story_points_field is not None:
        return _story_points_field
    for field in jira.fields():
        if "story" in field["name"].lower() and "point" in field["name"].lower():
            _story_points_field = field["id"]
            return _story_points_field
    return None


def _sprint_name(issue) -> str | None:
    import re
    for val in issue.raw["fields"].values():
        if not isinstance(val, list) or not val:
            continue
        first = val[0]
        if isinstance(first, str) and "sprint" in first.lower():
            m = re.search(r"name=([^,\]]+)", first)
            if m:
                return m.group(1).strip()
        if isinstance(first, dict) and "name" in first and "boardId" in str(first):
            return first["name"]
    return None


def get_my_tickets(assignee: str | None = None, max_results: int = 20) -> list[dict]:
    jira = _get_jira()
    sp = _story_points(jira)
    assignee = assignee or os.environ.get("JIRA_ASSIGNEE", "currentUser()")

    issues = jira.search_issues(
        f'assignee = "{assignee}" AND status != Done ORDER BY priority DESC',
        maxResults=max_results,
    )
    return [
        {
            "key": i.key,
            "summary": i.fields.summary,
            "description": (str(i.fields.description or "")[:300] + "...") if i.fields.description else "",
            "priority": str(i.fields.priority),
            "status": str(i.fields.status),
            "story_points": getattr(i.fields, sp, None) if sp else None,
            "sprint": _sprint_name(i),
        }
        for i in issues
    ]


def get_ticket_detail(ticket_key: str) -> dict:
    jira = _get_jira()
    sp = _story_points(jira)
    i = jira.issue(ticket_key)
    return {
        "key": i.key,
        "summary": i.fields.summary,
        "description": str(i.fields.description or ""),
        "priority": str(i.fields.priority),
        "status": str(i.fields.status),
        "assignee": str(i.fields.assignee),
        "story_points": getattr(i.fields, sp, None) if sp else None,
        "sprint": _sprint_name(i),
        "comments": [
            {"author": c.author.displayName, "body": c.body}
            for c in i.fields.comment.comments[-5:]
        ],
        "subtasks": [
            {"key": s.key, "summary": s.fields.summary, "status": str(s.fields.status)}
            for s in (i.fields.subtasks or [])
        ],
    }


def get_sprint_tickets(project_key: str, max_results: int = 50) -> list[dict]:
    jira = _get_jira()
    sp = _story_points(jira)
    issues = jira.search_issues(
        f'project = "{project_key}" AND sprint in openSprints() ORDER BY status ASC',
        maxResults=max_results,
    )
    return [
        {
            "key": i.key,
            "summary": i.fields.summary,
            "status": str(i.fields.status),
            "assignee": str(i.fields.assignee),
            "priority": str(i.fields.priority),
            "story_points": getattr(i.fields, sp, None) if sp else None,
        }
        for i in issues
    ]


def add_comment(ticket_key: str, comment: str) -> str:
    jira = _get_jira()
    jira.add_comment(ticket_key, comment)
    return f"{ticket_key}에 댓글 추가 완료"
