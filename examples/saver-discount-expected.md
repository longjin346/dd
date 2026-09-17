# Expected output — `examples/saver-discount-thread.md`

What a correct run produces from that thread. Derived from the export, gate
by gate, not carried over from any earlier version of this file.

**This is the regression fixture, not a blind test.** The same thread is
worked through in `references/extraction.md`, so a run that loads the rules
has already been shown these answers. Use this to diff after a rule change.
Measuring whether the rules can be applied at all takes a thread whose
answers appear nowhere in `references/`.

## Status: baseline, not a gold set

Every judgment below is derived from the rules in `references/`, by one
reader, and **no one who was in the thread has confirmed any of it.** That
matters more than it sounds: a baseline derived from the rules cannot detect
a wrong rule, because it will be wrong in the same direction and the diff
comes back clean. It checks consistency, not correctness.

The **facts** are solid — who said what and when, the addresses, the
handles, the reactions all come from the export. The **readings** are not.

### Seven readings awaiting the thread owner

Answer these and this file becomes a gold set for this thread. Each states
the message, the reading taken here, and what changes if the reading is
wrong. No need to read the rest of the file to answer them.

1. **Did `albert.lim`'s "ya that helps" (`2026-08-26 08:57`) approve the
   commitment to document?** Taken as yes, which is the whole basis for D2
   being `approved` rather than `pending`. *If no:* D2 becomes `uncertain`
   with no approver, and this thread records no completed decision at all.
   **Most load-bearing question here** — one run has already disagreed.
2. **Whose decision is D2?** Taken as `@arpit.goel`'s: he raised the
   documentation need (`2026-08-25 17:29`, `18:18`), `@sengkeong.ho` offered
   the solution. *If it is sengkeong's instead:* the proposer changes, and
   `albert.lim`'s acceptance still stands.
3. **Is D2 "record these configs somewhere" or "make a wiki page"?** Taken
   as the former, with the page as the agreed mechanism. *If the page is the
   decision:* the title, the details and the Action all change, and the page
   `@arpit.goel` already made reads as satisfying it.
4. **Is `@arpit.goel` the "respective eng PIC" `cui.ju` asked for?** Taken as
   no — `cui.ju 15:22` names him, but read in sequence that answers
   `jomil.villareal 15:21` about who to contact while `randy.tedjakusuma` is
   away, not the eng-PIC requirement two messages earlier. *If yes:* D1's
   approver names him, and the gate is met or nearly so.
5. **Is "the list will continue to be reviewed and maintained"
   (`@moch.zulfa 17:11`) a condition on execution?** Taken as yes, so it
   sits in `conditions`. *If it is just background:* `conditions` is empty
   for D1.
6. **Does `@arpit.goel`'s governance concern belong to D1's rationale or
   D2's?** Taken as D2's: it is an argument *against* proceeding with D1 as
   things stand, and the reason D2 exists. *If it belongs to D1:* a run that
   puts it there is right and this file is wrong.
7. **The wiki page `@arpit.goel` already made — does it attach to D1 or
   D2?** Taken as D1, since it documents this thread rather than the
   variable's configs. *If D2:* it and the outstanding page sit on the same
   Decision, and the overlap note reads differently.

Until these are answered, treat a clean diff against this file as evidence
that behaviour has not **changed**, never that it is **right**.

## About the source

`saver-discount-thread.md` is an export prepared by hand from the real
thread: full URLs, real timestamps with calendar dates, message `ts` values,
and reactions. **It is authoritative about the thread's content and not a
specimen of what a fetch returns** — its markdown layout is the exporter's
choice, so nothing here should be read as describing the shape the Slack
tooling hands the skill. What that shape is remains unverified.

It replaced a browser copy-paste that disagreed with it on four points of
content, each of which this file previously encoded as correct:

| | The paste said | The export says |
|---|---|---|
| ExP link | `experiments.grab.com/t/variables/…/455492?env=prd` | the full URL, no ellipsis |
| Jira link | unfurl title only, no address | `https://grabtaxi.atlassian.net/browse/TECHOPS-117402` |
| Addressed to | `@oncall-lead` | **`@pricing-team`** |
| Reactions | none | three |

**Citations carry the date**, since the thread spans two days and the source
states them: `cui.ju 2026-08-25 15:20`. The relative `Day 1` / `Day 2`
labelling in `references/extraction.md` applies only to a source that gives
clock times without dates, which this one does not.

---

# D1 — Saver discount for Kalbe & Wardah

## Gates

