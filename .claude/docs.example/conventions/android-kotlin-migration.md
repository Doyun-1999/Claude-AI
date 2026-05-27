# Kotlin 마이그레이션 가이드라인

> dev-android, code-reviewer 참조.
> Java → Kotlin 마이그레이션이 예정된 프로젝트에 적용.

## 준수 사항

### 1. 신규 파일은 Kotlin으로 작성
기존 Java 파일을 건드리지 않을 때는 `.kt` 파일로 생성.

### 2. 기존 파일 마이그레이션 시
Android Studio의 "Convert Java File to Kotlin File" 기능 활용.

### 3. Kotlin 관용구 사용

- `var`/`val` 명확히 구분 (가능하면 `val` 우선)
- Nullable 타입 (`?`) 명시
- `data class`로 모델 클래스 변환
- `object`로 싱글톤 변환
- `sealed class`로 상태 Enum 개선 가능
- `coroutines`로 CompletableFuture 대체 권장

### 4. ViewModel은 코루틴 우선

```kotlin
class YourViewModel : ViewModel() {
    private val _data = MutableLiveData<YourData>()
    val data: LiveData<YourData> = _data

    fun fetchData(param: String) {
        viewModelScope.launch {
            val result = withContext(Dispatchers.IO) {
                NetworkApi.getInstance().requestYourApi(param).get()
            }
            _data.value = parseResult(result)
        }
    }
}
```

### 5. DataBinding → ViewBinding 전환 고려
마이그레이션 시 함께 검토.

### 6. DI 도입 시 Hilt 사용
Dagger보다 Android 친화적.

## Java ↔ Kotlin 호환성 체크

- [ ] Kotlin 코드를 Java에서 호출할 때 `@JvmStatic`, `@JvmField`, `@JvmOverloads` 적용 여부
- [ ] Nullable 어노테이션 (`@Nullable`, `@NonNull`) 일관성
- [ ] Companion object의 멤버를 Java에서 정적으로 부르려면 `@JvmStatic` 필요

## 자가검증

체크리스트: `@.claude/docs/review-checklists/android.md`
