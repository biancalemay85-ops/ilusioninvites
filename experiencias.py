"""Builds one "La experiencia ..." page per collection (same design as the XV page, website/experiencia-xv.html).

Run automatically by build.py. Edit the texts, names, colors and photo positions in EXP below.
Photos live in nuevo/img/exp-<slug>-<pantalla|letrero|pieza|selfie>.webp (originals in brand/assets/mockups/).
Positions (x, y, w, h in %) say where our design sits on the blank screen / sign / printed piece of each photo.
All names are fictional.
"""
import os, re, json, html

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = 'https://ilusioninvites.com'
XV = open(os.path.join(HERE, '../website/experiencia-xv.html'), encoding='utf-8').read()
CSS = re.search(r'<style>(.*?)</style>', XV, re.S).group(1)
COLS = json.load(open(os.path.join(HERE, '../website/colecciones.json'), encoding='utf-8'))['colecciones']


def T(es, en, tag='span', cls='', attrs=''):
    c = f' class="{cls}"' if cls else ''
    return f'<{tag}{c}{attrs} data-en-html="{html.escape(en, quote=True)}">{es}</{tag}>'


WHERE = {
    'pases': [('ILUSIÓN', 'ILUSIÓN', 0), ('GALA', 'GALA', 0), ('EXPERIENCIA', 'EXPERIENCIA', 0)],
    'lista': [('ILUSIÓN', 'ILUSIÓN', 0), ('GALA', 'GALA', 0), ('EXPERIENCIA', 'EXPERIENCIA', 0)],
    'rec': [('GALA', 'GALA', 0), ('EXPERIENCIA', 'EXPERIENCIA', 0), ('O AGRÉGALO A TU PAQUETE', 'OR ADD IT TO YOUR PACKAGE', 1)],
    'video': [('ILUSIÓN · VIDEO INVITACIÓN', 'ILUSIÓN · VIDEO INVITATION', 0), ('O AGRÉGALO', 'OR ADD IT', 1)],
    'song': [('EXPERIENCIA', 'EXPERIENCIA', 0), ('O AGRÉGALA A TU PAQUETE', 'OR ADD IT TO YOUR PACKAGE', 1)],
    'marco': [('GALA · QR DE FOTOS', 'GALA · PHOTO QR', 0), ('EXPERIENCIA', 'EXPERIENCIA', 0), ('O AGRÉGALO', 'OR ADD IT', 1)],
    'pap': [('GALA · 3 PIEZAS', 'GALA · 3 PIECES', 0), ('EXPERIENCIA · TODAS', 'EXPERIENCIA · ALL', 0), ('O AGRÉGALAS', 'OR ADD THEM', 1)],
}


def where(k):
    return '<div class="where">' + ''.join(T(es, en, 'span', 'add' if add else '') for es, en, add in WHERE[k]) + '</div>'


def steps(lst):
    return '<ol class="steps">' + ''.join(T(es, en, 'li') for es, en in lst) + '</ol>'


def txt(num, sec):
    h2 = T(sec['h2'][0], sec['h2'][1], 'h2')
    return (f'<div class="txt">{T(num[0], num[1], "span", "num")}{h2}{T(sec["p"][0], sec["p"][1], "p")}'
            + (steps(sec['steps']) if sec.get('steps') else '') + where(sec['where']) + '</div>')


GEN = {
    'lista': {'h2': ('Sabes quién viene, <em>sin llamar a nadie</em>', 'Know who is coming, <em>without calling anyone</em>'),
              'p': ('Cada confirmación llega sola a tu lista privada, con el número de personas y su mensaje. La abres desde tu celular cuando quieras y se actualiza en vivo.',
                    'Every RSVP lands in your private list by itself, with the number of people and their message. Open it on your phone anytime: it updates live.'),
              'steps': [('Tus invitados confirman desde la invitación.', 'Your guests confirm from the invitation.'),
                        ('Tu lista se llena sola: confirmados, pendientes y quién no podrá ir.', "Your list fills itself: confirmed, pending and who can't come."),
                        ('Ideal para el salón y el banquete: el número exacto de lugares.', 'Perfect for the venue and catering: the exact number of seats.')], 'where': 'lista'},
    'pases': {'h2': ('Cada familia, <em>su propia invitación</em>', 'Every family, <em>its own invitation</em>'),
              'p': ('Cada invitado recibe un link con su nombre en el sobre y los lugares que le reservaste. Sin imprimir nada: nadie agrega personas de más.',
                    'Each guest gets a link with their name on the envelope and the seats you saved for them. Nothing to print: nobody adds extra people.'),
              'steps': [('Nos mandas tu lista: nombre, teléfono y lugares.', 'You send us your list: name, phone and seats.'),
                        ('Creamos un link para cada invitado y su mensaje de WhatsApp listo.', 'We create a link for each guest and its ready WhatsApp message.'),
                        ('Tú solo lo envías. Ellos confirman con un toque.', 'You just send it. They confirm with one tap.')], 'where': 'pases'},
    'rec': {'h2': ('Nadie se olvida <em>de tu día</em>', 'Nobody forgets <em>your day</em>'),
            'p': ('Mensajes por WhatsApp que salen solos: una semana antes, un día antes y dos horas antes con el mapa. Y un recordatorio amable a quien aún no confirma. En español, inglés o los dos.',
                  "WhatsApp messages that go out by themselves: a week before, a day before and two hours before with the map. Plus a kind nudge to anyone who hasn't confirmed. In Spanish, English or both."), 'where': 'rec'},
    'marco': {'h2': ('Cada foto, <em>con tu estilo</em>', 'Every photo, <em>in your style</em>'),
              'p': ('En cada mesa hay una tarjeta con un código QR. Tus invitados lo escanean, se toman una foto y sale con tu marco y tu nombre en oro, lista para Instagram o WhatsApp. Todas sus fotos y videos llegan a tu álbum, y te damos un link para descargarlas.',
                    'Each table has a card with a QR code. Guests scan it, take a photo and it comes out with your frame and your name in gold, ready for Instagram or WhatsApp. All their photos and videos land in your album, and you get a link to download them.'),
              'steps': [('Escanean el QR de su mesa con la cámara del celular.', "They scan their table's QR with the phone camera."),
                        ('Se toman la foto: aparece con tu marco al instante.', 'They take the photo: your frame appears instantly.'),
                        ('Tú recibes todas las fotos y videos en un solo link.', 'You receive every photo and video in one link.')], 'where': 'marco'},
    'pap': {'h2': ('Tu evento, <em>con el mismo estilo</em>', 'Your event, <em>in the same style</em>'),
            'p': ('Diseñamos las piezas impresas de tu evento con los mismos colores, flores y letra dorada de tu invitación. Te entregamos los archivos listos para imprimir donde tú prefieras.',
                  'We design the printed pieces of your event with the same colors, flowers and gold lettering as your invitation. You get print-ready files to print wherever you like.'), 'where': 'pap'},
}

