# Web Surface

## Covered Planning Artifacts

- `sdd/01_planning/01_feature/auth_feature_spec.md`
- `sdd/01_planning/01_feature/catalog_feature_spec.md`
- `sdd/01_planning/01_feature/order_feature_spec.md`

## Implemented Scope

- runtime root는 `client/web/src/main.tsx -> AuthProvider -> BrowserRouter -> client/web/src/app/App.tsx` 순서로 조립된다.
- public leaf는 `LoginPage`이며, gated branch는 `ProtectedRoute -> AppShell` 뒤에 `/`와 `/orders` route leaf를 둔다.
- route leaf는 `DashboardPage`, `OrdersPage`로 끝나고 backend leaf는 `server/main.py -> server/api/http/app.py -> server/api/http/router.py -> contexts/auth/contracts/http/router.py`, `contexts/catalog/contracts/http/router.py`, `contexts/orders/contracts/http/router.py` 체인으로 이어진다.
- web surface는 인증, catalog, orders baseline을 current runtime tree로 제공한다.
