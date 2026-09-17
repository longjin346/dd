# Rendering — the presentation layer

This file governs one thing: what every user-facing piece of text this skill
sends looks like, character by character, and the formatting rules that make
it survive the Hermes Slack Gateway. It does not decide what a Decision is,
when a candidate is `uncertain`, what fields exist, or when a receipt versus
a full render versus a finalize prompt is due — those are judgment and timing
calls owned by `references/extraction.md` and `references/review.md`
respectively. Where this file needs to explain *why* an artifact exists, it
names the owning file instead of restating the rule.

**There is no script.** A language model reads this file and follows it by
hand, for every card, every time. That is why almost everything below is
shown as a complete, ready-to-copy example rather than described in the
abstract — a rule that is only stated gets applied inconsistently; a rule
that is shown gets copied.

## Every user-facing message, and who decides when it is sent

This file owns the exact text of everything the skill sends. Another file
almost always owns *when* — `references/review.md` for the review and
publication steps, `references/sources.md` for acquisition,
`references/extraction.md` for what goes in a card. That division is
deliberate, and it is also where things fall through: a file can require a
message that was never written here, and nothing notices.

So this table is the join. Read it both ways — every row below needs a
template in this file, and every message another file requires needs a row.

| Message | Sent when | Timing owned by | Template |
|---|---|---|---|
| Opening line | Every invocation, opening whatever message goes out first | `SKILL.md` | The opening line |
| Single-thread offer | A request to sweep a channel, refused | `sources.md` | **none yet** |
| Target question | Invoked with nothing to point at | `sources.md` | **none yet** |
| Truncation confirmation | The fetch came back at the limit, before anything is extracted — carries the opening line above it | `sources.md` | The truncation confirmation |
| Source-selection prompt | After the fetch, only if the discovery pass found a source | `sources.md` | The source-selection prompt |
| Read Me | Once, heading the first card set | `SKILL.md` stage 3 | The required-field legend |
| Decision card | With the Read Me, on request, and in the save message | `review.md` §6 | The Decision card |
| References list | Only when asked for a candidate's refs | `review.md` §6 | References, on request |
| Review Notes | With the first card set; `Uncertain Decisions` alone in the save message | `review.md` §6 | Review Notes |
| Change receipt | After every edit batch, applied or not | `review.md` §6 | The change receipt |
| `Not applied` block | In that receipt, when an edit was refused outright | `review.md` §3.1–3.3 | The change receipt → What was not applied |
| Question block | In that receipt, when an edit needs an answer first | `review.md` §3.1–3.3 | The change receipt → What was not applied |
| Missing-fields prompt | Ends the response whenever a finalize-required field is unresolved | `review.md` §4 | The missing-fields prompt |
| Finalize prompt | Closing any reply whose batch left every required field filled | `review.md` §7 | The full current set, and the finalize prompt |
| Save message | On a finalize confirmation — cards, what cannot be saved, and the save request | `review.md` §6, §7 | The save message |
| Correction re-render | A gate-3 reply corrected a candidate rather than excluding it | `review.md` §8 gate 4 | The save message → After a correction at the gate |
| Publication result | Once the write returns, success or failure | `review.md` §9 | The publication result |

Four of these were added after a walk through the flow found the rule
requiring them and no text to send: the opening line, the `Not applied` and
question blocks, what is now the save message, and the publication result.
Each had
been specified somewhere as something the skill does, and each left the
model to invent the words.

**Two rows say `none yet`.** Building this table is what found them —
`sources.md` requires both and no text for either exists. Until one is
written, that row is a warning rather than a pointer: the message still has
to be sent, the rule for it lives in `sources.md`, and the words are yours.
The third of the three found that way, the truncation confirmation, is
written below, since it decides whether a run proceeds on a thread it
already knows is incomplete.

## Every fence in this file is an exhibit, not output

**Every value inside those exhibits is a placeholder.** Anything in angle
brackets — `<decision title>`, `<PST>`, `<one reason the thread gave>` — marks
a slot, not text to emit, and the people are `@alias`, `@second-alias`,
`@group-handle` rather than anyone real. What the exhibits demonstrate is
shape: which markers sit where, what wraps, what gets a blank line. A worked
thread and the values a run should actually produce from it live in
`examples/`, kept out of this file on purpose, so that reading the format
rules never doubles as reading the answers.

Every triple-backtick block below — including ones written as ` ```text ` —
exists so you can see the finished artifact. **None of them, including the
fence characters themselves, are ever emitted to Slack.** The Gateway forbids
language tags on code fences and this file uses `text` tags throughout purely
to stop this document's own renderer from trying to interpret the contents
as Markdown while you read it. When you construct the real message, copy the
content between the fences — the heading, the blank line, the bullets — and
send it as plain Markdown text with no fence around it at all. The one
exception is a genuine code block the skill itself is instructed elsewhere to
emit (a literal excerpt that must appear monospaced); even then it is a bare
triple-backtick fence with no language tag, never one carried over from this
file's own `text`-tagged exhibits.

## The Gateway contract, in one place

The skill sends standard Markdown; the Gateway converts it to Slack rich
blocks. It supports:

- `**bold**`, `*italic*`, inline code
- plain triple-backtick code blocks — no language tag
- `-` lists, with two-space indentation per nesting level
- ordered lists (`1.`, `2.`, …)
- `[label](URL)` links

It does **not** support, and none of these ever appear in output:

- Slack's own mrkdwn emphasis (single-asterisk-means-bold, underscore-means-italic) in place of standard Markdown
- angle-bracket link syntax (`<url|label>`) in place of `[label](url)`
- Markdown `#` headings
- tables
- HTML
- a language tag on a code fence
- raw Block Kit JSON

