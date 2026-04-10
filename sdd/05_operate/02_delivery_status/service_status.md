# service status

## Current Live State

- template repo는 root compose/developer baseline 기준의 current buildable state를 유지한다.
- production release timeline은 SDD에 누적하지 않는다.

## Monitoring Baseline

- backend `pytest`
- frontend app build
- parity harness current output path 확인

## Residual Risk

- 실제 서비스 레포에 이식할 때는 각 서비스의 runtime/edge 기준으로 다시 구체화해야 한다.
