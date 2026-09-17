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
current set, the save message) and left to that file. `schema.md`
defines the published record's field shapes, and this file follows it.

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
| Publication gate 3: a candidate is **corrected** (set to `approved`, or its awaited approver resolved) | Same as "a finalized set is edited," above — this is an edit, not an exclusion. |

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
ID permanently; the counter never rewinds. No other record ever becomes
`D2`.

**Retired is not the same as destroyed.** A dropped or merged-away record is
withdrawn from the set, not deleted: it stops rendering, stops counting
toward completeness, and cannot be published, but it is kept and can be
restored by its own ID for the rest of the review (§3.6). Restoring is not a
reassignment — the ID returns to the same record it always named, which is
exactly what the rule above protects. What the rule forbids is `D2` coming
back as something else.

This retention lives in the conversation, like every other piece of review
state; the skill keeps no store of its own. It lasts as long as the review
does and no longer, which is the one thing a user must not be left guessing
about — say so when it matters rather than implying a permanent undo.

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
  it. Unambiguous edits elsewhere in the same reply still apply. Every
  clarification this file calls for shares the one question block described
  in `references/rendering.md` — one per reply, however many edits raised a
  question.
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

- **Merge** (`D1 and D3 are the same`): keep the lower ID, withdraw the
  higher one. Where the two conflict on a field that carries a single
  settled answer — `decision_status`, `pst`, `decision_approver`,
  `decision_proposer` — surface the conflict as one question and wait rather
  than guessing.

  **The accumulating fields union rather than overwrite.** `refs` already
  did; `rationale` and `conditions` join it, deduplicating strands that say
  the same thing. The reasoning is extraction.md's own: a rationale is
  supposed to carry every distinct reason the thread gave, from whoever gave
  it. Two cards the reviewer says are the same decision are two readings of
  one decision, so both sets of reasons are about it — taking only the
  first-named card's would discard half the case the moment someone tidies
  up the set, which is exactly the loss that rule exists to prevent.

  For every remaining field, including `decision_details`, take the value
  from the card named first (or, named symmetrically, the lower-ID card),
  and **name any non-empty value that was displaced in the receipt** — a
  merge must never quietly throw away text the user can see on screen one
  message earlier.

  Every Action that was attached to the withdrawn ID now attaches to the
  retained one — automatically, since the Action's link is positional, not a
  value to reconcile. The withdrawn card itself is kept and restorable, as
  with any drop.
- **Confirm an Uncertain Decision** (`D2 should be treated as a Decision`):
  set `decision_classification: decision`. Change nothing else — status,
  evidence, and every stored field still reflect the thread evidence exactly
  as extracted.
- **Drop a Decision** (`Drop D1`): withdraw it from the set, and with it
  every Action attached to it. This is not a cascade rule bolted onto a
  relational model — an Action is part of its Decision, so withdrawing the
  Decision withdraws what it contains. There is nothing left over to orphan
  or clean up.

  Withdrawn, not destroyed (§2). It stops rendering, stops counting toward
  completeness, and cannot be published; its content and its Actions are
  kept intact so the drop can be taken back. No confirmation is asked
  first — the receipt already reports the drop and the Actions that went
  with it, and a reported, reversible action does not need a round-trip in
  front of it.
- **Restore a Decision** (`Restore D1`, `undo that drop`, `put D1 back`):
  return a withdrawn Decision to the set, with every field and every Action
  exactly as they were. This matters most for what a user cannot retype:
  `refs` are permalinks the acquisition layer collected, so a destroyed
  Decision's evidence trail could only be recovered by re-running the whole
  capture.

  It is an ordinary edit batch — `review_revision += 1`, recompute
  completeness — and on a finalized set it reopens review exactly like any
  other post-finalize edit (§1). Restoring something that is already in the
  set, or an ID that never existed, is refused the same way any unresolvable
  target is (§3.1), not silently ignored. A restored Decision is subject to
  every ordinary completeness, finalize, and publication rule from that
  point on; nothing about having been away exempts it.
