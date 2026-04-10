#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AGENT_DIR="$ROOT_DIR/.agent"
PRD_FILE="$AGENT_DIR/prd.json"
PROMPT_FILE="$AGENT_DIR/prompt.md"
PROGRESS_FILE="$AGENT_DIR/progress.txt"
RUNS_DIR="$AGENT_DIR/runs"
STATE_FILE="$AGENT_DIR/ralph-loop-state.json"

story_id=""
max_iterations=12
completion_promise="STORY_COMPLETE"
prompt_file="$PROMPT_FILE"
run_label=""
sleep_seconds=0
dry_run=0

usage() {
  cat <<'EOF'
Usage:
  .agent/ralph.sh [story_id]
  .agent/ralph.sh --story-id MOB-EXACT-AUTH-001 --max-iterations 20

Options:
  --story-id ID             Ralph story id from .agent/prd.json
  --max-iterations N        Maximum codex iterations to run
  --completion-promise TXT  Promise token to detect in codex output
  --prompt-file PATH        Base prompt markdown file
  --run-label LABEL         Optional run label for the log directory
  --sleep-seconds N         Sleep between iterations
  --dry-run                 Do not invoke codex exec; only emit prompt snapshots
  -h, --help                Show help

Behavior:
  - Select the first in_progress/pending story when no story id is given
  - Run codex exec in a loop until the completion promise is observed
  - Persist per-iteration prompt/output/status artifacts under .agent/runs/
  - Append monitor lines to .agent/progress.txt
EOF
}

require_file() {
  local file_path="$1"
  if [[ ! -f "$file_path" ]]; then
    echo "Missing required file: $file_path" >&2
    exit 1
  fi
}

select_story() {
  if [[ -n "$story_id" ]]; then
    return 0
  fi

  story_id="$(
    jq -r '
      .stories
      | map(select(.status == "in_progress" or .status == "pending"))
      | sort_by(.priority)
      | .[0].id // empty
    ' "$PRD_FILE"
  )"

  if [[ -z "$story_id" ]]; then
    echo "No open Ralph story found." >&2
    exit 1
  fi
}

load_story_payload() {
  jq -c --arg id "$story_id" '.stories[] | select(.id == $id)' "$PRD_FILE"
}

write_state() {
  local iteration="$1"
  local status="$2"
  local promise_seen="$3"
  local output_file="$4"
  local prompt_snapshot="$5"
  local exit_code="$6"
  local changed_files_json="$7"

  cat >"$STATE_FILE" <<EOF
{
  "updated_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "story_id": "$story_id",
  "max_iterations": $max_iterations,
  "current_iteration": $iteration,
  "status": "$status",
  "completion_promise": "$completion_promise",
  "promise_seen": $promise_seen,
  "last_exit_code": $exit_code,
  "prompt_snapshot": "${prompt_snapshot#$ROOT_DIR/}",
  "output_file": "${output_file#$ROOT_DIR/}",
  "changed_files": $changed_files_json
}
EOF
}

snapshot_prompt() {
  local destination="$1"
  local story_payload="$2"
  local iteration="$3"

  cat "$prompt_file" >"$destination"
  cat >>"$destination" <<EOF

Loop control:
- You are executing one iteration of a persistent Ralph loop runner.
- Current iteration: $iteration / $max_iterations
- Story id: $story_id
- Completion promise token: <promise>$completion_promise</promise>
- If and only if the requested story is actually complete and all validations pass in this iteration, print exactly:
  <promise>$completion_promise</promise>
- If the story is not complete, do not print the promise token.

Current story payload:
$(printf '%s\n' "$story_payload" | jq .)
EOF
}

append_progress_monitor_line() {
  local iteration="$1"
  local status="$2"
  local promise_seen="$3"
  local exit_code="$4"
  echo "$(date +%F) monitor iteration-$iteration story=$story_id status=$status promise=$promise_seen exit=$exit_code" >>"$PROGRESS_FILE"
}

