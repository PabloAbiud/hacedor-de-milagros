"""Genera las páginas de testimonios de hacedordemilagros.com.

Uso (desde la raíz del sitio):
    python3 _build/testimonios.py

Lee cada archivo _testimonios/AAAA-MM-DD-nombre.json y crea:
  - /testimonios/<slug>/index.html  (una página por testimonio, tarea #9)
  - /testimonios/index.html         (índice por categorías, tarea #10)
  - las URL de /testimonios/ en sitemap.xml
  - las tarjetas de "Primeras historias" en el inicio (cuando ya hay testimonios)

Instrucciones completas: _build/2026-11-16-LEEME-testimonios.md
"""
import argparse, datetime, html, json, os, re, sys
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import pagina, REPO

SITIO = 'https://hacedordemilagros.com'
LISTA_TESTIMONIOS = 'https://www.youtube.com/@podcasthacedordemilagros/videos'

# Si no hay testimonios publicados, ¿se publica el índice en modo "en preparación" (sin indexar)?
PUBLICAR_INDICE_VACIO = False

CATEGORIAS = {
    'sanidad':    ('Sanidad', 'Diagnósticos sin salida, enfermedades y cuerpos restaurados.'),
    'provision':  ('Provisión', 'Lo que llegó justo a tiempo: trabajo, casa, sustento y puertas abiertas.'),
    'familia':    ('Familia y restauración', 'Matrimonios, hijos y relaciones que volvieron a empezar.'),
    'liberacion': ('Liberación', 'Adicciones, vicios y ataduras que se rompieron.'),
}

RVR = ('Texto bíblico tomado de la Santa Biblia, versión Reina-Valera 1960 © Sociedades Bíblicas en '
       'América Latina, 1960. Renovado © Sociedades Bíblicas Unidas, 1988. Utilizado con permiso.')

OBLIGATORIOS = ['slug', 'publicado', 'categoria', 'titulo', 'descripcion', 'pais', 'youtube_id',
                'duracion', 'resumen', 'verificacion', 'consentimiento']

e = lambda s: html.escape(str(s), quote=True)


# ---------------------------------------------------------------- datos

def leer(datos_dir, hoy):
    """Lee y valida los testimonios. Devuelve (publicables, avisos)."""
    lista, avisos, slugs = [], [], set()
    for f in sorted(Path(datos_dir).glob('*.json')):
        t = json.loads(f.read_text(encoding='utf-8'))
        nombre = f.name
        if t.get('borrador'):
            avisos.append(f'{nombre}: es borrador, no se publica.')
            continue
        faltan = [k for k in OBLIGATORIOS if t.get(k) in (None, '', [])]
        if faltan:
            sys.exit(f'ERROR {nombre}: faltan campos: {", ".join(faltan)}')
        if t['consentimiento'] is not True:
            sys.exit(f'ERROR {nombre}: sin consentimiento por escrito no se publica.')
        if t['categoria'] not in CATEGORIAS:
            sys.exit(f'ERROR {nombre}: categoría "{t["categoria"]}" no existe. Usa: {", ".join(CATEGORIAS)}')
        if not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', t['slug']):
            sys.exit(f'ERROR {nombre}: el slug solo lleva minúsculas sin acentos, números y guiones.')
        if t['slug'] in slugs:
            sys.exit(f'ERROR {nombre}: slug repetido: {t["slug"]}')
        if not re.fullmatch(r'[A-Za-z0-9_-]{11}', t['youtube_id']):
            sys.exit(f'ERROR {nombre}: youtube_id debe ser el código de 11 caracteres del video.')
        if not re.fullmatch(r'PT(\d+H)?(\d+M)?(\d+S)?', t['duracion']) or t['duracion'] == 'PT':
            sys.exit(f'ERROR {nombre}: duracion va como PT18M32S (18 min 32 s) o PT1H5M.')
        fecha = datetime.date.fromisoformat(t['publicado'])
        if fecha > hoy:
            avisos.append(f'{nombre}: programado para {fecha}, todavía no se publica.')
            continue
        if len(t['descripcion']) > 155:
            avisos.append(f'{nombre}: la descripción mide {len(t["descripcion"])} caracteres; Google corta ~155.')
        if len(titulo_seo(t)) > 60:
            avisos.append(f'{nombre}: el título para Google mide {len(titulo_seo(t))} caracteres; mejor ≤60 (campo titulo_seo).')
        slugs.add(t['slug'])
        t['_fecha'] = fecha
        lista.append(t)
    lista.sort(key=lambda t: t['_fecha'], reverse=True)
    return lista, avisos


