# JWT 인증 규칙

> Spring Boot 프로젝트의 JWT 표준. dev-springboot, code-reviewer가 함께 참조.

## 토큰 구조

| 항목 | 값 |
|---|---|
| AccessToken 유효시간 | [N초/분] (RefreshToken 기반 갱신 전제) |
| RefreshToken 유효시간 | [N일] |
| 헤더 | `Authorization: Bearer {token}` |
| 알고리즘 | HS256 |

## JWT 유틸 사용

```java
// 토큰에서 username 추출
String username = JwtUtils.getUsernameFromToken(token);

// 토큰 유효성 검증
boolean valid = JwtUtils.validateToken(token);

// 토큰 만료 여부
boolean expired = JwtUtils.isTokenExpired(token);
```

## 화이트리스트 (토큰 불필요 엔드포인트)

`JwtRequestFilter.java`에서 관리.

**규칙:**
- 새 공개 API 추가 시 `JwtRequestFilter.java`의 화이트리스트에 경로 추가
- 보호 대상 엔드포인트가 실수로 화이트리스트에 들어가지 않도록 PR에서 반드시 확인
- 화이트리스트는 prefix 매칭 — `/admin/`이 통째로 들어가면 `/admin/secret`도 노출됨

## 역할 기반 접근 제어

```java
// SecurityConfig.java
.antMatchers("/admin/**").hasAnyRole("MANAGER", "ADMIN")
.antMatchers("/api/**").hasAnyRole("MANAGER", "ADMIN", "USER")
```

**역할 종류:** 프로젝트에 맞게 정의 (예: `ROLE_ADMIN`, `ROLE_USER`, `ROLE_GUEST`)

## 보안 체크 (PR 시)

- [ ] JWT 인증이 필요한 엔드포인트가 화이트리스트에 잘못 포함되지 않았는가
- [ ] 새 엔드포인트의 역할 요구사항이 SecurityConfig에 명시되었는가
- [ ] 토큰 검증 실패 시 적절한 에러 응답을 반환하는가 (401 vs 403)
- [ ] 토큰에 민감 정보(패스워드, 개인정보)가 클레임으로 포함되지 않는가
