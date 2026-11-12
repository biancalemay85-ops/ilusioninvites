"""Builds the public (GitHub Pages) copies from the artifact pages. Run: python3 build.py"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = 'https://ilusioninvites.com'
PAGES = [
    ('../demos/boda-jardin-blanco/index.html', 'demos/boda-jardin-blanco', 'Ana Sofía & Emiliano · Ilusión Invites', 'Invitación de boda de ejemplo: Jardín Blanco.'),
    ('../demos/boda-isabella-julian/index.html', 'demos/boda-isabella-julian', 'Isabella & Julián · Ilusión Invites', 'Invitación de boda de ejemplo: terciopelo vino y oro.'),
    ('../demos/boda-camila-sebastian/index.html', 'demos/boda-camila-sebastian', 'Camila & Sebastián · Ilusión Invites', 'Invitación de boda de ejemplo: encaje.'),
    ('../website/index.html', '', 'Ilusión Invites · Invitaciones digitales de lujo',
     'Invitaciones digitales que se abren como un sobre con sello: bodas, XV años, baby showers y cumpleaños. México y Canadá.'),
    # (source artifact file, output folder, title, description)
    ('../website/inicio-claro.html', 'nuevo', 'Ilusión Invites · Invitaciones digitales',
     'Invitaciones digitales de lujo para bodas, XV años, baby showers, cumpleaños, galas, posadas y Año Nuevo. México y Canadá.'),
    ('../website/pedido-xv.html', 'pedido-xv', 'Pedido XV Años · Ilusión Invites',
     'Llena los datos de los XV años y armamos su invitación digital.'),
]
for src, out, title, desc in PAGES:
    sub = (out + '/') if out else ''
    body = open(os.path.join(HERE, src), encoding='utf-8').read()
    head = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{BASE}/{sub}img/ilusion-logo.jpg">
<meta property="og:url" content="{BASE}/{(out + '/') if out else ''}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#1E0916">
<link rel="icon" href="img/ilusion-logo.jpg">
<style>body{{margin:0}} img{{max-width:100%}} [hidden]{{display:none!important}}</style>
</head>
<body>
'''
    os.makedirs(os.path.join(HERE, out), exist_ok=True)
    open(os.path.join(HERE, out, 'index.html'), 'w', encoding='utf-8').write(head + body + '\n</body>\n</html>\n')
    print('built', out or '(root)')
