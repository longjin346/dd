# TODO

A working list for whoever maintains this skill. **The skill does not read
this file** — `SKILL.md`'s routing table does not point at it, and nothing
here is a rule. It is here so that findings stop living only in merged pull
request descriptions, where they sink out of sight.

## Glossary terms to confirm

`references/glossary.md` holds ten confirmed terms. These appear in captured
threads with no confirmed meaning, so the skill currently leaves them exactly
as written — which is correct behaviour, not a bug. Confirm one with someone
who uses it and it can be added.

| Term | Where it showed up |
|---|---|
| `FR` | "balancing FR during crunch", "poorer FR", FR capacity discussions |
| `ZFF` | "use mex ZFF" |
| `EAR` | "correct for dax EAR" |
| `LO` | "if it's an LO it won't be batchable" |
| `grabx` | "no governance on the grabx group" |
| `DMS-Go+` | "combining both levers under DMS-Go+" |
| `FF` | the `FF Ecommerce` PST value |
| `Saver` | a Mart service tier |

Do not fill these in from a plausible guess. A wrong entry is trusted by
everything downstream — that is the whole reason the glossary exists, after
a run read `MEX` as Mexico.

## The eval set

**One thread, and it is the wrong one to test on.** `examples/saver-discount-thread.md`
is worked through gate by gate in `references/extraction.md`, so any run that
loads the rules has already been shown its answers. It is the teaching
example and the regression fixture; it cannot measure judgment.

**The nearest step is not a new thread.** `examples/saver-discount-expected.md`
now carries seven readings awaiting the thread's owner — the judgment calls
the rest of the file rests on. Answered, that file stops being one reader's
derivation and becomes a gold set for this thread, which is what makes a
clean diff mean anything. Until then a clean diff says behaviour has not
changed, never that it is right.

New threads are still needed, but for a different job: the seven answers make
*this* thread's standard trustworthy, and only an unseen thread measures
whether the rules generalise.

What is needed:

- **Real threads, three to five.** Picked by recency or at random from
  channels where the bot would actually be used — not picked for the rules
  they would exercise, which reintroduces the same problem.
- **At least one thread that settles nothing.** Every eval thread so far
  contains decisions, so Gate 1 has never been tested on the failure mode
  that matters most: inventing a decision that was never made.
- **Baselines reviewed by a person**, not written by the same process that
  produces the output. The existing baseline was drafted unilaterally and
  contradicted itself on D1's approver in three places before that was
  caught.

## `sources.md` offers the user something they cannot do

The truncation rule says to ask "whether to continue with the truncated read
or **split the thread and retry**". A person cannot split a Slack thread, so
the second half of that offer is not actionable by whoever is reading the
message.

The template written for it offers continue-or-stop and deliberately does
not invent a retry mechanism. Someone who knows the Slack tooling should
decide what the real second option is — anchoring the fetch at a later
message so the window starts further down might work, but that was not
verified and so was not promised. Until then the rule and the template
disagree by one option, on purpose.

## Publishing the same record twice

Two ways in, one cause. **Nothing in the skill records that a Decision was
written.** `references/review.md` §1 defines exactly four state variables
and none of them is about publication, and gate 3 — the only mechanism for
keeping a candidate out of a write — only reaches candidates that cannot be
published as they stand. An already-committed `approved` candidate has no
exit.

- **Inside one conversation.** Save D2, leave D1 out, then come back and
  name D1's approver. That is an edit, so review reopens, and §6's test
  ("has any batch been applied since the set was last shown whole?") makes
  the save message render the full set — D1 *and* D2. Nothing marks D2 as
  written, `Before saving` is empty because both are approved, and the write
  commits D2 a second time. Every message on this path has a template and
  every gate passes.
- **Across conversations.** The save message and the publication result both
  promise that what was left out is "still here... later". **Here is the
  conversation**; there is no store. A day later the whole pipeline re-runs
  from Acquire, re-extracts D1 and D2, and cannot tell that half its output
  is already in the Bank — the skill has no read path to it.

Cheap fix for the first, which would also make a deliberate re-save
possible: a fifth state variable holding the Decision IDs the publisher
confirmed, with their record URLs; gate 5 writes only IDs not in it, and
gate 3 lists the committed ones as *already saved — re-save to create an
updated record, or leave as is.* The second needs the Bank read during
acquisition, which is a different repository's problem.

Until either exists, the honest advice to a reviewer is: do not leave a
decision out planning to come back for it.

## Rule changes the owner's corrections imply

Collected as the baseline review proceeds, **not yet applied** — the review
is still open and each of these moves a rule that decides more than one
thing. Each is a case where the run followed the rule and the rule was
wrong.

- ~~**`pst` is what the decision acts on, not where the conversation sits.**~~
  **Applied in 4.2.0.** The rule now leads with that sentence, carries the
  eComm phrase as a worked *negative* with a table separating what each
  quotable phrase actually describes, and D1's worked example reads
  `Pax Pricing` instead of teaching the wrong answer.