def titulo_seo(t):
    return t.get('titulo_seo') or t['titulo']


def url(t):
    return f"{SITIO}/testimonios/{t['slug']}/"


def minutos(iso):
    h, m, s = (int(x or 0) for x in re.fullmatch(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', iso).groups())
    total = h * 60 + m + (1 if s >= 30 else 0)
    return f'{total} min' if total else '1 min'


def segundos(marca):
    partes = [int(p) for p in marca.split(':')]
    s = 0
    for p in partes:
        s = s * 60 + p
    return s


def quien(t):
    if t.get('anonimo'):
        return 'Testimonio anónimo'
    return t.get('persona') or 'Testimonio'


def miniatura(t, calidad='hqdefault'):
    return f"https://i.ytimg.com/vi/{t['youtube_id']}/{calidad}.jpg"


def fecha_larga(d):
    meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto',
             'septiembre', 'octubre', 'noviembre', 'diciembre']
    return f'{d.day} de {meses[d.month - 1]} de {d.year}'


def parrafos(lista):
    if isinstance(lista, str):
        lista = [lista]
    return '\n'.join(f'    <p>{e(p)}</p>' for p in lista)


# ---------------------------------------------------------------- estilos

CSS = '''
<style>
.tag{display:inline-block;font-family:'Outfit',sans-serif;font-size:12px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:var(--deep);background:var(--gold);padding:3px 11px;border-radius:999px;margin-bottom:12px;text-decoration:none!important}
.meta{color:var(--muted2);font-size:15px;margin:4px 0 0}
.meta .sep{margin:0 8px;opacity:.6}
.nota{color:var(--muted2);font-size:14px;margin:6px 0 0}
.video{position:relative;aspect-ratio:16/9;border-radius:16px;overflow:hidden;background:#000;margin:26px 0 12px;border:1px solid rgba(247,241,227,.12)}
.video img,.video iframe{position:absolute;inset:0;width:100%;height:100%;border:0;object-fit:cover}
.video button{position:absolute;inset:0;width:100%;height:100%;border:0;padding:0;background:transparent;cursor:pointer;display:grid;place-items:center}
.video button::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,21,48,0) 40%,rgba(10,21,48,.55))}
.play{position:relative;z-index:1;width:76px;height:76px;border-radius:50%;background:var(--gold);display:grid;place-items:center;box-shadow:0 6px 24px rgba(0,0,0,.4);transition:transform .15s}
.video button:hover .play,.video button:focus-visible .play{transform:scale(1.06)}
.play svg{width:30px;height:30px;margin-left:4px;fill:var(--deep)}
.video button:focus-visible{outline:3px solid var(--goldb);outline-offset:-3px}
.plataformas{display:flex;flex-wrap:wrap;gap:10px;margin:8px 0 6px}
.plataformas a{display:inline-flex;align-items:center;min-height:44px;padding:0 16px;border-radius:999px;border:1px solid rgba(247,241,227,.22);color:var(--cream);font-family:'Outfit',sans-serif;font-weight:600;font-size:14px}
.plataformas a:hover{border-color:var(--gold);text-decoration:none}
.momentos{list-style:none;padding:0;margin:12px 0}
.momentos li{margin:6px 0}
.momentos a{display:inline-flex;gap:12px;align-items:baseline;min-height:44px;align-items:center}
.momentos .t{font-family:'Outfit',sans-serif;font-weight:700;color:var(--goldb);min-width:52px;font-variant-numeric:tabular-nums}
.momentos .x{color:var(--cream)}
.verif{border-left:3px solid var(--gold);background:rgba(22,41,79,.45);border-radius:0 14px 14px 0;padding:16px 20px;margin:16px 0}
.verif p{margin:6px 0}
.compartir{display:flex;flex-wrap:wrap;gap:10px;margin:14px 0}
.compartir a,.compartir button{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 18px;border-radius:999px;border:1px solid rgba(247,241,227,.22);background:transparent;color:var(--cream);font:600 15px 'Outfit',sans-serif;cursor:pointer}
.compartir a:hover,.compartir button:hover{border-color:var(--gold);text-decoration:none}
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:18px;margin:18px 0}
@media(max-width:620px){.grid{grid-template-columns:1fr}}
.tcard{display:block;background:rgba(22,41,79,.45);border:1px solid rgba(247,241,227,.1);border-radius:16px;overflow:hidden;color:var(--cream);text-decoration:none!important;transition:border-color .15s}
.tcard:hover{border-color:var(--gold)}
.tcard .img{display:block;position:relative;aspect-ratio:16/9;background:#0b1836}
.tcard .img img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.tcard .dur{position:absolute;right:10px;bottom:10px;background:rgba(10,21,48,.85);color:var(--cream);font:600 12px 'Outfit',sans-serif;padding:3px 8px;border-radius:6px}
.tcard .tx{display:block;padding:14px 18px 18px}
.tcard .tag{margin-bottom:8px}
.tcard h3{margin:0 0 6px;font-size:18px;line-height:1.3}
.tcard p{margin:0;font-size:14px;color:var(--muted2)}
.chips{display:flex;flex-wrap:wrap;gap:10px;margin:22px 0 6px}
.chips a{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 16px;border-radius:999px;border:1px solid rgba(247,241,227,.22);color:var(--cream);font:600 14px 'Outfit',sans-serif}
.chips a:hover{border-color:var(--gold);text-decoration:none}
.chips .n{color:var(--muted2);font-weight:500}
.cat-desc{color:var(--muted);margin-top:-4px}
.pronto{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin:18px 0}
@media(max-width:620px){.pronto{grid-template-columns:1fr}}
.pronto div{background:rgba(22,41,79,.45);border:1px solid rgba(247,241,227,.1);border-top:4px solid var(--gold);border-radius:16px;padding:18px 20px}
.pronto h3{margin:0 0 4px}
.pronto p{margin:0;font-size:15px;color:var(--muted)}
</style>'''

ICON_PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>'


def tarjeta(t, nivel='h3'):
    cat = CATEGORIAS[t['categoria']][0]
    return (f'      <a class="tcard" href="/testimonios/{t["slug"]}/">\n'
            f'        <div class="img"><img src="{miniatura(t)}" alt="" width="480" height="270" loading="lazy" decoding="async">'
            f'<span class="dur">{minutos(t["duracion"])}</span></div>\n'
            f'        <div class="tx"><span class="tag">{e(cat)}</span><{nivel}>{e(t["titulo"])}</{nivel}>'
            f'<p>{e(quien(t))} · {e(t["pais"])}</p></div>\n'
            f'      </a>')


# ---------------------------------------------------------------- página de testimonio (#9)

JS_TESTIMONIO = '''<script>
(function(){
  var caja=document.getElementById('video');if(!caja)return;
  var id=caja.getAttribute('data-id');
  function reproducir(seg){
    var f=document.createElement('iframe');
    f.src='https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&rel=0'+(seg?'&start='+seg:'');
    f.title=caja.getAttribute('data-titulo');
    f.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
    f.setAttribute('allowfullscreen','');
    caja.innerHTML='';caja.appendChild(f);
  }
  var b=caja.querySelector('button');if(b)b.addEventListener('click',function(){reproducir(0)});
  document.querySelectorAll('[data-seg]').forEach(function(a){
    a.addEventListener('click',function(ev){ev.preventDefault();reproducir(+a.getAttribute('data-seg'));caja.scrollIntoView({behavior:'smooth',block:'center'});});
  });
  var c=document.getElementById('copiar');
  if(c&&navigator.clipboard)c.addEventListener('click',function(){
    navigator.clipboard.writeText(c.getAttribute('data-url')).then(function(){c.textContent='Enlace copiado';setTimeout(function(){c.textContent='Copiar enlace'},2500)});
  });else if(c)c.hidden=true;
})();
</script>'''


def pagina_testimonio(t, todos):
    u = url(t)
    cat_nombre, _ = CATEGORIAS[t['categoria']]
    yid = t['youtube_id']
    watch = f'https://www.youtube.com/watch?v={yid}'
    fecha_iso = t['_fecha'].isoformat()

    # Plataformas
    plat = [f'<a href="{watch}" target="_blank" rel="noopener">Ver en YouTube</a>']
    if t.get('spotify'):
        plat.append(f'<a href="{e(t["spotify"])}" target="_blank" rel="noopener">Escuchar en Spotify</a>')
    if t.get('apple'):
        plat.append(f'<a href="{e(t["apple"])}" target="_blank" rel="noopener">Escuchar en Apple Podcasts</a>')

    meta = [e(quien(t)), e(t['pais']), minutos(t['duracion']), fecha_larga(t['_fecha'])]
    nota = ''
    if t.get('nombre_cambiado') and not t.get('anonimo'):
        nota = '\n    <p class="nota">A petición suya, cambiamos su nombre.</p>'

    partes = [f'''    <nav class="crumbs" aria-label="Ruta"><a href="/">Inicio</a> › <a href="/testimonios/">Testimonios</a> › <a href="/testimonios/#{t["categoria"]}">{e(cat_nombre)}</a></nav>
    <a class="tag" href="/testimonios/#{t["categoria"]}">{e(cat_nombre)}</a>
    <h1>{e(t["titulo"])}</h1>
    <p class="meta">{'<span class="sep">·</span>'.join(meta)}</p>{nota}

    <div class="video" id="video" data-id="{yid}" data-titulo="{e(t["titulo"])}">
      <img src="{miniatura(t)}" alt="" width="480" height="270" decoding="async" fetchpriority="high">
      <button type="button" aria-label="Reproducir el testimonio en video"><span class="play">{ICON_PLAY}</span></button>
      <noscript><a href="{watch}">Ver el testimonio en YouTube</a></noscript>
    </div>
    <div class="plataformas">{"".join(plat)}</div>

    <h2>En resumen</h2>
{parrafos(t["resumen"])}''']

    v = t.get('versiculo')
    if v:
        partes.append(f'''
    <div class="verse">
      <p>«{e(v["texto"])}»</p>
      <cite>{e(v["cita"])}</cite>
    </div>''')

    if t.get('momentos'):
        items = '\n'.join(
            f'      <li><a href="{watch}&amp;t={segundos(m["t"])}s" data-seg="{segundos(m["t"])}"><span class="t">{e(m["t"])}</span><span class="x">{e(m["texto"])}</span></a></li>'
            for m in t['momentos'])
        partes.append(f'''
    <h2>Momentos del testimonio</h2>
    <ol class="momentos">
{items}
    </ol>''')

    partes.append(f'''
    <h2>Cómo verificamos esta historia</h2>
    <div class="verif">
{parrafos(t["verificacion"])}
    </div>
    <p class="small">Cada testimonio pasa por cuatro pasos antes de publicarse: lo escuchamos, conversamos con la persona, buscamos respaldo y lo contamos solo con su permiso. <a href="/iglesias/">Más sobre cómo cuidamos cada testimonio</a>.</p>''')

    if t.get('transcripcion'):
        partes.append(f'''
    <h2>Transcripción</h2>
    <details>
      <summary>Leer la transcripción completa</summary>
{parrafos(t["transcripcion"])}
    </details>''')

    texto_wa = quote(f'{t["titulo"]} — un testimonio real de lo que Dios sigue haciendo hoy: {u}')
    partes.append(f'''
    <h2>Comparte esta historia</h2>
    <p>Puede ser justo lo que alguien necesita escuchar hoy.</p>
    <div class="compartir">
      <a href="https://wa.me/?text={texto_wa}" target="_blank" rel="noopener">Compartir por WhatsApp</a>
      <button type="button" id="copiar" data-url="{u}">Copiar enlace</button>
    </div>

    <h2>¿Dios también hizo algo en tu vida?</h2>
    <p>Tu historia puede darle esperanza a alguien más. Cuéntanosla: la escuchamos con respeto y en oración. Y si hoy necesitas que oremos por ti, acompáñanos en la Madrugada de Oración.</p>
    <div class="btns">
      <a class="btn btn-gold" href="/#testimonio">Comparte tu testimonio</a>
      <a class="btn btn-ghost" href="/madrugada-de-oracion/">Madrugada de Oración</a>
    </div>''')

    # Más testimonios: primero de la misma categoría, luego los más recientes
    otros = [x for x in todos if x is not t]
    otros.sort(key=lambda x: (x['categoria'] != t['categoria'], -x['_fecha'].toordinal()))
    otros = otros[:2]
    if otros:
        partes.append('\n    <h2>Más testimonios</h2>\n    <div class="grid">\n'
                      + '\n'.join(tarjeta(x) for x in otros)
                      + '\n    </div>\n    <p><a href="/testimonios/">Ver todos los testimonios</a></p>')

    if v:
        partes.append(f'\n    <p class="small">{RVR}</p>')

    partes.append('\n' + JS_TESTIMONIO)

    # Datos estructurados
    ld = {
        '@context': 'https://schema.org',
        '@graph': [
            {
                '@type': 'WebPage', '@id': u + '#pagina', 'url': u, 'name': t['titulo'],
                'description': t['descripcion'], 'inLanguage': 'es', 'datePublished': fecha_iso,
                'isPartOf': {'@id': SITIO + '/#website'},
                'breadcrumb': {'@id': u + '#ruta'},
                'primaryImageOfPage': miniatura(t),
                'mainEntity': {'@id': u + '#video'},
            },
            {
                '@type': 'VideoObject', '@id': u + '#video', 'name': t['titulo'],
                'description': t['descripcion'],
                'thumbnailUrl': [miniatura(t, 'maxresdefault'), miniatura(t)],
                'uploadDate': f'{fecha_iso}T08:00:00-06:00',
                'duration': t['duracion'],
                'embedUrl': f'https://www.youtube.com/embed/{yid}',
                'inLanguage': 'es',
                'publisher': {'@id': SITIO + '/#org'},
            },
            {
                '@type': 'PodcastEpisode', '@id': u + '#episodio', 'url': u, 'name': t['titulo'],
                'description': t['descripcion'], 'datePublished': fecha_iso, 'inLanguage': 'es',
                'partOfSeries': {'@id': SITIO + '/#podcast'},
                'associatedMedia': {'@id': u + '#video'},
            },
            {
                '@type': 'BreadcrumbList', '@id': u + '#ruta',
                'itemListElement': [
                    {'@type': 'ListItem', 'position': 1, 'name': 'Inicio', 'item': SITIO + '/'},
                    {'@type': 'ListItem', 'position': 2, 'name': 'Testimonios', 'item': SITIO + '/testimonios/'},
                    {'@type': 'ListItem', 'position': 3, 'name': t['titulo'], 'item': u},
                ],
            },
        ],
    }
    if t.get('momentos'):
        ld['@graph'][1]['hasPart'] = [
            {'@type': 'Clip', 'name': m['texto'], 'startOffset': segundos(m['t']),
             'url': f'{watch}&t={segundos(m["t"])}s'} for m in t['momentos']]
        # endOffset: inicio del siguiente momento
        for i, clip in enumerate(ld['@graph'][1]['hasPart']):
            if i + 1 < len(t['momentos']):
                clip['endOffset'] = segundos(t['momentos'][i + 1]['t'])
            else:
                clip['endOffset'] = segundos_totales(t['duracion'])
    if t.get('transcripcion'):
        tr = t['transcripcion']
        ld['@graph'][1]['transcript'] = '\n\n'.join(tr) if isinstance(tr, list) else tr

    doc = pagina(ruta=f'/testimonios/{t["slug"]}/',
                 titulo=f'{e(titulo_seo(t))} | Hacedor de Milagros',
                 descripcion=e(t['descripcion']),
                 og_titulo=e(t['titulo']),
                 jsonld=json.dumps(ld, ensure_ascii=False, indent=2),
                 cuerpo=''.join(partes))
    og = e(t.get('og_imagen') or miniatura(t))
    doc = doc.replace('content="https://hacedordemilagros.com/og.jpg"', f'content="{og}"', 1)
    doc = doc.replace('<meta property="og:type" content="article">',
                      f'<meta property="og:type" content="video.other">\n<meta property="og:video" content="https://www.youtube.com/embed/{yid}">', 1)
    doc = doc.replace('</head>', CSS + '\n</head>', 1)
    return doc


def segundos_totales(iso):
    h, m, s = (int(x or 0) for x in re.fullmatch(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', iso).groups())
    return h * 3600 + m * 60 + s


# ---------------------------------------------------------------- índice (#10)

def pagina_indice(todos):
    u = SITIO + '/testimonios/'
    por_cat = {k: [t for t in todos if t['categoria'] == k] for k in CATEGORIAS}
    con = [k for k in CATEGORIAS if por_cat[k]]
    desc = ('Testimonios reales de milagros en español: sanidad, provisión, familias restauradas y liberación. '
            'Historias verificadas de lo que Dios sigue haciendo hoy.')[:155]

    cuerpo = ['''    <nav class="crumbs" aria-label="Ruta"><a href="/">Inicio</a> › Testimonios</nav>
    <div class="kicker">Historias reales de fe</div>
    <h1>Testimonios reales de milagros</h1>
    <p class="intro">Personas comunes de todo el mundo hispano cuentan lo que Dios hizo en su vida. Cada historia la escuchamos, la verificamos y la publicamos solo con permiso de quien la vivió.</p>''']

    if todos:
        chips = '\n'.join(
            f'      <a href="#{k}">{e(CATEGORIAS[k][0])} <span class="n">{len(por_cat[k])}</span></a>' for k in con)
        cuerpo.append(f'    <nav class="chips" aria-label="Categorías">\n{chips}\n    </nav>')
        for k in con:
            nombre, d = CATEGORIAS[k]
            cuerpo.append(f'''
    <h2 id="{k}">{e(nombre)}</h2>
    <p class="cat-desc">{e(d)}</p>
    <div class="grid">
{chr(10).join(tarjeta(t) for t in por_cat[k])}
    </div>''')
    else:
        pronto = '\n'.join(f'      <div><h3>{e(n)}</h3><p>{e(d)}</p></div>' for n, d in CATEGORIAS.values())
        cuerpo.append(f'''
    <div class="card">
      <h3>Las primeras historias vienen en camino</h3>
      <p>Estamos preparando los primeros testimonios. Estas son las historias que vas a encontrar aquí:</p>
    </div>
    <div class="pronto">
{pronto}
    </div>
    <div class="btns">
      <a class="btn btn-gold" href="/#avisame">Avísame del estreno</a>
      <a class="btn btn-ghost" href="{LISTA_TESTIMONIOS}" target="_blank" rel="noopener">Ver el canal de YouTube</a>
    </div>''')

    cuerpo.append('''
    <h2>¿Tienes un testimonio?</h2>
    <p>Si Dios hizo un milagro en tu vida, tu historia puede darle esperanza a alguien más. Puedes escribirla, grabarla con tu voz o subir un archivo.</p>
    <div class="btns">
      <a class="btn btn-gold" href="/#testimonio">Comparte tu testimonio</a>
      <a class="btn btn-ghost" href="/como-contar-tu-testimonio/">Cómo contar tu testimonio</a>
    </div>''')

    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'CollectionPage', '@id': u + '#pagina', 'url': u, 'name': 'Testimonios reales de milagros',
         'description': desc, 'inLanguage': 'es', 'isPartOf': {'@id': SITIO + '/#website'},
         'about': {'@id': SITIO + '/#podcast'}},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Inicio', 'item': SITIO + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Testimonios', 'item': u}]},
    ]}
    if todos:
        ld['@graph'][0]['mainEntity'] = {
            '@type': 'ItemList', 'numberOfItems': len(todos),
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': url(t), 'name': t['titulo']}
                                for i, t in enumerate(todos)]}

    doc = pagina(ruta='/testimonios/', titulo='Testimonios reales de milagros | Hacedor de Milagros',
                 descripcion=desc, og_titulo='Testimonios reales de milagros — Hacedor de Milagros',
                 jsonld=json.dumps(ld, ensure_ascii=False, indent=2), cuerpo='\n'.join(cuerpo))
    doc = doc.replace('<meta property="og:type" content="article">', '<meta property="og:type" content="website">', 1)
    if not todos:
        doc = doc.replace('<meta name="robots" content="index, follow">', '<meta name="robots" content="noindex, follow">', 1)
    doc = doc.replace('</head>', CSS + '\n</head>', 1)
    return doc


