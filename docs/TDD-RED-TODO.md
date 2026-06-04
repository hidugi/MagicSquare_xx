# MagicSquare_xx — RED 단계 To Do List

| 항목 | 내용 |
|------|------|
| 프로젝트 | MagicSquare_xx |
| 단계 | Dual-Track TDD · **RED** (실패 테스트 먼저) |
| 작성일 | 2026-06-04 |
| 관련 | [`PRD.md`](PRD.md), [`.cursor/commands/tdd-red.md`](../.cursor/commands/tdd-red.md), [`reference.md`](../.cursor/skills/magic-square-tdd/reference.md) |

**목적:** Boundary(UI) · Logic(D-*) RED 설계를 **체크리스트**로 고정한다.  
**규칙:** RED 단계에서는 `tests/`만 수정 · `src/`는 GREEN · Logic Track Domain Mock 금지 · UI Track control/I/O Mock 허용.

**RED 성공 기준:** 대상 테스트 **1건 이상 FAILED** 또는 **ImportError** · `skip`/`xfail`/assert 완화 금지.

---

## 진행 순서 (권장)

- [ ] **1.** Logic — `D-001` MagicConstant RED → GREEN
- [ ] **2.** Logic — `D-002`~`D-006` entity Rule RED → GREEN (순차)
- [ ] **3.** Logic — `D-007`~`D-008` control `validate_board` RED → GREEN
- [ ] **4.** Logic *(선택 P1)* — `D-009` `find_blank_coords` RED → GREEN
- [ ] **5.** Boundary — `U-IN-*` 입력 검증 RED → GREEN
- [ ] **6.** Boundary — `U-OUT-*` · `U-FLOW-*` RED → GREEN

---

## Track A — Boundary RED (`tests/boundary/test_u_*.py`)

**Layer:** `boundary` · **Track:** UI · **검증:** E001~E007, 입출력·흐름 · **Mock:** control·I/O stub 허용

### A-1 입력 검증 (U-IN)

| ID | Given | Then (기대값) | Expected RED Failure | To Do |
|----|-------|---------------|----------------------|-------|
| U-IN-01 | `grid=None` | `E003 INVALID_NULL` — boundary 즉시 반환, control 미호출 | `ModuleNotFoundError` / `ImportError` | [ ] 테스트 작성 · [ ] pytest FAIL 확인 |
| U-IN-02 | `grid=3×4` | `E001 INVALID_SIZE` | `AssertionError` | [ ] 테스트 작성 · [ ] pytest FAIL 확인 |
| U-IN-03 | `grid=4×4`, 빈칸 `0` **0개** | `E002 INVALID_BLANKS` | `AssertionError` | [ ] 테스트 작성 · [ ] pytest FAIL 확인 |
| U-IN-04 | `grid=4×4`, 빈칸 `0` **3개** | `E002 INVALID_BLANKS` | `AssertionError` | [ ] 테스트 작성 · [ ] pytest FAIL 확인 |
| U-IN-05 | 셀 `17` 또는 `-1` | `E004 INVALID_VALUE` | `AssertionError` | [ ] 테스트 작성 · [ ] pytest FAIL 확인 |
| U-IN-06 | 셀 `"3"` 등 비정수 | `E005 INVALID_TYPE` | `AssertionError` | [ ] 테스트 작성 · [ ] pytest FAIL 확인 |

### A-2 출력·메시지 (U-OUT)

| ID | Given | Then (기대값) | Expected RED Failure | To Do |
|----|-------|---------------|----------------------|-------|
| U-OUT-01 | 유효 부분 보드 **G1** | `validate_input(G1)` → control에 `ok` 전달, `violated_rules==[]` | `pytest.fail("RED")` / `ImportError` | [ ] 테스트 작성 · [ ] pytest FAIL 확인 |
| U-OUT-02 | **G_dup** (1~16 중복) | 사용자 메시지에 `DUPLICATE` 또는 E 매핑 문구 | `AssertionError` | [ ] 테스트 작성 · [ ] pytest FAIL 확인 |

### A-3 흐름 (U-FLOW)

| ID | Given | Then (기대값) | Expected RED Failure | To Do |
|----|-------|---------------|----------------------|-------|
| U-FLOW-01 | `grid=None` | `validate_board`(control) **0회** 호출 | `pytest.fail("RED")` | [ ] 테스트 작성 · [ ] pytest FAIL 확인 |
| U-FLOW-02 | `E001` 발생 입력 | control **0회**, boundary만 종료 | `AssertionError` | [ ] 테스트 작성 · [ ] pytest FAIL 확인 |

### A-4 E001~E007 ↔ PRD Rule (boundary 번역 — GREEN 시 고정)

| Boundary 코드 | 조건 | entity Rule ID | To Do |
|---------------|------|----------------|-------|
| E001 | 4×4 아님 | `SHAPE_INVALID` | [ ] 매핑·메시지 구현 |
| E002 | `0` ≠ 2개 | `BLANK_COUNT` | [ ] 매핑·메시지 구현 |
| E003 | `grid is None` | *(호출 전 차단)* | [ ] 매핑·메시지 구현 |
| E004 | 0·1~16 밖 값 | `VALUE_RANGE` | [ ] 매핑·메시지 구현 |
| E005 | 타입 오류 | *(boundary 전용)* | [ ] 매핑·메시지 구현 |
| E006~E007 | stdin/표시 실패 | Phase 4·I/O | [ ] *(Phase 1 제외 가능)* |

