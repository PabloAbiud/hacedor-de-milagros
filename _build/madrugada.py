import json, sys, os
from urllib.parse import quote
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import pagina, REPO

RUTA = '/madrugada-de-oracion/'
URL = 'https://hacedordemilagros.com' + RUTA
LIVE = 'https://www.youtube.com/@podcasthacedordemilagros/live'
CANAL = 'https://www.youtube.com/@podcasthacedordemilagros'
LISTA = 'https://www.youtube.com/playlist?list=PLR_LrxiZi8H0'
DESC = 'Oración cristiana en vivo por YouTube: martes y jueves de 4:30 a 5:15 a.m., hora del centro de México. Ora con nosotros y envía tu petición.'
MAIL = 'mailto:hola@hacedordemilagros.com?subject=Petici%C3%B3n%20de%20oraci%C3%B3n'

# Recordatorio en Google Calendar (serie semanal mar/jue, 4:30-5:15 CDMX = 10:30-11:15 UTC)
GCAL = ('https://calendar.google.com/calendar/render?action=TEMPLATE'
        '&text=' + quote('Madrugada de Oración en vivo') +
        '&dates=20261117T103000Z/20261117T111500Z'
        '&recur=' + quote('RRULE:FREQ=WEEKLY;BYDAY=TU,TH') +
        '&details=' + quote('Oración en vivo por YouTube: ' + LIVE + '\nMás información: ' + URL) +
        '&location=' + quote(LIVE))

jsonld = json.dumps({
    '@context': 'https://schema.org',
    '@graph': [
        {
            '@type': 'Event',
            '@id': URL + '#evento',
            'name': 'Madrugada de Oración en vivo',
            'description': 'Tiempo de oración cristiana en vivo por YouTube, martes y jueves de 4:30 a 5:15 a.m. (hora del centro de México).',
            'url': URL,
            'image': URL + 'og.jpg',
            'inLanguage': 'es',
            'startDate': '2026-11-17T04:30:00-06:00',
            'endDate': '2026-11-17T05:15:00-06:00',
            'eventSchedule': {
                '@type': 'Schedule',
                'repeatFrequency': 'P1W',
                'byDay': ['https://schema.org/Tuesday', 'https://schema.org/Thursday'],
                'startDate': '2026-11-17',
                'startTime': '04:30:00',
                'endTime': '05:15:00',
                'scheduleTimezone': 'America/Mexico_City',
            },
            'eventAttendanceMode': 'https://schema.org/OnlineEventAttendanceMode',
            'eventStatus': 'https://schema.org/EventScheduled',
            'location': {'@type': 'VirtualLocation', 'url': LIVE},
            'isAccessibleForFree': True,
            'organizer': {'@id': 'https://hacedordemilagros.com/#org'},
            'offers': {
                '@type': 'Offer', 'price': '0', 'priceCurrency': 'MXN',
                'availability': 'https://schema.org/InStock', 'url': URL,
            },
        },
        {
            '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Inicio', 'item': 'https://hacedordemilagros.com/'},
                {'@type': 'ListItem', 'position': 2, 'name': 'Madrugada de Oración', 'item': URL},
            ],
        },
    ],
}, ensure_ascii=False, indent=2)

CSS = '''
<style>
.horario{background:rgba(22,41,79,.45);border:1px solid rgba(244,183,64,.35);border-radius:18px;padding:22px 24px;margin:26px 0}
.horario .dias{font-family:'Outfit',sans-serif;font-weight:700;font-size:24px;color:var(--cream);line-height:1.25}
.horario .hora{font-family:'Outfit',sans-serif;font-weight:700;font-size:30px;color:var(--goldb);line-height:1.2;margin:4px 0 2px}
.horario .zona{font-size:15px;color:var(--muted2)}
.prox{margin-top:16px;padding-top:16px;border-top:1px solid rgba(247,241,227,.1);font-size:16px}
.prox strong{color:var(--cream)}
.prox .tu{display:block;margin-top:4px;color:var(--muted2);font-size:15px}
.envivo{display:inline-flex;align-items:center;gap:8px;font-family:'Outfit',sans-serif;font-weight:700;font-size:13px;letter-spacing:1px;text-transform:uppercase;color:var(--deep);background:var(--gold);padding:4px 12px;border-radius:999px;margin-bottom:8px}
.envivo::before{content:"";width:8px;height:8px;border-radius:50%;background:#c4122f}
</style>'''

