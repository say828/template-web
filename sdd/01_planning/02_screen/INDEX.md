# Screen Planning

- screen code format: `{SERVICE}-S{NNN}`
- canonical service code: `WEB`, `ADM`, `MOB`, `LND`

- [web_screen_spec.pdf](./web_screen_spec.pdf)
- [admin_screen_spec.pdf](./admin_screen_spec.pdf)
- [mobile_screen_spec.pdf](./mobile_screen_spec.pdf)
- [landing_screen_spec.pdf](./landing_screen_spec.pdf)

화면 코드와 기능 설명은 각 PDF 상세 페이지의 우측 테이블을 canonical surface로 사용한다.
build source, capture asset, generator는 `sdd/99_toolchain/01_automation` 아래에 둔다.
`MOB-S003`의 canonical route는 `/fulfillment`이고, landing catalog proof는 `GET /api/v1/catalog/products`를 기준으로 한다.
