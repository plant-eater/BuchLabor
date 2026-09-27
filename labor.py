#!/usr/bin/env python3
"""Schreiblabor — Szenen mit verschiedenen Zutaten und Modellen erzeugen und blind vergleichen.

Nur Python-Standardbibliothek (läuft mit dem python3 von macOS, ab 3.9).
Aufruf ohne Argumente zeigt die Hilfe.
"""

import datetime
import glob
import html
import json
import os
import random
import re
import shutil
import statistics
import subprocess
import sys
import time
import urllib.error
import urllib.request

LABOR = os.path.dirname(os.path.abspath(__file__))
BUCH = os.path.normpath(os.path.join(LABOR, "..", "BuchNeu"))
ZUTATEN = os.path.join(LABOR, "zutaten")
REZEPTE = os.path.join(LABOR, "rezepte")
LAEUFE = os.path.join(LABOR, "laeufe")
VERGLEICHE = os.path.join(LABOR, "vergleiche")
MARKER = "<!-- HIER DIE ANTWORT EINFÜGEN -->"

# Welche Rezept-Zeile welchen Zutatenordner meint, in der Reihenfolge, in der
# die Zutaten im Prompt landen. Die Aufgabe steht immer zuletzt.
BLOECKE = [
    ("stil", "stil", "stilvorlage"),
    ("bibel", "bibel", "bibel"),
    ("handbuch", "handbuch", "handbuch"),
    ("regeln", "regeln", "regel"),
]

HILFE = """Schreiblabor — Befehle

  python3 labor.py holen [--ueberschreiben]   Bibel, Stilvorlagen, Handbuch aus ../BuchNeu kopieren
  python3 labor.py aufgabe <nr>               Szenenauftrag aus ../BuchNeu/bible/scenes.tsv anlegen
  python3 labor.py zeigen <rezept>            Prompt bauen, nichts senden -> vorschau.md
  python3 labor.py lauf <rezept> [modelle]    Prompt an die Modelle senden -> laeufe/<datum>_<rezept>/
  python3 labor.py vergleich <lauf>...        Texte anonymisieren -> vergleiche/<datum>/
  python3 labor.py aufdecken <vergleich>      Zuordnung und Kennzahlen zeigen -> aufgedeckt.md
  python3 labor.py messen <datei>...          Kennzahlen einzelner Texte
  python3 labor.py modelle                    Modelle und fehlende Schlüssel anzeigen

<rezept> = Dateiname in rezepte/ (mit oder ohne .md). [modelle] = Kürzel aus modelle.txt,
mit Komma getrennt; überschreibt die Zeile 'modelle:' im Rezept.
Ausführlich: LIESMICH.md
"""


# --------------------------------------------------------------------------- Hilfen

def fehler(text):
    sys.exit("Fehler: " + text)


def lesen(pfad):
    with open(pfad, encoding="utf-8") as f:
        return f.read()


def schreiben(pfad, text):
    os.makedirs(os.path.dirname(pfad), exist_ok=True)
    with open(pfad, "w", encoding="utf-8") as f:
        f.write(text)


def wortzahl(text):
    return len(re.findall(r"\w+", text))


def rel(pfad):
    return os.path.relpath(pfad, LABOR)


