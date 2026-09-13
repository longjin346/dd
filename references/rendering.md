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

## Every fence in this file is an exhibit, not output

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

> Whenever a `-` list follows a line that is not itself a list item — a
> section heading, a card's inline-code title line, a sentence of prose —
> put exactly one blank line between that line and the first `-` item. A
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
  - `D1` — Why uncertain: an eng-PIC approval was required before this could
    close (`cui.ju 3:20 PM`); no eng PIC signs off anywhere in the available
    thread. [View source](slack-permalink)
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

Two different things can be missing from a card, and a reviewer has to be
able to tell which at a glance — this is the fix for the worst bug in the
original draft, where an unconditional approver requirement made an honestly
unapproved decision impossible to finalize.

| Marker | Meaning | Fields it appears on |
|---|---|---|
| `(*)` | Required to **finalize** — lock this version for review. | `decision_title`, `decision_details`, `pst`, `decision_proposer`, `rationale`, `decision_status` |
| `(**)` | Required only to **publish** this Decision as `approved`. Never blocks finalize. Leave blank freely on a `pending` or `uncertain` candidate — that is not a gap, it is the honest state of a decision nobody approved. | `decision_approver` only |
| *(no marker)* | Optional, permanently. Never blocks anything. | `conditions`, `refs`, every Action field |

State this once, in the Read Me block, so the distinction is visible before
the reviewer looks at a single card:

```text
▸ **Read Me**

- This is an AI-generated draft of Decision Candidates, each with its own attached Actions.
- `(*)` fields must be filled before I can lock this version. `(**)` — right now only `decision_approver` — is needed only if a Decision ends up `approved`; leave it blank on anything else.
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
| `(*)` field, empty | `? - need to fill` |
| `(**)` field (`decision_approver`), empty | `? - optional to fill (required only if approved for publishing)` |
| Optional scalar, empty | `? - optional to fill` |
| Optional array, empty, on a drafted or extracted card | `[]` |
| Optional array, empty, on a blank add-a-decision template only | `? - optional to fill` (fillable; normalizes to `[]` if left untouched) |
| A Decision list block with no members | `- None` (see empty-state rule below) |
| An Action with no named owner | `no owner` |
| An Action with no date | `no date` |

Never render a missing `(*)` value as `null`. Never require the user to fill
anything with no marker.

## The Decision card

One self-contained card per candidate. `candidate_id` and `decision_title`
live in the heading, never as a field bullet. Every other `record` field
appears exactly once, in this order: `decision_details`, `pst`, `rationale`,
`decision_status`, `decision_proposer`, `decision_approver`, `conditions`,
`refs`. Person values use the Slack alias (`@long.jin`), never a display
name; a non-person approver (a declared no-objection forum) is shown by
plain name with no `@`.

```text
`D1: Saver-fare discount for Kalbe & Wardah (tactical) (*)`

- `decision_details(*)`: rahadiyan.wisesa proposed a Saver-fare discount for two merchants, Kalbe and Wardah, for a tactical purpose. The request was still awaiting eng-PIC approval when the thread ends; no explicit approval or rejection was ever given.
- `pst(*)`: FF Ecommerce
- `rationale(*)`: Kalbe & Wardah pickup points sit far from many PAX, creating delivery friction that free delivery removes, unlocking demand beyond the existing pickup-point catchment (rahadiyan.wisesa 3:26 PM).
- `decision_status(*)(options:approved|rejected|pending)`: pending
- `decision_proposer(*)`: @rahadiyan.wisesa
- `decision_approver(**)`: ? - optional to fill (required only if approved for publishing)
- `conditions`: Unmet: eng-PIC approval required before proceeding (@cui.ju 3:20 PM). Review was redirected to @arpit.goel by @cui.ju (3:22 PM); @randy.tedjakusuma, who the approval was originally addressed to, never endorsed that redirection.
- `refs`: 4 sources (reply "D1 refs" to view)
- **Actions**
  - A1 Documented the thread in the Confluence wiki (completed within the thread) — @arpit.goel — no date
  - A2 Add the logic that recreates the merchant list (SQL, or partnership-based?) — @sengkeong.ho, @moch.zulfa, @rangga.pratama (requested, not yet acknowledged) — no date