### The two structural glyphs — and what the glyph rule actually forbids

Two glyphs pass the Gateway unchanged and are reserved for exactly one job
each:

- `▸` opens a user-facing section heading and never appears mid-sentence —
  `▸ **Read Me**`, `▸ **Applied**`, `▸ **Ready to finalize?**`.
- `────────────────────────` is the separator between top-level presentation
  blocks (see placement rule below) and never appears anywhere else, at any
  other length, or built from a different character.

That is the entire glyph restriction. It is not a ban on punctuation. Em
dash (`—`), right arrow (`→`), and ellipsis (`…`) are ordinary Unicode text,
not decoration, and every template below uses them exactly where prose or a
compact record line would use them — a receipt line reads `pending →
approved`, an Action line separates its parts with `—`, a shortened value
ends in `…`. Do not treat any of these as restricted.

What genuinely is forbidden: any other box-drawing or ASCII-art divider
character (`═`, `━`, `│`, `┃`, a row of plain hyphens or equals signs built
to look like a rule — which also risks being read as a Markdown heading
underline or horizontal rule, a separate failure mode on top of the glyph
one) — use only the one approved separator, at its one approved length, for
that job.

## The one spacing rule — applies everywhere, no exceptions

The Gateway recognizes a `-` list only when it starts a fresh block. A list
item glued to the line above it, or carrying stray leading whitespace on a
top-level item, renders as literal paragraph text with a visible `-`
character instead of a bullet.

The rule that prevents this, stated once, applies to **every** template in
this file with no per-template variation:

> Whenever a list follows a line that is not itself a list item — a
> section heading, a card's inline-code title line, a sentence of prose —
> put exactly one blank line between that line and the first item. This
> covers ordered lists (`1.`, `2.`, …) exactly as it covers `-` lists; both
> are recognized only when they start a fresh block. A
> list item that continues the same list (the next field bullet in a card,
> the next entry in a Review Notes category) needs no blank line before it —
> only the transition from non-list text into a list does. Every top-level
> `-` item starts at column 0 with no leading spaces. Every first-level
> nested item starts with exactly two spaces then `-`.

Two templates in the pre-rewrite skill put their first bullet directly under
a heading with no blank line — that inconsistency does not survive here.
Every template below — Read Me, a Decision card, the change receipt, the
missing-fields prompt, Review Notes, the finalize prompt, the publication
preview — opens its list the same way: heading line, one blank line, then
`-` at column 0. The cost of the blank line when the Gateway would have
tolerated its absence is nothing; the cost of omitting it when the Gateway
needed it is a broken card. Given the uncertainty, always include it.

### Wrapped list items

A field value, condition, or Review Notes entry that runs past one line
still has to read as part of the same list item. The rule: **a wrapped
continuation line indents to where that item's own text begins — two spaces
past its own bullet dash.** A top-level item (`- text`) wraps its
continuation at column 2. A first-level nested item (`  - text`) wraps its
continuation at column 4. Never wrap at column 0 — that starts what the
Gateway reads as a new, un-bulleted paragraph, breaking the list.

```text
- **Uncertain Decisions**
  - `D1` — Why uncertain: <one plain sentence, grounded in the source,
    saying what stopped this from closing> (`alias 3:20 PM`).
    [View source](slack-permalink)
```

### Where the separator goes

Place the exact `────────────────────────` line: after Read Me and before
the first Decision card; before the Review Notes section, when one renders;
and before a finalize or save prompt only when that prompt directly follows
the Decision cards with nothing in between. When a Review Notes block sits
between the cards and the prompt, that block's own separator already divides
the message and no second one is added — see the full-set render below,
which carries exactly one separator. Never place it between two Decision
cards, before the very first block in a message, after the final block, or
between two Review Notes categories.

## The required-field legend

One marker says a field must be filled before this version can be locked for
review. `decision_approver` carries it like any other, but it reaches that
marker far less often than it once did: `references/extraction.md` fills it
by working down a fallback ladder — who approved it, failing that who is
supposed to, marked inline as `(awaiting approval)` rather than given — and
only when the thread establishes neither does the card show
`? - need to fill`.

That is deliberate. A value supplied on the reviewer's behalf without
marking that it was never actually given would read as answered and get
skipped, making a required field look optional. An awaited value avoids that
because the inline marker (below) keeps it from being misread as a
disposition. Only when the ladder finds nothing at all does the reviewer get
asked, and the prompt states plainly what is wanted. Asking someone to
confirm what the thread shows is fine; asking them to supply what it does
not is the bug this skill was rebuilt to remove, and the difference lives
entirely in how the question is worded.

| Marker | Meaning | Fields it appears on |
|---|---|---|
| `(*)` | Required to **finalize** — lock this version for review. | `decision_title`, `decision_details`, `pst`, `decision_proposer`, `rationale`, `decision_status`, `decision_approver` |
| *(no marker)* | Optional, permanently. Never blocks anything. | `conditions`, `refs`, every Action field |

State this once, in the Read Me block, so the distinction is visible before
the reviewer looks at a single card:

