# Review ECB — 계약·아키텍처 리뷰 (읽기 전용)

MagicSquare_1004 Dual-Track TDD · ECB — **코드 수정 금지**. `src/`, `tests/` **변경·제안 패치·자동 수정 하지 않음**.

`.cursorrules`, `docs/PRD.md`, `.cursor/skills/magic-square-tdd/SKILL.md` 참고.

---

## 필수 선언

**응답 첫 줄:**

```
Phase: review | Mode: read-only | Scope: {src|tests|both|path}
```

---

## 절차

1. **범위 확인** — 사용자 지정 경로 또는 `src/`, `tests/` 전체 **읽기만**.
2. **체크 5항** — 아래 §체크리스트 기준으로 파일·import·테스트 스캔.
3. **위반만 표로 출력** — §보고 형식. **위반 없으면** “위반 없음” 한 줄 + 체크 통과 표.
4. **수정 금지** — refactor·GREEN·commit 제안은 **별도 사용자 요청** 시에만.

---

## 체크리스트 (5항)

| # | 항목 | 기준 | 위반 예 |
|---|------|------|---------|
| 1 | **import 방향** | `boundary → control → entity` 단방향 | entity가 control/boundary import; control이 boundary import; entity가 stdlib 외 상위 layer import |
| 2 | **entity E001~E005** | entity는 **Rule ID만** — E001~E005 문자열·처리·매핑·발생 **금지** | `E001` in entity; 입력 형식 검증 in entity |
| 3 | **int[6] 1-index** | 성공 출력 `[r1,c1,n1,r2,c2,n2]`, 행·열 **1~4** | 0-based 좌표 반환; 길이 ≠ 6; solver 출력 계약 불일치 |
| 4 | **MagicConstant SSOT** | `34`/`16`/격자 크기 **한 모듈**만 정의 | `src/`·`tests/`(Logic)에 `34`/`16` 리터럴 산재; MagicConstant 우회 상수 |
| 5 | **Logic Track Domain Mock** | `tests/entity/`, `tests/control/`, `test_d_*` — grid·Rule·entity **Mock/stub/patch 금지** | `@patch` on Rule; fake validator; MagicSquare stub in D-* |

**부가 관찰** (표에 포함, 별도 열): boundary만 E001~E007; UI Track `test_u_*` Mock 허용; skip/xfail/assert 완화.

---

## 스캔 힌트 (읽기만)

```bash
# import 방향 (수동 grep)
rg "^from (control|boundary)|^import (control|boundary)" src/entity/
rg "^from boundary|^import boundary" src/control/
rg "^from entity|^import entity" src/boundary/

# E001~E005 in entity
rg "E00[1-5]" src/entity/

# 리터럴 34/16 (Logic — MagicConstant 외)
rg "\b34\b|\b16\b" src/ tests/entity/ tests/control/

# Logic Mock
rg "patch|Mock|MagicMock|stub" tests/entity/ tests/control/
```

리뷰 결과에 **파일:줄** 근거를 적는다. 줄 번호 불명 시 `파일`만.

---

## 보고

**위반만** 아래 표에 기재. 수정안·코드 블록 **넣지 않음**.

```markdown
## ECB · 계약 리뷰

- **선언:** Phase: review | Mode: read-only | Scope: …
- **스캔 범위:** (파일·디렉터리 목록)

### 위반 목록

| # | 체크 | 심각도 | 위치 | 내용 |
|---|------|--------|------|------|
| 1 | import 방향 | 🔴/🟡 | `src/entity/foo.py:12` | entity → control import |
| … | … | … | … | … |

### 체크 요약

| # | 항목 | 결과 |
|---|------|------|
| 1 | import 방향 | ✅ / ❌ |
| 2 | entity E001~E005 | ✅ / ❌ |
| 3 | int[6] 1-index | ✅ / N/A |
| 4 | MagicConstant SSOT | ✅ / ❌ |
| 5 | Logic Domain Mock | ✅ / ❌ |

**총평:** (한 줄 — 위반 N건 / 없음)
```

- **심각도:** 🔴 계약·ECB 깨짐 · 🟡 경미·테스트만·N/A 해당 없음
- **N/A:** 해당 Layer·Phase에 아직 코드 없음 (예: solver·int[6] 미구현)

---

## 금지

| 금지 | 이유 |
|------|------|
| **파일 수정·생성·삭제** | read-only 리뷰 |
| **pytest 실행 후 코드 변경** | Review ≠ GREEN/REFACTOR |
| **위반 표 없이 “OK”만** | 5항 체크 요약 필수 |
| **스타일·네이밍만 장문 코멘트** | ECB·계약 위반만 |

위반 발견 시 **표로만** 보고. 사용자가 “고쳐줘” 요청할 때까지 구현하지 않음.
