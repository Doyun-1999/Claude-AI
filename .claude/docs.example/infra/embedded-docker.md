# 임베디드 환경 빌드 & 실행 풀체인

> dev-frontend 전용 참조. 임베디드 장치에서 HMI 시작 절차.

## 환경별 경로

| 환경 | 경로 |
|---|---|
| 로컬 (Mac) | `/Users/[USERNAME]/Project/[project]` |
| 임베디드 장치 | `/home/[user]/[project_path]` |
| 도커 컨테이너 안 | `/[project]` (장치 경로 마운트) |

## 빌드 (컨테이너 안)

```bash
cd /[project]
bash [build_script].sh build_frontend       # frontend (port [PORT_A])
bash [build_script].sh build_op-frontend    # op-frontend (port [PORT_B])
```

## 실행 풀체인 ⚠️ (반드시 이 순서)

```bash
# 1) 호스트 셸에서
cd [project_path]
./docker/scripts/dev_start.sh    # 환경 초기화 + 장치 정보 자동 설정
./docker/scripts/dev_into.sh     # 컨테이너 진입

# 2) 컨테이너 안에서
./scripts/bootstrap.sh           # HMI 서비스 시작
```

### 🚫 `bootstrap.sh` 단독 실행 금지

`dev_start.sh`가 다음 init을 처리합니다:
- 장치 식별 정보 자동 설정 (USB → 장치 → 설정 파일)
- 기타 환경 변수 초기화

단독 시작 시 장치 ID 빈 값 + 일부 init 누락으로 HMI FATAL 가능.

## 브라우저 접속 (장치 IP 기준)

- `http://<DEVICE_IP>:[PORT_A]` — frontend
- `http://<DEVICE_IP>:[PORT_B]` — op-frontend (Safety Operator HMI)

## 빌드 산출물 커밋 주의

`dist/app.bundle.js`, `dist/app.bundle.js.map` 등이 git tracked인 경우가 있음.

의도치 않게 빌드 산출물이 diff에 들어가면:
```bash
git checkout -- [dist 경로]/
```

## 본 에이전트 범위 외 (별도 핸들링)

- 백엔드 C++ 변경
- BUILD/WORKSPACE/webpack.config 구조 변경
- 컨테이너 자체 트러블슈팅
- 새 모드 config 파일 추가/삭제
