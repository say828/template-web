# domain surfaces

## Covered Planning Artifact

- `sdd/01_planning/01_feature/INDEX.md`

## Implemented Scope

- backend domain baseline은 `auth`, `user`, `catalog`, `inventory`, `orders`, `fulfillment`, `shipping`, `alerts`, `support`, `health` context를 중심으로 구성되어 있다.
- 각 domain feature spec은 현재 `server/contexts/*` 구현 owner 기준으로 유지된다.

## Implementation Shape

- API entrypoint는 `server/main.py`에서 통합되고, domain logic은 `server/contexts/*`에 분리된다.
- feature spec은 backend owner 기준으로 canonical domain split을 유지한다.

## Key Modules And Contracts

- `server/contexts/auth`
- `server/contexts/user`
- `server/contexts/catalog`
- `server/contexts/inventory`
- `server/contexts/orders`
- `server/contexts/fulfillment`
- `server/contexts/shipping`
- `server/contexts/alerts`
- `server/contexts/support`
- `server/contexts/health`
