"""D-LOC-01 — find_blank_coords (FR-LOC-01 / PRD §5.2) Golden Master."""

from entity.blank_coords import find_blank_coords
from entity.constants import BLANK_CELL

from _approval import assert_matches_golden

_GOLDEN_REL = "d_loc_01_g1_step_a.approved.txt"


def _coords_to_int6(coords: tuple[tuple[int, int], tuple[int, int]]) -> list[int]:
    """1-index [r1,c1,n1,r2,c2,n2] — 빈칸 값은 BLANK_CELL(0)."""
    (r1, c1), (r2, c2) = coords
    return [r1, c1, BLANK_CELL, r2, c2, BLANK_CELL]


def test_d_loc_01_step_a_success(grid_g1: list[list[int]]) -> None:
    # Given: G1 격자 (0이 2개)
    # When: find_blank_coords(grid_g1) 호출
    coords = find_blank_coords(grid_g1)
    actual = _coords_to_int6(coords)
    # Then: Golden Master int[6] 1-index row-major
    assert_matches_golden(actual, _GOLDEN_REL)
