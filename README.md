# claude-ai

개인 Claude AI 자동화 허브. 업무 자동화 에이전트들을 관리합니다.

## 구조

```
claude-ai/
├── core/           # 공통 기반 (클라이언트, BaseAgent)
├── agents/         # 재사용 가능한 에이전트
├── tools/          # 툴 구현체 (Jira, 파일 등)
├── skills/         # 에이전트별 시스템 프롬프트 (.md)
└── projects/       # 실제 자동화 프로젝트
    ├── jira-automation/
    └── code-reviewer/
```

## 시작하기

```bash
cd claude-ai

# 의존성 설치
pip install -e .

# 환경변수 설정
cp .env.example .env
# .env 파일에 API 키 입력

# Jira 자동화 실행
python projects/jira-automation/main.py

# 코드 리뷰
python projects/code-reviewer/main.py ~/Project/api-server/src/SomeFile.java
```

## 새 프로젝트 추가

```bash
mkdir projects/my-new-project
touch projects/my-new-project/main.py
```

## 새 에이전트 추가

1. `skills/my_skill.md` — 시스템 프롬프트 작성
2. `agents/my_agent.py` — `BaseAgent` 상속
3. `agents/__init__.py` — export 추가