def frontmatter(text):
    """Trennt einen ---Block am Dateianfang ab. Gibt (dict, rest) zurück."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.S)
    if not m:
        return {}, text
    werte = {}
    for zeile in m.group(1).splitlines():
        if ":" in zeile:
            k, v = zeile.split(":", 1)
            werte[k.strip()] = v.strip().strip('"')
    return werte, text[m.end():]


def ohne_kommentare(text):
    """HTML-Kommentare sind Notizen für dich und gehen nie an das Modell."""
    return re.sub(r"<!--.*?-->\s*", "", text, flags=re.S).strip()


def zutat(text):
    return ohne_kommentare(frontmatter(text)[1])


def schluessel_laden():
    pfad = os.path.join(LABOR, "schluessel.env")
    if not os.path.exists(pfad):
        return
    for zeile in lesen(pfad).splitlines():
        zeile = zeile.strip()
        if zeile and not zeile.startswith("#") and "=" in zeile:
            k, v = zeile.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"'))


# --------------------------------------------------------------------------- Rezept

def rezept_pfad(name):
    for p in (name, os.path.join(REZEPTE, name), os.path.join(REZEPTE, name + ".md")):
        if os.path.isfile(p):
            return os.path.abspath(p)
    fehler("Rezept nicht gefunden: %s (gesucht in rezepte/)" % name)


def liste(wert):
    wert = (wert or "").strip()
    if wert in ("", "-", "nein", "keine", "kein"):
        return []
    return [w.strip() for w in wert.split(",") if w.strip()]


def rezept_lesen(pfad):
    """Kopf: 'schluessel: wert'-Zeilen bis zur Zeile '---'. Danach: freier Zusatz."""
    kopf, _, zusatz = lesen(pfad).partition("\n---")
    r = {"name": os.path.splitext(os.path.basename(pfad))[0], "pfad": pfad}
    for zeile in kopf.splitlines():
        zeile = zeile.strip()
        if not zeile or zeile.startswith("#") or ":" not in zeile:
            continue
        k, v = zeile.split(":", 1)
        r[k.strip().lower()] = re.split(r"\s+#", " " + v)[0].strip()
    r["zusatz"] = ohne_kommentare(zusatz.lstrip("-\n"))
    if not r.get("aufgabe"):
        fehler("Das Rezept %s hat keine Zeile 'aufgabe:'." % rel(pfad))
    return r


def zutaten_dateien(ordner, eintraege):
    """'*' = alle Dateien des Ordners; sonst Namen ohne .md, Unterordner erlaubt."""
    basis = os.path.join(ZUTATEN, ordner)
    dateien = []
    for e in eintraege:
        if e == "*":
            dateien += sorted(p for p in glob.glob(os.path.join(basis, "*.md"))
                              if not os.path.basename(p).startswith("_"))
            continue
        p = os.path.join(basis, e if e.endswith(".md") else e + ".md")
        if not os.path.isfile(p):
            fehler("Zutat fehlt: %s" % rel(p))
        dateien.append(p)
    return dateien


def stil_block(pfad):
    fm, rest = frontmatter(lesen(pfad))
    kopf = []
    if fm.get("autor"):
        kopf.append("Vorlage: %s — %s" % (fm.get("autor"), fm.get("quelle", "")))
    if fm.get("funktion"):
        kopf.append("Funktion: " + fm["funktion"])
    return ("\n".join(kopf) + "\n\n" + ohne_kommentare(rest)).strip()


def prompt_bauen(r):
    teile, inventar = [], []
    for schluessel, ordner, tag in BLOECKE:
        for p in zutaten_dateien(ordner, liste(r.get(schluessel))):
            name = os.path.splitext(os.path.relpath(p, os.path.join(ZUTATEN, ordner)))[0]
            inhalt = stil_block(p) if ordner == "stil" else zutat(lesen(p))
            teile.append('<%s name="%s">\n%s\n</%s>' % (tag, name, inhalt, tag))
            inventar.append("%s/%s" % (ordner, name))
    aufgabe = zutaten_dateien("aufgabe", [r["aufgabe"]])[0]
    teile.append("<aufgabe>\n%s\n</aufgabe>" % zutat(lesen(aufgabe)))
    if r["zusatz"]:
        teile.append("<zusatz>\n%s\n</zusatz>" % r["zusatz"])
    rahmen = liste(r.get("rahmen"))
    system = zutat(lesen(zutaten_dateien("rahmen", rahmen[:1])[0])) if rahmen else ""
    return system, "\n\n".join(teile), inventar


def prompt_als_text(system, user):
    return "# SYSTEM\n\n%s\n\n# NACHRICHT\n\n%s\n" % (system or "(kein Rahmen)", user)


# --------------------------------------------------------------------------- Modelle

def modelle_lesen():
    pfad = os.path.join(LABOR, "modelle.txt")
    m = {}
    for zeile in lesen(pfad).splitlines():
        zeile = zeile.split("#")[0].strip()
        if not zeile:
            continue
        teile = zeile.split()
        if len(teile) < 3:
            fehler("modelle.txt, Zeile unvollständig: " + zeile)
        m[teile[0]] = {"kuerzel": teile[0], "anbieter": teile[1], "id": teile[2]}
    return m


SCHLUESSEL = {
    "anthropic": "ANTHROPIC_API_KEY",
    "openai": "OPENAI_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
    "google": "GEMINI_API_KEY",
}


def http_json(url, daten, kopf):
    anfrage = urllib.request.Request(url, data=json.dumps(daten).encode("utf-8"),
                                     headers=dict({"Content-Type": "application/json"}, **kopf))
    try:
        with urllib.request.urlopen(anfrage, timeout=900) as antwort:
            return json.loads(antwort.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError("HTTP %s: %s" % (e.code, e.read().decode("utf-8", "replace")[:600]))


def senden(modell, system, user, temperatur):
    a, mid = modell["anbieter"], modell["id"]
    key = os.environ.get(SCHLUESSEL.get(a, ""), "")
    if a in SCHLUESSEL and not key:
        raise RuntimeError("%s fehlt (in schluessel.env eintragen)" % SCHLUESSEL[a])

    if a == "claude-code":
        return claude_code(mid, system, user)

    if a == "anthropic":
        daten = {"model": mid, "max_tokens": 16000, "messages": [{"role": "user", "content": user}]}
        if system:
            daten["system"] = system
        if temperatur is not None:
            daten["temperature"] = temperatur
        antwort = http_json("https://api.anthropic.com/v1/messages", daten,
                            {"x-api-key": key, "anthropic-version": "2023-06-01"})
        return "".join(b.get("text", "") for b in antwort["content"] if b.get("type") == "text")

    if a in ("openai", "openrouter", "ollama"):
        nachrichten = ([{"role": "system", "content": system}] if system else []) + \
                      [{"role": "user", "content": user}]
        daten = {"model": mid, "messages": nachrichten}
        if a == "ollama":
            daten["stream"] = False
            if temperatur is not None:
                daten["options"] = {"temperature": temperatur}
            antwort = http_json("http://localhost:11434/api/chat", daten, {})
            return antwort["message"]["content"]
        if temperatur is not None:
            daten["temperature"] = temperatur
        url = {"openai": "https://api.openai.com/v1/chat/completions",
               "openrouter": "https://openrouter.ai/api/v1/chat/completions"}[a]
        antwort = http_json(url, daten, {"Authorization": "Bearer " + key})
        return antwort["choices"][0]["message"]["content"]

    if a == "google":
        daten = {"contents": [{"role": "user", "parts": [{"text": user}]}]}
        if system:
            daten["systemInstruction"] = {"parts": [{"text": system}]}
        if temperatur is not None:
            daten["generationConfig"] = {"temperature": temperatur}
        url = ("https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent?key=%s"
               % (mid, key))
        antwort = http_json(url, daten, {})
        return "".join(p.get("text", "") for p in antwort["candidates"][0]["content"]["parts"])

    raise RuntimeError("unbekannter Anbieter '%s' in modelle.txt" % a)


def claude_code(mid, system, user):
    """Claude Code im Druckmodus, mit deinem Abo, ohne API-Schlüssel.
    Eigener Systemprompt statt des Programmier-Prompts von Claude Code, keine Werkzeuge.
    Kennt die installierte Version eine Option nicht, wird ohne sie wiederholt."""
    if not shutil.which("claude"):
        raise RuntimeError("Befehl 'claude' nicht gefunden")
    versuche = [
        ["claude", "-p", "--model", mid, "--tools", "", "--system-prompt", system or " "],
        ["claude", "-p", "--model", mid, "--system-prompt", system or " "],
        ["claude", "-p", "--model", mid],
    ]
    letzter = ""
    for i, befehl in enumerate(versuche):
        eingabe = user if "--system-prompt" in befehl or not system else system + "\n\n" + user
        p = subprocess.run(befehl, input=eingabe, capture_output=True, text=True,
                           timeout=900, cwd=os.path.expanduser("~"))
        if p.returncode == 0 and p.stdout.strip():
            return p.stdout
        letzter = (p.stderr or p.stdout).strip()
        if not re.search(r"unknown option|unrecognized|error: option", letzter, re.I):
            break
    raise RuntimeError("claude -p: " + letzter[:600])


# --------------------------------------------------------------------------- Befehle

def cmd_holen(args):
    ueber = "--ueberschreiben" in args
    if not os.path.isdir(BUCH):
        fehler("../BuchNeu nicht gefunden (%s)" % BUCH)
    quellen = [("bible", "*.md", "bibel"), ("style/passagen", "*.md", "stil"),
               ("handbook", "*.md", "handbuch")]
    for von, muster, nach in quellen:
        neu, alt = 0, 0
        for q in sorted(glob.glob(os.path.join(BUCH, von, muster))):
            ziel = os.path.join(ZUTATEN, nach, os.path.basename(q))
            if os.path.exists(ziel) and not ueber:
                alt += 1
                continue
            os.makedirs(os.path.dirname(ziel), exist_ok=True)
            shutil.copy2(q, ziel)
            neu += 1
        print("%-10s %2d kopiert, %2d schon da (unverändert)" % (nach, neu, alt))
    if not ueber:
        print("Geänderte Kopien bleiben erhalten. Neu holen: python3 labor.py holen --ueberschreiben")


def cmd_aufgabe(args):
    if not args:
        fehler("Szenennummer fehlt: python3 labor.py aufgabe 3")
    nr = args[0].lstrip("sS").lstrip("0") or "0"
    tsv = os.path.join(BUCH, "bible", "scenes.tsv")
    zeilen = [z.split("\t") for z in lesen(tsv).splitlines() if z.strip()]
    kopf = zeilen[0]
    zeile = next((dict(zip(kopf, z)) for z in zeilen[1:] if z[0].strip() == nr), None)
    if not zeile:
        fehler("Szene %s steht nicht in scenes.tsv" % nr)
    ziel = os.path.join(ZUTATEN, "aufgabe", "s%02d.md" % int(nr))
    if os.path.exists(ziel):
        fehler("%s gibt es schon. Löschen oder umbenennen, dann neu anlegen." % rel(ziel))
    offen = [k for k, v in zeile.items() if "[offen" in v]
    anschluss = ""
    vorher = glob.glob(os.path.join(BUCH, "manuscript", "ch*", "s%02d-*.md" % (int(nr) - 1)))
    if vorher:
        woerter = re.sub(r"^# .*\n", "", lesen(vorher[0])).split()
        anschluss = ("\n## Anschluss\n\nSo endet die vorige Szene (letzte 150 Wörter):\n\n> %s\n"
                     % " ".join(woerter[-150:]))
    text = """<!-- Erzeugt aus BuchNeu/bible/scenes.tsv, Zeile %(nr)s, am %(datum)s.
     Frei bearbeitbar: Die Kopie im Labor gehört dir, das Original bleibt unberührt. -->

