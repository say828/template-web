# catalog feature spec

- 작성 버전: 1.1.0

## 1. Purpose

`catalog` bounded context가 제공하는 상품 카탈로그 조회와 관리자 상품 편집 기능을 구현 기준으로 정리한다.

## 2. Scope

- 포함 범위:
  - landing/public 상품 카탈로그 조회와 단일 상품 상세 조회
  - admin surface의 상품 생성, 수정, 상태 변경 command
- 제외 범위:
  - landing 화면의 정렬, 탭, CTA 같은 UI 상호작용
  - 주문 생성이나 재고 선점 같은 타 context orchestration

## 3. Actor Summary

| Actor | Description | Appears In |
| --- | --- | --- |
| `Landing Visitor` | 비로그인 상태로 공개 상품 카탈로그와 상품 상세를 탐색하는 방문자다. | `CAT-F001`, `CAT-F002` |
| `Landing Member` | 로그인된 landing 회원으로 공개 상품을 둘러보고 구매 전 탐색을 수행하는 사용자다. | `CAT-F001`, `CAT-F002` |
| `Web User` | web 서비스에서 주문 생성이나 운영 판단을 위해 상품 정보를 조회하는 내부 사용자다. | `CAT-F001`, `CAT-F002` |
| `Admin Operator` | admin 서비스에서 상품을 등록, 수정, 상태 변경하는 운영 관리자다. | `CAT-F003`, `CAT-F004`, `CAT-F005` |

## 4. Bounded Context Summary

| Item | Value |
| --- | --- |
| Domain Code | `CAT` |
| Bounded Context | Product Catalog |
| Primary Backend Owner | `server/contexts/catalog` |
| Related Context | `auth`, `inventory`, `orders`, `landing` |
| Main Entry Contract | `GET /api/v1/catalog/products`, `GET /api/v1/catalog/products/{product_id}`, `POST /api/v1/catalog/products`, `PUT /api/v1/catalog/products/{product_id}`, `PATCH /api/v1/catalog/products/{product_id}/status` |

## 5. Aggregate / Model Snapshot

| Aggregate / Model | Role |
| --- | --- |
| `ProductRecord` | 상품 원본 저장 모델 |
| `ProductSummary` | 상품 목록 응답 모델 |
| `ProductDetail` | 상품 상세 응답 모델 |
| `CreateProductCommand` | 상품 생성 명령 |
| `UpdateProductCommand` | 상품 수정 명령 |
| `UpdateProductStatusCommand` | 상품 상태 변경 명령 |

## 6. Use Case Matrix

| Feature Code | Use Case | Actor | Bounded Context | Aggregate / Model | Type | Preconditions | Domain Outcome | Invariant / Business Rule |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `CAT-F001` | 상품 카탈로그 목록을 조회한다 | Landing Visitor, Landing Member, Web User | Product Catalog | `ProductSummary`, `ProductRecord` | Query | 상품 bootstrap 데이터가 존재해야 한다 | 공개 가능한 상품 목록을 필터와 검색 조건에 맞게 반환한다 | `status`, `category`, `q` 조건은 모두 현재 카탈로그 집합 안에서 계산한다 |
| `CAT-F002` | 단일 상품 상세를 조회한다 | Landing Visitor, Landing Member, Web User | Product Catalog | `ProductDetail`, `ProductRecord` | Query | 요청한 `product_id`가 저장소에 존재해야 한다 | 상세 페이지 구성을 위한 상품 전체 속성을 반환한다 | 존재하지 않는 `product_id`면 `404 Catalog product not found`를 반환한다 |
| `CAT-F003` | 관리자가 새 상품을 등록한다 | Admin Operator | Product Catalog | `CreateProductCommand`, `ProductDetail`, `ProductRecord` | Command | 관리자 토큰이 유효하고 slug, 이름, 가격, variant 정보가 전달되어야 한다 | 새 상품 레코드가 생성되어 카탈로그 목록에 합류한다 | `slug`는 카탈로그 내에서 유일해야 하며 variant는 최소 1개 이상이어야 한다 |
| `CAT-F004` | 관리자가 상품 속성을 수정한다 | Admin Operator | Product Catalog | `UpdateProductCommand`, `ProductDetail`, `ProductRecord` | Command | 관리자 토큰이 유효하고 요청한 `product_id`가 존재해야 한다 | 상품 속성이 부분 갱신되고 `updated_at`이 갱신된다 | 빈 수정 요청은 `400 No catalog product fields provided`, 중복 slug는 `409`를 반환한다 |
| `CAT-F005` | 관리자가 상품 상태를 변경한다 | Admin Operator | Product Catalog | `UpdateProductStatusCommand`, `ProductDetail`, `ProductRecord` | Command | 관리자 토큰이 유효하고 요청한 `product_id`가 존재해야 한다 | 상품 `status`가 `draft`, `active`, `archived` 중 하나로 전환된다 | 존재하지 않는 `product_id`면 `404 Catalog product not found`를 반환한다 |

## 7. Notes

- `catalog`는 landing/public read surface와 admin write surface를 함께 소유한다.
- 카탈로그의 가격, 이미지, 속성, variant는 모두 product aggregate 내부 속성으로 유지한다.