```

Card mechanics, carried forward unchanged in substance from the Gateway
contract above and applied identically to every card:

- Heading, one blank line, then top-level `-` field bullets with no leading
  spaces, then one blank line before the next card. A glued or indented
  top-level field renders as literal `-` text instead of a bullet.
- Field labels are the exact JSON key in inline code, with `(*)` or `(**)`
  appended inside the code span where it applies — `` `decision_details(*)` ``,
  never a renamed label like "Decision".
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
fields shown are exactly the finalize-required set plus the two permanently
optional ones; `decision_approver` is never demanded here either, for the
same reason it is never demanded anywhere during review:

```text
`D{next}: ? - need to fill (*)`

- `decision_details(*)`: ? - need to fill
- `pst(*)`: ? - need to fill
- `rationale(*)`: ? - need to fill
- `decision_status(*)(options:approved|rejected|pending)`: ? - need to fill
- `decision_proposer(*)`: ? - need to fill
- `decision_approver(**)`: ? - optional to fill (required only if approved for publishing)
- `conditions`: ? - optional to fill
- `refs`: ? - optional to fill
```

`add an action` no longer sends a card — a single blank line, naming its
parent Decision as established at creation:

```text
A{next} ? - optional to fill (task) — ? - optional to fill (owner) — ? - optional to fill (date)
```

## References, on request

Hidden by default behind the card's summary line; shown in full only when
asked ("D1 refs"). Each reference is one bullet with one compact link:

```text
`D1` references

- [slack, "may we proceed with this approval request from rahadiyan.wisesa"](slack-permalink-1)
- [slack, "please inform the respective eng PIC and get approval from them first"](slack-permalink-2)
- [slack, "Since there is no governance on the grabx group…"](slack-permalink-3)
- [wiki, "I have documented the thread here…"](https://grabtaxi.atlassian.net/wiki/spaces/.../foodSaverOptionDiscount)
```

Link text is `ref_type, "excerpt"` — and an excerpt is free text pulled
verbatim from the thread, so it can contain exactly the characters that
break a Markdown link: a closing bracket or parenthesis, or a URL (several
messages in the reference thread paste one directly into their text, as in
the fourth bullet above). Sanitize before building the link, every time:

1. Scan the excerpt for the first `]`, `)`, or a recognizable URL (a
   `http://`/`https://` run, or a bare domain-shaped fragment like
   `grabtaxi.atlassian.net/…`).
2. If found, cut the excerpt immediately before it and append `…`. That is
   the entire fix for the fourth bullet above: the raw excerpt is `I have
   documented the thread here - grabtaxi.atlassian.net/wiki/…` — the
   sanitized label stops at `I have documented the thread here…`, and the
   real URL still lives where it belongs, as the link's actual target.
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

- **Inferred Values to Confirm**
  - `D1 pst`: FF Ecommerce — inferred from the thread calling this "this
    eComm decision" and tying the product to Fulfillment. Confirm or change.
- **Uncertain Decisions**
  - `D1` — Why uncertain: eng-PIC approval was required before this could
    close (`cui.ju 3:20 PM`); no eng PIC appears anywhere in the available
    thread, and the review that followed was redirected to `@arpit.goel`,
    who was never the entitled party. [View source](slack-permalink)
- **Not Identified as Decisions**
  - Interim ZFF/EAR stopgap — reported as the team's existing approach, not
    proposed for a decision here. [View source](slack-permalink)
  - The fare-certainty/batching principle and the FR capacity-vs-pricing
    discussion — background reasoning, no proposed course of action.
    [View source](slack-permalink)
  - The request to use the capture tool, and the question about available
    sources — messages about the capture process itself.
  - "Heart, Hunger, Honour, Humility" — an automated values-bot message, no
    proposal content.
- **Source Limitations**
  - [Jira — ABC-123](URL) could not be read because access was denied.
```

- Never add a missing-fields category here — the inline `? - need to fill`
  markers and the Read Me block already say what's missing; repeating it
  would only duplicate and crowd out the notes that carry new information.
- List an inferred value only when the model actually filled it by
  inference — never a value taken from direct source evidence, and never a
  field that's simply unresolved (that's already `? - need to fill` on the
  card).
- Never expose a Gate id, an enum name, `evidence_type`, or chain-of-thought
  in a `Why uncertain` line — rewrite it as one plain, source-grounded
  sentence.
- Source Limitations, when present, is always last, one entry per unread or
  inaccessible selected source, stated once — never repeated per Candidate.

## The change receipt

Follows every applied edit batch, always — never a re-rendered card set.
Structural changes (add, drop, merge, confirm) come first, in this order,
then field-level changes, each showing previous → new value verbatim
(shorten a long *previous* value to a few words plus `…`; never shorten the
new value):

```text
▸ **Applied**

