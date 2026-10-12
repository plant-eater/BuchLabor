# Moderne Stilvorlagen – Übersicht

Dateien, die mit `_` beginnen, lädt das Labor nie. Diese hier ist nur zum Nachschlagen.

**Was hier liegt:** je Buch und Szenentyp zwei Stellen, jede als Langfassung (800–1.200 Wörter)
und als Kurzfassung (250–400 Wörter, dieselbe Stelle gekürzt). 3 Bücher × 10 Typen × 2 Stellen
= 60 Stellen, 120 Dateien. Aufbau wie `BuchNeu/style/passagen/`: Kopfteil, „Was daran übernommen
werden soll", „Was ausdrücklich nicht übernommen werden soll", Passage. Absatznummern (¶) nach
`BuchNeu/tools/norm.py` in den Quelltexten `spellshop.md`, `falling-midgard.md`,
`dungeon-crawler-carl.md`.

**Im Rezept:** `stil: modern/spellshop-verlust-1` (lang) oder `stil: modern/spellshop-verlust-1-kurz`.
Lang gegen kurz derselben Stelle ändert nur die Länge – das ist der saubere Vergleich zu Hebel 1
(Vorbild 800–1.200 Wörter) gegenüber Entscheidung S1 (250–400 Wörter).

**Was beim Vergleich zu beachten ist**

- Spellshop und Dungeon Crawler Carl sind Übersetzungen aus dem Englischen: übernehmbar ist nur die
  Technik (wie S4 für Tolstoi und Dostojewski). Falling Midgard ist deutsches Original.
- Spellshop liegt inhaltlich nah an „Die Wolke, die zu laut lacht" (Stadt verlassen, Inseldorf, Cozy).
  Das widerspricht S1 („inhaltlich fern vom eigenen Roman“) – für ein Vorbild nach Hebel 1 ist es gewollt.
- Dungeon Crawler Carl ist Ich-Erzählung mit Leseransprache; das Buch erzählt in dritter Person.
  Jede DCC-Datei sagt das unter „nicht übernehmen“.
- Zwei Langfassungen liegen unter 800 Wörtern, weil die Szene vorher endet:
  `dungeon-crawler-carl-verlust-2` (733) und `dungeon-crawler-carl-figurenbild-2` (762).
- In Falling Midgard kreuzen `eskalation-1` und `eskalation-2` einen Perspektivwechsel; die
  Kapitelüberschrift steht dort als `* * *`.
- Kurzfassungen nennen unter „übernehmen“ nur die Punkte, die im Auszug zu sehen sind.

