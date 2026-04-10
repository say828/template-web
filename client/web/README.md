# web

일반 사용자용 제품 앱 보일러플레이트다.

포함 패턴:

- 상단 shell + workspace content
- KPI cards
- searchable list/table
- detail side panel
- CSS variable 기반 theme surface

시작:

```bash
npm install
npm run dev
```

기본 DEV 포트는 `3001`이다.

복제 직후 초기화:

```bash
npm run ui:parity:init
```

이 단계는 repo-level contract, `ui_parity_web_contract.yaml`, route-gap manifest를 생성한다.

첫 proof 부트스트랩:

```bash
npm run ui:parity:bootstrap
```

이 단계는 build, preview, reference materialization, route-gap gate, proof gate까지 한 번에 수행한다.

패리티/하네스:

```bash
npm run ui:parity:scaffold
npm run ui:parity:materialize-references
npm run ui:parity:route-gap
npm run ui:parity:proof
```

이 템플릿은 repo root의 `sdd/99_toolchain/01_automation` 도구를 사용하고, `client/web/scripts/ui-parity-web-adapter.mjs`는 앱별 adapter 예시다.
