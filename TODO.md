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

- **`pst` is what the decision acts on, not where the conversation sits.**
  `extraction.md`'s rule offers *"a decision the thread explicitly calls
  'this eComm decision'"* as its worked example of a sound inference. That
  is the exact inference that produced the wrong value: a Saver discount is
  a discount on pax pricing, and "this eComm decision" describes the
  surrounding conversation. Replace the example with this case as a worked
  negative, and state the distinction the owner drew.
- **Read the named person's conduct, not only the naming message.** The
  rung-2 passage tells a reader to check what question a naming message was
  answering, and illustrates it with *"who is covering for an absent
  addressee"* — which is precisely the case where the name is right, since
  the person covering held the role. Its fallback, *leave the role
  unresolved when the sequence is ambiguous*, produced a worse record than
  naming him. What settled it was that he then probed the request like
  someone exercising a gate. The rule inspects the naming message's
  neighbours and never looks at what the named person does next.
- **`Saver` belongs in the glossary.** Reaching the right `pst` depends on
  knowing a Saver discount is a discount on pax pricing, and the skill has
  no way to know it. Sits in the unconfirmed list above.
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

**Permalinks are built wrong.** A run rendered
`.../archives/C04KSAY0K/p1787642328.064969`. The real form has no dot —
`p1787642328064969` — and the export's own header shows it. The run took the
`ts` field and prefixed `p` rather than using the address it was given. Same
family as the URL problems: an address that looks right and fails on click.
Nothing tells a run how a permalink is constructed, and it should not be
constructing one at all when the source supplies it.

**D2's classification is not stable.** Two runs on the old fixture and the
first on the export all closed D2 as `approved` on `albert.lim`'s "ya that
helps". The run on the corrected fixture called it `pending`, missed that
closure signal entirely, put `decision_proposer` on rung 3, and named the
person who raised the need as the awaited approver — which Rule 3.3 exists
to prevent. **It got worse as the input got cleaner**, which no theory here
explains. This needs repeated runs under identical conditions before any
rule is touched: if it fails repeatedly the rules are wrong, and if it
alternates the judgment was never stable and the earlier passes were luck.

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
- **A run's self-report is evidence, not a finding.** One reported three
  gaps; two did not exist and would have led to "fixing" things that were
  already correct. Verify each against the file before acting.
