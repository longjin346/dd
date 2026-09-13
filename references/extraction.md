# Extraction — the judgment layer

This file governs one thing: reading a Slack thread and deciding what is a
decision, what its status is, who decided it, and what follow-up work
attaches to it. It does not cover how results are rendered as cards, how
conversational corrections are applied, or how an approved record is
committed — those live in other reference files and are only named here
where a handoff matters.

## Input to this layer

The judgment pass reads the Slack thread (and any external sources the user
selected) directly. There is no intermediate numbered-block transcript
(`[S0001]`, `[J0001]`, …) and no separate source-type prefix scheme. A
hand-assigned id that points at the wrong message fails silently and never
leaves the reasoning pass anyway — citing it bought no traceability. Instead:

- Keep messages in chronological order, root through final reply.
- Keep a reaction attached to the message it targets; it is evidence, not
  decoration.
- Use the current visible text of an edited message; strip only a literal
  `(edited)` marker.
- Label bot and workflow-app messages as automated. Never treat one as human
  agreement, even if its content looks like a disposition.
- Carry forward, rather than silently absorbing, any note that the fetch was
  truncated or that a linked source could not be read — these become
  `source_limitations`, not gaps the model papers over.

**Citing evidence.** Cite by author and displayed time, copied from the
thread — never computed or re-numbered:

- Default: `cui.ju 3:20 PM`
- Same author, more than one message in the same displayed minute: add a
  short verbatim fragment to disambiguate — `jomil.villareal 3:21 PM
  ("Product is from under Fulfillment")`.
- Thread spans more than one day: include the date —
  `jane.doe 2026-08-29 11:23 PM`.
- When the source carries clock times but no calendar dates, as some thread
  exports do, never synthesize one. Where the ordering is unambiguous —
  times ascend, then restart lower, which can only be the next day — label
  the spans relatively (`Day 1`, `Day 2`) and say that is what you did. An
  invented date is the same error as an invented due date.
- Do not attach the fragment by default. A classification reason routinely
  cites two or three messages in one sentence; a fragment on each would make
  it unreadable.

This format is for reasoning citations (`classification_refs`,
`classification_reason`) and for anything user-facing. The published `refs`
array is a separate, machine-precise layer — exact Slack permalink plus
verbatim excerpt — and is unaffected by this section.

## The gate model

Classification answers one question per candidate: *did this thread reach a
closed disposition on a concrete proposition?* Five gates answer it, in
order, and they do two different jobs:

- **Gate 1 is the admission gate.** It decides whether a Decision Candidate
  exists at all. Failing it removes the topic from the candidate set
  entirely — it goes to `no_decision_topics`, shown to the user with a
  reason, never silently dropped.
- **Gates 2 through 5 are classification gates.** They apply only to a
  candidate that already passed Gate 1. Failing one never discards the
  candidate — it stays `uncertain`, with the failing gate named in
  `classification_reason`, because the human reviewer makes the final call,
  not the model.

Preserve this asymmetry. It is the reason `uncertain` candidates carry real
information instead of being a dumping ground.

### Gate 1 — Is there a decision object?

