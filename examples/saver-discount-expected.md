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

**Six of seven are now answered by the thread owner**, and the answers are
folded into the file below. What remains open is marked. Two of the six
reversed what this file previously asserted — those are the valuable ones,
because a baseline derived from the rules could never have produced them.

1. ~~**Did "ya that helps" approve the commitment to document?**~~
   **Answered: yes.** D2 is `approved`, `@albert.lim` is the approver. The
   run that read it as `pending` was wrong.
2. ~~**Whose decision is D2?**~~ **Answered: `@arpit.goel`** — he raised
   it, and the field carries that one name. The voicer marker the owner
   dropped is not coming back: it decides Gate 3 during classification and
   is not a stored value.
3. ~~**Is D2 "record these configs" or "make a wiki page"?**~~
   **Answered: record the configs.** The title says document, and the page
   is named as the agreed platform inside the details.
4. ~~**Is `@arpit.goel` the "respective eng PIC"?**~~ **Answered: yes — he
   is the pricing eng PIC.** So the awaited party is one person, not two:
   Randy is on leave and Arpit covers that role, which makes `cui.ju 15:22`
   the answer to both questions on the table. This file previously read the
   two as separate and left the role unnamed. Gate 5 no longer finds an
   unendorsed redirection.
5. **Still open — is "the list will continue to be reviewed and maintained"
   (`@moch.zulfa 17:11`) a condition on execution?** Taken as yes, so it
   sits in D1's `conditions`. *If it is just background:* `conditions` is
   empty for D1.
6. ~~**Does `@arpit.goel`'s governance concern belong to D1 or D2?**~~
   **Answered: D2.** It is the first strand of D2's rationale. A run that
   folds it into D1's is recording an argument against something as an
   argument for it.
7. ~~**The wiki page `@arpit.goel` already made — D1 or D2?**~~
   **Answered: neither — it is not a separate Action.** It is the same piece
   of work as the page requested at `08:59`, so D1 carries only the
   merchant-list change. The `Actions That May Overlap` check raised exactly
   this pair; the question was right and this file's answer was wrong.

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
sets an in-thread gate. The PIC is `@arpit.goel`, and he never signs off
anywhere in the source: he asks questions and the thread ends. The gate is
unmet because the approval never came, not because nobody could be found to
give it.

**Gate 5 — Scope/authority fit:** PASS, and moot in practice since Gate 3
found no signal. `cui.ju 2026-08-25 15:22` — "@arpit.goel could you help to
check?" — is **routing to the eng PIC the gate at 15:20 called for**, not a
third party redirecting review on its own initiative. `@arpit.goel` is that
PIC (confirmed by the thread owner), so nothing needs transferring and Rule
5.2 does not bite. Had he said "approved", it would have closed this
candidate.

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
- `decision_approver`: **`@arpit.goel (awaiting approval)`** — the pricing
  eng PIC, confirmed by the thread owner.

  Rung 1 fails outright, since Gate 3 found no closure signal, so extraction
  drops to rung 2 and records who is supposed to approve. One party, not
  two: the request goes to `@randy.tedjakusuma / @pricing-team`
  (`2026-08-25 15:18`), `cui.ju 15:20` requires the respective eng PIC's
  sign-off, and `cui.ju 15:22` routes it — "@arpit.goel could you help to
  check?"

  **Those look like two separate awaited parties and are one.** Randy is on
  leave (`jomil.villareal 15:21`), and Arpit is the pricing eng PIC, so
  `15:22` answers the cover-for-Randy question *and* names the eng PIC —
  the two questions have the same answer.

  This is worth stating because the wording invites a wrong turn. Earlier
  versions of this file argued that `15:22` answers only the cover question
  and therefore leaves the eng-PIC role unnamed. The sequence does read that
  way; it is still wrong, because the premise that the two questions have
  different answers is false.

  The value is reached by inference — the thread never says Arpit holds the
  role — so it is flagged under `Inferred Values to Confirm`. A run that
  leaves the role unnamed has been too literal, not disobedient.

- `conditions`: the merchant group is a business-team priority list,
  reviewed and maintained against partnership needs and merchant
  performance rather than fixed, and adjustable as relevance changes
  (`@moch.zulfa`).

  **This field is not empty.** The eng-PIC gate and the unendorsed
  redirection are approval-process facts, not conditions on execution — they
  belong in `classification_reason`, and a run that files either here has
  put process into a field about the decision.
- `refs`: available — the approval-request message, the eng-PIC condition,
  the routing to `@arpit.goel`, the rationale messages.

**`classification_reason`** should name the deciding gate and nothing else:
approval requested in `jomil.villareal 2026-08-25 15:18`; eng-PIC sign-off
required by `cui.ju 15:20` and routed to `@arpit.goel` at `15:22`; he
questions the request through to the end of the thread and never disposes of
it. **One gate decides this candidate now, not three** — the earlier reading
also cited an unendorsed redirection and a missing entitled party, and
neither survives the eng-PIC correction.

**Completeness:** all seven required fields present, `decision_approver`
included. An awaited value, marked as awaited, is a filled and honest value,
not a gap. D1 is finalizable exactly as drafted — and not publishable,
which is a different thing and is what `Complete, but not a decision yet`
exists to say.

---

# D2 — Document MEX-specific configs on ExP

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
Value: `@arpit.goel` — one name, which is all this field ever holds. The
**proposing side** is `arpit.goel` + `sengkeong.ho`, used to decide Gates 3
and 5 below and stored nowhere.

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