# Szene %(nr)s

Schreibe Szene %(nr)s des Romans „Die Wolke, die zu laut lacht" (Cozy Fantasy, deutsch).

- Perspektive: %(pov)s
- Was %(pov)s in der Szene erreichen will: %(ziel)s
- Was dagegen steht: %(opposition)s
- Wie es ausgeht: %(ausgang)s
- Was sich ändert: %(wertwechsel)s
- Frage, die am Ende offen bleibt (nicht beantworten, nicht aussprechen): %(frage)s
- Stelle im Plot: %(beat)s
- Länge: etwa %(wortziel)s Wörter
%(anschluss)s
Gib nur den Szenentext aus: kein Titel, keine Einleitung, kein Kommentar.
""" % dict(zeile, nr=nr, datum=datetime.date.today().isoformat(), anschluss=anschluss)
    schreiben(ziel, text)
    print("angelegt: " + rel(ziel))
    if offen:
        print("Achtung, noch offen in scenes.tsv: " + ", ".join(offen))


def cmd_zeigen(args):
    if not args:
        fehler("Rezept fehlt: python3 labor.py zeigen b-nackt")
    r = rezept_lesen(rezept_pfad(args[0]))
    system, user, inventar = prompt_bauen(r)
    ziel = os.path.join(LABOR, "vorschau.md")
    schreiben(ziel, prompt_als_text(system, user))
    w = wortzahl(system + " " + user)
    print("Rezept %s · Aufgabe %s · %d Wörter Prompt (~%d Tokens)" % (r["name"], r["aufgabe"], w, w * 1.6))
    print("Zutaten: " + (", ".join(inventar) or "keine"))
    print("Rahmen:  " + (r.get("rahmen") or "keiner"))
    print("-> " + rel(ziel))


def cmd_lauf(args):
    if not args:
        fehler("Rezept fehlt: python3 labor.py lauf b-nackt [opus,gpt]")
    schluessel_laden()
    r = rezept_lesen(rezept_pfad(args[0]))
    alle = modelle_lesen()
    wahl = liste(args[1] if len(args) > 1 else r.get("modelle") or "hand")
    unbekannt = [k for k in wahl if k not in alle]
    if unbekannt:
        fehler("unbekannte Modelle: %s (siehe modelle.txt)" % ", ".join(unbekannt))
    n = int(r.get("wiederholen") or 1)
    temp = float(r["temperatur"]) if r.get("temperatur") else None
    system, user, inventar = prompt_bauen(r)

    stempel = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    ordner = os.path.join(LAEUFE, "%s_%s" % (stempel, r["name"]))
    while os.path.exists(ordner):
        ordner += "b"
    schreiben(os.path.join(ordner, "prompt.md"), prompt_als_text(system, user))
    shutil.copy2(r["pfad"], os.path.join(ordner, "rezept.md"))

    print("Lauf %s · %d Modell(e) × %d" % (rel(ordner), len(wahl), n))
    for k in wahl:
        for i in range(1, n + 1):
            name = k if n == 1 else "%s-%d" % (k, i)
            ziel = os.path.join(ordner, name + ".md")
            kopf = "---\nmodell: \"%s\"\nanbieter: \"%s\"\nmodell_id: \"%s\"\nrezept: \"%s\"\naufgabe: \"%s\"\n" % (
                k, alle[k]["anbieter"], alle[k]["id"], r["name"], r["aufgabe"])
            if alle[k]["anbieter"] == "manuell":
                schreiben(ziel, kopf + "---\n\n" + MARKER + "\n")
                print("  %-12s von Hand: prompt.md in einen Chat kopieren, Antwort in %s einfügen"
                      % (name, rel(ziel)))
                kopiere_in_zwischenablage(prompt_als_text(system, user))
                continue
            print("  %-12s läuft …" % name, end="", flush=True)
            t0 = time.time()
            try:
                text = senden(alle[k], system, user, temp).strip()
            except Exception as e:  # ein Modell darf ausfallen, die anderen laufen weiter
                print(" Fehler: %s" % e)
                continue
            dauer = time.time() - t0
            woerter = wortzahl(text)
            schreiben(ziel, kopf + "dauer_s: %d\nwoerter: %d\n---\n\n%s\n" % (dauer, woerter, text))
            print(" %d Wörter, %d s" % (woerter, dauer))

    protokoll = os.path.join(LAEUFE, "protokoll.tsv")
    neu = not os.path.exists(protokoll)
    with open(protokoll, "a", encoding="utf-8") as f:
        if neu:
            f.write("lauf\trezept\taufgabe\trahmen\tzutaten\tmodelle\twiederholen\n")
        f.write("\t".join([os.path.basename(ordner), r["name"], r["aufgabe"], r.get("rahmen") or "-",
                           " ".join(inventar) or "-", ",".join(wahl), str(n)]) + "\n")
    print("Nächster Schritt: python3 labor.py vergleich %s [weitere Läufe]" % rel(ordner))


def kopiere_in_zwischenablage(text):
    if shutil.which("pbcopy"):
        subprocess.run(["pbcopy"], input=text, text=True)
        print("               (Prompt liegt in der Zwischenablage)")


def texte_sammeln(pfade):
    texte = []
    for p in pfade:
        dateien = [p] if os.path.isfile(p) else sorted(glob.glob(os.path.join(p, "*.md")))
        for d in dateien:
            if os.path.basename(d) in ("prompt.md", "rezept.md"):
                continue
            roh = lesen(d)
            if MARKER in roh:
                print("übersprungen (noch leer): " + rel(d))
                continue
            fm, text = frontmatter(roh)
            if not text.strip():
                continue
            texte.append({
                "datei": rel(d),
                "modell": fm.get("modell", os.path.splitext(os.path.basename(d))[0]),
                "rezept": fm.get("rezept", os.path.basename(os.path.dirname(d))),
                "aufgabe": fm.get("aufgabe", "?"),
                "text": text.strip(),
            })
    return texte


def buchstaben(i):
    s = ""
    i += 1
    while i:
        i, rest = divmod(i - 1, 26)
        s = chr(65 + rest) + s
    return s


def cmd_vergleich(args):
    if not args:
        fehler("Welche Läufe? python3 labor.py vergleich laeufe/<lauf1> laeufe/<lauf2>")
    pfade = []
    for a in args:
        treffer = glob.glob(a) or glob.glob(os.path.join(LABOR, a))
        if not treffer:
            fehler("nicht gefunden: " + a)
        pfade += treffer
    texte = texte_sammeln(pfade)
    if len(texte) < 2:
        fehler("Zum Vergleichen braucht es mindestens zwei fertige Texte (gefunden: %d)." % len(texte))
    random.shuffle(texte)
    stempel = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    ordner = os.path.join(VERGLEICHE, stempel)
    while os.path.exists(ordner):
        ordner += "b"
    for i, t in enumerate(texte):
        t["label"] = buchstaben(i)
        schreiben(os.path.join(ordner, t["label"] + ".md"), t["text"] + "\n")
    schreiben(os.path.join(ordner, ".schluessel.json"),
              json.dumps([{k: t[k] for k in ("label", "datei", "modell", "rezept", "aufgabe")}
                          for t in texte], ensure_ascii=False, indent=1))
    aufgaben = sorted(set(t["aufgabe"] for t in texte))
    zeilen = "\n".join("| %s |  |  |  |  |  |  |  |" % t["label"] for t in texte)
    warnung = ("\n> **Achtung:** Hier sind verschiedene Aufgaben gemischt (%s). Der Vergleich misst "
               "dann auch die Szene, nicht nur das Rezept.\n" % ", ".join(aufgaben)) if len(aufgaben) > 1 else ""
    schreiben(os.path.join(ordner, "bewertung.md"), """# Bewertung — %s

