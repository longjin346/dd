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

This author + time format governs internal reasoning, `classification_refs`,
`classification_reason`, and Review Notes — anywhere the reader may need to
locate the exact message to verify a judgment. It is not used inside a
Decision record field that appears on the card (`rationale`,
`decision_details`, `conditions`): there, cite the person only, with no
timestamp — `(@rahadiyan.wisesa)`, never `(rahadiyan.wisesa 3:26 PM)`. The
timestamp does little work on the card itself — `refs` sits two lines below
with exact permalinks — and on a thread whose export carries clock times but
no dates, a bare time on the card is actively ambiguous. The published `refs`
array is a separate, machine-precise layer — exact Slack permalink plus
verbatim excerpt — and is unaffected by this section.

**Person mentions render as `@alias`, everywhere.** Anywhere a person is
named — inside `rationale`, `decision_details`, `conditions`, a
`classification_reason` clause outside its author+time citations, or Review
Notes prose — use their Slack alias, `@long.jin`, never a bare handle and
never a display name. This is a general rule, not one limited to
`decision_proposer`, `decision_approver`, and `action_owner` — those fields
simply happen to be entirely a person value. A non-person approver (a
declared no-objection forum) stays a plain name with no `@`. An author+time
citation itself — `cui.ju 3:20 PM` — is a distinct notation, not a mention,
and keeps the form this section already defines.

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

**The commitment is the object; the vehicle that carries it is not.** Gate 1
decides not only *whether* there is an object but *which* proposition it is,
and a proposal routinely names an instrument — a wiki page, a dashboard, a
recurring meeting, a ticket, a channel — as the way to meet a need. Naming
the instrument as the decision records the tool and loses the commitment.

**Test it by substitution.** Swap the instrument for a different one and ask
whether what was agreed still stands. If it does, the commitment is the
object: the instrument is how it gets done, and it belongs in
`decision_details` as the agreed mechanism and in the Action as the step
someone executes — never as the subject of `decision_title`. If swapping the
instrument destroys the agreement, the instrument *is* the object; "we
standardize on Confluence rather than Notion" is a decision about the tool,
and abstracting it into "we will document things" would record something
nobody agreed to.

Two signals in the thread usually settle it:

- **The proposal states its own purpose.** "can we set up an wiki page *to
  document this*" puts documenting as the end and the page as the means. A
  proposal offered conditionally — "if it helps" — is being put forward as
  one way to meet a need, not as the thing itself.
- **The acceptance restates the commitment without the instrument.** "part
  of solving that problem is to properly document the incoming new ones" is
  the accepter saying what they understood themselves to be agreeing to.

Where both point the same way, take the commitment. Where the thread only
ever discusses the instrument and no underlying commitment is stated, the
instrument is all there is — use it, and do not invent a purpose it was
serving.

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
identifies no such party, a disposition from any participant outside the
proposing side can close, subject to Rule 3.1 — the side, not just the
`decision_proposer` name, so that whoever voiced the proposal cannot close
it either. Never derive authority from
seniority, title, channel membership, message volume, attendance, or who
wrote the recap; authority comes only from what the thread itself assigns.

**Rule 3.3 — Not the proposing side.** A reaction to, or restatement of,
the proposal by anyone on the proposing side — the `decision_proposer` or
whoever voiced the object — is never a closure signal. Neither is a recap
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
  candidate is `pending`. This is a fact about the approval process, not
  about the decision itself, so it never goes in `conditions`: name it in
  `classification_reason` as the deciding gate, and it reaches the reviewer
  through Review Notes' `Uncertain Decisions` category
  (`references/rendering.md`).
- **A condition on future execution** — "we'll revisit if volumes drop" —
  does not block closure. Classify by the closure signal and record the
  condition in `conditions` — this is the only kind of condition that
  belongs there.

If you cannot tell which kind a condition is, treat it as an unmet gate and
say so in `classification_reason`.

### Gate 5 — Does the signal attach to the final object, from authority that was actually held?

Gate 3 tests who gave a signal and what form it took. It never tests what the
signal attached to, or whether whoever conferred the authority to close
actually possessed it. This gate closes both gaps. It only applies once Gate
3 has found a signal; if Gate 3 already fails, Gate 5 is moot.

**Rule 5.1 — Scope fit.** Check the closure signal against the final scope
Gate 2 established, not the scope at the moment of the signal.