```text
▸ **Read Me**

- This is an AI-generated draft of Decision Candidates, each with its own attached Actions.
- Nothing is saved to the Decision Bank until you've reviewed this and asked me to save it.
- `(*)` fields must be filled before I can lock this version.
- Fill each `? - need to fill` before finalizing. Anything else marked `? - optional to fill` can stay as is.
- To update a Decision or Action, use either method:
  - **Natural language:** name the ID, the field, and the new value — "D1 decision_approver is @jane. Change A1 to 2026-09-11."
  - **Copy and edit:** copy the full card, edit its values, and paste it back.
- Missed something? Reply "add a decision" or "add an action" and I'll send a blank one to fill in.
- To remove one: "Drop D1" or "Drop A1."
- I keep replies short: after each change I report only what changed. Reply "show D1" or "show all" to see a full card again.
```

### Placeholder vocabulary

| Situation | Render as |
|---|---|
| `(*)` field, empty — including `decision_approver` when the thread establishes neither an approver nor an awaited party | `? - need to fill` |
| Optional scalar, empty | `? - optional to fill` |
| Optional array, empty, on a drafted or extracted card | `[]` |
| Optional array, empty, on a blank add-a-decision template only | `? - optional to fill` (fillable; normalizes to `[]` if left untouched) |
| A Decision list block with no members | `- None` (see empty-state rule below) |
| An Action with no named owner | `no owner` |
| An Action with no date | `no date` |

Never render a missing `(*)` value as `null`. Never require the user to fill
anything with no marker.

## The opening line

The first thing the skill ever sends, and the only message that goes out on
every single invocation — including one triggered by a bare @-mention with
no instruction. Someone who has never seen this bot before meets it here.

One line, the same one every time, so it stays recognizable:

```text
I'll read this thread and work out what was decided.
```

**"Work out," not "pull out."** The skill infers what was decided; it does
not lift a sentence that was already sitting there labelled as a decision.
A verb that promises transcription sets up a reader to be surprised by
Review Notes.

Actions are not mentioned here, deliberately. An Action is an attribute of
its Decision (`references/extraction.md`), and naming the two side by side
would teach a structure the cards immediately contradict. The Read Me's
first bullet already introduces the nesting, which is the right place for
it.

**It is never sent on its own account.** The line opens whichever message
the run sends first, and what that message is depends on what the fetch and
the discovery pass turned up. It cannot be sent before them: every form
below needs something only the fetch knows, and a bare "I'll read this
thread" followed moments later by a second message is two notifications
where the skill promised one (`SKILL.md`, *keep the thread quiet*).

- **The fetch came back at the limit** — the line, a blank line, then the
  truncation confirmation. This is the case that decides the rule: a
  truncation stop is the first thing a stranger would otherwise see, and it
  opens by saying the bot cannot do something before ever saying what it is.
  Discovery has not run yet at this point, so the source-selection prompt is
  not part of this message; it follows after the go-ahead, without the
  opening line, which has already been sent.
- **External sources found** — the line, a blank line, then the
  source-selection prompt below, all in one message.
- **Neither** — the line alone, with one added sentence so the silence that
  follows is expected:

  ```text
  I'll read this thread and work out what was decided. Back shortly with a draft for you to check.
  ```

  Nothing else goes out until the cards.

Never in this line: the Decision Bank, a PST, a schema field name, a gate, or
any stage name from this skill. Never narrate the step you are about to take
internally — "let me first check whether there are any external sources"
tells the reader nothing the prompt underneath it does not already show.
Never promise a time. Never add a third sentence.

## The truncation confirmation

`references/sources.md` fetches a thread in one call against a hard limit
with no pagination. When the number of messages returned equals the limit
requested, the thread is probably cut off — and the end of a thread is where
approvals and objections land, so what is missing is disproportionately the
part that decides things.

This is the first of the skill's two pauses and it is a real stop: the run
extracts nothing until an explicit go-ahead arrives.

It is also, on a truncated thread, the first message the run sends, so it
carries the opening line above it — otherwise a stranger's introduction to
this bot is a sentence about what it cannot do:

```text
I'll read this thread and work out what was decided.

▸ **This thread is longer than I can read in one go**

I read <number> messages, which is as many as I can fetch at once, so there may be more after that — and the end of a thread is usually where the approvals and objections land.

Reply "go ahead" and I'll work from what I have. Anything I produce will say it came from a partial read, so nobody later mistakes it for the whole thread. Without that, I'll stop here rather than guess at what I'm missing.
```

- **Give the number.** "Some messages may be missing" cannot be judged;
  `I read 200 messages` can — the reader knows their own thread and can tell
  at a glance whether that is most of it or half of it.
- **Say what continuing costs, in plain words.** Not `partial`, not
  `inaccessible`, not "the bundle" — those are internal states. What the
  reader needs to know is that the result will carry the limitation with it.
- **Only an explicit go-ahead continues.** Silence, a reaction, an unrelated
  message in the thread, and a reply about something else are all not a
  go-ahead. Do not ask twice; the question stands until it is answered.
- **Never send this and extract anyway.** The one thing this message must
  not become is a notice that the run is proceeding regardless.
- **Do not offer to split the thread and retry.** `sources.md` names that as
  the alternative, but a person cannot split a Slack thread, and this file
  does not invent a mechanism to make the offer true. The honest second
  option is stopping.

## The source-selection prompt

Sent once the discovery pass has found at least one external source, and
only then — carrying the opening line above it, unless a truncation
confirmation already carried it: `references/sources.md` discovers
what the thread links to without opening anything, and this prompt asks
which of those to read. With none found the question is skipped entirely and
no message goes out — the opening line's second form covers that case on its
own.

Number the sources in the order they appear in the thread, label each by
what Slack already reveals about it (unfurled title, Jira key, filename, or
URL host — never opened to get a better one), and link each to its own URL:

