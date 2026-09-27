# The Novel Writing Handbook

## A craft manual written for an AI that has to write a whole book on its own

This handbook is not a description of how novels work. It is a set of operating
instructions. Every module is written to be read by a model that is about to
make a decision, and every module ends with rules that can be checked against a
draft.

It covers **long-form fiction** in two modes: commercial genre fiction and
literary fiction. Where the two modes disagree, the disagreement is stated
explicitly rather than averaged away.

---

## The modules

| # | Module | Answers |
|---|--------|---------|
| 01 | [Structure](01-structure.md) | How is a book shaped? Which skeleton, and where do the load-bearing beats sit? |
| 02 | [Narration](02-narration.md) | Who tells this, from how far away, in what tense, in what order? |
| 03 | [Character](03-character.md) | Why does anyone care about this person? What changes in them? |
| 04 | [Hook & Tension](04-hooks-and-tension.md) | Why does the reader turn page 1, and page 147? |
| 05 | [Scene & Prose](05-scene-and-prose.md) | What happens inside a scene, sentence by sentence? |
| 06 | [Genre Conventions](06-genre-conventions.md) | What does a reader of *this* genre demand and never forgive? |
| 07 | [Literary Mode](07-literary-mode.md) | What changes when the point is not the plot? |
| 08 | [Quality Control](08-quality-control.md) | How do I catch my own failures before the reader does? |
| 09 | [Production](09-production.md) | How do I get 90,000 words of this onto disk without the book falling apart? |

Setup and tooling for the project itself live outside the handbook, in
[`00-getting-started.md`](../00-getting-started.md).

---

## Order of operations

Do not write prose until steps 1–5 are answered in writing. A model that begins
drafting from an unanswered premise will produce fluent, competent, forgettable
text — this is the single most common failure mode, and no amount of good
sentence-level writing repairs it.

1. **Premise.** A story question in two sentences: *When [event], [specific
   protagonist] must [goal]. Can she, when [specific opposition], and failure
   would cost her [specific stakes]?* The **stakes** are what she stands to
   lose — scaled to the genre: a cozy premise puts a shop, a place in a
   community, a friendship at risk; a thriller premise puts lives at risk.
   The premise names the stakes only. It does not have to name the **price**
   — what is actually taken from her, and when — because that is decided with
   the Wound in step 3. The one exception: if the premise already implies a
   price mechanic (a magic that takes something, a bargain, a curse), the
   three price checks in Module 03, section 5a apply now, because a broken
   price mechanic cannot be repaired later without rewriting the premise.
   A premise is not a story bible: it does not yet contain the
   character's Lie, the midpoint, or the climax mechanics. Those are built in
   steps 3–4 and must not be demanded of the premise. Test: would this
   sentence, with names and places swapped, describe one existing well-known
   book exactly? Then sharpen the one element that makes it yours.
   The premise is built from the author's wish list, not from the rules alone;
   see the antagonist checks in Module 03, section 5a, for what *can* be
   tested at this stage.
2. **Genre contract.** Module 06. Which genre, which obligatory scenes, which
   ending shape, what length.
3. **Character core.** Module 03. Wound → Lie → Want → Need for the protagonist
   and for the antagonist.
4. **Structure.** Module 01. Pick one skeleton, place the beats at word counts,
   not at vague fractions.
5. **Narration.** Module 02. POV, tense, distance, timeline. Lock it. Drifting
   later is the second most common failure mode.
6. **Scene list.** Every scene gets: POV character, goal, opposition, outcome
   (`no` / `no and` / `yes but`), and the value that flips (Module 05).
7. **Draft**, scene by scene, never chapter-summary by chapter-summary.
8. **Self-audit** against Module 08 before declaring anything finished.

---

## Vocabulary: stakes, price, cost

Three things are routinely called "cost" and they behave differently. The
handbook uses one word for each, and uses them as terms of art wherever they
appear in bold.

| Term | Definition | Tense | Where it is fixed |
|---|---|---|---|
| **Stakes** | What she may lose if she fails. Conditional, in the future. Can be raised, lowered, or escalated. | future | Premise (step 1), Module 04 §2 |
| **Price** | What has actually been taken from her and does not come back. Unconditional, in the past. Cannot be un-paid. | past | Character core (step 3), Module 03 §5a–5b, Module 04 §8 |
| **Cost** | What a mechanic spends per use — mana, metal, body heat, a year of life. A property of a system, not of a person. | per use | Genre contract (step 2), Module 06, Fantasy |

Three consequences:

- **Stakes are not a price.** A book in which everything is threatened and
  nothing is lost teaches the reader that the threats are decorative.
- **A cost is not a price.** A mechanic that drains a tank produces resource
  management. It becomes a price only when spending it changes who she is, or
  forces a choice between two things she wants. See Module 03 §5a.
- **Lower case is not a term.** "The Lie operating at cost", "a scene that
  costs nothing" and similar ordinary uses are left alone throughout.

---

## Five standing rules

These override any other instruction in this handbook when they conflict.

**1. Specificity beats competence.**
The default failure of a language model is the plausible average. A "dusty
tavern," a "hardened detective," a "storm rolling in." Every time a detail could
be swapped for the generic version of itself without loss, it is the wrong
detail. Choose the detail only this character, in this place, would notice.

**2. Dramatize, do not report.**
If a moment matters, it happens on stage in real time with dialogue and physical
action. Summary is for the connective tissue between the moments that matter.
A model that summarizes its own best scenes has written an outline, not a novel.

**3. Nothing is stated twice.**
Do not have a character feel something, then say it, then have the narrator
explain it. Pick one register per beat, usually the least explicit one that
still lands.

**4. Every scene costs the character something.**
See Module 05. A scene where the protagonist wants nothing, or gets what they
want cleanly, is a scene the reader can skip. Readers who can skip, stop.

**5. Consistency is a hard constraint, not a stylistic preference.**
Eye colour, sibling counts, the day of the week, who knows what and when, how
long the journey takes. Maintain a running story bible and consult it before
each scene. Contradictions destroy reader trust faster than weak prose.

---

## How critique is run

These four rules apply to every review pass in this handbook — premise,
outline, scene, or draft. They exist because a critic instructed only to find
faults will find them, every time, and a process whose criteria grow faster
than its candidates never converges.

- **No objection without a repair.** Every fault named comes with a proposed
  fix of at most three sentences that turns one dial.
- **A gap is not a break.** What a text does not yet say is listed as "open",
  not scored as a failure. Only what the text says can be wrong.
- **Criteria are frozen before the pass.** A new failure pattern discovered
  during a review is recorded under "observations" and applied from the next
  round on, never to the text it was found in.
- **Scores, not verdicts.** A text is not "rejected"; it receives a number per
  criterion and a repaired version. The author decides what goes forward.

---

## How to use this with a model

- Load **README + Module 01 + 03 + 06** during planning.
- Load **README + Module 02 + 05** during drafting, plus the relevant genre
  section of 06.
- Load **Module 08** alone for a revision or critique pass, and run it as a
  separate task with a fresh context so the model is not defending its own work.
- Load **Module 09** once to set up the working loop, then follow it rather than
  re-reading it. It defines the scene loop, the context budget per task type, the
  continuity system, the critic roles, and the language-specific blacklist.

The handbook assumes the model can hold a story bible (characters, timeline,
established facts, open promises) and re-read it. If it cannot, the book will
break somewhere around the middle regardless of craft. Module 09 is how that
assumption is made true in practice.