- Dropped `D3: Pilot in SG` and its linked Action `A2`
- Merged `D4` into `D1`; kept `D1: Adopt option A`
- Added `D5: Extend the pilot`
- Confirmed `D2` as a Decision; no field values changed
- `D2 pst`: ? - need to fill → FF Ecommerce
- `D1 decision_status`: pending → approved
```

- Show a previous placeholder verbatim (`? - need to fill` or `? - optional
  to fill (required only if approved for publishing)`) so the user can tell
  a filled blank from an overwritten value.
- Mention uncertainty only when this batch actually changed a candidate's
  uncertain state — one line saying it's now confident, or newly uncertain
  with its `Why uncertain` sentence. Don't resend the whole category for no
  reason.
- Whether a given response carries a receipt, a single card, or the full set
  is decided by `references/review.md` §6, never here. When it calls for a
  single card, render that card in the Decision card format above. Never
  render the same card twice in one message.

## The missing-fields prompt

Ends the response instead of a finalize prompt — never both in the same
message — whenever a finalize-required field is still unresolved on any
current Decision. Actions are never checked; they have no required field at
either tier.

```text
▸ **Still needed before finalizing**

- `D2 pst(*)` — Which PST does this belong to?
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
- Never list `decision_approver` here — it carries `(**)`, not `(*)`.
- Never ask for `conditions`, `refs`, an Action field, or any other
  unmarked field.
- A missing `pst` always gets the numbered list, in `psts.json`'s configured
  order, so a bare number reply resolves against it.

## The full current set, and the finalize prompt

Renders in full only at the two moments the reviewer is about to be asked to
lock or commit something they have not yet seen whole in its current form —
timing owned by `references/review.md`; this section only fixes its shape.
Begin with every current Decision card (this format, nested Actions
included). Then, only when at least one Decision is still uncertain, one
separator followed by the `▸ **Review Notes**` heading carrying the
`Uncertain Decisions` category alone. The finalize prompt closes the
message, with no further separator:

```text
▸ **Decision Candidates**

`D1: Saver-fare discount for Kalbe & Wardah (tactical) (*)`

- `decision_details(*)`: rahadiyan.wisesa proposed a Saver-fare discount for two merchants, Kalbe and Wardah, for a tactical purpose. The request was still awaiting eng-PIC approval when the thread ends; no explicit approval or rejection was ever given.
- `pst(*)`: FF Ecommerce
- `rationale(*)`: Kalbe & Wardah pickup points sit far from many PAX, creating delivery friction that free delivery removes, unlocking demand beyond the existing pickup-point catchment (rahadiyan.wisesa 3:26 PM).
- `decision_status(*)(options:approved|rejected|pending)`: pending
- `decision_proposer(*)`: @rahadiyan.wisesa
- `decision_approver(**)`: ? - optional to fill (required only if approved for publishing)
- `conditions`: Unmet: eng-PIC approval required before proceeding (@cui.ju 3:20 PM). Review was redirected to @arpit.goel by @cui.ju (3:22 PM); @randy.tedjakusuma, who the approval was originally addressed to, never endorsed that redirection.
- `refs`: 4 sources (reply "D1 refs" to view)
- **Actions**
  - A1 Documented the thread in the Confluence wiki (completed within the thread) — @arpit.goel — no date
  - A2 Add the logic that recreates the merchant list (SQL, or partnership-based?) — @sengkeong.ho, @moch.zulfa, @rangga.pratama (requested, not yet acknowledged) — no date

`D2: Wiki page to document the pricing-config variable (*)`

- `decision_details(*)`: sengkeong.ho proposed a wiki page to document mex-specific pricing configs, narrowed from "all markets" to this one variable, linked back to the variable as the central source of truth.
- `pst(*)`: FF Ecommerce
- `rationale(*)`: Handling mex-specific pricing configs on ExP is established practice; the wiki closes the traceability gap the team hit today, where legacy configs have no visible owner or purpose (sengkeong.ho 8:55 AM; albert.lim 8:57 AM).
- `decision_status(*)(options:approved|rejected|pending)`: approved
- `decision_proposer(*)`: @sengkeong.ho
- `decision_approver(**)`: @albert.lim
- `conditions`: ? - optional to fill
- `refs`: 3 sources (reply "D2 refs" to view)
- **Actions**
  - A3 Set up a wiki page for this variable and document the pricing configs there — @rahadiyan.wisesa (requested, not yet acknowledged) — no date

────────────────────────

▸ **Review Notes**

- **Uncertain Decisions**
  - `D1` — Why uncertain: eng-PIC approval was required before this could
    close (`cui.ju 3:20 PM`); no eng PIC appears anywhere in the available
    thread. [View source](slack-permalink)

▸ **Ready to finalize?**
Look right? Reply "Yes, finalize" to lock this version, or send any remaining changes.
```