| Szenentyp | Datei (+ `-kurz`) | Stelle | lang | kurz | Funktion |
|---|---|---|---:|---:|---|
| `kapitelanfang` | `spellshop-kapitelanfang-1` | ¶1–28 | 999 | 304 | Eine Katastrophe wird als Packproblem verwaltet: die Figur sortiert Bücher, während der Palast brennt |
| `kapitelanfang` | `spellshop-kapitelanfang-2` | ¶531–552 | 925 | 293 | Neuer Tag, neue Aufgabe: der verwilderte Garten wird mit dem Ordnungssystem der alten Arbeit erobert |
| `kapitelanfang` | `falling-midgard-kapitelanfang-1` | ¶1–12 | 807 | 381 | Ein Buch beginnt nach der Schlacht: zerstörter Garten, Schmerz im Körper, Schuld – die Lage wird über Aufräumen gesetzt |
| `kapitelanfang` | `falling-midgard-kapitelanfang-2` | ¶1575–1590 | 951 | 348 | Kapitel beginnt mitten in einer Suche: die Figur geht durch eine fremde Burg, sieht genau hin und findet nichts |
| `kapitelanfang` | `dungeon-crawler-carl-kapitelanfang-1` | ¶1–17 | 820 | 296 | Ein Weltuntergang im Protokollton: Uhrzeit, Wetter, wer tot ist – dann der Sprung zurück zur Katze im Baum |
| `kapitelanfang` | `dungeon-crawler-carl-kapitelanfang-2` | ¶1582–1610 | 811 | 286 | Ein neues Kapitel öffnet eine neue Lage über die Karte: vierzig blaue Punkte – und dann der Blick, wer sie sind |
| `figureneinfuehrung` | `spellshop-figureneinfuehrung-1` | ¶131–162 | 1053 | 284 | Die Figur tritt als Bedrohung auf und wird Satz für Satz entschärft; was sie ist, zeigt sie über Verhalten, nicht über Beschreibung |
| `figureneinfuehrung` | `spellshop-figureneinfuehrung-2` | ¶1987–2013 | 980 | 286 | Eine Fremde wird über Dritte aufgebaut: die Hauptfigur hört nur zu, das Dorf fragt sie aus, ein einziges Wort (Bibliothek) trifft |
| `figureneinfuehrung` | `falling-midgard-figureneinfuehrung-1` | ¶153–176 | 1190 | 332 | Ein Gott platzt in eine Café-Küche und wird nicht erkannt: die Einführung kippt vom Retter zum Verdächtigen |
| `figureneinfuehrung` | `falling-midgard-figureneinfuehrung-2` | ¶248–283 | 1166 | 308 | Eine verstoßene Göttin wird eingeführt über das, was ihr angetan wurde; der Besucher kommt als Bittsteller und geht als Schuldiger |
| `figureneinfuehrung` | `dungeon-crawler-carl-figureneinfuehrung-1` | ¶174–204 | 1182 | 286 | Eine Figur wird durch eine Türkette eingeführt: sie redet zu viel, hilft zu wenig und hält sich an Regeln, während draußen gekämpft wird |
| `figureneinfuehrung` | `dungeon-crawler-carl-figureneinfuehrung-2` | ¶568–600 | 833 | 308 | Eine Katze spricht zum ersten Mal – und ist sofort eine fertige Figur: Titel, Herablassung, Forderungen |
| `konfliktgespraech` | `spellshop-konfliktgespraech-1` | ¶496–529 | 1112 | 307 | Zwei verhandeln Hilfe und Schuld; das eigentliche Thema – die versteckten Bücher – fällt nie |
| `konfliktgespraech` | `spellshop-konfliktgespraech-2` | ¶3290–3328 | 1106 | 362 | Verhör als Höflichkeit: beide wissen, dass gelogen wird, keiner sagt es; das Gespräch über eine Dritte meint die Sprecherin |
| `konfliktgespraech` | `falling-midgard-konfliktgespraech-1` | ¶31–63 | 801 | 304 | Ein Gärtner prüft einen Gott: beide wissen, dass der andere mehr ist, als er zeigt; das eigentliche Thema – wer Aaron ist und ob Runa die Hüterin ist – kommt nur in Andeutungen |
| `konfliktgespraech` | `falling-midgard-konfliktgespraech-2` | ¶100–120 | 825 | 288 | Frühstück zu dritt: die Eltern wissen etwas, die Tochter weiss etwas anderes nicht – gestritten wird über Café und Archiv |
| `konfliktgespraech` | `dungeon-crawler-carl-konfliktgespraech-1` | ¶633–661 | 1026 | 389 | Ein Mann will die Katze verlassen; die Katze lenkt ein und trifft ihn mit dem, was er sich selbst nicht eingestanden hat |
| `konfliktgespraech` | `dungeon-crawler-carl-konfliktgespraech-2` | ¶1430–1462 | 1141 | 306 | Ein Fremder erzählt eine Geschichte, die Hauptfigur hört zu und prüft jedes Detail – das Gespräch ist eine Falle in beide Richtungen |
| `innere-passage` | `spellshop-innere-passage-1` | ¶587–610 | 866 | 307 | Eine Erinnerung korrigiert sich am Ort: der Tümpel liegt näher, als das Kind glaubte – die Eltern wussten es immer |
| `innere-passage` | `spellshop-innere-passage-2` | ¶2015–2032 | 920 | 311 | Die Figur will arbeiten und kann nicht: die Gedanken kehren in kurzen Absätzen immer zum selben Mann zurück |
| `innere-passage` | `falling-midgard-innere-passage-1` | ¶94–98 | 812 | 252 | Aufwachen mit Kopfschmerz: Traumfetzen, ein fremdes Wort, das eigene Leben fühlt sich falsch an |
| `innere-passage` | `falling-midgard-innere-passage-2` | ¶709–711 | 1076 | 298 | Allein im Keller: Ordnung lesen, eine Lücke bemerken, eine verborgene Tür finden – Vernunft und Neugier verhandeln, die Hand entscheidet |
| `innere-passage` | `dungeon-crawler-carl-innere-passage-1` | ¶1531–1550 | 831 | 327 | Stunden auf dem Gefährt: Gedanken über eine Falle, einen Vater, der lachen würde, und die Regel, dass Tempo blind macht |
| `innere-passage` | `dungeon-crawler-carl-innere-passage-2` | ¶1945–1960 | 802 | 282 | Mitten im Bosskampf eine Kindheitserinnerung: der Laster unter der Brücke, der Vater fährt weiter |
| `eskalation` | `spellshop-eskalation-1` | ¶553–583 | 1076 | 326 | Not führt zu einem verbotenen Entschluss; die Figur redet sich Schritt für Schritt aus dem Gesetz heraus |
| `eskalation` | `spellshop-eskalation-2` | ¶3404–3441 | 967 | 289 | Im Sturm entscheidet die Hauptfigur gegen alle Einwände, den Feind zu retten; die Lage zieht sich zu, bis nur noch ein unmöglicher Weg bleibt |
| `eskalation` | `falling-midgard-eskalation-1` | ¶1604–1630 | 1134 | 294 | Eine harmlose Heimfahrt kippt: Aufprall, rote Augen, Graben, Glas – und der Perspektivwechsel zum Retter |
| `eskalation` | `falling-midgard-eskalation-2` | ¶3131–3165 | 1019 | 332 | Vor dem Zweikampf fordert die Mutter des Gegners Fairness; der Held gibt seinen Kraftgürtel ab – ein Entschluss, der nicht zurückzunehmen ist |
| `eskalation` | `dungeon-crawler-carl-eskalation-1` | ¶1462–1491 | 1021 | 295 | Der Hinterhalt fällt, das System friert die Täter ein – und die Katze sagt den Satz, der die Flucht zur Entscheidung macht |
| `eskalation` | `dungeon-crawler-carl-eskalation-2` | ¶3662–3699 | 994 | 297 | Vor dem Bossraum: kranke Hunde in Käfigen, Jubel hinter der Tür – die Hauptfigur begreift, rennt los, und alles friert ein |
| `schauplatzwechsel` | `spellshop-schauplatzwechsel-1` | ¶89–121 | 1090 | 282 | Ankunft am verfallenen Elternhaus: Steg, Treppe, Cottage – der Ort erzeugt das Zögern der Figur |
| `schauplatzwechsel` | `spellshop-schauplatzwechsel-2` | ¶319–335 | 1047 | 341 | Der Weg ins Dorf: von der Klippe sieht alles schön aus, aus der Nähe ist es heruntergekommen |
| `schauplatzwechsel` | `falling-midgard-schauplatzwechsel-1` | ¶509–520 | 820 | 389 | Erstes Betreten des geerbten Hauses: vertraut ohne Erinnerung, aufgeräumt nach einem Kampf, ein Geruch aus den Träumen |
| `schauplatzwechsel` | `falling-midgard-schauplatzwechsel-2` | ¶3119–3131 | 841 | 307 | Odins Halle als Arena: Sand, Tribünen, gefesselte Götter am Thron – der Ort zeigt die Machtverhältnisse, bevor jemand spricht |
| `schauplatzwechsel` | `dungeon-crawler-carl-schauplatzwechsel-1` | ¶82–110 | 850 | 313 | Die Treppe hinab in den Dungeon: Wärme nach dem Frost, Muster, die Fische oder Dämonen sind, ein Tor, das sich hinter ihm schliesst |
| `schauplatzwechsel` | `dungeon-crawler-carl-schauplatzwechsel-2` | ¶2220–2250 | 905 | 304 | Ankunft auf der zweiten Ebene: weisser Boden, orange Flechten, Ziegel statt Fels – und die Sorge, dass Ruhm schadet |
| `verlust` | `spellshop-verlust-1` | ¶197–226 | 873 | 281 | Die Nachwirkung der Flucht kommt beim Waschen: Ruß im Handtuch |
| `verlust` | `spellshop-verlust-2` | ¶274–307 | 906 | 284 | Ein Herdfeuer ruft die brennende Stadt zurück; die Figur löscht und atmet, bis die Gegenwart wieder trägt |
| `verlust` | `falling-midgard-verlust-1` | ¶301–311 | 1113 | 347 | Eine Akte auf dem Schreibtisch: adoptiert, leibliche Eltern tot – der Verlust kommt im Nachhinein und trifft trotzdem |
| `verlust` | `falling-midgard-verlust-2` | ¶999–1005 | 1073 | 274 | Eine Kiste »Für Runa«: Babyschuhe, Zeitungsausschnitte vom Unfall, ein Jahrbuchfoto – Trauer um Eltern, die sie nie kannte |
| `verlust` | `dungeon-crawler-carl-verlust-1` | ¶1630–1651 | 1142 | 287 | Ein Pfleger erzählt, wer nicht mehr da ist; die Hauptfigur sieht die Totenköpfe neben einem Namen und fragt nicht weiter |
| `verlust` | `dungeon-crawler-carl-verlust-2` | ¶35–57 | 733 | 323 | Das Haus verschwindet, ein Kopf liegt neben dem Fuss – und erst dann begreift er, dass in den Gebäuden Menschen waren |
| `kapitelschluss` | `spellshop-kapitelschluss-1` | ¶57–82 | 947 | 290 | Ein Kapitel endet mit Entschluss und Witz: das Ziel ist gesetzt, die letzte Replik nimmt der Lage den Ernst, nicht das Gewicht |
| `kapitelschluss` | `spellshop-kapitelschluss-2` | ¶600–634 | 1166 | 318 | Ein Kapitel endet mitten im Warten: der Zauber ist gesprochen, das Ergebnis offen, da ruft jemand vor dem Haus |
| `kapitelschluss` | `falling-midgard-kapitelschluss-1` | ¶70–92 | 895 | 297 | Kapitelende mit Gegenbefehl: der Alb sagt »tu nichts«, der Gott nimmt seinen Hammer und beschliesst, da zu sein |
| `kapitelschluss` | `falling-midgard-kapitelschluss-2` | ¶455–483 | 804 | 286 | Kapitelende nach einem Spiel: Fake-Kuss vor den Eltern, ein Zwerg auf dem Beifahrersitz, eine Wange, die kribbelt |
| `kapitelschluss` | `dungeon-crawler-carl-kapitelschluss-1` | ¶58–79 | 853 | 310 | Ein Kapitel endet nach einer Behördenansage über das Ende der Welt mit einem einfachen Satz: zum Licht, rennen |
| `kapitelschluss` | `dungeon-crawler-carl-kapitelschluss-2` | ¶540–566 | 869 | 345 | Ein Kapitel endet mit einer fremden Stimme, die die Hose bemängelt – es ist die Katze |
| `figurenbild` | `spellshop-figurenbild-1` | ¶43–62 | 856 | 285 | Die Figur erklärt sich: sie mag Menschen, nur Bücher lieber – der Text zeigt, dass sie seit Wochen mit niemandem gesprochen hat |
| `figurenbild` | `spellshop-figurenbild-2` | ¶173–196 | 1007 | 399 | Die Figur sieht das verwahrloste Haus und erkennt sich darin, redet die Erkenntnis aber sofort klein |
| `figurenbild` | `falling-midgard-figurenbild-1` | ¶18–30 | 981 | 354 | Der Gott hält sich für ehrenhaft, nicht für feige – und hält einen blinden Racheplan für seinen besten |
| `figurenbild` | `falling-midgard-figurenbild-2` | ¶555–576 | 869 | 300 | Ein Mann ärgert sich über die Vertrautheit zweier anderer und weiss nicht, warum – der Leser weiss es |
| `figurenbild` | `dungeon-crawler-carl-figurenbild-1` | ¶1505–1529 | 1002 | 295 | Der Mann durchschaut einen Fremden in Sekunden – die Katze fragt, warum er bei seiner Freundin nichts gemerkt hat |
| `figurenbild` | `dungeon-crawler-carl-figurenbild-2` | ¶18–34 | 762 | 336 | Er mag kein Drama und ist kein Arschloch – sagt er, während er aus Trotz in der Wohnung raucht und in Crocs der Ex hinausrennt |
| `stimmen` | `spellshop-stimmen-1` | ¶346–378 | 1091 | 287 | Erster Auftritt im Dorf: viele Stimmen reden über die Hauptfigur, nicht mit ihr; Erinnerung, Misstrauen und Wohlwollen überbieten sich |
| `stimmen` | `spellshop-stimmen-2` | ¶2285–2313 | 1012 | 289 | Ein Wunder am Brunnen wird zum Tribunal: eine Stimme klagt an, die Menge schwankt, eine zeigt auf die Hauptfigur, eine andere schlägt zurück |
| `stimmen` | `falling-midgard-stimmen-1` | ¶944–980 | 1040 | 325 | Ein Pubtisch, an dem Geheimnisse herausplatzen: Loki lebt, ein Antrag von vor zweihundert Jahren, Segen erbeten – die Fremde versteht die Hälfte |
| `stimmen` | `falling-midgard-stimmen-2` | ¶2954–2973 | 809 | 287 | Ein Kriegsrat gegen den Feldherrn: er hat entschieden, die Walküren widersprechen von allen Tischen, bis er auf den Tisch schlägt und nachgibt |
| `stimmen` | `dungeon-crawler-carl-stimmen-1` | ¶2116–2151 | 997 | 308 | Eine Talkshow im All: die Moderatorin fragt, die Katze spielt das Publikum, die Menge brüllt, der Mann soll seinen Slogan sagen |
| `stimmen` | `dungeon-crawler-carl-stimmen-2` | ¶3350–3382 | 1093 | 298 | Eine Show namens Death Watch: die Menge skandiert, der Moderator verhöhnt zwei Gäste, bis die Hauptfigur aufsteht und geht |
