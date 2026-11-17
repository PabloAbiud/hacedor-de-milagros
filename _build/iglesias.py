import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import pagina, REPO

RUTA = '/iglesias/'
URL = 'https://hacedordemilagros.com' + RUTA
DESC = 'Testimonios reales de lo que Dios hace hoy. Conozca cómo su iglesia puede participar: compartir testimonios, respaldarlos y difundirlos.'
MAIL = 'mailto:hola@hacedordemilagros.com?subject=Iglesia%20-%20Quiero%20colaborar'

jsonld = json.dumps({
    '@context': 'https://schema.org',
    '@graph': [
        {
            '@type': 'WebPage',
            '@id': URL + '#pagina',
            'name': 'Para iglesias y pastores',
            'description': DESC,
            'url': URL,
            'inLanguage': 'es',
            'isPartOf': {'@id': 'https://hacedordemilagros.com/#website'},
            'about': {'@id': 'https://hacedordemilagros.com/#org'},
        },
        {
            '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Inicio', 'item': 'https://hacedordemilagros.com/'},
                {'@type': 'ListItem', 'position': 2, 'name': 'Para iglesias', 'item': URL},
            ],
        },
    ],
}, ensure_ascii=False, indent=2)

cuerpo = f'''    <nav class="crumbs" aria-label="Ruta"><a href="/">Inicio</a> › Para iglesias</nav>
    <div class="kicker">Para iglesias y pastores</div>
    <h1>Su iglesia tiene las historias. Nosotros, la voz.</h1>
    <p class="intro">Hacedor de Milagros es un podcast cristiano en español donde personas comunes cuentan el milagro que transformó su vida. Si usted es pastor o líder, su congregación puede ser parte de este proyecto de forma sencilla.</p>
    <div class="btns">
      <a class="btn btn-gold" href="{MAIL}">Quiero colaborar</a>
      <a class="btn btn-ghost" href="/#video">Ver el video de presentación</a>
    </div>

    <h2>Qué es Hacedor de Milagros</h2>
    <p>Internet está lleno de contenido que vive del morbo y del miedo. Hacedor de Milagros es el espacio para la otra clase de historias: las de la gente común a la que Dios le cambió la vida, contadas para todo el mundo hispano.</p>
    <ul>
      <li><strong>Verificado.</strong> No contamos rumores: cada testimonio se investiga y se respalda antes de contarlo.</li>
      <li><strong>Cristocéntrico.</strong> Cristo en el centro de cada historia, sin sensacionalismo.</li>
      <li><strong>Esperanza.</strong> Contenido que levanta y renueva la fe.</li>
    </ul>

    <h2>Cómo puede participar su iglesia</h2>
    <h3>1. Comparta testimonios</h3>
    <p>Seguramente en su congregación hay hermanos que vivieron un milagro: una sanidad, una provisión a tiempo, una familia restaurada. Invítelos a contarlo. Pueden escribirlo, grabarlo con su voz o subir un archivo desde el formulario del sitio. Para ayudarles a ordenar su historia preparamos una guía: <a href="/como-contar-tu-testimonio/">Cómo contar tu testimonio</a>.</p>

    <h3>2. Respalde un testimonio</h3>
    <p>Antes de contar una historia buscamos respaldo: documentos, testigos o el aval del pastor cuando es posible. Si alguien de su iglesia comparte su testimonio, su confirmación nos ayuda a contarlo con responsabilidad.</p>

    <h3>3. Difunda</h3>
    <p>Comparta el video de presentación y el <a href="https://www.youtube.com/@podcasthacedordemilagros" target="_blank" rel="noopener">canal de YouTube</a> con su congregación y en sus redes. Cuando salgan los episodios, compartirlos ayuda a que la esperanza llegue a más personas.</p>

    <h3>4. Enlácenos desde su sitio web</h3>
    <p>Si su iglesia tiene página web o una sección de recursos, un enlace a Hacedor de Milagros ayuda a que más personas encuentren estas historias. Puede usar este texto:</p>
    <code class="copy">Hacedor de Milagros: testimonios reales de lo que Dios sigue haciendo hoy. https://hacedordemilagros.com</code>

    <h2>Cómo cuidamos cada testimonio</h2>
    <ol class="steps">
      <li><strong>Escuchamos.</strong> Leemos o escuchamos cada testimonio que llega, con respeto y en oración.</li>
      <li><strong>Conversamos.</strong> Contactamos a la persona para conocer los detalles y entender bien la historia.</li>
      <li><strong>Verificamos.</strong> Buscamos respaldo: documentos, testigos o el aval de su pastor cuando es posible.</li>
      <li><strong>Contamos.</strong> Solo con el consentimiento de la persona, que puede pedir otro nombre o el anonimato.</li>
    </ol>
    <p class="small">Los datos de quienes comparten su testimonio se tratan conforme a nuestro <a href="/aviso-de-privacidad.html">Aviso de Privacidad</a>.</p>

    <h2>Nuestra base</h2>
    <div class="card">
      <p>Creemos en un solo Dios, en Jesucristo como Señor y Salvador, y en la Biblia como Palabra de Dios. Creemos que Dios sigue obrando milagros hoy y que ninguna historia de redención es demasiado pequeña para contarse. Compartimos estos testimonios para dar gloria a Dios y renovar la esperanza de quien los escucha.</p>
    </div>

    <h2>Hablemos</h2>
    <p>Si quiere que su iglesia participe, o tiene preguntas sobre el proyecto, escríbanos a <a class="mail" href="{MAIL}">hola@hacedordemilagros.com</a>. Con gusto le respondemos.</p>
    <div class="btns">
      <a class="btn btn-gold" href="{MAIL}">Escríbanos</a>
      <a class="btn btn-ghost" href="/#nosotros">Quién está detrás</a>
    </div>'''

html = pagina(ruta=RUTA,
              titulo='Para iglesias y pastores | Hacedor de Milagros',
              descripcion=DESC,
              og_titulo='Para iglesias y pastores — Hacedor de Milagros',
              jsonld=jsonld, cuerpo=cuerpo)
os.makedirs(str(REPO) + '/iglesias', exist_ok=True)
open(str(REPO) + '/iglesias/index.html', 'w', encoding='utf-8').write(html)
print('iglesias ok', len(DESC))