- **Add a Decision from a blank template** (`add a decision`): the user's
  request is itself the human confirmation that this is a Decision —
  initialize `decision_classification: decision` immediately; never ask
  again or raise it as a separate uncertainty. The fields the template asks
  the user to fill are exactly the **required** set from extraction.md —
  title, details, pst, proposer, rationale, status, approver. Nothing is
  populated on the reviewer's behalf here — they are supplying every field —
  and `decision_approver` is required the same as any other field: whoever
  actually approved it, or, if nobody has yet, whoever it is awaiting,
  written with the same inline awaited marker extraction.md defines. Offer
  `conditions` and `refs` as optional. Do not
  extract, infer, or prefill any value for a manually added Decision; it is
  subject to every ordinary completeness, finalize, and publication rule
  from that point on.

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
- **Drop** (`Drop A1`): withdraw the single Action. Nothing else references
  it. Withdrawn, not destroyed, exactly as for a Decision (§2) — `Restore
  A1` brings it back to the Decision it was attached to, or, if that
  Decision has itself been withdrawn, restoring the Decision brings its
  Actions with it.

## 4. Completeness and the missing-fields prompt

After every applied edit batch (including the initial Step 3→4 handoff),
recompute completeness against the **required** field set defined in
extraction.md, across every current Decision — meaning the ones in the set,
never a Decision that has been withdrawn by a drop or a merge (§3.6). A
withdrawn record holds no completeness claim on the set it is not part of,
and restoring one brings its unfilled required fields back with it.

- **Actions are never checked.** An Action has no required field at all
  (extraction.md), so it can never be incomplete and never appears in a
  missing-fields prompt. Running a completeness pass over Actions is dead
  work with no possible finding — don't do it.
- Incomplete: keep `review_state: reviewing`, set `awaiting_finalize_revision`
  to unset, and end the response with one consolidated prompt listing every
  missing required field, grouped by Decision, with its ID and field key.
  `decision_approver` appears here like any other unfilled field, whenever
  extraction's fallback ladder (`references/extraction.md`) reached rung 3 —
  the thread established neither who approved the candidate nor who is
  awaited to. That is the exception, not the common case: most candidates
  the thread never closed still name an addressee, a gatekeeper, or a
  required sign-off role, which rung 2 already captures before this prompt
  is ever reached. When it does appear here, the question states plainly
  what is wanted — who approved this, or who it is awaiting
  (`references/rendering.md`). Never ask the user to fill an optional field.
- Complete: set `awaiting_finalize_revision` to the current revision and
  close the reply with the finalize prompt (§7). The cards do not accompany
  it — §6 keeps them for the save message.
- Never show the missing-fields prompt and the finalize prompt in the same
  response — a revision is either missing something or ready to lock, never
  presented as both.
- If a correction plainly contradicts a cited excerpt, point out the
  conflict once, then apply whatever the user decides.

## 5. Where the approver/status coupling lives

`decision_approver` is required, same tier as every other field
(extraction.md). When the thread closed the candidate, extraction fills it
with whoever closed it; when nobody has closed it yet but the thread says
who is supposed to, extraction fills it with that party, marked as awaited;
only when the thread establishes neither does it arrive unresolved for the
missing-fields prompt to ask for (§4). Either way the reviewer settles it
before finalize, so by the time anything downstream reads the field it holds
a deliberate value rather than an assumed one. During ordinary review,
naming a different approver on a `pending` candidate does **not** trigger a
follow-up question about status, and setting `decision_status: approved`
does **not** by itself trigger a follow-up question about the approver.
Apply each edit at face value. A named approver may sit quietly on a
candidate the reviewer still wants to keep `pending`, and a candidate may
sit with `decision_approver` still marked awaited while its status reads
`approved` — the ordinary edit path never blocks either.

The coupling itself — that these two fields bear on each other — is still
correct reasoning. It resurfaces at exactly the point where it stops being
optional: **Publication gate 3** (§8), because the publisher accepts only
`approved` candidates, and an `approved` candidate whose `decision_approver`
still carries the awaited marker is a contradiction, not an honest gap. When
a candidate is corrected to `approved` at that gate (or is already
`approved` with `decision_approver` still marked awaited when gate 3 is
reached), resolve the approver to who actually approved in the same
response — never split the pair across two turns there, since by then both
are genuinely required together.

## 6. What gets rendered, and when

One rule replaces the branching that used to decide between a receipt, a
single card, or the whole set.

- **A receipt follows every edit batch.** Always — whether the batch applied
  in whole, in part, or not at all. It names every structural change (add,
  drop, restore, merge, confirm) before any field-level change, and every
  field-level change with its prior and new value. It mentions uncertainty
  only when this batch changed a candidate's uncertain state. Edits this layer refuses
  outright, and the questions it needs answered before applying the rest,
  travel in the same reply — `references/rendering.md` owns their blocks and
  the order the three appear in. A batch that applied nothing still gets a
  reply.
