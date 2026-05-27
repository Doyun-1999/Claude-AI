# Kotlin + Compose 코드 컨벤션

> dev-android-kotlin, code-reviewer 참조. 프로젝트 컨텍스트: `@.claude/docs/projects/kotlin-compose-app.md`

## ViewModel + StateFlow

```kotlin
@HiltViewModel
class ArrivalViewModel @Inject constructor(
    private val repository: ArrivalRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow<UiState>(UiState.Loading)
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()

    private var refreshJob: Job? = null

    fun startAutoRefresh(param: String) {
        refreshJob?.cancel()
        refreshJob = viewModelScope.launch {
            while (isActive) {
                fetchData(param)
                delay(5_000)
            }
        }
    }

    override fun onCleared() {
        super.onCleared()
        refreshJob?.cancel()
    }
}

sealed class UiState {
    object Loading : UiState()
    data class Success(val data: List<YourModel>) : UiState()
    data class Error(val message: String) : UiState()
}
```

## Compose Screen 기본 구조

```kotlin
@Composable
fun YourScreen(
    param: String,
    viewModel: YourViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsState()

    LaunchedEffect(param) {
        viewModel.startAutoRefresh(param)
    }

    val pullRefreshState = rememberPullRefreshState(
        refreshing = uiState is UiState.Loading,
        onRefresh = { viewModel.refresh(param) }
    )

    Box(Modifier.pullRefresh(pullRefreshState)) {
        when (val state = uiState) {
            is UiState.Success -> ContentList(state.data)
            is UiState.Loading -> CircularProgressIndicator()
            is UiState.Error -> ErrorMessage(state.message)
        }
        PullRefreshIndicator(
            refreshing = uiState is UiState.Loading,
            state = pullRefreshState,
            modifier = Modifier.align(Alignment.TopCenter)
        )
    }
}
```

## Room 로컬 DB

```kotlin
@Entity(tableName = "your_table")
data class YourEntity(
    @PrimaryKey val id: String,
    val addedAt: Long = System.currentTimeMillis()
)

@Dao
interface YourDao {
    @Query("SELECT * FROM your_table ORDER BY addedAt DESC")
    fun getAll(): Flow<List<YourEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(entity: YourEntity)

    @Delete
    suspend fun delete(entity: YourEntity)
}
```

## Hilt 모듈

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object AppModule {

    @Provides @Singleton
    fun provideRetrofit(): Retrofit = Retrofit.Builder()
        .baseUrl(BuildConfig.API_BASE_URL)
        .addConverterFactory(Json.asConverterFactory("application/json".toMediaType()))
        .build()

    @Provides @Singleton
    fun provideApiService(retrofit: Retrofit): YourApiService =
        retrofit.create(YourApiService::class.java)

    @Provides @Singleton
    fun provideDatabase(@ApplicationContext ctx: Context): AppDatabase =
        Room.databaseBuilder(ctx, AppDatabase::class.java, "app.db").build()
}
```

## 코드 규칙

- **Composable 함수는 side-effect 없이 순수하게 유지** (부수효과는 `LaunchedEffect`, `SideEffect`, `DisposableEffect`)
- **Repository는 항상 `Result<T>` 또는 `Flow<T>`로 반환** (직접 throw 금지)
- **하드코딩 금지** — API key는 `local.properties` → `BuildConfig`로 주입
- `var` 보다 `val` 우선, `sealed class` 와 `data class` 적극 사용

## 자가검증

체크리스트: `@.claude/docs/review-checklists/android.md`
