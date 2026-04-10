#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AGENT_DIR="$ROOT_DIR/.agent"
PRD_FILE="$AGENT_DIR/prd.json"
PROGRESS_FILE="$AGENT_DIR/progress.txt"
RUNS_DIR="$AGENT_DIR/runs"
STATE_FILE="$AGENT_DIR/ralph-supervisor-state.json"
RALPH_RUNNER="$AGENT_DIR/ralph.sh"

max_iterations=1000
story_iterations=1
completion_promise="STORY_COMPLETE"
run_label=""
sleep_seconds=0
dry_run=0

usage() {
  cat <<'EOF'
Usage:
  .agent/ralph-supervisor.sh [options]

Options:
  --max-iterations N        Maximum global iterations across all stories. Default: 1000
  --story-iterations N      Iterations per selected story invocation. Default: 1
  --completion-promise TXT  Promise token passed to child Ralph runner
  --run-label LABEL         Optional label suffix for this supervisor run
  --sleep-seconds N         Sleep between global iterations
  --dry-run                 Use child runner in dry-run mode
  -h, --help                Show help

Behavior:
  - Picks the next pending/in_progress story from .agent/prd.json each global iteration
  - Invokes .agent/ralph.sh for one focused child loop
  - Stops when all stories complete, when max iterations are exhausted,
    or when the same story/status pair repeats 3 times with no new signal
  - Writes state to .agent/ralph-supervisor-state.json and appends monitor lines to .agent/progress.txt
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
  jq -r '
    .stories
    | map(select(.status == "in_progress" or .status == "pending"))
    | sort_by(.priority)
    | .[0].id // empty
  ' "$PRD_FILE"
}

read_story_status() {
  local story_id="$1"
  jq -r --arg id "$story_id" '.stories[] | select(.id == $id) | .status // "missing"' "$PRD_FILE"
}

write_state() {
  local iteration="$1"
  local active_story="$2"
  local child_exit="$3"
  local child_status="$4"
  local repeat_count="$5"
  local status="$6"
  local run_dir="$7"

  cat >"$STATE_FILE" <<EOF
{
  "updated_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "max_iterations": $max_iterations,
  "story_iterations": $story_iterations,
  "current_iteration": $iteration,
  "active_story": "$active_story",
  "child_exit_code": $child_exit,
  "child_status": "$child_status",
  "repeat_count": $repeat_count,
  "status": "$status",
  "run_dir": "${run_dir#$ROOT_DIR/}"
}
EOF
}

main() {
  require_file "$PRD_FILE"
  require_file "$PROGRESS_FILE"
  require_file "$RALPH_RUNNER"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --max-iterations)
        max_iterations="${2:-}"
        shift 2
        ;;
      --story-iterations)
        story_iterations="${2:-}"
        shift 2
        ;;
      --completion-promise)
        completion_promise="${2:-}"
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
  if ! [[ "$story_iterations" =~ ^[0-9]+$ ]] || [[ "$story_iterations" -lt 1 ]]; then
    echo "--story-iterations must be a positive integer" >&2
    exit 2
  fi
  if ! [[ "$sleep_seconds" =~ ^[0-9]+$ ]] || [[ "$sleep_seconds" -lt 0 ]]; then
    echo "--sleep-seconds must be a non-negative integer" >&2
    exit 2
  fi

  mkdir -p "$RUNS_DIR"
  local run_id
  run_id="$(date +%Y%m%d-%H%M%S)"
  if [[ -n "$run_label" ]]; then
    run_id="$run_id-$run_label"
  fi
  local supervisor_run_dir="$RUNS_DIR/supervisor-$run_id"
  mkdir -p "$supervisor_run_dir"

  local previous_signature=""
  local repeat_count=0
  local final_status="max_iterations_reached"

  local iteration=1
  while [[ "$iteration" -le "$max_iterations" ]]; do
    local story_id
    story_id="$(select_story)"
    if [[ -z "$story_id" ]]; then
      final_status="all_stories_completed"
      write_state "$iteration" "" 0 "none" 0 "$final_status" "$supervisor_run_dir"
      echo "$(date +%F) supervisor all-stories-complete iteration=$iteration" >>"$PROGRESS_FILE"
      break
    fi

    echo "[supervisor] iteration $iteration/$max_iterations story=$story_id"

    local child_args=(
      --story-id "$story_id"
      --max-iterations "$story_iterations"
      --completion-promise "$completion_promise"
      --run-label "supervisor-$iteration-$story_id"
    )
    if [[ $dry_run -eq 1 ]]; then
      child_args+=(--dry-run)
    fi

    set +e
    "$RALPH_RUNNER" "${child_args[@]}"
    local child_exit=$?
    set -e

    local child_status="unknown"
    if [[ -f "$AGENT_DIR/ralph-loop-state.json" ]]; then
      child_status="$(jq -r '.status // "unknown"' "$AGENT_DIR/ralph-loop-state.json")"
    fi

    local story_status
    story_status="$(read_story_status "$story_id")"
    local signature="$story_id:$child_status:$story_status"
    if [[ "$signature" == "$previous_signature" ]]; then
      repeat_count=$((repeat_count + 1))
    else
      repeat_count=1
      previous_signature="$signature"
    fi

    if [[ "$story_status" == "completed" || "$child_status" == "completed" ]]; then
      final_status="story_completed"
    elif [[ "$repeat_count" -ge 3 ]]; then
      final_status="stopped_same_signal_3x"
    elif [[ "$child_status" == "iteration_pass_no_promise" || "$child_status" == "dry_run" || "$child_exit" -eq 0 ]]; then
      final_status="iteration_ok"
    else
      final_status="iteration_failed"
    fi

    write_state "$iteration" "$story_id" "$child_exit" "$child_status" "$repeat_count" "$final_status" "$supervisor_run_dir"
    echo "$(date +%F) supervisor iteration-$iteration story=$story_id child_status=$child_status story_status=$story_status repeat=$repeat_count exit=$child_exit" >>"$PROGRESS_FILE"

    if [[ "$final_status" == "stopped_same_signal_3x" ]]; then
      break
    fi

    iteration=$((iteration + 1))
    if [[ "$iteration" -le "$max_iterations" && "$sleep_seconds" -gt 0 ]]; then
      sleep "$sleep_seconds"
    fi
  done

  echo "[supervisor] final_status=$final_status run_dir=${supervisor_run_dir#$ROOT_DIR/}"
  if [[ "$final_status" == "all_stories_completed" ]]; then
    exit 0
  fi
  if [[ "$final_status" == "stopped_same_signal_3x" ]]; then
    exit 1
  fi
  if [[ "$final_status" == "max_iterations_reached" ]]; then
    exit 1
  fi
  exit 0
}

main "$@"