%d Texte, Aufgabe %s. Wer welchen Text geschrieben hat, steht in `.schluessel.json` —
**nicht öffnen.** Erst lesen (`vergleich.html` oder die Einzeldateien), dann diese Tabelle
ausfüllen, dann aufdecken:

    python3 labor.py aufdecken %s
%s
**Rang:** 1 = bester. Jeder Rang nur einmal. **Skalen:** 1 (schwach) bis 5 (stark).

| Text | Rang | Lese ich weiter? (ja/nein) | Klingt wie echtes Deutsch (1–5) | Eigene Stimme (1–5) | Szene erfüllt (ja/teils/nein) | Beste Stelle (Zitat) | Schwächste Stelle (Zitat) |
|---|---|---|---|---|---|---|---|
%s

## Notizen

- Was hatten die besten Texte gemeinsam?
- Was hat mich bei den schwächsten zuerst gestört?
""" % (stempel, len(texte), ", ".join(aufgaben), rel(ordner), warnung, zeilen))
    html_seite(ordner, texte, stempel)
    print("%d Texte anonymisiert -> %s" % (len(texte), rel(ordner)))
    print("Lesen: %s/vergleich.html · Bewerten: %s/bewertung.md" % (rel(ordner), rel(ordner)))


def html_seite(ordner, texte, titel):
    spalten = []
    for t in texte:
        absaetze = "".join("<p>%s</p>" % html.escape(a).replace("\n", "<br>")
                           for a in re.split(r"\n\s*\n", t["text"]) if a.strip())
        spalten.append('<article><h2>%s</h2><div class="w">%d Wörter</div>%s</article>'
                       % (t["label"], wortzahl(t["text"]), absaetze))
    seite = """<!doctype html><html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Vergleich %s</title>
