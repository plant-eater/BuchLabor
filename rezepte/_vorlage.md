# Vorlage für ein Rezept — kopieren, umbenennen, ausfüllen
# Zeilen mit # sind Notizen. Leer oder "-" heisst: diese Zutat weglassen.
# Mehrere Einträge mit Komma trennen. Namen ohne .md. "*" = alle Dateien des Ordners.

aufgabe:     s01              # zutaten/aufgabe/<name>.md — Pflicht, sonst nichts
rahmen:      handwerker       # zutaten/rahmen/ — der Systemprompt (nur einer)
stil:        -                # zutaten/stil/ — Passagen, auch eigene/<name>
bibel:       -                # zutaten/bibel/ — z. B. narration, characters, facts
handbuch:    -                # zutaten/handbuch/ — ganze Module, z. B. 05-scene-and-prose
regeln:      -                # zutaten/regeln/ — Regelkarten, einzeln ein- und ausschaltbar
modelle:     opus, sonnet     # Kürzel aus modelle.txt
wiederholen: 1                # Texte pro Modell. Ab 2 siehst du, was Zufall ist
temperatur:                   # leer = Standard des Modells

---
Alles unter dem Strich geht wörtlich als Zusatz an das Modell (nach der Aufgabe).
Leer lassen, wenn es keinen Zusatz gibt.
