# Schreiblabor

Ein Ort zum Ausprobieren, nicht zum Buchschreiben. Hier findest du heraus, **welche
Zutaten die Prosa besser machen** — bevor du sie in `BuchNeu/` fest einbaust.

`BuchNeu/` bleibt, wie es ist: Bibel, Handbuch und Stilvorlagen dort sind das Original.
Das Labor arbeitet mit Kopien, die du hier beliebig ändern, kürzen oder verwerfen kannst.

---

## Die Idee in einem Bild

```
  Zutaten                 Rezept                  Lauf                     Vergleich
  ───────                 ──────                  ────                     ─────────
  rahmen/   ─┐
  stil/      │            a-wie-bisher.md         laeufe/…_a-wie-bisher/   vergleiche/…/
  bibel/     ├──────▶     b-nackt.md      ──▶     opus.md  sonnet.md  ──▶  A.md B.md C.md …
  handbuch/  │            e-vorbild-….md          gpt.md   prompt.md       vergleich.html
  regeln/    │            (was rein kommt,                                 bewertung.md
  aufgabe/  ─┘             welche Modelle)                                 → aufdecken
```

- **Zutat** — eine Datei, die im Prompt landen kann: eine Stilvorlage, ein Bibel-Kapitel,
  eine Regelkarte, ein Handbuch-Modul.
- **Rezept** — eine kurze Datei, die sagt, welche Zutaten rein kommen und welche Modelle
  schreiben. Ein Rezept ändern heisst: eine Zeile ändern.
- **Lauf** — ein Rezept, an die Modelle geschickt. Jeder Lauf bekommt einen eigenen Ordner
  mit dem genauen Prompt, damit du später weisst, was drin war.
- **Vergleich** — die Texte aus mehreren Läufen, gemischt und ohne Namen. Du liest, du
  rangierst, dann deckst du auf.

---

## Einmal einrichten (5 Minuten)

Im Terminal:

```bash
cd ~/Claude/BuchProjekt-cosyfan/Labor
python3 labor.py holen          # Bibel, 14 Stilvorlagen und Handbuch aus BuchNeu kopieren
python3 labor.py aufgabe 1      # Szenenauftrag aus scenes.tsv → zutaten/aufgabe/s01.md
python3 labor.py modelle        # zeigt, welche Modelle bereit sind
```

`holen` und `aufgabe 1` + `2` sind schon erledigt. Die Modelle `opus`, `sonnet` und `fable`
laufen über dein Claude-Abo (Befehl `claude`), ohne weiteren Schlüssel.