A decision object is a proposition someone put forward *to be adopted,
rejected, or executed*. Look for proposal framing — a request for approval, a
proposal, a directive, a commitment, a recommendation, an explicit rejection.
The test is the framing, not the topic: the same subject can appear as a
proposal ("let's move the revamp to Q4") or as an observation ("Q4 is already
packed"), and only the first is an object.

Not decision objects, however much discussion they attract:

- Observations, opinions, warnings, and questions with no proposed course of
  action.
- Status updates and FYI content, including automated/bot messages.
- A course of action reported as already in place or decided elsewhere ("our
  interim stopgap is X"). The thread is relaying, not deciding. It becomes an
  object only if the thread reopens, modifies, or challenges it.
- Messages about the capture process itself — asking someone to record the
  thread, @-mentioning the bot, confirming it may proceed.
- Pure logistics ("I'll send the deck"). These never become objects. Never
  invent a decision object in order to house an action — where an Action
  belongs is settled under "Actions are attributes of Decisions" below, and
  no Action is ever discarded for being hard to place.

A topic with no concrete object fails Gate 1: route it to `no_decision_topics`
with a source-grounded reason and stop — do not run Gates 2–5, do not assign a
`decision_classification`, and never keep it as `uncertain`. Failing Gate 1 is
the only gate result that removes a topic from the candidate set.

The Slack thread defines candidate scope. Selected external sources may
explain or verify a candidate the thread raised; they never create one the
thread did not raise.

**Attribution: whose proposal is it?** A message can carry someone else's
proposal rather than its author's own. When a message explicitly marks
itself as relaying another person's request — "approval request from X",
"on behalf of X", "X asked me to raise this" — the object belongs to X, the
named source, not to the person who typed the message. Absent such a marker,
the object belongs to its author. This is a general rule about where
authority actually sits versus who is merely speaking; Gate 5 applies the
same rule to closing authority.

### Gate 2 — What is the final state of the object?

Follow the object through the whole thread before judging it. Threads
revise: a proposal gets narrowed, a condition gets attached, an approval gets
challenged. The candidate's state is the state at the end of the available
source, not at the moment it was first proposed. When the source is
truncated, "end of available source" means the last message read, not the
true thread end; treat closure found only in that tail as unverifiable and
lean toward `uncertain`.

- **Scope revisions are one candidate.** "Set up a wiki for all markets"
  narrowed later to "for this variable" is a single candidate carrying the
  final scope. Two candidates are distinct only when they answer different
  questions of the form "what did we decide about X"; if they answer the same
  question, merge them and keep the earliest message as primary evidence. Keep
  materially independent choices as separate candidates.
- **Later signals override earlier ones.** An objection, correction, or
  reversal after an apparent closure changes the state.
- **Reopening without re-closure is `uncertain`.** A candidate closed and
  then contested, reversed, or reopened, with no subsequent closure signal,
  is `uncertain`. Cite both the original closure message and the reopening
  message.

### Gate 3 — Is there a closure signal, from someone entitled to give it?

A closure signal is evidence that the object was adopted, rejected, or
explicitly deferred. Three rules govern whether a signal counts.

**Rule 3.1 — Form.** A closure signal is either (a) words that dispose of the
object — "approved", "let's do it", "no, we park this", "go ahead" — or (b) a
reaction or short reply whose meaning as approval or rejection is unambiguous
in context. If the meaning is arguable, it is not a closure signal; the
candidate is `uncertain`, and `classification_reason` says why the signal was
ambiguous.

**Rule 3.2 — Authority, as established by the thread itself.** When the
thread identifies whose disposition is being sought — an approval request
addressed to someone, a named gatekeeper, a delegated reviewer — only that
party's signal, or their explicit delegation, closes the candidate.
Acceptance from anyone else is engagement, not closure. When the thread
identifies no such party, a disposition from any participant other than the
proposer can close, subject to Rule 3.1. Never derive authority from
seniority, title, channel membership, message volume, attendance, or who
wrote the recap; authority comes only from what the thread itself assigns.

**Rule 3.3 — Not the proposer.** The proposer's own reaction to, or
restatement of, their proposal is never a closure signal. Neither is a recap
that merely repeats the proposal.

**Silence.** Ordinary silence — no reply, no reaction, the thread moving on —
is never a closure signal. The single exception is a no-objection mechanism
the thread itself declared ("if no objections by Friday we proceed") whose
stated period has ended within the available source with no objection
recorded. That, and only that, is `evidence_type: no_objection`.

### Gate 4 — Is there an unmet in-thread condition?

A closure signal can be real and still not close the object, because the
thread attached a gate to it. Distinguish two kinds of condition:

- **An unmet in-thread gate assigned to a named party** — "get approval from
  the eng PIC first", "pending legal's sign-off" — means the object is not
  closed until that party's signal appears in the source. Until then the
  candidate is `pending`, and the gate goes in `conditions`.
- **A condition on future execution** — "we'll revisit if volumes drop" —
  does not block closure. Classify by the closure signal and record the
  condition in `conditions`.

If you cannot tell which kind a condition is, treat it as an unmet gate and
say so in `classification_reason`.

### Gate 5 — Does the signal attach to the final object, from authority that was actually held?

Gate 3 tests who gave a signal and what form it took. It never tests what the
signal attached to, or whether whoever conferred the authority to close
actually possessed it. This gate closes both gaps. It only applies once Gate
3 has found a signal; if Gate 3 already fails, Gate 5 is moot.

**Rule 5.1 — Scope fit.** Check the closure signal against the final scope
Gate 2 established, not the scope at the moment of the signal.

- A **narrowing by the proposer**, after their proposal was accepted, does
  not reopen the candidate — the acceptance carries to the narrowed scope.
  The proposer retains authority over their own proposal's shape; narrowing
  it is not a new proposition requiring fresh consent, only a tightening of
  the one already accepted.
- A **widening or other material change** after acceptance does reopen the
  candidate. The accepted signal covered the earlier, smaller or different
  proposition, not the changed one, so the candidate reverts to `uncertain`
  under Gate 2's "later signals override" rule, awaiting a fresh signal
  against the new scope.

**Rule 5.2 — Authority conferral.** Authority to close can be transferred,
but only by the party the thread already entitled (Rule 3.2), or by a
mechanism the thread itself established — never by a third party's own
initiative. This is the same attribution principle from Gate 1 applied to
closing: a person can act on behalf of an authority they were actually given,
not one they assign to themselves or hand to someone else. When someone the
thread never entitled redirects the question to another reviewer, or attaches
a condition naming a different approver, that redirection is recorded as a
`conditions` entry naming the person who made it — it does not make the
redirected party's later signal a valid closure, unless the originally
entitled party endorses the redirection. The disqualified sources of
authority in Rule 3.2 (seniority, title, channel membership, message volume,
who wrote the recap) disqualify a claimed transfer exactly as they disqualify
a claimed closer.

A candidate that fails Gate 5 stays `uncertain`; cite the scope-mismatch or
the unendorsed redirection in `classification_reason`.

### Classification

Set `decision_classification: decision` only when all five gates pass:

1. A decision object exists (Gate 1).
2. Its final state is settled — no unresolved later conflict (Gate 2).
3. A closure signal exists, in valid form, from a party entitled to give it,
   cited to an exact message (Gate 3).
4. No unmet in-thread gate remains (Gate 4).
5. The signal attaches to the object as finally scoped, and any authority it
   relies on was actually held or genuinely transferred (Gate 5).

A topic that failed Gate 1 is not classified here — it already left for
`no_decision_topics`. For a candidate that passed Gate 1, set
`decision_classification: uncertain` whenever Gate 2, 3, 4, or 5 fails. Never
discard such a candidate; the whole point of `uncertain` is to put the
judgment in front of the reviewer with the reason attached.

Classification is independent of completeness. A decision with no recorded
approver or rationale is still a decision if the five gates pass — it is
*incomplete*, handled separately below. Conversely, a fully populated
candidate with no closure signal is still `uncertain`. Do not let one leak
into the other, and never let a missing field change a classification.

## Outcome and evidence type

Outcome and evidence type are read off the gate results; they are never
inputs to classification.

`decision_status`:

- `approved` — the object was adopted.
- `rejected` — the object was explicitly declined. Classifiable as a
  decision; not publishable in the MVP.
- `pending` — no disposition reached, an unmet in-thread gate remains, or the
  object was explicitly deferred. An explicit deferral is a *decision* with
  status `pending`, and the deferral statement is its closure signal. Not
  publishable in the MVP.

`evidence_type`:

- `explicitly_stated` — words, or an unambiguous reaction/reply, per Rule
  3.1.
- `no_objection` — a declared no-objection mechanism ran its course, per the
  silence rule in Gate 3.
- `none` — no closure evidence exists. Valid only with `pending`.

Generate candidates for every outcome, including `rejected` and `pending`.
Publication gating is enforced later, by the publisher, never during
extraction — a candidate silently dropped here can never be corrected in
review.

Valid combinations:

```text
decision  + approved + explicitly_stated
decision  + rejected + explicitly_stated
decision  + pending  + explicitly_stated     (explicit deferral)
decision  + approved + no_objection          (declared mechanism only)
uncertain + pending  + none
uncertain + pending  + explicitly_stated     (signal present but ambiguous,
                                              wrong authority, reopened,
                                              gated, or failing Gate 5's
                                              scope fit or transfer test)
```

Any other combination is a consistency error: re-examine the gate that
produced it, mark the candidate `uncertain` with `classification_reason:
"inconsistent gate results — needs review"`, and carry it forward rather than
calling the model again.

Apply these evidence rules throughout: never treat ordinary silence as
consent; never treat the proposer's reaction to their own proposal as
approval; treat a reaction as evidence only when its meaning is clear in
context; cite the exact source carrying the closure signal; never infer
approval from seniority or presumed authority.

## Populating the Decision record

**`decision_title`** — short, specific, neutral. Describe the subject of the
decision, not the approval process. Do not add unsupported certainty.

**`decision_details`** — one to three sentences stating the selected
direction or disposition. Preserve the FINAL scope after any revision. Keep
conditions in `conditions`, not folded into the title or details. For an
`uncertain` candidate, describe the proposed outcome without presenting it as
approved.

**`pst`** — select only an active value from `references/psts.json`. Use
explicit source evidence or clearly established project context; never infer
it from a channel name alone. When the sources support a reasonable but not
certain value — for example, a decision the thread explicitly calls "this
eComm decision" — fill the best-supported active value and flag it as
inferred so the reviewer confirms or changes it. Never stop to ask before
drafting. Leave it unresolved only when no source gives any basis at all.

**`decision_proposer`** — the person or group that introduced the object, per
the attribution rule under Gate 1: the named source of a relayed request, not
the relayer. Use only a source-established identity; never infer it from who
triggered the capture. Leave unresolved when the source does not establish
it.

**`decision_approver`** — the person, people, or forum whose signal was
accepted under Gates 3 and 5, and only them. Someone who engaged but was not
the entitled party, or whose standing came only from an unendorsed
redirection (Rule 5.2), is not the approver. For `evidence_type:
no_objection`, the approver is the declared mechanism or forum, not an
individual. Never infer it from seniority, attendance, channel membership,
authorship of a recap, or a request to record the thread. Leave it
unresolved when the source does not establish it — this is expected and
correct for many `pending` candidates; see Completeness below for why an
unresolved approver does not block finalizing the record.

**`rationale`** — reasons supported by the source only, explaining why the
direction was selected, rejected, or deferred. Keep it separate from
conditions. Never invent a rationale from general domain knowledge. Leave it
unresolved when the source provides none.

**`conditions`** — material assumptions, gates, exclusions, or dependencies,
including any unmet in-thread gate (Gate 4) and any unendorsed redirection or
third-party gate (Gate 5.2), named to the person who imposed it. Use `null`
when no condition is established. Do not convert ordinary discussion detail
into a condition.

**`refs`** — optional. For an automatically extracted candidate, include the
available Slack evidence because it makes the record easier to verify: exact
message link, verbatim excerpt, `ref_type`. For a manually added candidate,
`refs: []` is fine and never blocks review or publication.

## Actions are attributes of Decisions, not peers

The Decision is the core record. An Action is something captured about a
Decision, not an independent record with its own foreign key to maintain.

- Every Action attaches to exactly one Decision. Position expresses the
  link; a linked-decision identifier is derived at publication time from
  what the Action attaches to — it is never a value authored or corrected
  here.
- **All Action fields are optional.** An Action never blocks finalize and
  never blocks publication. Capture what the thread establishes — task,
  owner, due date — and leave the rest empty rather than demanding it.
- There is no orphan category. Attach each Action to the Decision it most
  plausibly serves. If the thread produced no Decision at all, there is
  nothing to attach to and nothing to capture — this is the only case where
  an action-shaped thing is dropped, and it follows from Gate 1, not from a
  separate action-linking rule.
- Keep a short label (`A1`, `A2`, …) in Slack-thread chronology so a reviewer
  can address an Action in conversation. It is a label, not a foreign key.
- Multiple named owners are normal; store them as a list.
- An Action already completed inside the thread is still captured, in past
  tense, with an inline note that it completed in-thread — e.g. "Documented
  the thread in the wiki (completed within the thread)." The note lives in
  the `action` value itself.
- An owner who was asked but never acknowledged is recorded with an inline
  note saying so — e.g. "@jane (requested, not yet acknowledged)." Never
  infer ownership from participation or expertise.
- Never guess a date. Preserve the original date phrase; resolve a calendar
  date only when it is certain from the source. No date is a normal, complete
  Action.

## Completeness: two required-field sets

Completeness is judged only after classification and record drafting, and it
never feeds back into classification. A decision with missing fields is
still a decision.

Two different questions get two different field sets. Conflating them is
what breaks `pending` candidates: a `pending` decision the thread never
resolved is a well-formed, valuable record, and demanding an approver for it
forces the reviewer to invent one, delete the thread's actual subject, or
never finalize — all three defeat the tool.

**Finalize-required** — what a faithful record of what this thread contains
needs before it can be locked for review:

- `decision_title`
- `decision_details`
- `pst`
- `decision_proposer`
- `rationale`
- `decision_status`

A candidate missing any of these is `completeness_status: incomplete`; list
every missing field path in `missing_required_fields`. `decision_approver` is
never in this set, regardless of `decision_status` — a `pending` candidate
with no approver, because none was ever given, is complete.

The field rules above say to leave `pst`, `decision_proposer`, and
`rationale` unresolved when the source does not establish them. That is
correct *at extraction* and does not conflict with requiring them here: the
reviewer was in the thread and can supply any of the three, so the finalize
prompt asks and they answer. `decision_approver` is the one field where that
does not work — if nobody approved, nobody can honestly supply a name — which
is exactly why it sits in the publish set instead.

**Publish-required** — what an *approved* decision needs before the
publication gate (defined elsewhere) will commit it: everything in
Finalize-required, plus `decision_approver`. This is proportionate rather
than arbitrary — the publisher only ever accepts `approved` candidates, so an
approver is exactly what an approved decision cannot lack, and nothing is
lost by not demanding one earlier.

Track Action completeness the same permissive way: an Action has no required
fields at all, at either tier. A missing owner or date on an Action never
marks its linked Decision incomplete.

When required information is missing: set `completeness_status: incomplete`,
add every missing field path to `missing_required_fields`, preserve the
candidate for review, never invent a value to make it look complete, and
never change `decision_classification` because a field is missing.

## Topics that are not Decisions

Each `no_decision_topics` entry is a Gate 1 failure: one concise,
source-grounded line naming the topic, the reason it was not identified as a
Decision, and a stable source link when available. Never expose gate ids or
internal reasoning here — the reason must read as plain language a reviewer
can act on.

## Worked examples

These trace the reference thread (`example slackthread/slack thread
converted in txt.txt`) line by line. Verify any new example the same way
before trusting it — a plausible-sounding reading that skips the actual
message order is exactly how the old draft misattributed a decision below.

### D1 — the Saver-discount approval request

- **Gate 1:** `jomil.villareal 3:18 PM` asks "may we proceed with this
  approval request from rahadiyan.wisesa" — an approval request, explicitly
  relayed. Object exists. Attribution: the object belongs to
  `rahadiyan.wisesa`, the named source, not to `jomil.villareal`, who is only
  transmitting it. `decision_proposer`: `@rahadiyan.wisesa`.
- **Gate 2:** the object's scope — a Saver discount for the named merchant
  group (Kalbe & Wardah) — is never itself narrowed or widened. The
  surrounding discussion about merchant-list governance is related context
  and produces Actions, not a scope change to this object.
- **Gate 3:** `cui.ju 3:20 PM` responds with a condition, not a disposition.
  `arpit.goel` probes repeatedly (`3:23 PM`, `5:06 PM`, `5:29 PM`, `6:18 PM`)
  but never says approved, rejected, or equivalent, and closes by saying "I
  have documented the thread here" (`arpit.goel 11:23 PM (Day 2)`) —
  documentation is a wrap-up, not a disposition. No closure signal exists.
  `evidence_type: none`.
- **Gate 4:** `cui.ju 3:20 PM` sets an unmet in-thread gate — "please inform
  the respective eng PIC and get approval from them first." No eng PIC signs
  off anywhere in the available source. Unmet.
- **Gate 5:** `cui.ju 3:22 PM` — "arpit.goel could you help to check?" —
  redirects review to `arpit.goel`. The approval was addressed to
  `randy.tedjakusuma` / `@oncall-lead` at `3:18 PM`; `cui.ju` is not shown to
  be that party, and `randy.tedjakusuma` never reappears to endorse the
  redirect. Under Rule 5.2 the redirection does not transfer closing
  authority to `arpit.goel` — moot in practice here since Gate 3 already
  found no disposition from him, but it is why his extensive engagement could
  never have closed this candidate even if he had said "approved."
- **Result:** `uncertain`, `decision_status: pending`, `evidence_type: none`.
  `decision_approver`: unresolved. `conditions`: eng-PIC approval unmet
  (`cui.ju 3:20 PM`); review redirected to `@arpit.goel` by `@cui.ju`,
  unendorsed by the originally addressed `@randy.tedjakusuma`
  (`cui.ju 3:22 PM`). `pst`: `FF Ecommerce` (inferred — the thread later
  calls this "this eComm decision" and ties the product to Fulfillment;
  flagged for reviewer confirmation).
- This candidate is finalizable exactly as drafted: every Finalize-required
  field is present, and the empty `decision_approver` does not block that,
  per Completeness above.

### D2 — the wiki page to document the pricing config

- **Gate 1:** `sengkeong.ho 8:55 AM` — "can we set up an wiki page to
  document this for all markets?" — a proposal. Object exists,
  `decision_proposer`: `@sengkeong.ho`.
- **Gate 2:** `sengkeong.ho 8:59 AM` — "rahadiyan.wisesa lets set up a wiki
  page for this variable and document all the configs here" — narrows the
  object from "all markets" to the single variable. Final scope is the
  narrowed one.
- **Gate 3:** `albert.lim 8:57 AM` — "sengkeong.ho ya that helps" — explicit
  acceptance. The thread names no specific approver for this proposal, so
  under Rule 3.2 any participant other than the proposer can close it;
  `albert.lim` is such a participant. Valid, unambiguous form.
- **Gate 5 (scope fit):** the narrowing at `8:59 AM` comes from
  `sengkeong.ho`, the proposer, and happens after `albert.lim`'s acceptance
  at `8:57 AM`. A proposer's own narrowing after acceptance does not reopen
  the candidate, so the acceptance carries forward to the narrowed scope.
- **Result:** `decision`, `decision_status: approved`,
  `evidence_type: explicitly_stated`. `decision_approver`: `@albert.lim`.

  **Correcting a prior misreading:** an earlier draft of this example
  described the accepter as "the person whose cleanup concern prompted" the
  proposal. That does not hold up against the thread. The governance concern
  that motivated the whole exchange — "no governance on the grabx group... no
  documentation on knowing what the right set of merchants are" — was raised
  earlier by a different person, `arpit.goel`, at `5:29 PM` and `6:18 PM` the
  day before. `albert.lim`'s own remark about cleaning up legacy pricing
  configs arrives at `8:57 AM`, immediately *after* his acceptance, as
  supporting context he adds — not as the concern that prompted
  `sengkeong.ho`'s proposal. Do not attribute a stakeholder's motivating
  concern to whoever happens to accept a later, related proposal without
  checking which message came first and who said which.

- **Action (attaches to D2):** `sengkeong.ho 8:59 AM` asks
  `@rahadiyan.wisesa` to set up the wiki page. `rahadiyan.wisesa` does not
  speak again in the available source. `action_owner`: "@rahadiyan.wisesa
  (requested, not yet acknowledged)". No date given; none guessed.

### Actions attaching to D1

- `arpit.goel 11:23 PM (Day 2)` asks `@sengkeong.ho`, `@moch.zulfa`, and
  `@rangga.pratama` to add the logic that recreates the merchant list. Three
  named owners, store as a list; requested, not yet acknowledged in the
  available source; no date given.
- The same message — "I have documented the thread here" — is a completed
  action: `action`: "Documented the thread in the Confluence wiki (completed
  within the thread)", owner `@arpit.goel`, no date needed.

### Not decisions

- "Our interim stopgap is to use mex ZFF and correct for dax EAR by
  overpaying for these jobs" (`sengkeong.ho 9:06 AM`) — reported as the
  existing approach, not put forward for disposition. Fails Gate 1.
- The fare-certainty/batching principle (`sengkeong.ho 8:54 AM`) and the FR
  capacity/pricing-lever discussion (`albert.lim 9:02 AM`) — background
  reasoning, no proposed course of action. Fails Gate 1.
- `moch.zulfa 5:11 PM` explaining how the merchant group is currently
  prioritized and maintained, answering a question — describes existing
  practice, proposes nothing new. It feeds D1's conditions and motivates an
  Action, but is not itself an object.
- `albert.lim 8:50 AM` asking `long.jin` to use the capture tool, and
  `long.jin 8:55 AM` asking what sources are available — messages about the
  capture process itself. Excluded by Gate 1's explicit carve-out.
- `Grab 8:51 AM` — "Heart, Hunger, Honour, Humility" — an automated values-bot
  message with no proposal content.
