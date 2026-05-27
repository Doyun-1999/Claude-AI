# 서버 배포 & 운영 환경

> dev-springboot, code-reviewer 참조.

## 환경

| 환경 | 인프라 |
|---|---|
| 개발 | AWS EC2 + RDS (ap-northeast-2) |
| 운영 | 별도 AWS RDS (prd) |
| 파일 저장 | `/home/[user]/[storage-path]/` |
| 로그 | `/home/[user]/logs/[app-name]/` |

## CI/CD

`.github/workflows/dev.yml` 기반.

## 빌드 & 실행

```bash
# 개발 서버 실행
./mvnw spring-boot:run -Dspring-boot.run.profiles=dev

# 운영 빌드
./mvnw clean package -Pprd
```

## 프로파일별 설정 위치

| 프로파일 | 파일 |
|---|---|
| 공통 | `application.properties` |
| dev | `application-dev.properties` |
| prd | `application-prd.properties` (수정 금지) |

## 운영 영향 변경 — 사용자 확인 필요

- `application-prd.properties` 수정 시 (DB connection, 외부 서비스 endpoint 변경 등)
- DB 스키마 변경 (DDL)
- 외부 서비스 키 회전
- SecurityConfig 화이트리스트 변경
- `@Async` 스레드풀 사이즈 변경

위 변경은 orchestrator의 "중단 조건"에 해당. 자동 진행 금지.

## PR 체크

- [ ] application-prd.properties 변경이 diff에 들어있지 않은가
- [ ] DB 변경이 있으면 `DB/` 폴더에 SQL 파일 추가되었는가
- [ ] 운영에 영향 가는 변경이면 PR 본문에 영향도 명시
