---
name: magic-square-tdd
description: MagicSquare_1004 Dual-Track TDD·ECB 개발 시 Agent가 따를 절차. validate_board·D-*/U-* 테스트·entity/control/boundary 구현·RED/GREEN/REFACTOR·pytest 회귀 시 적용.
---

# MagicSquare Dual-Track TDD · ECB

`.cursorrules`, `docs/PRD.md`, [`reference.md`](reference.md) 와 함께 사용한다.

## 언제 이 Skill을 켜는지

| 트리거 | 예 |
|--------|-----|
| TDD 사이클 | RED / GREEN / REFACTOR, “테스트 먼저”, “한 사이클” |
| Dual-Track | Logic Track(D-*), UI Track(U-*), `test_d_*`, `test_u_*` |
| ECB Layer | `entity` / `control` / `boundary` 구현·리팩터 |
| Phase 1 Command | `validate_board`, `find_blank_coords`, INV·Rule ID |
| 회귀·리뷰 | pytest 전체/부분, SC-1~3, Refactor 후 검증 |

**끄기(적용 안 함):** Harness만, Mom Test·문서만, Solver/GUI 일괄 구현, 사용자가 “본문 작성 금지” 명시.

---

## 작업 시작 선언 (필수)

한국어로 한 줄 출력:

```
Phase {N} · Layer {entity|control|boundary} · Track {Logic|UI} · {RED|GREEN|REFACTOR} · {D-xxx|U-xxx}
```

---

## Logic Track vs UI Track

| | **Logic Track** | **UI Track** |
|---|-----------------|--------------|
| **Layer** | entity, control | boundary |
| **테스트 ID** | **D-*** | **U-*** |
| **파일명** | `test_d_*.py` | `test_u_*.py` |
| **위치** | `tests/entity/`, `tests/control/` | `tests/boundary/` |
| **Mock** | **도메인 Mock 금지** — 실 Rule·실 객체 | **Mock 허용** — control·I/O stub |
| **검증 대상** | INV, Rule ID, 판정 계약 | E001~E007, 입출력·메시지 |
| **상수** | MagicConstant SSOT (`34`/`16` 리터럴 금지) | boundary는 상수 **참조만** |

---

## ECB · Mock · E001~E007

### 의존 방향

```
boundary → control → entity
```

| Layer | **허용** | **금지** |
|-------|----------|----------|
| **entity** | 순수 Rule, INV, MagicConstant | `control`/`boundary` import; **E001~E005** 처리·변환·매핑; I/O |
| **control** | entity 호출, 흐름 조율, ValidationResult 조립 | boundary import; E001~E007 **발생**; entity 우회 판정 |
| **boundary** | E001~E007, 입력 검증, 사용자 메시지, control 호출 | entity **직접** import; 도메인 Rule 중복 구현 |

### 오류 코드

| 코드 | 담당 | entity | control | boundary |
|------|------|:------:|:-------:|:--------:|
| E001~E005 | 입력·형식·범위 | ❌ | ❌ 발생 | ✅ |
| E006~E007 | I/O·표시 | ❌ | ❌ | ✅ |
| Rule ID (`BLANK_COUNT` 등) | 도메인 판정 | ✅ | ✅ 조립 | ❌ (번역만) |

### Mock 규칙

- **Logic:** `MagicSquare`, grid, Rule 로직 **Mock/stub/patch 금지**
- **UI:** boundary 테스트에서 control·stdin/stdout **Mock 허용**
- **공통 금지:** `@pytest.mark.skip`, `xfail`, assert 완화, “일단 통과” 더미

---

## RED (5~7단계)

