"""Golden Master approval — UPDATE_GOLDEN=1 로 기준 파일 갱신."""

from __future__ import annotations

import os
from pathlib import Path

GOLDEN_DIR = Path(__file__).resolve().parent / "golden"


def serialize_golden(actual: list[int] | str) -> str:
    """고정 포맷: SUCCESS + int[6] 공백 구분, 또는 ERROR + Rule/경계 코드 문자열."""
    if isinstance(actual, str):
        return f"ERROR\n{actual.strip()}"
    if not isinstance(actual, list) or len(actual) != 6:
        raise TypeError("SUCCESS golden requires list[int] of length 6")
    parts = " ".join(str(x) for x in actual)
    return f"SUCCESS\n{parts}"


def assert_matches_golden(actual: list[int] | str, relative: str) -> None:
    """relative: golden/ 이하 경로 (예: d_sol_01_g1_step_a.approved.txt)."""
    path = GOLDEN_DIR / relative
    text = serialize_golden(actual)

    if os.environ.get("UPDATE_GOLDEN") == "1":
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n", encoding="utf-8", newline="\n")
        return

    if not path.is_file():
        raise AssertionError(f"Golden file missing: {path}")

    approved = path.read_text(encoding="utf-8").replace("\r\n", "\n").strip()
    if text == approved:
        return

    raise AssertionError(
        f"Golden mismatch for {relative}\n"
        f"--- expected (approved)\n{approved}\n"
        f"--- actual\n{text}"
    )
