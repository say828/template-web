# health feature spec

- 작성 버전: 1.1.0

## 1. Purpose

`health` bounded context가 제공하는 기술 상태 확인 contract를 구현 기준으로 정리한다.

## 2. Scope

- 포함 범위:
  - 무인증 liveness/status probe contract
  - runtime이 기동 중인지 확인하는 최소 운영 신호
- 제외 범위:
  - 알림 전파, auto-recovery, runbook 절차 같은 운영 후속 조치
  - business domain readiness나 데이터 정합성 검증

## 3. Actor Summary

| Actor | Description | Appears In |
| --- | --- | --- |
| `CI Runner` | CI 파이프라인에서 서버 기동과 기본 응답 계약을 확인하는 자동 검증 주체다. | `HLT-F001`, `HLT-F002` |
| `Compose Runtime` | compose healthcheck나 container supervisor처럼 주기적으로 프로브를 호출하는 런타임 주체다. | `HLT-F001`, `HLT-F002` |
| `External Monitor` | 외부 uptime/monitoring 시스템에서 서비스 생존 여부를 확인하는 감시 주체다. | `HLT-F001`, `HLT-F002` |

## 4. Bounded Context Summary

| Item | Value |
| --- | --- |
| Domain Code | `HLT` |
| Bounded Context | Technical Health |
| Primary Backend Owner | `server/contexts/health` |
| Related Context | `server/api/http/app.py` |
| Main Entry Contract | `GET /health`, `GET /api/v1/status` |

## 5. Aggregate / Model Snapshot

| Aggregate / Model | Role |
| --- | --- |
| `health_response()` | 루트 프로브 응답 생성 함수 |
| `get_status_payload()` | API prefix 하의 상태 응답 생성 함수 |

## 6. Use Case Matrix

| Feature Code | Use Case | Actor | Bounded Context | Aggregate / Model | Type | Preconditions | Domain Outcome | Invariant / Business Rule |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `HLT-F001` | 루트 health probe를 조회한다 | CI Runner, Compose Runtime, External Monitor | Technical Health | `health_response()` | Query | FastAPI app이 기동 중이어야 한다 | `{"status":"ok"}` 응답을 반환한다 | 인증 없이 호출 가능해야 한다 |
| `HLT-F002` | API status probe를 조회한다 | CI Runner, Compose Runtime, External Monitor | Technical Health | `get_status_payload()` | Query | API router가 정상 mount되어야 한다 | `{"service":"template-server","status":"healthy"}` 응답을 반환한다 | 인증 없이 호출 가능해야 한다 |

## 7. Notes

- `health`는 비즈니스 도메인이 아니라 technical bounded context지만, 운영/검증 contract를 위해 canonical feature spec에 포함한다.