# ---------------------------------------------------------------- sitemap e inicio

def actualizar_sitemap(salida, todos, indice_publicado, hoy):
    p = Path(salida) / 'sitemap.xml'
    s = p.read_text(encoding='utf-8')
    s = re.sub(r'\s*<url>\s*<loc>https://hacedordemilagros\.com/testimonios/.*?</url>', '', s, flags=re.S)
    nuevos = []
    if indice_publicado and todos:
        nuevos.append(('/testimonios/', todos[0]['_fecha'].isoformat(), 'weekly', '0.9'))
    for t in todos:
        nuevos.append((f'/testimonios/{t["slug"]}/', t.get('actualizado', t['publicado']), 'monthly', '0.8'))
    bloque = ''.join(f'\n  <url>\n    <loc>{SITIO}{r}</loc>\n    <lastmod>{lm}</lastmod>\n'
                     f'    <changefreq>{cf}</changefreq>\n    <priority>{pr}</priority>\n  </url>'
                     for r, lm, cf, pr in nuevos)
    s = s.replace('\n</urlset>', bloque + '\n</urlset>')
    p.write_text(s, encoding='utf-8')


def actualizar_inicio(salida, todos):
    """Con testimonios publicados, cambia las tarjetas "En preparación" del inicio por los 3 más recientes."""
    p = Path(salida) / 'index.html'
    s = p.read_text(encoding='utf-8')
    ini, fin = '<!-- testimonios:inicio -->', '<!-- testimonios:fin -->'
    if ini not in s:
        return False
    if not todos:
        return False  # se queda el contenido "Las primeras historias vienen en camino"
    tarjetas = []
    for t in todos[:3]:
        tarjetas.append(
            f'      <a class="scard" href="/testimonios/{t["slug"]}/"><span class="tag">{e(CATEGORIAS[t["categoria"]][0])}</span>'
            f'<h3>{e(t["titulo"])}</h3><p>{e(quien(t))} · {e(t["pais"])} · {minutos(t["duracion"])}</p>'
            f'<div class="soon">Ver testimonio →</div></a>')
    nuevo = (f'''{ini}
    <div class="kicker">Testimonios</div>
    <h2 class="title">Las historias más recientes</h2>
    <p class="lead">Testimonios reales de todo el mundo hispano, verificados y contados con permiso de quien los vivió.</p>
    <div class="cards">
{chr(10).join(tarjetas)}
    </div>
    <p style="margin-top:22px"><a class="btn btn-ghost" href="/testimonios/">Ver todos los testimonios</a></p>
    {fin}''')
    s = re.sub(re.escape(ini) + r'.*?' + re.escape(fin), lambda m: nuevo, s, flags=re.S)
    p.write_text(s, encoding='utf-8')
    return True


