You are running one Ralph iteration in this repository.

Rules:
1. Read `.agent/prd.json` and `.agent/progress.txt`.
2. Work only on the requested story id.
3. Lock one reproduction or validation command before editing.
4. Make one focused change set toward the requested story.
5. Re-run the requested validation commands immediately.
6. Update the matching `sdd/02_plan`, `sdd/03_build`, and `sdd/03_verify` current-state artifacts when scope changes.
7. Update `.agent/prd.json` story status and append one short line to `.agent/progress.txt`.
8. Stop after this iteration and report:
   - story id
   - validation status
   - files changed
   - next story or blocker
9. If the caller provided a completion promise token and the story is truly complete in this iteration, print that token exactly once.

Guardrails:
- Do not create a parallel `docs/` tree when `sdd/` exists.
- Do not leave execution-history narrative inside `sdd/03_build`.
- Do not claim completion without validation evidence.