```text
▸ **Additional sources found in this thread**

1. [Link — <what the unfurl already shows>](URL)
2. Jira — <issue key and title, as unfurled>
3. [Confluence — <page title, as unfurled>](URL)

Reply with the ones you want me to read:

- `1, 3` — just those
- `all`
- `none`

I only open the sources you pick, and nothing linked inside them.
```

- The closing line is not decoration: the one-hop boundary is a real limit
  on what the user is authorizing, and stating it is how they know what
  they are agreeing to.
- **A source with no URL you can actually see renders as a plain label, with
  no link.** `(URL)` above is a placeholder for a real one the fetch
  supplied; when the unfurl carries a title but no resolvable address —
  a Jira card rendered as an attachment, a file preview, a truncated paste —
  write `2. Jira — <issue key and title>` and nothing more. Never
  invent an address, never guess at one from the host or the title, and
  never park explanatory text in the link target (`[label](URL not visible)`
  renders as a broken link, which is worse than no link at all). The user is
  being asked which sources to open; a fabricated address sends them
  somewhere that does not exist, and a source they cannot identify from its
  label they simply will not pick.
- A source linked from several messages is one numbered entry, not several.
- An ordinary permalink to another message in the same thread is not an
  external source and never appears in this list.

## The Decision card

One self-contained card per candidate. `candidate_id` and `decision_title`
live in the heading, never as a field bullet. Every other `record` field
appears exactly once, in this order: `decision_details`, `pst`, `rationale`,
`decision_status`, `decision_proposer`, `decision_approver`, `conditions`,
`refs`. Every person, wherever mentioned — a field that is itself a person
value (`decision_proposer`, `decision_approver`, an Action's owner) or a
person named inside a free-text field's own prose (`rationale`,
`decision_details`, `conditions`) — uses the Slack alias (`@long.jin`), never
a display name and never a bare handle; a non-person approver (a declared
no-objection forum) is shown by plain name with no `@`. A citation embedded
in a field's own text cites the person only, with no timestamp
(`references/extraction.md` owns why).

```text
`D1: <decision title> (*)`

- `decision_details(*)`: <what was decided and its final scope, in two to four sentences — the substance, the boundary, and the mechanism if one was agreed>
- `pst(*)`: <PST>
- `rationale(*)`: <one reason the thread gave> (@alias). <a second, different reason, from someone else> (@second-alias).
- `decision_status(*)(options:approved|rejected|pending)`: pending
- `decision_proposer(*)`: @alias
- `decision_approver(*)`: @alias / @group-handle (awaiting approval); <a further sign-off the thread required>, person not named in thread
- `conditions`: <a condition on future execution> (@alias).
- `refs`: 4 sources (reply "D1 refs" to view)
- **Actions**
  - A1 <a task already done, in the past tense> (completed within the thread) — @alias — no date
  - A2 <a task still to do> — @alias, @second-alias (requested, not yet acknowledged) — no date
```

### One sequence, no classification on the card

Render every Decision in a single sequence, in the order the thread raised
them. Never split them into separate confident and uncertain groups, never
sort by status, and never put a classification label in a card heading or
anywhere else on the card.

This is a deliberate choice, not an omission. A card that announces itself
as uncertain, or that sits under an "Uncertain" heading, has prejudged the
question the reviewer is there to answer — and it does so before they have
read the evidence. Uncertainty is explained exactly once, in the
`Uncertain Decisions` category of Review Notes, where it comes with the
source-grounded reason that makes it actionable. The card itself carries
`decision_status`, which is a fact about the thread, not a verdict on the
extraction.

Card mechanics, carried forward unchanged in substance from the Gateway
contract above and applied identically to every card:

- Heading, one blank line, then top-level `-` field bullets with no leading
  spaces, then one blank line before the next card. A glued or indented
  top-level field renders as literal `-` text instead of a bullet.
- Field labels are the exact JSON key in inline code, with `(*)` appended
  inside the code span where it applies — `` `decision_details(*)` ``, never
  a renamed label like "Decision".
- `decision_proposer` names the party whose need the decision serves, which
  is not always whoever typed the proposal
  (`references/extraction.md` owns which). When the thread splits those two
  roles, the value carries the voicer inline — `@alias (raised the need;
  proposed by @second-alias)` — one field, both people, no second field on
  the card. Render it as one value; never split it across two
  bullets, and never drop the parenthetical to shorten the card.
- `decision_status` always shows the full compact label
  `` `decision_status(*)(options:approved|rejected|pending)` `` followed by
  its plain-text value — never wrap `approved`/`rejected`/`pending` in code,
  never repeat the option list after the value.
- `refs` defaults to a one-line summary — `N sources (reply "Dx refs" to
  view)`, singular `source` for one — never the full list inline. A
  Candidate with zero references shows `refs`: `[]`, with no summary hint
  and no Review Notes mention.
- If a card would exceed a Slack size limit, shorten only link labels and
  reference excerpts, never a record value; if it still doesn't fit, say the
  record can't be rendered intact.

### Actions, nested inside their Decision's card

An Action is an attribute of its Decision, not a peer record, so it is a
compact line — never its own card, never a separate top-level section. When
a Decision has one or more Actions, one bold bullet closes its card (`-
**Actions**`, matching the same bold-bullet-with-nested-entries shape
Review Notes uses below — one proven-safe pattern, reused rather than
invented twice), with each Action as a nested line underneath:

```text
{ID} {task, in the tense extraction.md specifies} — {owner, or "no owner"} — {date, or "no date"}
```

- Separate the three parts with `—`, never `|` — a pipe reads as broken
  table syntax, and tables are forbidden.
