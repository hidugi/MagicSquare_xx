# Golden Master — GREEN PASS 기준

| 항목 | 내용 |
|------|------|
| 프로젝트 | MagicSquare_xx |
| 갱신일 | 2026-06-04 |
| 현재 체크포인트 | **D-LOC-01** entity GREEN PASS |

**목적:** GREEN 통과 시점의 **관찰 가능한 출력**을 JSON으로 고정해, 이후 REFACTOR·회귀에서 **Golden Master vs 실제** 비교 기준으로 쓴다.

---

## 1. Golden Master 파일

| Test ID | Golden 파일 | When | Then (1-index, row-major) |
|---------|-------------|------|---------------------------|
| **D-LOC-01** | [`tests/golden/d_loc_01_g1.json`](../tests/golden/d_loc_01_g1.json) | `find_blank_coords(G1)` | `[[2,4],[3,3]]` |
| **D-SOL-01** | [`tests/golden/d_sol_01_g1_step_a.approved.txt`](../tests/golden/d_sol_01_g1_step_a.approved.txt) | `solve_step_a(G1)` | `SUCCESS` + int[6] `2 4 8 3 3 7` |

0-based 참고: `[[1,3],[2,2]]` (PRD §5.2·문제정의 부록).

---

## 2. GREEN PASS 확인 명령

```powershell
cd c:\DEV\MagicSquare_xx
.\.venv\Scripts\Activate.ps1
python -m pytest tests/entity/test_d_loc_01.py -v
```

**D-SOL-01 Golden 갱신 / 검증:**

```powershell
$env:UPDATE_GOLDEN="1"
python -m pytest tests/entity/test_d_sol_01.py::test_d_sol_01_step_a_success -v
Remove-Item Env:UPDATE_GOLDEN
python -m pytest tests/entity/test_d_sol_01.py::test_d_sol_01_step_a_success -v
```

**PASS 기준:** `1 passed`, 실패 0.

시스템 Python 사용 시에도 동일 경로·`pyproject.toml` (`pythonpath=src`, `--import-mode=importlib`) 적용.

---

## 3. 체크포인트 이력

| Phase | Layer | Track | ID | 상태 | 커밋 *(로컬)* |
|-------|-------|-------|-----|------|---------------|
| green | entity | Logic | D-LOC-01 | **PASS** | *(미커밋 — 사용자 요청 시)* |

---

## 4. 다음 Golden Master 후보

| ID | Golden *(예정)* | 선행 |
|----|-----------------|------|
| D-LOC-02 | `d_loc_02_blank_count_zero.json` | GREEN |
| D-LOC-03 | `d_loc_03_blank_count_three.json` | GREEN |

---

*끝.*
