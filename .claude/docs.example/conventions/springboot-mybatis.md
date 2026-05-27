# Spring Boot + MyBatis 코드 컨벤션

> dev-springboot, code-reviewer 참조. 프로젝트 컨텍스트: `@.claude/docs/projects/springboot-api.md`

## 공통 응답 포맷

**모든 API는 아래 형식으로 응답:**
```json
{
  "result": "SUCCESS",
  "resultMsg": "처리 완료",
  "data": {}
}
```

**Controller에서 응답 구성:**
```java
@PostMapping("/yourEndpoint")
public Map<String, Object> yourMethod(@RequestBody Map<String, Object> request) {
    Map<String, Object> result = new HashMap<>();
    try {
        Object data = yourService.doSomething(request);
        result.put("result", "SUCCESS");
        result.put("resultMsg", "처리 완료");
        result.put("data", data);
    } catch (Exception e) {
        result.put("result", "FAILURE");
        result.put("resultMsg", e.getMessage());
    }
    return result;
}
```

## 새 기능 모듈 추가 절차

### 1. 디렉토리 구조

```
src/main/java/com/[yourcompany]/[모듈명]/
├── controller/[모듈명]Controller.java
├── service/[모듈명]Service.java
├── mapper/[모듈명]Mapper.java
└── model/[모듈명]Model.java

src/main/resources/mapper/[모듈명]/[모듈명].xml
```

### 2. Controller

```java
@RestController
public class [모듈명]Controller {

    private final [모듈명]Service [모듈명]Service;

    public [모듈명]Controller([모듈명]Service [모듈명]Service) {
        this.[모듈명]Service = [모듈명]Service;
    }

    @PostMapping("/your/endpoint")
    public Map<String, Object> yourMethod(@RequestBody Map<String, Object> request) {
        Map<String, Object> result = new HashMap<>();
        try {
            result.put("result", "SUCCESS");
            result.put("resultMsg", "완료");
            result.put("data", [모듈명]Service.doSomething(request));
        } catch (Exception e) {
            result.put("result", "FAILURE");
            result.put("resultMsg", e.getMessage());
        }
        return result;
    }
}
```

### 3. Service

```java
@Service
public class [모듈명]Service {

    private final [모듈명]Mapper [모듈명]Mapper;

    public [모듈명]Service([모듈명]Mapper [모듈명]Mapper) {
        this.[모듈명]Mapper = [모듈명]Mapper;
    }

    @Transactional
    public Object doSomething(Map<String, Object> params) {
        return [모듈명]Mapper.selectSomething(params);
    }
}
```

### 4. Mapper 인터페이스

```java
@Mapper
public interface [모듈명]Mapper {
    List<Map<String, Object>> selectSomething(Map<String, Object> params);
    int insertSomething(Map<String, Object> params);
    int updateSomething(Map<String, Object> params);
    int deleteSomething(Map<String, Object> params);
}
```

### 5. MyBatis XML 매퍼

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
    "http://mybatis.org/dtd/mybatis-3-mapper.dtd">

<mapper namespace="com.[yourcompany].[모듈명].mapper.[모듈명]Mapper">

    <select id="selectSomething" parameterType="map" resultType="map">
        SELECT column1, column2
        FROM your_table
        WHERE 1=1
        <if test="param != null and param != ''">
            AND column1 = #{param}
        </if>
        ORDER BY created_at DESC
    </select>

    <insert id="insertSomething" parameterType="map">
        INSERT INTO your_table (column1, column2, created_at)
        VALUES (#{column1}, #{column2}, NOW())
    </insert>

</mapper>
```

⚠️ **SQL 인젝션 방지** — 사용자 입력은 `${}` 대신 `#{}` 사용.

## 비동기 처리

```java
// @Async (스레드풀 설정은 AsyncConfig 참조)
@Async
public void asyncMethod() {
    // 비동기 처리
}
```

> 같은 클래스 내에서 self-invocation은 프록시 우회로 `@Async`가 동작하지 않음.

## 에러 처리

```java
throw new ErrorException(ErrorCode.YOUR_ERROR_CODE);
// GlobalExceptionHandler가 자동으로 처리:
// { "result": "FAILURE", "resultMsg": "에러 메시지" }
```

## 로깅

```java
private static final Logger log = LoggerFactory.getLogger(YourClass.class);

log.debug("디버그: {}", value);
log.info("정보: {}", value);
log.error("에러: {}", e.getMessage(), e);
```

> 로그에 민감 정보 출력 금지: `@.claude/docs/security/secret-handling.md`

## 자가검증

체크리스트: `@.claude/docs/review-checklists/springboot.md`
