# Expected extraction — saver-discount thread (regression baseline)

This file is a **baseline to diff against, not documentation of how the
skill works.** It records what `references/extraction.md`'s judgment layer
is expected to produce when it reads `examples/saver-discount-thread.txt` —
every Decision Candidate's classification, its five-gate trace with the
deciding message, every populated field (including ones deliberately left
unresolved), every Action, and every topic routed to `no_decision_topics`.

**How to use it:** when the gate model or a field rule in `extraction.md`
changes, re-run this thread through the changed rules and diff the new
output against this file. If a value moved, one of two things is true: the
rule change was wrong, or this baseline needs a deliberate, reviewed update.
Either way the diff makes the change visible instead of letting it surface
later as a bad record in the Decision Bank. This file is not the place to
learn *why* a gate works a certain way — that's `extraction.md` — or what a
rendered card looks like — that's `rendering.md`, which already renders D1
and D2 from this same thread as worked examples.

Citations use `references/extraction.md`'s format: `author + displayed
time`, with a same-minute fragment when one author has two messages in the
same displayed minute. See "On dates," directly below, for why no citation
here carries a calendar date. That format is for internal reasoning and gate
traces — a Decision record field that would actually appear on a rendered
card (`decision_details`, `rationale`, `conditions`) cites a person by alias
only, with no timestamp, per the same file's card-field citation rule; those
fields are marked below where it applies.

## On dates — read before trusting any timestamp below

`saver-discount-thread.txt` carries **clock times only, no calendar dates,
anywhere in the export.** The thread also crosses midnight: it runs evening
messages (3:18 PM–6:18 PM, ascending) into morning messages (8:50 AM–9:06
AM, ascending) with no time-of-day overlap, which is only possible if the
second block is the next calendar day; a final message (11:23 PM) then falls
later the same day as that morning block, since 11:23 PM > 9:06 AM.

So this baseline labels the two spans **Day 1** (3:18 PM–6:18 PM) and **Day
2** (8:50 AM–11:23 PM) — relative labels inferred from time-of-day ordering,
not calendar dates.

An earlier draft of `extraction.md` cited a specific ISO date for the final
message in its own worked examples. No such date exists anywhere in this
export; it was a placeholder that read as an established fact. Writing this
baseline is what surfaced it, and `extraction.md` now uses these same
relative labels and states the rule directly: when a source carries clock
times but no dates, never synthesize one. If a future export of this thread
carries real dates, or someone confirms them out of band, update this
baseline deliberately rather than by inference.

Same-minute disambiguation needed once: `jomil.villareal` posts twice at
3:21 PM (Day 1) — `jomil.villareal 3:21 PM ("if randy.tedjakusuma is on
leave...")` and `jomil.villareal 3:21 PM ("Product is from under
Fulfillment")`.

## Decision Candidates

### D1 — Saver-fare discount for Kalbe & Wardah (tactical)

**Classification:** `uncertain`
**Status:** `pending`
**Evidence type:** `none`

**Gate 1 — Object exists:** PASS. `jomil.villareal 3:18 PM (Day 1)` —
"may we proceed with this approval request from rahadiyan.wisesa" —
justification: "applying saver discount for selected MEX (Kalbe & Wardah)
for tactical purpose." An approval request, explicitly relayed. Attribution
rule applies: the object belongs to `rahadiyan.wisesa`, the named source,
not to `jomil.villareal`, who is only transmitting it.

**Gate 2 — Final state:** PASS (no revision). The object's scope — a Saver
discount for Kalbe & Wardah — is never narrowed or widened anywhere in the
thread. The extended merchant-list-governance discussion (`arpit.goel
5:06 PM`–`6:18 PM (Day 1)`, `moch.zulfa 5:11 PM (Day 1)`) is related context
that produces conditions and an Action, not a scope change to this object.

**Gate 3 — Closure signal:** FAIL. `cui.ju 3:20 PM (Day 1)` responds with a
condition, not a disposition. `arpit.goel` probes repeatedly (`3:23 PM`,
`5:06 PM`, `5:29 PM`, `6:18 PM`, all Day 1) but never says approved,
rejected, or equivalent. The thread closes with `arpit.goel 11:23 PM
(Day 2)` — "I have documented the thread here" — which is a wrap-up, not a
disposition. No closure signal exists anywhere in the available source.

**Gate 4 — Unmet condition:** UNMET, blocking. `cui.ju 3:20 PM (Day 1)` —
"please inform the respective eng PIC and get approval from them first." No
eng PIC signs off, or appears at all, anywhere in the available source.

**Gate 5 — Scope/authority fit:** Evaluated hypothetically only, since Gate
3 already fails outright. `cui.ju 3:22 PM (Day 1)` — "arpit.goel could you
help to check?" — redirects review to `arpit.goel`. The approval was
addressed to `randy.tedjakusuma` / `@oncall-lead` at `3:18 PM`; nothing in
the thread establishes `cui.ju` as that party, and `randy.tedjakusuma` never
reappears to endorse the redirect. Under Rule 5.2 this redirection does not
transfer closing authority to `arpit.goel` — moot in practice since Gate 3
already found no disposition from him, but it is why his extensive
engagement could never have closed this candidate even had he said
"approved."

**Fields:**
- `decision_title`: Saver-fare discount for Kalbe & Wardah (tactical)
- `decision_details`: Apply a Saver-fare discount to a selected merchant
  group — Kalbe and Wardah — as a tactical measure, configured on the ExP
  variable behind Mart's Saver option rather than as a change to standard
  fares. In effect it gives these two merchants free delivery, aimed
  specifically at the pickup-point catchment problem rather than at their
  pricing generally. States substance and final scope only — nothing about
  approval state, per `extraction.md`'s rule that this must stay true even
  if `decision_status` later changes.
- `pst`: `FF Ecommerce` — **inferred, not established.** Basis:
  `jomil.villareal 3:21 PM (Day 1)` ("Product is from under Fulfillment")
  plus `albert.lim 9:02 AM (Day 2)` calling the surrounding thread "this
  eComm decision." Neither statement names a PST directly; this is the
  best-supported active value from `references/psts.json`, flagged for the
  reviewer to confirm or change, per the rule to never stop and ask before
  drafting.
- `decision_proposer`: `@rahadiyan.wisesa`
- `rationale`: Many PAX sit far from Kalbe & Wardah pickup points, and the
  delivery cost that creates is what caps demand; free delivery removes the
  barrier and unlocks volume beyond the existing catchment
  (`@rahadiyan.wisesa`). Commercially, these merchants carry Grab's
  e-commerce partnerships with FMCG principals, and a competitive Saver fare
  is one of the requirements for those partnerships to drive enough sales
  volume to stay sustainable (`@moch.zulfa`). **Both strands are required**
  — the thread justifies this decision from two directions, and keeping only
  the proposer's operational argument would discard the commercial case
  entirely. Cited by alias only, no timestamp, per `extraction.md`'s
  card-field citation rule — the full `author + time` form for this same
  evidence is above, in the Gate 3
  trace.
- `decision_status`: `pending`
- `decision_approver`: **`@randy.tedjakusuma / @oncall-lead (awaiting
  approval); eng-PIC sign-off also required, person not named in thread`.** No
  party entitled to close this gave a signal (Gate 3 fails outright), so
  extraction drops to rung 2 of the fallback ladder: who is supposed to
  approve, when nobody has yet. The thread names that twice — the original
  approval request (`jomil.villareal 3:18 PM, Day 1`) addressed to
  `randy.tedjakusuma` / `@oncall-lead` directly, and `cui.ju 3:20 PM (Day 1)`
  additionally requiring sign-off from "the respective eng PIC," a role with
  no name given.

  **The role stays unresolved, and this is the part most likely to be got
  wrong on a re-run.** `cui.ju 3:22 PM (Day 1)` names `@arpit.goel`, and it
  is tempting to read that as identifying the eng PIC. Read in sequence it
  does not: `jomil.villareal 3:21 PM (Day 1)` asks who to contact while
  `randy.tedjakusuma` is on leave, and `3:22 PM` answers *that*. Being asked
  to "help to check" is not holding the role whose sign-off was required two
  messages earlier, and the thread never says `@arpit.goel` holds it. A name
  here would send a reviewer chasing the wrong person, or let his later
  agreement read as the approval. If a future run resolves this role to a
  person, that is a regression unless the thread text changed.

  The awaited party is marked `(awaiting approval)` inline so it cannot read
  as a disposition that happened — the same safety the skill applies to
  `action_owner`'s `(requested, not yet acknowledged)`. Recording who is
  awaited is independent of Gate 5: `@arpit.goel`'s standing came only from
  `cui.ju`'s unendorsed redirection, so his signal could not have closed this
  candidate even had he given one.
- `conditions`: The merchant group is a business-team priority list reviewed
  against partnership needs and merchant performance, not a fixed setup —
  membership is expected to change as relevance does (`@moch.zulfa`). This
  is a genuine condition on future execution and belongs here. The eng-PIC
  gate and the unendorsed redirection do **not**: they are approval-process
  facts, so they live in `classification_reason` (the Gate 3/4/5 traces
  above) and reach the reviewer through Review Notes' `Uncertain Decisions`
  category instead. The same message supplies both, which is exactly why the
  distinction has to be drawn on what the statement is about, not on who
  said it or when.
- `refs`: available (approval-request message, the eng-PIC condition
  message, the governance-concern message, the wiki-documentation message)
  — not enumerated here; see `rendering.md`'s D1 references block for the
  rendered form.

**Completeness:**
- All seven required fields present, `decision_approver` included via rung 2
  of the fallback ladder → `completeness_status: complete`. No
  `missing_required_fields` entry, and no finalize-prompt round-trip needed
  for this candidate.
- **The awaited value is a filled, honest field, not a gap.**
  `decision_approver` names both parties the thread shows are owed a
  disposition — `@randy.tedjakusuma` / `@oncall-lead`, the original
  addressee, and the eng PIC role `cui.ju` required, inferred as
  `@arpit.goel` — each marked `(awaiting approval)` so neither can be
  misread as a signal that was actually given. The distinction that matters,
  and the one this whole design turns on: a reviewer may be asked to
  *confirm what the thread shows*, never to *supply what it does not* — and
  rung 2 is exactly that confirmation, drawn straight from the thread.
- Not publishable as `approved` — and not because anything is missing:
  `decision_status` is `pending`, and even once `decision_approver` is
  corrected to name who actually approved, `decision_status` would still
  need correcting to `approved` in the same reply for
  `references/review.md`'s publication gate 3 to resolve.

**Actions attaching to D1:**
- **A1** — "Documented the thread in the Confluence wiki (completed within
  the thread)." Owner: `@arpit.goel`. No date. Source:
  `arpit.goel 11:23 PM (Day 2)` — "I have documented the thread here."
