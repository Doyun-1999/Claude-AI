#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from mcp.server.fastmcp import FastMCP
from tools.jira_tools import get_my_tickets, get_ticket_detail, get_sprint_tickets, add_comment

mcp = FastMCP("jira")


@mcp.tool()
def jira_my_tickets(assignee: str = "", max_results: int = 20) -> list[dict]:
    """내게 할당된 미완료 Jira 티켓 목록을 가져옵니다. assignee 생략 시 .env의 JIRA_ASSIGNEE 사용."""
    return get_my_tickets(assignee=assignee or None, max_results=max_results)


@mcp.tool()
def jira_ticket_detail(ticket_key: str) -> dict:
    """특정 Jira 티켓의 상세 내용을 가져옵니다. (description 전문, 댓글, 서브태스크 포함)"""
    return get_ticket_detail(ticket_key)


@mcp.tool()
def jira_sprint_tickets(project_key: str, max_results: int = 50) -> list[dict]:
    """현재 활성 스프린트의 전체 티켓을 가져옵니다."""
    return get_sprint_tickets(project_key, max_results)


@mcp.tool()
def jira_add_comment(ticket_key: str, comment: str) -> str:
    """Jira 티켓에 댓글을 추가합니다."""
    return add_comment(ticket_key, comment)


if __name__ == "__main__":
    mcp.run()
