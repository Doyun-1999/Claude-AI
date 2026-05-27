# [YOUR_APP_NAME] (Kotlin + Compose) — 프로젝트 컨텍스트

> dev-android-kotlin 참조.

## 기본 정보

| 항목 | 값 |
|---|---|
| 앱명 | [앱 이름] |
| 경로 | `/Users/[USERNAME]/Project/[AppName]` |
| 패키지명 | `com.[yourname].[appname]` |
| 언어 | Kotlin 전용 (Java 혼용 금지) |
| UI | Jetpack Compose (XML 레이아웃 사용 금지) |

## 기술 스택

| 분류 | 라이브러리 |
|---|---|
| UI | Jetpack Compose + Material3 |
| 상태관리 | ViewModel + StateFlow + collectAsState |
| DI | Hilt |
| 네트워크 | Retrofit2 + OkHttp3 + kotlinx.serialization |
| 로컬 DB | Room |
| 비동기 | Kotlin Coroutines + Flow |
| 네비게이션 | Navigation Compose |

## 아키텍처 — Clean MVVM

```
UI Layer (Compose Screen)
  └── ViewModel (StateFlow 상태 노출)
        └── Repository (단일 진실 공급원)
              ├── RemoteDataSource (Retrofit → 외부 API)
              └── LocalDataSource (Room → 로컬 캐시)
```

## 디렉토리 구조

```
com.[yourname].[appname]/
├── ui/
│   ├── [feature]/
│   │   ├── [Feature]Screen.kt
│   │   └── [Feature]ViewModel.kt
│   └── theme/
├── data/
│   ├── remote/
│   │   ├── ApiService.kt
│   │   └── dto/
│   ├── local/
│   │   ├── AppDatabase.kt
│   │   └── [Feature]Dao.kt
│   └── repository/
├── domain/
│   └── model/
└── di/
    └── AppModule.kt
```

## 외부 API

**Base URL:** `[API_BASE_URL]` — `local.properties`의 `API_KEY`로 인증

## 관련 docs

- 코드 컨벤션: `@.claude/docs/conventions/android-kotlin-compose.md`