**Gate 1 — Object exists:** PASS. `jomil.villareal 2026-08-25 15:18` asks
"may we proceed with this approval request from @rahadiyan.wisesa" — an
approval request, explicitly relayed. The object belongs to the named
source, not the relayer: rung 1 of `decision_proposer`, which settles it
before rung 2 is reached. The proposing side has one member.

**Gate 2 — Final state:** PASS. The scope — a Saver discount for the named
merchant group — is never narrowed or widened. The surrounding discussion
about merchant-list governance is related context that produces Actions and
feeds `conditions`; it is not a scope change to this object.

**Gate 3 — Closure signal:** FAIL. No disposition from any entitled party.

- `cui.ju 2026-08-25 15:20` sets a condition, not a disposition.
- `cui.ju 2026-08-25 16:01` asks "is the above clarification ok to
  approve?" — asking for one, not giving one.
- `arpit.goel` probes at `15:23`, `17:06`, `17:29`, `18:18` and never says
  approved, rejected or equivalent.
- `arpit.goel 2026-08-26 23:23` closes with "I have documented the thread
  here" — a wrap-up, not a disposition.

**The three reactions are not closure signals**, and a run should say why
rather than ignoring them. Rule 3.1(b) admits a reaction only where its
meaning as approval or rejection is unambiguous in context. None of these
sits on the proposal or on any disposition of it:

| Reaction | On | Reads as |
|---|---|---|
| `+1` ×2 | `arpit.goel 2026-08-25 18:18`, the governance concern | agreement with a concern |
| `ack` ×1 | `albert.lim 2026-08-26 09:02`, FR-lever commentary | receipt of a point |
| `+1` ×2 | `sengkeong.ho 2026-08-26 09:06`, the stopgap explanation | agreement with an explanation |

`evidence_type: none`.

**Gate 4 — Unmet condition:** UNMET, blocking. `cui.ju 2026-08-25 15:20` —
"please inform the respective eng PIC and get approval from them first" —
sets an in-thread gate on a role. No eng PIC signs off anywhere in the
source.

**Gate 5 — Scope/authority fit:** FAIL on authority conferral, moot in
practice since Gate 3 found no signal. `cui.ju 2026-08-25 15:22` redirects
review to `@arpit.goel`. The request was addressed to `@randy.tedjakusuma` /
`@pricing-team`; `cui.ju` is not shown to be that party, and
`@randy.tedjakusuma` never reappears to endorse the redirect. Under Rule 5.2
this transfers nothing — which is why `arpit.goel`'s extensive engagement
could not have closed this candidate even had he said "approved".

**Result:** `uncertain` · `pending` · `none`.

## Card

- `decision_title`: Saver-fare discount for Kalbe & Wardah (tactical)
- `decision_details`: a Saver discount applied to a named merchant group
  (Kalbe & Wardah) as a tactical measure, with the group maintained by the
  ID business team. Must preserve the merchant names, the tactical framing,
  and the fact that the group is a maintained list rather than a fixed set.
  **`MEX` stays `MEX` wherever it appears** (`references/glossary.md`): it
  means merchant here, and a record that renders this as applying "in
  Mexico" reads perfectly, cites real messages, and is false.
- `pst`: **`Pax Pricing`** — confirmed by the thread owner, and **not** what
  the thread's own language suggests. A Saver discount is a discount on pax
  pricing; that is what the decision acts on.

  `jomil.villareal 2026-08-25 15:21` ("Product is from under Fulfillment")
  and `albert.lim 2026-08-26 09:02` ("this eComm decision") describe where
  the conversation sits and which team raised it — not what is being
  decided. Reading either as the PST is the specific error this value exists
  to correct, and earlier versions of this file made it.

  Still flagged under `Inferred Values to Confirm`: the thread never states
  the PST, so any run reaching `Pax Pricing` reaches it by knowing what a
  Saver discount is — domain knowledge the thread does not supply.
- `rationale`: **two contributors, three strands.**
  - Brand visibility is strong but demand is constrained by pickup-point
    accessibility; many PAX are far from the pickup points, and delivery
    friction is too expensive (`@rahadiyan.wisesa`).
  - Free delivery removes that barrier and unlocks incremental demand beyond
    the existing catchment (`@rahadiyan.wisesa`).
  - The merchants enable and sustain e-commerce partnerships with FMCG
    principals, and a competitive Saver fare is a key requirement to drive
    the sales volume that makes those partnerships sustainable
    (`@moch.zulfa`).

  **`arpit.goel`'s governance concern does not belong here.** It is an
  objection raised *about* this decision and the reason D2 exists; it is not
  a reason for the discount. A run that folds it into D1's rationale has
  recorded an argument against something as an argument for it.
