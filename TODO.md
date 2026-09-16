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

**One thread, and it is the wrong one to test on.** `examples/saver-discount-thread.txt`
is worked through gate by gate in `references/extraction.md`, so any run that
loads the rules has already been shown its answers. It is the teaching
example and the regression fixture; it cannot measure judgment.

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

## Two messages with no template

`references/rendering.md` opens with a table of every user-facing message and
who decides when it is sent. Building that table found three that
`references/sources.md` requires and nobody had written. One is now written —
the truncation confirmation. Two remain, both marked `none yet` in that
table so the gap is visible where someone would go looking for the words:

- **Single-thread offer.** A request to sweep a whole channel is refused,
  with an offer to run the single-thread version instead. A refusal plus an
  offer is exactly where wording matters.
- **Target question.** Invoked with nothing to point at, the run asks which
  thread to read.

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

## Known gaps, roughly by cost of being wrong

- **A truncated URL has no rule.** The rules cover "no address at all"
  (render a plain label) but not "an address that is visibly incomplete" —
  a link with an elided path segment, a missing scheme, a half-pasted URL.
  The second case is worse: it looks real and fails on click. Seen in the
  reference thread, where both source links carry an elided path.
- **`Source Limitations` rendered when the user declined every source.**
  A run produced an entry after the user answered "just the thread", which
  the rules treat as `none` — and `none` is a `complete` bundle with nothing
  missing that anyone wanted. Possibly introduced by the "choice never
  settled" rule added for the no-answer path; worth diffing that change.
- **Nothing checks Actions against each other.** In the reference thread,
  `A1` (a Confluence page already created) and `A3` (a wiki page someone was
  asked to create) may be the same artifact or two competing ones, and the
  skill has no way to notice.
- **A published record carries no provenance for its own edits.** A
  reviewer-corrected `decision_approver` inherits the credibility of `refs`
  that support the extracted value, not the typed one. Considered and
  deliberately not addressed — the thread carries every receipt and the
  preview shows the whole record — but worth revisiting if the Bank is ever
  read by people who were not in the thread.
- **Non-overwriting writes have no supersession story.** Publishing the same
  decision twice after an edit leaves two records with two `record_url`s and
  nothing saying which is current. May be the publisher's concern; that repo
  is not here, so the behaviour is unknown rather than wrong.
- **"Finalize and save" in one reply renders the full set twice.** §6
  removed that echo on the finalize side but does not cover the combined
  reply, so the finalize prompt and publication preview render the same set
  back to back.
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
