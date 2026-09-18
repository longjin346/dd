# Publishing — the Decision Bank boundary

Everything about how a record leaves the skill. Loaded at publication, after
the five gates in `references/review.md` §8 have passed. Nothing here
decides *whether* to publish; that is settled before this file is opened.

## The boundary

`publisher/publish.py` is the only thing that writes to the Decision Bank.
The skill builds a payload, hands it over, and reads the result. It does not
know how the write happens and must not care — that is the whole point of
the split. How it reaches GitLab is its business and can change without any
rule in this skill changing.

**There is no second path, and no fallback.** Not the GitLab API, not `git`,
not a file write, not a scratch copy "so the work isn't lost", not a
different destination that happens to be reachable. If the publisher cannot
be run, the correct outcome is that nothing was written — see **When it
fails**, which is the whole of what to do about it.

## The destination is fixed, and that is the point

There is no configuration file. Host, project and branch are constants at
the top of `publish.py`:

```python
GITLAB_HOST = "https://gitlab.myteksi.net"
GITLAB_PROJECT = "long.jin/decision-capture-slack-bank"
GITLAB_BRANCH = "main"
```

**A publisher that can be pointed somewhere else is one that can be pointed
somewhere wrong**, and that is the failure with no symptom — a reviewer told
their decision is banked while it sits somewhere nobody will look. Changing where
records go is a code change, reviewed like one — not a value someone edits.

## Credentials

The publisher reads what it needs from its own environment. The skill never
reads, sets, passes, prints or logs a credential, and never puts one in the
payload or on a command line. `GITLAB_PAT_DECISIONBANK` is declared in
`SKILL.md` so the environment can be provisioned, and that declaration is
the only place the skill mentions it.

## Invocation

```
publisher/publish.py  < payload.json  > result.json
```

The payload goes in on **stdin**, the result comes back on **stdout**, and
the exit code is the verdict. Two flags exist for testing and are never used
by the skill: `--input <file>` reads the payload from a file instead of
stdin, and `--dry-run` validates and prints the paths it would write without
touching GitLab.

### What goes in

`schema.md`'s top-level object, filtered to what is actually being
published:

```json
{
  "schema_version": 4,
  "candidates": [ <every candidate confirmed `approved` and cleared by gate 3> ],
  "action_items": [ <every Action attached to one of those candidates> ],
  "no_decision_topics": [ ... ]
}
```

Candidates that gate 3 excluded are **not** in the payload. Neither is
anything still `pending` or `rejected` — the MVP publisher accepts only
`approved` (`references/schema.md`). An Action goes in whatever its optional
fields hold; an Action never blocks a publication and is never filtered out
for being sparse.

### What comes back

```json
{
  "status": "ok" | "partial" | "failed" | "not_implemented",
  "written": [ { "id": "D1", "record_url": "<permanent url>" }, ... ],
  "error": "<one sentence, when anything went wrong>"
}
```

`written` carries the permanent record for each id. Report those URLs to the
reviewer; they are what makes a save checkable afterwards.

### Exit codes

| | |
|---|---|
| `0` | every record in the payload was written |
| anything else | **nothing was written** |

**A partial write cannot happen.** Every record goes in one atomic GitLab
commit, so the Bank either has all of them or none. Validation runs before
that commit is attempted. This is why a non-zero exit can promise the Bank
is untouched rather than merely reporting that something went wrong, and it
is worth preserving in any future implementation: without it the skill would
have to reconcile a half-written Bank it cannot see.

**There is no CI and no pipeline.** The publisher performs the write itself
and returns when it is done, so there is no queued or in-flight state to
poll and no "it will land shortly". The exit code is the entire answer at
the moment it returns.

## When it fails

A missing script, a non-zero exit, a malformed result, an unrunnable
publisher, an unavailable token — all one case, and all handled the same
way:

1. **Nothing was written.** Say that plainly, in those words, with whatever
   `error` came back.
2. **The locked version is still here.** `finalized_revision` is untouched
   by a failed write, so the reviewer can retry without redoing anything.
   Say so.
3. **Do not write anywhere else.** Not to a file, not to a branch, not to a
   temp path. A record the reviewer cannot find is worse than no record,
   because they were told it exists.
4. **Do not report a success.** Never `✓ Saved to the Decision Bank` for a
   write that did not happen, and never for a write performed somewhere
   else. This has happened: a run with no publisher in reach created a local
   JSON file, watched that write succeed, and truthfully reported it as the
   Decision Bank. It never lied about a tool result — it substituted the
   destination. **A write to anything other than the Bank is not a
   publication, however successfully it completes.**

The failure text itself lives in `references/rendering.md`, like every other
message. What this file settles is that the outcome is a failure and is
reported as one.

## What it rejects

The publisher validates before it commits, and every check below fails the
whole publication rather than dropping a record. Most of them should be
unreachable — the gates in `references/review.md` §8 cover the same ground
where a reviewer can do something about it — so a failure here means a gate
was skipped or mis-scoped, not that the payload was merely imperfect.

- The payload is not a strict v4 object, or carries a field the schema does
  not define. Field sets are compared exactly, in both directions.
- A candidate is not `approved`, or its status and evidence type are not one
  of the valid pairs in `references/schema.md`.
- A candidate's `pst` is not an active value in `references/psts.json`.
- A candidate is missing `decision_title`, `decision_details`,
  `decision_proposer`, `decision_approver` or `rationale`.
- An Action names a `linked_decision_id` that is not in this payload, or two
  records would land on the same path.

**Actions are checked for shape, never for presence.** `action_owner` is a
list and may be empty; `action_due_date.resolved` may be `null`. An Action
with no owner and no date publishes exactly as the reviewer left it, because
no Action field is required at either tier (`references/schema.md`) — and
because the reference thread has one of each, so a publisher that required
them could not publish the one thread this skill has been tested on.

## After a successful write

The write is **non-overwriting**. An edited Decision is not reflected in a
record already written; re-publishing after any post-publication edit runs
all five gates again from gate 1 (`references/review.md` §8, §9).

`linked_decision_id` is derived by the publisher from what each Action
attaches to, and review-time ids such as `D1` are replaced with permanent
ones at write time. Neither is authored during review.