- `decision_status`: `pending`
- `decision_proposer`: `@rahadiyan.wisesa`
- `decision_approver`: **`@randy.tedjakusuma / @pricing-team (awaiting
  approval); eng-PIC sign-off also required, person not named in thread`**

  Rung 1 fails outright — Gate 3 found no closure signal — so extraction
  drops to rung 2, and the thread names an awaited party twice: the request
  at `15:18` is addressed to `@randy.tedjakusuma` / `@pricing-team`
  directly, and `cui.ju 15:20` additionally requires sign-off from "the
  respective eng PIC", a role with no name.

  **The role stays unresolved, and this is the trap in this thread.**
  `cui.ju 2026-08-25 15:22` names `@arpit.goel`, who then engages on exactly
  the engineering-side concerns an eng PIC would own, which makes resolving
  the role to him look well-supported. Read in sequence it is not: that
  message answers `jomil.villareal 15:21` asking who to contact while
  `randy.tedjakusuma` is on leave — not the eng-PIC requirement two messages
  earlier. Nothing says `@arpit.goel` holds that role. Naming him here sends
  a reviewer chasing the wrong person, and turns any later "ok" from him
  into an approval the thread never gave.

  Nothing in this value was filled by inference, so it gets **no**
  `Inferred Values to Confirm` entry. The open role reaches the reviewer
  through `Uncertain Decisions`, where the eng-PIC gate already goes.
- `conditions`: the merchant group is a business-team priority list,
  reviewed and maintained against partnership needs and merchant
  performance rather than fixed, and adjustable as relevance changes
  (`@moch.zulfa`).

  **This field is not empty.** The eng-PIC gate and the unendorsed
  redirection are approval-process facts, not conditions on execution — they
  belong in `classification_reason`, and a run that files either here has
  put process into a field about the decision.
- `refs`: available — the approval-request message, the eng-PIC condition,
  the redirection, the rationale messages.

**`classification_reason`** should name the deciding gates and nothing else:
approval requested in `jomil.villareal 2026-08-25 15:18`; eng-PIC gate set
in `cui.ju 15:20`; review redirected to `arpit.goel` by `cui.ju` at `15:22`,
unendorsed by the originally addressed `randy.tedjakusuma`; no signal from
any entitled party through the end of the thread.

**Completeness:** all seven required fields present, `decision_approver`
included. An awaited value, marked as awaited, is a filled and honest value,
not a gap. D1 is finalizable exactly as drafted — and not publishable,
which is a different thing and is what `Complete, but not a decision yet`
exists to say.

---

# D2 — Documenting the pricing configs on the ExP variable

## Gates

**Gate 1 — Object exists:** PASS, **and the wiki page is not the object.**
`sengkeong.ho 2026-08-26 08:55` — "If it helps, can we set up an wiki page
to document this for all markets?" Both signals point the same way: the
proposal states its own purpose ("to document this") and offers the page
conditionally ("if it helps"), and the acceptance restates the commitment
without the instrument — `albert.lim 08:57`, "part of solving that problem
is to properly document the incoming new ones". Substitution confirms it:
put the documentation somewhere other than a wiki and what was agreed still
stands.

So the object is the commitment to document these configs; the page is
recorded in `decision_details` as the agreed mechanism and executed as the
Action. Titling this after the wiki page records the tool and loses the
commitment — and makes the record read as unfulfilled, since the page that
actually got made came from a different person documenting something else.

**`decision_proposer` resolves on rung 2.** The proposal message opens "Can
I understand the concern about documentation further?", which makes it
explicitly responsive to the documentation gap `arpit.goel` stated the
previous day (`2026-08-25 17:29` and `18:18`). `albert.lim 2026-08-26 08:57`
voices the same need again, but a later restatement does not transfer it.
Value: `@arpit.goel (raised the need; proposed by @sengkeong.ho)`. The
**proposing side** is `arpit.goel` + `sengkeong.ho`.

**Gate 2 — Final state:** Narrowed, one candidate. `sengkeong.ho 2026-08-26
08:59` narrows from "all markets" to this single variable and adds the
linking requirement. The linking clause splits across two fields on the
substitution test: the committed property — the documentation is reachable
from the config, making it the source of truth — survives any change of tool
and belongs in `decision_details`; "find a way to" is unresolved work with
no mechanism chosen, so it is part of the Action.

