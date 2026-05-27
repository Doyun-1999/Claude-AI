# 시크릿 / 민감정보 처리 규칙

> 모든 프로젝트 공통. dev-*, code-reviewer가 함께 참조.

## 절대 수정 금지 파일

### Spring Boot
- `application-prd.properties` — 운영 DB 연결 정보
- `src/main/resources/*.json` — Firebase 서비스 계정 키 등

### Android
- `gradle.properties` — keystore 정보
- `google-services.json` — Firebase 설정

### 임베디드 / 기타
- 환경 초기화 스크립트 내 디바이스 식별 처리 로직
- 장치 환경 설정 파일

> 위 파일에 변경이 필요한 경우 사용자에게 먼저 확인.

## 로그 출력 금지 항목

다음은 어떤 레벨(debug/info/error)이든 **로그에 출력 금지**:

- 패스워드 (raw, 해시, 마스킹 무관)
- JWT 토큰 본문 (`Bearer eyJ...` 전체)
- 리프레시 토큰
- API 키, AWS 키, Firebase 서비스 계정 키
- 사용자 개인정보 (주민번호, 카드번호 등)
- 결제 게이트웨이 응답 본문 (마스킹 처리 없이 통째로)

**예외:** 디버그용이 필요하면 마지막 4자리만 마스킹된 형태 (`****1234`).

## 환경별 시크릿 주입

| 환경 | 위치 |
|---|---|
| Spring Boot dev | `application-dev.properties` |
| Spring Boot prd | `application-prd.properties` (수정 금지) |
| Android | `gradle.properties`의 `buildConfigField` |
| Kotlin 앱 | `local.properties` → `BuildConfig`로 주입 |

## 외부 서비스 키 변경이 필요한 경우

- 사용자에게 영향도 보고 후 진행
- 자동 진행 금지 (orchestrator의 중단 조건)

## PR 체크

- [ ] 새 코드에 하드코딩된 키/URL/토큰이 없는가
- [ ] `.gitignore`가 새 secret 파일을 포함하는가
- [ ] 로그에 민감 정보가 출력되지 않는가
- [ ] `application-prd.properties` 또는 Firebase 키 파일이 diff에 들어있지 않은가
