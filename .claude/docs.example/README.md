# .claude/docs.example — 에이전트 참조 문서 템플릿

> **이 폴더는 공개용 예시입니다.**
> 실제 프로젝트 정보는 `.claude/docs/` (gitignored)에 두고,
> 이 예시를 복사해 자신의 프로젝트에 맞게 채워 사용하세요.

에이전트들이 작업 전에 로드하는 도메인 지식·컨벤션·체크리스트 모음.

## 📁 디렉토리 구조

```
.claude/docs/
├── projects/            # 프로젝트별 컨텍스트 (패키지 구조, 아키텍처, 외부 서비스)
├── conventions/         # 코드 컨벤션 (패턴, 모듈 추가 절차, 마이그레이션 가이드)
├── security/            # 횡단 보안 규칙 (JWT, 시크릿)
├── infra/               # 빌드 / 배포 / 운영 환경
└── review-checklists/   # 코드 리뷰 / 자가검증 체크리스트
```

## 📑 파일별 책임

### projects/ — 어떤 프로젝트인가
- [android-app.md](projects/android-app.md) — Android 앱 (Java, Kotlin 마이그레이션 예정)
- [springboot-api.md](projects/springboot-api.md) — Spring Boot 백엔드 API
- [embedded-hmi.md](projects/embedded-hmi.md) — 임베디드 환경 React HMI
- [kotlin-compose-app.md](projects/kotlin-compose-app.md) — Kotlin + Compose 신규 앱

### conventions/ — 어떻게 코드를 작성하는가
- [android-java.md](conventions/android-java.md) — Android Java 코드 패턴
- [android-kotlin-migration.md](conventions/android-kotlin-migration.md) — Java→Kotlin 마이그레이션 규칙
- [android-kotlin-compose.md](conventions/android-kotlin-compose.md) — Compose + StateFlow + Hilt 패턴
- [springboot-mybatis.md](conventions/springboot-mybatis.md) — Controller/Service/Mapper/XML 추가 절차
- [react-mobx.md](conventions/react-mobx.md) — React + MobX 패턴 및 함정

### security/ — 보안 표준 (스택 횡단)
- [jwt.md](security/jwt.md) — JWT 구조, 화이트리스트, 역할 기반 접근
- [secret-handling.md](security/secret-handling.md) — 시크릿/로그 출력 금지

### infra/ — 빌드 / 배포 / 운영
- [embedded-docker.md](infra/embedded-docker.md) — 임베디드 환경 빌드 & 실행 풀체인
- [cloud-deployment.md](infra/cloud-deployment.md) — 클라우드 서버 배포 환경

### review-checklists/ — 자가검증 / 코드 리뷰
- [common.md](review-checklists/common.md) — 모든 스택 공통 체크
- [android.md](review-checklists/android.md) — Android 공통 체크
- [springboot.md](review-checklists/springboot.md) — Spring Boot 응답·트랜잭션·DB·인증 체크
- [frontend.md](review-checklists/frontend.md) — React + MobX 체크

## 📝 유지보수 원칙

- **한 정보는 한 곳에만** — 같은 규칙을 여러 docs에 적지 않음
- **에이전트는 얇게** — 도메인 지식·체크리스트는 docs에. 에이전트 파일은 "역할 + 어떤 docs 로드 + 작업 절차"만
- **시간에 따라 변하는 정보는 memory** — `~/.claude/projects/.../memory/`. 안정적 규약만 docs
- 새 프로젝트 추가 시 → `projects/`에 컨텍스트 파일 + 필요시 `conventions/`에 코드 스타일
