# Mobile Surface

## Covered Planning Artifacts

- `sdd/01_planning/01_feature/auth_feature_spec.md`
- `sdd/01_planning/01_feature/fulfillment_feature_spec.md`
- `sdd/01_planning/01_feature/shipping_feature_spec.md`

## Implemented Scope

- runtime root는 `client/mobile/src/main.tsx -> AuthProvider -> BrowserRouter -> client/mobile/src/app/App.tsx` 순서로 조립된다.
- public leaf는 `LoginPage` 하나이며, gated branch는 `ProtectedRoute -> InShell` 뒤에 `/`, `/fulfillment`, `/shipping` route leaf를 둔다.
- route leaf는 `DashboardPage`, `FulfillmentPage`, `ShippingPage`로 끝나고 backend leaf는 `server/main.py -> server/api/http/app.py -> server/api/http/router.py -> contexts/auth/contracts/http/router.py`, `contexts/fulfillment/contracts/http/router.py`, `contexts/shipping/contracts/http/router.py` 체인으로 이어진다.
- mobile surface는 auth, fulfillment, shipping baseline을 current runtime tree로 제공한다.