- **Editing never renders the full set.** However many candidates a batch
  adds, drops, restores or merges, the reply is the receipt. The reviewer
  reads deltas while they work and sees the whole thing once, at the point
  it decides something.

  This replaces a rule that tried to work out whether the reviewer had
  "seen this revision whole", which needed a maintained list of what counts
  as a membership change — and that list went stale the moment `Restore`
  was added to §3.6 without being added to it. A rule that has to enumerate
  operations will keep going stale as operations are added.
- **A finalize confirmation renders the full set, and asks for the save in
  the same message.** One test decides whether the cards are repeated: has
  any edit batch been applied since the set was last shown whole? If yes,
  render it. If no — the reviewer confirmed straight off the first card
  set, changing nothing — the cards are one message up, so send the save
  message without them.

  That message carries three things in order: the cards (per the test
  above), every candidate that cannot be published as it stands, and the
  request to save. `references/rendering.md` owns its text. Folding them
  together is what makes the sequence honest — the reviewer is looking at
  the complete record at the moment they are asked whether it should be
  written, rather than approving a lock and then discovering, several
  messages later, that one candidate was never publishable.
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
Incomplete → ask for the gaps (§4). Complete → set
`awaiting_finalize_revision` and send the finalize prompt, then wait for an
actual confirmation before locking. Do not shortcut into the save message on
the strength of a confirmation given before there was anything to confirm.

