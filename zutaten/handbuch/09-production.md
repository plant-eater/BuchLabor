# Module 09 — Production: writing a whole book chapter by chapter

Modules 01–08 describe the craft. This module describes the **process** that gets
90,000 words of it onto disk without the book falling apart in the middle.

It exists because a language model writing a novel has one failure mode no human
author has: it cannot hold the book in mind. A human writer forgets details. A
model forgets the book. Everything below is machinery for compensating.

Read alongside [`00-getting-started.md`](../00-getting-started.md), which sets up
the folders this module operates on.

---

## 1. The invariant

> **The bible is the truth. The manuscript is derived from it.**

Whenever the two disagree, one of them is wrong and the disagreement must be
resolved explicitly, in writing, before the next scene is drafted. It is never
resolved by drafting onward and hoping.

Consequence: a fact that exists only in the manuscript does not exist. If scene 12
established that the aunt lives in the next valley, and that is not in
`bible/facts.md`, then by scene 40 it is gone.

---

## 2. Three states, three access rules

| State | Files | Rule |
|---|---|---|
| **Plan** | `bible/premise.md`, `structure.md`, `scenes.tsv` | Changed only in a planning session, never mid-scene |
| **Memory** | `bible/characters.md`, `facts.md`, `timeline.md`, `promises.md` | Read before every scene, written after every scene |
| **Product** | `manuscript/**` | Written once per scene, revised only in a revision pass |

The most common process failure is a drafting session that quietly edits the
plan to make the scene it wants to write legal. If the plan is wrong, stop
drafting and say so.

---

## 3. The scene loop

This is the core cycle. It runs once per scene, start to finish, in one session.
Do not run two scenes in one session until the loop is boring.

### Step 1 — Contract check

Read the scene's row in `scenes.tsv`. Fields (German column names from Module 00):

```
nr | kapitel | beat | pov | ziel | opposition | ausgang | wertwechsel | frage | wortziel | status | szenentyp
```

If any contract field (`pov`, `ziel`, `opposition`, `ausgang`, `wertwechsel`,
`wortziel`) is empty or contains `[offen: …]`, **stop and ask**. A row with
`status` = `gestrichen` is not drafted. `beat` and `frage` are planning aids; `frage`
is the scene question that must still be open when the scene ends. `szenentyp`
is the exception: it only selects the style model (`style/szenentyp.md`) and may stay
empty. Do not invent a scene goal. A scene drafted without a contract is the
single most expensive kind of wasted work, because it reads competently and hides
its own emptiness.

### Step 2 — Pre-flight load

Load exactly this, and nothing else:

- `bible/characters.md` — the entries for the characters in this scene only
- `bible/facts.md`
- `bible/narration.md` — the locked narration: person, distance, tense, the POV
  character's vocabulary
- `bible/timeline.md` — the last three entries
- The **previous scene's final 150 words**, for continuity of moment and rhythm
- `handbook/05-scene-and-prose.md`
- The genre section of `handbook/06` relevant to this book

Do **not** load: the whole manuscript, earlier chapters in full, the whole
handbook, or the full character file for a cast of twenty. Every irrelevant token
loaded is capacity taken from the writing.

### Step 3 — Draft

One scene, one file, to the word target. Write to the end. Do not stop to
evaluate; evaluation happens in Step 5, in a different session.

### Step 4 — Post-flight update

Part of the task, not a follow-up request:

- `bible/promises.md` — add every question this scene raised; close every one it
  answered, with the scene number
- `bible/timeline.md` — day, elapsed time, location, and any physical state that
  persists (injury, exhaustion, weather, what someone is carrying)
- `bible/facts.md` — every new concrete detail invented while drafting
- `bible/characters.md` — what each present character now knows, and as of when
- `scenes.tsv` — status → `draft`, actual word count

The knowledge column is the one that gets skipped and the one that breaks books.
Track it as: `character | learned | in scene | from whom`.

### Step 5 — Commit and clear

```bash
git add -A && git commit -m "Szene 14 Rohfassung"
```

Then `/clear`. The session that wrote the scene is finished. It has nothing
further to contribute, and everything it still holds is now noise.

---

## 4. Context budget

Treat context as a scarce resource with an explicit budget per task type.

