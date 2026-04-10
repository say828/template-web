# Operate Governance

## Purpose

- `sdd/05_operate/`는 현재 배포 상태, 모니터링 기준, 운영 절차를 durable 문서로 유지하는 루트다.
- raw 운영 로그나 히스토리성 release note는 남기지 않는다.

## Canonical Rule

- runbook은 절차를 설명하는 durable 문서로 유지한다.
- delivery status는 현재 live state와 확인 기준만 남기고 덮어쓴다.
- raw runtime log와 상세 incident timeline은 backend/application logging system의 역할이다.
