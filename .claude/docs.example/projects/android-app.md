# [YOUR_APP_NAME] (Android) — 프로젝트 컨텍스트

> dev-android, dev-android-kotlin (참고용), code-reviewer 참조.

## 기본 정보

| 항목 | 값 |
|---|---|
| 경로 | `/Users/[USERNAME]/Project/[YOUR_APP]` |
| 패키지명 | `com.[company].[appname]` |
| compileSdk / minSdk / targetSdk | 35 / 24 / 35 |
| 현재 언어 | Java (Kotlin 마이그레이션 예정) |
| Kotlin 버전 | 2.0.x |
| AGP | 8.x.x |

## 아키텍처

**MVVM + Fragment 기반**

```
Activity
  └── Fragment (UI)
        └── ViewModel (LiveData 상태관리)
              └── NetworkApi / Repository (데이터)
                    └── RetrofitInterface (Retrofit API)
```

## 주요 디렉토리

```
app/src/main/java/com/[company]/[appname]/
├── new_ui/
│   ├── MainActivity.java             # 메인 진입점 (Fragment 호스트)
│   ├── fragment/                     # UI Fragment들
│   ├── model/
│   │   ├── viewModel/               # ViewModel 클래스들
│   │   ├── WAS/                     # API 응답 모델
│   │   ├── enums/                   # Enum 정의
│   │   └── info/                    # 데이터 홀더 클래스
│   ├── network/
│   │   ├── RetrofitInterface.java   # Retrofit API 인터페이스
│   │   ├── NetworkApi.java          # API 싱글톤 (CompletableFuture 기반)
│   │   └── NetworkHelper.java       # Retrofit + OkHttp 설정
│   └── service/                     # Android Service들
└── util/
    ├── Constants.java               # 상수 (서버 URL 등)
    ├── UserSession.java             # 사용자 정보 싱글톤
    ├── ErrorNotifier.java           # 에러 알림 (Slack 등)
    └── Logger.java                  # 로깅
```

## 네트워크 레이어

- **Retrofit 2.x** + **OkHttp 3** + **Gson**
- **CompletableFuture** 패턴 주로 사용
- Base URL: `Constants.SERVER_URL`
- User-Agent 헤더 인터셉터 자동 적용

## 지도 SDK (프로젝트에 맞게 선택)

- **T-map SDK** — 네비게이션 경로
- **Google Maps** — 범용 지도
- **Kakao Maps** — POI

## UI 특이사항

- 화면 방향: `[portrait / sensorLandscape / 기타]`
- DataBinding 활성화 여부

## 빌드 설정 주의

- **서명:** `gradle.properties`에 keystore 정보 (수정 금지)
- **외부 서비스 키:** `buildConfigField`로 주입 — `build.gradle`의 `buildConfig` 섹션
- **Firebase:** `google-services.json`은 app 모듈에 위치

> 시크릿/민감정보 규칙: `@.claude/docs/security/secret-handling.md`
