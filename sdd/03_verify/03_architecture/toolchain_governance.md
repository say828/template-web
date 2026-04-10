# toolchain governance verification

## Status

- pass

## Retained Checks

- `python3 sdd/99_toolchain/01_automation/run_playwright_exactness.py --list`
  - pass
  - canonical Playwright suite registry entrypoint가 현재 toolchain에 추가됐다
- `python3 sdd/99_toolchain/01_automation/run_playwright_exactness.py --suite example --base-url http://127.0.0.1:3000 --dry-run`
  - not run
  - template repo에는 아직 등록된 suite가 없어 dry-run 대상 suite는 downstream repo가 채운 뒤 검증해야 한다
- `python3 -m py_compile sdd/99_toolchain/01_automation/playwright_exactness_manifest.py sdd/99_toolchain/01_automation/run_playwright_exactness.py`
  - pass
  - Playwright exactness wrapper/manifest Python syntax가 유효하다
- `git check-ignore -v .claude/settings.local.json .agent/sdd-build-ast-audit.json .agent/runs/README.md client/admin/dist server/.venv`
  - pass
  - durable scaffold/config는 unignore 대상으로 승격했고, generated artifact는 계속 ignore 대상으로 남겼다
- `rg -n "trigger하는가|정본과 우선순위|문서 거버넌스와 산출물 원칙|Schema parity와 persistence 작업은 왜 별도 축인가|Regression verification은 왜 별도 구조를 갖는가|완료 기준을 어떻게 봐야 하는가" SDD_SKILL.md`
  - pass
  - 루트 `SDD_SKILL.md`가 `sdd` 스킬의 trigger, governance, schema parity, regression, completion gate까지 설명하도록 확장됐다
- `rg -n "Toolchain을 어떻게 봐야 하는가|Visual Fidelity를 맞추는 구조|Exactness를 맞추는 구조|기능 정합성을 맞추는 구조" SDD_SKILL.md`
  - pass
  - 루트 `SDD_SKILL.md`가 toolchain, visual fidelity, exactness, 기능 정합성 구조를 별도 섹션으로 설명한다
- `rg -n "folder structure|Feature 플로우|Screen 플로우|Architecture 플로우|Operate / Rollout 플로우" SDD_SKILL.md`
  - pass
  - 루트 `SDD_SKILL.md`가 workflow와 `sdd/` 구조, flow별 설명을 포함하도록 확장됐다
- `rg -n "sdd-dev/|screen_design_guide_builder\\.py|explicitly in scope|Do not infer rollout scope" .codex/skills/sdd .claude/skills/sdd*`
  - pass
  - stale `.codex/skills/sdd-dev/` reference가 제거됐고, rollout gate는 explicit deployment scope 기준으로 정리됐으며, 없는 design guide builder file path 고정도 제거됐다
- `test -f SDD_SKILL.md`
  - pass
  - 프로젝트 루트에 `sdd` skill 요약 entrypoint가 추가됐다
- `rg -n "brand_assets|brand asset|Brand Asset|브랜드 자산|브랜드 에셋|build_mobile_brand_assets|mobile_brand_asset_manifest|BRAND_ASSET_RECIPES" sdd/01_planning/02_screen sdd/02_plan/03_architecture sdd/03_build/03_architecture sdd/99_toolchain .codex/skills/sdd .claude/skills/sdd`
  - pass
  - template repo planning/toolchain/local skill에서 legacy brand asset naming이 제거됐다
- `git diff --check -- SDD_SKILL.md sdd/02_plan/03_architecture/toolchain_governance.md sdd/03_build/03_architecture/toolchain_governance.md sdd/03_verify/03_architecture/toolchain_governance.md .codex/skills/sdd/SKILL.md .claude/skills/sdd-dev/SKILL.md`
  - pass
- `sdd/99_toolchain/02_policies/regression-verification-policy.md`가 회귀 검수 규칙의 정본으로 추가됐다.
- `AGENTS.md`, `.codex/skills/sdd/SKILL.md`, `sdd/99_toolchain/01_automation/README.md`가 direct-only verification 금지와 selected regression surface 기록 규칙을 함께 설명한다.
- `sdd/01_planning/02_screen/assets/README.md`, `.codex/skills/sdd/SKILL.md`, `.claude/skills/sdd/SKILL.md`, `sdd/99_toolchain/01_automation/README.md`가 reusable asset planning root를 `assets/`로 일치시킨다.
- `sdd/02_plan/10_test/regression_verification.md`, `sdd/03_build/10_test/regression_verification.md`, `sdd/03_verify/10_test/regression_verification.md`가 current-state trail을 이룬다.
- `.claude/skills/sdd-dev/SKILL.md`가 현재 Codex canonical path와 section map path를 직접 가리킨다.
- `.codex/skills/sdd/SKILL.md`는 rollout scope를 `sdd/05_operate` 존재 여부가 아니라 explicit deployment scope 또는 completion policy로 해석한다.
- `.codex/skills/sdd/SKILL.md`, `sdd/99_toolchain/01_automation/README.md`, `sdd/99_toolchain/02_policies/regression-verification-policy.md`가 Playwright exactness wrapper/manifest를 canonical local gate로 함께 설명한다.
- `SDD_SKILL.md`는 루트에서 빠르게 찾는 설명 entrypoint이고, workflow/structure 설명과 canonical source 분리를 함께 명시한다.
- `SDD_SKILL.md`는 visual fidelity, exactness, 기능 정합성을 각각 분리해 설명하고, toolchain과 verify artifact가 이 셋을 어떻게 연결하는지 명시한다.
- `SDD_SKILL.md`는 이제 `sdd` 스킬 전체를 이해하기 위한 루트 해설서 역할을 하며, skill 원문 해석 전에 필요한 mental model을 제공한다.
- durable local scaffold와 generated artifact를 구분하는 ignore policy가 `.gitignore`에 반영됐다.

## Residual Risk

- regression surface selector 자동화가 아직 없어서 initial scope selection은 문서 기준/manual 판단에 의존한다.
- template repo에는 concrete Playwright suite source가 아직 없으므로, downstream repo가 harness root와 suite registry를 채우기 전까지는 runner가 empty registry 상태로 유지된다.
- rollout completion bar 해석은 여전히 저장소 정책과 사용자 요청의 명시성에 의존하므로, 배포가 애매한 요청은 시작 시 scope를 분명히 해야 한다.
- `.claude/settings.local.json`은 local override 이름을 유지하므로 downstream에서 환경별 차이가 생기면 별도 override policy 정리가 필요할 수 있다.