| Task | Load | Never load |
|---|---|---|
| Plan a scene | scenes.tsv, structure.md, promises.md | Manuscript prose |
| Draft a scene | Section 3, Step 2 | Other chapters, other scenes' drafts |
| Critique a scene | Module 08, the scene, characters.md | The plan, the author's intent, your own earlier reasoning |
| Chapter review | The chapter's scenes only | Anything outside the chapter |
| Continuity sweep | bible/*, plus grep results | Full prose |

**Rule: never let a drafting session exceed one scene of accumulated output.**
Quality decline from a full context window is silent. It does not announce
itself, and the prose stays fluent while the judgement degrades.

---

## 5. Continuity

### What actually breaks

In order of frequency:

1. **Knowledge.** A character acts on information they were never given.
2. **Time.** Two days pass in chapter 8 and one day in chapter 9's reference to it.
3. **Physical state.** A wound from chapter 11 has no effect in chapter 12.
4. **Objects.** Something is left behind and then used.
5. **Named details.** Eye colour, sibling count, the name of the inn.
6. **Established rules.** Magic that costs something in chapter 4 and nothing in
   chapter 30.

### Mechanical checks

Run these before each chapter is declared complete. They are cheap and they catch
the majority of breaks without reading anything.

```bash
# Every capitalised word ever used, with counts — spelling drift shows up as
# near-duplicates (Tarek / Tarrek). -P and the UTF-8 locale are required, or
# umlauts break the word boundaries and the output is garbage.
LC_ALL=C.UTF-8 grep -ohP '(?<![\p{L}])\p{Lu}\p{Ll}{2,}' manuscript/ch*/s*.md \
  | sort | uniq -c | sort -rn | head -60

# Scene word counts against target
wc -w manuscript/ch*/s*.md

# Open promises: rows whose Stand column is "offen" or "läuft"
grep -cE '\| *(offen|läuft)' bible/promises.md

