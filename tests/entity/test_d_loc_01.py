"""D-LOC-01 — find_blank_coords row-major (FR-LOC-01 / PRD §5.2)."""

import json
from pathlib import Path

from entity.blank_coords import find_blank_coords

_GOLDEN = Path(__file__).resolve().parent.parent / "golden" / "d_loc_01_g1.json"


def test_d_loc_01_blank_coords_row_major(grid_g1: list[list[int]]) -> None:
    # Given: G1 격자 (0이 2개) — Golden Master grid와 일치
    with _GOLDEN.open(encoding="utf-8") as f:
        golden = json.load(f)
    assert grid_g1 == golden["grid"]

    # When: find_blank_coords(grid_g1) 호출
    result = find_blank_coords(grid_g1)

    # Then: Golden Master 1-index row-major
    expected = tuple(tuple(pair) for pair in golden["then"]["coords_1index_row_major"])
    assert result == expected