- Keep the short label (`A1`, `A2`, …) so the reviewer can address it
  conversationally, exactly as they address a Decision by `D1`.
- Carry forward any inline annotation already baked into the owner value by
  extraction (`(requested, not yet acknowledged)`, `(completed within the
  thread)`) — the renderer displays it, it does not compose the wording.
- Multiple owners render as one comma list on that line — see A2 above.
- No Action field is ever required. A missing owner reads as `no owner`, a
  missing date as `no date` — plain, legible, and explicitly not phrased as
  `? - need to fill`, because nothing about it is a gap the reviewer is
  failing to close.
- Omit the whole `- **Actions**` bullet when a Decision has no Actions
  attached. There is no empty-Actions placeholder to render.

### Adding a Decision or Action from a blank template

`add a decision` gets the same card shape with every value blank — the
fields shown are exactly the required set plus the two permanently optional
ones. Unlike an extracted candidate, nothing populates `decision_approver`
on the reviewer's behalf here — they are filling in every field themselves,
so it is required the same as any other field: whoever actually approved
it, or, if nobody has yet, whoever it is awaiting, marked inline as
`(awaiting approval)`:

```text
`D{next}: ? - need to fill (*)`

- `decision_details(*)`: ? - need to fill
- `pst(*)`: ? - need to fill
- `rationale(*)`: ? - need to fill
- `decision_status(*)(options:approved|rejected|pending)`: ? - need to fill
- `decision_proposer(*)`: ? - need to fill
- `decision_approver(*)`: ? - need to fill
- `conditions`: ? - optional to fill
- `refs`: ? - optional to fill
```

`add an action` sends a single blank line, not a card, naming its parent
Decision as established at creation:

```text
A{next} ? - optional to fill (task) — ? - optional to fill (owner) — ? - optional to fill (date)
```

## References, on request

Hidden by default behind the card's summary line; shown in full only when
asked ("D1 refs"). Each reference is one bullet with one compact link:

```text
`D1` references

- [slack, "<excerpt>"](slack-permalink-1)
- [slack, "<excerpt>"](slack-permalink-2)
- [slack, "<excerpt>"](slack-permalink-3)
- [wiki, "<excerpt, cut before the URL the message pasted>…"](<the real URL, kept as the link target>)
```

Link text is `ref_type, "excerpt"` — and an excerpt is free text pulled
verbatim from the thread, so it can contain exactly the characters that
break a Markdown link: a closing bracket or parenthesis, or a URL — people
routinely paste one straight into the message text, which is the case the
fourth bullet above stands for. Sanitize before building the link, every
time:

1. Scan the excerpt for the first `]`, `)`, or a recognizable URL (a
   `http://`/`https://` run, or a bare domain-shaped fragment).
2. If found, cut the excerpt immediately before it and append `…`. That is
   the entire fix for the fourth bullet above: the label stops at the last
   word before the pasted URL, and the real URL still lives where it
   belongs, as the link's actual target.
3. If that cut would leave nothing usable (the offending character sits at
   or near the start), fall back to the source title or key instead — the
   same fallback already used when `excerpt` is null.

Never touch the URL inside `(…)` — only the visible label text is ever
sanitized. When `excerpt` is null, use the source title or key in its place,
per the same rule. Never show bare `ref`/`excerpt`/`ref_type` sub-bullets or
a naked URL.

## Review Notes

One `▸ **Review Notes**` section after all Decision cards, when it has
content. Each category renders as a bold top-level bullet with its entries
nested underneath, in this fixed order, and — replacing any config file —
the whole visibility rule is exactly this: **render a category when it has
at least one entry; omit a category with none; omit the entire section when
every category is empty.** Nothing else gates it.

```text
▸ **Review Notes**

- **Complete, but not a decision yet**
  - `D1` — the record is finished; the Bank only holds decisions that were
    actually made. Tell me who approved it, or it stays here and out of any
    save.
- **Inferred Values to Confirm**
  - `D1 pst`: <PST> — inferred from <what in the thread supports it>.
    Confirm or change.
- **Uncertain Decisions**
  - `D1` — Why uncertain: <one plain sentence saying what stopped this from
    closing> (`alias 3:20 PM`), <and, where it applies, that the review went
    to someone the thread never entitled>. [View source](slack-permalink)
- **Not Identified as Decisions**
  - <the topic, named briefly> — <why it is not a decision object>.
    [View source](slack-permalink)
  - <a topic covering two related discussions at once, where they failed for
    the same reason> — <why>. [View source](slack-permalink)
  - <a message about the capture process itself> — excluded by Gate 1's own
    carve-out.
  - <an automated or bot message, quoted> — no proposal content.
- **Source Limitations**
  - [Jira — ABC-123](URL) could not be read because access was denied.
```

- **Complete, but not a decision yet** carries one entry per candidate that
  cannot be published as it stands — `decision_status` not `approved`, or an
  approver still marked `(awaiting approval)`. It comes first because it is
  the only category that changes what a reviewer can do with the record, and
  it appears from the first card set onward rather than waiting for the save
  step. A reviewer who learns at the last gate that a candidate was never
  publishable has been told too late; it was knowable at extraction.

  Say it as a fact about the thread, never as a defect in the record. The
  record is complete — every required field is filled, including an approver
  honestly marked as awaited. What is missing is an approval that has not
  happened, and no amount of reviewing produces one.

  **A candidate usually appears here and under `Uncertain Decisions` both**,
  since whatever stopped it closing is usually also what leaves it
  unpublishable. Split the work rather than saying it twice: this category
  carries what the reviewer can do about it, `Uncertain Decisions` carries
  the evidence and the link. Neither restates the other's half. Two adjacent
  bullets that both explain that nobody approved `D1` teach the reviewer to
  skim the section.
