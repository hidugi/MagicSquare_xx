"""Blank cell coordinates — FR-LOC-01 / PRD §5.2."""

from entity.constants import (
    BLANK_CELL,
    COORD_ONE_BASE,
    EXPECTED_BLANK_COUNT,
    GRID_SIZE,
)


class BlankCountError(Exception):
    """INV-02 — blank count ≠ 2 (domain Rule, not E001~E005)."""

    rule_id = "BLANK_COUNT"


def find_blank_coords(grid: list[list[int]]) -> tuple[tuple[int, int], tuple[int, int]]:
    """Return two blank positions as 1-index (row, col), row-major order."""
    blanks: list[tuple[int, int]] = []
    for row_idx in range(GRID_SIZE):
        for col_idx in range(GRID_SIZE):
            if grid[row_idx][col_idx] == BLANK_CELL:
                blanks.append((row_idx + COORD_ONE_BASE, col_idx + COORD_ONE_BASE))
    if len(blanks) != EXPECTED_BLANK_COUNT:
        raise BlankCountError()
    return blanks[0], blanks[1]
