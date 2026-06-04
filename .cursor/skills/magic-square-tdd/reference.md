# D-* Logic Track 테스트 ID (참조)

| ID | 대상 Layer | 요약 |
|----|------------|------|
| D-001 | entity | MagicConstant SSOT — `34`/`16`/격자 크기 단일 정의 |
| D-002 | entity | INV-01 `SHAPE_INVALID` — 4×4 아님 |
| D-003 | entity | INV-02 `BLANK_COUNT` — 빈칸 `0` 정확히 2 |
| D-004 | entity | INV-03 `VALUE_RANGE` — 0 또는 1~16 |
| D-005 | entity | INV-03 `DUPLICATE` — 1~16 중복 |
| D-006 | entity | INV-04 `LINE_SUM` — 10선 합 34 |
| D-007 | control | `validate_board` — structural 정상·위반 조립 |
| D-008 | control | SC-3 동일 grid → 동일 ValidationResult |
| D-009 | control | `find_blank_coords` — 빈칸 2 좌표 (P1, 선택) |

> U-* 목록은 boundary 구현 Phase에서 `test_u_*` 와 함께 추가.
