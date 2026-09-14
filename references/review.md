# Review and publication — state, corrections, and the commit gate

This file governs everything after the first set of Decision and Action
cards is posted: how the reviewer's corrections are applied, what gets
reported back after each change, when a version is locked, and the gates in
front of committing it. It builds on `references/extraction.md` — read that
first — and does not redefine any judgment call that belongs there
(classification, field values, completeness field lists, what an Action is).

**Boundary.** This file says *when* something happens and *what it means*.
It never specifies a card layout, a template, an exact prompt string, or a
spacing rule — that is `references/rendering.md`. Where a rendered artifact
is needed, it is named (the change receipt, the finalize prompt, the full
current set, the publication preview) and left to that file. `schema.md`
defines the published record's field shapes; it is stale on one point —
Action fields as publication-required — and this file does not inherit that
part (see Publication record, below).

## 1. Review state

Four variables carry all review state. Their behavior is defined once, here,
rather than scattered across the steps that touch them.

| Variable | Values | Meaning |
|---|---|---|
| `review_state` | `reviewing` \| `finalized` | Whether the current version is still open to edits. |
| `review_revision` | integer ≥ 0 | Counts applied edit batches. Starts at 0 at the Step 3→4 handoff; incremented by exactly 1 each time a batch of edits is applied; never decremented. |
| `awaiting_finalize_revision` | **unset**, or a revision number (0 is a valid held value) | The revision currently eligible to be locked, if any. |
| `finalized_revision` | **unset**, or a revision number | The revision that was actually locked, if any. |

**Pitfall to avoid:** `awaiting_finalize_revision` and `finalized_revision`
are *tri-state* — unset, or holding a number, and 0 is a legitimate number
(a set that arrives complete on the very first response is revision 0).
Never gate finalize on a truthiness test of these variables. Gate on an
explicit "is a revision number currently held" check. A set that is complete
on arrival, at revision 0, must be finalizable exactly like one that reaches
completeness at revision 4.

### Transitions

| Event | Effect |
|---|---|
| Step 3 → 4 handoff | `review_state: reviewing`, `review_revision: 0`. Completeness is checked on this initial set exactly like after any edit batch (see §4) — this is what lets a set that arrives complete route straight to the finalize prompt without waiting for a first edit. |
| An edit batch is applied (any correction, structural operation, or template fill) | `review_revision += 1`. Recompute completeness. If complete: set `awaiting_finalize_revision` to the new revision. If incomplete: set `awaiting_finalize_revision` to unset. |
| A read-only request (show a card, show refs) | No change to any of the four variables. |
| Valid finalize confirmation | `review_state: finalized`, `finalized_revision` ← the confirmed revision, `awaiting_finalize_revision` → unset. Snapshot the publication record internally (§9). |
| A finalized set is edited | `review_state: reviewing`, `finalized_revision` → unset, then apply the edit as an ordinary batch (`review_revision += 1`, recompute completeness, etc.). |
| Publication gate 3: a candidate is **excluded** | No state change. `finalized_revision` remains valid. |
| Publication gate 3: a candidate is **corrected to approved** | Same as "a finalized set is edited," above — this is an edit, not an exclusion. |

`awaiting_finalize_revision` is only ever set in the same response that
either displays the full current set or a receipt that fully accounts for
every change since the set was last shown whole (§6). A confirmation
therefore always targets content the reviewer has actually seen — that
guarantee comes from *when* the flag is set, not from a separate rule about
disclosure.

## 2. Identifier lifecycle

A Decision or Action ID, once issued, is never reassigned to a different
record. "The next unused ID" is not computed by scanning the current set for
a gap — after a drop or a merge, that scan would reissue a retired number,
and every earlier receipt or citation that used it would now point at the
wrong record.

Instead, track one monotonically increasing counter per record type (next
Decision number, next Action number), seeded from extraction's own
thread-chronological numbering. Adding a Decision or Action — whether from a
blank template or as the product of extraction — draws the next value from
that counter and advances it. Dropping or merging away a record retires its
ID permanently; the counter never rewinds. `D2`, once gone, is never seen
again in this review.

## 3. Editing model

Corrections arrive as ordinary Slack text, and every prompt this layer sends
is answered the same way. **Never offer or require an interactive control** —
no buttons, no menus, no picker. Where a tool exists that would render a
choice as an interactive element, do not reach for it here; the numbered PST
list in §3.5 is the pattern for every bounded choice, and the reason it is a
text list is given there.

