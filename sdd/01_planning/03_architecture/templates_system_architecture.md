# templates system architecture

- 작성 버전: 1.0.0

## Purpose

`templates` 레포의 현재 runtime 구조와 bounded context 경계를 구현 기준으로 정리한다.

## Document Boundary

- frontend, backend, infra 공통 구조와 구현 선택을 이 문서에서 다룬다.
- entity/schema/relationship/key policy 같은 데이터 모델링 상세는 `sdd/01_planning/04_data/`에서 다룬다.

## 1. Runtime Topology

| Layer | Owner | Responsibility |
| --- | --- | --- |
| `server` | HTTP backend | auth, user, catalog, inventory, orders, fulfillment, shipping, alerts, support, health를 HTTP API surface로 제공 |
| `client/web` | React + Vite frontend | 보호된 web shell과 dashboard/orders surface |
| `client/admin` | React + Vite frontend | 보호된 관리자 shell과 overview/queue/support surface |
| `client/mobile` | React + Vite frontend | 보호된 모바일 shell과 dashboard/fulfillment surface |
| `client/landing` | React + Vite frontend | public landing + protected workspace surface |
| `infra/compose` | container runtime | root compose baseline + dedicated DEV(개발계)/PROD overlay 레이아웃 |

## 2. Transport Topology

| Surface | Module | Responsibility |
| --- | --- | --- |
| HTTP | `server/api/http` | FastAPI app, router aggregation, `/health`, `/api/v1/*` 제공 |

## 3. Backend Context Map

| Bounded Context | Module | Role |
| --- | --- | --- |
| Authentication & Session | `server/contexts/auth` | login, bearer token 해석, 인증 계정 저장 |
| User Directory | `server/contexts/user` | 사용자 profile 목록/상세/상태 관리 |
| Product Catalog | `server/contexts/catalog` | public catalog read와 admin catalog write |
| Inventory Availability | `server/contexts/inventory` | SKU/거점 재고 조회와 운영 mutation |
| Order Operations | `server/contexts/orders` | web/admin 주문 overview, 목록, 생성, 상태 전이 |
| Fulfillment Operations | `server/contexts/fulfillment` | mobile overview, board, task 상태 전이 |
| Shipping Operations | `server/contexts/shipping` | mobile 배송 overview, shipment 목록, 배송 상태 전이 |
| Alert Center | `server/contexts/alerts` | admin 운영 알람 feed, 읽음 처리 |
| Support Content | `server/contexts/support` | 관리자 FAQ 목록/작성/노출 상태 변경 |
| Health | `server/contexts/health` | technical health/status contract |

## 4. Context Relationship

- `auth`는 `user`와 분리된 인증 계정 bootstrap을 사용한다.
- `user`는 profile directory만 소유하고 credential hash를 저장하지 않는다.
- `catalog`는 landing/public read와 admin write surface를 함께 소유한다.
- `inventory`는 현재 admin 운영 surface를 통해 직접 조정되고, `orders`와 `fulfillment`의 참조 도메인으로 연결된다.
- `orders`는 web read model과 admin read model을 동시에 노출한다.
- `fulfillment`는 mobile 서비스의 canonical backend surface다.
- `shipping`은 `fulfillment`의 downstream delivery 상태를 분리해 mobile/operator surface에 제공한다.
- `alerts`는 admin이 소비하는 운영 알람 표현과 읽음 상태를 별도 context로 소유한다.

## 5. Layering Rule

- context 외부 진입점은 `contexts/*/contracts/http`에 둔다.
- application layer는 use case orchestration만 담당한다.
- domain layer는 request/response model과 aggregate/read model을 가진다.
- infrastructure layer는 adapter, repository factory, shared gateway binding을 담당한다.
- shared logic는 `shared/application`, `shared/infrastructure`에 두되, 특정 domain 소유물이 되면 context 내부로 이동한다.
- transport wiring은 `api/http`에 두고 domain 로직은 `contexts/*`에만 둔다.

## 6. Runtime Component Baseline

| Component | Current Baseline | Next Step |
| --- | --- | --- |
| HTTP server | `FastAPI + Uvicorn` | authz, rate limit, observability middleware 추가 |
| Persistence | bootstrap JSON + selectable DB adapter | transaction boundary와 repository parity 강화 |
| Frontend runtime | `React 18 + Vite 5 + pnpm workspace` | contract-driven env injection 자동화 |

## 7. Current Known Gaps

- persistence baseline은 여전히 bootstrap JSON + in-memory mutation 중심이다.
- order 생성과 fulfillment/shipping 전이가 inventory 자동 연동까지는 아직 확장되지 않았다.
- support는 FAQ 관리 중심이고 ticket/workflow 도메인까지는 아직 포함하지 않는다.

## 8. Next Refactoring Direction

- catalog/inventory/order/fulfillment/shipping 간의 orchestration을 application service 수준으로 확장한다.
- auth account와 user profile 사이의 provisioning 흐름을 별도 domain service로 일반화한다.
- admin surface에서 alerts/support/catalog/inventory command를 직접 소비하도록 frontend scope를 넓힌다.