- Never add a missing-fields category here — the inline `? - need to fill`
  markers and the Read Me block already say what's missing; repeating it
  would only duplicate and crowd out the notes that carry new information.
- List an inferred value only when the model actually filled it by
  inference — never a value taken from direct source evidence, and never a
  field that's simply unresolved (that's already `? - need to fill` on the
  card). A `decision_approver` that names an awaited party the thread
  stated, with a required role left open because nobody was named, is both
  of those and belongs in neither: the value came from the source, and the
  open role is what `Uncertain Decisions` already reports.
- Never expose a Gate id, an enum name, `evidence_type`, or chain-of-thought
  in a `Why uncertain` line — rewrite it as one plain, source-grounded
  sentence.
- Source Limitations, when present, is always last, one entry per unread or
  inaccessible selected source, stated once — never repeated per Candidate.
  A run where the source-selection choice was never settled
  (`references/sources.md`) contributes **one** entry covering all of them
  together, not one per link: the sources went unread because the question
  went unanswered, which is a single fact about the run. State it flatly —
  it is never a complaint that nobody replied.

## The change receipt

Follows every edit batch, always — whether it applied in whole, in part, or
not at all — and never a re-rendered card set. A batch where nothing could
be applied still gets a reply: the user said something, and silence is not
an answer to it.
Structural changes come first, in this fixed order — **add, drop, restore,
merge, move, confirm** — then field-level changes, each showing previous
→ new value verbatim (shorten a long *previous* value to a few words plus
`…`; never shorten the new value):

```text
▸ **Applied**

- Added `D5: <title>`
- Dropped `D3: <title>` and its linked Action `A4` — reply "Restore D3" to put it back
- Restored `D6: <title>` and its linked Action `A7`
- Merged `D4` into `D1`; kept `D1: <title>`
  - Combined the rationale and conditions from both
  - `D4 decision_details` was displaced by `D1`'s: "<first few words of the value that won>…"
- Moved `A2` from `D1` to `D5`
- Confirmed `D2` as a Decision; no field values changed
- `D5 pst`: ? - need to fill → <PST>
- `D1 decision_status`: pending → approved
```

That block shows every line shape at once, which no single batch would
produce — a real receipt carries only the lines its own edits earned, in
that order, and nothing else.

- Show a previous placeholder verbatim (`? - need to fill` or `? - optional
  to fill (required only if approved for publishing)`) so the user can tell
  a filled blank from an overwritten value.
- **A drop line carries the way back**, once, on the line itself — a drop is
  reversible (`references/review.md` §3.6) and the user has no reason to
  know that unless told at the moment it happens. Say it on the drop, not as
  a standing note anywhere else, and not on a restore.
- **A merge names what it displaced**, nested under the merge line: one line
  saying the accumulating fields were combined, and one line per non-empty
  value that lost out, with the winning text shortened to a few words plus
  `…`. A merge that silently overwrites text the user could read on screen
  one message earlier is the one structural operation that can lose content
  without anyone noticing.
- **A structural operation with no line here cannot be reported at all.**
  Adding one to `review.md` §3.6 or §3.7 means adding it to the order above
  and giving it a line shape. The receipt is the only channel an edit batch
  has — editing never renders the cards (`review.md` §6) — so an operation
  this list forgets happens silently.
- **A move names both ends.** `review.md` §3.7's `Link A1 to D2` changes
  which Decision an Action attaches to, and that attachment is positional —
  there is no parent field on the card, so a move cannot be reported as a
  field-level change and needs this structural line instead. Name where the
  Action came from as well as where it went: the reviewer is checking that
  it left the right Decision as much as that it arrived at the right one.
- Mention uncertainty only when this batch actually changed a candidate's
  uncertain state — one line saying it's now confident, or newly uncertain
  with its `Why uncertain` sentence. Don't resend the whole category for no
  reason.
- Whether a given response carries a receipt, a single card, or the full set
  is decided by `references/review.md` §6, never here. When it calls for a
  single card, render that card in the Decision card format above. Never
  render the same card twice in one message.

### What was not applied

`references/review.md` requires several edits to be refused or held, and
they need somewhere to go. Two blocks cover it, and a reply carries each one
only when it has content:

**The `Not applied` block** — edits refused outright, where there is nothing
to ask. One line each, naming what was skipped and why, in plain language:

```text
▸ **Not applied**

- `D7` — no Decision with that ID. Current IDs: D1, D2, D5.
```

An ID can be missing because it was dropped or merged earlier in this
review, so say what exists rather than implying a typo. Nothing here changes
`review_revision`, completeness, or either finalize/publication flag — no
record moved.

**The question block — at most one per reply** — every edit the batch could
not resolve without an answer, gathered under a single heading rather than
asked one message at a time:

```text
▸ **Before I apply the rest**

- `D2 pst`: "<what the user typed>" isn't one of the PSTs. Reply with a number:
  1. DCA
  2. Dispatch
  <… every remaining active PST, in `psts.json` order …>
- The pasted `D1` card is missing the second half of `decision_details`
  ("<the text that went missing>"). Drop it, or keep it?
```

