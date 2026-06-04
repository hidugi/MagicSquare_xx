"""D-SOL-01 — solve_step_a int[6] Golden Master (G1 step A)."""

from entity.solution import solve_step_a

from _approval import assert_matches_golden

_GOLDEN_REL = "d_sol_01_g1_step_a.approved.txt"


def test_d_sol_01_step_a_success(grid_g1: list[list[int]]) -> None:
    # Given: G1
    # When: solve_step_a
    result = solve_step_a(grid_g1)
    # Then: Golden Master (int[6] 1-index)
    assert_matches_golden(result, _GOLDEN_REL)
