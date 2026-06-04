# Magic Square 4×4 — 제품 요구사항 (PRD)

| 항목 | 내용 |
|------|------|
| 프로젝트 | MagicSquare_xx |
| 버전 | 0.1 (초안) |
| 작성일 | 2026-06-04 |
| 문서 상태 | 초안 |
| 문제 정의 | [`Report/01.MagicSquare_ProblemDefinition_Report.md`](../Report/01.MagicSquare_ProblemDefinition_Report.md) |
| Mom Test | [`Report/01.REPORT.md`](../Report/01.REPORT.md) |

---

## 1. 배경 · Mom Test

### 1.1 페르소나

4×4 격자, **빈칸 2개(`0`)**, **1~16**, **10선 합 34** 맞추는 **학습자**.

### 1.2 진짜 문제 (한 문장)

부분적으로 채워진 4×4 격자가 **10선·34·빈칸 2·1~16** 규칙을 만족하는지, 손이든 코드든 **같은 기준으로 빠짐없이 판정**하고 다시 확인할 때마다 **시간과 확신**이 계속 깎인다.

**Mom Test 증거:** *“지난번에 빈칸 2개 넣었다가 34가 안 맞아서 **20분** 헤맸다.”*

### 1.3 제품 방향 (솔루션 최소화)

1차 목표는 **“완성 프로그램”** 이 아니라 **반복 가능한 판정 계약**이다.  
해 자동 채우기·GUI·전체 ECB 스택은 **후속 Phase**.

---

## 2. 목표 · 비목표

### 2.1 목표 (Phase 1 — 세션 3)

| ID | 목표 |
|----|------|
| **G-01** | 4×4 보드에 대해 **Rule(INV)** 기반 **판정** 제공 |
| **G-02** | 실패 시 **어느 Rule/선** 위반인지 반환 |
| **G-03** | **Test Loop**로 판정 **회귀 보호** (SC-1~3) |

### 2.2 비목표 (표면 문제 — 하지 않음)

| ID | 비목표 | 이유 |
|----|--------|------|
| **OOS-01** | “마방진 **완성 앱**” | Mom Test 표면 문제 |
| **OOS-02** | **Solver** / 빈칸 자동 채우기 1차 | 판정·확신이 먼저 |
| **OOS-03** | **GUI** (GridUI 등) | Phase 1 Output 아님 |
| **OOS-04** | **ECB 전체**·N×N 일반화 | 범위 초과 |
| **OOS-05** | TDD/ECB를 **제품 목표**로 기재 | 방법론 ≠ 사용자 고통 |

---

## 3. 도메인 규칙

### 3.1 용어

| 용어 | 정의 |
|------|------|
| **격자** | `4×4` 정수 배열 |
| **빈칸** | 값 **`0`** |
| **10선** | 행 4 + 열 4 + **주대각 2** (합 검사 대상) |
| **마법 합** | **34** |
| **완성 격자** | 빈칸 0, 1~16 각 1회, 10선 합 34 |

### 3.2 Invariant (SSoT)

| ID | 규칙 |
|----|------|
| **INV-01** | `len(grid)==4`, 각 행 길이 4 |
| **INV-02** | **`0` 정확히 2개** |
| **INV-03** | `0` 제외 값 ∈ [1,16], **중복 없음** |
| **INV-04** | **10선** 각각의 합 = **34** (완성·판정 시) |
| **INV-05** | 실패 시 **violated_rules** 에 Rule ID 기록 |
| **INV-06** | 동일 입력 → 동일 판정 결과 |

### 3.3 10선 정의

```
행: (0,0)~(0,3), (1,0)~(1,3), (2,0)~(2,3), (3,0)~(3,3)
열: (0,0)~(3,0), … (0,3)~(3,3)
대각: (0,0)(1,1)(2,2)(3,3), (0,3)(1,2)(2,1)(3,0)
```

---

## 4. R-G-I-O (Phase 1)

| | 내용 |
|---|---|
| **Role** | 학습자 / 호출자 — 부분 보드 **판정** 필요 |
| **Goal** | SC-1~3 충족하는 **validate_board** |
| **Input** | `grid: list[list[int]]` — 4×4 |
| **Output** | `ValidationResult`: `{ ok: bool, violated_rules: list[str] }` |

---

## 5. 기능 · Command (Phase 1)

### 5.1 `validate_board(grid) -> ValidationResult`

**우선순위:** P0 (세션 3 필수)