**An invalid `pst` gets the list, never a guess.** `review.md` §3.2 forbids
fuzzy-matching a typo and §3.5 forbids selecting the closest-looking value,
so "did you mean X?" is not available here even as a question — it puts one
candidate in front of the user on a resemblance the rules say not to
compute, and a wrong guess that reads as helpful is the one they are most
likely to accept. The numbered list costs more lines and asks nothing the
user has to overrule. The full list is written out once, under the
missing-fields prompt below; render every active value here too, elided
above only so this file carries one copy of `psts.json` rather than two.

`review.md` tells each of its ambiguity paths to "ask one concise
clarification question" — target omitted with several candidates,
normalization landing on no single value, a pasted card that cannot be
matched, a pasted diff exposing a probably-unintended change. Several of
those can fire in one batch. They are gathered here, one bullet each, not
split across several messages: one batch in, one batch out, and the user
answers everything in a single reply.

**Order within the reply is fixed:** `Applied`, then `Not applied`, then the
question block. Result first, then what was skipped, and last the only thing
that needs the reader to do something. A reply never carries two question
blocks, and never asks a question that belongs in `Not applied` — a
refusal is not a choice being offered.

## The missing-fields prompt

Ends the response instead of a finalize prompt — never both in the same
message — whenever a finalize-required field is still unresolved on any
current Decision. Actions are never checked; they have no required field at
either tier.

A candidate extracted from a thread that named a PST, an approver and a
rationale reaches finalize with nothing outstanding, so this prompt never
fires for it. The example below therefore shows the shape using a Decision
added from a blank template, which is the common case for an unresolved
`pst`:

```text
▸ **Still needed before finalizing**

- `D5 pst(*)` — Which PST does this belong to?
  1. DCA
  2. Dispatch
  3. FFI
  4. ITE
  5. Pax Pricing
  6. Earnings
  7. DQO
  8. Supply Planning
  9. Dax App Core
  10. MLE
  11. Data Engineering
  12. PRT
  13. Test Automation
  14. Scaled Ops
  15. PA
  16. FF Ecommerce
  17. TPM

Please provide all known values in one reply. Anything else you want to change? Reply "show all" at any time to see every card.
```

- List every missing `(*)` field once, grouped in Decision order, ID plus
  exact field key plus one short plain-language question.
- **The `decision_approver` question states plainly what is wanted.** It
  reaches this prompt only when extraction's fallback ladder
  (`references/extraction.md`) found neither an approver nor an awaited
  party in the thread — the reviewer is being asked to supply real
  knowledge the transcript didn't capture, the same as `pst`,
  `decision_proposer`, and `rationale` already are, never to invent a
  person:
  `` - `D5 decision_approver(*)` — Who approved this? If nobody has yet, who
  is it waiting on? `` In practice this rarely fires for an extracted
  candidate — rung 2 of the ladder already fills the field with an awaited
  party whenever the thread names one — so it is the common case only for a
  Decision added from a blank template, where the reviewer is filling every
  field themselves.
- Never ask for `conditions`, `refs`, an Action field, or any other
  unmarked field.
- A missing `pst` always gets the numbered list, in `psts.json`'s configured
  order, so a bare number reply resolves against it.
- **The list above is a copy, and `psts.json` is the original.** It is
  written out once in this file so the shape is unambiguous — bare numbers,
  no codes, no descriptions — but nothing keeps the two in sync. Read the
  active values from `psts.json` at render time and use those; if they
  disagree with the exhibit, the exhibit is out of date, not the config.

## The full current set, and the finalize prompt

The finalize prompt closes any reply whose edit batch left every
finalize-required field filled — a receipt and this prompt, nothing else.
Editing never renders the cards (`references/review.md` §6); the reviewer
reads deltas while they work.

The full set below is what the **save message** renders once the reviewer
confirms. It is kept here, with the finalize prompt, because the two share a
shape: every current Decision card in this format, nested Actions included,
then — only when at least one Decision is still uncertain — one separator and
the `▸ **Review Notes**` heading carrying the `Uncertain Decisions` category
alone. What differs is the closing block, and the save message supplies its
own:

```text
▸ **Decision Candidates**

`D1: <decision title> (*)`

- `decision_details(*)`: <what was decided and its final scope, in two to four sentences — the substance, the boundary, and the mechanism if one was agreed>
- `pst(*)`: <PST>
- `rationale(*)`: <one reason the thread gave> (@alias). <a second, different reason, from someone else> (@second-alias).
- `decision_status(*)(options:approved|rejected|pending)`: pending
- `decision_proposer(*)`: @alias
- `decision_approver(*)`: @alias / @group-handle (awaiting approval); <a further sign-off the thread required>, person not named in thread
- `conditions`: <a condition on future execution> (@alias).
- `refs`: 4 sources (reply "D1 refs" to view)
- **Actions**
  - A1 <a task already done, in the past tense> (completed within the thread) — @alias — no date
  - A2 <a task still to do> — @alias, @second-alias (requested, not yet acknowledged) — no date

`D2: <decision title> (*)`

- `decision_details(*)`: <what was decided and its final scope — where an instrument was agreed, it appears here as the mechanism, never in the title>
- `pst(*)`: <PST>
- `rationale(*)`: <the need this decision answers, from whoever raised it> (@alias). <a second reason> (@second-alias). <a third> (@third-alias).
- `decision_status(*)(options:approved|rejected|pending)`: approved
- `decision_proposer(*)`: @alias (raised the need; proposed by @second-alias)
- `decision_approver(*)`: @third-alias
- `conditions`: ? - optional to fill
- `refs`: []
- **Actions**
  - A3 <a task still to do> — @alias (requested, not yet acknowledged) — no date
  - A4 <a task nobody was assigned> — no owner — no date

────────────────────────

▸ **Review Notes**

- **Uncertain Decisions**
  - `D1` — Why uncertain: <one plain sentence, grounded in the source,
    saying what stopped this from closing> (`alias 3:20 PM`).
    [View source](slack-permalink)

▸ **Ready to finalize?**
Look right? Reply "Yes, finalize" to lock this version, or send any remaining changes.
```