**Gate 3 — Closure signal:** PASS. `albert.lim 2026-08-26 08:57` — "ya that
helps" — explicit acceptance, unambiguous in form. The thread names no
specific approver for this proposal, so under Rule 3.2 a disposition from
any participant outside the proposing side can close it. `albert.lim` is
neither `arpit.goel` nor `sengkeong.ho`.

**This is where rung 2's "whoever stated it first" tiebreak earns its
keep.** Had `albert.lim`'s restatement carried the need to him, he would be
on the proposing side, his own acceptance would fall to Rule 3.3, and D2
would close as `uncertain` with no approver — from a thread that plainly
settled the question.

**Gate 4:** No unmet gate.

**Gate 5 — Scope fit:** PASS. The narrowing at `08:59` comes from
`sengkeong.ho`, who voiced the object and is therefore on the proposing
side, and lands after the acceptance at `08:57`. Under Rule 5.1 a narrowing
from that side does not reopen the candidate. **Read this against the side,
not the field** — `sengkeong.ho` is not the name in `decision_proposer`.

**Result:** `decision` · `approved` · `explicitly_stated`.

## Card

- `decision_title`: describes documenting the configs, **not** creating a
  wiki page.
- `decision_details`: the commitment to document the pricing configs for
  this ExP variable, with the wiki page as the agreed mechanism and the link
  from variable to page so it becomes the central source of truth.
- `pst`: `FF Ecommerce` — **inferred on a weaker chain than D1's.** The
  thread never places this sub-discussion in a product area directly; the
  basis is the surrounding thread. Flag it, and flag it as weaker.
- `rationale`: **three strands, and the first is the one runs drop.**
  - Legacy configs carry no approvals, documentation or freshness check, so
    mistakes go undetected and nobody can later reconstruct which merchants
    belong in a group or how they were derived (`@arpit.goel`).
  - Handling mex-specific pricing configs on ExP is established practice, so
    what is missing is documentation rather than the mechanism
    (`@sengkeong.ho`).
  - The team cannot today remove or trace configs ops set up long ago, which
    is what documenting new ones prevents (`@albert.lim`).

  The first strand is the need the proposal answers and sits *before* it in
  the thread. Rationale gathered only from the proposal message forward
  keeps the answer and discards the question.
- `decision_status`: `approved`
- `decision_proposer`: `@arpit.goel (raised the need; proposed by
  @sengkeong.ho)`
- `decision_approver`: `@albert.lim`
- `conditions`: no future-execution condition is established, so the card
  shows **`? - optional to fill`**. Never `null` — `references/rendering.md`
  forbids rendering an empty value that way.
- `refs`: available.

**Check which message came first before crediting a motivating concern.** It
is tempting to read the accepter as the person whose concern prompted the
proposal — `albert.lim` accepts at `08:57` and, in the same message, talks
about cleaning up legacy configs. But that remark arrives *after* his
acceptance, as supporting context. The concern that actually motivated the
exchange was raised by `arpit.goel` the day before.

---

# Actions

**Labels follow thread chronology, across the whole thread — not grouped by
Decision.** `references/extraction.md` is explicit. Two of the three sit in
the same message, where textual order is the only ordering available.

| | Task | Source | Attaches to |
|---|---|---|---|
| **A1** | Set up the wiki page for this variable, document the configs there, and link the variable to it | `sengkeong.ho 2026-08-26 08:59` | D2 |
| **A2** | Documented the thread in the Confluence wiki (completed within the thread) | `arpit.goel 2026-08-26 23:23` | D1 |
| **A3** | Add the logic that recreates the merchant list | `arpit.goel 2026-08-26 23:23` | D1 |

- **A1 is one Action, not two.** One message asks one person to stand up the
  page and wire the variable to it; they are steps of a single piece of
  work. A run that splits the linking into its own Action has put an
  artificial handoff in the record — three Actions across this thread, not
  four. `action_owner`: `@rahadiyan.wisesa (requested, not yet
  acknowledged)` — he does not speak again anywhere in the source. No date
  given, none guessed.
- **A2** is past tense with the in-thread completion note inside the
  `action` value. Owner `@arpit.goel`.
- **A3** has three named owners, stored as a list, requested and not
  acknowledged.

## Actions that may overlap

One entry expected, naming **`A1` and `A2`**.

Both produce a wiki page, and they sit on different Decisions, so nothing in
the card set ever shows them together. `A2` is done — `@arpit.goel` made it
inside the thread, documenting **the thread**. `A1` is outstanding with
`@rahadiyan.wisesa`, documenting **the variable's pricing configs**. Read
carefully they are two different pages; the thread never says so, and it is
the same tool, the same area, four minutes of reading apart.