### 3.1 Resolving a target

- Identify the target Decision or Action by its visible ID.
- If the ID is omitted and exactly one Decision (or Action) exists, apply the
  edit to it and name it when reporting back.
- If omission leaves more than one plausible target, ask one concise
  clarification question before applying anything that depends on resolving
  it. Unambiguous edits elsewhere in the same reply still apply.
- **A named ID that does not exist is not a target to guess at.** Say so in
  one line, list the IDs that do currently exist, and leave everything
  unchanged for that ID — including when the reply names several targets and
  only one is unknown: apply the valid ones and report the unknown one. An ID
  can be absent because it was dropped or merged away earlier in this review
  (§2), so an unrecognised ID is often a stale reference rather than a typo.
- One reply may edit multiple Decisions and Actions in the same batch, as
  long as each target is unambiguous.

### 3.2 Normalization, before any edit is resolved

- Trim and collapse incidental whitespace around IDs, field labels, and
  controlled values (status, pst); never alter meaningful wording inside
  free-text values (`decision_details`, `rationale`, `conditions`).
- Treat ASCII `:` and full-width `：` as equivalent separators.
- Match IDs, field labels, `decision_status`, and `pst` case-insensitively;
  store and report back the canonical form.
- Ignore incidental Markdown (bullets, backticks, presentation markers) while
  parsing what the user sent.
- Never fuzzy-match a typo or invent an enum value. The one allowed
  normalization beyond exact matching is a clear morphological variant of
  `decision_status` (`approve`/`approval` → `approved`,
  `reject`/`rejection` → `rejected`, `pend` → `pending`); this does not
  extend to `pst` or any other field.
- When normalization does not resolve to exactly one target or one allowed
  value, ask one concise clarification question rather than guessing.

### 3.3 Two edit modes, one underlying rule

Corrections arrive either as natural-language statements (`D2
decision_approver is @jane`) or as a pasted, edited copy of a card. Both
reduce to the same operation: **diff the supplied values against the
currently stored ones and apply only what actually changed.**

- Preserve every field the user did not touch.
- Never delete a value merely because a pasted card omits its line — deletion
  requires an explicit instruction (`remove`, `clear`, `set to null`).
- Treat placeholder markers (an unfilled-field marker, the references
  summary line) as presentation, never as literal values to store.
- If a pasted diff exposes a probably-unintended change (for example, text
  quietly dropped from `decision_details` while being copied), flag it once
  and ask whether to keep it, rather than silently applying it.
- Ask one concise clarification question when a pasted card cannot be
  matched to a current record or parsed safely.
- Multiple targets — several pasted cards, or several natural-language
  statements — may be applied in one batch as long as every target ID in the
  batch is unique and resolvable.

### 3.4 `decision_status` edits

- An explicit `approved` or `rejected` correction sets
  `evidence_type: explicitly_stated`.
- An explicit `pending` correction sets `evidence_type: explicitly_stated`
  only when the user is confirming an actual deferral; otherwise
  `evidence_type: none`.
- Accept the normalized morphological variants from §3.2 silently, and state
  the canonical value that was stored in the change receipt.
- When the supplied value matches none of the three, or could resolve to more
  than one, leave the current status unchanged and ask the user to name one
  of `approved` / `rejected` / `pending`.
- Never infer a status change from an unrelated edit or from a finalize
  request. Only an explicit statement changes it.
- During ordinary review, `decision_status` and `decision_approver` are
  **not** coupled — see §5 for why, and where that coupling actually applies.

### 3.5 `pst` edits

- Compare the trimmed, case-insensitive supplied value against the active
  values in `references/psts.json`.
- Exactly one match: store its canonical configured spelling and report that
  spelling back.
- No match: leave the existing `pst` unchanged (or unresolved, for a new
  Decision), state that the supplied value is not an active option, and list
  the active values as a numbered list in configured order.
- While such a numbered prompt is active, accept a bare 1-based number as the
  selection, resolved against that same list; reject an out-of-range number
  by showing the list again. Never treat a bare number as a `pst` selection
  when no such prompt is currently active.
- **The numbered text list is deliberate — do not substitute an interactive
  picker for it.** The Slack adapter renders a large option set as rows of
  buttons plus an `Other…` overflow rather than as a dropdown, which for the
  full PST list is worse to read and worse to answer than a numbered list a
  user can reply to with one character.