- `decision_title`: **Document MEX-specific configs on ExP**
- `decision_details`: the need to document the tactical pricing configs for
  the ExP variable, with the wiki page as the agreed platform, and the
  variable linked to that page so the change is traceable.
- `pst`: **`Pax Pricing`** — the same as D1's, and for a reason worth
  stating: **D2 documents the behaviour of D1**, so it takes the PST of the
  decision it is about. A decision that records, governs or tracks another
  one does not get its own subject area; it inherits.

  This is not something the thread says, and it is not something the current
  rules derive. A run reaching it has to notice that D2's subject is D1.

- `rationale`: **three strands, and the first is the one runs drop.**
  - Legacy configs carry no approvals, documentation or freshness check, so
    mistakes go undetected and nobody can later reconstruct which merchants
    belong in a group or how they were derived (`@arpit.goel`).
  - Handling mex-specific pricing configs on ExP is established practice, so
    what is missing is documentation rather than the mechanism
    (`@sengkeong.ho`).
  - The team has had difficulty cleaning up legacy price configurations
    because nobody knows the rationale or the owner of those setups; proper
    documentation prevents this recurring (`@albert.lim`).

  The first strand is the need the proposal answers and sits *before* it in
  the thread. Rationale gathered only from the proposal message forward
  keeps the answer and discards the question.
- `decision_status`: `approved`
- `decision_proposer`: **`@arpit.goel`** — he raised this.

  **One name, no marker.** Earlier versions carried the voicer inline as
  `@arpit.goel (raised the need; proposed by @sengkeong.ho)`; the owner's
  value dropped it and the rules now agree. That `@sengkeong.ho` voiced the
  proposal still decides Gate 3 — it is why `albert.lim` can close it — but
  that question is settled during classification, with the thread in hand,
  and the answer is not part of the record. A run that renders the marker
  is wrong.
- `decision_approver`: `@albert.lim`
- `conditions`: `? - optional to fill`
- `refs`: available

**Check which message came first before crediting a motivating concern.** It
is tempting to read the accepter as the person whose concern prompted the
proposal — `albert.lim` accepts at `08:57` and, in the same message, talks
about cleaning up legacy configs. But that remark arrives *after* his
acceptance, as supporting context. The concern that actually motivated the
exchange was raised by `arpit.goel` the day before.

---

# Actions

**Two Actions, not three.** Labels follow thread chronology across the whole
thread, never grouped by Decision.

| | Task | Source | Attaches to |
|---|---|---|---|
| **A1** | Set up the wiki page for this variable, document the configs there, and link the variable to it | `sengkeong.ho 2026-08-26 08:59` | D2 |
| **A2** | Add the logic that recreates the merchant list | `arpit.goel 2026-08-26 23:23` | D1 |

- **A1 is one Action, not two.** One message asks one person to stand up the
  page and wire the variable to it; they are steps of a single piece of
  work. A run that splits the linking into its own Action has put an
  artificial handoff in the record. `action_owner`:
  `@rahadiyan.wisesa (requested, not yet acknowledged)`.
- **A2** has three named owners, stored as a list, requested and not
  acknowledged. No date given, none guessed. This is the only Action D1
  carries — the change someone has to make.

## The page arpit.goel made is not a third Action

`arpit.goel 2026-08-26 23:23` says "I have documented the thread here", and
earlier versions of this file recorded that as its own completed Action on
D1, reasoning that it documents *the thread* while A1 documents *the
variable's configs* — two different pages.

**They are the same piece of work** (confirmed by the thread owner). So it
is not a second Action; it is work against A1.

This is the single most useful thing the `Actions That May Overlap` check
does, and this thread is its case: the two sat on different Decisions, so
nothing in the card set ever showed them together, and only a flag brings
them into the same view. The check was right to raise the pair. What this
file got wrong was the answer, not the question.

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
   answering a question. It feeds D1's `conditions` and motivates A2, but
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
- **Inferred Values to Confirm** — three entries.
  - `D1 pst`: `Pax Pricing`, reached from knowing what a Saver discount is
    rather than from anything the thread states.
  - `D2 pst`: `Pax Pricing`, inherited because D2 documents D1.
  - `D1 decision_approver`: `@arpit.goel`, reached from his conduct through
    the thread. Nothing says he holds the eng-PIC role.

  **This reverses what earlier versions of this file expected.** They said
  the approver carried no entry, on the reasoning that it came from direct
  evidence. It does not: naming him is an inference, and one a reviewer
  should be asked to confirm.
- **Uncertain Decisions** — `D1`, with the unmet eng-PIC gate, in plain
  language, with a source link. Never a gate id or an enum name. **The
  unendorsed redirection is not a second reason** — it did not survive the
  eng-PIC correction, and a run still citing it is reading the old file.
- **Actions That May Overlap** — **absent.** With the duplicate resolved
  there is one wiki Action, so no pair remains to flag. A run that has not
  resolved it will raise the pair, and raising it is correct behaviour on
  the evidence the thread gives; the entry disappears only once someone
  answers.
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
- **The eng-PIC role left unnamed**, or recorded as a second awaited party
  alongside `@randy.tedjakusuma`. Reading `cui.ju 15:22` as answering only
  the cover-for-Randy question is defensible from the wording and still
  wrong: Arpit is the pricing eng PIC, so both questions resolve to him.
- **`Not Identified as Decisions` omitted entirely** while the run's own
  reasoning listed the Gate 1 failures correctly.
- **Action labels grouped by Decision** instead of thread chronology.
