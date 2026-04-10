# UI Parity Tooling

이 디렉터리는 템플릿을 복제한 각 서비스 레포에서 사용하는 repo-local parity 실행 도구의 정본이다.

계층:

- `core/`: parity 결과 생성과 공통 유틸
- `cli/`: scaffold, proof, route-gap 같은 진입점
- `contracts/`: output/metadata schema 예시
- `interfaces/`: 실행 계약과 산출물 규약 문서
- `runtime/`: 브라우저 런타임 adapter

복제 직후 초기화:

```bash
bash sdd/99_toolchain/01_automation/agentic-dev/init_frontend_parity.sh . web
```

이 명령은 다음을 생성한다.

- `sdd/99_toolchain/01_automation/agentic-dev/repo-contract.json`
- `.codex/agentic-dev.json`
- `.claude/agentic-dev.json`
- `sdd/02_plan/10_test/templates/ui_parity_web_contract.yaml`
- `sdd/02_plan/99_generated/from_planning/ui_parity/ui_parity_route_gap_report.json`
- `sdd/02_plan/99_generated/from_planning/ui_parity/ui_parity_route_gap_report.md`

대상 프론트 선택:

- 기본 대상은 `sdd/99_toolchain/01_automation/agentic-dev/repo-contract.json`의 `frontend.default_target`에서 결정한다.
- `web`, `mobile`, `admin`, `landing` 같은 각 프론트는 `frontend.targets.<id>`에 `dir`, `adapter_path`, `screens_path`, `routes_path`, `preview_url`을 선언한다.
  예시 `dir` 값은 `client/web`처럼 실제 디렉터리 경로를 가리킨다.
- `init_frontend_parity.sh`, `bootstrap_frontend_parity.sh`, `run_frontend_target.sh`는 모두 이 metadata만 읽고 동작한다.

첫 proof 부트스트랩:

```bash
bash sdd/99_toolchain/01_automation/agentic-dev/bootstrap_frontend_parity.sh . web
```

이 명령은 preview 서버를 띄운 뒤 reference materialization, route-gap gate, proof gate까지 수행한다.
`plan_audit`와 `proof` gate는 각각 route-gap/proof JSON을 schema까지 검증한 뒤 판정한다.

기본 사용 예시:

```bash
node sdd/99_toolchain/01_automation/ui-parity/cli/scaffold-contract.mjs \
  --adapter client/web/scripts/ui-parity-web-adapter.mjs \
  --out sdd/02_plan/10_test/templates/ui_parity_web_contract.yaml

node sdd/99_toolchain/01_automation/ui-parity/cli/run-proof.mjs \
  --adapter client/web/scripts/ui-parity-web-adapter.mjs \
  --contract sdd/02_plan/10_test/templates/ui_parity_web_contract.yaml \
  --out sdd/03_verify/10_test/ui_parity/templates_web_agentic_dev_latest.json
```

관련 계약:

- [UI Parity Proof Interface](interfaces/ui-parity-proof-interface.md)
- [UI Parity Route Gap Interface](interfaces/ui-parity-route-gap-interface.md)
