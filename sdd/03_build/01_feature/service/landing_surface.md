# Landing Surface

## Covered Planning Artifacts

- `sdd/01_planning/01_feature/catalog_feature_spec.md`
- `sdd/01_planning/01_feature/health_feature_spec.md`

## Implemented Scope

- runtime root는 `client/landing/src/main.tsx -> AuthProvider -> BrowserRouter -> client/landing/src/App.tsx` 순서로 조립된다.
- public branch는 `/`의 `LandingHomePage`, `/login`의 `LandingLoginPage`로 끝나며 gated branch는 `ProtectedRoute -> LandingShell -> /workspace -> LandingWorkspacePage` 체인이다.
- backend leaf는 `server/main.py -> server/api/http/app.py -> server/api/http/router.py -> contexts/catalog/contracts/http/router.py`, `contexts/health/contracts/http/router.py`, `contexts/user/contracts/http/router.py` 체인으로 이어진다.
- landing surface는 public discovery와 authenticated workspace baseline을 current runtime tree로 제공한다.
