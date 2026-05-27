# Android Java 코드 컨벤션

> dev-android, code-reviewer 참조. 프로젝트 컨텍스트: `@.claude/docs/projects/android-app.md`

## 1. 새 API 엔드포인트 추가

**RetrofitInterface.java에 선언:**
```java
@POST("your/endpoint")
Call<Map<String, Object>> requestYourApi(@Body Map<String, Object> body);
```

**NetworkApi.java에 구현 (CompletableFuture 패턴):**
```java
public CompletableFuture<HashMap<String, Object>> requestYourApi(String param) {
    return CompletableFuture.supplyAsync(() -> {
        HashMap<String, Object> res = new HashMap<>();
        try {
            Map<String, Object> body = new HashMap<>();
            body.put("param", param);
            Response<Map<String, Object>> response =
                NetworkHelper.getApiService().requestYourApi(body).execute();
            if (response.isSuccessful() && response.body() != null) {
                res.putAll(response.body());
            }
        } catch (Exception e) {
            Logger.e("TAG", e.getMessage());
        }
        return res;
    });
}
```

## 2. 새 Fragment 추가

```java
public class YourFeatureFragment extends Fragment {
    private YourViewModel viewModel;

    @Override
    public void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        viewModel = new ViewModelProvider(requireActivity()).get(YourViewModel.class);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_your, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        viewModel.getSomeData().observe(getViewLifecycleOwner(), data -> {
            // UI 업데이트
        });
    }
}
```

## 3. 새 ViewModel 추가

```java
public class YourViewModel extends ViewModel {
    private final MutableLiveData<YourData> data = new MutableLiveData<>();

    public LiveData<YourData> getData() { return data; }

    public void fetchData(String param) {
        NetworkApi.getInstance().requestYourApi(param)
            .thenAccept(result -> {
                data.postValue(parseResult(result));
            });
    }
}
```

## 4. 사용자 정보 접근

```java
// 싱글톤으로 로그인된 사용자 정보 접근
String userId = UserSession.getInstance().getUserId();
```

## 5. 에러 처리 및 로깅

```java
// 운영 에러 알림 (Slack 등)
ErrorNotifier.sendError("기능명", "에러 설명", exception.getMessage());

// 로깅
Logger.d("TAG", "디버그 메시지");
Logger.e("TAG", "에러 메시지");
```

> 로그에 민감 정보 출력 금지: `@.claude/docs/security/secret-handling.md`

## 자가검증

체크리스트: `@.claude/docs/review-checklists/android.md`