# POV consistency: the POV name should dominate its own scene
grep -o 'Mira' manuscript/ch03/s09-*.md | wc -l
```

### The knowledge matrix

For any book with a secret — which is every mystery, most romance, and all
fantasy with a hidden past — maintain an explicit table:

```
Fakt              | wer weiß es | seit Szene | von wem
Der Brief         | Mira        | 7          | selbst gefunden
Der Brief         | Tarek       | 19         | Mira hat es gesagt
Der Brief         | Leser       | 7          |
```

The reader is a row in this table. Dramatic irony (Module 04) is engineered by
deliberately putting the reader's row ahead of a character's.

### Chapter-boundary sweep

At the end of each chapter, in a fresh session, with the bible and the chapter
loaded and nothing else:

- List every fact this chapter asserts that contradicts `facts.md`.
- List every character who acts on knowledge not in their row of the matrix.
- List every promise opened and not recorded.
- Report only contradictions. No summary, no praise.

---

## 6. Self-critique in fresh contexts

### Why the fresh context is non-negotiable

A model that just produced a text has that text's reasoning in context, and
critique becomes justification. This is not a matter of prompting harder. The
only reliable fix is separation: the critic must not have written the thing, and
must not know what the author intended.

Two implementations, from Module 00 section 8: `/clear` plus a new session, or a
read-only subagent with its own context window. Use the second once the routine
is established.

### The three critics

Run them separately. A single "critique this" prompt returns shallow, evenly
distributed comments on everything; a narrow brief returns findings.

**Critic 1 — the scene critic** (after each scene)
> You did not write this text and you do not know what the author intended.
> Read `handbook/08-quality-control.md`, pass 4 and pass 5, and the scene.
> Report: (a) the value at scene open and close — if unchanged, say so; (b) every
> sentence where the POV character's goal is not detectable; (c) every blacklist
> hit with a quote. No praise, no rewrites, no summary.

**Critic 2 — the reader** (after each chapter)
> Read this chapter cold. Answer four questions and nothing else:
> What do I want to know at the end of this chapter? Why would I turn the page?
> Where did I get bored — name the paragraph. What did I not understand?

The reader critic is the most useful of the three and the one most often skipped,
because its findings are the least actionable and the most important.

**Critic 3 — the structural critic** (every 10 scenes)
> Read `bible/structure.md`, `scenes.tsv` and the scene list only — no prose.
> Where is the draft against its beat schedule in words? Which scenes have the
> same outcome type in a row? Which subplot has not been touched in more than
> four scenes? Which promise is older than 40 scenes and still open?

### Adjudication

Critique output is evidence, not instruction. Before acting on a finding:

- **Accept** if it cites a specific line and names a rule from the handbook.
- **Reject** if it is a preference ("I would have..."), a rewrite offered without
  a diagnosis, or a request for more explanation of something deliberately withheld.
- **Escalate to the author** if two critics disagree, or if the fix requires
  changing the plan.

Record accepted findings in `notes/` and apply them in a **revision** session, not
in the critique session. A critic that also fixes stops being a critic.

---

## 7. Revision cadence

Do not polish scene 1 forty times. Diminishing returns arrive faster than they
feel like they do, and a heavily polished opening on an unproven structure is the
most common way a book dies.

| Level | When | What |
|---|---|---|
| Scene | Immediately after critic 1 | Only accepted findings. One pass. Then move on. |
| Chapter | At chapter close | Continuity sweep, reader critic, transitions between scenes |
| Act | At 25%, 50%, 75% | Module 08 passes 1–3. Structure before prose. |
| Book | After the full draft | Module 08, all six passes, in order |

**The rule for the first draft:** a scene is done when it meets its contract and
survives critic 1. It is not done when it is good. Books are finished in
revision; drafts are finished by moving forward.

---

## 8. Drift

Over 50 scenes, voice, distance and register slide. The model does not notice,
because each scene resembles the one before it.

**The anchor.** After the first three scenes are accepted, copy the strongest 400
words into `bible/voice-anchor.md`, with three lines naming what makes it work
(sentence rhythm, distance, what the narrator notices). Load it with every
drafting session. It costs ~600 tokens and it is the cheapest quality
intervention available.

**The drift check.** Every 15 scenes, in a fresh session, load only the anchor and
the most recent scene:

> These are from the same book. Name every difference in sentence rhythm,
> psychic distance, vocabulary register and what the narration chooses to notice.
> Do not judge quality. Only describe difference.

Deliberate change (a character under pressure, a tonal shift) is fine. Undirected
change is drift, and the fix is to redraft toward the anchor.

---

## 9. When the plan breaks

It will. Around scene 20 a scene will reveal that the outline is wrong — usually
that a character would not do the thing the plan requires.

**The outline is a hypothesis.** It was written before anyone knew these people.
When the draft contradicts it, the draft is usually right about the character and
the plan is usually right about the shape.

Procedure, in a planning session, never mid-scene:

1. State the contradiction in one sentence.
2. Decide which is wrong: the character (behaving out of their established Lie
   and Want) or the plan (requiring behaviour the character would not produce).
3. If the plan: re-plan **forward only**. Change the remaining scenes. Do not
   rewrite the finished ones yet; note the required retrofits in
   `notes/retrofit.md` and apply them in the book-level revision.
4. If the character: `bible/characters.md` was incomplete. Fix it there first,
   then redraft the scene.
5. Update `structure.md` and `scenes.tsv`, commit, and only then resume.

Never resolve a plan break by writing a scene that satisfies both. That scene
will be vague, and vagueness at the level of story is not recoverable by prose.

---

## 10. German-language AI blacklist

Module 05's blacklist is English. This book is written in German, so that list
catches nothing. Use this one, by the same method: literal search, count, budget,
rewrite down.

### Verbotene Konstruktionen

- **„Nicht nur X, sondern Y"** und Varianten: *nicht bloß, mehr als nur, weniger
  ein X als vielmehr ein Y*
- **Die Antithese im Zweisatz:** „Sie hatte keine Angst vor dem Sterben. Sie
  hatte Angst davor, vergessen zu werden."
- **Der Ein-Wort-Absatz als Trommelwirbel:** *Stille. Dann. Nichts.*
- **Der zusammenfassende Schlusssatz** eines Absatzes, der erklärt, was der
  Absatz bedeutete
- **Dreierfiguren überall** — jede Aufzählung, jede Beschreibung dreigliedrig
- **Filterkonstruktionen:** *sie spürte, wie… / sie sah, wie… / sie merkte, dass…
  / sie fühlte, wie…* In personaler Erzählweise nahezu vollständig streichen.

### Verbotenes Vokabular

*ein Hauch von, ein Anflug von, greifbar, unausgesprochen, ein Wandteppich aus,
eine Symphonie aus, ein Tanz aus, letztendlich, im Grunde, ein Stück weit,
irgendwie, dabei (als Füllwort), etwas in ihr zerbrach, etwas verschob sich,
ein Lächeln, das die Augen nicht erreichte, sein Blick verdunkelte sich,
die Luft war schwer von, es lag etwas in der Luft*

### Verbotene Gefühlskürzel

*Das Herz schlug ihr bis zum Hals. Ein Schauer lief ihr über den Rücken. Ein Kloß
im Hals. Sie hielt den Atem an, ohne es zu merken. Ihr Magen zog sich zusammen.
Gänsehaut. Sie atmete tief durch. Sie wusste nicht, ob sie lachen oder weinen
sollte.*

Ersetzen durch: eine konkrete Handlung, eine verzerrte Wahrnehmung, oder einen
Gedanken, der den Zustand seitlich verrät (Modul 02).

### Deutschspezifische Warnsignale

- **Nominalstil.** *unter Zuhilfenahme von, im Rahmen der, es erfolgte eine* —
  Behördendeutsch in der Prosa.
- **Zu korrekte Syntax.** Ein Modell schreibt grammatisch tadellose,
  gleichförmige Hauptsatz-Nebensatz-Ketten. Deutsche Erzählprosa lebt von
  Ellipsen, Anakoluthen und Sätzen ohne Verb.
- **Dialog ohne Dialekt, Soziolekt oder Idiolekt.** Alle Figuren sprechen
  gepflegtes Hochdeutsch mit vollständigen Sätzen. Niemand spricht so.
- **Übersetzungsklang.** Wendungen, die aus dem Englischen gedacht sind:
  *Es macht Sinn. Ich schätze, ja. Am Ende des Tages. Realisieren* (statt
  *begreifen*). *Nicht wirklich.*

### Die Prüfung

```bash
# Blacklist-Treffer, mit Datei und Zeile
grep -oniE 'nicht nur .{0,40} sondern|ein Hauch von|ein Anflug von|greifbar|unausgesprochen|Kloß im Hals|Gänsehaut|bis zum Hals|über den Rücken|letztendlich|irgendwie|ein Stück weit|mach(t|te|en) .{0,20}Sinn|nicht wirklich|die Augen nicht erreichte' manuscript/ch*/s*.md

