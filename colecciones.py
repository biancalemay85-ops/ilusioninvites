"""Builds the 8 collection pages and injects the collection list into the home page.

Run after build.py:   python3 build.py && python3 colecciones.py
Edit content in:       ../website/colecciones.json
Edit page design in:   ../website/coleccion-plantilla.html
"""
import json, os, html
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = 'https://ilusioninvites.com'
data = json.load(open(os.path.join(HERE, '../website/colecciones.json'), encoding='utf-8'))
cols = data['colecciones']
tpl = open(os.path.join(HERE, '../website/coleccion-plantilla.html'), encoding='utf-8').read()

lite = [{k: c.get(k, '') for k in ('slug', 'frame', 'img', 'deco', 'decoPos', 'es', 'en')} for c in cols]
for c in cols:
    t = c['tema']
    decos = ''
    if c.get('deco') and c['deco'] != 'arreglo':
        decos = (f'<img class="deco d1" src="../../img/{c["deco"]}.webp" alt="">'
                 f'<img class="deco d2" src="../../img/{c["deco"]}.webp" alt="">')
    page = tpl
    rep = {
        '{{TITLE}}': html.escape(c['es']['nombre'] + ' · Ilusión Invites'),
        '{{DESC}}': html.escape(c['es']['intro']),
        '{{BASE}}': BASE, '{{IMG}}': c['img'], '{{HERO}}': c['img'].replace('cat-', ''),
        '{{BG}}': t['bg'], '{{BG2}}': t['bg2'], '{{INK}}': t['ink'], '{{ACCENT}}': t['accent'], '{{SOFT}}': t['soft'],
        '{{SCHEME}}': 'dark' if t.get('oscuro') else 'light',
        '{{DECOS}}': decos,
        '{{DATA}}': json.dumps({'actual': c, 'todas': lite}, ensure_ascii=False).replace('</', '<\\/'),
    }
    for k, v in rep.items():
        page = page.replace(k, v)
    out = os.path.join(HERE, 'nuevo', 'coleccion', c['slug'])
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(page)
    print('built coleccion/' + c['slug'])

home = os.path.join(HERE, 'nuevo', 'index.html')
s = open(home, encoding='utf-8').read()
s = s.replace('__COLECCIONES__', json.dumps({'colecciones': lite}, ensure_ascii=False).replace('</', '<\\/'))
open(home, 'w', encoding='utf-8').write(s)
print('home: collections injected')