**Andere Modelle (GPT, Gemini, Kimi …):** Am einfachsten über [OpenRouter](https://openrouter.ai)
— ein Konto, ein Schlüssel, alle Modelle. Schlüssel eintragen:

```bash
cp schluessel.env.beispiel schluessel.env
open -e schluessel.env           # OPENROUTER_API_KEY=… eintragen
```

**Ganz ohne Schlüssel:** Modell `hand`. Das Labor legt den Prompt in die Zwischenablage,
du fügst ihn in ChatGPT, Gemini oder Le Chat ein und kopierst die Antwort in die Datei,
die das Labor dafür anlegt.

---

## Ein Experiment in vier Schritten

**1. Frage wählen, zwei Rezepte, die sich in genau einer Sache unterscheiden.**

```bash
python3 labor.py zeigen b-nackt          # Prompt ansehen, ohne zu senden → vorschau.md
```

**2. Laufen lassen.**

```bash
python3 labor.py lauf b-nackt
python3 labor.py lauf c-nur-bibel
python3 labor.py lauf b-nackt gpt,gemini      # andere Modelle, gleiches Rezept
```

**3. Blind vergleichen.**

```bash
python3 labor.py vergleich laeufe/2026-09-27_*
open vergleiche/<datum>/vergleich.html   # alle Texte nebeneinander, A, B, C …
```

Lies alle Texte, fülle `bewertung.md` aus (Rang, „würde ich weiterlesen?", Zitate).
**Nicht vorher aufdecken** — sobald du weisst, welcher Text von welchem Modell stammt,
liest du anders.

**4. Aufdecken.**

```bash
python3 labor.py aufdecken vergleiche/<datum>
```

→ `aufgedeckt.md`: welcher Text woher kam, dein Rang, mittlerer Rang je Rezept und je Modell,
dazu Kennzahlen (Satzlängen, Redeanteil, Filterverben, Blacklist-Treffer). Die Kennzahlen
sind Hygiene, kein Urteil: Ein Text kann alle Zahlen erfüllen und trotzdem tot sein.

---

## Mitgelieferte Rezepte (alle für Szene 1)

| Rezept | Rahmen | Stil | Bibel | Regeln / Handbuch | Frage dahinter |
|---|---|---|---|---|---|
| `a-wie-bisher` | Handwerker | Kafka + Zweig | 5 Dateien | 5 Regelkarten | So entstand der bisherige Text (eine statt fünf Fassungen) |
| `b-nackt` | — | — | — | — | Die Nulllinie. Was schreibt das Modell ohne alles? |
| `c-nur-bibel` | — | — | 3 Dateien | — | Hilft das Weltwissen allein? |
| `d-nur-stil` | — | Kafka | — | — | Hilft die Stilvorlage allein? |
| `e-vorbild-rauheit` | Autorin | Nell-Beispiel + Kafka | 3 Dateien | Rauheit, Deutsch, Dialog zuerst | Die fünf Hebel vom 26.09., nie getestet |
| `f-freihand` | Autorin | — | 3 Dateien | Regeln aufgehoben | Schaden die Schreibregeln? |
| `g-handbuch-voll` | Handwerker | — | 3 Dateien | Module 02, 05, 09 ganz | Ganzes Handbuch statt Auszügen? |

Dazu `laeufe/0000_referenz_s01/`: der heutige Stand von Szene 1 aus `BuchNeu`. Nimm ihn in
jeden Vergleich zu Szene 1 mit — dann siehst du, ob ein Rezept den bisherigen Text schlägt.

### Fragen und welche Rezepte sie beantworten

| Du willst wissen … | vergleiche | ändert sich nur |
|---|---|---|
| … ob die Bibel etwas bringt | `b-nackt` ↔ `c-nur-bibel` | Bibel |
| … ob die Stilvorlage etwas bringt | `b-nackt` ↔ `d-nur-stil` | Stil |
| … welche Stilvorlage besser passt | `d-nur-stil` ↔ Kopie mit anderer `stil:`-Zeile | eine Passage |
| … ob die Regeln schaden | `a-wie-bisher` ↔ `f-freihand` | Regeln + Rahmen |
| … ob der bisherige Weg überhaupt besser ist als nichts | `a-wie-bisher` ↔ `b-nackt` ↔ Referenz | alles |
| … ob die neuen Hebel wirken | `a-wie-bisher` ↔ `e-vorbild-rauheit` | Rahmen, Stil, Regeln |
| … welches Modell am besten Deutsch schreibt | ein Rezept, `lauf <rezept> opus,gpt,gemini,kimi` | Modell |

**Faustregel:** Pro Vergleich nur eine Sache ändern. Wenn A mit Bibel, Stil *und* anderen
Regeln gewinnt, weisst du nicht, woran es lag. Und ein Text pro Modell ist ein Einzelfall —
mit `wiederholen: 2` im Rezept siehst du, wie stark ein Modell mit sich selbst streut.

---

## Selbst etwas ändern

| Du willst … | so geht's |
|---|---|
| ein neues Rezept | `_vorlage.md` in `rezepte/` kopieren, umbenennen, Zeilen ändern |
| eine Stilvorlage umschreiben | Datei in `zutaten/stil/` bearbeiten — oder als Kopie mit neuem Namen |
| ein eigenes Vorbild | nach `zutaten/stil/eigene/` legen (Aufbau siehe `_LIESMICH.md` dort) |
| eine Handbuch-Regel in Frage stellen | Regelkarte in `zutaten/regeln/` ändern, oder im Rezept weglassen |
| eine neue Regel testen | neue Datei in `zutaten/regeln/`, im Rezept unter `regeln:` nennen |
| die Bibel kürzen | Kopie in `zutaten/bibel/` bearbeiten (z. B. `characters-kurz.md`) |
| den Szenenauftrag lockern | Kopie von `aufgabe/s01.md`, z. B. `aufgabe/s01-kurz.md` (liegt schon da) |
| andere Szene | `python3 labor.py aufgabe 3`, dann im Rezept `aufgabe: s03` |
| ein weiteres Modell | Zeile in `modelle.txt` |

Alles in `<!-- … -->` ist eine Notiz für dich und geht nie an das Modell.

Wenn sich in `BuchNeu/` die Bibel ändert: `python3 labor.py holen` holt nur neue Dateien.
`python3 labor.py holen --ueberschreiben` ersetzt alle Kopien — deine Änderungen daran
gehen dabei verloren.

---

## Ordner

| Ordner / Datei | Inhalt |
|---|---|
| `labor.py` | das einzige Skript, nur Python-Bordmittel |
| `modelle.txt` | Kürzel → Anbieter → Modell-ID |
| `rezepte/` | ein Rezept pro Versuchsaufbau |
| `zutaten/aufgabe/` | Szenenaufträge (aus `scenes.tsv` erzeugt, frei änderbar) |
| `zutaten/rahmen/` | Systemprompts: `handwerker` (bisher), `autorin` (Gegenentwurf) |
| `zutaten/stil/` | die 14 Passagen aus `BuchNeu/style/passagen/`, dazu `eigene/` |
| `zutaten/bibel/` | Kopie von `BuchNeu/bible/` |
| `zutaten/handbuch/` | Kopie von `BuchNeu/handbook/` |
| `zutaten/regeln/` | Regelkarten: Handbuch-Regeln einzeln zum Ein- und Ausschalten |
| `laeufe/` | ein Ordner pro Lauf: `prompt.md`, `rezept.md`, ein Text pro Modell; `protokoll.tsv` listet alle |
| `vergleiche/` | ein Ordner pro Blindvergleich |

## Was das Labor bewusst nicht tut

- Es schreibt nichts nach `BuchNeu/`. Was sich bewährt, übernimmst du von Hand.
- Es bewertet keine Texte. Die Kennzahlen zählen, du urteilst.
- Es pflegt die Bibel nicht nach. Dafür bleibt `/uebernehmen` in `BuchNeu`.