| 단계 | 검사 | Rule ID |
|------|------|---------|
| 1 | 형태 4×4 | `SHAPE_INVALID` |
| 2 | 빈칸 개수 = 2 | `BLANK_COUNT` |
| 3 | 범위 0 또는 1~16 | `VALUE_RANGE` |
| 4 | 0 제외 중복 | `DUPLICATE` |
| 5 | 10선 합 = 34 *(0 포함 선도 합산)* | `LINE_SUM` |

> **Note:** 부분 보드에서 `LINE_SUM` 실패는 **허용** (아직 미완성). Phase 1 정책은 **아래 §5.3** 참고.

### 5.2 `find_blank_coords(grid) -> tuple[tuple[int,int], tuple[int,int]]` *(선택 P1)*

- **INV-02** 보조: `0` 두 좌표, **row-major** (0-based).
- 빈칸 ≠ 2 → `BLANK_COUNT` 예외.

### 5.3 Phase 1 판정 정책 (초안)

| 모드 | 설명 |
|------|------|
| **strict** | INV-01~04 **전부** 만족해야 `ok=true` |
| **structural** *(기본)* | INV-01~03만 검사; `LINE_SUM`은 **완성 격자**(빈칸 0)일 때만 |

**Mom Test 연결:** 학습자는 “34 안 맞음”으로 **20분** 헤맸으므로, **완성 후** `LINE_SUM` + **어느 선** 위반인지가 SC-2 핵심.

**초안 기본:** `structural` + 빈칸 0개일 때 **10선** 검사. *(구현 전 팀 확정 가능)*

---

## 6. 입출력 · 오류 계약

### 6.1 ValidationResult

```python
{
  "ok": bool,
  "violated_rules": ["BLANK_COUNT", "LINE_SUM", ...]  # ok=true 이면 []
}
```

### 6.2 LINE_SUM 상세 *(Phase 1.1)*

`violated_rules`에 `LINE_SUM` 포함 시, 선택적으로:

```python
"failed_lines": ["row:1", "diag:main", ...]
```

### 6.3 예외 (Boundary, 후속)

| 코드 | 조건 |
|------|------|
| `SHAPE_INVALID` | 4×4 아님 |
| `BLANK_COUNT` | `0` ≠ 2 |
| `VALUE_RANGE` | 허용 밖 값 |
| `DUPLICATE` | 1~16 중복 |
| `LINE_SUM` | 10선 중 하나라도 ≠ 34 |

---

## 7. 성공 기준 (수용)

| ID | Given | When | Then | Mom Test |
|----|-------|------|------|----------|
| **SC-1** | 알려진 위반 픽스처 | `validate_board` | **1초 이내** fail + Rule ID | 20분 → 즉시 판정 |
| **SC-2** | 행만 34, 대각 틀림 | `validate_board` | `ok=false`, `LINE_SUM` | 10선 누락 방지 |
| **SC-3** | 동일 grid 두 번 | `validate_board` | 동일 결과; refactor 후 pytest green | 재현·회귀 |

---

## 8. Test Loop (Phase 1)

```
Red   → Rule별 실패 테스트 (BLANK_COUNT, DUPLICATE, LINE_SUM, 정상 1건)
Green → validate_board 최소 구현
Refactor → Rule 상수·메시지 정리, SC-3 유지
```

**산출:** `tests/test_validate_board.py` (또는 동등 경로)

---

## 9. 비기능 (NFR)

| ID | 요구 |
|----|------|
| **NFR-01** | Domain 판정 로직 **pytest** 100% 경로 (Phase 1) |
| **NFR-02** | Rule ID ↔ 테스트 **1:1 추적** |
| **NFR-03** | PRD ↔ Problem Definition **동기** (SSoT: 본 PRD, 서술: Report) |

---

## 10. Phase 로드맵 (초안)

| Phase | 범위 | 산출 |
|-------|------|------|
| **1** (세션 3) | Rule, Command, Test Loop | `validate_board`, tests |
| **2** | `find_blank_coords`, structural 계약 확정 | 좌표 API |
| **3** | Solver, `solution()` | 빈칸 2 해 |
| **4** | Boundary, GUI | GridUI, 입력 검증 |

---

## 11. 추적성

| Mom Test | PRD |
|----------|-----|
| 20분 헤맴 | SC-1, G-01 |
| 10선·34 | INV-04, §3.3 |
| 빈칸 2 | INV-02 |
| 표면(솔버 앱) | §2.2 OOS |
| 재현·확신 | INV-06, SC-3, §8 |

---

## 12. 개정 이력

| 버전 | 날짜 | 변경 |
|------|------|------|
| 0.1 | 2026-06-04 | Mom Test·세션 3 초안 — Problem Definition Report와 동시 생성 |

---

*끝.*
