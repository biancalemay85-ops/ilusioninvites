"""Builds the public (GitHub Pages) copies from the artifact pages. Run: python3 build.py"""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = 'https://ilusioninvites.com'
PAGES = [
    ('../demos/boda-jardin-blanco/index.html', 'demos/boda-jardin-blanco', 'Ana Sofía & Emiliano · Ilusión Invites', 'Invitación de boda de ejemplo: Jardín Blanco.'),
    ('../demos/boda-isabella-julian/index.html', 'demos/boda-isabella-julian', 'Isabella & Julián · Ilusión Invites', 'Invitación de boda de ejemplo: terciopelo vino y oro.'),
    ('../demos/boda-camila-sebastian/index.html', 'demos/boda-camila-sebastian', 'Camila & Sebastián · Ilusión Invites', 'Invitación de boda de ejemplo: encaje.'),
    ('../demos/xv-valentina/index.html', 'demos/xv-valentina', 'Mis XV · Valentina · Ilusión Invites', 'Invitación de XV años de ejemplo: Rosa Roja, rojo y dorado.'),
    ('../demos/xv-renata/index.html', 'demos/xv-renata', 'Mis XV · Renata · Ilusión Invites', 'Invitación de XV años de ejemplo: Noche de Zafiro, azul y plata.'),
    ('../demos/xv-ximena/index.html', 'demos/xv-ximena', 'Mis XV · Ximena · Ilusión Invites', 'Invitación de XV años de ejemplo: Jardín de Jade, verde jade y oro.'),
    ('../demos/cumple-ricardo/index.html', 'demos/cumple-ricardo', 'Los 50 de Ricardo · Ilusión Invites', 'Invitación de cumpleaños de ejemplo: Clásico 67, negro, cromo y oro.'),
    ('../demos/cumple-mariana/index.html', 'demos/cumple-mariana', 'Los 40 de Mariana · Ilusión Invites', 'Invitación de cumpleaños de ejemplo: Noche de Champaña, art déco negro y oro.'),
    ('../demos/cumple-elena/index.html', 'demos/cumple-elena', 'Los 60 de Elena · Ilusión Invites', 'Invitación de cumpleaños de ejemplo: Cena en la Toscana, terracota y olivo.'),
    ('../demos/baby-nube/index.html', 'demos/baby-nube', 'Baby shower · Mateo · Ilusión Invites', 'Invitación de baby shower de ejemplo: Nube de Algodón, una caja de regalo azul cielo.'),
    ('../demos/baby-mariposas/index.html', 'demos/baby-mariposas', 'Baby shower · Valeria · Ilusión Invites', 'Invitación de baby shower de ejemplo: Jardín de Mariposas, rubor y salvia.'),
    ('../demos/baby-luna/index.html', 'demos/baby-luna', 'Baby shower · Paola y Luis · Ilusión Invites', 'Invitación de baby shower de ejemplo: Bajo la Luna, azul noche y oro.'),
    ('../demos/empresa-gala/index.html', 'demos/empresa-gala', 'Gala Anual 2027 · Grupo Altavista · Ilusión Invites', 'Evento de empresa de ejemplo: Gala Esmeralda, negro, esmeralda y oro.'),
    ('../demos/empresa-lanzamiento/index.html', 'demos/empresa-lanzamiento', 'Lanzamiento Aurum · Maison Lumière · Ilusión Invites', 'Evento de empresa de ejemplo: lanzamiento de producto, mármol negro y oro.'),
    ('../demos/empresa-aniversario/index.html', 'demos/empresa-aniversario', '25 años · Grupo Solaris · Ilusión Invites', 'Evento de empresa de ejemplo: aniversario, champaña y oro.'),
    ('../demos/navidad-posada/index.html', 'demos/navidad-posada', 'Posada Navideña · Familia Ruiz · Ilusión Invites', 'Posada de ejemplo: piñata de estrella, papel picado y ponche.'),
    ('../demos/navidad-noche-paz/index.html', 'demos/navidad-noche-paz', 'Nochebuena · Familia Castillo · Ilusión Invites', 'Cena de Nochebuena de ejemplo: marfil, blanco y oro.'),
    ('../demos/navidad-bosque/index.html', 'demos/navidad-bosque', 'Navidad en el bosque · Familia Ortega · Ilusión Invites', 'Navidad de ejemplo: esfera de nieve, cabaña y bosque nevado.'),
    ('../demos/cumple-whisky/index.html', 'demos/cumple-whisky', 'Noche de Whisky · Andrés 40 · Ilusión Invites', 'Cumpleaños de ejemplo: Noche de Whisky.'),
    ('../demos/cumple-golf/index.html', 'demos/cumple-golf', 'Hoyo 18 · Roberto 50 · Ilusión Invites', 'Cumpleaños de ejemplo: Hoyo 18.'),
    ('../demos/cumple-abanico/index.html', 'demos/cumple-abanico', 'Abanico de Encaje · Sofía 30 · Ilusión Invites', 'Cumpleaños de ejemplo: Abanico de Encaje.'),
    ('../demos/cumple-disco/index.html', 'demos/cumple-disco', 'Disco Glam · Paola 40 · Ilusión Invites', 'Cumpleaños de ejemplo: Disco Glam.'),
    ('../demos/cumple-carrusel/index.html', 'demos/cumple-carrusel', 'Carrusel Mágico · Valeria 6 años · Ilusión Invites', 'Cumpleaños de ejemplo: Carrusel Mágico.'),
    ('../demos/cumple-hadas/index.html', 'demos/cumple-hadas', 'Jardín de Hadas · Lucía 8 años · Ilusión Invites', 'Cumpleaños de ejemplo: Jardín de Hadas.'),
    ('../demos/cumple-espacio/index.html', 'demos/cumple-espacio', 'Misión Espacial · Mateo cumple 7 · Ilusión Invites', 'Cumpleaños de ejemplo: Misión Espacial.'),
    ('../demos/cumple-dino/index.html', 'demos/cumple-dino', 'Expedición Dino · Santiago cumple 5 · Ilusión Invites', 'Cumpleaños de ejemplo: Expedición Dino.'),
    ('../demos/boda-regina-emilio/index.html', 'demos/boda-regina-emilio', 'Regina & Emilio · Ilusión Invites', 'Invitación de boda de ejemplo: pétalos blancos, encaje, sello de perla y cristal.'),
    # the old homepage (website/index.html) is retired: ilusioninvites.com now sends visitors to the new site at /nuevo/
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
  back.href = '/nuevo/coleccion/' + c + '/#disenos'; cta.href = '/nuevo/?evento=' + c + '&diseno=' + encodeURIComponent('__DISN__') + '#imagina';
  back.querySelector('span').textContent = en ? 'Back' : 'Volver'; cta.textContent = en ? 'I want one like this ✨' : 'Quiero una así ✨';
  back.addEventListener('click', function (e) { try { if (document.referrer && new URL(document.referrer).origin === location.origin && history.length > 1) { e.preventDefault(); history.back(); } } catch (x) {} });
  nav.hidden = false;
  var last = scrollY, shown = false;
  setTimeout(function () { shown = true; cta.classList.remove('off'); }, 3500);
  addEventListener('scroll', function () { if (!shown) return; var y = scrollY; if (y > last + 8) cta.classList.add('off'); else if (y < last - 8 || innerHeight + y >= document.documentElement.scrollHeight - 40) cta.classList.remove('off'); last = y; }, { passive: true });
})();
</script>
"""
FREEZE = """
<div id="ilu-freeze">
<style>
#ilu-pause{position:fixed;z-index:2147483001;left:max(12px,env(safe-area-inset-left,0px));bottom:calc(16px + env(safe-area-inset-bottom,0px));width:42px;height:42px;border-radius:50%;border:0;cursor:pointer;display:grid;place-items:center;padding:0;color:#3A2A26;background:rgba(255,252,246,.82);box-shadow:inset 0 0 0 1px rgba(182,138,78,.45),0 8px 18px -8px rgba(40,25,20,.5);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);-webkit-tap-highlight-color:transparent}
#ilu-pause svg{width:15px;height:15px}
#ilu-pause .pl{display:none} html.ilu-frozen #ilu-pause .pa{display:none} html.ilu-frozen #ilu-pause .pl{display:block}
html.ilu-frozen *,html.ilu-frozen *::before,html.ilu-frozen *::after{animation-play-state:paused!important}
</style>
<button id="ilu-pause" type="button" aria-pressed="false" aria-label="Pausar animación"><svg class="pa" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><rect x="6" y="5" width="4" height="14" rx="1.2"/><rect x="14" y="5" width="4" height="14" rx="1.2"/></svg><svg class="pl" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5.5v13a1 1 0 0 0 1.5.86l10.2-6.5a1 1 0 0 0 0-1.72L9.5 4.64A1 1 0 0 0 8 5.5z"/></svg></button>
<script>
/* pause button: freezes every animation so a guest (or the designer) can stop at any moment */
(function(){
  var raf=window.requestAnimationFrame.bind(window), q=[], frozen=false, paused=[];
  window.requestAnimationFrame=function(cb){ if(frozen){ q.push(cb); return 0; } return raf(cb); };
  var b=document.getElementById('ilu-pause'), en=false; try{ en=localStorage.getItem('ilu-lang')==='en'||localStorage.getItem('ilusion-lang')==='en'; }catch(e){}
  function label(){ b.setAttribute('aria-label', frozen ? (en?'Resume animation':'Continuar animación') : (en?'Pause animation':'Pausar animación')); b.setAttribute('aria-pressed', String(frozen)); }
  b.addEventListener('click', function(e){
    e.stopPropagation(); frozen=!frozen; document.documentElement.classList.toggle('ilu-frozen', frozen);
    if(frozen){ paused=(document.getAnimations?document.getAnimations():[]).filter(function(a){ return a.playState==='running'; }); paused.forEach(function(a){ try{a.pause();}catch(x){} }); }
    else { paused.forEach(function(a){ try{a.play();}catch(x){} }); paused=[]; var cbs=q; q=[]; cbs.forEach(function(cb){ raf(cb); }); }
    label();
  });
  label();
})();
</script>
</div>
"""
DIS_NAMES = {d['id']: d['nombre'] for c in json.load(open(os.path.join(HERE, '..', 'website', 'colecciones.json'), encoding='utf-8'))['colecciones'] for d in c.get('disenos', [])}
DEMO_INFO = {'demos/boda-jardin-blanco': ('bodas', 'jardin-blanco'), 'demos/boda-isabella-julian': ('bodas', 'terciopelo-vino'), 'demos/boda-camila-sebastian': ('bodas', 'encaje-perlas'), 'demos/boda-regina-emilio': ('bodas', 'perla-cristal'), 'demos/xv-valentina': ('xv-anos', 'rosa-roja'), 'demos/xv-renata': ('xv-anos', 'noche-zafiro'), 'demos/xv-ximena': ('xv-anos', 'jardin-jade'), 'demos/cumple-ricardo': ('cumpleanos', 'clasico-67'), 'demos/cumple-mariana': ('cumpleanos', 'noche-champana'), 'demos/cumple-elena': ('cumpleanos', 'cena-toscana'), 'demos/baby-nube': ('baby-shower', 'nube-algodon'), 'demos/baby-mariposas': ('baby-shower', 'jardin-mariposas'), 'demos/baby-luna': ('baby-shower', 'bajo-la-luna'), 'demos/empresa-gala': ('empresas', 'gala-esmeralda'), 'demos/empresa-lanzamiento': ('empresas', 'gran-lanzamiento'), 'demos/empresa-aniversario': ('empresas', 'aniversario-25'), 'demos/navidad-posada': ('navidad', 'posada-tradicional'), 'demos/navidad-noche-paz': ('navidad', 'noche-de-paz'), 'demos/navidad-bosque': ('navidad', 'navidad-bosque'), 'demos/cumple-whisky': ('cumpleanos', 'noche-whisky'), 'demos/cumple-golf': ('cumpleanos', 'hoyo-18'), 'demos/cumple-abanico': ('cumpleanos', 'abanico-encaje'), 'demos/cumple-disco': ('cumpleanos', 'disco-glam'), 'demos/cumple-carrusel': ('cumpleanos', 'carrusel-magico'), 'demos/cumple-hadas': ('cumpleanos', 'jardin-hadas'), 'demos/cumple-espacio': ('cumpleanos', 'mision-espacial'), 'demos/cumple-dino': ('cumpleanos', 'expedicion-dino')}
# pages with their own link preview (shown when the link is shared on WhatsApp, iMessage, Instagram...)
OG = {
    'demos/cumple-whisky': ('Andrés cumple 40 🥃', 'Viernes 3 de septiembre de 2027 · San Pedro Garza García. Toca el vaso para servir.', 'img/compartir.jpg', 'img/vaso-lleno.webp', '#1E130C'),
    'demos/cumple-golf': ('Roberto cumple 50 ⛳', 'Sábado 15 de mayo de 2027 · Querétaro. Toca la pelota para tirar.', 'img/compartir.jpg', 'img/bola.webp', '#F4F6F0'),
    'demos/cumple-abanico': ('Los 30 de Sofía 🌸', 'Sábado 12 de junio de 2027 · Roma Norte, CDMX. Toca el abanico para abrirlo.', 'img/compartir.jpg', 'img/abanico-abierto.webp', '#F4E2DE'),
    'demos/cumple-disco': ('Paola · 40 & Fabulosa 🪩', 'Sábado 23 de octubre de 2027 · Polanco, CDMX. Toca la bola disco.', 'img/compartir.jpg', 'img/bola-mini.webp', '#1E0F2E'),
    'demos/cumple-carrusel': ('Valeria cumple 6 🎠', 'Sábado 15 de mayo de 2027 · Polanco, CDMX. Toca el carrusel para hacerlo girar.', 'img/compartir.jpg', 'img/objeto.webp', '#F8E8E6'),
    'demos/cumple-hadas': ('Lucía cumple 8 ✨', 'Sábado 18 de septiembre de 2027 · Valle de Bravo. Toca el frasco para abrirlo.', 'img/compartir.jpg', 'img/objeto.webp', '#2A2240'),
    'demos/cumple-espacio': ('Mateo cumple 7 🚀', 'Sábado 13 de marzo de 2027 · San Pedro Garza García. Toca el cohete para despegar.', 'img/compartir.jpg', 'img/objeto.webp', '#0B1530'),
    'demos/cumple-dino': ('Santiago cumple 5 🦕', 'Sábado 24 de abril de 2027 · Cuernavaca. Toca el huevo para abrirlo.', 'img/compartir.jpg', 'img/objeto.webp', '#F1E6D2'),
    'demos/boda-jardin-blanco': ('Boda de Ana Sofía & Emiliano 🤍', 'Sábado 5 de junio de 2027 · Querétaro. Toca el sello y cruza el arco del jardín.', 'img/compartir.jpg', 'img/sello-rosas.webp', '#F6F1E8'),
    'demos/boda-isabella-julian': ('Boda de Isabella & Julián ❤️', 'Sábado 16 de octubre de 2027 · Guadalajara. Toca el sello para abrir tu invitación.', 'img/compartir.jpg', 'img/sello-cisnes.webp', '#3A0E18'),
    'demos/empresa-gala': ('Gala Anual 2027 · Grupo Altavista ✨', 'Viernes 26 de noviembre de 2027 · Ciudad de México. Toca para abrir tu invitación.', 'img/compartir.jpg', 'img/cordon.webp', '#071A14'),
    'demos/empresa-lanzamiento': ('Maison Lumière presenta AURUM ✨', 'Jueves 14 de octubre de 2027 · Polanco, CDMX. Toca para descubrir.', 'img/compartir.jpg', 'img/producto.webp', '#060606'),
    'demos/empresa-aniversario': ('Grupo Solaris celebra 25 años ✨', 'Sábado 19 de junio de 2027 · Guadalajara. Toca el corcho para abrir tu invitación.', 'img/compartir.jpg', 'img/botella-full.webp', '#F4E8D2'),
    'demos/navidad-posada': ('Posada Navideña · Familia Ruiz ✨', 'Sábado 18 de diciembre de 2027 · Querétaro. Toca la piñata para abrir tu invitación.', 'img/compartir.jpg', 'img/pinata.webp', '#1C2240'),
    'demos/navidad-noche-paz': ('Nochebuena · Familia Castillo ✨', 'Viernes 24 de diciembre de 2027 · Valle de Bravo. Toca la esfera para abrir tu invitación.', 'img/compartir.jpg', 'img/esfera.webp', '#FBF7EF'),
    'demos/navidad-bosque': ('Navidad en el bosque · Familia Ortega ✨', 'Sábado 25 de diciembre de 2027 · Mazamitla. Agita la esfera para abrir tu invitación.', 'img/compartir.jpg', 'img/esfera.webp', '#1F3B2D'),
    'demos/baby-nube': ('Baby shower · Esperamos a Mateo ✨', 'Sábado 20 de marzo de 2027 · Puebla. Toca para abrir tu invitación.', 'img/compartir.jpg', 'img/caja.webp', '#EAF1F8'),
    'demos/baby-mariposas': ('Baby shower · Esperamos a Valeria ✨', 'Sábado 17 de abril de 2027 · Valle de Bravo. Toca para abrir tu invitación.', 'img/compartir.jpg', 'img/mariposa-1.webp', '#F6E6E2'),
    'demos/baby-luna': ('Baby shower · Bajo la Luna ✨', 'Domingo 9 de mayo de 2027 · Cuernavaca. Toca para abrir tu invitación.', 'img/compartir.jpg', 'img/luna.webp', '#1E2A4A'),
    'demos/cumple-ricardo': ('Los 50 de Ricardo ✨', 'Sábado 15 de mayo de 2027 · Querétaro. Toca para abrir tu invitación.', 'img/compartir.jpg', 'img/sello.webp', '#0B0B0B'),
    'demos/cumple-mariana': ('Los 40 de Mariana ✨', 'Sábado 4 de septiembre de 2027 · Ciudad de México. Toca para abrir tu invitación.', 'img/compartir.jpg', 'img/sello.webp', '#070605'),
    'demos/cumple-elena': ('Los 60 de Elena ✨', 'Sábado 23 de octubre de 2027 · Valle de Guadalupe. Toca para abrir tu invitación.', 'img/compartir.jpg', 'img/sello.webp', '#F3EBDD'),
    'demos/xv-valentina': ('Mis XV Años · Valentina ✨', 'Sábado 13 de marzo de 2027 · Guadalajara. Toca para abrir tu invitación.', 'img/compartir.jpg', 'img/sello.webp', '#3A0A14'),
    'demos/xv-renata': ('Mis XV Años · Renata ✨', 'Sábado 12 de junio de 2027 · Monterrey. Toca para abrir tu invitación.', 'img/compartir.jpg', 'img/sello.webp', '#0B1E46'),
    'demos/xv-ximena': ('Mis XV Años · Ximena ✨', 'Sábado 9 de octubre de 2027 · San Miguel de Allende. Toca para abrir tu invitación.', 'img/compartir.jpg', 'img/sello.webp', '#EEF3EC'),
    'demos/boda-regina-emilio': ('Regina & Emilio · Nos casamos ✨', 'Sábado 17 de abril de 2027 · San Miguel de Allende. Toca para abrir tu invitación.', 'img/compartir.jpg', 'img/sello-corona.webp', '#F3ECE2'),
}
for src, out, title, desc in PAGES:
    sub = (out + '/') if out else ''
    body = open(os.path.join(HERE, src), encoding='utf-8').read()
    og = OG.get(out)
    og_title, og_desc = (og[0], og[1]) if og else (title, desc)
    og_img = f"{BASE}/{sub}{og[2]}" if og else f"{BASE}/{sub}img/ilusion-logo.jpg"
    og_extra = (f'\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n<meta property="og:image:alt" content="{og_title}">\n<meta name="twitter:card" content="summary_large_image">') if og else ''
    icon = og[3] if og else 'img/ilusion-logo.jpg'
    apple = f'\n<link rel="apple-touch-icon" href="{og[3]}">' if og else ''
    theme = og[4] if og else '#1E0916'
    if og: title = og_title
    head = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="{desc}">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{og_desc}">
<meta property="og:image" content="{og_img}">{og_extra}
<meta property="og:url" content="{BASE}/{(out + '/') if out else ''}">
<link rel="canonical" href="{BASE}/{(out + '/') if out else ''}">
<meta property="og:type" content="website">
<meta name="theme-color" content="{theme}">
<link rel="icon" href="{icon}">{apple}
<style>body{{margin:0}} img{{max-width:100%}} [hidden]{{display:none!important}}</style>
</head>
<body>
'''
    os.makedirs(os.path.join(HERE, out), exist_ok=True)
    if out in DEMO_INFO:
        body += DEMO_NAV.replace('__COL__', DEMO_INFO[out][0]).replace('__DIS__', DEMO_INFO[out][1]).replace('__DISN__', DIS_NAMES.get(DEMO_INFO[out][1], ''))
        body += FREEZE
    open(os.path.join(HERE, out, 'index.html'), 'w', encoding='utf-8').write(head + body + '\n</body>\n</html>\n')
    print('built', out or '(root)')

# always finish with the collections step (it fills the home page and "Crea la tuya" with the collections)
import subprocess, sys
subprocess.run([sys.executable, os.path.join(HERE, 'experiencias.py')], check=True)
subprocess.run([sys.executable, os.path.join(HERE, 'colecciones.py')], check=True)

# ilusioninvites.com -> the new site (/nuevo/). Keeps a nice link preview for the bare domain.
ROOT = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ilusión Invites · Invitaciones digitales de lujo</title>
<meta name="description" content="Invitaciones digitales de lujo para bodas, XV años, baby showers, cumpleaños, galas, posadas y Año Nuevo. México y Canadá.">
<meta property="og:title" content="Ilusión Invites · Invitaciones digitales de lujo">
<meta property="og:description" content="Invitaciones digitales de lujo para bodas, XV años, baby showers, cumpleaños, galas, posadas y Año Nuevo. México y Canadá.">
<meta property="og:image" content="{BASE}/nuevo/img/ilusion-logo.jpg">
<meta property="og:url" content="{BASE}/nuevo/">
<link rel="canonical" href="{BASE}/nuevo/">
<link rel="icon" href="nuevo/img/ilusion-logo.jpg">
<meta http-equiv="refresh" content="0; url=/nuevo/">
<script>location.replace('/nuevo/' + location.search + location.hash);</script>
<style>body{{margin:0;background:#FBF6EF;font-family:Georgia,serif;display:grid;place-items:center;min-height:100vh;color:#3A2A26}}a{{color:#B68A4E}}</style>
</head>
<body><p><a href="/nuevo/">Ilusión Invites ✨</a></p></body>
</html>
"""
open(os.path.join(HERE, 'index.html'), 'w', encoding='utf-8').write(ROOT)
print('built / -> /nuevo/')
