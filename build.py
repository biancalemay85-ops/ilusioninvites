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
    ('../website/crear.html', 'nuevo/crear', 'Crea tu invitación · Ilusión Invites',
     'Elige tu diseño, agrega tus fotos y cuéntanos tu idea. Creamos tu invitación digital contigo.'),
    ('../website/experiencia-xv.html', 'nuevo/experiencia/xv-anos', 'La experiencia XV · Ilusión Invites',
     'Link por invitado, lista de confirmados, recordatorios, video de entrada, canción personalizada, marco para Instagram y papelería para tus XV.'),
    ('../website/pedido-xv.html', 'pedido-xv', 'Pedido XV Años · Ilusión Invites',
     'Llena los datos de los XV años y armamos su invitación digital.'),
]
DEMO_NAV = """
<div id="ilu-nav" hidden>
<style>
#ilu-back,#ilu-cta{position:fixed;z-index:2147483000;display:inline-flex;align-items:center;gap:8px;min-height:40px;border-radius:999px;text-decoration:none;font:500 13px/1 Jost,"Avenir Next",system-ui,sans-serif;letter-spacing:.03em;-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);transition:opacity .5s ease,transform .5s ease;-webkit-font-smoothing:antialiased}
#ilu-back{top:calc(12px + env(safe-area-inset-top,0px));left:max(12px,env(safe-area-inset-left,0px));padding:0 15px 0 11px;background:rgba(255,252,246,.88);color:#3A2A26;box-shadow:0 8px 20px -10px rgba(40,25,20,.5),inset 0 0 0 1px rgba(182,138,78,.45)}
#ilu-back svg{width:16px;height:16px}
#ilu-cta{left:50%;bottom:calc(16px + env(safe-area-inset-bottom,0px));transform:translateX(-50%);padding:0 22px;min-height:46px;font-weight:600;font-size:14px;color:#3A2210;background:linear-gradient(180deg,#F7E4B4 0%,#EBC988 34%,#D6A963 70%,#C4914D 100%);box-shadow:inset 0 0 0 1px rgba(170,120,55,.3),0 12px 26px -12px rgba(110,70,30,.65),0 0 22px rgba(236,204,140,.5);white-space:nowrap}
#ilu-cta.off{opacity:0;transform:translate(-50%,24px);pointer-events:none}
@media (prefers-reduced-motion: reduce){#ilu-back,#ilu-cta{transition:none}}
</style>
<a id="ilu-back" href="/nuevo/"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg><span>Volver</span></a>
<a id="ilu-cta" class="off" href="/nuevo/crear/">Quiero una así ✨</a>
</div>
<script>
(function(){
  if (window.top !== window) return; /* inside the preview on the collection page: it has its own buttons */
  var q = new URLSearchParams(location.search), c = q.get('c') || '__COL__', d = q.get('d') || '__DIS__';
  var en = false; try { en = localStorage.getItem('ilu-lang') === 'en'; } catch (e) {}
  var nav = document.getElementById('ilu-nav'), back = document.getElementById('ilu-back'), cta = document.getElementById('ilu-cta');
  back.href = '/nuevo/coleccion/' + c + '/#disenos'; cta.href = '/nuevo/crear/?c=' + c + '&d=' + d;
  back.querySelector('span').textContent = en ? 'Back' : 'Volver'; cta.textContent = en ? 'I want one like this ✨' : 'Quiero una así ✨';
  back.addEventListener('click', function (e) { try { if (document.referrer && new URL(document.referrer).origin === location.origin && history.length > 1) { e.preventDefault(); history.back(); } } catch (x) {} });
  nav.hidden = false;
  var last = scrollY, shown = false;
  setTimeout(function () { shown = true; cta.classList.remove('off'); }, 3500);
  addEventListener('scroll', function () { if (!shown) return; var y = scrollY; if (y > last + 8) cta.classList.add('off'); else if (y < last - 8 || innerHeight + y >= document.documentElement.scrollHeight - 40) cta.classList.remove('off'); last = y; }, { passive: true });
})();
</script>
"""
DEMO_INFO = {'demos/boda-jardin-blanco': ('bodas', 'jardin-blanco'), 'demos/boda-isabella-julian': ('bodas', 'terciopelo-vino'), 'demos/boda-camila-sebastian': ('bodas', 'encaje-perlas')}
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
    if out in DEMO_INFO:
        body += DEMO_NAV.replace('__COL__', DEMO_INFO[out][0]).replace('__DIS__', DEMO_INFO[out][1])
    open(os.path.join(HERE, out, 'index.html'), 'w', encoding='utf-8').write(head + body + '\n</body>\n</html>\n')
    print('built', out or '(root)')

# always finish with the collections step (it fills the home page and "Crea la tuya" with the collections)
import subprocess, sys
subprocess.run([sys.executable, os.path.join(HERE, 'experiencias.py')], check=True)
subprocess.run([sys.executable, os.path.join(HERE, 'colecciones.py')], check=True)