- A re-render never repeats `Inferred Values to Confirm`, `Complete, but not
  a decision yet`, `Not Identified as Decisions`, or `Source Limitations` —
  those have not changed since the first card set showed them. It carries the
  `▸ **Review Notes**` heading with the `Uncertain Decisions` category alone,
  preceded by the standard separator, and nothing else from Review Notes
  accompanies it.
- When no Decision remains at all, render the heading followed by the empty
  state, with the same blank line the spacing rule always requires between
  a heading and its list:

  ```text
  ▸ **Decision Candidates**

  - None
  ```

  There is no separate empty Action block to render alongside it — Actions
  no longer have a section of their own; a Decision with no Actions simply
  omits its `- **Actions**` bullet, exactly as it does anywhere else in this
  file.
- **When the prompt above shows, it shows alone.** A reply carrying the
  finalize prompt carries the receipt and the prompt — never the cards. The
  cards come next, in the save message, once the reviewer says yes.

## The save message

Sent the moment a finalize confirmation lands. It carries the lock, what
cannot be saved, and the request to save in one message, because these are
three parts of one decision and splitting them asks the reviewer to hold
them in their head across several turns.

Three blocks, in this order, each rendered only when it applies:

**1. The cards.** The full current set, in the shape above. Skip them only
when no edit batch has been applied since they were last shown whole — the
reviewer confirmed straight off the first card set and changed nothing, so
the cards are one message up. `references/review.md` §6 owns that test.

**2. What cannot be saved as it stands.** One line per candidate that is not
`approved`, or whose approver still carries `(awaiting approval)`. Never a
surprise: the same candidates have been flagged in Review Notes since the
first card set.

**3. The request to save.** Always.

```text
────────────────────────

▸ **Before saving**

- `D1: <title>` — still not approved, as flagged earlier. Leave it out, or tell me who approved it.
- `D5: <title>` — <one plain sentence saying what is unresolved>.

Say "save" when you're ready, and I'll write the rest to the Decision Bank. Nothing goes in until you do. Anything you leave out stays here.
```

- **The closing line does the work a lock acknowledgement used to do badly.**
  It says the version is settled, says nothing has been written, and says
  what to send next — the three things a reviewer needs at the one point in
  the flow where they have just finished everything they thought was asked
  of them.
- **Where block 2 is empty**, the message is the cards and a closing line
  with no `Before saving` heading: `Say "save" when you're ready…`. Never
  render an empty heading.
- **Say what each item needs in plain words**, using the same
  source-grounded sentence Review Notes uses — never a gate number, an enum
  name, or `evidence_type`.
- **Never imply that leaving something out discards it.** It stays in the
  finalized review and can be saved later.
- **When the save was already requested** — a reply that finalized and asked
  to save in one message — the closing line asks for confirmation instead:
  `Reply "yes" to write this to the Decision Bank.` Everything above it is
  unchanged.

### After a correction at the gate

A reply that only excludes candidates changes no record, so the save
proceeds against what was already shown. A reply that corrects one — setting
it to `approved`, or naming who actually approved a candidate whose approver
was still marked awaited — changes what will be written, and the
confirmation given for the earlier version cannot carry across it.

Re-render only the cards that changed, then ask again:

```text
`D1: <title> (*)`

- `decision_status(*)(options:approved|rejected|pending)`: approved
- `decision_approver(*)`: @alias
- <the rest of the card, unchanged>

▸ **Ready to save?**
That's `D1` updated. Reply "yes" and this goes to the Decision Bank.
```

- **Never repeat the whole set here.** A reviewer who corrected one
  candidate needs to see that candidate. Repeating the others buries the
  change they are being asked to check.
- The card renders in full, not as a diff — this is the last thing seen
  before an irreversible write, and a diff cannot be read as a record.

## The publication result

The last message of a successful run, and the only evidence the user has
that anything was written. Sent once, immediately after the write returns.

```text
▸ **Saved to the Decision Bank**

- `D2: <title>` — [record](URL)

Not saved: `D1: <title>` — left out at your request; still here if you want to save it later.
```

- One bullet per committed Decision, with the record address the publisher
  returned for it. Its Actions were committed inside it and are not listed
  again. When the publisher returns no address for a record, say so on that
  bullet in plain words rather than linking to something invented — the
  rule for a source with no URL, above, applies here for the same reason.
- The "Not saved" line repeats what gate 3 excluded, so the thread carries
  the full outcome in one place rather than only in a preview scrolled past.
  Omit the line entirely when nothing was excluded.
- Never restate the card contents here. The preview one message earlier
  showed them, and this message answers a different question: did it land.

**When the write fails**, the run still ends with a message — a silent
failure after an explicit "Yes, save" is the worst possible outcome, because
the user has every reason to believe it worked:

```text
▸ **Not saved**

The write to the Decision Bank didn't go through, so nothing was written. The version you confirmed is still locked here — reply "Yes, save" to try it again.
```

- Never surface the raw tool or MCP error, per `SOUL.md`; say what happened
  in plain language and what the user can do next.
- Say explicitly that nothing was written. After a confirmation, the default
  assumption is that it was.
- Never leave the locked version in doubt: it is unchanged, and retrying
  commits exactly what was previewed.
