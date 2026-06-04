# MagicSquare_xx

4×4 **부분 마방진** — Mom Test로 문제를 고정하고, **Rule · Command · Test Loop**로 **판정 계약**을 구현하는 학습·TDD 프로젝트.

| 항목 | 내용 |
|------|------|
| 격자 | **4×4** |
| 숫자 | **1~16** (빈칸 **`0` 정확히 2개**) |
| 검사 | **10선**(행 4 + 열 4 + 주대각 2) 합 **34** |
| Phase 1 | `validate_board` + Dual-Track pytest |
| RED To Do | [`docs/TDD-RED-TODO.md`](docs/TDD-RED-TODO.md) (상세 설계표) |
| PRD | [`docs/PRD.md`](docs/PRD.md) |

---

## 한 줄 요약

**“마방진 앱을 만든다”가 아니라**, 부분 채워진 보드가 **10선·34·빈칸 2** 규칙을 지키는지 **같은 기준으로 빠짐없이 판정**할 수 있게 한다.

**Mom Test 근거:** *“지난번에 빈칸 2개 넣었다가 34가 안 맞아서 20분 헤맸다.”*

---

## 도메인 규칙 (요약)

| ID | 규칙 |
|----|------|
| INV-01 | 4×4 격자 |
| INV-02 | **`0` = 빈칸, 정확히 2개** |
| INV-03 | 그 외 **1~16**, 중복 없음 |
| INV-04 | **10선** 각 합 **= 34** (완성·판정 시) |

예시 (빈칸 2, 합=34):

| 16 | 3 | 2 | 13 |
|:---:|:---:|:---:|:---:|
| 5 | 10 | 11 | **0** |
| 9 | 6 | **0** | 12 |
| 4 | 15 | 14 | 1 |

---

## 프로젝트 구조

```
MagicSquare_xx/
├── README.md
├── pyproject.toml            # pytest Harness
├── src/
│   ├── entity/               # Rule, MagicConstant
│   ├── control/              # validate_board
│   └── boundary/             # E001~E007
├── tests/
│   ├── entity/               # test_d_*.py (Logic)
│   ├── control/
│   └── boundary/             # test_u_*.py (UI)
├── docs/
│   ├── PRD.md
│   └── TDD-RED-TODO.md       # RED 설계·체크리스트 (SSoT)
└── Report/
    ├── 01.MagicSquare_ProblemDefinition_Report.md
    ├── 01.REPORT.md
    └── 02.REPORT.md          # ECB Harness
```

> **현재 상태:** ECB Harness 준비 완료 · **RED 단계 진행 중** (아래 체크리스트). RED에서는 `tests/`만 수정, `src/`는 GREEN.

---

## 문서 읽는 순서

1. [`Report/01.REPORT.md`](Report/01.REPORT.md) — Mom Test 인터뷰·진짜/표면 문제  
2. [`Report/01.MagicSquare_ProblemDefinition_Report.md`](Report/01.MagicSquare_ProblemDefinition_Report.md) — Invariant, R-G-I-O, 세션 3 범위  
3. [`docs/PRD.md`](docs/PRD.md) — API·오류 코드·Phase 로드맵·수용 기준  
4. [`docs/TDD-RED-TODO.md`](docs/TDD-RED-TODO.md) — RED 설계표·Given·추적성  

---

## TDD RED 체크리스트

상세 Given·기대값·Expected Failure는 [`docs/TDD-RED-TODO.md`](docs/TDD-RED-TODO.md) 참고.

**RED 규칙:** `tests/`만 수정 · Logic Track Domain Mock 금지 · UI Track control/I/O Mock 허용 · 대상 테스트 **FAILED** 또는 **ImportError** 확인.

### 진행 순서

- [ ] **1.** Logic — `D-001` MagicConstant RED → GREEN
- [ ] **2.** Logic — `D-002`~`D-006` entity Rule RED → GREEN
- [ ] **3.** Logic — `D-007`~`D-008` control `validate_board` RED → GREEN
- [ ] **4.** Logic *(선택 P1)* — `D-009` `find_blank_coords` RED → GREEN
- [ ] **5.** Boundary — `U-IN-*` 입력 검증 RED → GREEN
- [ ] **6.** Boundary — `U-OUT-*` · `U-FLOW-*` RED → GREEN

### 사전 준비 — Given 픽스처

- [ ] **G1** — 문제정의 부록 격자 (빈칸 `(1,3)`, `(2,2)` 0-based)
- [ ] **G_blank_0** — `0` 없음 → `BLANK_COUNT`
- [ ] **G_dup** — 1~16 중복
- [ ] **G_line_bad** — 빈칸 0, 행 OK·대각 NG (SC-2)

### Logic Track — Entity (`tests/entity/test_d_*.py`)

- [ ] **D-001** — `test_d_magic_constant.py` · MagicConstant `34`/`4`/`16` · FAIL 확인
- [ ] **D-002** — `test_d_shape.py` · `3×4` → `SHAPE_INVALID` · FAIL 확인
- [ ] **D-003** — `test_d_blank_count.py` · 빈칸 `0` **0개** → `BLANK_COUNT` · FAIL 확인
- [ ] **D-003b** — 동일 파일 · 빈칸 `0` **3개** → `BLANK_COUNT` · FAIL 확인
- [ ] **D-004** — `test_d_value_range.py` · 셀 `17` → `VALUE_RANGE` · FAIL 확인
- [ ] **D-005** — `test_d_duplicate.py` · 중복 `5` → `DUPLICATE` · FAIL 확인
- [ ] **D-006** — `test_d_line_sum.py` · 완성 격자·대각 틀림 → `LINE_SUM` (SC-2) · FAIL 확인
- [ ] **D-006b** — 동일 파일 · 부분 보드 **G1** · structural 시 `LINE_SUM` 미검사 · FAIL 확인

