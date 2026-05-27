from pathlib import Path


def read_file(path: str) -> str:
    p = Path(path).expanduser()
    if not p.exists():
        return f"파일 없음: {path}"
    if p.stat().st_size > 1_000_000:
        return f"파일이 너무 큽니다 (1MB 초과): {path}"
    return p.read_text(encoding="utf-8", errors="ignore")


def write_file(path: str, content: str) -> str:
    p = Path(path).expanduser()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return f"파일 저장 완료: {path}"
