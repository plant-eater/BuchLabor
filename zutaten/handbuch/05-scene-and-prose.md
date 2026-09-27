# Module 05 — Scene craft and prose

Structure is planning. This module is where the book is actually written.

---

## Part 1 — The scene

### Definition

McKee: a scene is an action through conflict, in continuous time and space, that
**turns the value-charged condition of a character's life**.

The operative word is *turns*. A scene that does not change the charge on some
value is a non-event, however much dialogue it contains.

### The value-shift test

Before writing a scene, name the value at stake — trust, safety, love, freedom,
hope, control — and its charge at the opening. After writing, name the charge at
the close. If the two are identical, the scene does not exist. Either make it
turn or cut it and redistribute its information.

```
Scene 14 — value: trust
  Opening charge: + (she believes her partner)
  Closing charge: – (she finds the second phone)
```

### Swain's scene structure: goal → conflict → disaster

**Goal.** The POV character wants something specific in this scene, stated or
made obvious in the first paragraphs. Concrete enough that the reader can score
it.

**Conflict.** Something specifically blocks that goal, and the opposition
escalates. Escalation means new complications, not the same obstacle repeated.
Conflict tests how badly the character wants it.

**Disaster.** The scene ends with the situation altered and the character worse
positioned than the reader expected. Two shapes:

- **`No, and…`** — they fail, *and* a new problem arrives
- **`Yes, but…`** — they succeed, *but* the success creates a worse problem

A plain `yes` ends the drive. A plain `no` stalls it. Use plain outcomes rarely
and deliberately.

### The sequel

After a disaster, the character processes. This is the sequel, and it is what
makes the reader feel the scene mattered.

**Reaction → Dilemma → Decision**

- **Reaction:** emotional and physical response, immediate and involuntary
- **Dilemma:** the options, all of them bad, weighed
- **Decision:** a new goal, which becomes the next scene's goal

Sequels are the deceleration mechanism. Long sequel after a big disaster; a
single paragraph, or none, when accelerating toward a climax. Skipping every
sequel produces an exhausting book where nothing seems to cost anything.

### Motivation–Reaction Units (MRU)

Inside a scene, at sentence level, cause precedes effect. Every stimulus from
outside gets a response, in this fixed order:

1. **Motivating stimulus** (external, objectively observable)
2. **Reaction**, in this order:
   a. involuntary physical/emotional response
   b. reflex action
   c. speech or considered action

> The door came off its hinges. *(motivation)*
> Her stomach dropped. She was moving before she decided to, three steps to the
> window, and heard herself say, "Go, go —" *(reaction, in order)*