### Logic Track — Control (`tests/control/test_d_*.py`)

- [ ] **D-007** — `test_d_validate_board.py` · **G1** → `{ok: true, violated_rules: []}` · FAIL 확인
- [ ] **D-007b** — 동일 파일 · **G_blank_0** → `BLANK_COUNT` · FAIL 확인
- [ ] **D-007c** — 동일 파일 · **G_line_bad** → `LINE_SUM` (SC-2) · FAIL 확인
- [ ] **D-008** — 동일 파일 · **G1** 두 번 호출 → 동일 결과 (SC-3) · FAIL 확인
- [ ] **D-009** *(선택)* — `test_d_find_blank_coords.py` · **G1** → `((1,3),(2,2))` · FAIL 확인

### Boundary Track — UI (`tests/boundary/test_u_*.py`)

- [ ] **U-IN-01** — `grid=None` → `E003 INVALID_NULL` · control 미호출 · FAIL 확인
- [ ] **U-IN-02** — `grid=3×4` → `E001 INVALID_SIZE` · FAIL 확인
- [ ] **U-IN-03** — 빈칸 `0` **0개** → `E002 INVALID_BLANKS` · FAIL 확인
- [ ] **U-IN-04** — 빈칸 `0` **3개** → `E002 INVALID_BLANKS` · FAIL 확인
- [ ] **U-IN-05** — 셀 `17`/`-1` → `E004 INVALID_VALUE` · FAIL 확인
- [ ] **U-IN-06** — 비정수 셀 → `E005 INVALID_TYPE` · FAIL 확인
- [ ] **U-OUT-01** — **G1** 유효 입력 → control에 `ok` 전달 · FAIL 확인
- [ ] **U-OUT-02** — **G_dup** → 메시지에 `DUPLICATE`/E 매핑 · FAIL 확인
- [ ] **U-FLOW-01** — `grid=None` → `validate_board` **0회** · FAIL 확인
- [ ] **U-FLOW-02** — `E001` 입력 → control **0회** · FAIL 확인

### RED 완료 시 (ID마다)

- [ ] 선언: `Phase: red | Layer: … | Track: … | ID: …`
- [ ] `tests/`만 변경 (`src/` 미수정)
- [ ] 한 테스트 = 한 실패 이유 · skip/xfail/assert 완화 없음
- [ ] `python -m pytest tests/.../test_*.py -v` → **FAILED** 또는 **ImportError**
- [ ] TDD RED 보고 후 GREEN 진행

```powershell
python -m pytest tests/entity/test_d_blank_count.py -v
python -m pytest tests/control/test_d_validate_board.py -v
python -m pytest tests/boundary/test_u_input_shape.py -v
```

---

## Phase 로드맵

| Phase | 범위 | 산출 |
|-------|------|------|
| **1** *(현재)* | Rule, Command, Test Loop | `validate_board`, `tests/{entity,control,boundary}/test_*` |
| **2** | 빈칸 좌표 | `find_blank_coords` |
| **3** | 해 탐색 | `solution()` / Solver |
| **4** | 경계·UI | Boundary, GridUI |

### Phase 1 — 하지 않는 것

- 마방진 **완성 앱** / **Solver** / **GUI** / **ECB 전체** (Mom Test **표면 문제**)

---

## Phase 1 목표 (구현 시)

| Command | 설명 |
|---------|------|
| `validate_board(grid)` | INV 기반 판정 → `{ ok, violated_rules[] }` |

**성공 기준 (PRD SC-1~3):**

- 위반 픽스처 **수 초 이내** 판정 (20분 헤맴 대체)
- **10선** 누락 없이 검사 (행만 맞고 통과 금지)
- Refactor 후에도 **동일 Input → Output** (pytest 회귀)

**Test Loop:** Red → Green → Refactor — [`docs/PRD.md` §8](docs/PRD.md) · RED 목록은 [위 체크리스트](#tdd-red-체크리스트)

---

## 실행 방법

```powershell
cd c:\DEV\MagicSquare_xx
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
python -m pytest -v
```

Harness만 있을 때는 **0 tests collected** 가 정상이다. RED 테스트 추가 후에는 해당 파일이 **FAILED** 또는 **ImportError** 여야 RED 완료다.

---

## 관련 링크

| 문서 | 용도 |
|------|------|
| [PRD](docs/PRD.md) | 입·출력, 오류 코드, NFR |
| [TDD RED To Do](docs/TDD-RED-TODO.md) | Boundary·Logic RED 설계표 (SSoT) |
| [문제 정의 보고서](Report/01.MagicSquare_ProblemDefinition_Report.md) | Why, Invariant, 8계층(세션 3) |
| [Harness 보고서](Report/02.REPORT.md) | ECB·Dual-Track·pytest 골격 |
| [Mom Test 보고서](Report/01.REPORT.md) | 인터뷰·증거·채점 |
| [Prompt Export](Prompting/01.REPORT-Prompt.md) | Cursor 대화 기록 |

---

## 라이선스

*(미정)*