- Never select the closest-looking value, invent a new one, or edit the
  configuration.

### 3.6 Structural operations on Decisions

- **Merge** (`D1 and D3 are the same`): keep the lower ID, discard the
  higher one. For each field, take the value from the card named first (or,
  named symmetrically, the lower-ID card); where the two conflict on a
  substantive field such as `decision_status`, surface the conflict as one
  question and wait rather than guessing. Union and deduplicate `refs`.
  Every Action that was attached to the discarded ID now attaches to the
  retained one — automatically, since the Action's link is positional, not a
  value to reconcile.
- **Confirm an Uncertain Decision** (`D2 should be treated as a Decision`):
  set `decision_classification: decision`. Change nothing else — status,
  evidence, and every stored field still reflect the thread evidence exactly
  as extracted.
- **Drop a Decision** (`Drop D1`): remove it, and with it every Action
  attached to it. This is not a cascade rule bolted onto a relational model —
  an Action is part of its Decision, so removing the Decision removes what it
  contains. There is nothing left over to orphan or clean up.
- **Add a Decision from a blank template** (`add a decision`): the user's
  request is itself the human confirmation that this is a Decision —
  initialize `decision_classification: decision` immediately; never ask
  again or raise it as a separate uncertainty. The fields the template asks
  the user to fill are exactly the **finalize-required** set from
  extraction.md — title, details, pst, proposer, rationale, status.
  `decision_approver` is never demanded here, for the same reason it is
  never demanded anywhere during ordinary review: it is not required to
  finalize. Offer `decision_approver`, `conditions`, and `refs` as optional.
  Do not extract, infer, or prefill any value for a manually added Decision;
  it is subject to every ordinary completeness, finalize, and publication
  rule from that point on.

### 3.7 Operations on Actions

Because an Action is an attribute of exactly one Decision rather than an
independent record, there is no relink-with-integrity-check operation, no
orphan category, and no cascade rule to maintain beyond "it moves and is
removed with its parent." What remains are four plain edits:

- **Add** (`add an action`): establish its parent Decision at creation —
  either named by the user, or the sole current Decision, or, if genuinely
  ambiguous, resolved by one clarification question (§3.1). No field on the
  new Action is required: owner and due date are both optional to fill, same
  as an extracted Action. An Action is never created in an unlinked state —
  that state does not exist in this model.
- **Edit** (`A1 action_owner is @jane`): resolve by `action_id` regardless of
  which Decision currently holds it; apply the change; no field is ever
  required to keep the Action valid.
- **Move** (`Link A1 to D2`): change which Decision the Action attaches to.
  This is an ordinary edit to the parent pointer, resolved the same way any
  target ID is resolved — not a special "relink" operation, because the
  pointer is definitionally always valid once resolved: you are naming an
  existing Decision, nothing more.
- **Drop** (`Drop A1`): remove the single Action. Nothing else references it.

## 4. Completeness and the missing-fields prompt

After every applied edit batch (including the initial Step 3→4 handoff),
recompute completeness against the **finalize-required** field set defined
in extraction.md, across every current Decision.

- **Actions are never checked.** An Action has no required field at either
  tier (extraction.md), so it can never be incomplete and never appears in a
  missing-fields prompt. Running a completeness pass over Actions is dead
  work with no possible finding — don't do it.
- Incomplete: keep `review_state: reviewing`, set `awaiting_finalize_revision`
  to unset, and end the response with one consolidated prompt listing every
  missing finalize-required field, grouped by Decision, with its ID and field
  key. Never list `decision_approver` here — it is not in this set. Never ask
  the user to fill an optional field.
- Complete: set `awaiting_finalize_revision` to the current revision and
  issue the finalize prompt (§7). Apply the render rule in §6 to decide
  whether the full set accompanies it.
- Never show the missing-fields prompt and the finalize prompt in the same
  response — a revision is either missing something or ready to lock, never
  presented as both.
- If a correction plainly contradicts a cited excerpt, point out the
  conflict once, then apply whatever the user decides.

## 5. Where the approver/status coupling lives