- ~~**A decision about another decision inherits its PST.**~~
  **Applied in 4.2.0**, stated in the `pst` rule and exhibited on D2, which
  now carries `Pax Pricing` and says why.
- **Read the named person's conduct, not only the naming message.** The
  rung-2 passage tells a reader to check what question a naming message was
  answering, and illustrates it with *"who is covering for an absent
  addressee"* — which is precisely the case where the name is right, since
  the person covering held the role. Its fallback, *leave the role
  unresolved when the sequence is ambiguous*, produced a worse record than
  naming him. What settled it was that he then probed the request like
  someone exercising a gate. The rule inspects the naming message's
  neighbours and never looks at what the named person does next.
- ~~**`Saver` belongs in the glossary.**~~ **Added in 4.2.0**, confirmed by
  the thread owner during the baseline review.
- **Nothing to fix in the overlap check.** It flagged the right pair, on two
  Decisions that never appear together, and the owner's answer was that they
  are the same work. The 3.5.0 feature did its job on its first real test.

## From the first run on a corrected fixture

Three findings, kept apart because they need different things.

**`presentation.yaml` is never opened.** The 3.6.0 display switch shipped and
no run has touched the file. The run that was asked to list every file it
opened named seven, and that was not among them. Nothing in the flow makes a
run look for it: `rendering.md` says to read it when rendering Review Notes,
and that instruction sits inside the section a run reaches after it has
already decided what to render. Until this is settled the switch is
decorative — a reviewer who sets it will see no effect and have no way to
tell.

~~**Permalinks are built wrong.**~~ **Fixed in 4.1.0.**
`references/extraction.md` now states where a Slack address comes from:
copy the one the source gave byte for byte, or build it by a worked formula
— `p` plus the `ts` with its dot removed — and where neither is possible,
cite author + time and omit the link. **Not verified against live Slack
tooling**, which may return per-message permalinks and make the construction
branch unnecessary; the rule covers both cases so that answer does not block
anything.

**D2's classification is not stable.** Two runs on the old fixture and the
first on the export all closed D2 as `approved` on `albert.lim`'s "ya that
helps". The run on the corrected fixture called it `pending`, missed that
closure signal entirely, put `decision_proposer` on rung 3, and named the
person who raised the need as the awaited approver — which Rule 3.3 exists
to prevent. **It got worse as the input got cleaner**, which no theory here
explains. This needs repeated runs under identical conditions before any
rule is touched: if it fails repeatedly the rules are wrong, and if it
alternates the judgment was never stable and the earlier passes were luck.

## From the interaction run

The first run taken past Present: twelve reviewer turns through Correct,
Finalize and Publish. **The state machine held throughout** — twelve edit
batches, two locks, one post-finalize reopen, one post-publication reopen,
and all four review variables correct at every step. What follows is what
did not hold.

**The publisher was invented, and the reviewer was told the save
succeeded.** Asked to save, the run evaluated all five publication gates
correctly, then — with no whitelisted publisher and no
`GITLAB_PAT_DECISIONBANK` anywhere in reach — used the generic file-write
tool to create a `decisions-bank.json` in a scratch directory, observed that
write succeed, and posted `✓ Saved to the Decision Bank.` It never lied
about a tool result; it substituted a target. The standing rule in
`SKILL.md` names the publisher as the only permitted channel and says
nothing about what to do when that channel is absent, so the run filled the
gap itself. Every guard held and the outcome was still a reviewer told their
decision is banked while it sits in a temp file nobody will read. **No gate
can catch this** — it happens after all five have passed — and nothing in
the conversation lets a reviewer detect it. What is missing is a rule for
the absent-publisher case, not a sixth gate. Highest severity found so far:
silent data loss under a green checkmark.

**The blank Decision template does not match its own exhibit.**
`rendering.md:628` gives the card verbatim, and the run rewrote it four
ways: the title placeholder `? - need to fill` became a bare `?`, the `(*)`
marker was dropped, the backticked card-header form became `▸ **bold**`
(and `▸` is the *section* glyph, used for Read Me and Review Notes), and the
`refs` row was omitted. The effect is that the title stops reading as a
field at all — a heading with a shrug in it, above six rows that do read as
a form — so the reviewer has no way to fill it. The run's own next message
then had to list `decision_title(*)` as missing, from a template that never
offered a row for it.

**A receipt printed the schema's field description as the old value.**
Clearing `D1 rationale` was reported as
`D1 rationale: <two to four sentences of reasoning> → ? - need to fill`.
The left side is the template's description of the field, not the paragraph
that was destroyed. A receipt exists to show what was lost; this one showed
a definition. An earlier turn got it right (`FF Ecommerce → Pax Pricing`),
so the rule is reachable — something about a field being *emptied* routes
around it.

**Two refusals went out as silence.** A finalize attempt on an incomplete
set re-sent the missing-fields block with no line saying the lock was
refused; a vague acknowledgement (`nice, thanks 🙏`) produced no message at
all. Both decisions were correct — nothing was locked, nothing was written,
no variable moved. But from the reviewer's side a declined instruction is
indistinguishable from being ignored, and the natural next move is to type
the same command again, harder. Refusing correctly and saying so are two
different requirements, and only the first is specified.