- A **narrowing from the proposing side**, after the proposal was accepted,
  does not reopen the candidate — the acceptance carries to the narrowed
  scope. That side retains authority over its own proposal's shape;
  narrowing it is not a new proposition requiring fresh consent, only a
  tightening of the one already accepted. This covers a narrowing by
  whoever voiced the object, which under rung 2 of `decision_proposer` is
  not the name in that field.
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
consent; never treat a reaction from the proposing side to its own proposal
as approval; treat a reaction as evidence only when its meaning is clear in
context; cite the exact source carrying the closure signal; never infer
approval from seniority or presumed authority.

## Populating the Decision record

**`decision_title`** — short, specific, neutral. Describe the subject of the
decision, not the approval process, and not the instrument that carries it
(Gate 1's substitution test). Do not add unsupported certainty.

**`decision_details`** — what was decided, at its final scope, with the
specifics that make it actionable: what is being done, to or for what, by
what mechanism, within what boundary. Preserve the FINAL scope after any
revision. Where Gate 1's substitution test moved an instrument out of the
object, "by what mechanism" is where it lands — the agreed vehicle is
recorded here as one clause, not promoted to the subject of the decision and
not dropped.

Write for someone who was not in the thread and reads this record months
later, when the thread is gone or unsearchable. They should understand what
was decided without opening `refs`. Err toward keeping a material
specific — a named group, the system or config the change lands in, a
figure, an exclusion — rather than compressing it away. Two to four
sentences is typical, but length is not the constraint; substance is. A
one-line summary that forces a reader back to the source has failed at the
one job this field has.

What does not belong: the shape of the conversation ("X proposed, Y asked,
Z agreed"), anything already carried by `decision_proposer`, `conditions`
or `refs`, and a restatement of `decision_title`. Keep conditions in
`conditions`, not folded into the title or details. Never state or imply
whether the decision was approved, rejected,
pending, or blocked — that is what `decision_status` and `evidence_type`
carry, and restating it here only duplicates them while risking a record
that goes stale the moment `decision_status` is corrected. Test: the
sentence must stay true even if `decision_status` changes later.

**`pst`** — select only an active value from `references/psts.json`. Use
explicit source evidence or clearly established project context; never infer
it from a channel name alone. When the sources support a reasonable but not
certain value — for example, a decision the thread explicitly calls "this
eComm decision" — fill the best-supported active value and flag it as
inferred so the reviewer confirms or changes it. Never stop to ask before
drafting. Leave it unresolved only when no source gives any basis at all.

**`decision_proposer`** — the party the decision exists to serve: whoever
raised the need it answers, not whoever happened to type the proposal. This
is the Gate 1 attribution rule generalized. That rule already separates
these two roles for a relayed request; a thread separates them a second way,
when one person states a gap and a different person offers the thing that
closes it. One field covers both — work down this ladder and stop at the
first rung the source supports:

1. **A relayed request** — the named source, not the relayer.
   `jomil.villareal` relaying `rahadiyan.wisesa`'s approval request gives
   `@rahadiyan.wisesa`.
2. **A solution offered to a need someone else raised** — the person who
   raised the need, when the message introducing the object is explicitly
   responsive to it: it answers, quotes, or is addressed to that need. Where
   several people voiced the same need, it belongs to whoever stated it
   first; a later restatement by someone else does not transfer it. Record
   the person who voiced the proposal inline, as `@needraiser (raised the
   need; proposed by @voicer)`, so one field keeps both facts.
3. **Otherwise** — whoever introduced the object.

Rung 2 is deliberately narrow. A need is a stated gap, requirement, or
problem someone asked to have addressed — not background commentary, not an
opinion, and not any complaint that merely sits earlier in the thread. When
the responsive link is not explicit, drop to rung 3. Guessing here writes a
name into the record that the thread does not support, and puts the wrong
person at the top of the card six months later.

**The proposing side.** Rung 2 splits one role across two people, so the
gate rules that turn on "the proposer" need both: the **proposing side** is
the `decision_proposer` together with whoever voiced the object. At rungs 1
and 3 the side has exactly one member and nothing changes. Rules 3.2, 3.3
and 5.1 are stated against the side, not the field — read them that way, and
never narrow them back to the field's single name. Getting this backwards
lets the person who proposed something approve it themselves.

Use only a source-established identity; never infer it from who triggered
the capture. Leave unresolved when the source does not establish it.

**`decision_approver`** — required for every candidate, no tier and no
exception. Fill it by working down this fallback ladder and stop at the
first rung the source supports:

1. **Who approved it.** The person, people, or forum whose signal was
   accepted under Gates 3 and 5, and only them. Someone who engaged but was
   not the entitled party, or whose standing came only from an unendorsed
   redirection (Rule 5.2), is not the approver. For
   `evidence_type: no_objection`, the approver is the declared mechanism or
   forum, not an individual. Never infer it from seniority, attendance,
   channel membership, authorship of a recap, or a request to record the
   thread. Render as the plain value.
2. **Who is supposed to approve it, when nobody has yet.** The thread
   routinely establishes this even when no approval arrived — an approval
   request addressed to someone, a named gatekeeper, a required sign-off
   role. Record that party, explicitly marked as awaited rather than given:
   `@name (awaiting approval)` — the same shape `action_owner` already uses
   for `@jane (requested, not yet acknowledged)`. An awaited value must never
   render as a bare name; the inline marker is what stops a reader from
   mistaking an outstanding request for a disposition that happened. When
   the thread names the awaited party only by role and a specific person can
   be resolved from what the thread shows, resolve it and flag the inference
   for the reviewer under Review Notes' `Inferred Values to Confirm`
   (`references/rendering.md`), exactly as an inferred `pst` already is.
   When the role cannot be resolved to a person, record the role exactly as
   the thread stated it, still marked as awaiting approval — never guess a
   name to fill it.

   **Before resolving a role to a person, check what question the naming
   message was actually answering.** A thread that requires "the eng PIC's
   sign-off" and, two messages later, names someone, has often answered a
   different question in between — who is covering for an absent addressee,
   who can take a first look — and the name attaches to that question, not
   to the role. Read the intervening messages, not just the two that seem to
   pair up. Being asked to check something is not the same as holding the
   role whose sign-off was required, and a person put in this field on that
   reading becomes someone a reviewer may go chase, or whose later "ok" gets
   read as the approval. When the sequence is ambiguous, leave the role
   unresolved; an unnamed role is a smaller error than a confidently wrong
   name.

   This rung is independent of Gate 5.2: whether a
   redirected or role-holding party's eventual signal would actually count
   as closure is a separate question from who the thread says is awaited,
   and answering the second never disturbs the gate's answer to the first.
3. **Nothing at all.** Only when the source establishes neither of the
   above. Leave it unresolved; the card shows the standard `? - need to
   fill` marker and the finalize prompt asks for it, stating plainly what is
   wanted — who approved this, or, failing that, who it is awaiting. Never
   write a value on the reviewer's behalf here.

**`rationale`** — why this direction was selected, rejected, or deferred,
drawn only from the source.

**Capture every distinct reason the thread gave, not only the first one or
the one the proposal led with.** Threads routinely justify the same decision
from two directions — one participant argues it operationally, another
commercially — and keeping only the earliest silently discards the half of
the case a later reader may care about most. When more than one person
contributed a reason, attribute each with `(@alias)` so the record shows the
case was made from more than one side.

**The reason that motivated the proposal is usually stated before it, and is
the one most often dropped.** Where `decision_proposer` resolved to rung 2 —
someone offered a solution to a need another person raised — the need itself
is a rationale strand and must appear here, cited to whoever raised it.
Rationale gathered only from the proposal message forward keeps the answer
and discards the question, which is exactly the context a later reader is
looking for.

Keep it separate from conditions. Never invent a rationale from general
domain knowledge. Leave it unresolved when the source provides none.

**`conditions`** — a condition on future execution only (Gate 4's second
kind) — "we'll revisit if volumes drop" — named to the person who raised it
when relevant. An unmet in-thread approval gate and an unendorsed redirection
or third-party gate (Gate 5.2) are facts about the approval process, not
about the decision's execution: they never populate this field. Cite them in
`classification_reason` instead, and they reach the reviewer through Review
Notes' `Uncertain Decisions` category (`references/rendering.md`) — never in
both places at once. Use `null` when no future-execution condition is
established. Do not convert ordinary discussion detail into a condition.

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

## Completeness: one required-field set

Completeness is judged only after classification and record drafting, and it
never feeds back into classification. A decision with missing fields is
still a decision.

**Required to finalize** — what a faithful record of what this thread
contains needs before it can be locked for review:

- `decision_title`
- `decision_details`
- `pst`
- `decision_proposer`
- `rationale`
- `decision_status`
- `decision_approver`

A candidate missing any of these is `completeness_status: incomplete`; list
every missing field path in `missing_required_fields`.

`decision_approver` sits in this set without reintroducing the bug it once
caused, and the reason is worth stating precisely, because the bug was never
"the field is required" — it was that the only way to satisfy the
requirement was to name someone who did not exist.

It reaches the reviewer unresolved only at rung 3 of the fallback ladder
above — when the thread establishes neither who approved the candidate nor
who is awaited to. That is rarer than it once was: most candidates the
thread never closed still name an addressee, a gatekeeper, or a required
sign-off role, and rung 2 fills the field from that, clearly marked as
awaited rather than given. When rung 3 is genuinely reached, the
missing-fields prompt states plainly what is wanted
(`references/rendering.md`) — who approved this, or who it is awaiting — and
the reviewer, who was in the thread, supplies it. That holds for every field
in this set: `pst`, `decision_proposer` and `rationale` are likewise left
unresolved when the source does not establish them.

The line this skill holds is not "never ask the reviewer for anything." It
is that a reviewer may be asked to **confirm what the thread shows**, and
never to **supply what it does not**.

Publication adds exactly one more check on top of this set, owned by
`references/review.md`: an `approved` candidate cannot carry a
`decision_approver` that still reads as awaited — that is a contradiction
the publication gate catches, not a missing-field gap tracked here.

`references/schema.md`'s publication list additionally names `candidate_id`
and `evidence_type`, which this layer always assigns itself — they are never
missing and never something to prompt anyone for.

Track Action completeness the same permissive way: an Action has no required
fields at all. A missing owner or date on an Action never marks its linked
Decision incomplete.

When required information is missing: set `completeness_status: incomplete`,
add every missing field path to `missing_required_fields`, preserve the
candidate for review, never invent a value to make it look complete, and
never change `decision_classification` because a field is missing.

## What this layer hands off

Keep two things separate in the candidate you produce: the **record**, which
is the proposed Decision Bank entry and whose field shapes are defined in
`references/schema.md`, and the **workflow** bookkeeping, which exists only
to drive review and never reaches the Bank.

Workflow carries: `decision_classification` (`decision` or `uncertain`),
`decision_status`, `evidence_type`, `classification_reason` (one concise,
source-verifiable sentence naming the gate that decided it — "Approval
requested in `jomil.villareal 3:18 PM`; eng-PIC gate set in
`cui.ju 3:20 PM`; no signal from that party through the end of the thread",
never "seems approved"), `classification_refs`, `completeness_status`, and
`missing_required_fields`.

Alongside the candidates sit the Actions attached to each, plus
`no_decision_topics` and any `source_limitations` carried from acquisition.

Two of the workflow fields are not purely internal: `decision_status` is
shown on the card as a reviewable field, and `evidence_type` travels into
the published record with it. Everything else in that list is dropped at
publication — `references/review.md` §9 owns that step. Never expose a
workflow field name, a gate id, or `classification_reason` in its raw form
to the user; Review Notes shows a rewritten, plain-language version
(`references/rendering.md`).

Assign `candidate_id` (`D1`, `D2`, …) and Action labels (`A1`, `A2`, …) in
thread chronology. Once issued, an identifier is never reused, including
after a drop or a merge — `references/review.md` §2 owns that rule for the
rest of the session.

## Topics that are not Decisions

Each `no_decision_topics` entry is a Gate 1 failure: one concise,
source-grounded line naming the topic, the reason it was not identified as a
Decision, and a stable source link when available. Never expose gate ids or
internal reasoning here — the reason must read as plain language a reviewer
can act on.

## Worked examples

These trace the reference thread (`examples/saver-discount-thread.txt`) line
by line. Its full expected output is recorded in
`examples/saver-discount-expected.md` — when any rule in this file changes,
re-run that thread and diff against it. Verify any new example the same way
before trusting it — a plausible-sounding reading that skips the actual
message order is exactly how the old draft misattributed a decision below.

### D1 — the Saver-discount approval request

- **Gate 1:** `jomil.villareal 3:18 PM` asks "may we proceed with this
  approval request from rahadiyan.wisesa" — an approval request, explicitly
  relayed. Object exists. Attribution: the object belongs to
  `rahadiyan.wisesa`, the named source, not to `jomil.villareal`, who is only
  transmitting it — rung 1 of `decision_proposer`, which settles it before
  rung 2 is reached. `decision_proposer`: `@rahadiyan.wisesa`, and the
  proposing side has just that one member.
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
  `decision_approver`: rung 1 fails outright — Gate 3 found no closure
  signal — so extraction drops to rung 2. The thread names an awaited party
  twice: the original approval request at `jomil.villareal 3:18 PM` is
  addressed to `randy.tedjakusuma` / `@oncall-lead` directly, and
  `cui.ju 3:20 PM` additionally requires sign-off from "the respective eng
  PIC" — a role, not a name. That role is resolvable: `cui.ju 3:22 PM`
  routes the same review to `arpit.goel`, who then engages substantively on
  exactly the engineering-side concerns (merchant-group maintenance,
  governance, documentation freshness) an eng PIC would own, through to the
  end of the available source. Resolving the role to `arpit.goel` is an
  inference, not a stated fact, so it is flagged for the reviewer under
  Review Notes' `Inferred Values to Confirm`, same as `pst` below. This is
  independent of Gate 5's finding — `arpit.goel`'s standing came only from
  `cui.ju`'s unendorsed redirection, so his signal still could not have
  closed this candidate even if he had given one; who is awaited and who is
  entitled to close are separate questions. Value:
  `@randy.tedjakusuma / @oncall-lead (awaiting approval); eng-PIC sign-off
  also required, person not named in thread`. The role stays unresolved on
  purpose: `cui.ju 3:22 PM` names `@arpit.goel`, but read in sequence that
  message answers `jomil.villareal 3:21 PM` asking who to contact while
  `randy.tedjakusuma` is on leave — not the eng-PIC requirement two messages
  earlier. Nothing in the thread says `@arpit.goel` holds that role, and
  putting him in this field would send a reviewer chasing the wrong person.
  The eng-PIC gate and the
  unendorsed redirection also remain what `classification_reason` cites as
  the deciding gates — recording who is awaited does not remove either from
  that reasoning: "Approval requested in `jomil.villareal 3:18 PM`; eng-PIC
  gate set in `cui.ju 3:20 PM`; review redirected to `arpit.goel` by `cui.ju`
  at `3:22 PM`, unendorsed by the originally addressed `randy.tedjakusuma`;
  no signal from any entitled party through the end of the thread." Neither
  fact populates `conditions` — both are approval-process facts, not a
  condition on execution. That leaves `conditions` carrying only what is a
  genuine condition on future execution: the merchant group is a
  business-team priority list, reviewed against partnership needs and
  merchant performance rather than fixed (`@moch.zulfa`). **`conditions` is
  not empty for this candidate** — the two approval-process facts are
  excluded from it, not the field as a whole. `pst`: `FF Ecommerce` (inferred — the
  thread later calls this "this eComm decision" and ties the product to
  Fulfillment; flagged for reviewer confirmation).
- This candidate is finalizable exactly as drafted: every required field is
  present, `decision_approver` included — an awaited value, clearly marked
  as such, is a filled, honest value, not a gap — per Completeness above.

### D2 — documenting the pricing configs on the ExP variable

- **Gate 1:** `sengkeong.ho 8:55 AM` — "If it helps, can we set up an wiki
  page to document this for all markets?" — a proposal. Object exists, but
  **the wiki page is not it.** Both signals point the same way: the proposal
  states its own purpose ("to document this") and offers the page
  conditionally ("if it helps"), and the acceptance restates the commitment
  without it — `albert.lim 8:57 AM`, "part of solving that problem is to
  properly document the incoming new ones." Substitution confirms it: put
  the documentation somewhere other than a wiki and what was agreed still
  stands. The object is the commitment to document these configs, with the
  page recorded in `decision_details` as the agreed mechanism and executed
  as the Action.

  The thread itself demonstrates why this matters. The wiki page that
  actually got made came from `arpit.goel 11:23 PM` — a different person
  from the one asked, documenting the thread rather than the variable's
  configs. Framed as "`@rahadiyan.wisesa` creates a wiki page", the record
  reads as unfulfilled; framed as the commitment, that message is partial
  progress toward it.
  `decision_proposer` resolves on **rung 2**, not to the person who typed
  the proposal: the same message opens "Can I understand the concern about
  documentation further?", which makes it explicitly responsive to the
  documentation gap `arpit.goel` stated the day before (`5:29 PM`,
  `6:18 PM`). `albert.lim 8:57 AM` voices the same need again, but a later
  restatement does not transfer it. So `decision_proposer`:
  `@arpit.goel (raised the need; proposed by @sengkeong.ho)`, and the
  **proposing side** is `arpit.goel` + `sengkeong.ho`.
- **Gate 2:** `sengkeong.ho 8:59 AM` — "rahadiyan.wisesa lets set up a wiki
  page for this variable and document all the configs here? and then find a
  way to link this variable to this wiki so this becomes the central source
  of truth" — narrows the object from "all markets" to the single variable,
  and adds the linking requirement. Final scope is the narrowed one.

  The linking clause splits across two fields, and the split is on the
  substitution test again. The committed property — the documentation is
  reachable from the config, making it the source of truth — survives any
  change of tool and belongs in `decision_details`. "Find a way to" is
  unresolved work with no mechanism chosen, so it is part of the Action.

  Note also that `albert.lim`'s acceptance at `8:57 AM` speaks of "the
  incoming new ones" — all new pricing configs, wider than the single
  variable this narrows to. Rule 5.1 carries the acceptance forward to the
  narrower scope; the gap between the two is what that rule's Review Notes
  entry exists to surface.
- **Gate 3:** `albert.lim 8:57 AM` — "sengkeong.ho ya that helps" — explicit
  acceptance. The thread names no specific approver for this proposal, so
  under Rule 3.2 a disposition from any participant outside the proposing
  side can close it. `albert.lim` is neither `arpit.goel` nor
  `sengkeong.ho`, so he qualifies. Valid, unambiguous form.

  This is where rung 2's "whoever stated it first" tiebreak earns its
  keep. `albert.lim` restates the same documentation need at `8:57 AM`; had
  the restatement carried the need to him, he would be on the proposing
  side, his own "ya that helps" would fall to Rule 3.3, and D2 would close
  as `uncertain` with no approver — from a thread that plainly settled the
  question. The need stays with `arpit.goel`, who stated it first and never
  responded to the proposal, and the acceptance stands.
- **Gate 5 (scope fit):** the narrowing at `8:59 AM` comes from
  `sengkeong.ho`, who voiced the object and is therefore on the proposing
  side, and happens after `albert.lim`'s acceptance at `8:57 AM`. A
  narrowing from that side after acceptance does not reopen the candidate,
  so the acceptance carries forward to the narrowed scope. Note that Rule
  5.1 has to be read against the side here: `sengkeong.ho` is not the name
  in `decision_proposer`.
- **Result:** `decision`, `decision_status: approved`,
  `evidence_type: explicitly_stated`. `decision_approver`: `@albert.lim`.
- **`rationale` — three strands, not two.** The governance gap that
  motivated the proposal is the first of them and is the one a run of this
  thread has actually dropped: legacy configs carry no approvals,
  documentation, or freshness check, so mistakes go undetected and nobody
  can later reconstruct which merchants belong in a group or how they were
  derived (`@arpit.goel`). Then the two strands from the proposal forward:
  handling mex-specific pricing configs on ExP is established practice, so
  what is missing is documentation rather than the mechanism
  (`@sengkeong.ho`); and the team cannot today remove or trace configs ops
  set up long ago, which is what documenting new ones prevents
  (`@albert.lim`).

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

  That same message order is what rung 2 of `decision_proposer` now reads
  deliberately rather than incidentally: `arpit.goel` raised the need, so
  the decision is attributed to him; `albert.lim` restated it and then
  accepted, so he closes it. One reading of the thread, two fields.

- **Action (attaches to D2):** `sengkeong.ho 8:59 AM` asks
  `@rahadiyan.wisesa` to set up the wiki page, document the configs there,
  and link the variable to it. **One Action, not two** — the same person is
  asked, in one message, to stand up a page and wire it to the config; they
  are steps of a single piece of work, and splitting them would put an
  artificial handoff in the record. `rahadiyan.wisesa` does not speak again
  in the available source. `action_owner`: "@rahadiyan.wisesa (requested,
  not yet acknowledged)". No date given; none guessed.

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