# Filterkonstruktionen
grep -oniE 'spürte, wie|sah, wie|merkte, dass|fühlte, wie|bemerkte, dass' manuscript/ch*/s*.md | wc -l
```

Budget: zero for the constructions and the emotional shorthand; at most one per
20,000 words for the vocabulary items that occasionally have a legitimate use.

---

## 11. The automation ladder

Climb it in order. Each rung is justified only by having done the rung below it
by hand often enough to know what the routine actually is.

1. **By hand.** Ten scenes, full loop, manually. Learn where it hurts.
2. **Slash commands.** The repeated prompts become files in `.claude/commands/`
   (Module 00, section 9). `/szene 12`, `/kritik 12`, `/kapitelcheck 3`.
3. **Subagents.** `/agents` for `szenen-kritiker`, `leser`, `kontinuitaets-pruefer`
   — read-only, separate context windows, invoked by name.
4. **Scripts.** `tools/` for the mechanical checks in sections 5 and 10, run
   before each chapter close.
5. **Hooks.** Only once everything above is stable, and only for checks that can
   never produce a false positive.

Automating before step 1 produces a fast pipeline that generates work you throw
away.

---

## 12. Throughput

Realistic cadence for a 90,000-word book at ~1,800 words per scene, 50 scenes:

| Phase | Sessions | Note |
|---|---|---|
| Planning (Module 00, sessions 1–5) | 5–8 | Do not shorten this |
| Drafting | 50 scene loops + 50 critiques | One to three scenes per working day |
| Chapter closes | ~20 | Continuity sweep and reader critic |
| Act reviews | 3 | Structure, before prose |
| Book revision | 6 passes | Module 08, in order |

The rate limiter is not generation speed. It is the author's judgement on each
scene, and that is the correct rate limiter. A pipeline that outruns your ability
to read what it produces is producing text, not a book.

---

## Production audit

- [ ] Does every drafted scene have a complete contract in `scenes.tsv`?
- [ ] Is the bible updated after every scene, including the knowledge column?
- [ ] Is every scene committed to git separately?
- [ ] Has any drafting session written more than one scene?
- [ ] Has any critique run in the same context as the drafting?
- [ ] Does `bible/voice-anchor.md` exist, and is it loaded during drafting?
- [ ] When was the last drift check, and what did it find?
- [ ] Are there open promises older than 40 scenes?
- [ ] Does the manuscript assert anything not recorded in `facts.md`?
- [ ] Do the German blacklist counts sit inside budget?
- [ ] Has the plan been changed mid-scene at any point? (It should never be.)