<style>
:root{--bg:#fbfaf7;--fg:#222;--mut:#888;--line:#e4e0d8;--card:#fff}
@media (prefers-color-scheme:dark){:root{--bg:#1b1b1a;--fg:#e8e6e1;--mut:#8a8780;--line:#34332f;--card:#232321}}
body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.6 Georgia,"Iowan Old Style",serif}
header{padding:16px;font:14px system-ui,sans-serif;color:var(--mut)}
label{margin-left:12px}
main{display:grid;grid-auto-flow:column;grid-auto-columns:minmax(300px,%s);gap:16px;padding:0 16px 32px;overflow-x:auto}
article{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px 20px 20px}
h2{font:600 22px system-ui,sans-serif;margin:8px 0 0}
.w{font:12px system-ui,sans-serif;color:var(--mut);margin-bottom:8px}
p{margin:0 0 .9em;hyphens:auto}
</style></head><body>
<header>Blindvergleich %s · %d Texte · Reihenfolge zufällig · Bewertung in bewertung.md
<label><input type="checkbox" id="b"> Spalten schmal</label></header>
<main id="m">%s</main>
<script>document.getElementById('b').onchange=function(e){document.getElementById('m').style.gridAutoColumns=e.target.checked?'minmax(300px,420px)':'minmax(300px,%s)'}</script>
</body></html>""" % (titel, "38em", titel, len(texte), "".join(spalten), "38em")
    schreiben(os.path.join(ordner, "vergleich.html"), seite)


# ---- Kennzahlen: Hygiene, kein Qualitätsurteil (Entscheidung A2)

FILTER = re.compile(r"\b(spürte|sah|hörte|merkte|fühlte|bemerkte|erkannte)\b[^.!?]{0,4}\b(wie|dass)\b"
                    r"|wurde (ihr|ihm) klar", re.I)
BLACKLIST = re.compile(
    r"nicht nur\b.{0,40}\bsondern|nicht blo(ß|ss)|mehr als nur|ein Hauch von|ein Anflug von|greifbar|"
    r"unausgesprochen|Klo(ß|ss) im Hals|Gänsehaut|bis zum Hals|über den Rücken|letztendlich|irgendwie|"
    r"ein Stück weit|mach(t|te|en) .{0,20}Sinn|nicht wirklich|die Augen nicht erreichte|"
    r"etwas in (ihr|ihm) zerbrach|etwas verschob sich|die Luft war schwer|lag etwas in der Luft|"
    r"atmete tief durch|Wandteppich|Symphonie aus", re.I | re.S)
ANTITHESE = re.compile(r"\b(nicht|kein\w*)\b[^.!?]{1,60},\s*sondern\b", re.I)


def kennzahlen(text):
    woerter = re.findall(r"\w+", text)
    saetze = [s for s in re.split(r"(?<=[.!?…])[»«„“\"')\s]*\s+|\n\s*\n", text) if re.search(r"\w", s)]
    laengen = [len(re.findall(r"\w+", s)) for s in saetze] or [0]
    rede = sum(len(re.findall(r"\w+", m)) for m in re.findall(r"[„»\"](.*?)[“«\"]", text, re.S))
    return {
        "woerter": len(woerter),
        "saetze": len(saetze),
        "schnitt": statistics.mean(laengen),
        "streuung": statistics.pstdev(laengen),
        "kurz": sum(1 for l in laengen if l < 6),
        "lang": sum(1 for l in laengen if l > 30),
        "rede": 100.0 * rede / max(1, len(woerter)),
        "filter": len(FILTER.findall(text)),
        "blacklist": len(BLACKLIST.findall(text)),
        "antithese": len(ANTITHESE.findall(text)),
        "absaetze": len([a for a in re.split(r"\n\s*\n", text) if a.strip()]),
    }


KZ_KOPF = ("| Wörter | Sätze | Ø Satz | Streuung | <6 W | >30 W | Rede % | Absätze | Filterverben "
           "| Blacklist | nicht…sondern |")
KZ_TRENN = "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"


def kz_zeile(k):
    return ("| %(woerter)d | %(saetze)d | %(schnitt).1f | %(streuung).1f | %(kurz)d | %(lang)d | "
            "%(rede).0f | %(absaetze)d | %(filter)d | %(blacklist)d | %(antithese)d |" % k)


def cmd_messen(args):
    if not args:
        fehler("Welche Dateien? python3 labor.py messen laeufe/<lauf>/*.md")
    print("| Datei " + KZ_KOPF)
    print("|---" + KZ_TRENN)
    for p in args:
        if os.path.basename(p) in ("prompt.md", "rezept.md"):
            continue
        text = frontmatter(lesen(p))[1]
        if MARKER in text:
            continue
        print("| %s " % os.path.join(os.path.basename(os.path.dirname(os.path.abspath(p))), os.path.basename(p)) + kz_zeile(kennzahlen(text)))


def bewertung_lesen(ordner):
    """Liest die ausgefüllte Tabelle: Label -> Liste der Zellen."""
    pfad = os.path.join(ordner, "bewertung.md")
    werte = {}
    if os.path.exists(pfad):
        for z in lesen(pfad).splitlines():
            zellen = [c.strip() for c in z.strip().strip("|").split("|")]
            if len(zellen) >= 2 and re.fullmatch(r"[A-Z]+", zellen[0]):
                werte[zellen[0]] = zellen
    return werte


def cmd_aufdecken(args):
    if not args:
        fehler("Welcher Vergleich? python3 labor.py aufdecken vergleiche/<datum>")
    ordner = args[0] if os.path.isdir(args[0]) else os.path.join(LABOR, args[0])
    schluessel = json.loads(lesen(os.path.join(ordner, ".schluessel.json")))
    bew = bewertung_lesen(ordner)
    zeilen, nach_rezept, nach_modell = [], {}, {}
    for s in sorted(schluessel, key=lambda s: (bew.get(s["label"], ["", "99"])[1] or "99").zfill(3)):
        k = kennzahlen(lesen(os.path.join(ordner, s["label"] + ".md")))
        b = bew.get(s["label"], [])
        rang = b[1] if len(b) > 1 else ""
        weiter = b[2] if len(b) > 2 else ""
        zeilen.append("| %s | %s | %s | %s | %s " % (s["label"], rang or "–", weiter or "–", s["rezept"],
                                                     s["modell"]) + kz_zeile(k))
        if rang.isdigit():
            nach_rezept.setdefault(s["rezept"], []).append(int(rang))
            nach_modell.setdefault(s["modell"], []).append(int(rang))

    def schnitt(d):
        return "\n".join("| %s | %.1f | %d |" % (n, statistics.mean(r), len(r))
                         for n, r in sorted(d.items(), key=lambda x: statistics.mean(x[1])))

    text = "# Aufgedeckt — %s\n\nSortiert nach deinem Rang. Kennzahlen sind Hygiene, kein Urteil: " \
           "grüne Zahlen heissen nicht, dass die Prosa lebt.\n\n" % os.path.basename(ordner.rstrip("/"))
    text += "| Text | Rang | weiter? | Rezept | Modell " + KZ_KOPF + "\n|---|---|---|---|---" + KZ_TRENN + "\n"
    text += "\n".join(zeilen) + "\n"
    if nach_rezept:
        text += "\n## Mittlerer Rang je Rezept\n\n| Rezept | Ø Rang | Texte |\n|---|---:|---:|\n" + schnitt(nach_rezept)
        text += "\n\n## Mittlerer Rang je Modell\n\n| Modell | Ø Rang | Texte |\n|---|---:|---:|\n" + schnitt(nach_modell)
        text += ("\n\nBei einem Text pro Rezept und Modell ist das ein Einzelfall, kein Befund. "
                 "Belastbar wird es mit `wiederholen: 2` oder mehr im Rezept.\n")
    else:
        text += "\n_Keine Ränge in bewertung.md gefunden — erst bewerten, dann aufdecken._\n"
    text += "\n## Herkunft\n\n" + "\n".join("- %s = `%s`" % (s["label"], s["datei"]) for s in schluessel) + "\n"
    schreiben(os.path.join(ordner, "aufgedeckt.md"), text)
    print(text)


def cmd_modelle(args):
    schluessel_laden()
    for k, m in modelle_lesen().items():
        status = "bereit"
        if m["anbieter"] in SCHLUESSEL and not os.environ.get(SCHLUESSEL[m["anbieter"]]):
            status = "Schlüssel fehlt: " + SCHLUESSEL[m["anbieter"]]
        if m["anbieter"] == "claude-code" and not shutil.which("claude"):
            status = "Befehl 'claude' fehlt"
        print("%-10s %-12s %-34s %s" % (k, m["anbieter"], m["id"], status))


BEFEHLE = {"holen": cmd_holen, "aufgabe": cmd_aufgabe, "zeigen": cmd_zeigen, "lauf": cmd_lauf,
           "vergleich": cmd_vergleich, "aufdecken": cmd_aufdecken, "messen": cmd_messen,
           "modelle": cmd_modelle}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in BEFEHLE:
        print(HILFE)
        sys.exit(0 if len(sys.argv) < 2 else 1)
    BEFEHLE[sys.argv[1]](sys.argv[2:])