- **A2** — "Add the logic that recreates the merchant list." Owners (list):
  `@sengkeong.ho`, `@moch.zulfa`, `@rangga.pratama` — requested, not yet
  acknowledged in the available source. No date. Source:
  `arpit.goel 11:23 PM (Day 2)`.

### D2 — Wiki page to document the mex-specific pricing-config variable

**Classification:** `decision`
**Status:** `approved`
**Evidence type:** `explicitly_stated`

**Gate 1 — Object exists:** PASS. `sengkeong.ho 8:55 AM (Day 2)` — "can we
set up an wiki page to document this for all markets?" — a proposal.

`decision_proposer` resolves on **rung 2** of `extraction.md`'s ladder, not
to the author of that message. The same message opens "Can I understand the
concern about documentation further?", making it explicitly responsive to
the documentation gap `arpit.goel` stated the day before (`5:29 PM`,
`6:18 PM`, Day 1). `albert.lim 8:57 AM (Day 2)` voices the same need again,
but rung 2's tiebreak keeps it with whoever stated it first, so a later
restatement does not move it. Value:
`@arpit.goel (raised the need; proposed by @sengkeong.ho)`. The **proposing
side** — the pair that Rules 3.2, 3.3 and 5.1 are read against — is
`arpit.goel` + `sengkeong.ho`.

