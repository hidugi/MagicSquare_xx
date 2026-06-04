# MagicSquare_xx

4×4 **부분 마방진** — Mom Test로 문제를 고정하고, **Rule · Command · Test Loop**로 **판정 계약**을 구현하는 학습·TDD 프로젝트.

| 항목 | 내용 |
|------|------|
| 격자 | **4×4** |
| 숫자 | **1~16** (빈칸 **`0` 정확히 2개**) |
| 검사 | **10선**(행 4 + 열 4 + 주대각 2) 합 **34** |
| Phase 1 | `validate_board` + pytest (구현 예정) |
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
├── README.md                 # 본 파일
├── docs/
│   └── PRD.md                # 제품 계약 (SSoT)
├── Report/
│   ├── 01.MagicSquare_ProblemDefinition_Report.md  # 문제 정의·Invariant·세션 3
│   └── 01.REPORT.md          # Mom Test STEP 1
└── Prompting/
    └── 01.REPORT-Prompt.md   # 개발 대화 Export
```

> **현재 상태:** 문서·문제 정의 단계. `src/`, `tests/` 는 Phase 1 구현 시 추가 예정.

---

## 문서 읽는 순서

1. [`Report/01.REPORT.md`](Report/01.REPORT.md) — Mom Test 인터뷰·진짜/표면 문제  
2. [`Report/01.MagicSquare_ProblemDefinition_Report.md`](Report/01.MagicSquare_ProblemDefinition_Report.md) — Invariant, R-G-I-O, 세션 3 범위  
3. [`docs/PRD.md`](docs/PRD.md) — API·오류 코드·Phase 로드맵·수용 기준  

---

## Phase 로드맵

| Phase | 범위 | 산출 |
|-------|------|------|
| **1** *(현재)* | Rule, Command, Test Loop | `validate_board`, `tests/test_validate_board.py` |
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

**Test Loop:** Red → Green → Refactor — [`docs/PRD.md` §8](docs/PRD.md)

---

## 실행 방법 *(Phase 1 구현 후)*

```powershell
cd c:\DEV\MagicSquare_xx
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install pytest
python -m pytest -v
```

구현 전에는 위 명령을 실행할 테스트·소스가 없습니다.

---

## 관련 링크

| 문서 | 용도 |
|------|------|
| [PRD](docs/PRD.md) | 입·출력, 오류 코드, NFR |
| [문제 정의 보고서](Report/01.MagicSquare_ProblemDefinition_Report.md) | Why, Invariant, 8계층(세션 3) |
| [Mom Test 보고서](Report/01.REPORT.md) | 인터뷰·증거·채점 |
| [Prompt Export](Prompting/01.REPORT-Prompt.md) | Cursor 대화 기록 |

---

## 라이선스

*(미정)*
