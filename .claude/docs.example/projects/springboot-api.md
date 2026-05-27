# [YOUR_API_NAME] (Spring Boot) — 프로젝트 컨텍스트

> dev-springboot, code-reviewer 참조.

## 기본 정보

| 항목 | 값 |
|---|---|
| 경로 | `/Users/[USERNAME]/[path/to/project]` |
| 패키지명 | `com.[yourcompany].[appname]` |
| Spring Boot | 2.x.x |
| Java | 11 / 17 |
| 빌드 도구 | Maven / Gradle |
| DB | MariaDB / MySQL / PostgreSQL |
| ORM | MyBatis (XML 매퍼) / JPA |

## 아키텍처

**3계층 Controller → Service → Mapper 구조**

```
HTTP Request
  └── Controller (@RestController)
        └── Service (@Service)
              └── Mapper (@Mapper, MyBatis)
                    └── XML 매퍼 (src/main/resources/mapper/)
                          └── DB
```

## 패키지 구조

```
src/main/java/com/[yourcompany]/[appname]/
├── [AppName]Application.java
├── config/
│   ├── SecurityConfig.java          # Spring Security + JWT 필터 등록
│   ├── JwtRequestFilter.java        # JWT 토큰 검증 필터
│   ├── DataBaseConfig.java          # MyBatis 설정
│   └── AsyncConfig.java             # @Async 스레드풀 설정
├── handler/
│   └── GlobalExceptionHandler.java  # @RestControllerAdvice
├── common/
│   └── util/
│       ├── JwtUtils.java            # JWT 생성/검증
│       └── OTPUtil.java             # OTP (선택)
└── [모듈명]/
    ├── controller/
    ├── service/
    ├── mapper/
    └── model/

src/main/resources/
├── application.properties
├── application-dev.properties
├── application-prd.properties       # 운영 환경 (수정 금지)
└── mapper/
    └── [모듈명]/[모듈명].xml
```

## 외부 서비스 통합 (예시)

| 서비스 | 용도 | 설정 위치 |
|---|---|---|
| SMS (Nurigo 등) | SMS 발송 | application-{dev,prd}.properties |
| 결제 게이트웨이 | 결제 | application-{dev,prd}.properties |
| Firebase FCM | 푸시 알림 | `/resources/*.json` (수정 금지) |
| 지도 API | 경로/지도 | application-{dev,prd}.properties |

## 관련 docs

- 코드 컨벤션 / 모듈 추가 절차: `@.claude/docs/conventions/springboot-mybatis.md`
- JWT 인증 규칙: `@.claude/docs/security/jwt.md`
- 시크릿 처리: `@.claude/docs/security/secret-handling.md`
- 배포 / 운영: `@.claude/docs/infra/cloud-deployment.md`
