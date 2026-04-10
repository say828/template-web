# Infra Compose

루트 [compose.yml](../../compose.yml)은 템플릿 저장소의 canonical dev-focused runtime baseline이다.
이 디렉터리는 dedicated host나 분리된 환경 스택이 필요할 때 사용하는 DEV(개발계)/PROD overlay와 env example을 유지한다.

파일:

- `dev.yml`: dedicated DEV(개발계) host/reference stack
- `prod.yml`: dedicated PROD/reference stack
- `.env.dev.example`: DEV(개발계) 변수 예시
- `.env.prod.example`: PROD 변수 예시

사용:

```bash
cp .env.example .env
docker compose up --build

cp infra/compose/.env.dev.example infra/compose/.env.dev
docker compose --env-file infra/compose/.env.dev -f infra/compose/dev.yml up -d --build

cp infra/compose/.env.prod.example infra/compose/.env.prod
docker compose --env-file infra/compose/.env.prod -f infra/compose/prod.yml up -d --build
```

주의:

- 루트 `compose.yml`은 clone 직후 4개 frontend surface, `server`, 기본 `postgres`를 함께 올리는 dev-focused baseline이다.
- optional DB adapter 검증은 root compose profile로 수행한다: `mysql`, `mariadb`, `mongo`.
- `infra/compose/dev.yml`, `infra/compose/prod.yml`은 dedicated host/runtime split이 필요할 때 쓰는 overlay이며, root compose baseline을 대체하는 문서 기준선은 아니다.
- provider-first canonical delivery split은 `AWS edge/domain -> OpenStack backend compute -> AWS data plane`이고, 세부 구조는 `infra/terraform/README.md`를 기준으로 설명한다.
- `VITE_API_BASE_URL`은 컨테이너 내부 DNS가 아니라 브라우저가 도달 가능한 API URL이어야 한다.
- 포트 역할은 root compose baseline과 같은 순서를 따른다: landing, web, mobile, admin, server/http.
- PROD 웹 앱은 `pnpm build + pnpm preview`로 기동한다.
- OpenStack에서 자동 배포까지 묶고 싶으면 `infra/terraform/openstack/server` 또는 lower-level `openstack/dev`, `openstack/prod` root를 사용한다.
