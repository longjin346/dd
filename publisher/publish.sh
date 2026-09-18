#!/usr/bin/env bash
#
# Decision Bank publisher — PLACEHOLDER, NOT IMPLEMENTED.
#
# This is the only thing permitted to write to the Decision Bank. The skill
# invokes it and reads its exit code; nothing else in the skill may write,
# and there is no fallback path. See references/publishing.md for the
# contract this file has to satisfy.
#
# Until it is implemented it exits 78 and writes nothing, which is the
# correct behaviour: a publish attempt reports that nothing was written and
# the locked version is still available to retry.
#
# To implement: read the payload from stdin, write each approved Decision
# and each attached Action to the Bank with the GitLab CLI, print the result
# JSON described below to stdout, and exit 0 only once every record is
# written. Credentials come from the environment this script runs in — never
# from an argument, and never from the skill.

set -euo pipefail

payload=$(cat)

cat <<JSON
{
  "status": "not_implemented",
  "written": [],
  "error": "The Decision Bank publisher is not implemented. Nothing was written.",
  "received_bytes": ${#payload}
}
JSON

echo "publisher/publish.sh is a placeholder: no records were written." >&2
exit 78