- This is the exact block for defect 4: the re-render before locking never
  repeats `Inferred Values to Confirm`, `Not Identified as Decisions`, or
  `Source Limitations` — those haven't changed since Step 3 first showed
  them. It shows the `▸ **Review Notes**` heading together with only the
  `Uncertain Decisions` category, preceded by the standard separator, and
  nothing else from Review Notes accompanies it.
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
- Confirming finalize renders nothing new — the set was just shown as part
  of setting the finalize flag in the same turn; acknowledge the lock by
  referencing that already-shown revision.

## The publication preview

Renders unconditionally right before the one save confirmation — this is
irreversible, so the reviewer sees the exact set that is about to commit,
including anything excluded at the gate. Because an Action now lives inside
its Decision's card, a saved Decision's card already shows every Action
attached to it — there is no separate `Actions to Save` section to keep in
sync with it.

```text
▸ **Decisions to Save**

`D2: Wiki page to document the pricing-config variable (*)`

- `decision_details(*)`: sengkeong.ho proposed a wiki page to document mex-specific pricing configs, narrowed from "all markets" to this one variable, linked back to the variable as the central source of truth.
- `pst(*)`: FF Ecommerce
- `rationale(*)`: Handling mex-specific pricing configs on ExP is established practice; the wiki closes the traceability gap the team hit today, where legacy configs have no visible owner or purpose (sengkeong.ho 8:55 AM; albert.lim 8:57 AM).
- `decision_status(*)(options:approved|rejected|pending)`: approved
- `decision_proposer(*)`: @sengkeong.ho
- `decision_approver(**)`: @albert.lim
- `conditions`: ? - optional to fill
- `refs`: 3 sources (reply "D2 refs" to view)
- **Actions**
  - A3 Set up a wiki page for this variable and document the pricing configs there — @rahadiyan.wisesa (requested, not yet acknowledged) — no date

▸ **Not Included**

- `D1: Saver-fare discount for Kalbe & Wardah (tactical)` — excluded (still `pending`; eng-PIC approval was never given). Reply "D1 approved by <name>" to include it instead.

▸ **Ready to Save?**
These are the exact Decisions and Actions that will be saved to the Decision Bank.

Reply "Yes, save" to commit this version, or send any remaining changes.
```

- Every Decision shown here already carries the full publish-required set —
  finalize-required plus a named `decision_approver` — and
  `decision_status: approved`; that field check is owned by
  `references/review.md` §8, this section only renders its result.
- List every excluded item under `▸ **Not Included**` with its ID, title,
  and reason — never drop one silently, and never treat silence as
  approval.
- Never show raw JSON anywhere in this preview.

## Worked check against the reference thread

Building D1 and D2 against every rule above surfaces the same failure mode
the original draft had: it is easy to state a rule and violate it three
templates later. Checked line by line here:

- D1's card and the full-set render both put a blank line between the
  heading and the first `-` field, and between `▸ **Review Notes**` and
  `- **Uncertain Decisions**` — no template above skips it.
- D1's `decision_approver` reads `? - optional to fill (required only if
  approved for publishing)`, not `? - need to fill` — a reviewer scanning
  the card sees immediately that this is not something blocking finalize,
  which is the entire fix for the original's unconditional `(*)`.
- D1's Actions (`A1`, `A2`) sit nested under `- **Actions**` inside D1's own
  card — no separate Action Candidates section exists anywhere in this
  file.
- D1's fourth reference sanitizes the pasted Confluence URL out of the link
  label while keeping it as the actual link target — the concrete fix for
  defect 6.
- The publication preview excludes D1 (still `pending`, no approver) and
  publishes D2 outright (`approved`, `@albert.lim`) — matching
  `references/review.md` §10's own worked check — and needs no `Actions to
  Save` section because D2's card already shows `A3`.
