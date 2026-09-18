# Publishing — the Decision Bank boundary

Everything about how a record leaves the skill. Loaded at publication, after
the five gates in `references/review.md` §8 have passed. Nothing here
decides *whether* to publish; that is settled before this file is opened.

## The boundary

`publisher/publish.sh` is the only thing that writes to the Decision Bank.
The skill builds a payload, hands it over, and reads the result. It does not
know how the write happens and must not care — that is the whole point of
the split. Whether the publisher uses the GitLab CLI, the API, or something
else is its business and can change without any rule in this skill changing.

**There is no second path, and no fallback.** Not the GitLab API, not `git`,
not a file write, not a scratch copy "so the work isn't lost", not a
different destination that happens to be reachable. If the publisher cannot
be run, the correct outcome is that nothing was written — see **When it
fails**, which is the whole of what to do about it.

## Configuring the Bank

`publisher/config.env` holds three values — project path, branch, and an
optional host — and nothing else. It is sourced by `publish.sh`, so every
value is quoted; an unquoted one containing a space or a colon breaks the
source.

**Only what differs between deployments is configured.** Directory names,
the filename pattern and the push message are the publisher's own decisions
and sit at the top of `publish.sh`, visible and editable there. A setting
nobody varies is one more thing that can be set wrong or drift out of step
with the code — the mirror of the `presentation.yaml` lesson, where a file
nothing read was decorative.

`BANK_PROJECT` ships as `CHANGE_ME` and **the publisher refuses to run
while it is unset.** A half-configured publisher that guesses a destination
is the failure this whole boundary exists to prevent, and it is the one
that leaves no symptom. It fails the same way an absent publisher does, and
the reviewer is told the same thing — nothing was written.

The file is committed and contains nothing secret.

## Credentials

The publisher reads what it needs from its own environment. The skill never
reads, sets, passes, prints or logs a credential, and never puts one in the
payload or on a command line. `GITLAB_PAT_DECISIONBANK` is declared in
`SKILL.md` so the environment can be provisioned, and that declaration is
the only place the skill mentions it.

## Invocation

```
publisher/publish.sh  < payload.json  > result.json
```

The payload goes in on **stdin**, the result comes back on **stdout**, and
the exit code is the verdict. Nothing is passed as an argument.

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
| anything else | **nothing was written**, whatever `status` says |

Treat a non-zero exit as authoritative over the body. A publisher that
half-wrote and exited non-zero is reporting a failed publication, and the
skill says so; reconciling a partial write is the publisher's problem, not
something to guess at from here.

**There is no CI and no pipeline.** The publisher performs the write itself
and returns when it is done, so there is no queued or in-flight state to
poll and no "it will land shortly". The exit code is the entire answer at
the moment it returns.

## When it fails

A missing script, a non-zero exit, a malformed result, an unrunnable
publisher — all one case, and all handled the same way:

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

## After a successful write

The write is **non-overwriting**. An edited Decision is not reflected in a
record already written; re-publishing after any post-publication edit runs
all five gates again from gate 1 (`references/review.md` §8, §9).

`linked_decision_id` is derived by the publisher from what each Action
attaches to, and review-time ids such as `D1` are replaced with permanent
ones at write time. Neither is authored during review.