**This is the value most likely to regress, in either direction.** A run
that reports `@sengkeong.ho` has read only who typed the proposal and lost
the stakeholder the record exists for. A run that reports `@albert.lim` has
let a restatement carry the need, which additionally breaks Gate 3 below.

**Gate 2 — Final state:** Narrowed. `sengkeong.ho 8:59 AM (Day 2)` —
"rahadiyan.wisesa lets set up a wiki page for this variable and document all
the configs here" — narrows the object from "all markets" to the single
variable, and adds linking the variable to the wiki as the central source of
truth. Final scope is the narrowed one; nobody explicitly re-confirms the
narrowed version, which matters for Gate 5, not Gate 2.

**Gate 3 — Closure signal:** PASS. `albert.lim 8:57 AM (Day 2)` —
"sengkeong.ho ya that helps" — explicit, unambiguous acceptance (Rule 3.1).
The thread names no specific approver for this proposal, so under Rule 3.2 a
disposition from any participant **outside the proposing side** can close
it; `albert.lim` is neither `arpit.goel` nor `sengkeong.ho`, so he
qualifies.

The rung-2 tiebreak carries a load here. Had `albert.lim`'s `8:57 AM`
restatement of the documentation need moved the need to him, he would sit on
the proposing side, his own "ya that helps" would be disqualified by Rule
3.3, and D2 would come out `uncertain` with no approver — from a thread that
plainly settled the question. Reading Rule 3.2 against only the
`decision_proposer` name rather than the side is the mirror-image failure:
it would let `sengkeong.ho` close the proposal he himself voiced.

