# Support And Observability

## Covered Planning Artifacts

- `sdd/01_planning/01_feature/alerts_feature_spec.md`
- `sdd/01_planning/01_feature/support_feature_spec.md`
- `sdd/01_planning/01_feature/health_feature_spec.md`

## Implemented Scope

- admin alerts, support content, health probe baseline은 `alerts`, `support`, `health` context로 분리되어 있다.
- admin surface는 alerts/support current contract를, runtime baseline은 health probe를 사용한다.

## Implementation Shape

- backend owner는 `server/contexts/alerts`, `server/contexts/support`, `server/contexts/health`다.
- frontend는 admin 중심의 typed API와 status surface로 current contract를 노출한다.

## Current Behavior

- 템플릿은 운영 알림, 고객지원, health probe baseline을 current implementation 예시로 제공한다.
