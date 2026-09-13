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
here carries a calendar date.

## On dates — read before trusting any timestamp below

`saver-discount-thread.txt` carries **clock times only, no calendar dates,
anywhere in the export.** The thread also crosses midnight: it runs evening
messages (3:18 PM–6:18 PM, ascending) into morning messages (8:50 AM–9:06
AM, ascending) with no time-of-day overlap, which is only possible if the
second block is the next calendar day; a final message (11:23 PM) then falls
later the same day as that morning block, since 11:23 PM > 9:06 AM.

So this baseline labels the two spans **Day 1** (3:18 PM–6:18 PM) and **Day
2** (8:50 AM–11:23 PM) — relative labels inferred from time-of-day ordering,
not calendar dates. This deliberately departs from `extraction.md`'s own
worked example, which cites `arpit.goel 2026-08-29 11:23 PM` — that ISO date
is not supported anywhere in the source thread; it appears to be a
placeholder the reference file's author supplied for illustration. Asserting
it here would be exactly the invented-date mistake the task guarding this
file warns against. If a future thread export adds real dates, or someone
confirms 2026-08-29 out-of-band, this baseline should be updated deliberately
— not by silently copying the reference file's placeholder.

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
- `decision_details`: A Saver-fare discount for two merchants, Kalbe and
  Wardah, for a tactical purpose, relayed by `jomil.villareal` on behalf of
  `rahadiyan.wisesa` (`3:18 PM, Day 1`). Scope is never narrowed or widened.
  An eng-PIC approval condition remains unmet through the end of the
  available source, and no closure signal — approval, rejection, or
  explicit deferral — is ever given.
- `pst`: `FF Ecommerce` — **inferred, not established.** Basis:
  `jomil.villareal 3:21 PM (Day 1)` ("Product is from under Fulfillment")
  plus `albert.lim 9:02 AM (Day 2)` calling the surrounding thread "this
  eComm decision." Neither statement names a PST directly; this is the
  best-supported active value from `references/psts.json`, flagged for the
  reviewer to confirm or change, per the rule to never stop and ask before
  drafting.
- `decision_proposer`: `@rahadiyan.wisesa`
- `rationale`: Kalbe & Wardah pickup points sit far from many PAX, creating
  delivery friction that free delivery removes, unlocking demand beyond the
  existing pickup-point catchment (`rahadiyan.wisesa 3:26 PM, Day 1`).
- `decision_status`: `pending`
- `decision_approver`: unresolved — no party entitled to close this ever
  gave a signal.
- `conditions`:
  - Unmet: eng-PIC approval required before proceeding
    (`@cui.ju 3:20 PM, Day 1`).
  - Review redirected to `@arpit.goel` by `@cui.ju` (`3:22 PM, Day 1`);
    `@randy.tedjakusuma`, the party the approval was originally addressed
    to, never endorsed that redirection.
- `refs`: available (approval-request message, the eng-PIC condition
  message, the governance-concern message, the wiki-documentation message)
  — not enumerated here; see `rendering.md`'s D1 references block for the
  rendered form.

**Completeness:**
- Finalize-required: all six fields present (`pst`, `decision_proposer`,
  and `rationale` present as inferred/established values a reviewer can
  confirm) → `completeness_status: complete` for finalize.
- Publish-required: missing `decision_approver` → cannot publish as-is. Not
  actually reachable anyway, since `decision_status` is `pending`, not
  `approved`.
- This candidate is finalizable exactly as drafted — the empty
  `decision_approver` does not block finalize, per Completeness in
  `extraction.md`.

**Actions attaching to D1:**
- **A1** — "Documented the thread in the Confluence wiki (completed within
  the thread)." Owner: `@arpit.goel`. No date. Source:
  `arpit.goel 11:23 PM (Day 2)` — "I have documented the thread here."
- **A2** — "Add the logic that recreates the merchant list (SQL, or
  partnership-based?)." Owners (list): `@sengkeong.ho`, `@moch.zulfa`,
  `@rangga.pratama` — requested, not yet acknowledged in the available
  source. No date. Source: `arpit.goel 11:23 PM (Day 2)`.

