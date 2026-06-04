# TDD RED — 실패 테스트 먼저

MagicSquare_1004 Dual-Track TDD · ECB — **RED 단계만**. 구현(`src/`)은 GREEN에서.

`.cursorrules`, `docs/PRD.md`, `.cursor/skills/magic-square-tdd/reference.md` (D-* ID) 참고.

---

## 필수 선언

**응답 첫 줄** (한국어, 이 형식 고정):

```
Phase: red | Layer: {entity|control|boundary} | Track: {Logic|UI} | ID: {D-xxx|U-xxx}
```

| Track | Layer | 테스트 ID | 파일 |
|-------|-------|-----------|------|
| Logic | entity, control | **D-*** | `tests/{layer}/test_d_*.py` |
| UI | boundary | **U-*** | `tests/boundary/test_u_*.py` |

---

## 절차

1. **ID 확인** — `reference.md` 또는 사용자 지정 D-*/U-* 하나 선택. 이미 green인 ID 재사용 금지(새 assert 추가 시 새 ID).
2. **범위** — PRD Phase·해당 Layer만. 한 테스트 = **한 실패 이유**.
3. **AAA 테스트 작성** — `tests/` 아래만 수정.
   - **Arrange:** 4×4 grid 또는 boundary 입력 (Given·INV·Mom Test 연결).
   - **Act:** import 대상 호출 *(아직 없으면 ImportError로 RED OK)*.
   - **Assert:** Rule ID / ValidationResult / E00x **하나** — `34`/`16` 리터럴 대신 MagicConstant 또는 픽스처 값.
4. **pytest FAIL** — 아래 bash 실행. **FAILED** 또는 **ImportError** 확인 필수.
5. **금지 점검** — §금지 항목 위반 없음.
6. **보고** — §보고 형식 출력. **GREEN·REFACTOR·src/ 수정 하지 않음.**

---

## pytest 예시 (bash)

```bash
# Logic — entity (D-003 예)
python -m pytest tests/entity/test_d_blank_count.py -v

# Logic — control (D-007 예)
python -m pytest tests/control/test_d_validate_board.py::test_d007_structural_violation -v

# UI — boundary (U-001 예)
python -m pytest tests/boundary/test_u_input_shape.py -v

# Layer 전체 (RED 확인 — 새 테스트만 fail 기대)
python -m pytest tests/entity/ -v
```

**RED 성공 기준:** 대상 테스트 **1건 이상 FAILED** (또는 모듈 **ImportError**). 전부 passed면 RED **미완** — assert·Given 강화 또는 미구현 API 확인.

---

## 보고

```markdown
## TDD RED 보고

- **선언:** Phase: red | Layer: … | Track: … | ID: …
- **테스트 ID:** D-xxx / U-xxx
- **pytest FAIL 요약:** (한 줄 — AssertionError / ImportError / 메시지)
- **변경 파일:** tests/… 만 (목록)
- **다음:** GREEN (`/tdd-green` 또는 사용자 요청)
```

---

## 금지

| 금지 | 이유 |
|------|------|
| **`src/` 수정** | GREEN 담당 |
| **Logic Track Domain Mock** | entity/control Rule·grid stub/patch 금지 |
| **assert 완화·삭제** | RED는 실패가 목표 |
| **`skip` / `xfail`** | 우회 금지 |
| **한 파일에 여러 ID 혼합** | ID 1:1 유지 |
| **GREEN·REFACTOR 선행** | RED 보고 전 구현 금지 |

UI Track(boundary)만 control·I/O **Mock 허용**. Logic Track은 Mock **금지**.