This is the flagged shape exactly: one completed in-thread, one outstanding,
a shared artifact the thread never connected. A run that renders no entry
has missed it. **A run that merges them, drops either, or rewrites one to
reference the other is wrong** — the entry names the pair and leaves the
call to the reviewer, and nothing about it reaches the Bank.

---

# Topics routed to `no_decision_topics`

**Six entries.** This is the only place a reviewer can catch a decision the
skill invented or missed, so a run that renders `Not Identified as
Decisions` empty, or omits the category while having produced Gate 1
failures, has dropped them silently.

1. **FR-balancing principle during crunch.** `albert.lim 2026-08-26 08:51`
   asks what the principle is; `sengkeong.ho 08:54` answers with the
   fare-certainty / longer-SLA batching strategy. A question and a
   background-reasoning answer, no proposed course of action.
2. **Interim ZFF/EAR stopgap.** `sengkeong.ho 2026-08-26 09:06` — "our
   interim stopgap is to use mex ZFF and correct for dax EAR" — reported as
   the existing approach, not put forward for disposition. `ZFF` and `EAR`
   stay unexpanded; neither has a confirmed glossary entry.
3. **FR capacity vs. pricing-lever discussion.** `albert.lim 2026-08-26
   09:02` — batching limits on large Mart orders, pricing and visibility as
   the real FR levers, `DMS-Go+`. Background reasoning.
4. **Merchant-list governance explanation.** `moch.zulfa 2026-08-25 17:11`
   describes how the group is currently prioritized and maintained,
   answering a question. It feeds D1's `conditions` and motivates A3, but
   proposes nothing new.
5. **Capture-process messages.** `albert.lim 2026-08-26 08:50` asking
   `long.jin` to use the decision-capture tool, `long.jin 08:55` asking what
   sources are available, and `albert.lim 08:59` replying about extracting
   more context. Excluded by Gate 1's own carve-out.
6. **Automated bot message.** `Slackbot 2026-08-26 08:51` — "Heart, Hunger,
   Honour, Humility" — no proposal content.

---

# Review Notes, expected

Five of the six categories have content; `Source Limitations` does not.

- **Complete, but not a decision yet** — `D1`. What the reviewer can do
  about it. Does not repeat `Uncertain Decisions`' evidence.
- **Inferred Values to Confirm** — `D1 pst` and `D2 pst`, the second flagged
  as the weaker chain. **No `decision_approver` entry**: that value came
  from direct evidence and its open role is not an inferred value.
- **Uncertain Decisions** — `D1`, with the unmet eng-PIC gate and the
  unendorsed redirection, in plain language, with a source link. Never a
  gate id or an enum name.
- **Actions That May Overlap** — `A1` and `A2`.
- **Not Identified as Decisions** — the six above.
- **Source Limitations** — **absent.** The user answered `none`, which makes
  the bundle `complete`: they saw what was on offer and declined it, so
  nothing is missing that anyone wanted. An entry here on this run is wrong.

# External sources, expected

Three, all with real addresses, all rendered as links. The user declines
them, so none is read and none reaches `refs`.

| | Label from | Address |
|---|---|---|
| 1 | the ExP variable link | `https://experiments.grab.com/t/variables/foodSaverOptionDiscount/rollout/approve-request/455492?env=prd` |
| 2 | Jira `TECHOPS-117402` | `https://grabtaxi.atlassian.net/browse/TECHOPS-117402` |
| 3 | Confluence `foodSaverOptionDiscount` | `https://grabtaxi.atlassian.net/wiki/spaces/FSTF/pages/2341437752/foodSaverOptionDiscount` |

**None of these is the "no address" case.** The rule for a source Slack
shows without a resolvable address exists for other threads; this one does
not exercise it, and an earlier copy of this fixture made it look as though
it did.

---

# What runs get wrong on this thread

Kept short on purpose. Each of these has actually happened.

- **`MEX` read as Mexico.** The sentence reads perfectly and is false.
- **D2 titled after the wiki page** rather than the commitment.
- **D2's first rationale strand dropped** — the governance gap that
  motivated the proposal sits before it in the thread.
- **`arpit.goel` named as the eng PIC**, on a message that answers a
  different question.
- **`Not Identified as Decisions` omitted entirely** while the run's own
  reasoning listed the Gate 1 failures correctly.
- **Action labels grouped by Decision** instead of thread chronology.