`decision_approver` is not in the finalize-required set (extraction.md): a
`pending` candidate the thread never resolved is a complete, honest record
without one. So during ordinary review, naming an approver on a `pending`
candidate does **not** trigger a follow-up question about status, and
setting `decision_status: approved` does **not** trigger a follow-up
question about the approver. Apply each edit at face value. A named approver
may sit quietly on a candidate the reviewer still wants to keep `pending`.

The coupling itself — that these two fields bear on each other — is still
correct reasoning. It resurfaces at exactly the point where it stops being
optional: **Publication gate 3** (§8), because the publisher accepts only
`approved` candidates and an `approved` candidate cannot lack an approver
(publish-required = finalize-required + `decision_approver`). When a
candidate is corrected to `approved` at that gate, resolve its approver in
the same response — never split the pair across two turns there, since by
then both are genuinely required together.

## 6. What gets rendered, and when

One rule replaces the branching that used to decide between a receipt, a
single card, or the whole set.

- **A receipt follows every applied edit batch.** Always. It names every
  structural change (add, drop, merge, confirm) before any field-level
  change, and every field-level change with its prior and new value. It
  mentions uncertainty only when this batch changed a candidate's uncertain
  state.
- **The full current set renders in addition to the receipt at exactly two
  moments** — both are moments where the reviewer is about to be asked to
  lock or commit a version whose *current, complete* contents they have not
  yet been shown whole:
  1. Whenever `awaiting_finalize_revision` is being set for a revision the
     reviewer has not already seen in full — that is, this batch is the one
     that first reaches completeness, or membership changed since the set
     was last shown whole (a Decision or Action was added, dropped, or
     merged away), even if the set was already complete. A batch that only
     changes field values on a set the reviewer has already seen whole does
     **not** re-trigger this: the receipt is a complete, legible delta
     against a baseline they already have. The governing test is *has the
     reviewer seen this revision whole*, not *did completeness just change*.
     A set that arrives already complete at the Step 3→4 handoff was shown
     whole by the cards themselves, so it takes the finalize prompt alone,
     with no second render.
  2. Immediately before the publication confirmation (Step 5 gate 4),
     unconditionally — because gate 3's exclusions and corrections can
     change what is actually about to be committed relative to what was
     last shown, and because this step is irreversible.
- **Confirming finalize renders nothing new.** The full set was just shown as
  part of setting `awaiting_finalize_revision` in the same turn the
  confirmation responds to; acknowledge the lock by referencing that
  already-disclosed revision rather than repeating it. This removes the
  redundant echo between the finalize prompt and the finalize confirmation —
  the set is shown once before the lock (point 1 above) and once before the
  commit (point 2 above), never a third time in between.
- **Anything else is on request** — a named card, a candidate's references,
  or the whole set — and never changes `review_revision`, completeness, or
  either finalize/publication flag.

## 7. The finalize gate

