#!/usr/bin/env bash
#
# Decision Bank publisher — PLACEHOLDER, the write is NOT IMPLEMENTED.
#
# This is the only thing permitted to write to the Decision Bank. The skill
# invokes it, hands the payload on stdin, and reads the exit code. Nothing
# else in the skill may write and there is no fallback path — see
# references/publishing.md for the contract this file has to satisfy.
#
# Configuration lives in config.env beside this file. Credentials do not:
# the token comes from the environment this script runs in, never from an
# argument and never from the skill.
#
# TO IMPLEMENT: replace the marked section below with the GitLab CLI calls
# that write each record, then print the result JSON and exit 0 only once
# every record in the payload is written. Nothing in the skill changes when
# you do.

set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
payload="$(cat)"

fail() {  # fail <status> <message>
  printf '{\n  "status": "%s",\n  "written": [],\n  "error": "%s"\n}\n' "$1" "$2"
  echo "publish.sh: $2" >&2
  exit 78
}

# --- Configuration --------------------------------------------------------

[ -f "$here/config.env" ] || fail "not_configured" \
  "publisher/config.env is missing. Nothing was written."

set -a; . "$here/config.env"; set +a

for key in BANK_HOST BANK_PROJECT BANK_BRANCH; do
  value="${!key-}"
  case "$value" in
    ""|CHANGE_ME) fail "not_configured" \
      "$key is not set in publisher/config.env. Nothing was written." ;;
  esac
done

# --- Payload --------------------------------------------------------------

command -v jq >/dev/null 2>&1 || fail "failed" \
  "jq is required to read the payload. Nothing was written."

echo "$payload" | jq -e . >/dev/null 2>&1 || fail "failed" \
  "The payload was not valid JSON. Nothing was written."

decisions=$(echo "$payload" | jq '.candidates | length')
actions=$(echo "$payload"  | jq '.action_items | length')

# --- The write ------------------------------------------------------------
# REPLACE FROM HERE.
#
# For each candidate in .candidates and each action in .action_items:
#   - assign the permanent record id
#   - resolve each action's linked_decision_id to that permanent id
#   - write it to $BANK_DECISIONS_DIR / $BANK_ACTIONS_DIR on $BANK_BRANCH
#   - collect {id, record_url} per record
#
# Then print {"status":"ok","written":[...]} and exit 0.
# Exit non-zero if any record failed — a non-zero exit means NOTHING was
# written, so roll back or leave the Bank untouched rather than exiting 0
# on a partial write.

fail "not_implemented" \
  "The Decision Bank publisher is not implemented, so none of the ${decisions} decision(s) and ${actions} action(s) were written."

# REPLACE TO HERE.
