# [YOUR_HMI_PROJECT] — 임베디드 HMI 프로젝트 컨텍스트

> dev-frontend, code-reviewer 참조.

## 작업 범위

✅ **만지는 곳**
- `modules/[hmi]/frontend/src/` — 일반 HMI 프론트엔드 (port [PORT_A])
- `modules/[hmi]/op-frontend/src/` — 운영자 HMI 프론트엔드 (port [PORT_B])

❌ **만지지 않는 곳**
- `modules/[hmi]/backend/` (C++) — 별도 에이전트 또는 협의 필요
- `docker/`, 빌드 설정 파일
- `dist/` 빌드 산출물 (자동 생성)

## 경로

| 환경 | 경로 |
|---|---|
| 로컬 (Mac) | `/Users/[USERNAME]/Project/[project]` |
| 임베디드 장치 | `/home/[user]/[project_path]` |
| 도커 컨테이너 안 | `/[project]` |

## 스택

- **React** (class components 패턴)
- **MobX** (`@inject('store') @observer` 데코레이터)
- **Webpack** — `webpack.config.js` 설정
- **Proto** — `proto_bundle/`에 백엔드 proto 정의 번들
- **WebSocket** — 백엔드와 단방향 push, `store/websocket/websocket_realtime.js`가 라우팅 허브

## 두 프론트엔드 차이

| | `frontend/` | `op-frontend/` |
|---|---|---|
| 포트 | [PORT_A] | [PORT_B] |
| 용도 | 개발자/엔지니어 HMI | 운영자 HMI |
| 모드 dropdown | `Header/HMISelectors.js`의 `<Selector>` | `Modes/index.js`의 버튼 리스트 |
| 장치 분기 | `currentMode.includes()` 기반 | `isDeviceTypeA` 기반 |

## 핵심 파일 인덱스

### op-frontend

```
src/
├── components/
│   ├── ModuleController/
│   │   ├── index.js                    # 모듈 상태 표시
│   │   └── StatusDisplay.js            # 센서 상태 아이콘
│   ├── Modes/index.js                  # 모드/장치/맵 dropdown
│   └── Dreamview.js                    # 최상위 라우팅
└── store/
    ├── hmi.js                          # HMIStatus 받아 상태 저장
    └── websocket/websocket_realtime.js # WS 메시지 라우터
```

## 데이터 흐름 (모드 dropdown 예)

```
[Backend C++ — hmi_worker.cc]
   status_.add_modes(mode)
        │ (websocket push)
        ▼
[WS 핸들러: websocket_realtime.js]
   case 'HMIStatus' → store.hmi.updateStatus(message)
        │
        ▼
[Store: hmi.js]
   this.modes = newStatus.modes.sort()
        │
        ▼
[컴포넌트 렌더]
   frontend  → Header/HMISelectors.js
   op-front  → Modes/index.js
```

## 관련 docs

- 코드 패턴 / 함정: `@.claude/docs/conventions/react-mobx.md`
- 빌드 & 실행 풀체인: `@.claude/docs/infra/embedded-docker.md`