# ---------------------------------------------------------------- per collection
EXP = {
 'bodas': {
  'theme': ['#FBF6EF', '#F3EADD', '#FDFAF5', '#B68A4E', '#3A2A26', '#6E5B54', '#9A877F'], 'hero': 'hero-bodas', 'seal': 'sello-marfil', 'decos': ['rosa-marfil', 'hortensia-marfil', 'cristal-1'],
  'eyebrow': ('LA EXPERIENCIA BODA', 'THE WEDDING EXPERIENCE'), 'h1': ('Todo lo que vive <span class="gold">su gran día</span>', 'Everything <span class="gold">your big day</span> holds'),
  'intro': ('Así se ve cada detalle que podemos crear para su boda, en el mismo estilo de su invitación: marfil, oro y flores blancas. Los nombres son de ejemplo.', 'This is how every detail we can create for your wedding looks, in the same style as your invitation: ivory, gold and white flowers. Names are examples.'),
  'who': ('NUESTRA BODA · ANA & EMILIANO', 'OUR WEDDING · ANA & EMILIANO'), 'para': ('Para: Familia López', 'For: The López Family'),
  'seats': ('Con mucho cariño reservamos<br><b>4 lugares</b> para ustedes', 'With love, we saved<br><b>4 seats</b> for you'),
  'btns': [('Confirmar 4 lugares', 'Confirm 4 seats'), ('Seremos menos', 'We will be fewer'), ('No podremos ir', "We can't make it")],
  'bubble': ('Hola Familia López 💌 Con mucho cariño les compartimos la invitación a nuestra boda:', 'Hi López family 💌 With love, here is the invitation to our wedding:'), 'link': 'ilusioninvites.com/ana-y-emiliano?para=familia-lopez',
  'list': (('Nuestros invitados', 'Our guests'), ('BODA DE ANA & EMILIANO · EN VIVO', "ANA & EMILIANO'S WEDDING · LIVE"), [142, 31, 9]),
  'rows': [('Familia Torres', 'ok', 3), ('Familia López', 'ok', 4), ('Tía Carmen', 'ok', 2), ('Familia Ruiz', 'wait', 0), ('Sofía y Andrés', 'ok', 2), ('Familia Méndez', 'no', 0), ('Padrinos Ortega', 'ok', 2), ('Familia Castro', 'wait', 0)],
  'chat': ('Boda Ana & Emiliano', [('7 de marzo', 'March 7'), ('FALTA UNA SEMANA', 'ONE WEEK TO GO', '¡Hola Familia López! ✨ Falta una semana para nuestra boda. Aquí tienen su invitación, la ubicación y la mesa de regalos.', 'Hi López family! ✨ One week until our wedding. Here are your invitation, the location and the gift registry.'),
           ('16 de abril', 'April 16'), ('ES MAÑANA', "IT'S TOMORROW", 'Mañana es el gran día 💍 Ceremonia 5:00 pm, recepción 7:30 pm. Vestimenta: formal.', 'Tomorrow is the big day 💍 Ceremony 5:00 pm, reception 7:30 pm. Dress code: formal.'),
           ('me', '¡Ahí estaremos! 🥂', "We'll be there! 🥂"), ('17 de abril', 'April 17'), ('EN 2 HORAS', 'IN 2 HOURS', 'Los esperamos a las 5:00 pm en Hacienda Los Olivos. Toquen aquí para el mapa 📍', 'See you at 5:00 pm at Hacienda Los Olivos. Tap here for directions 📍')]),
  'video': {'num': ('VIDEO DE BIENVENIDA Y SAVE THE DATE', 'WELCOME VIDEO & SAVE THE DATE'), 'h2': ('Su historia, <em>en la pantalla grande</em>', 'Your story, <em>on the big screen</em>'),
            'p': ('Un video con sus fotos de novios, sus nombres en oro y su canción, para recibir a los invitados o antes del primer baile. Y su versión corta para el celular: el save the date de 15 a 30 segundos para WhatsApp e Instagram.',
                  'A video with your couple photos, your names in gold and your song, to welcome guests or play before the first dance. Plus a short phone version: a 15–30 second save the date for WhatsApp and Instagram.'),
            'screen': (('NOS CASAMOS', "WE'RE GETTING MARRIED"), 'Ana & Emiliano')},
  'song': {'h2': ('Una canción <em>para su primer baile</em>', 'A song <em>for your first dance</em>'), 'art': 'cat-bodas', 'name': 'Ana & Emiliano', 'title': ('Para siempre contigo', 'Forever with You'), 'by': ('Hecha para Ana Sofía y Emiliano', 'Made for Ana Sofía and Emiliano'),
           'lyrics': ('“Te encontré en un día cualquiera<br>y el mundo se volvió canción;<br><em>hoy te elijo, Ana Sofía</em>,<br>para siempre, mi amor.”', '“I found you on an ordinary day<br>and the world became a song;<br><em>today I choose you, Ana Sofía</em>,<br>forever, my love.”'),
           'styles': [('Balada romántica', 'Romantic ballad'), ('Español', 'Spanish'), ('Con su historia', 'With your story')],
           'p': ('Escribimos una canción original con sus nombres y su historia: cómo se conocieron, lo que los hace únicos. En el estilo que les guste y en español, inglés o los dos. Les mandamos dos versiones para elegir, y suena en su invitación y en su primer baile.',
                 'We write an original song with your names and your story: how you met, what makes you unique. In the style you love and in Spanish, English or both. You get two versions to choose from, and it plays in your invitation and at your first dance.')},
  'marco': (('NUESTRA BODA', 'OUR WEDDING'), 'Ana & Emiliano', '17 · 04 · 2027'),
  'sign': (('BIENVENIDOS A LA BODA DE', 'WELCOME TO THE WEDDING OF'), 'Ana & Emiliano', ('17 · ABRIL · 2027', 'APRIL 17 · 2027')),
  'piece': {'kind': 'mesa', 'small': ('MESA', 'TABLE'), 'big': ('Cinco', 'Five'), 'cap': ('NÚMERO DE MESA', 'TABLE NUMBER')},
  'chips': [('Letrero de bienvenida', 'Welcome sign'), ('Plano de mesas', 'Seating chart'), ('Números de mesa', 'Table numbers'), ('Tarjetas de lugar', 'Place cards'), ('Menú', 'Menu'), ('Programa de ceremonia', 'Ceremony program'),
            ('Letrero con hashtag y QR de fotos', 'Hashtag and photo QR sign'), ('Letrero “ceremonia sin celulares”', '“Unplugged ceremony” sign'), ('Menú de cócteles', 'Signature cocktail menu'), ('Tarjetas de agradecimiento', 'Thank-you cards'), ('Guía de viaje bilingüe', 'Bilingual travel guide')],
 },
 'cumpleanos': {
  'theme': ['#FBF5F6', '#EFE3EE', '#FDF9FB', '#A77FA0', '#3B2A3A', '#6A5568', '#9C8A9A'], 'hero': 'hero-cumpleanos', 'seal': 'sello-rubor', 'decos': ['rosa-rubor', 'rosa-marfil', 'mariposa-dorada-1'],
  'eyebrow': ('LA EXPERIENCIA CUMPLEAÑOS', 'THE BIRTHDAY EXPERIENCE'), 'h1': ('Todo lo que vive <span class="gold">tu celebración</span>', 'Everything <span class="gold">your celebration</span> holds'),
  'intro': ('Así se ve cada detalle que podemos crear para tu cumpleaños, en el mismo estilo de tu invitación: lila, rubor y oro. Los nombres son de ejemplo.', 'This is how every detail we can create for your birthday looks, in the same style as your invitation: lilac, blush and gold. Names are examples.'),
  'who': ('MIS 30 AÑOS · MARIANA', "MARIANA'S 30TH"), 'para': ('Para: Sofía y Andrés', 'For: Sofía & Andrés'),
  'seats': ('Con mucho cariño reservamos<br><b>2 lugares</b> para ustedes', 'With love, we saved<br><b>2 seats</b> for you'),
  'btns': [('Confirmar 2 lugares', 'Confirm 2 seats'), ('Iré yo solo', 'Just me'), ('No podremos ir', "We can't make it")],
  'bubble': ('Hola Sofía y Andrés 🎉 Los invito a celebrar mis 30:', 'Hi Sofía & Andrés 🎉 Come celebrate my 30th:'), 'link': 'ilusioninvites.com/mariana-30?para=sofia-y-andres',
  'list': (('Mis invitados', 'My guests'), ('CUMPLEAÑOS DE MARIANA · EN VIVO', "MARIANA'S BIRTHDAY · LIVE"), [48, 12, 3]),
  'rows': [('Sofía y Andrés', 'ok', 2), ('Laura Méndez', 'ok', 1), ('Familia Ruiz', 'ok', 3), ('Diego y Paola', 'wait', 0), ('Tía Carmen', 'ok', 2), ('Javier Soto', 'no', 0), ('Ana y Luis', 'ok', 2), ('Regina Castro', 'wait', 0)],
  'chat': ('Cumple de Mariana', [('15 de agosto', 'August 15'), ('FALTA UNA SEMANA', 'ONE WEEK TO GO', '¡Hola! 🎉 Falta una semana para los 30 de Mariana. Aquí está tu invitación y la ubicación.', "Hi! 🎉 One week until Mariana's 30th. Here are your invitation and the location."),
           ('21 de agosto', 'August 21'), ('ES MAÑANA', "IT'S TOMORROW", 'Mañana celebramos 🥂 Cena 8:00 pm. Vestimenta: cóctel.', "Tomorrow we celebrate 🥂 Dinner 8:00 pm. Dress code: cocktail."),
           ('me', '¡No me lo pierdo! 🎂', "Wouldn't miss it! 🎂"), ('22 de agosto', 'August 22'), ('EN 2 HORAS', 'IN 2 HOURS', '¡Hoy es el día! Te esperamos a las 8:00 pm en Casa Jardín 📍', 'Today is the day! See you at 8:00 pm at Casa Jardín 📍')]),
  'video': {'num': ('VIDEO INVITACIÓN Y VIDEO DE LA FIESTA', 'VIDEO INVITATION & PARTY VIDEO'), 'h2': ('Tu celebración, <em>en video</em>', 'Your celebration, <em>on video</em>'),
            'p': ('Un video invitación de 15 a 30 segundos para enviar por WhatsApp e Instagram, y un video para proyectar en la fiesta con las fotos de tu vida y tus mejores momentos.',
                  'A 15–30 second video invitation to send on WhatsApp and Instagram, and a video to play at the party with photos of your life and best moments.'),
            'screen': (('CELEBREMOS', "LET'S CELEBRATE"), 'Mariana · 30')},
  'song': {'h2': ('Una canción <em>para tu día</em>', 'A song <em>for your day</em>'), 'art': 'cumpleanos-ej1', 'name': 'Mariana', 'title': ('Treinta velas', 'Thirty Candles'), 'by': ('Hecha para los 30 de Mariana', "Made for Mariana's 30th"),
           'lyrics': ('“Treinta velas y una risa<br>que ilumina este lugar;<br><em>esta noche es tuya, Mariana</em>,<br>que empiece a celebrar.”', '“Thirty candles and a laugh<br>that lights up all the room;<br><em>tonight is yours, Mariana</em>,<br>let the party bloom.”'),
           'styles': [('Pop alegre', 'Upbeat pop'), ('Español', 'Spanish'), ('Con tu historia', 'With your story')],
           'p': ('Escribimos una canción original con tu nombre y tu historia, en el estilo que te guste y en español, inglés o los dos. Te mandamos dos versiones para elegir, y suena en tu invitación y en tu fiesta.',
                 'We write an original song with your name and your story, in the style you love and in Spanish, English or both. You get two versions to choose from, and it plays in your invitation and at your party.')},
  'marco': (('MIS 30 AÑOS', 'MY 30TH'), 'Mariana', '22 · 08 · 2027'),
  'sign': (('BIENVENIDOS A LOS 30 DE', "WELCOME TO THE 30TH OF"), 'Mariana', ('22 · AGOSTO · 2027', 'AUGUST 22 · 2027')),
  'piece': {'kind': 'mesa', 'small': ('MESA DE', 'THE'), 'big': ('Dulces', 'Sweets'), 'cap': ('TARJETA DE MESA DE DULCES', 'DESSERT TABLE CARD')},
  'chips': [('Letrero de bienvenida', 'Welcome sign'), ('Tarjetas de mesa', 'Table cards'), ('Accesorios para fotos', 'Photo booth props'), ('Etiquetas para recuerdos', 'Favor tags'), ('Topper para pastel', 'Cake topper'), ('Menú', 'Menu'), ('Reel resumen de la fiesta', 'Party recap reel')],
 },
 'baby-shower': {
  'theme': ['#F5F8FB', '#E6EEF5', '#FAFCFE', '#6F8DB3', '#2E3B4B', '#5C6B7C', '#8C9AAA'], 'hero': 'hero-baby-shower', 'seal': 'sello-marino', 'decos': ['nube-gypsophila', 'rosa-marfil', 'cristal-1'],
  'eyebrow': ('LA EXPERIENCIA BABY SHOWER', 'THE BABY SHOWER EXPERIENCE'), 'h1': ('Todo lo que vive <span class="gold">su llegada</span>', 'Everything <span class="gold">their arrival</span> holds'),
  'intro': ('Así se ve cada detalle que podemos crear para tu baby shower, en el mismo estilo de tu invitación: azul cielo, nubes y oro suave. Los nombres son de ejemplo.', 'This is how every detail we can create for your baby shower looks, in the same style as your invitation: sky blue, clouds and soft gold. Names are examples.'),
  'who': ('BABY SHOWER · MATEO', 'BABY SHOWER · MATEO'), 'para': ('Para: Tía Carmen', 'For: Aunt Carmen'),
  'seats': ('Con mucho cariño reservamos<br><b>2 lugares</b> para ti', 'With love, we saved<br><b>2 seats</b> for you'),
  'btns': [('Confirmar 2 lugares', 'Confirm 2 seats'), ('Iré yo sola', 'Just me'), ('No podré ir', "I can't make it")],
  'bubble': ('Hola Tía Carmen 💙 Te invitamos al baby shower de Mateo:', "Hi Aunt Carmen 💙 You're invited to Mateo's baby shower:"), 'link': 'ilusioninvites.com/bebe-mateo?para=tia-carmen',
  'list': (('Invitados', 'Guests'), ('BABY SHOWER DE MATEO · EN VIVO', "MATEO'S BABY SHOWER · LIVE"), [36, 9, 2]),
  'rows': [('Tía Carmen', 'ok', 2), ('Abuela Rosa', 'ok', 1), ('Familia Ruiz', 'ok', 3), ('Laura y Diego', 'wait', 0), ('Paola Soto', 'ok', 1), ('Familia Méndez', 'no', 0), ('Ana y Luis', 'ok', 2), ('Regina Castro', 'wait', 0)],
  'chat': ('Baby shower de Mateo', [('5 de abril', 'April 5'), ('FALTA UNA SEMANA', 'ONE WEEK TO GO', '¡Hola! 💙 Falta una semana para el baby shower de Mateo. Aquí está tu invitación y la mesa de regalos.', "Hi! 💙 One week until Mateo's baby shower. Here are your invitation and the gift registry."),
           ('11 de abril', 'April 11'), ('ES MAÑANA', "IT'S TOMORROW", 'Mañana nos vemos ☁️ 4:00 pm. ¡No olvides tu consejo para los papás!', "See you tomorrow ☁️ 4:00 pm. Don't forget your advice for the parents!"),
           ('me', '¡Ahí estaré! 🍼', "I'll be there! 🍼"), ('12 de abril', 'April 12'), ('EN 2 HORAS', 'IN 2 HOURS', 'Te esperamos a las 4:00 pm en Casa Nube. Toca aquí para el mapa 📍', 'See you at 4:00 pm at Casa Nube. Tap here for directions 📍')]),
  'video': {'num': ('VIDEO RECUERDO PARA EL BEBÉ', 'KEEPSAKE VIDEO FOR THE BABY'), 'h2': ('Un recuerdo <em>para toda la vida</em>', 'A keepsake <em>for a lifetime</em>'),
            'p': ('Un video con las ecografías, las fotos de la espera y los mensajes de la familia, para proyectar en el baby shower y guardar para cuando el bebé crezca. Y su versión corta para invitar por WhatsApp.',
                  'A video with the ultrasounds, the waiting photos and family messages, to play at the baby shower and keep for when the baby grows up. Plus a short version to invite on WhatsApp.'),
            'screen': (('BIENVENIDO', 'WELCOME'), 'Mateo')},
  'song': {'h2': ('Una canción de cuna <em>con su nombre</em>', 'A lullaby <em>with their name</em>'), 'art': 'baby-shower-ej1', 'name': 'Mateo', 'title': ('Duerme, Mateo', 'Sleep, Mateo'), 'by': ('Hecha para el bebé Mateo', 'Made for baby Mateo'),
           'lyrics': ('“Duerme, Mateo, que el cielo te cuida,<br>nubes de algodón para ti;<br><em>llegaste a llenar nuestra vida</em>,<br>y aquí estaremos por ti.”', '“Sleep, little Mateo, the sky keeps you near,<br>soft cotton clouds just for you;<br><em>you came to fill all our days</em>,<br>and we\'ll always be here for you.”'),
           'styles': [('Canción de cuna', 'Lullaby'), ('Español', 'Spanish'), ('Para el bebé', 'For the baby')],
           'p': ('Una canción de cuna original con el nombre del bebé y la historia de su familia, en español, inglés o los dos. Suena en la invitación, en el baby shower y se queda para arrullarlo.',
                 "An original lullaby with the baby's name and the family's story, in Spanish, English or both. It plays in the invitation, at the shower, and stays to sing them to sleep.")},
  'marco': (('BABY SHOWER', 'BABY SHOWER'), 'Mateo', '12 · 04 · 2027'),
  'sign': (('BIENVENIDOS AL BABY SHOWER DE', 'WELCOME TO THE BABY SHOWER OF'), 'Mateo', ('12 · ABRIL · 2027', 'APRIL 12 · 2027')),
  'piece': {'kind': 'loteria', 'small': ('LOTERÍA DEL', 'BABY'), 'big': ('Bebé', 'Bingo'), 'cap': ('JUEGO PARA LOS INVITADOS', 'GAME FOR GUESTS'),
            'grid': [('Biberón', 'Bottle'), ('Chupón', 'Pacifier'), ('Cuna', 'Crib'), ('Osito', 'Teddy'), ('Pañal', 'Diaper'), ('Sonaja', 'Rattle'), ('Babero', 'Bib'), ('Carriola', 'Stroller'), ('Cobija', 'Blanket')]},
  'chips': [('Letrero de bienvenida', 'Welcome sign'), ('Lotería y juegos', 'Bingo and games'), ('Adivina el bebé', 'Guess the baby'), ('Boletos para rifa de pañales', 'Diaper raffle tickets'), ('Tarjetas “consejos para los papás”', '“Advice for the parents” cards'), ('Etiquetas para recuerdos', 'Favor tags'), ('Tarjeta de mesa de regalos', 'Gift registry card')],
 },
 'navidad': {
  'theme': ['#F6F4EE', '#EAE6DA', '#FBFAF6', '#2F5A43', '#1F2E25', '#4D5C52', '#7F8A82'], 'hero': 'hero-navidad-posadas', 'seal': 'sello-esmeralda', 'decos': ['ramita-hojas-doradas', 'peonia-vino', 'cristal-1'],
  'eyebrow': ('LA EXPERIENCIA POSADA', 'THE CHRISTMAS EXPERIENCE'), 'h1': ('Todo lo que vive <span class="gold">tu posada</span>', 'Everything <span class="gold">your Christmas party</span> holds'),
  'intro': ('Así se ve cada detalle que podemos crear para tu posada o cena navideña, en el mismo estilo de tu invitación: verde profundo, rojo y oro. Los nombres son de ejemplo.', 'This is how every detail we can create for your Christmas party or dinner looks, in the same style as your invitation: deep green, red and gold. Names are examples.'),
  'who': ('POSADA · FAMILIA HERNÁNDEZ', 'CHRISTMAS PARTY · THE HERNÁNDEZ FAMILY'), 'para': ('Para: Familia Ruiz', 'For: The Ruiz Family'),
  'seats': ('Con mucho cariño reservamos<br><b>5 lugares</b> para ustedes', 'With love, we saved<br><b>5 seats</b> for you'),
  'btns': [('Confirmar 5 lugares', 'Confirm 5 seats'), ('Seremos menos', 'We will be fewer'), ('No podremos ir', "We can't make it")],
  'bubble': ('Hola Familia Ruiz 🎄 Los esperamos en nuestra posada:', 'Hi Ruiz family 🎄 Join us at our Christmas party:'), 'link': 'ilusioninvites.com/posada-hernandez?para=familia-ruiz',
  'list': (('Invitados', 'Guests'), ('POSADA HERNÁNDEZ · EN VIVO', 'HERNÁNDEZ PARTY · LIVE'), [64, 18, 4]),
  'rows': [('Familia Ruiz', 'ok', 5), ('Tía Carmen', 'ok', 2), ('Familia Torres', 'ok', 4), ('Los García', 'wait', 0), ('Abuelos Ortega', 'ok', 2), ('Familia Méndez', 'no', 0), ('Primos Castro', 'ok', 3), ('Laura y Diego', 'wait', 0)],
  'chat': ('Posada Hernández', [('9 de diciembre', 'December 9'), ('FALTA UNA SEMANA', 'ONE WEEK TO GO', '¡Hola Familia Ruiz! 🎄 Falta una semana para la posada. Recuerden su regalo para el intercambio (hasta $300).', 'Hi Ruiz family! 🎄 One week until the party. Remember your gift for the exchange (up to $300).'),
           ('15 de diciembre', 'December 15'), ('ES MAÑANA', "IT'S TOMORROW", 'Mañana es la posada ✨ 7:00 pm. Habrá piñata, ponche y villancicos.', "Tomorrow is the party ✨ 7:00 pm. There will be a piñata, ponche and carols."),
           ('me', '¡Ahí estaremos con todo y regalo! 🎁', "We'll be there, gift and all! 🎁"), ('16 de diciembre', 'December 16'), ('EN 2 HORAS', 'IN 2 HOURS', 'Los esperamos a las 7:00 pm en casa de los Hernández. Toquen aquí para el mapa 📍', "See you at 7:00 pm at the Hernández home. Tap here for directions 📍")]),
  'video': {'num': ('VIDEO DEL AÑO EN FAMILIA', 'FAMILY YEAR-IN-REVIEW VIDEO'), 'h2': ('El año de la familia, <em>en la pantalla</em>', "The family's year, <em>on the screen</em>"),
            'p': ('Un video con las fotos del año de la familia para proyectar durante la cena o antes del brindis, con música navideña. Y su versión corta para invitar por WhatsApp.',
                  "A video with the family's photos of the year to play during dinner or before the toast, with Christmas music. Plus a short version to invite on WhatsApp."),
            'screen': (('POSADA NAVIDEÑA', 'CHRISTMAS PARTY'), 'Familia Hernández')},
  'marco': (('POSADA NAVIDEÑA', 'CHRISTMAS PARTY'), 'Familia Hernández', '16 · 12 · 2027'),
  'sign': (('BIENVENIDOS A LA POSADA DE LA', 'WELCOME TO THE CHRISTMAS PARTY OF THE'), 'Familia Hernández', ('16 · DICIEMBRE · 2027', 'DECEMBER 16 · 2027')),
  'piece': {'kind': 'mesa', 'small': ('TU LUGAR', 'YOUR SEAT'), 'big': ('Tía Carmen', 'Aunt Carmen'), 'cap': ('TARJETA DE LUGAR', 'PLACE CARD')},
  'chips': [('Letrero de bienvenida', 'Welcome sign'), ('Menú navideño', 'Christmas menu'), ('Tarjetas de lugar', 'Place cards'), ('Tarjetas para intercambio de regalos', 'Gift exchange cards'), ('Cancionero de posada', 'Carol booklet'), ('Boletos para rifa', 'Raffle tickets'), ('Álbum familiar con QR', 'Family photo album with QR')],
 },
 'ano-nuevo': {
  'theme': ['#F7F4EE', '#ECE5D8', '#FCFAF6', '#9A7A3E', '#1C1B20', '#4F4B52', '#85808A'], 'hero': 'hero-ano-nuevo', 'seal': 'sello-ilusion-oro-s', 'decos': ['cristal-1', 'ramita-hojas-doradas', 'cristal-1'],
  'eyebrow': ('LA EXPERIENCIA AÑO NUEVO', "THE NEW YEAR'S EVE EXPERIENCE"), 'h1': ('Todo lo que vive <span class="gold">tu medianoche</span>', 'Everything <span class="gold">your midnight</span> holds'),
  'intro': ('Así se ve cada detalle que podemos crear para tu fiesta de Año Nuevo, en el mismo estilo de tu invitación: negro, champaña y destellos dorados. Los nombres son de ejemplo.', "This is how every detail we can create for your New Year's Eve party looks, in the same style as your invitation: black, champagne and gold sparkle. Names are examples."),
  'who': ('AÑO NUEVO · VALERIA & ANDRÉS', "NEW YEAR'S EVE · VALERIA & ANDRÉS"), 'para': ('Para: Sofía y Daniel', 'For: Sofía & Daniel'),
  'seats': ('Con mucho cariño reservamos<br><b>2 lugares</b> para ustedes', 'With love, we saved<br><b>2 seats</b> for you'),
  'btns': [('Confirmar 2 lugares', 'Confirm 2 seats'), ('Iré yo solo', 'Just me'), ('No podremos ir', "We can't make it")],
  'bubble': ('Hola Sofía y Daniel ✨ Los invitamos a recibir el 2028 con nosotros:', 'Hi Sofía & Daniel ✨ Ring in 2028 with us:'), 'link': 'ilusioninvites.com/ano-nuevo-2028?para=sofia-y-daniel',
  'list': (('Invitados', 'Guests'), ('AÑO NUEVO 2028 · EN VIVO', "NEW YEAR'S EVE 2028 · LIVE"), [72, 15, 5]),
  'rows': [('Sofía y Daniel', 'ok', 2), ('Laura Méndez', 'ok', 1), ('Familia Torres', 'ok', 4), ('Diego y Paola', 'wait', 0), ('Ana y Luis', 'ok', 2), ('Javier Soto', 'no', 0), ('Regina y Pablo', 'ok', 2), ('Familia Castro', 'wait', 0)],
  'chat': ('Año Nuevo con Valeria & Andrés', [('24 de diciembre', 'December 24'), ('FALTA UNA SEMANA', 'ONE WEEK TO GO', '¡Hola! ✨ Falta una semana para recibir el 2028 juntos. Aquí está tu invitación y la ubicación.', "Hi! ✨ One week until we ring in 2028 together. Here are your invitation and the location."),
           ('30 de diciembre', 'December 30'), ('ES MAÑANA', "IT'S TOMORROW", 'Mañana despedimos el año 🥂 Cena 9:00 pm. Vestimenta: dorado y negro.', 'Tomorrow we say goodbye to the year 🥂 Dinner 9:00 pm. Dress code: gold and black.'),
           ('me', '¡Listos para el brindis! 🍾', 'Ready for the toast! 🍾'), ('31 de diciembre', 'December 31'), ('EN 2 HORAS', 'IN 2 HOURS', 'Te esperamos a las 9:00 pm en Terraza Aurora. Toca aquí para el mapa 📍', 'See you at 9:00 pm at Terraza Aurora. Tap here for directions 📍')]),
  'video': {'num': ('CUENTA REGRESIVA EN PANTALLA', 'COUNTDOWN ON SCREEN'), 'h2': ('La medianoche, <em>en la pantalla grande</em>', 'Midnight, <em>on the big screen</em>'),
            'p': ('Una cuenta regresiva con sus nombres y fuegos artificiales dorados para proyectar en los últimos minutos del año, y un video invitación de 15 a 30 segundos para enviar por WhatsApp.',
                  'A countdown with your names and golden fireworks to play in the last minutes of the year, plus a 15–30 second video invitation to send on WhatsApp.'),
            'screen': (('FELIZ', 'HAPPY'), '2028')},
  'marco': (('AÑO NUEVO', "NEW YEAR'S EVE"), '2028', 'VALERIA & ANDRÉS'),
  'sign': (('BIENVENIDOS A RECIBIR EL', 'WELCOME TO'), '2028', ('31 · DICIEMBRE · 2027', 'DECEMBER 31 · 2027')),
  'piece': {'kind': 'mesa', 'small': ('BRINDIS DE', 'MIDNIGHT'), 'big': ('Medianoche', 'Toast'), 'cap': ('TARJETA PARA EL BRINDIS', 'TOAST CARD')},
  'chips': [('Letrero de bienvenida', 'Welcome sign'), ('Tarjetas de cuenta regresiva', 'Countdown cards'), ('Tarjetas para el brindis', 'Toast cards'), ('Menú', 'Menu'), ('Accesorios para fotos “2028”', '“2028” photo booth props'), ('Reel de medianoche', 'Midnight reel')],
 },
 'empresas': {
  'theme': ['#F4F5F8', '#E4E7EE', '#FAFBFC', '#2E3F66', '#1E2633', '#4E586A', '#8890A0'], 'hero': 'hero-gala-empresa', 'seal': 'sello-marino', 'decos': ['ramita-hojas-doradas', 'ramita-hojas-doradas', 'cristal-1'], 'corp': True,
  'eyebrow': ('LA EXPERIENCIA CORPORATIVA', 'THE CORPORATE EXPERIENCE'), 'h1': ('Todo lo que vive <span class="gold">tu evento</span>', 'Everything <span class="gold">your event</span> holds'),
  'intro': ('Así se ve cada detalle que podemos crear para tu gala, lanzamiento o evento de empresa, con el estilo de tu marca: azul noche y oro. Los nombres son de ejemplo.', 'This is how every detail we can create for your gala, launch or company event looks, in your brand style: midnight blue and gold. Names are examples.'),
  'who': ('GALA ANUAL · GRUPO AURORA', 'ANNUAL GALA · GRUPO AURORA'), 'para': ('Para: Andrea Torres', 'For: Andrea Torres'),
  'seats': ('Su pase de acceso<br><b>Mesa 4</b> · Lumière', 'Your access pass<br><b>Table 4</b> · Lumière'),
  'btns': [('Confirmar asistencia', 'Confirm attendance'), ('Iré con acompañante', 'Bringing a guest'), ('No podré asistir', "I can't attend")],
  'bubble': ('Estimada Andrea, es un honor invitarle a la Gala Anual de Grupo Aurora. Su invitación y pase:', "Dear Andrea, it is our honor to invite you to Grupo Aurora's Annual Gala. Your invitation and pass:"), 'link': 'ilusioninvites.com/gala-aurora?para=andrea-torres',
  'list': (('Asistentes', 'Attendees'), ('GALA GRUPO AURORA · EN VIVO', 'GRUPO AURORA GALA · LIVE'), [210, 45, 12]),
  'rows': [('Andrea Torres · Lumière', 'ok', 1), ('Luis Ortega · Casa Valle', 'ok', 2), ('Paola Ruiz · Nova', 'ok', 1), ('Diego Soto · Altum', 'wait', 0), ('Ana Méndez · Lumière', 'ok', 1), ('Jorge Castro · Kora', 'no', 0), ('Regina Paz · Aurora', 'ok', 2), ('Mario León · Vértice', 'wait', 0)],
  'chat': ('Gala Grupo Aurora', [('8 de noviembre', 'November 8'), ('FALTA UNA SEMANA', 'ONE WEEK TO GO', 'Estimada Andrea: falta una semana para la Gala Anual. Aquí está su pase QR y la ubicación.', 'Dear Andrea: one week until the Annual Gala. Here are your QR pass and the location.'),
           ('14 de noviembre', 'November 14'), ('ES MAÑANA', "IT'S TOMORROW", 'Mañana es la gala ✨ Registro 7:00 pm, cena 8:00 pm. Vestimenta: etiqueta.', 'The gala is tomorrow ✨ Check-in 7:00 pm, dinner 8:00 pm. Dress code: black tie.'),
           ('me', 'Confirmado, ahí estaré.', "Confirmed, I'll be there."), ('16 de noviembre', 'November 16'), ('GRACIAS', 'THANK YOU', 'Gracias por acompañarnos anoche, Andrea 🤍 Aquí están las fotos del evento y la presentación.', 'Thank you for joining us last night, Andrea 🤍 Here are the event photos and the presentation.')]),
  'pases': {'num': ('INVITACIÓN Y PASE CON QR', 'INVITATION & QR PASS'), 'h2': ('Cada invitado, <em>su pase de acceso</em>', 'Every guest, <em>their own access pass</em>'),
            'p': ('Cada invitado recibe su invitación con su nombre y un pase con código QR. En la entrada solo se escanea: registro en segundos y sabes quién llegó.',
                  'Each guest receives their invitation with their name and a QR pass. At the door it is just scanned: check-in in seconds, and you know who arrived.'),
            'steps': [('Nos mandas tu lista con nombre, empresa y correo.', 'You send us your list with name, company and email.'), ('Enviamos a cada uno su invitación y su pase QR.', 'We send each guest their invitation and QR pass.'), ('En la entrada se escanea el QR y queda registrado.', 'At the door the QR is scanned and check-in is recorded.')]},
  'listsec': {'num': ('LISTA DE ASISTENTES Y CONTACTOS', 'ATTENDEE & CONTACT LIST'), 'h2': ('Tus contactos, <em>listos al terminar</em>', 'Your contacts, <em>ready when it ends</em>'),
              'p': ('Cada confirmación llega con nombre, empresa y correo. Al terminar tienes la lista de asistentes para dar seguimiento, y un correo de agradecimiento sale solo al día siguiente.',
                    'Every RSVP arrives with name, company and email. When it ends you have the attendee list to follow up, and a thank-you email goes out by itself the next day.')},
  'video': {'num': ('PRESENTACIÓN Y VIDEO RESUMEN', 'PRESENTATION & RECAP VIDEO'), 'h2': ('Tu marca, <em>en la pantalla grande</em>', 'Your brand, <em>on the big screen</em>'),
            'p': ('Una presentación de bienvenida con tu marca para proyectar al inicio, y un video resumen con las fotos del evento para compartir después en redes y con tu equipo.',
                  'A welcome presentation with your brand to open the event, and a recap video with the event photos to share afterwards on social media and with your team.'),
            'screen': (('BIENVENIDOS', 'WELCOME'), 'Gala Aurora')},
  'marco': (('GALA ANUAL', 'ANNUAL GALA'), 'Grupo Aurora', '15 · 11 · 2027'),
  'sign': (('BIENVENIDOS A LA GALA ANUAL', 'WELCOME TO THE ANNUAL GALA'), 'Grupo Aurora', ('15 · NOVIEMBRE · 2027', 'NOVEMBER 15 · 2027')),
  'piece': {'kind': 'gafete', 'small': ('LUMIÈRE · INVITADA', 'LUMIÈRE · GUEST'), 'big': ('Andrea Torres', 'Andrea Torres'), 'cap': ('GAFETE CON NOMBRE Y QR', 'NAME BADGE WITH QR')},
  'chips': [('Letrero de bienvenida', 'Welcome sign'), ('Gafetes con nombre', 'Name badges'), ('Agenda del evento', 'Event agenda'), ('Números de mesa', 'Table numbers'), ('Señalización', 'Directional signs'), ('Reconocimientos y diplomas', 'Awards and certificates'), ('Marco de fotos con tu marca', 'Branded photo frame'), ('Correos de agradecimiento y seguimiento', 'Thank-you and follow-up emails')],
 },
}

