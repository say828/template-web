`data/`는 sample payload, fixture, seed data를 두는 루트다.

기본 정책:

- domain/application logic는 `contexts/*`에 둔다
- 재사용 가능한 fixture와 seed payload는 `data/`에 둔다
- adapter별 local bootstrap 데이터도 이 루트에 둔다

현재 canonical bootstrap:

- `bootstrap/auth_accounts.json`: auth credential/account bootstrap 원본
- `bootstrap/users.json`: user profile bootstrap 원본
- `bootstrap/catalog_products.json`: catalog product 원본
- `bootstrap/inventory_levels.json`: inventory level 원본
- `bootstrap/orders.json`: web/admin order surface 원본
- `bootstrap/fulfillment_tasks.json`: mobile fulfillment board task 원본
- `bootstrap/fulfillment_events.json`: mobile fulfillment timeline 원본
- `bootstrap/fulfillment_notes.json`: mobile fulfillment note 원본
- `bootstrap/support_faqs.json`: admin support surface 원본

규칙:

- 코드 안에 seed 레코드를 하드코딩하지 않는다
- memory/postgres/mysql/mariadb/mongodb adapter는 같은 `data/bootstrap/*` 원본을 consume한다
