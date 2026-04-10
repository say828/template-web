# frontend live integration

## Covered Planning Artifact

- `sdd/02_plan/07_integration/frontend_live_integration.md`

## Implemented Scope

- service app은 backend domain contract와 typed API helper를 통해 연결된다.
- landing/catalog, mobile/fulfillment-shipping, admin/alerts-orders, web/catalog-orders-support 흐름을 current baseline으로 유지한다.
- mobile template shared lib에 `useSpeechRecognitionInput.ts`를 추가해 browser Web Speech API 입력을 consumer screen에서 재사용할 수 있게 했다.
