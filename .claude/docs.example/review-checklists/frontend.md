# Frontend (React) 리뷰 체크리스트

> dev-frontend, code-reviewer 참조.
> 공통 체크리스트는 `@.claude/docs/review-checklists/common.md` 먼저 적용.

## strict mode 함정 ⚠️

ES6 모듈은 자동 strict — 미선언 변수에 할당하면 ReferenceError → 컴포넌트 마운트 실패 → **화면 빈 페이지**.

- [ ] **새 변수 선언 누락 없는가** — `let`/`const` 빠짐 없이
- [ ] **페어 변수 함께 선언했는가** — `_err`/`_warn` 같이 페어로 쓰는 패턴에서 한쪽만 추가하지 않았는가

## 백엔드 key vs UI label

백엔드가 보내는 컴포넌트 키와 UI 라벨이 다른 경우가 있음.

- [ ] 새 항목 추가 시 매핑이 한 곳에서만 일어나는가 (양쪽 등록은 죽은 코드 유발)
- [ ] `SensorErrorIconMapping` 등 변환 위치에서 일관적인가

## 장치 타입별 컴포넌트 분기

- [ ] 장치 타입별 별도 컴포넌트가 있는 경우 한쪽만 수정하지 않았는가
- [ ] 두 프론트엔드(frontend / op-frontend)에 동일 변경이 필요한지 확인했는가

## 빌드 산출물

- [ ] **dist/ 빌드 산출물이 diff에 들어있지 않은가** — `dist/app.bundle.js`, `*.map`
- [ ] 의도치 않게 들어갔으면 `git checkout -- [dist 경로]/`

## MobX

- [ ] `@inject('store') @observer` 데코레이터가 빠지지 않았는가
- [ ] store 직접 mutate가 아닌 action을 통한 변경인가
- [ ] dimension 등 레이아웃 관련 store update 시 window 크기 0 체크 가드가 있는가