Getting the order wrong ("She ran for the window as the door came off its
hinges") reads as slightly wrong even to readers who cannot name why. In action
sequences, keep the order strict. In reflective passages, relax it.

### Scene checklist

Every scene gets a line in the scene list:

```
#  POV | Goal | Opposition | Outcome (no,and / yes,but) | Value shift | Word target
```

If any field is empty, do not write the scene.

**Style models.** Each scene also carries a `szenentyp` in `bible/scenes.tsv`. It
selects exactly one reference passage from `style/` (mapping in `style/README.md`,
values and decision rule in `style/szenentyp.md`); `/szene-varianten` loads it. The
field is not part of the contract above: if it is empty or the type has no primary
passage, write without a model and say so — never pick a passage freely.

---

## Part 2 — Dialogue

### The rule

**Characters say what serves them, not what is true.** Dialogue is action. People
in fiction use speech to get things, defend themselves, and avoid subjects.

### On-the-nose dialogue and how to fix it

On-the-nose means characters state their feelings and intentions directly.

> "You're a terrible partner. I can't do this anymore. I'm leaving you because
> your father's absence damaged you."

Three fixes:

**1. Make the conversation about what is not being said.** Give the characters a
surface topic and let the real one show through pressure.

> "You're late." She slid the box across the floor with her foot. "The rest are
> by the door."

**2. Let characters pursue different agendas.** Two people having slightly
different conversations at once produces subtext automatically. A wants to
confess; B wants to leave before the traffic.

**3. Use silence.** A pause, an action, a change of subject. Most truth in
dialogue lives in the space between the lines.

### Techniques

- **Interruption and non-answer.** People deflect, misunderstand, and answer the
  question they wish had been asked.
- **Asymmetric knowledge.** One character knows something the other does not,
  and the reader knows who knows.
- **Distinct idiolect.** Different characters have different sentence lengths,
  different registers, different filler words, and different subjects they
  return to. Test by removing all attribution and checking whether the speakers
  are still distinguishable.
- **Action beats instead of adverbs.** Replace `"Fine," she said angrily` with
  `"Fine." She put the glass down harder than she meant to.`
- **Attribution:** `said` and `asked` are invisible; use them. Exotic tags
  (*hissed, chuckled, expostulated*) draw attention to the writing.
- **Compression.** Cut greetings, small talk, and logistics. Enter the
  conversation late and leave it early.

### What dialogue must never do

Explain the plot to someone who already knows it. Deliver world-building
lectures. Have characters describe their own psychology accurately.

---

## Part 3 — Prose

### Show and tell

"Show, don't tell" is wrong as an absolute. The correct rule:

**Dramatize what matters. Summarize what connects.**

- Show: decisions, revelations, confrontations, first meetings, deaths, anything
  the reader will remember.
- Tell: journeys, routines, repeated actions, the passage of a week, the
  five-minute walk between two important scenes.

A book that shows everything is bloated. A book that tells everything is a
synopsis. The ratio is the craft.

### Concrete detail

The specific noun does more work than any adjective. *Vehicle* → *car* →
*Corolla with a cracked wing mirror*.

**Detail selection is characterisation.** What the POV character notices tells
the reader who they are. Never describe a room neutrally; describe it as this
person sees it, in this mood.

**Three details beat twelve.** Choose the odd one, the one that carries emotion,
and the one that will matter later. Delete the rest.

### Sentence rhythm

Vary sentence length deliberately. A run of same-length sentences flattens into
a drone regardless of content. Short sentences land. Long sentences, which
accumulate clauses and delay their resolution, create tension or drift depending
on where the emphasis falls.

Put the most important word at the end of the sentence, and the most important
sentence at the end of the paragraph.

### White space

Paragraph breaks control pace and emphasis. A one-line paragraph after a long one
lands like a hammer. Use it rarely so it keeps working.

---

## Part 4 — The AI prose blacklist

These are the specific failure patterns that mark machine-written fiction. Treat
this list as hard constraints during drafting and as a search list during
revision.

### Banned constructions

- **The "not just X, but Y" frame** and its variants ("It wasn't about A. It was
  about B."). Also `not merely`, `more than just`.
- **Isolated dramatic fragments** used as a beat: *Silence. A beat. And then.*
  Occasionally fine; as a tic, fatal.
- **Triads everywhere.** The rule of three applied to every list, every
  description, every emotional beat.
- **The summarising final sentence** that tells the reader what the paragraph
  meant.
- **Balanced antithesis on a schedule.** "She was not afraid of dying. She was
  afraid of being forgotten."
- **Em-dash interruption as the default rhythm.** Vary punctuation.

### Banned vocabulary in fiction

*delve, tapestry, testament to, navigate (figuratively), palpable, unspoken,
weight of (as metaphor), a mixture of X and Y, something shifted, a beat passed,
liminal, visceral, grounded, quietly (as narrator's judgement), symphony of,
dance of, whisper of, ghost of a smile, breath she didn't know she was holding,
the air was thick with, eyes that held (anything), a storm was coming*

### Banned emotional shorthand

Pounding hearts, clenched jaws, knots in stomachs, breaths caught in throats,
shivers down spines, blood running cold. These are placeholders for emotion, not
emotion. Replace each with a specific action, a distorted perception, or a
thought.

### Structural tells

- **Every scene the same length.** Vary by a factor of three or more.
- **Every chapter ending on a portentous one-liner.**
- **Symmetrical dialogue** where characters take clean turns of equal length and
  nobody interrupts, deflects, or talks past anyone.
- **Uniform competence.** Every character articulate, insightful, and
  emotionally literate. Real people are inarticulate about exactly the things
  that matter most to them.
- **Resolved endings for every thread.** Leave something ragged.
- **Overexplained metaphor.** If an image is doing thematic work, do not then
  tell the reader what it means.

### The revision pass for this

Search the manuscript for each banned item. Count occurrences. Set a budget
(zero for most, at most one per 20,000 words for the near-unavoidable ones) and
rewrite down to it. This is mechanical, and it makes an enormous difference.

---

## Scene and prose audit

- [ ] Does every scene have a named value that flips?
- [ ] Does every scene end on `no, and` or `yes, but`?
- [ ] Is there a sequel after every major disaster, and is it in proportion?
- [ ] Strip dialogue tags from the longest conversation: can you still tell who
      is speaking?
- [ ] Does any character say aloud what they should be hiding?
- [ ] Pick three descriptive passages: are they filtered through the POV
      character's mood and knowledge?
- [ ] Run the blacklist search. Count and fix.
- [ ] Read a page aloud. Where the voice stumbles, the rhythm is broken.