# photo positions, filled after looking at each generated photo (x, y, w, h in %)
POS = json.load(open(os.path.join(HERE, 'experiencias-pos.json'), encoding='utf-8')) if os.path.exists(os.path.join(HERE, 'experiencias-pos.json')) else {}


def page(slug, d):
    pos = POS.get(slug, {})
    sc = pos.get('pantalla', [30, 30, 40, 40]); sg = pos.get('letrero', [34, 15, 32, 34]); pc = pos.get('pieza', [38, 40, 26, 36])
    img = lambda k: f'../../img/exp-{slug}-{k}.webp'
    th = d['theme']
    secs = []
    n = 0
    def num(es, en):
        nonlocal n; n += 1
        return (f'{n:02d} · {es}', f'{n:02d} · {en}')
    # 1 guest link / QR pass
    ps = d.get('pases', {})
    pz = dict(GEN['pases'], **{k: v for k, v in ps.items() if k != 'num'})
    pnum = num(*(ps.get('num') or ('LINK POR INVITADO', 'LINK PER GUEST')))
    card_inner = (f'<div class="qrp" data-qr="{BASE}/nuevo/"></div>' if d.get('corp') else f'<img class="fl" src="../../img/{d["decos"][0]}.webp" alt="">') + f'<img class="seal" src="../../img/{d["seal"]}.webp" alt="">'
    secs.append(f'''<section class="piece" id="pases"><div class="vis"><div class="phone"><div class="scr"><div class="env">
      {T(*d['who'], 'span', 'who')}{T(*d['para'], 'span', 'para gold')}<div class="card">{card_inner}</div>{T(*d['seats'], 'p', 'seats')}
      <div class="btns">{T(*d['btns'][0], 'span', 'y')}{T(*d['btns'][1], 'span', 'n')}{T(*d['btns'][2], 'span', 'n')}</div></div></div></div>
      <div class="bubble">{T(d['bubble'][0], d['bubble'][1])}<br><span class="l">{d['link']}</span><small>10:24 ✓✓</small></div></div>
      {txt(pnum, pz)}</section>''')
    # 2 RSVP list
    ls = d.get('listsec', {})
    lz = dict(GEN['lista'], **{k: v for k, v in ls.items() if k != 'num'})
    lnum = num(*(ls.get('num') or ('LISTA DE CONFIRMADOS', 'RSVP LIST')))
    (lt, lsub, k3) = d['list']
    st = {'ok': ('Confirmó · {n}', 'Confirmed · {n}', 'ok'), 'wait': ('Pendiente', 'Pending', 'wait'), 'no': ('No asistirá', 'Not coming', 'no')}
    NEW = ' class="new"'
    rows = ''.join(f'<div{NEW if i == 0 else ""}><b>{html.escape(nm)}</b>{T(st[s][0].format(n=c), st[s][1].format(n=c), "i", st[s][2])}</div>' for i, (nm, s, c) in enumerate(d['rows']))
    secs.append(f'''<section class="piece" id="lista"><div class="vis"><div class="phone tilt"><div class="scr"><div class="list">
      {T(*lt, 'h4')}{T(*lsub, 'span', 'sub')}
      <div class="kpis"><div><b>{k3[0]}</b>{T('CONFIRMADOS', 'CONFIRMED')}</div><div><b>{k3[1]}</b>{T('PENDIENTES', 'PENDING')}</div><div><b>{k3[2]}</b>{T('NO ASISTEN', 'NOT COMING')}</div></div>
      <div class="rows">{rows}</div></div></div></div></div>{txt(lnum, lz)}</section>''')
    # 3 reminders
    hdr, msgs = d['chat']
    ms = ''
    for m in msgs:
        if len(m) == 2: ms += T(m[0], m[1], 'span', 'daychip')
        elif m[0] == 'me': ms += f'<div class="msg me">{T(m[1], m[2])}<small>18:04 ✓✓</small></div>'
        else: ms += f'<div class="msg">{T(m[0], m[1], "span", "day")}{T(m[2], m[3])}<small>18:00</small></div>'
    rnum = num('RECORDATORIOS AUTOMÁTICOS', 'AUTOMATIC REMINDERS')
    secs.append(f'''<section class="piece" id="recordatorios"><div class="vis"><div class="phone"><div class="scr"><div class="chat">
      <div class="hd"><img src="../../img/sello-ilusion-oro-s.webp" alt=""><div><b>{html.escape(hdr)}</b>{T('mensaje automático', 'automatic message', 'small')}</div></div>
      <div class="ms">{ms}</div></div></div></div></div>{txt(rnum, GEN['rec'])}</section>''')
    # 4 video
    v = d['video']; vnum = num(*v['num'])
    vs = (v['screen'][0], v['screen'][1])
    onstyle = f'--sx:{sc[0]}%;--sy:{sc[1]}%;--sw:{sc[2]}%;--sh:{sc[3]}%;border-radius:2px'
    bgx = f'<div class="bgx" style="background-image:url(../../img/{d["hero"]}.webp)"></div>'
    secs.append(f'''<section class="piece" id="video"><div class="vis" style="flex-direction:column"><div class="screen"><img src="{img('pantalla')}" alt="" width="1600" height="900">
      <div class="on" style="{onstyle}">{bgx}<div class="tt">{T(*vs[0], 'small')}<b class="gold">{html.escape(vs[1])}</b></div></div>
      <div class="vphone"><div class="phone"><div class="scr" style="background:#1d1820"><div class="on" style="position:absolute;inset:0;--sx:0;--sy:0;--sw:100%;--sh:100%">{bgx}<div class="tt">{T(*vs[0], 'small')}<b class="gold">{html.escape(vs[1])}</b></div></div></div></div></div>
      </div></div>{txt(vnum, {'h2': v['h2'], 'p': v['p'], 'where': 'video'})}</section>''')
    # 5 song (optional)
    if d.get('song'):
        s = d['song']; snum = num('TU CANCIÓN PERSONALIZADA', 'YOUR PERSONALIZED SONG')
        secs.append(f'''<section class="piece" id="cancion"><div class="vis"><div class="player">
          <div class="art"><img src="../../img/{s['art']}.webp" alt=""><div class="ov">{T('CANCIÓN ORIGINAL', 'ORIGINAL SONG', 'small')}<b>{html.escape(s['name'])}</b></div></div>
          {T(*s['title'], 'h3')}{T(*s['by'], 'span', 'by')}<div class="bar"><i></i></div><div class="times"><span>1:12</span><span>3:05</span></div>
          <div class="ctrls"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6 6h2v12H6zM9.5 12L18 6v12z"/></svg><span class="pp"><span class="eq"><i></i><i></i><i></i><i></i></span></span><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16 6h2v12h-2zM6 6l8.5 6L6 18z"/></svg></div>
          {T(*s['lyrics'], 'p', 'lyrics')}<div class="styles">{''.join(T(a, b) for a, b in s['styles'])}</div></div></div>
          {txt(snum, {'h2': s['h2'], 'p': s['p'], 'where': 'song', 'steps': [('Nos cuentas su historia y el estilo que les gusta.', 'You tell us your story and the style you love.'), ('Te enviamos dos versiones para escuchar.', 'We send you two versions to listen to.'), ('Elegimos juntos y la ponemos en la invitación y el video.', 'We choose together and add it to the invitation and video.')]})}</section>''')
    # 6 guest photos + frame
    mk = d['marco']; mnum = num('FOTOS DE TUS INVITADOS', "YOUR GUESTS' PHOTOS")
    dec = d['decos']
    secs.append(f'''<section class="piece" id="marco"><div class="vis"><div class="phone"><div class="scr"><div class="ig">
      <div class="ph" style="background-image:url({img('selfie')})"></div>
      <div class="fr"><img class="f1" src="../../img/{dec[0]}.webp" alt=""><img class="f2" src="../../img/{dec[1]}.webp" alt=""><img class="bf" src="../../img/{dec[2]}.webp" alt=""></div>
      <div class="bar"><i></i></div><div class="user"><i></i>tu_mejor_amiga</div>
      <div class="lbl">{T(*mk[0], 'small')}<b>{html.escape(mk[1])}</b><span>{html.escape(mk[2])}</span></div></div></div></div>
      <div class="qrcard">{T('COMPARTE TU FOTO', 'SHARE YOUR PHOTO', 'small')}{T('en mi álbum', 'in my album', 'b')}<div class="qr" data-qr="{BASE}/nuevo/"></div>{T('ESCANEA AQUÍ', 'SCAN HERE', 'small')}</div></div>
      {txt(mnum, GEN['marco'])}</section>''')
    # 7 printables
    sgn = d['sign']; p = d['piece']; pnum2 = num('PAPELERÍA DEL EVENTO', 'EVENT PRINTABLES')
    if p['kind'] == 'loteria':
        rot = f'transform:rotate({pc[4]}deg);' if len(pc) > 4 else ''
        pin = f'''<div class="lay lot" style="--x:{pc[0]}%;--y:{pc[1]}%;--w:{pc[2]}%;--h:{pc[3]}%;{rot}">{T(*p['small'], 'small')}{T(*p['big'], 'b')}<div class="grid">{''.join(T(a, b) for a, b in p['grid'])}</div></div>'''
    elif p['kind'] == 'gafete':
        rot = f'transform:rotate({pc[4]}deg);' if len(pc) > 4 else ''
        pin = f'''<div class="lay badge" style="--x:{pc[0]}%;--y:{pc[1]}%;--w:{pc[2]}%;--h:{pc[3]}%;{rot}"><img class="bseal" src="../../img/sello-ilusion-oro-s.webp" alt=""><span class="evt">GRUPO AURORA</span><b>{html.escape(p['big'][0])}</b>{T(*p['small'], 'small')}<div class="qr" data-qr="{BASE}/nuevo/"></div></div>'''
    else:
        pin = f'''<div class="lay mesa" style="--x:{pc[0]}%;--y:{pc[1]}%;--w:{pc[2]}%;--h:{pc[3]}%"><img class="bfl" src="../../img/{dec[2]}.webp" alt="">{T(*p['small'], 'small')}{T(*p['big'], 'b', '', f' style="font-size:{min(10, 64 / max(len(p[chr(98)+chr(105)+chr(103)][0]), 1)):.1f}cqw"')}</div>'''
    chips = ''.join(T(a, b) for a, b in d['chips'])
    secs.append(f'''<section class="piece" id="papeleria"><div class="vis" style="flex-direction:column;gap:22px"><div class="pair">
      <figure style="margin:0"><div class="photo"><img src="{img('letrero')}" alt="" width="1200" height="1600">
        <div class="lay sign" style="--x:{sg[0]}%;--y:{sg[1]}%;--w:{sg[2]}%;--h:{sg[3]}%">{T(*sgn[0], 'small')}<b style="font-size:{min(8, 118 / max(len(sgn[1]), 1)):.1f}cqw">{html.escape(sgn[1])}</b><i class="rl"></i>{T(*sgn[2])}</div></div>
        {T('LETRERO DE BIENVENIDA', 'WELCOME SIGN', 'figcaption', 'cap')}</figure>
      <figure style="margin:0"><div class="photo"><img src="{img('pieza')}" alt="" width="1200" height="1200">{pin}</div>{T(*p['cap'], 'figcaption', 'cap')}</figure>
      </div></div>{txt(pnum2, GEN['pap'])[:-6]}<div class="all">{T('TODO LO QUE PODEMOS DISEÑAR PARA TI', 'EVERYTHING WE CAN DESIGN FOR YOU', 'span', 'all-t')}<div class="chips">{chips}</div></div></div></section>''')
    # other worlds
    others = ''.join(f'<a class="ow" href="../../coleccion/{c["slug"]}/"><span class="ar"><img src="../../img/{c["img"]}.webp" alt="" loading="lazy"></span>{T(html.escape(c["es"]["nombre"]), html.escape(c["en"]["nombre"]), "b")}</a>' for c in COLS if c['slug'] != slug)
    col = next(c for c in COLS if c['slug'] == slug)
    index = ''.join(f'<a href="#{i}">{T(a, b)}</a>' for i, a, b in [('pases', 'Link por invitado', 'Link per guest') if not d.get('corp') else ('pases', 'Pase con QR', 'QR pass'), ('lista', 'Lista de confirmados', 'RSVP list'), ('recordatorios', 'Recordatorios', 'Reminders'), ('video', 'Video', 'Video')] + ([('cancion', 'Tu canción', 'Your song')] if d.get('song') else []) + [('marco', 'Fotos de invitados', 'Guest photos'), ('papeleria', 'Papelería', 'Printables')])
    extra_css = f''':root {{ --bg: {th[0]}; --bg2: {th[1]}; --paper: {th[2]}; --accent: {th[3]}; --ink: {th[4]}; --ink2: {th[5]}; --ink3: {th[6]}; }}
.sign b {{ font-size: 8cqw; text-align: center; line-height: 1.05; }} .sign small {{ text-align: center; max-width: 92%; }}
.all {{ margin-top: 14px; }} .all-t {{ display: block; font: 500 10px var(--f-caps); letter-spacing: .26em; color: var(--ink3); margin-bottom: 8px; }}
.chips {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 7px; }} .chips span {{ font-size: 13px; padding: 6px 12px; border-radius: 999px; color: var(--ink2); background: rgba(255,255,255,.75); box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--accent) 30%, transparent); }}
.qrp {{ position: absolute; left: 8%; top: 18%; width: 34%; aspect-ratio: 1; padding: 4px; background: #fff; border-radius: 6px; box-shadow: 0 6px 12px -6px rgba(0,0,0,.3); z-index: 1; }} .qrp img, .qrp canvas, .qr img, .qr canvas {{ width: 100% !important; height: 100% !important; }}
.lot small {{ font: 500 2.6cqw var(--f-caps); letter-spacing: .3em; color: var(--ink2); }} .lot b {{ font: 400 9cqw/1 var(--f-script); background: var(--gold-text); -webkit-background-clip: text; background-clip: text; color: transparent; padding: 0 .1em .1em; }}
.lot .grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.2cqw; width: 88%; margin-top: 2cqw; }} .lot .grid span {{ aspect-ratio: 1.15; display: grid; place-items: center; font: 500 2.1cqw var(--f-serif); color: var(--ink); border: 1px solid color-mix(in srgb, var(--accent) 45%, transparent); border-radius: 4px; background: rgba(255,255,255,.4); }}
.badge {{ gap: 1.2cqw; }} .badge .bseal {{ width: 18%; }} .badge .evt {{ font: 500 1.4cqw var(--f-caps); letter-spacing: .16em; color: var(--accent); text-align: center; }} .badge b {{ font: 600 4.6cqw/1.05 var(--f-serif); color: var(--ink); text-align: center; }} .badge small {{ font: 500 1.5cqw var(--f-caps); letter-spacing: .14em; color: var(--ink2); }} .badge .qr {{ width: 30%; aspect-ratio: 1; margin-top: 1cqw; }}
.others {{ display: flex; gap: 18px; overflow-x: auto; padding: 8px 4px 20px; justify-content: safe center; scrollbar-width: none; }} .ow {{ flex: none; width: 128px; display: flex; flex-direction: column; align-items: center; gap: 8px; text-decoration: none; }}
.ow .ar {{ width: 100%; aspect-ratio: .74; border-radius: 50% 50% 12px 12px / 36% 36% 12px 12px; overflow: hidden; box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--gold) 50%, transparent), 0 16px 26px -16px rgba(40,25,20,.5); }} .ow img {{ width: 100%; height: 100%; object-fit: cover; transition: transform .8s; }} .ow:hover img {{ transform: scale(1.08); }} .ow b {{ font: 500 16px var(--f-serif); text-align: center; }}
'''
    css = CSS.replace('url(../../img/hero-xv.webp)', f'url(../../img/{d["hero"]}.webp)')
    name_es, name_en = col['es']['nombre'], col['en']['nombre']
    body = f'''<title>{html.escape(T(*d["eyebrow"]) and d["eyebrow"][0].capitalize())} · Ilusión Invites</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600&family=Allura&family=Great+Vibes&family=Cormorant+Garamond:ital,wght@0,500;0,600;1,400;1,500&family=Jost:wght@300;400;500&display=swap">
<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
<style>{css}
{extra_css}</style>
<div class="bg" aria-hidden="true"><i class="tint"></i></div>
<header class="top"><div class="wrap">
  <a class="back" href="../../coleccion/{slug}/"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>{T(html.escape(name_es), html.escape(name_en))}</a>
  <a class="brand" href="../../" aria-label="Ilusión Invites"><img src="../../img/sello-ilusion-oro-s.webp" alt="" width="140" height="139"><b><i class="I">I</i>lusión</b></a>
  <div class="right"><div class="lang" role="group" aria-label="Idioma"><button type="button" id="es" aria-pressed="true">ES</button><button type="button" id="en" aria-pressed="false">EN</button></div>{T('Crear la mía', 'Create mine', 'a', 'cta-top', f' href="../../crear/?c={slug}"')}</div>
</div></header>
<main class="wrap">
  <section class="intro">{T(*d['eyebrow'], 'span', 'eyebrow')}{T(*d['h1'], 'h1')}{T('más allá de la invitación', 'beyond the invitation', 'span', 'tag')}{T(*d['intro'], 'p')}<nav class="index" aria-label="En esta página">{index}</nav></section>
  <div class="rule"></div>
  {('<div class="rule"></div>').join(secs)}
  <div class="rule"></div>
  <section class="close">{T('TU EVENTO, COMPLETO', 'YOUR EVENT, COMPLETE', 'span', 'eyebrow')}{T('Elige tu paquete <em>o arma el tuyo</em>', 'Choose a package <em>or build your own</em>', 'h2', '', ' style="margin:0;font:500 clamp(34px,4.4vw,54px)/1.1 var(--f-serif)"')}
    {T('Cada pieza se puede sumar a cualquier paquete.', 'Every piece can be added to any package.', 'p', 'note')}
    <div class="row">{T('Crear mi invitación', 'Create my invitation', 'a', 'btn', f' href="../../crear/?c={slug}"')}{T('Ver paquetes y precios', 'See packages &amp; prices', 'a', 'btn line', ' href="../../#paquetes"')}</div></section>
  <div class="rule"></div>
  <section class="close" style="padding-top:clamp(40px,6vw,70px)">{T('SIGUE SOÑANDO', 'KEEP DREAMING', 'span', 'eyebrow')}{T('Otros <em>mundos</em>', 'Other <em>worlds</em>', 'h2', '', ' style="margin:0 0 10px;font:500 clamp(30px,3.6vw,44px)/1.1 var(--f-serif)"')}<nav class="others" aria-label="Otras colecciones">{others}</nav></section>
</main>
<script>
(function () {{
  document.querySelectorAll('[data-qr]').forEach(function (el) {{ try {{ if (window.QRCode) new QRCode(el, {{ text: el.getAttribute('data-qr'), width: 160, height: 160, colorDark: '{th[4]}', colorLight: '#ffffff', correctLevel: QRCode.CorrectLevel.M }}); }} catch (e) {{}} }});
  document.querySelectorAll('.on').forEach(function (on) {{ for (var i = 0; i < 10; i++) {{ var s = document.createElement('i'); s.className = 'sp'; s.style.left = (8 + Math.random() * 84) + '%'; s.style.top = (8 + Math.random() * 84) + '%'; s.style.animationDelay = (-Math.random() * 2.4) + 's'; on.appendChild(s); }} }});
  var nodes = [].slice.call(document.querySelectorAll('[data-en-html]'));
  nodes.forEach(function (el) {{ el.setAttribute('data-es-html', el.innerHTML); }});
  var TITLES = {{ es: {json.dumps(d['eyebrow'][0].capitalize() + ' · Ilusión Invites', ensure_ascii=False)}, en: {json.dumps(d['eyebrow'][1].title() + ' · Ilusión Invites', ensure_ascii=False)} }};
  function setLang(l) {{
    nodes.forEach(function (el) {{ el.innerHTML = l === 'en' ? el.getAttribute('data-en-html') : el.getAttribute('data-es-html'); }});
    document.documentElement.lang = l; document.title = TITLES[l];
    document.getElementById('es').setAttribute('aria-pressed', String(l === 'es')); document.getElementById('en').setAttribute('aria-pressed', String(l === 'en'));
    try {{ localStorage.setItem('ilu-lang', l); }} catch (e) {{}}
  }}
  document.getElementById('es').addEventListener('click', function () {{ setLang('es'); }});
  document.getElementById('en').addEventListener('click', function () {{ setLang('en'); }});
  var saved = null; try {{ saved = localStorage.getItem('ilu-lang'); }} catch (e) {{}}
  var q = new URLSearchParams(location.search).get('lang');
  setLang(q === 'en' || (q !== 'es' && saved === 'en') ? 'en' : 'es');
}})();
</script>'''
    title = d['eyebrow'][0].capitalize() + ' · Ilusión Invites'
    body = re.sub(r'^<title>.*?</title>', f'<title>{html.escape(title)}</title>', body)
    desc = html.escape(d['intro'][0])
    out = os.path.join(HERE, 'nuevo', 'experiencia', slug)
    os.makedirs(out, exist_ok=True)
    head = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="{desc}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{BASE}/nuevo/img/exp-{slug}-letrero.webp">
