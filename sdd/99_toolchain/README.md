# Toolchain

`99_toolchain`은 SDD 산출물을 만들고 검증하는 generator, harness, 정책 문서를 둔다.

## Structure

- `01_automation`
  - SDD generator, parity harness, projection 문서, capture automation, agentic repo contract
- `02_policies`
  - 저장소 공통 규칙의 정본
- `03_templates`
  - 재사용 가능한 템플릿 자산

## Rule

- planning 산출물은 `01_planning`에 둔다.
- 그 planning 산출물을 생성하거나 검증하는 스크립트와 asset은 `99_toolchain`에 둔다.
- screen spec generator, capture policy, manifest는 `01_automation`에 둔다.
- 정책 문서는 `02_policies`를 정본으로 사용하고, `AGENTS.md`에는 핵심 실행 규칙만 요약한다.
- compose/runtime 기준선은 `02_policies/compose-runtime-baseline-policy.md`를 정본으로 사용한다.
- 현재 canonical screen toolchain은 `build_screen_spec_pdf.py`, `capture_screen_assets.mjs`, `screen_spec_manifest.py`다.
- Claude/Codex/Ralph 하네스는 저장소 루트 `.claude`, `.codex`, `.agent`에 두고, 그 계약 설명은 `01_automation`과 `02_policies`에 둔다.
- `sdd/03_build`는 AST-style runtime tree current-state를 유지하고, 관련 gate는 `scripts/dev/audit_sdd_build_ast.py`와 `03_verify` summary로 관리한다.
