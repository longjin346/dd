#!/usr/bin/env python3
"""Create linked Decision and Action files in one fixed GitLab commit.

The Decision Bank publisher. The skill hands it a finalized strict v4 output
on stdin and reads the exit code; nothing else in the skill may write, and
there is no fallback path. `references/publishing.md` holds the contract.

**It never chooses a repository or branch.** The destination is fixed in the
constants below and is deliberately not configurable — a publisher that can
be pointed somewhere else is a publisher that can be pointed somewhere
wrong, and that failure leaves no symptom.

**The write is one atomic GitLab commit.** Every record lands or none does,
so a partial write cannot happen and a non-zero exit always means the Bank
is untouched.

It sends no Slack or MCP requests.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


GITLAB_HOST = "https://gitlab.myteksi.net"
GITLAB_PROJECT = "long.jin/decision-capture-slack-bank"
GITLAB_BRANCH = "main"
TOKEN_NAME = "GITLAB_PAT_DECISIONBANK"
DEFAULT_PSTS = Path(__file__).resolve().parent.parent / "references/psts.json"
STATUSES = {"approved", "rejected", "pending"}
EVIDENCE = {"explicitly_stated", "no_objection", "none"}
VALID_STATUS_EVIDENCE = {
    ("approved", "explicitly_stated"),
    ("approved", "no_objection"),
    ("rejected", "explicitly_stated"),
    ("pending", "explicitly_stated"),
    ("pending", "none"),
}


def fail(message: str, status: str = "failed") -> None:
    """Report a failure in the shape references/publishing.md specifies.

    Nothing was written whenever this is reached: validation runs before the
    commit, and the commit itself is atomic.
    """
    print(json.dumps({"status": status, "written": [], "error": message}))
    print(f"publish.py: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        fail("publisher input is unavailable or invalid JSON")


def read_stdin_json() -> Any:
    try:
        return json.loads(sys.stdin.read())
    except (OSError, json.JSONDecodeError):
        fail("publisher input on stdin is missing or invalid JSON")


def non_blank(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def nullable_non_blank(value: Any) -> bool:
    return value is None or non_blank(value)


def iso_date(value: Any) -> bool:
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return False
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return False
    return True


def nullable_iso_date(value: Any) -> bool:
    return value is None or iso_date(value)


def active_psts(path: Path) -> set[str]:
    config = read_json(path)
    entries = config.get("psts") if isinstance(config, dict) else None
    if not isinstance(entries, list):
        fail("publisher PST configuration is invalid")
    values = {entry.get("value") for entry in entries if isinstance(entry, dict) and entry.get("active") is True}
    if not values or not all(non_blank(value) for value in values):
        fail("publisher PST configuration has no valid active values")
    return values


def validate_output(
    output: Any, allowed_psts: set[str]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    output_fields = {
        "schema_version",
        "candidates",
        "action_items",
        "no_decision_topics",
    }
    if not isinstance(output, dict) or set(output) != output_fields:
        fail("publisher input must be a strict v4 output object")
    if output["schema_version"] != 4:
        fail("publisher input must use schema_version 4")
    candidates = output.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        fail("publisher requires at least one candidate")
    review_actions = output.get("action_items")
    topics = output.get("no_decision_topics")
    if not isinstance(review_actions, list) or not isinstance(topics, list):
        fail("publisher input has invalid top-level arrays")
    if not all(non_blank(topic) for topic in topics):
        fail("publisher input has an invalid no_decision_topics entry")

    candidate_fields = {
        "candidate_id",
        "pst",
        "decision_title",
        "decision_details",
        "decision_proposer",
        "decision_approver",
        "decision_status",
        "evidence_type",
        "rationale",
        "conditions",
        "refs",
    }
    candidate_ids: set[str] = set()
    for index, candidate in enumerate(candidates, start=1):
        label = f"candidate {index}"
        if not isinstance(candidate, dict):
            fail(f"{label} must be an object")
        if set(candidate) != candidate_fields:
            fail(f"{label} does not match the v4 candidate fields")
        candidate_id = candidate["candidate_id"]
        if not isinstance(candidate_id, str) or not re.fullmatch(r"D[1-9][0-9]*", candidate_id):
            fail(f"{label} has an invalid candidate_id")
        if candidate_id in candidate_ids:
            fail("publisher input has duplicate candidate_id values")
        candidate_ids.add(candidate_id)
        if candidate["pst"] not in allowed_psts:
            fail(f"{label} has no active PST")
        if not non_blank(candidate["decision_title"]) or not non_blank(candidate["decision_details"]):
            fail(f"{label} needs a title and details")
        for field in ("decision_proposer", "decision_approver", "rationale"):
            if not non_blank(candidate[field]):
                fail(f"{label} needs {field}")
        if not nullable_non_blank(candidate["conditions"]):
            fail(f"{label} has invalid conditions")
        status, evidence = candidate["decision_status"], candidate["evidence_type"]
        if status not in STATUSES or evidence not in EVIDENCE:
            fail(f"{label} has invalid decision status or evidence type")
        if (status, evidence) not in VALID_STATUS_EVIDENCE:
            fail(f"{label} has an invalid status and evidence combination")
        if status != "approved":
            fail(f"{label} must be approved before publication")
        refs = candidate["refs"]
        if not isinstance(refs, list):
            fail(f"{label} refs must be an array")
        for ref in refs:
            if (
                not isinstance(ref, dict)
                or set(ref) != {"ref", "excerpt", "ref_type"}
                or not non_blank(ref["ref"])
                or not nullable_non_blank(ref["excerpt"])
                or ref["ref_type"]
                not in {"slack", "jira", "document", "wiki", "link"}
            ):
                fail(f"{label} has an invalid reference")

    action_fields = {
        "action_id",
        "action",
        "action_owner",
        "action_due_date",
        "linked_decision_id",
    }
    action_ids: set[str] = set()
    for index, action in enumerate(review_actions, start=1):
        label = f"action {index}"
        if not isinstance(action, dict) or set(action) != action_fields:
            fail(f"{label} does not match the v4 action fields")
        action_id = action["action_id"]
        if not isinstance(action_id, str) or not re.fullmatch(r"A[1-9][0-9]*", action_id):
            fail(f"{label} has an invalid action_id")
        if action_id in action_ids:
            fail("publisher input has duplicate action_id values")
        action_ids.add(action_id)
        if action["linked_decision_id"] not in candidate_ids:
            fail(f"{label} must link to a Candidate in this output")
        if not non_blank(action["action"]):
            fail(f"{label} needs a described task")

        # No Action field except the task itself is required, at either tier
        # (references/schema.md). An Action with no owner and no due date is
        # captured exactly as the reviewer left it and publishes as it
        # stands — it never blocks a Decision. Validate the shape of what is
        # present; never require presence.
        owners = action["action_owner"]
        if not isinstance(owners, list) or not all(non_blank(owner) for owner in owners):
            fail(f"{label} action_owner must be a list of names, empty when nobody was named")

        due = action["action_due_date"]
        if (
            not isinstance(due, dict)
            or set(due) != {"raw", "resolved"}
            or not nullable_non_blank(due["raw"])
            or not nullable_iso_date(due["resolved"])
        ):
            fail(f"{label} has an invalid action_due_date")
    return candidates, review_actions


def slug(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return (normalized or "decision")[:72].rstrip("-")


def make_actions(
    candidates: list[dict[str, Any]],
    review_actions: list[dict[str, Any]],
    today: str,
) -> tuple[list[dict[str, str]], dict[str, str], dict[str, str]]:
    actions: list[dict[str, str]] = []
    paths: set[str] = set()
    decision_ids: dict[str, str] = {}
    candidate_by_id = {candidate["candidate_id"]: candidate for candidate in candidates}
    for candidate in candidates:
        decision_id = f"D-{today.replace('-', '')}-{slug(candidate['decision_title'])}"
        path = f"decisions/{candidate['pst']}/{today[:4]}/{decision_id}.json"
        if path in paths:
            fail("publisher input creates duplicate decision paths")
        paths.add(path)
        decision_ids[candidate["candidate_id"]] = decision_id
        record = {
            "schema_version": 4,
            "decision_id": decision_id,
            **{
                key: value
                for key, value in candidate.items()
                if key != "candidate_id"
            },
        }
        actions.append(
            {
                "action": "create",
                "file_path": path,
                "content": json.dumps(record, ensure_ascii=False, indent=2) + "\n",
            }
        )

    action_ids: dict[str, str] = {}
    for review_action in review_actions:
        review_action_id = review_action["action_id"]
        candidate = candidate_by_id[review_action["linked_decision_id"]]
        action_id = (
            f"A-{today.replace('-', '')}-{slug(review_action['action'])}-"
            f"{review_action_id.lower()}"
        )
        path = f"actions/{candidate['pst']}/{today[:4]}/{action_id}.json"
        if path in paths:
            fail("publisher input creates duplicate action paths")
        paths.add(path)
        action_ids[review_action_id] = action_id
        record = {
            "schema_version": 4,
            "action_id": action_id,
            "action": review_action["action"],
            "action_owner": review_action["action_owner"],
            "action_due_date": review_action["action_due_date"],
            "linked_decision_id": decision_ids[review_action["linked_decision_id"]],
        }
        actions.append(
            {
                "action": "create",
                "file_path": path,
                "content": json.dumps(record, ensure_ascii=False, indent=2) + "\n",
            }
        )
    return actions, decision_ids, action_ids


def record_url(file_path: str) -> str:
    """A browsable address for one written record.

    The stored path keeps the PST verbatim, so most of them contain a space
    (`decisions/Pax Pricing/2026/...`). That is the Bank's layout and is left
    alone; the address quotes it, because a raw space makes a link that looks
    right and does not resolve.
    """
    quoted = urllib.parse.quote(file_path)
    return f"{GITLAB_HOST}/{GITLAB_PROJECT}/-/blob/{GITLAB_BRANCH}/{quoted}"


def commit(actions: list[dict[str, str]], message: str) -> dict[str, Any]:
    token = os.environ.get(TOKEN_NAME)
    if not token:
        fail(f"{TOKEN_NAME} is unavailable")
    endpoint = f"{GITLAB_HOST}/api/v4/projects/{urllib.parse.quote(GITLAB_PROJECT, safe='')}/repository/commits"
    payload = json.dumps({"branch": GITLAB_BRANCH, "commit_message": message, "actions": actions}).encode("utf-8")
    request = urllib.request.Request(endpoint, data=payload, headers={"PRIVATE-TOKEN": token, "Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        fail(f"Decision Bank commit failed with GitLab HTTP {error.code}")
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        fail("Decision Bank commit could not be completed")
    if not isinstance(result, dict) or not non_blank(result.get("web_url")):
        fail("Decision Bank commit returned an invalid response")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Commit confirmed v4 Slack Decisions and Actions to the fixed Decision Bank")
    parser.add_argument("--input", type=Path, help="read the payload from this file instead of stdin")
    parser.add_argument("--psts", type=Path, default=DEFAULT_PSTS, help=argparse.SUPPRESS)
    parser.add_argument("--dry-run", action="store_true", help="validate and show planned paths without a GitLab write")
    args = parser.parse_args()
    payload = read_json(args.input) if args.input else read_stdin_json()
    candidates, review_actions = validate_output(payload, active_psts(args.psts))
    today = datetime.now(ZoneInfo("Asia/Singapore")).date().isoformat()
    actions, decision_ids, action_ids = make_actions(
        candidates, review_actions, today
    )
    if args.dry_run:
        print(
            json.dumps(
                {
                    "validated": True,
                    "branch": GITLAB_BRANCH,
                    "paths": [action["file_path"] for action in actions],
                    "decision_ids": decision_ids,
                    "action_ids": action_ids,
                }
            )
        )
        return
    summary = (
        candidates[0]["decision_title"]
        if len(candidates) == 1
        else f"add {len(candidates)} decisions"
    )
    result = commit(actions, f"decision: {summary}"[:250])
    written = [
        {"id": record_id, "record_url": record_url(f"decisions/{candidate['pst']}/{today[:4]}/{record_id}.json")}
        for candidate in candidates
        for record_id in [decision_ids[candidate["candidate_id"]]]
    ]
    print(
        json.dumps(
            {
                "status": "ok",
                "written": written,
                "commit_url": result["web_url"],
                "paths": [action["file_path"] for action in actions],
                "decision_ids": decision_ids,
                "action_ids": action_ids,
            }
        )
    )


if __name__ == "__main__":
    main()