**Finalize + save in one reply** (e.g. "yes, finalize and save to the
bank"): satisfies this gate and Publication gate 2 (§8) simultaneously.
Publication gates 3–5 are still required afterward in full — this reply is
not a shortcut past them. The message that follows is the same one, with one
difference: the save has already been asked for, so it closes by asking the
reviewer to confirm what they are now looking at rather than to request a
save they have already requested.

**On success:** `review_state: finalized`; `finalized_revision` ← the
confirmed revision; `awaiting_finalize_revision` → unset. Snapshot the
publication record (§9) internally. Then send the message §6 describes: the
full set (unless nothing has been edited since it was last shown whole),
every candidate that cannot be published as it stands, and the request to
save.

There is no bare acknowledgement of the lock. A message that says only "this
version is locked" leaves the reviewer at the one point in the flow with
nothing telling them what happens next — and they have just done everything
they believe was asked of them, so they have no reason to expect a further
step. The save request *is* the acknowledgement.

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
3. **Every candidate that cannot be published as it stands is resolved by a
   human.** Two things put a candidate here, and the predicate is the same
   one the save message and Review Notes' `Complete, but not a decision yet`
   have been using since the first card set
   (`references/rendering.md`) — deliberately, so a reviewer is never asked
   about a different set than the one they were shown:
   - `decision_status` is not `approved` — `pending` or `rejected`. Every
     candidate still classified `uncertain` is here already: the valid
     combinations in extraction.md pair `uncertain` only with `pending`.
   - `decision_status` is `approved` but `decision_approver` still carries
     the awaited marker. An `approved` candidate whose approver was never
     given is a contradiction, not a gap (§5), and it belongs here rather
     than at gate 5: this gate has a way to resolve it and gate 5 only has a
     way to fail.

   Either way the candidate must be:
   - **Excluded from this publication.** No record changes. `finalized_revision`
     stays valid because nothing about the finalized state changed — this
     candidate simply isn't part of what gets committed *this time*; it
     remains in the finalized review for a possible later attempt. Proceed
     straight to gate 4 and carry the exclusion (with its reason) into the
     preview.
   - **Corrected.** Set to `approved`, or — for a candidate already
     `approved` — the awaited approver resolved to who actually approved.
     Either edits the finalized record, so it
     reopens review exactly like any other post-finalize edit (§7's
     "editing a finalized set"): gate 1 now fails by construction and must
     be earned again. `decision_approver` was already required and already
     populated before this edit, but an `approved` candidate cannot honestly
     carry an approver still marked awaited — if it still carries that
     marker, resolve it to who actually approved in the same response — this
     is the one place the §5 coupling applies. Recompute completeness,
     obtain a fresh finalize confirmation, then re-enter gate 3 for
     whatever, if anything, still needs resolving. Gate 4 governs what that
     re-confirmation shows: the corrected cards, not the whole set. The save request from
     gate 2 still stands across this loop — never make the user ask to save
     a second time, only to re-confirm the version — and say plainly why
     re-confirmation is being asked for: the correction changed the record
     that was locked.
   Never silently drop an unresolved candidate from the preview and never
   treat silence as approval.

   **They were already named, and they were named early.** Every candidate
   that cannot be published as it stands is listed in the save message §7
   sends, and flagged in Review Notes from the first card set onward
   (`references/rendering.md`). This gate is not where the reviewer finds
   out — it is where they answer. A candidate reaching it is never news.

   **Take every resolution in one batch.** A single reply may mix them —
   exclude one, approve another — and where any was corrected to `approved`,
   the reopen-and-re-finalize loop above runs once for the batch, not once
   per candidate. Handling them one at a time would multiply that loop by
   however many are unresolved, for a reply the reviewer could have written
   once. Re-enter the gate only for what the reply left unresolved.
4. **The reviewer has seen what is about to be written.** The save message
   §7 sends showed the full set, and gate 3's items were named in it. So
   this gate asks only whether anything has changed since — and exactly one
   thing can have: a gate-3 resolution that corrected a candidate — set to
   `approved`, or its awaited approver resolved to who actually approved.

   - **Nothing changed.** An exclusion changes no record, so what is about
     to be written is what was shown. Proceed to gate 5.
   - **A candidate was corrected.** What gets written is no longer what was
     shown. Re-render the cards that changed, and ask for one more
     confirmation against them. Never carry the earlier confirmation across
     a correction — it was given for a different set.

   Do not re-render the whole set for this. A reviewer who just corrected
   one candidate needs to see that candidate, not a repeat of the rest.
5. **One confirmation, bound to what was last shown.** The confirmation
   applies only to the set and `finalized_revision` the reviewer most
   recently saw — the save message, or the re-render from gate 4 where there
   was one. Never alter a field or re-run reasoning silently between that
   and the commit; a reply that changes something restarts from the gate it
   affects instead of proceeding.

**Field check before gate 5 can be satisfied:** every candidate in the
previewed set carries every required field from extraction.md (including a
`decision_approver` that names who actually approved, not one still
carrying the awaited marker) and `decision_status: approved`. Every Action
attached to a publishing Decision
publishes regardless of which of its optional fields — owner, due date — are
filled; nothing about an Action ever blocks this gate.

This check should never be the thing that stops a publication: gate 3 covers
both ways a candidate can fail it, and covers them where there is something
the reviewer can do about it. Treat a failure here as a sign that gate 3 was
skipped or mis-scoped — go back to it rather than reporting a blocked write,
because this gate has no resolution branch and stopping at it leaves the
reviewer with a refusal and no next step.

## 9. Publication record and post-publication editing

At finalize, snapshot the publication-ready record internally: every
Decision field from `schema.md`'s shape plus `decision_status` and
`evidence_type`, with internal-only bookkeeping dropped — classification,
its reason and refs, completeness fields, and every variable from §1.
`no_decision_topics` is kept; `source_limitations` has no field in the
published schema, so it is not folded into the record. It is not re-sent to
the user either: Review Notes carried it with the first card set and the
save message deliberately does not repeat it
(`references/rendering.md`), so there is nothing further to surface. What
this line settles is only that the limitation does not silently become part
of a published record that has no field for it.

**Actions never block.** Per extraction.md and `schema.md`'s own
"No Action field is required, at either tier", an Action carries no required
field — do not enforce one at finalize or at publication. An Action with no
owner and no due date is captured and published exactly as the reviewer left
it, attached to its Decision through the permanent ID the publisher derives
from position at commit time (never a value authored or corrected during
review).

**The run ends with a result, either way.** Once the write returns, say what
happened — which Decisions were committed and where, or that nothing was
written and the locked version is still here to retry. The text belongs to
`references/rendering.md`; what matters here is that neither outcome is
allowed to end in silence. A user who replied "Yes, save" and then heard
nothing has every reason to assume it worked.

**Mechanics kept at policy level:** only the whitelisted publisher may ever
write to the Bank — never the GitLab API or `git` directly, and never a
substituted script or destination. The publishing credential is passed only
to that publisher and never printed or logged. The write is non-overwriting.
An edited Decision or Action is not automatically reflected in a prior
commit; re-publishing after any post-commit edit requires all five gates
again, from gate 1.