<meta property="og:url" content="{BASE}/nuevo/experiencia/{slug}/">
<meta name="theme-color" content="{th[0]}">
<link rel="icon" href="../../img/sello-ilusion-oro-s.webp">
<style>body{{margin:0}} img{{max-width:100%}} [hidden]{{display:none!important}}</style>
</head>
<body>
'''
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(head + body + '\n</body>\n</html>\n')


ready = [s for s in EXP if all(os.path.exists(os.path.join(HERE, 'nuevo', 'img', f'exp-{s}-{k}.webp')) for k in ('pantalla', 'letrero', 'pieza', 'selfie'))]
for slug in ready:
    page(slug, EXP[slug])
    print('built experiencia/' + slug)


# ---------------------------------------------------------------- home showcase (Experiencia Ilusión)
# One block per event, switched on the home page. Reuses the experience photos and designs above.
XV_SHOW = {
  'theme': ['#FCF3F4', '#FBEFF0', '#FDF7F6', '#B8798A', '#4A2633', '#7A5560', '#A88893'], 'hero': 'hero-xv', 'seal': 'sello-rubor', 'decos': ['rosa-rubor', 'rosa-marfil', 'mariposa-cristal-1'],
  'who': ('MIS XV AÑOS · VALENTINA', 'VALENTINA · MY QUINCEAÑERA'), 'para': ('Para: Familia López', 'For: The López Family'),
  'seats': ('Con mucho cariño reservamos<br><b>4 lugares</b> para ustedes', 'With love, we saved<br><b>4 seats</b> for you'),
  'btns': [('Confirmar 4 lugares', 'Confirm 4 seats'), ('Seremos menos', 'We will be fewer'), ('No podremos ir', "We can't make it")],
  'video': {'screen': (('MIS XV AÑOS', 'MY QUINCEAÑERA'), 'Valentina')},
  'marco': (('MIS XV AÑOS', 'MY QUINCEAÑERA'), 'Valentina', '14 · 03 · 2027'),
  'sign': (('BIENVENIDOS A LOS XV AÑOS DE', 'WELCOME TO THE QUINCEAÑERA OF'), 'Valentina', ('14 · MARZO · 2027', 'MARCH 14 · 2027')),
  'piece': {'kind': 'mesa', 'small': ('MESA', 'TABLE'), 'big': ('Tres', 'Three'), 'cap': ('NÚMERO DE MESA', 'TABLE NUMBER')},
  'imgs': {'pantalla': 'xv-salon-pantalla', 'letrero': 'xv-letrero', 'pieza': 'xv-mesa', 'selfie': 'xv-selfie'},
  'pos': {'pantalla': [31.6, 38.9, 37.3, 37.9], 'letrero': [34.5, 15, 35, 34], 'pieza': [38.5, 46, 27, 37]},
}
SHOW_ORDER = [('bodas', 'Boda', 'Wedding'), ('xv-anos', 'XV Años', 'Quinceañera'), ('cumpleanos', 'Cumpleaños', 'Birthday'), ('baby-shower', 'Baby Shower', 'Baby Shower'),
              ('navidad', 'Posada', 'Christmas'), ('ano-nuevo', 'Año Nuevo', "New Year's"), ('empresas', 'Empresa', 'Corporate')]


def show_block(slug, d, first):
    pos = d.get('pos') or POS.get(slug, {})
    imgs = d.get('imgs') or {k: f'exp-{slug}-{k}' for k in ('pantalla', 'letrero', 'pieza', 'selfie')}
    sc = pos.get('pantalla', [30, 30, 40, 40]); sg = pos.get('letrero', [34, 15, 32, 34]); pc = pos.get('pieza', [38, 40, 26, 36])
    th, dec, p, sgn = d['theme'], d['decos'], d['piece'], d['sign']
    rot = f'transform:rotate({pc[4]}deg);' if len(pc) > 4 else ''
    pstyle = f'--x:{pc[0]}%;--y:{pc[1]}%;--w:{pc[2]}%;--h:{pc[3]}%;{rot}'
    if p['kind'] == 'loteria':
        pin = f'<div class="lay lot" style="{pstyle}">{T(*p["small"], "small")}{T(*p["big"], "b")}<div class="grid">' + ''.join(T(a, b) for a, b in p['grid']) + '</div></div>'
    elif p['kind'] == 'gafete':
        pin = f'<div class="lay badge" style="{pstyle}"><img class="bseal" src="img/sello-ilusion-oro-s.webp" alt=""><span class="evt">GRUPO AURORA</span><b>{html.escape(p["big"][0])}</b>{T(*p["small"], "small")}</div>'
    else:
        big = p['big'][0]
        fs = ' style="font-size:%.1fcqw"' % min(10, 64 / max(len(big), 1))
        pin = f'<div class="lay mesa" style="{pstyle}"><img class="bfl" src="img/{dec[2]}.webp" alt="">{T(*p["small"], "small")}{T(*p["big"], "b", "", fs)}</div>'
    vs = d['video']['screen']; mk = d['marco']
    card = (f'<span class="qrp"></span>' if d.get('corp') else f'<img class="fl" src="img/{dec[0]}.webp" alt="">') + f'<img class="seal" src="img/{d["seal"]}.webp" alt="">'
    style = f'--bg:{th[0]};--bg2:{th[1]};--paper:{th[2]};--accent:{th[3]};--ink:{th[4]};--ink2:{th[5]};--ink3:{th[6]}'
    hidden = '' if first else ' hidden'
    return f'''<div class="xs-ev" data-ev="{slug}" style="{style}"{hidden}>
  <figure class="xs-t t-sign"><div class="photo"><img src="img/{imgs['letrero']}.webp" alt="" loading="lazy" width="1200" height="1600">
    <div class="lay sign" style="--x:{sg[0]}%;--y:{sg[1]}%;--w:{sg[2]}%;--h:{sg[3]}%">{T(*sgn[0], 'small')}<b style="font-size:{min(8, 118 / max(len(sgn[1]), 1)):.1f}cqw">{html.escape(sgn[1])}</b><i class="rl"></i>{T(*sgn[2])}</div></div>
    {T('Letrero de bienvenida', 'Welcome sign', 'figcaption')}</figure>
  <div class="xs-col">
    <figure class="xs-t"><div class="screen"><img src="img/{imgs['pantalla']}.webp" alt="" loading="lazy" width="1600" height="900">
      <div class="on" style="--sx:{sc[0]}%;--sy:{sc[1]}%;--sw:{sc[2]}%;--sh:{sc[3]}%"><div class="bgx" style="background-image:url(img/{d['hero']}.webp)"></div><div class="tt">{T(*vs[0], 'small')}<b class="gold">{html.escape(vs[1])}</b></div></div></div>
      {T('Video para la pantalla', 'Video for the big screen', 'figcaption')}</figure>
    <figure class="xs-t"><div class="photo sq"><img src="img/{imgs['pieza']}.webp" alt="" loading="lazy" width="1200" height="1200">{pin}</div>{T(*p['cap'], 'figcaption')}</figure>
  </div>
  <figure class="xs-t t-ph"><div class="phone"><div class="scr"><div class="env">
    {T(*d['who'], 'span', 'who')}{T(*d['para'], 'span', 'para gold')}<div class="card">{card}</div>{T(*d['seats'], 'p', 'seats')}
    <div class="btns">{T(*d['btns'][0], 'span', 'y')}{T(*d['btns'][1], 'span', 'n')}</div></div></div></div>
    {T('Invitación con link por invitado', 'Invitation with a link per guest', 'figcaption')}</figure>
  <figure class="xs-t t-ph"><div class="phone"><div class="scr"><div class="ig">
    <div class="ph" style="background-image:url(img/{imgs['selfie']}.webp)"></div>
    <div class="fr"><img class="f1" src="img/{dec[0]}.webp" alt=""><img class="f2" src="img/{dec[1]}.webp" alt=""></div>
    <div class="lbl">{T(*mk[0], 'small')}<b>{html.escape(mk[1])}</b><span>{html.escape(mk[2])}</span></div></div></div></div>
    {T('Fotos de invitados con tu marco', 'Guest photos with your frame', 'figcaption')}</figure>