# ---------------------------------------------------------------- principal

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--datos', default=str(REPO / '_testimonios'))
    ap.add_argument('--salida', default=str(REPO))
    ap.add_argument('--hoy', default=None, help='AAAA-MM-DD (para pruebas)')
    a = ap.parse_args()
    hoy = datetime.date.fromisoformat(a.hoy) if a.hoy else datetime.date.today()

    todos, avisos = leer(a.datos, hoy)
    raiz = Path(a.salida) / 'testimonios'

    # Borra páginas de testimonios que ya no están en los datos (p. ej., si alguien retira su permiso)
    vigentes = {t['slug'] for t in todos}
    if raiz.exists():
        for d in raiz.iterdir():
            if d.is_dir() and d.name not in vigentes and (d / 'index.html').exists():
                (d / 'index.html').unlink()
                d.rmdir()
                avisos.append(f'Se quitó /testimonios/{d.name}/ porque ya no está en los datos.')

    for t in todos:
        destino = raiz / t['slug']
        destino.mkdir(parents=True, exist_ok=True)
        (destino / 'index.html').write_text(pagina_testimonio(t, todos), encoding='utf-8')

    publicar_indice = bool(todos) or PUBLICAR_INDICE_VACIO
    if publicar_indice:
        raiz.mkdir(parents=True, exist_ok=True)
        (raiz / 'index.html').write_text(pagina_indice(todos), encoding='utf-8')
    elif (raiz / 'index.html').exists():
        avisos.append('No hay testimonios publicados y PUBLICAR_INDICE_VACIO es False: '
                      'el índice existente no se tocó.')

    actualizar_sitemap(a.salida, todos, publicar_indice, hoy)
    inicio = actualizar_inicio(a.salida, todos)

    print(f'Testimonios publicados: {len(todos)}')
    for t in todos:
        print(f'  /testimonios/{t["slug"]}/  ({CATEGORIAS[t["categoria"]][0]}, {t["publicado"]})')
    print('Índice /testimonios/:', 'generado' if publicar_indice else 'no se generó (no hay testimonios)')
    print('Inicio:', 'tarjetas actualizadas' if inicio else 'sin cambios')
    for x in avisos:
        print('Aviso:', x)


if __name__ == '__main__':
    main()