cuerpo = f'''    <nav class="crumbs" aria-label="Ruta"><a href="/">Inicio</a> › Madrugada de Oración</nav>
    <div class="kicker">Oración en vivo</div>
    <h1>Madrugada de Oración en vivo</h1>
    <p class="intro">Dos madrugadas por semana nos levantamos temprano para orar juntos, en vivo por YouTube. Oramos lo que Dios nos habla en el devocional del día y presentamos delante de Él las peticiones que nos comparten. Estás invitado, desde cualquier país.</p>

    <div class="horario" aria-label="Horario">
      <div class="dias">Martes y jueves</div>
      <div class="hora">4:30 a 5:15 a.m.</div>
      <div class="zona">Hora del centro de México (Ciudad de México)</div>
      <div class="prox" id="proxima" aria-live="polite"><strong>Próxima oración:</strong> el siguiente martes o jueves a las 4:30 a.m.</div>
    </div>

    <div class="btns">
      <a class="btn btn-gold" id="btn-vivo" href="{LIVE}" target="_blank" rel="noopener">Ir a la oración en YouTube</a>
      <a class="btn btn-ghost" href="{GCAL}" target="_blank" rel="noopener">Agregar a Google Calendar</a>
      <a class="btn btn-ghost" href="/madrugada-de-oracion/madrugada-de-oracion.ics" download>Agregar a otro calendario</a>
    </div>
    <p class="small">El recordatorio se repite cada martes y jueves y te avisa 10 minutos antes.</p>

    <div class="verse">
      <p>«Levantándose muy de mañana, siendo aún muy oscuro, salió y se fue a un lugar desierto, y allí oraba.»</p>
      <cite>Marcos 1:35</cite>
    </div>

    <h2>Cómo unirte</h2>
    <ol class="steps">
      <li><strong>Entra al canal a la hora.</strong> Abre el <a href="{CANAL}" target="_blank" rel="noopener">canal Hacedor de Milagros en YouTube</a>. Cuando estamos en vivo, la transmisión aparece primero.</li>
      <li><strong>Activa el aviso.</strong> En la transmisión programada toca «Notificarme» y YouTube te avisará cuando empecemos. También puedes usar los botones de calendario de arriba.</li>
      <li><strong>Ora con nosotros.</strong> Escucha, ora en tu casa y, si quieres, escribe en el chat de la transmisión por qué estás orando.</li>
    </ol>

    <h2>¿Tienes una petición de oración?</h2>
    <p>Escríbenos a <a class="mail" href="{MAIL}">hola@hacedordemilagros.com</a> con el asunto «Petición de oración» y oraremos por ella. Puedes firmar solo con tu nombre de pila; no necesitas darnos más datos.</p>
    <div class="btns">
      <a class="btn btn-gold" href="{MAIL}">Enviar mi petición</a>
    </div>

    <div class="verse">
      <p>«Porque donde están dos o tres congregados en mi nombre, allí estoy yo en medio de ellos.»</p>
      <cite>Mateo 18:20</cite>
    </div>

    <h2>Preguntas frecuentes</h2>
    <details>
      <summary>¿Necesito una cuenta de YouTube?</summary>
      <p>Para ver y escuchar, no. Para escribir en el chat sí necesitas iniciar sesión en YouTube.</p>
    </details>
    <details>
      <summary>¿Y si no puedo a esa hora?</summary>
      <p>Cada oración queda guardada en la lista <a href="{LISTA}" target="_blank" rel="noopener">Madrugada de Oración</a> del canal, para que ores cuando puedas.</p>
    </details>
    <details>
      <summary>Vivo fuera de México, ¿a qué hora es para mí?</summary>
      <p>Arriba, en el horario, te mostramos la próxima oración en la hora de tu país. Si no aparece, toma como base la hora del centro de México.</p>
    </details>
    <details>
      <summary>¿Se ve a la persona que ora?</summary>
      <p>Casi siempre es solo voz, con la imagen de la Madrugada de Oración en pantalla. Algunos días puede ser a cámara.</p>
    </details>
    <details>
      <summary>¿Tiene algún costo?</summary>
      <p>No. Es gratuito y abierto a todos.</p>
    </details>

    <h2>¿Dios ya respondió tu oración?</h2>
    <p>Si viviste un milagro, tu historia puede darle esperanza a alguien más. Cuéntanosla: la escuchamos con respeto y en oración.</p>
    <div class="btns">
      <a class="btn btn-gold" href="/#testimonio">Comparte tu testimonio</a>
      <a class="btn btn-ghost" href="/como-contar-tu-testimonio/">Cómo contar tu testimonio</a>
    </div>
    <p class="small">Texto bíblico tomado de la Santa Biblia, versión Reina-Valera 1960 © Sociedades Bíblicas en América Latina, 1960. Renovado © Sociedades Bíblicas Unidas, 1988. Utilizado con permiso.</p>

<script>
(function(){{
  var el=document.getElementById('proxima'),btn=document.getElementById('btn-vivo');
  if(!el||!window.Intl)return;
  var H=36e5,D=864e5,ahora=Date.now();
  // Ciudad de México: UTC-6 todo el año. 4:30 a.m. = 10:30 UTC; 5:15 a.m. = 11:15 UTC.
  for(var i=0;i<8;i++){{
    var d=new Date(ahora-6*H+i*D),dow=d.getUTCDay();
    if(dow!==2&&dow!==4)continue;
    var ini=Date.UTC(d.getUTCFullYear(),d.getUTCMonth(),d.getUTCDate(),10,30),fin=ini+45*6e4;
    if(fin<=ahora)continue;
    if(ahora>=ini){{
      el.innerHTML='<span class="envivo">En vivo ahora</span><br><strong>Estamos orando en este momento.</strong> Termina a las 5:15 a.m. (hora del centro de México).';
      if(btn)btn.textContent='Entrar a la oración en vivo';
      return;
    }}
    var f=function(tz,zona){{var o={{weekday:'long',day:'numeric',month:'long',hour:'numeric',minute:'2-digit'}};if(tz)o.timeZone=tz;if(zona)o.timeZoneName='short';return new Intl.DateTimeFormat('es-MX',o).format(new Date(ini));}};
    var mx=f('America/Mexico_City'),local=f(null),html='<strong>Próxima oración:</strong> '+mx+' (hora del centro de México)';
    if(local!==mx)html+='<span class="tu">En tu hora: '+f(null,true)+'</span>';
    el.innerHTML=html;
    return;
  }}
}})();
</script>'''

