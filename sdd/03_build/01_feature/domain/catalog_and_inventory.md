# Catalog And Inventory

## Covered Planning Artifacts

- `sdd/01_planning/01_feature/catalog_feature_spec.md`
- `sdd/01_planning/01_feature/inventory_feature_spec.md`

## Implemented Scope

- 상품/카탈로그와 재고 baseline은 `catalog`, `inventory` context로 분리되어 있다.
- landing/web surface는 catalog read model을, admin surface는 catalog/inventory 관리 contract를 사용한다.

## Implementation Shape

- backend owner는 `server/contexts/catalog`, `server/contexts/inventory`다.
- frontend는 service별 `client/*/src/api` 계층에서 typed response를 통해 contract를 소비한다.

## Current Behavior

- landing은 catalog discovery baseline, admin은 catalog/inventory 관리 baseline을 제공한다.
