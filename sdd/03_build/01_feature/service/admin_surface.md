# Admin Surface

## Covered Planning Artifacts

- `sdd/01_planning/01_feature/alerts_feature_spec.md`
- `sdd/01_planning/01_feature/catalog_feature_spec.md`
- `sdd/01_planning/01_feature/inventory_feature_spec.md`
- `sdd/01_planning/01_feature/support_feature_spec.md`

## Implemented Scope

- runtime root는 `client/admin/src/main.tsx -> AuthProvider -> BrowserRouter -> client/admin/src/app/App.tsx` 순서로 조립된다.
- public leaf는 `AdminLoginPage`이며, gated branch는 `ProtectedRoute -> AdminShell` 뒤에 `/`, `/queue`, `/support` route leaf를 둔다.
- route leaf는 `AdminDashboardPage`, `AdminQueuePage`, `AdminSupportPage`로 끝나고 backend leaf는 `server/main.py -> server/api/http/app.py -> server/api/http/router.py -> contexts/alerts/contracts/http/router.py`, `contexts/inventory/contracts/http/router.py`, `contexts/support/contracts/http/router.py` 체인으로 이어진다.
- admin surface는 alerts, inventory, support baseline을 current runtime tree로 제공한다.