---

## Track B — Logic RED

**Track:** Logic · **Mock:** 도메인 Mock **금지** (실 Rule·실 객체)

### B-1 Entity (`tests/entity/test_d_*.py`)

| ID | Given | Then (기대값) | Expected RED Failure | To Do |
|----|-------|---------------|----------------------|-------|
| D-001 | MagicConstant import | `MAGIC_SUM==34`, `GRID_SIZE==4`, `CELL_MAX==16` | `ImportError` | [ ] `test_d_magic_constant.py` · [ ] FAIL |
| D-002 | `grid=3×4` | `check_shape` → `SHAPE_INVALID` ∈ `violated_rules` | `ImportError` / `AssertionError` | [ ] `test_d_shape.py` · [ ] FAIL |
| D-003 | `grid=4×4`, `0` **0개** | `BLANK_COUNT` | `AssertionError` | [ ] `test_d_blank_count.py` · [ ] FAIL |
| D-003b | `grid=4×4`, `0` **3개** | `BLANK_COUNT` | `AssertionError` | [ ] *(D-003 동일 파일)* · [ ] FAIL |
| D-004 | 셀 `17` | `VALUE_RANGE` | `AssertionError` | [ ] `test_d_value_range.py` · [ ] FAIL |
| D-005 | `5`가 두 칸 | `DUPLICATE` | `AssertionError` | [ ] `test_d_duplicate.py` · [ ] FAIL |
| D-006 | 완성 격자, 행만 34·주대각 틀림 **(SC-2)** | `LINE_SUM` ∈ `violated_rules` | `AssertionError` | [ ] `test_d_line_sum.py` · [ ] FAIL |
| D-006b | 부분 보드 **G1**, `LINE_SUM` 불일치 | `structural`: `LINE_SUM` 미검사, `ok=true` | `AssertionError` | [ ] `test_d_line_sum.py` · [ ] FAIL |

### B-2 Control (`tests/control/test_d_*.py`)

| ID | Given | Then (기대값) | Expected RED Failure | To Do |
|----|-------|---------------|----------------------|-------|
| D-007 | **G1** (부록 예시, INV-01~03 충족) | `validate_board(G1)` → `{ok: true, violated_rules: []}` | `ImportError` | [ ] `test_d_validate_board.py` · [ ] FAIL |
| D-007b | **G_blank_0** | `{ok: false, violated_rules: ["BLANK_COUNT"]}` | `AssertionError` | [ ] 동일 파일 · [ ] FAIL |
| D-007c | **G_line_bad** (SC-2) | `{ok: false, violated_rules: ["LINE_SUM"]}` | `AssertionError` | [ ] 동일 파일 · [ ] FAIL |
| D-008 | **G1** 두 번 호출 | 두 `ValidationResult` 완전 동일 **(SC-3)** | `AssertionError` | [ ] `test_d_validate_board.py` · [ ] FAIL |
| D-009 *(P1·선택)* | **G1** | `find_blank_coords` → `((1,3),(2,2))` 0-based, row-major | `ImportError` | [ ] `test_d_find_blank_coords.py` · [ ] FAIL |

---

## Given 픽스처 (테스트 Arrange)

| 별칭 | 설명 | To Do |
|------|------|-------|
| **G1** | 문제정의 부록 — 빈칸 `(1,3)`, `(2,2)` (0-based) | [ ] `tests/conftest.py` 또는 픽스처 모듈에 정의 |
| **G_blank_0** | 4×4, `0` 없음 → `BLANK_COUNT` | [ ] 정의 |
| **G_dup** | 4×4, 1~16 중복 | [ ] 정의 |
| **G_line_bad** | 빈칸 0, 행 합 34·대각 1개 ≠34 (SC-2) | [ ] 정의 |

**G1 격자 (참고):**

```
16  3  2  13
 5 10 11   0
 9  6  0  12
 4 15 14   1
```

---

## RED 완료 시 체크 (공통)

각 ID마다 RED 보고 전 확인:

- [ ] 선언: `Phase: red | Layer: … | Track: … | ID: …`
- [ ] `tests/`만 변경 (`src/` 미수정)
- [ ] 한 테스트 = 한 실패 이유
- [ ] `python -m pytest tests/.../test_*.py -v` → **FAILED** 또는 **ImportError**
- [ ] skip / xfail / assert 완화 없음
- [ ] TDD RED 보고 작성 (다음: GREEN)

### pytest 예시

```powershell
# Logic — entity
python -m pytest tests/entity/test_d_blank_count.py -v

# Logic — control
python -m pytest tests/control/test_d_validate_board.py -v

# UI — boundary
python -m pytest tests/boundary/test_u_input_shape.py -v
```

---

## 추적성

| Mom Test / PRD | RED ID |
|----------------|--------|
| 20분 헤맴 → 즉시 판정 (SC-1) | D-007, D-008 |
| 10선·대각 누락 금지 (SC-2) | D-006, D-007c |
| 재현·회귀 (SC-3) | D-008 |
| 빈칸 2 (INV-02) | D-003, U-IN-03/04 |
| boundary E00x 전담 | U-IN-* ~ U-FLOW-* |

---

## 개정 이력

| 버전 | 날짜 | 변경 |
|------|------|------|
| 0.1 | 2026-06-04 | Boundary·Logic RED 설계표 To Do 초안 |

---

*끝.*
