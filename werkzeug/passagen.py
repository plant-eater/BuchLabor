"""Stilvorlagen-Passagen aus Quelltexten erzeugen (Format wie BuchNeu/style/passagen).

Die Auswahl steht in werkzeug/auswahl/<buch>.py: BUCH (Datei, Autor, Quelle, Hinweise für alle
Passagen) und P (je Stelle: Szenentyp, Nummer, Absätze lang, Absätze kurz, Funktion, nutzen_fuer,
nicht_nutzen_fuer, was übernehmen, was nicht). Absatznummern (¶) wie BuchNeu/tools/norm.py.

  python3 werkzeug/passagen.py spellshop falling_midgard dungeon_crawler_carl

Schreibt <datei>-<typ>-<n>.md und <datei>-<typ>-<n>-kurz.md nach zutaten/stil/modern/ und
überschreibt vorhandene. Kurzfassungen nennen unter „übernehmen“ nur Punkte, deren »Zitate«
im Auszug stehen. Kapitelköpfe am Anfang werden übersprungen, im Inneren zu * * *.
"""
import sys, os, importlib, re
sys.dont_write_bytecode = True
LABOR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(LABOR, '..', 'BuchNeu', 'tools'))
sys.path.insert(0, os.path.join(LABOR, 'werkzeug', 'auswahl'))
import norm
ZIEL = os.path.join(LABOR, 'zutaten', 'stil', 'modern')
TK = dict(kapitelanfang='KA', figureneinfuehrung='FE', konfliktgespraech='KG', **{'innere-passage': 'IP'},
          eskalation='ES', schauplatzwechsel='SW', verlust='VL', kapitelschluss='KS', figurenbild='FB', stimmen='ST')
def q(s):
    assert '"' not in s, s
    return '"%s"' % s
bericht = []
if len(sys.argv) < 2: sys.exit(__doc__)
for modul in sys.argv[1:]:
    m = importlib.import_module(modul); B = m.BUCH
    ps = norm.paragraphs(os.path.join(ZIEL, B['datei'] + '.md'))
    for typ, n, (a, b), (ka, kb), funktion, nutzen, nicht_nutzen, ueber, nicht in m.P:
        assert a <= ka <= kb <= b, (B['datei'], typ, n)
        for kurz in (False, True):
            x, y = (ka, kb) if kurz else (a, b)
            while ps[x].startswith('# '):
                print('Hinweis: Start verschoben', B['datei'], typ, n, x, '->', x + 1, file=sys.stderr); x += 1
            if not kurz: a = x
            teil = ps[x:y + 1]
            for p in teil[1:]:
                if p.startswith('# '): print('Hinweis: Kopf im Inneren', B['datei'], typ, n, p, file=sys.stderr)
            teil = ['* * *' if p.startswith('# ') else p for p in teil]
            w = sum(len(p.split()) for p in teil if p != '* * *')
            name = '%s-%s-%d%s' % (B['datei'], typ, n, '-kurz' if kurz else '')
            kopf = ['---',
                    'id: ' + q('%s-%s%d%s' % (B['kurz'], TK[typ], n, 'k' if kurz else '')),
                    'autor: ' + q(B['autor']),
                    'quelle: ' + q(B['quelle']),
                    'stelle: ' + q('%s.md ¶%d–%d' % (B['datei'], x, y)),
                    'funktion: ' + q(funktion),
                    'woerter: %d' % w,
                    'nutzen_fuer: ' + q(nutzen),
                    'nicht_nutzen_fuer: ' + q(nicht_nutzen),
                    '---', '']
            if kurz:
                kopf += ['<!-- Kurzfassung von %s-%s-%d.md (¶%d–%d, %s Wörter): dieselbe Stelle, gekürzt auf 250–400 Wörter.' % (B['datei'], typ, n, a, b, '{lang}'),
                         '     Für Vergleiche, in denen nur die Länge der Stilvorlage wechselt. -->', '']
            text = '\n'.join(kopf) + '\n'
            ganz = ' '.join(teil).replace('*', '')
            def passt(s): return all(z.replace('*', '') in ganz for z in re.findall(r'»([^«]+)«', s))
            ueb = [s for s in ueber if passt(s)] if kurz else ueber
            if kurz and not ueb: ueb = ueber[:1]
            text += '## Was daran übernommen werden soll\n\n' + '\n'.join('- ' + s for s in ueb) + '\n\n'
            text += '## Was ausdrücklich nicht übernommen werden soll\n\n' + '\n'.join('- ' + s for s in nicht + B['immer_nicht']) + '\n\n'
            text += '## Passage (%d Wörter)\n\n' % w + '\n\n'.join(teil) + '\n'
            if kurz: text = text.replace('{lang}', str(lang_w))
            else: lang_w = w
            open(os.path.join(ZIEL, name + '.md'), 'w', encoding='utf-8').write(text)
            bericht.append((name, w))
for name, w in bericht:
    print('%-55s %5d' % (name, w))
print(len(bericht), 'Dateien')
