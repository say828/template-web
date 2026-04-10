# server

hexagonal/DDD 구조를 따르는 HTTP 서버 보일러플레이트다.

포함 패턴:

- `api/http`, `contexts`, `data`, `tests` root layout
- `contexts/*/(application|domain|infrastructure|contracts)` 중심 DDD 분리
- `contexts/auth`, `contexts/user`, `contexts/shipping`, `contexts/alerts` 예시 도메인과 실제 호출 가능한 sample logic
- HTTP 계약은 `contexts/*/contracts/http`에 둔다
- `shared/(application|infrastructure)` 공통 레이어
- `memory`, `postgres`, `mysql`, `mariadb`, `mongodb` adapter 선택 가능
- `api/http/app.py` FastAPI app entrypoint
- `config.py` settings cache
- `api/http/router.py` 중심의 HTTP router aggregation
- `/health`와 `/api/v1/*` 기본 계약
- `.env.example`와 pytest 기본 테스트

시작:

```bash
uv sync --extra dev
uv run uvicorn api.http.app:app --reload
```

기본 인증 예시:

- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `GET /api/v1/users`
- `GET /api/v1/users/{user_id}`
- `GET /api/v1/shipping/overview`
- `GET /api/v1/alerts`