</div>'''


def scoped_css():
    keep = ('.phone', '.scr', '.env', '.ig', '.screen', '.photo', '.lay', '.sign', '.mesa', '.gold')
    out = []
    clean = re.sub(r'/\*.*?\*/', '', CSS, flags=re.S)
    for m in re.finditer(r'([^{}@]+)\{([^{}]*)\}', clean):
        sel, body = m.group(1).strip(), m.group(2)
        parts = [s.strip() for s in sel.split(',')]
        if parts and all(any(s.startswith(k) for k in keep) for s in parts):
            out.append(', '.join('.xs ' + s for s in parts) + ' {' + body + '}')
    out += [m.group(0) for m in re.finditer(r'@keyframes (kb|up|tw) \{(?:[^{}]*\{[^{}]*\})*[^{}]*\}', CSS)]
    return '\n'.join(out).replace('@keyframes kb', '@keyframes xkb').replace('@keyframes up', '@keyframes xup').replace('@keyframes tw', '@keyframes xtw').replace('animation: kb ', 'animation: xkb ').replace('animation: up ', 'animation: xup ').replace('animation: tw ', 'animation: xtw ')


blocks = []
for i, (slug, es, en) in enumerate(SHOW_ORDER):
    d = XV_SHOW if slug == 'xv-anos' else EXP[slug]
    blocks.append(show_block(slug, d, i == 0))
tabs = ''.join(f'<button type="button" data-ev="{s}" aria-pressed="{str(i == 0).lower()}" data-en="{html.escape(en)}">{html.escape(es)}</button>' for i, (s, es, en) in enumerate(SHOW_ORDER))
open(os.path.join(HERE, '_expshow.html'), 'w', encoding='utf-8').write(f'<style>{scoped_css()}</style><div class="xs-tabs" role="group" aria-label="Tipo de evento">{tabs}</div><div class="xs-stage">' + ''.join(blocks) + '</div>')
print('home showcase: ' + str(len(blocks)) + ' events')
