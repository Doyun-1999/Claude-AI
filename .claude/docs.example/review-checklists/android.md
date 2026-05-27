# Android 리뷰 체크리스트

> dev-android, dev-android-kotlin, code-reviewer 참조.
> 공통 체크리스트는 `@.claude/docs/review-checklists/common.md` 먼저 적용.

## 메모리 / 라이프사이클

- [ ] **메모리 누수 가능성** — Context 참조, inner class, static 필드에 Activity/Fragment 보관 여부
- [ ] **LifecycleOwner** — LiveData `observe` 시 `viewLifecycleOwner` vs `this` 올바른가
  - Fragment에서 view를 observe하는 경우 `viewLifecycleOwner` 사용
  - Activity나 ViewModel 자체에서 observe할 때만 `this`
- [ ] **Fragment backstack** — 뒤로가기/replace 시 상태 보존이 의도대로인가

## 스레드

- [ ] **UI는 Main Thread에서만** — 백그라운드에서 View 직접 접근 금지
- [ ] **CompletableFuture 결과 UI 반영** — `postValue` 사용 (`setValue`는 Main Thread 전용)
- [ ] **코루틴 사용 시 (Kotlin)** — `Dispatchers.IO`에서 네트워크, `Main`에서 UI 갱신

## 권한

- [ ] **권한 체크 누락 없는가** — 위치, 카메라, 저장소, 알림 등 dangerous permission
- [ ] 권한 거부 시 fallback 처리

## Kotlin 마이그레이션 진행 중일 때

- [ ] Java ↔ Kotlin 호환성 — `@JvmStatic`, `@JvmField`, nullable 어노테이션 적절한가
- [ ] 신규 파일은 Kotlin으로 작성했는가

## UI

- [ ] DataBinding expression이 너무 복잡하지 않은가 (로직은 ViewModel로)
- [ ] 화면 방향 고정이 필요한 앱이라면 의도대로 설정되어 있는가

## 외부 SDK 사용 시

- [ ] 지도 SDK / 외부 서비스 API 키 노출 여부
- [ ] 운영 에러 알림(Slack 등)이 너무 자주 호출되는 위치에 있지 않은가