**Gate 4 — Unmet condition:** None found. No party attaches an in-thread
gate to this proposal.

**Gate 5 — Scope/authority fit:** PASS. The narrowing at `8:59 AM (Day 2)`
comes from `sengkeong.ho`, who voiced the object and is therefore on the
proposing side, and happens *after* `albert.lim`'s acceptance at `8:57 AM
(Day 2)`. Per Rule 5.1, a narrowing from that side after acceptance does not
reopen the candidate — the acceptance carries forward to the narrowed scope.
Rule 5.1 has to be read against the side here too: `sengkeong.ho` is not the
name in `decision_proposer`. Authority conferral
(Rule 5.2) is not in question here since `albert.lim`'s standing to close
comes from Rule 3.2 directly, not from a transfer.

**Attribution check (the known misreading):** this is now read
deliberately, by rung 2 of `decision_proposer`, rather than left to whoever
the reader happens to notice — but the message order it depends on is the
same, and is recorded here because a rule change that got it backwards would
still produce a plausible-looking card. The accepter is `albert.lim`, not
"the person whose cleanup concern prompted the proposal." The governance
concern that motivated the whole exchange — "no governance on the grabx
group... no documentation on knowing what the right set of merchants are" —
was raised earlier, on **Day 1**, by a different person, `arpit.goel`, at
`5:29 PM` and `6:18 PM`. `albert.lim`'s own remark about cleaning up legacy
pricing configs arrives at `8:57 AM (Day 2)`, in the same message block as,
and immediately *after*, his acceptance ("ya that helps") — it is supporting
context he adds afterward, not the concern that prompted `sengkeong.ho`'s
proposal. Verified against message order in the source thread; this
baseline records the corrected attribution.

**Fields:**
- `decision_title`: Wiki page to document the mex-specific pricing-config
  variable
- `decision_details`: Create a wiki page documenting the mex-specific
  pricing configs carried on this ExP variable, and link the variable to
  that page so the wiki becomes the central source of truth for what each
  config is and why it exists. Scope is this one variable, not pricing
  configs across all markets. The final, narrowed scope is stated as the
  decision; who narrowed it and when is conversation shape and belongs to
  the Gate 2 trace above, not to this field.
- `pst`: `FF Ecommerce` — **inferred, weaker basis than D1.** The thread
  gives no phrase tying D2 itself to a PST the way `3:21 PM`/`9:02 AM` do
  for D1; this value is carried over on the basis that D2 is the same
  thread, same product context, and same participants as D1, immediately
  adjacent to `albert.lim`'s "this eComm decision" remark
  (`9:02 AM, Day 2`) about the surrounding conversation. Flag for reviewer
  confirmation at least as strongly as D1's.
- `decision_proposer`: `@arpit.goel (raised the need; proposed by
  @sengkeong.ho)` — see the Gate 1 trace above for the rung-2 derivation.
- `rationale`: The grabx merchant group carries no approvals, documentation,
  or freshness check, so mistakes go undetected and nobody can later
  reconstruct which merchants belong in a group or how they were derived
  (`@arpit.goel`). Handling mex-specific pricing configs on ExP is
  established practice, so what is missing is documentation rather than the
  mechanism itself (`@sengkeong.ho`). The team currently cannot remove or
  trace legacy configs set up by ops long ago, because nothing records what
  they were for or who asked for them; documenting new configs as they are
  created is what stops that recurring (`@albert.lim`). **Three
  contributors, all kept** — and the first strand is the one a run has
  actually dropped: a rationale gathered from the proposal message forward
  keeps the answer and discards the question that prompted it. Cited by
  alias only, no timestamp, per `extraction.md`'s card-field citation rule.
- `decision_status`: `approved`
- `decision_approver`: `@albert.lim`
- `conditions`: none established — `null`.
- `refs`: available (the "all markets" proposal, the narrowing message, the
  acceptance message) — not enumerated here; see `rendering.md`'s D2
  references block.

**Completeness:**
- Required: all seven fields present, including `decision_approver:
  @albert.lim` → `complete`, and — because `decision_status` is `approved`
  and the approver is a real name, not one still marked `(awaiting
  approval)` — also clear of the one extra check publication gate 3
  (`references/review.md`) applies to `approved` candidates. D2 is the one
  candidate in this thread eligible to actually
  publish as `approved`.

**Actions attaching to D2:**
- **A3** — "Set up a wiki page for this variable and document the pricing
  configs there." Owner: `@rahadiyan.wisesa` — requested, not yet
  acknowledged; he does not speak again anywhere in the available source.
  No date given, none guessed. Source: `sengkeong.ho 8:59 AM (Day 2)`.

## Topics routed to `no_decision_topics` (Gate 1 failures)

- **FR-balancing principle during crunch.** `albert.lim 8:51 AM (Day 2)`
  asks "what is our principle here in terms of balancing FR during crunch?"
  and `sengkeong.ho 8:54 AM (Day 2)` answers with the fare-certainty /
  longer-SLA-batching strategy. A question and a background-reasoning
  answer — no proposed course of action.
- **Interim ZFF/EAR stopgap.** `sengkeong.ho 9:06 AM (Day 2)` — "our interim
  stopgap is to use mex ZFF and correct for dax EAR by overpaying for these
  jobs" — reported as the team's existing approach, not put forward for
  disposition. The thread never reopens or challenges it.
- **FR capacity vs. pricing-lever discussion.** `albert.lim 9:02 AM
  (Day 2)` — batching limits on large Mart orders, pricing/visibility as
  the only real FR lever, folding both levers under DMS-Go+ — background
  reasoning and observation, no proposed course of action.
- **Merchant-list governance explanation.** `moch.zulfa 5:11 PM (Day 1)` —
  explains how the merchant group is currently prioritized and maintained,
  in response to `arpit.goel`'s question. Describes existing practice, not
  a proposal to adopt anything new. (This context feeds D1's Gate 2 scope
  check and motivates Action A2; it is not itself a decision object.)
- **Capture-process messages.** `albert.lim 8:50 AM (Day 2)` asking
  `long.jin` to use the decision-capture tool, and `long.jin 8:55 AM
  (Day 2)` asking whether all information sources are in this thread —
  messages about the capture process itself, excluded by Gate 1's explicit
  carve-out.
- **Automated bot message.** `Grab 8:51 AM (Day 2)` — "Heart, Hunger,
  Honour, Humility" — an automated values-bot response, no proposal
  content.

## Source limitations

Three external links appear in the thread text and were not opened for this
extraction, consistent with the skill asking the user before reading any
external source:

- `experiments.grab.com/t/variables/…/455492?env=prd` — the ExP variable
  the approval request links to (`jomil.villareal 3:18 PM, Day 1`).
- The JIRA ticket embedded as "Approval_Request - ID for Mart"
  (`jomil.villareal 3:18 PM, Day 1`).
- `grabtaxi.atlassian.net/wiki/…/foodSaverOptionDiscount` — the Confluence
  page `arpit.goel` created to document the thread
  (`arpit.goel 11:23 PM, Day 2`).

This baseline assumes none of the three were opened. Nothing in any field
above relies on their content; every value is grounded in the Slack thread
text alone. If a future run of this thread opens one of these sources, the
resulting diff against this file is expected to change and does not by
itself indicate a regression.

## Judgment calls and disagreements worth flagging

- **A fallback ladder, not a value that reports emptiness.** This field has
  now been through four designs, and the reasoning is worth keeping in full
  because a future change is likely to be tempted by the same wrong turns.
  (1) It was once unconditionally required with no honest way to satisfy it,
  which made D1 unfinalizable without inventing a name — the original bug.
  (2) It was then split into two tiers, marked `(*)` and `(**)` on the card,
  which fixed that but made the reader decode a notation whose intuitive
  reading ("two stars = even more required") is backwards. (3) It was then
  auto-filled with the literal `none` when nothing closed the candidate,
  which removed the notation but read as an answered field, got skipped, and
  quietly undercut the marker that says the field is required. The immediate
  fix to that — leaving it unresolved on the card and asking the reviewer to
  type `none` at the finalize prompt — solved the "reads as answered"
  problem, but it was still asking the reviewer to confirm an absence in a
  thread that, more often than not, already says who the approval was
  addressed to or who was supposed to sign off. That signal was sitting
  right there in the source, and every one of the first three designs threw
  it away. (4) The field now works down a ladder instead: who approved it;
  failing that, who is supposed to, marked inline as `(awaiting approval)` so
  an outstanding request can never be misread as a disposition that
  happened; only failing both is it left unresolved. `none` is removed
  entirely — it is not a value, not an accepted reply, not an option named in
  any prompt anywhere in this skill. D1 is the worked case: nobody ever
  approved it, but the thread names an addressee
  (`@randy.tedjakusuma` / `@oncall-lead`) and, once the eng-PIC role `cui.ju`
  required is resolved by inference, a second awaited party
  (`@arpit.goel`) — both recorded, both marked awaiting, neither confused
  with D2's real approver `@albert.lim`. The invariant across all four
  designs, and the thing any future change must preserve: a reviewer may be
  asked to confirm what the thread shows, never to supply what it does not —
  and an awaited approver must never render as a bare name, because that is
  indistinguishable from one who actually signed off.
- **`decision_details` and `conditions` no longer carry approval-process
  content**: an earlier draft's D1 `decision_details` stated that no
  approval was ever given, and its `conditions` repeated the unmet eng-PIC
  gate and the redirection that Review Notes already carries. Both are
  trimmed here — `decision_details` states substance and scope only, and
  the approval-process facts live solely in `classification_reason` and
  Review Notes' `Uncertain Decisions` category.
- **Dates**: no citation here carries a calendar date, because the export
  has none — see "On dates" above. Establishing that corrected an invented
  date in `extraction.md`'s own worked examples.
- **D2's `pst`** is inferred on a visibly weaker chain of evidence than
  D1's; `extraction.md`'s own D2 worked example does not walk through a
  `pst` justification at all (only `rendering.md`'s rendered card assigns
  it). This baseline supplies the reasoning explicitly so a future diff can
  tell whether a rule change affects D1's inference, D2's, or both.
- **Everything else** — D1's classification (`uncertain`/`pending`/`none`),
  D2's classification (`decision`/`approved`/`explicitly_stated`), the
  gate-by-gate outcomes, the three Actions, and the corrected attribution
  of D2's accepter versus the governance concern's originator — matches the
  orientation given for this task and `extraction.md`'s own worked examples
  after independent verification against the thread's message order.
