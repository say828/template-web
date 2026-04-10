# Ordering And Fulfillment

## Covered Planning Artifacts

- `sdd/01_planning/01_feature/order_feature_spec.md`
- `sdd/01_planning/01_feature/fulfillment_feature_spec.md`
- `sdd/01_planning/01_feature/shipping_feature_spec.md`

## Implemented Scope

- 주문, 처리, 배송 baseline은 `orders`, `fulfillment`, `shipping` context로 분리되어 있다.
- mobile/operator surface는 fulfillment/shipping read model을 사용하고, admin/web은 order overview contract를 사용한다.

## Implementation Shape

- backend owner는 `server/contexts/orders`, `server/contexts/fulfillment`, `server/contexts/shipping`이다.
- frontend는 route/page 단위에서 typed API module을 통해 current contract를 소비한다.

## Current Behavior

- 템플릿은 주문 상태, 처리 현황, 배송 현황 같은 e-commerce baseline 흐름을 current example로 제공한다.