main() {
  require_file "$PRD_FILE"
  require_file "$prompt_file"
  require_file "$PROGRESS_FILE"

  if [[ $# -gt 0 && "${1:-}" != --* ]]; then
    story_id="$1"
    shift
  fi

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --story-id)
        story_id="${2:-}"
        shift 2
        ;;
      --max-iterations)
        max_iterations="${2:-}"
        shift 2
        ;;
      --completion-promise)
        completion_promise="${2:-}"
        shift 2
        ;;
      --prompt-file)
        prompt_file="${2:-}"
        shift 2
        ;;
      --run-label)
        run_label="${2:-}"
        shift 2
        ;;
      --sleep-seconds)
        sleep_seconds="${2:-}"
        shift 2
        ;;
      --dry-run)
        dry_run=1
        shift
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        echo "Unknown argument: $1" >&2
        usage >&2
        exit 2
        ;;
    esac
  done

  if ! [[ "$max_iterations" =~ ^[0-9]+$ ]] || [[ "$max_iterations" -lt 1 ]]; then
    echo "--max-iterations must be a positive integer" >&2
    exit 2
  fi

  if ! [[ "$sleep_seconds" =~ ^[0-9]+$ ]] || [[ "$sleep_seconds" -lt 0 ]]; then
    echo "--sleep-seconds must be a non-negative integer" >&2
    exit 2
  fi

  select_story

  local story_payload
  story_payload="$(load_story_payload)"
  if [[ -z "$story_payload" ]]; then
    echo "Story not found: $story_id" >&2
    exit 1
  fi

  if [[ $dry_run -eq 0 ]] && ! command -v codex >/dev/null 2>&1; then
    echo "codex command not found in PATH" >&2
    exit 1
  fi

  mkdir -p "$RUNS_DIR"
  local run_id
  run_id="$(date +%Y%m%d-%H%M%S)"
  if [[ -n "$run_label" ]]; then
    run_id="$run_id-$run_label"
  fi
  local run_dir="$RUNS_DIR/$run_id-$story_id"
  mkdir -p "$run_dir"

  local iteration=1
  local final_status="max_iterations_reached"
  local promise_seen=false

  while [[ "$iteration" -le "$max_iterations" ]]; do
    story_payload="$(load_story_payload)"
    if [[ -z "$story_payload" ]]; then
      echo "Story disappeared from PRD: $story_id" >&2
      final_status="story_missing"
      break
    fi

    local prompt_snapshot="$run_dir/iteration-$iteration.prompt.md"
    local output_file="$run_dir/iteration-$iteration.output.log"
    local changed_files_file="$run_dir/iteration-$iteration.changed-files.txt"
    local status_file="$run_dir/iteration-$iteration.status.json"

    snapshot_prompt "$prompt_snapshot" "$story_payload" "$iteration"

    echo "[ralph] iteration $iteration/$max_iterations story=$story_id"
    echo "[ralph] prompt: ${prompt_snapshot#$ROOT_DIR/}"

    local exit_code=0
    if [[ $dry_run -eq 1 ]]; then
      printf '[ralph] dry-run: codex exec skipped\n' | tee "$output_file" >/dev/null
      final_status="dry_run"
    else
      set +e
      codex exec -s danger-full-access -C "$ROOT_DIR" - <"$prompt_snapshot" | tee "$output_file"
      exit_code=${PIPESTATUS[0]}
      set -e
    fi

    git status --short >"$changed_files_file"
    local changed_files_json
    changed_files_json="$(
      jq -R -s '
        split("\n")
        | map(select(length > 0))
      ' "$changed_files_file"
    )"

    if rg -q "<promise>${completion_promise}</promise>" "$output_file"; then
      promise_seen=true
      final_status="completed"
    elif [[ "$exit_code" -eq 0 ]]; then
      final_status="iteration_pass_no_promise"
    else
      final_status="iteration_failed"
    fi

    write_state "$iteration" "$final_status" "$promise_seen" "$output_file" "$prompt_snapshot" "$exit_code" "$changed_files_json"
    cat >"$status_file" <<EOF
{
  "iteration": $iteration,
  "story_id": "$story_id",
  "exit_code": $exit_code,
  "status": "$final_status",
  "promise_seen": $promise_seen,
  "output_file": "${output_file#$ROOT_DIR/}",
  "changed_files_file": "${changed_files_file#$ROOT_DIR/}"
}
EOF
    append_progress_monitor_line "$iteration" "$final_status" "$promise_seen" "$exit_code"

    echo "[ralph] status=$final_status exit=$exit_code promise=$promise_seen"
    echo "[ralph] changed-files: ${changed_files_file#$ROOT_DIR/}"

    if [[ "$promise_seen" == "true" ]]; then
      break
    fi

    iteration=$((iteration + 1))
    if [[ "$iteration" -le "$max_iterations" && "$sleep_seconds" -gt 0 ]]; then
      sleep "$sleep_seconds"
    fi
  done

  echo "[ralph] final_status=$final_status story=$story_id run_dir=${run_dir#$ROOT_DIR/}"

  if [[ "$final_status" == "completed" || "$final_status" == "dry_run" ]]; then
    exit 0
  fi

  exit 1
}

main "$@"