### D2 — Wiki page to document the mex-specific pricing-config variable

**Classification:** `decision`
**Status:** `approved`
**Evidence type:** `explicitly_stated`

**Gate 1 — Object exists:** PASS. `sengkeong.ho 8:55 AM (Day 2)` — "can we
set up an wiki page to document this for all markets?" — a proposal.
`decision_proposer`: `@sengkeong.ho`.

**Gate 2 — Final state:** Narrowed. `sengkeong.ho 8:59 AM (Day 2)` —
"rahadiyan.wisesa lets set up a wiki page for this variable and document all
the configs here" — narrows the object from "all markets" to the single
variable, and adds linking the variable to the wiki as the central source of
truth. Final scope is the narrowed one; nobody explicitly re-confirms the
narrowed version, which matters for Gate 5, not Gate 2.

**Gate 3 — Closure signal:** PASS. `albert.lim 8:57 AM (Day 2)` —
"sengkeong.ho ya that helps" — explicit, unambiguous acceptance (Rule 3.1).
The thread names no specific approver for this proposal, so under Rule 3.2
any participant other than the proposer can close it; `albert.lim` is such a
participant, and is not `sengkeong.ho`.

**Gate 4 — Unmet condition:** None found. No party attaches an in-thread
gate to this proposal.

**Gate 5 — Scope/authority fit:** PASS. The narrowing at `8:59 AM (Day 2)`
comes from `sengkeong.ho`, the proposer himself, and happens *after*
`albert.lim`'s acceptance at `8:57 AM (Day 2)`. Per Rule 5.1, a proposer's
own narrowing after acceptance does not reopen the candidate — the
acceptance carries forward to the narrowed scope. Authority conferral
(Rule 5.2) is not in question here since `albert.lim`'s standing to close
comes from Rule 3.2 directly, not from a transfer.

**Attribution check (the known misreading):** the accepter is `albert.lim`,
not "the person whose cleanup concern prompted the proposal." The governance
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
- `decision_details`: `sengkeong.ho` proposed a wiki page to document
  mex-specific pricing configs (`8:55 AM, Day 2`), narrowed by himself to
  documenting this single ExP variable and linking it back as the central
  source of truth (`8:59 AM, Day 2`). Final scope is the narrowed one.
- `pst`: `FF Ecommerce` — **inferred, weaker basis than D1.** The thread
  gives no phrase tying D2 itself to a PST the way `3:21 PM`/`9:02 AM` do
  for D1; this value is carried over on the basis that D2 is the same
  thread, same product context, and same participants as D1, immediately
  adjacent to `albert.lim`'s "this eComm decision" remark
  (`9:02 AM, Day 2`) about the surrounding conversation. Flag for reviewer
  confirmation at least as strongly as D1's.
- `decision_proposer`: `@sengkeong.ho`
- `rationale`: Handling mex-specific pricing configs on ExP is established
  practice, not a new one (`sengkeong.ho 8:55 AM, Day 2`); the wiki closes a
  traceability gap the team hit that same morning, where legacy configs
  have no visible owner or purpose and are hard to remove or trace
  (`albert.lim 8:57 AM, Day 2`).
- `decision_status`: `approved`
- `decision_approver`: `@albert.lim`
- `conditions`: none established — `null`.
- `refs`: available (the "all markets" proposal, the narrowing message, the
  acceptance message) — not enumerated here; see `rendering.md`'s D2
  references block.

**Completeness:**
- Finalize-required: all six fields present → `complete`.
- Publish-required: `decision_approver` present (`@albert.lim`) → also
  `complete`. D2 is the one candidate in this thread eligible to actually
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

- **Dates**: this baseline deliberately does not adopt `extraction.md`'s
  own worked-example date (`2026-08-29`) — see "On dates" above. This is
  the single largest intentional divergence from the orientation this file
  was written against.
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