html = pagina(ruta=RUTA,
              titulo='Madrugada de Oración en vivo | Hacedor de Milagros',
              descripcion=DESC,
              og_titulo='Madrugada de Oración en vivo — Hacedor de Milagros',
              jsonld=jsonld, cuerpo=cuerpo)
html = html.replace('content="https://hacedordemilagros.com/og.jpg"', f'content="{URL}og.jpg"', 1)
html = html.replace('<meta name="twitter:card"', '<meta property="og:image:width" content="1280">\n<meta property="og:image:height" content="720">\n<meta name="twitter:card"', 1)
html = html.replace('</head>', CSS + '\n</head>', 1)

def plegar(linea):
    # RFC 5545: líneas de máx. 75 octetos; las siguientes empiezan con un espacio
    b = linea.encode('utf-8'); partes = []
    while len(b) > 75:
        corte = 75 if not partes else 74
        while (b[corte] & 0xC0) == 0x80: corte -= 1
        partes.append(b[:corte].decode('utf-8')); b = b[corte:]
    partes.append(b.decode('utf-8'))
    return '\r\n '.join(partes)

ICS = '\r\n'.join(plegar(l) for l in [
    'BEGIN:VCALENDAR',
    'VERSION:2.0',
    'PRODID:-//Hacedor de Milagros//Madrugada de Oracion//ES',
    'CALSCALE:GREGORIAN',
    'METHOD:PUBLISH',
    'BEGIN:VEVENT',
    'UID:madrugada-de-oracion@hacedordemilagros.com',
    'DTSTAMP:20261115T000000Z',
    'DTSTART:20261117T103000Z',
    'DTEND:20261117T111500Z',
    'RRULE:FREQ=WEEKLY;BYDAY=TU,TH',
    'SUMMARY:Madrugada de Oración en vivo',
    'DESCRIPTION:Oración en vivo por YouTube: ' + LIVE + '\\nMás información: ' + URL,
    'LOCATION:' + LIVE,
    'URL:' + URL,
    'BEGIN:VALARM',
    'ACTION:DISPLAY',
    'DESCRIPTION:Madrugada de Oración en 10 minutos',
    'TRIGGER:-PT10M',
    'END:VALARM',
    'END:VEVENT',
    'END:VCALENDAR']) + '\r\n'

out = str(REPO) + '/madrugada-de-oracion'
os.makedirs(out, exist_ok=True)
open(out + '/index.html', 'w', encoding='utf-8').write(html)
open(out + '/madrugada-de-oracion.ics', 'w', encoding='utf-8', newline='').write(ICS)
print('madrugada ok, desc', len(DESC))
