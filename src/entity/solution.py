"""Partial board solver — D-SOL-01 step A (int[6] 1-index contract)."""

from __future__ import annotations

from itertools import permutations

from entity.blank_coords import find_blank_coords
from entity.constants import BLANK_CELL, CELL_MAX, GRID_SIZE, MAGIC_SUM


class NoSolutionError(Exception):
    """No values complete all 10 lines to MAGIC_SUM."""

    rule_id = "NO_SOLUTION"


def _ten_lines() -> list[list[tuple[int, int]]]:
    lines: list[list[tuple[int, int]]] = []
    for row in range(GRID_SIZE):
        lines.append([(row, col) for col in range(GRID_SIZE)])
    for col in range(GRID_SIZE):
        lines.append([(row, col) for row in range(GRID_SIZE)])
    lines.append([(i, i) for i in range(GRID_SIZE)])
    lines.append([(i, GRID_SIZE - 1 - i) for i in range(GRID_SIZE)])
    return lines


_LINES = _ten_lines()


def _lines_valid(grid: list[list[int]]) -> bool:
    for line in _LINES:
        if sum(grid[r][c] for r, c in line) != MAGIC_SUM:
            return False
    return True


def solve_step_a(grid: list[list[int]]) -> list[int]:
    """Return [r1, c1, n1, r2, c2, n2] — 1-index, row-major blank order."""
    (r1, c1), (r2, c2) = find_blank_coords(grid)
    used = {cell for row in grid for cell in row if cell != BLANK_CELL}
    available = [n for n in range(1, CELL_MAX + 1) if n not in used]
    b0 = (r1 - 1, c1 - 1)
    b1 = (r2 - 1, c2 - 1)

    for n_a, n_b in permutations(available, 2):
        trial = [row[:] for row in grid]
        trial[b0[0]][b0[1]] = n_a
        trial[b1[0]][b1[1]] = n_b
        if _lines_valid(trial):
            return [r1, c1, n_a, r2, c2, n_b]

    raise NoSolutionError()
