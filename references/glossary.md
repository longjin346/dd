# Glossary — in-house terms that appear in captured threads

The threads this skill reads are written by people talking to each other,
not to a reader outside the team. They are dense with abbreviations that
carry a specific local meaning, and several of them look exactly like
something else: `MEX` is the ISO country code for Mexico, `ID` is the one
for Indonesia, and only one of those two readings is right in a thread that
uses both.

This file exists because a wrong expansion is invisible. A record that says
a discount applies "in Mexico" reads perfectly, cites real messages, and is
false — and nothing downstream can catch it, because the error was made
while reading, not while reasoning.

`references/extraction.md` owns the rule this file serves: **never expand an
abbreviation the source did not expand.** The tables below are the narrow
exception — terms confirmed by the team, safe to read with their stated
meaning.

## Confirmed

Use these meanings when the term appears. They are confirmed, not inferred.

| Term | Meaning |
|---|---|
| `MEX`, `mex` | merchant, merchants |
| `PAX` | consumer — the person ordering |
| `DAX` | driver |
| `ExP` | the experiments and configuration platform (`experiments.grab.com`) |
| `PIC` | person in charge |
| `SLA` | the delivery-time commitment on a service type |
| `AOV` | average order value |
| `FMCG` | fast-moving consumer goods |
| `ID` | Indonesia |
| `Mart` | the GrabMart product line |

`MEX` and `ID` sit in the same table on purpose. One is a country code in
this context and the other is not, and no amount of care with the shape of a
token will tell them apart — only this table does.

## Unconfirmed — never expand these

These appear in captured threads and have **no confirmed meaning**. They are
listed so a reader knows the omission is deliberate rather than an oversight,
and so nobody fills one in from a plausible guess.

Treat every term here as the rule's default case: **write it exactly as the
thread wrote it.** A guess that lands in `decision_details` or `rationale`
becomes part of a published record.

| Term | Where it appears |
|---|---|
| `FR` | "balancing FR during crunch", "poorer FR", FR capacity discussions |
| `ZFF` | "use mex ZFF" |
| `EAR` | "correct for dax EAR" |
| `LO` | "if it's an LO it won't be batchable" |
| `grabx` | "no governance on the grabx group" |
| `DMS-Go+` | "combining both levers under DMS-Go+" |
| `FF` | the `FF Ecommerce` PST value |
| `Saver` | a Mart service tier |

## Adding an entry

An entry moves from Unconfirmed to Confirmed when a person who works with
the term says what it means. Not when a thread makes one reading look
likely, and not when a model finds a plausible expansion — those are the two
routes that produce a confident, wrong glossary, which is worse than no
glossary at all, because a wrong entry is trusted by everything downstream.

Terms that never need an entry: ordinary English, industry-standard terms a
general reader would get right, and anything the thread expands itself.
