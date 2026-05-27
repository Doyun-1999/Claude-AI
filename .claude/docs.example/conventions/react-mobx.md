# React + MobX 코드 패턴 / 함정

> dev-frontend, code-reviewer 참조. 프로젝트 컨텍스트: `@.claude/docs/projects/embedded-hmi.md`

## 1. 변수 선언 누락 (strict mode) — 가장 큰 함정

ES6 모듈은 자동 strict — 미선언 변수에 할당하면 **ReferenceError → 컴포넌트 마운트 실패 → 화면 빈 페이지**.

### 패턴
`StatusDisplay.js`처럼 `_err`/`_warn` 변수 페어로 선언하는 패턴이 많음.

**새 센서 추가 시 양쪽 그룹 다 선언 추가 필수.**

> 과거 사례: 페어 변수 한 줄 선언 누락으로 화면 전체 마운트 실패한 사례 있음.

## 2. Backend key vs UI label 분리

백엔드 monitor가 보내는 컴포넌트 키와 UI에 표시하는 라벨이 다른 경우가 있음.

### 변환 위치
- `index.js`의 `SensorErrorIconMapping`
- `sensorError.js`의 case문

### 새 센서 추가 시
- Backend가 보내는 키가 무엇인지 확정
- UI 라벨이 무엇인지 확정
- 두 키 모두 매핑에 등록 vs 한 키만 + 어딘가에서 변환 — **둘 중 하나로 통일**
- 양쪽 다 등록은 죽은 코드 유발

## 3. 장치 타입별 별도 컴포넌트

장치 타입별 별도 컴포넌트가 존재하는 경우:
- `StatusDisplay.js` ↔ `StatusDisplayTypeA.js`

한쪽 수정 시 다른 쪽도 일관되게 바꿔야 하는지 **항상 확인**.

## 4. 빌드 산출물 커밋 주의

`dist/app.bundle.js`, `dist/app.bundle.js.map` 등이 git tracked인 경우가 있음.

의도치 않게 빌드 산출물이 diff에 들어가면:
```bash
git checkout -- [dist 경로]/
```

## 5. MobX 사용 규칙

- 클래스 컴포넌트에서 `@inject('store') @observer` 데코레이터로 store 주입
- store 직접 mutate가 아닌 action을 통한 변경
- `@observable`로 선언된 필드만 자동 리렌더 트리거
- dimension 등 레이아웃 store의 `update()`는 `window.innerWidth/Height === 0` 체크 후 실행 권장

## 6. WebSocket 메시지 라우팅

새 백엔드 메시지 type 핸들 추가 시 `store/websocket/websocket_realtime.js`가 진입점.
case 문 추가 후 적절한 store 메서드로 라우팅.

## 자가검증

체크리스트: `@.claude/docs/review-checklists/frontend.md`
