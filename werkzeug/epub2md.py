"""epub -> Quelltext-Markdown im Format von BuchNeu/style/quellen (lesbar mit tools/norm.py).

1. Übersicht: welche Teile hat das Buch, wo beginnt der Roman?
     python3 werkzeug/epub2md.py buch.epub
   -> eine Zeile pro Spine-Teil: ID, Wortzahl, Textanfang

2. Umwandeln, vom ersten bis zum letzten Romanteil (IDs aus der Übersicht):
     python3 werkzeug/epub2md.py buch.epub ziel.md "<!-- Quelle: … -->" chapter2 chapter37

Ergebnis: ein Absatz pro Block, Überschriften als "# …", Kursives als *…*,
Szenenwechsel als * * *, eingerückte Kästen (Fischer "einschub") als "> …".
"""
import sys, re, zipfile, posixpath, html
from html.parser import HTMLParser

def css_regeln(z, namen):
    regeln = {}
    for n in namen:
        if n.endswith(".css"):
            css = z.read(n).decode("utf-8", "replace")
            for sel, body in re.findall(r"([^{}]+)\{([^}]*)\}", css):
                for s in sel.split(","):
                    m = re.fullmatch(r"\s*(?:[a-z0-9]*)\.([\w-]+)\s*", s)
                    if m: regeln.setdefault(m.group(1), "")
                    if m: regeln[m.group(1)] += body
    return regeln

def kursiv(cls, css): return any("font-style: italic" in re.sub(r"\s+", " ", css.get(c, "")).replace("font-style:italic", "font-style: italic") for c in cls)
def abstand_oben(cls, css):
    for c in cls:
        r = re.sub(r"\s+", " ", css.get(c, ""))
        m = re.search(r"margin-top:\s*([\d.]+)", r) or re.search(r"margin:\s*([\d.]+)\w*\s", r)
        if m and float(m.group(1)) > 0: return True
    return False

class P(HTMLParser):
    def __init__(s, css):
        super().__init__(convert_charrefs=True)
        s.css = css; s.out = []; s.buf = None; s.art = None; s.stapel = []
        s.einschub = 0; s.kopf = []; s.nach_kopf = True; s.still = 0
    def _flush_kopf(s):
        if s.kopf:
            s.out.append("# " + " · ".join(s.kopf)); s.kopf = []; s.nach_kopf = True
    def handle_starttag(s, t, a):
        a = dict(a); cls = (a.get("class") or "").split()
        if t in ("br",):
            if s.buf is not None: s.buf.append(" ")
            return
        if t in ("img", "meta", "link", "hr"): return
        marke = ""
        if t in ("script", "style", "head") or "origpage" in cls or "pagebreak" in (a.get("epub:type") or ""):
            s.still += 1; marke = "still"
        elif t == "div" and "einschub" in cls:
            s.einschub += 1; marke = "einschub"
        elif t in ("h1", "h2", "h3", "h4") or (t == "p" and "untertitel" in cls):
            s.buf = []; s.art = "kopf"
        elif t == "p":
            s._flush_kopf()
            if "leerzeile" in cls:
                s.art = "leer"
            else:
                s.art = "absatz"
                if not s.nach_kopf and not s.einschub and abstand_oben(cls, s.css) and s.out and s.out[-1] != "* * *":
                    s.out.append("* * *")
            s.buf = []
        elif s.buf is not None and (t in ("em", "i") or (t == "span" and kursiv(cls, s.css))):
            s.buf.append("*"); marke = "*"
        elif s.buf is not None and t in ("strong", "b"):
            s.buf.append("**"); marke = "**"
        s.stapel.append((t, marke))
    def handle_endtag(s, t):
        while s.stapel:
            tt, marke = s.stapel.pop()
            if marke == "still": s.still -= 1
            elif marke == "einschub": s.einschub -= 1
            elif marke and s.buf is not None: s.buf.append(marke)
            if tt == t: break
        if t in ("h1", "h2", "h3", "h4", "p") and s.buf is not None:
            txt = re.sub(r"\s+", " ", "".join(s.buf)).strip()
            txt = re.sub(r"(\*+)(\s*)\1", r"\2", txt)          # leere Kursivmarken
            if s.art == "kopf":
                if txt: s.kopf.append(txt.replace("*", ""))
            elif s.art == "leer":
                if not s.einschub and s.out and s.out[-1] != "* * *": s.out.append("* * *")
            elif txt:
                s.out.append(("> " if s.einschub else "") + txt); s.nach_kopf = False
            s.buf = None; s.art = None
    def handle_data(s, d):
        if s.buf is not None and not s.still: s.buf.append(d)
    def close(s):
        super().close(); s._flush_kopf()
        while s.out and s.out[-1] == "* * *": s.out.pop()

def inhalt(z):
    namen = z.namelist()
    opf = [n for n in namen if n.endswith(".opf")][0]; o = z.read(opf).decode("utf-8")
    man = {}
    for m in re.finditer(r"<item\b[^>]*>", o):
        i = re.search(r'\bid="([^"]*)"', m.group(0)); h = re.search(r'\bhref="([^"]*)"', m.group(0))
        if i and h: man[i.group(1)] = posixpath.normpath(posixpath.join(posixpath.dirname(opf), h.group(1)))
    return namen, man, re.findall(r'itemref idref="([^"]*)"', o)

if len(sys.argv) == 2:
    z = zipfile.ZipFile(sys.argv[1]); namen, man, spine = inhalt(z)
    for i in spine:
        t = z.read(man[i]).decode("utf-8", "replace")
        t = re.sub(r"(?s)<head.*?</head>", "", t)
        w = html.unescape(re.sub(r"<[^>]+>", "", re.sub(r"</(p|h\d|div)>", " ", t))).split()
        print("%-14s %6d  %s" % (i, len(w), " ".join(w[:12])))
    sys.exit()
if len(sys.argv) != 6:
    sys.exit(__doc__)

epub, ziel, kopf, von, bis = sys.argv[1:6]
z = zipfile.ZipFile(epub); namen, man, spine = inhalt(z)
teil = spine[spine.index(von):spine.index(bis) + 1]
css = css_regeln(z, namen)
bloecke = []
for i in teil:
    p = P(css); p.feed(z.read(man[i]).decode("utf-8")); p.close(); bloecke += p.out
open(ziel, "w", encoding="utf-8").write(kopf + "\n\n" + "\n\n".join(bloecke) + "\n")
print(ziel, len(teil), "Spine-Teile,", len(bloecke), "Blöcke")