1. **선언** — Phase · Layer · Track · RED · 대상 `D-*`/`U-*` ( [`reference.md`](reference.md) 확인).
2. **범위 확인** — PRD Phase·해당 Layer만; 다른 Layer 구현 선행 금지.
3. **픽스처** — Given(4×4 grid 또는 boundary 입력)을 **Mom Test·INV**에 연결해 명시.
4. **테스트 작성** — `test_d_*` 또는 `test_u_*`에 **하나의 실패 이유**만 assert.
5. **실행** — 아래 [Test/Review Loop](#testreview-loop) **RED 명령**; **실패 확인**(ImportError·AssertionError OK).
6. **금지 점검** — skip/xfail/완화 assert·Logic Track Mock 없음.
7. **기록** — 실패 메시지·기대 Rule ID/E00x를 완료 보고에 남길 준비.

---

## GREEN (5~7단계)

1. **선언** — 동일 ID로 GREEN 전환.
2. **최소 구현** — **해당 테스트만** 통과하는 코드; 다른 Rule 선구현 금지.
3. **Layer 준수** — entity=Rule만, control=조율, boundary=E00x·I/O만.
4. **상수** — `34`/`16`/격자 크기는 MagicConstant **한 곳**에서만 추가·사용.
5. **실행** — **GREEN 명령**(해당 파일 → Layer → 전체 Logic/UI 순).
6. **통과 확인** — 대상 테스트 green; **기존 테스트 깨지면** 즉시 수정(완화 금지).
7. **완료 보고** — 아래 체크리스트 초안.

---

## REFACTOR (5~7단계)

1. **선언** — REFACTOR · 영향 Layer·Track 명시.
2. **전제** — 대상 GREEN 테스트 **이미 통과** 상태.
3. **허용 변경** — 이름·중복 제거·MagicConstant 추출·ECB 경계 정리; **관찰 가능한 동작 동일**.
4. **금지** — assert 삭제·완화, Rule 순서·의미 변경, cross-layer import 추가.
5. **실행** — **REFACTOR 명령**(해당 Track → `pytest` 전체).
6. **SC-3** — 동일 grid 두 번 호출 결과 동일(D-008 등).
7. **완료 보고** — 변경 요약·전체 green 여부.

---

## Test/Review Loop

프로젝트 루트에서 실행. **항상 실패를 확인한 뒤** 다음 단계.

| 시점 | 명령 | 목적 |
|------|------|------|
| **RED 직후** | `python -m pytest tests/{layer}/test_d_xxx.py -v` 또는 `test_u_xxx.py -v` | **새 테스트만** 실패 확인 |
| **GREEN 중** | 위 동일 파일 `-v` | 대상 green |
| **GREEN 후** | `python -m pytest tests/entity tests/control -v` (Logic) 또는 `tests/boundary -v` (UI) | **Track 회귀** |
| **REFACTOR 후** | `python -m pytest -v` | **전체** 회귀 (SC-3) |
| **Layer 완료** | `python -m pytest tests/{layer}/ -v` | Layer 단위 리뷰 |
| **PR/세션 종료** | `python -m pytest -v --tb=short` | 최종 Review Loop |

**Logic Track** 작업 중 UI 테스트 실패 시: boundary **미착수**면 U-*는 **별도 이슈**로 기록, Logic 우선 완료 후 UI 사이클.

**금지:** green 확인 없이 REFACTOR; 전체 pytest 생략하고 “통과했다”고 보고.

---

## 완료 보고 항목

매 RED/GREEN/REFACTOR 종료 시 한국어로:

```markdown
## TDD 완료 보고

- **선언:** Phase · Layer · Track · 단계 · ID
- **변경 파일:** (목록)
- **pytest:** (실행한 명령 + passed/failed 수)
- **Rule / 오류:** 위반 Rule ID 또는 E00x (해당 시)
- **Mock 사용:** 없음(Logic) / stub 목록(UI)
- **ECB 위반:** 없음 / (있으면 수정)
- **다음:** (다음 D-* 또는 U-*)
```

**git commit/push:** 사용자 **명시 요청 시에만**.

---

## 추가 참고

- D-* 테스트 ID 목록: [`reference.md`](reference.md)
- 도메인 SSoT: `docs/PRD.md`, `Report/01.*`, `Report/02.*`