**Preconditions:** `review_state: reviewing` and `awaiting_finalize_revision`
holds a revision number (§1's tri-state rule — 0 counts).

**Confirmation:** an explicit reply whose clear meaning is "lock this exact
version" (e.g. an unambiguous finalize/lock instruction). An unanchored
"yes," an earlier approval, silence, or a reaction is never a confirmation.

**Binding:** the confirmation applies only to the revision currently held in
`awaiting_finalize_revision`. If a further edit lands first, that value has
already moved (or gone unset); a confirmation arriving after cannot reach
back and lock the stale revision.

**Early confirmation** (no finalize prompt currently active): treat it as a
request to run the completeness check now, not as a confirmation in itself.
Incomplete → ask for the gaps (§4); complete → this is the moment
completeness was reached, so render the full set and set
`awaiting_finalize_revision` per §6, and still wait for an actual
confirmation before locking.

**Finalize + save in one reply** (e.g. "yes, finalize and save to the
bank"): satisfies this gate and Publication gate 2 (§8) simultaneously.
Publication gates 3–5 are still required afterward in full — this reply is
not a shortcut past them.

**On success:** `review_state: finalized`; `finalized_revision` ← the
confirmed revision; `awaiting_finalize_revision` → unset. Snapshot the
publication record (§9) internally. Per §6, do not re-render the full set as
part of this response.

**Editing a finalized set:** return to `review_state: reviewing`,
`finalized_revision` → unset, and apply the new reply as an ordinary edit
batch under §3–§6 — including asking to finalize again if the result is
complete. Never publish against an unset or superseded `finalized_revision`.

## 8. The publication gate

Publishing a finalized set to the Decision Bank requires five gates, in
order, all required.

1. **Still finalized.** `finalized_revision` equals the current
   `review_revision`, `review_state` is `finalized`, and no edit has
   reopened review since.
2. **Explicit save request.** The user has explicitly asked to save/commit/
   store to the bank in this conversation. Never infer it from a vague
   acknowledgement, and never from the original capture request itself.
3. **Every non-approved candidate is resolved by a human.** A candidate
   still `uncertain`, `pending`, or `rejected` must be either:
   - **Excluded from this publication.** No record changes. `finalized_revision`
     stays valid because nothing about the finalized state changed — this
     candidate simply isn't part of what gets committed *this time*; it
     remains in the finalized review for a possible later attempt. Proceed
     straight to gate 4 and carry the exclusion (with its reason) into the
     preview.
   - **Corrected to `approved`.** This edits the finalized record, so it
     reopens review exactly like any other post-finalize edit (§7's
     "editing a finalized set"): gate 1 now fails by construction and must
     be earned again. Because `approved` pulls `decision_approver` into the
     required set, resolve the approver in the same response if it isn't
     already named — this is the one place the §5 coupling applies. Recompute
     completeness, obtain a fresh finalize confirmation (full render, per
     §6's first moment), then re-enter gate 3 for whatever, if anything,
     still needs resolving. The save request from gate 2 still stands across
     this loop — never make the user ask to save a second time, only to
     re-confirm the version — and say plainly why re-confirmation is being
     asked for: the correction changed the record that was locked.
   Never silently drop an unresolved candidate from the preview and never
   treat silence as approval.
4. **Preview the exact publishable set.** Render the full, current
   publishable set — unconditionally, per §6's second moment — including
   every item excluded under gate 3 and its reason.
5. **One confirmation, bound to that exact preview.** The confirmation
   applies only to the set and `finalized_revision` just previewed. Never
   alter a field or re-run reasoning silently between preview and commit; a
   reply that changes something restarts from the gate it affects instead of
   proceeding.

**Field check before gate 5 can be satisfied:** every candidate in the
previewed set carries the full publish-required set (finalize-required +
`decision_approver`, per extraction.md) and `decision_status: approved`.
Every Action attached to a publishing Decision publishes regardless of which
of its optional fields — owner, due date — are filled; nothing about an
Action ever blocks this gate.

## 9. Publication record and post-publication editing

At finalize, snapshot the publication-ready record internally: every
Decision field from `schema.md`'s shape plus `decision_status` and
`evidence_type`, with internal-only bookkeeping dropped — classification,
its reason and refs, completeness fields, and every variable from §1.
`no_decision_topics` is kept; `source_limitations` has no field in the
published schema, so surface it as accompanying visible text instead of
folding it into the record.

**Override schema.md on Actions.** Per extraction.md, an Action carries no
required field at any tier. `schema.md`'s Action-required-fields list is
stale and does not apply here — do not enforce it at finalize or at
publication. An Action with no owner and no due date is captured and
published exactly as the reviewer left it, attached to its Decision through
the permanent ID the publisher derives from position at commit time (never a
value authored or corrected during review).

**Mechanics kept at policy level:** only the whitelisted publisher may ever
write to the Bank — never the GitLab API or `git` directly, and never a
substituted script or destination. The publishing credential is passed only
to that publisher and never printed or logged. The write is non-overwriting.
An edited Decision or Action is not automatically reflected in a prior
commit; re-publishing after any post-commit edit requires all five gates
again, from gate 1.

## 10. Worked check against the reference thread

- **D1** (uncertain, `pending`, no approver, unmet eng-PIC condition):
  finalizes as drafted — every finalize-required field is present, and the
  empty approver does not block it (§4–§5). At the publication gate (§8
  gate 3) it is resolved either by exclusion — D2 still publishes, and the
  finalization survives untouched — or by correcting it to `approved`,
  which requires naming an approver in that same reply, reopens review, and
  requires a fresh finalize before gate 3 can be re-entered.
- **D2** (`approved`, approver `@albert.lim`): satisfies publish-required
  outright and moves through the gate cleanly once gates 1–2 hold.
- **Actions with no owner and no date** (several, attached to both D1 and
  D2): never appear in a missing-fields prompt, never block finalize, never
  block publication — per §4 and §8's field check, exactly as extraction.md
  requires.
