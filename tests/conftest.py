"""공통 픽스처 — 격자 데이터만 (도메인 로직 없음)."""

import sys
from pathlib import Path

import pytest

_SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(_SRC))
for _mod in ("entity.constants", "entity"):
    sys.modules.pop(_mod, None)

from entity.constants import GRID_SIZE


@pytest.fixture
def grid_g1() -> list[list[int]]:
    """G1 — 문제정의 부록 격자. 빈칸 `0` 2개, row-major."""
    grid = [
        [16, 3, 2, 13],
        [5, 10, 11, 0],
        [9, 6, 0, 12],
        [4, 15, 14, 1],
    ]
    assert len(grid) == GRID_SIZE
    assert all(len(row) == GRID_SIZE for row in grid)
    assert sum(cell == 0 for row in grid for cell in row) == 2
    return grid