**A relative date was resolved to a calendar date and stated as given.**
`by end of next week` became `2026-09-25` in the receipt, with nothing
marking it as computed. Compare `pst`, which is inferred and surfaced under
`Inferred Values to Confirm`. Same class of move, different treatment, and
the reviewer sees a specific date they never typed.

**The missing-fields prompt asks a manually-added Decision to justify
itself from the thread.** For a reviewer-typed `D3`, the prompt read
`rationale(*) — Why was this decision made, based on what the thread
showed?` The wording is right for an extracted candidate and wrong for a
typed one, and the form has no idea which kind it is holding.

**A Decision the reviewer typed is indistinguishable from one the skill
extracted.** `D3` sits beside `D1` and `D2`, passes the same gates, and
would land in the Bank with nothing recording that it was never in the
thread. `refs` is the only possible tell, and the blank template omits that
row — see above.

### What held, so it is not re-tested

Paste-back diffed correctly against the held version, including an edit
nested inside an Action, with no phantom changes reported on untouched
fields and no display scaffolding written in as a value. `? - need to fill`
pasted back unchanged was read as still-empty rather than stored. A partial
card carrying `arpit` and `pricing config` produced no guessed `pst`,
proposer or approver. A one-shot natural-language Action add resolved its
parent Decision, took a fresh identifier rather than reusing a dropped one,
and resolved a bare first name to a handle. A vague acknowledgement did not
satisfy the explicit-save gate.

## Known gaps, roughly by cost of being wrong

- **A published record carries no provenance for its own edits.** A
  reviewer-corrected `decision_approver` inherits the credibility of `refs`
  that support the extracted value, not the typed one. Considered and
  deliberately not addressed — the thread carries every receipt and the
  preview shows the whole record — but worth revisiting if the Bank is ever
  read by people who were not in the thread.
- **Non-overwriting writes have no supersession story.** Publishing the same
  decision twice after an edit leaves two records with two `record_url`s and
  nothing saying which is current. May be the publisher's concern; that repo
  is not here, so the behaviour is unknown rather than wrong. What is *not*
  the publisher's concern is the skill sending the same record twice in the
  first place — see above.
- **A second, plainer source-selection re-ask has no template.**
  `sources.md` allows exactly one ("ask once more, more plainly"), and the
  message index in `rendering.md` has no row for it, since its trigger is
  not the trigger the source-selection prompt row describes. Small, but it
  is the fourth message found by reading that table backwards.
- **`SOUL.md` and `SKILL.md` disagree on the principal.** "Long Jin's
  Decision Memory agent" and "the admitted user" against "anyone in the
  channel can trigger it, not just the bank owner". Decide which is true;
  it determines whether identity matters anywhere in the flow.
- **A non-person approver has no rendered example.** A declared no-objection
  forum is written as a plain name with no `@`. Stated in one clause,
  demonstrated nowhere — the same shape as two rules that runs got wrong
  until an example was added. Rare enough to leave alone for now.
- **The baseline's design-history section runs 585 words** and could compress
  to about 80 without losing the guardrail it exists for. It already hid one
  stale contradiction for a full round of fixes.

## Things learned worth not relearning

- **Two correct rules in two files do not meet on their own.** Five runs
  got the same reply declining every source; all of them set the bundle
  `complete`, correctly and for the right reason; two then rendered a
  `Source Limitations` entry anyway. Neither file was wrong — `sources.md`
  said `none` is `complete`, `rendering.md` said what an entry looks like —
  and nothing said the second depends on the first. A run holding both
  facts has no rule that makes it use them together, and the result is a
  coin flip. When a defect reproduces about half the time, look for the
  missing link between two files rather than for a wrong rule in one.
- **An exhibit beats prose, and beats a prompt-level instruction.** Three
  runs fabricated a URL for a source that had none, twice after the rule
  forbidding it was written and once after being told not to in the prompt
  itself. Changing the *example* so one entry rendered without a link fixed
  it on the next run. When a rule is not taking, check whether the example
  beside it demonstrates the other branch.
- **Answers in the teaching material hide real gaps.** Runs looked accurate
  while copying values out of `rendering.md`'s exhibits. Replacing those with
  placeholders made the output look worse and made it honest — that is the
  run that surfaced the Mexico error.
- **An exhibit stops working where a formatting habit is stronger.** The
  blank Decision card is given verbatim in `rendering.md`, and a run
  followed the six field rows beneath it exactly while rewriting its header
  four ways — placeholder, marker, glyph, and a dropped row. Exhibits carry
  list-shaped content reliably; a lone heading line sitting next to a
  familiar convention is where one gets overridden. First counter-example
  to the rule above, and the reason it is stated as a limit rather than a
  law.
- **A run's self-report is evidence, not a finding.** One reported three
  gaps; two did not exist and would have led to "fixing" things that were
  already correct. Verify each against the file before acting.
