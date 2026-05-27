# Spring Boot 리뷰 체크리스트

> dev-springboot, code-reviewer 참조.
> 공통 체크리스트는 `@.claude/docs/review-checklists/common.md` 먼저 적용.

## 응답 / 트랜잭션

- [ ] **공통 응답 포맷** — `{ result, resultMsg, data }` 준수
- [ ] **`@Transactional`** — 여러 DB 호출 + 일관성 필요한 Service 메서드에 적용했는가
- [ ] Controller에서 도메인 로직 처리하지 않고 Service에 위임했는가

## DB / Mapper

- [ ] **MyBatis XML** — 사용자 입력은 `${}` 대신 `#{}` 사용 (SQL 인젝션 방지)
- [ ] **N+1 쿼리** — 반복문 내에서 DB 호출하지 않는가
- [ ] DDL 변경 시 `DB/` 폴더에 SQL 파일 추가했는가

## 인증 / 권한

- [ ] JWT 인증이 필요한 엔드포인트가 `JwtRequestFilter` 화이트리스트에 잘못 포함되지 않았는가
- [ ] 새 엔드포인트의 역할 요구사항이 `SecurityConfig`에 명시되었는가
- [ ] 관리자 전용 API에 적절한 역할 제약이 걸려 있는가

## 시크릿 / 로그

- [ ] 민감 정보(패스워드, 토큰)가 로그에 출력되지 않는가
- [ ] `application-prd.properties` 수정이 포함된 경우 — 운영 영향도 확인 (사용자 컨펌)
- [ ] Firebase 등 서비스 계정 키 파일이 diff에 들어있지 않은가

## 비동기 / 성능

- [ ] 오래 걸리는 작업에 `@Async` 적용을 고려했는가
- [ ] `@Async` 메서드는 같은 클래스 내에서 호출하지 않는가 (프록시 우회 주의)

## 운영

- [ ] 운영 영향 가는 변경이면 PR 본문에 영향도 명시
- [ ] 외부 서비스 키 변경이 필요한 경우 사용자 확인 받았는가
