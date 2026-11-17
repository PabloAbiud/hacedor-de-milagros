import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import pagina, REPO

RUTA = '/como-contar-tu-testimonio/'
URL = 'https://hacedordemilagros.com' + RUTA
DESC = 'Guía sencilla para contar lo que Dios hizo en tu vida: cómo ordenar tu historia, qué incluir, cuánto debe durar y cómo compartirla con Hacedor de Milagros.'

FAQ = [
    ('¿Mi historia es demasiado pequeña para contarse?',
     'No. Creemos que ninguna historia de redención es demasiado pequeña para contarse. Lo que para ti parece algo sencillo puede ser justo lo que otra persona necesita escuchar hoy.'),
    ('¿Tiene que ser un milagro de sanidad?',
     'No. También buscamos historias de provisión, de familias restauradas, de libertad de adicciones, de protección y de vidas que Dios cambió por completo.'),
    ('¿Puedo compartir mi testimonio sin dar mi nombre?',
     'Sí. En el formulario puedes pedir que usemos otro nombre o que tu historia se cuente de forma anónima. Solo necesitamos tu correo o tu WhatsApp para poder contactarte.'),
    ('¿Necesito que mi pastor confirme mi historia?',
     'No es obligatorio. Si alguien puede confirmarla (tu pastor, un familiar o un médico), nos ayuda a respaldarla, pero puedes enviarla de todos modos.'),
    ('¿Desde qué país puedo enviarla?',
     'Desde cualquier país. Hacedor de Milagros es para todo el mundo hispano.'),
]

jsonld = json.dumps({
    '@context': 'https://schema.org',
    '@graph': [
        {
            '@type': 'Article',
            '@id': URL + '#articulo',
            'headline': 'Cómo contar tu testimonio',
            'description': DESC,
            'inLanguage': 'es',
            'datePublished': '2026-11-15',
            'dateModified': '2026-11-15',
            'mainEntityOfPage': URL,
            'image': 'https://hacedordemilagros.com/og.jpg',
            'author': {'@type': 'Person', 'name': 'Pablo Abiud Cabadas Reyna', 'url': 'https://hacedordemilagros.com/#nosotros'},
            'publisher': {'@id': 'https://hacedordemilagros.com/#org'},
        },
        {
            '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Inicio', 'item': 'https://hacedordemilagros.com/'},
                {'@type': 'ListItem', 'position': 2, 'name': 'Cómo contar tu testimonio', 'item': URL},
            ],
        },
        {
            '@type': 'FAQPage',
            'mainEntity': [
                {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ
            ],
        },
    ],
}, ensure_ascii=False, indent=2)

faq_html = '\n'.join(f'    <details>\n      <summary>{q}</summary>\n      <p>{a}</p>\n    </details>' for q, a in FAQ)

cuerpo = f'''    <nav class="crumbs" aria-label="Ruta"><a href="/">Inicio</a> › Cómo contar tu testimonio</nav>
    <div class="kicker">Guía</div>
    <h1>Cómo contar tu testimonio</h1>
    <p class="intro">Tu historia con Dios no tiene que ser perfecta para contarse; tiene que ser verdadera. Esta guía te ayuda a ordenarla para que quien la escuche pueda ver la mano de Dios en ella.</p>

    <div class="verse">
      <p>«Vete a tu casa, a los tuyos, y cuéntales cuán grandes cosas el Señor ha hecho contigo, y cómo ha tenido misericordia de ti.»</p>
      <cite>Marcos 5:19</cite>
    </div>

    <h2>Por qué vale la pena contarlo</h2>
    <p>Lo que Dios hizo contigo no es solo para ti. Cuando lo cuentas, alguien que hoy está donde tú estuviste recibe esperanza. La Biblia lo dice así: «Díganlo los redimidos de Jehová» (Salmo 107:2). Y en Apocalipsis 12:11 leemos que los creyentes vencieron «por medio de la sangre del Cordero y de la palabra del testimonio de ellos».</p>

    <h2><span class="num">1</span>Ordena tu historia en tres momentos</h2>
    <ul>
      <li><strong>Antes.</strong> Cómo era tu vida o cuál era la situación. ¿Qué te preocupaba? ¿Qué parecía imposible?</li>
      <li><strong>Lo que Dios hizo.</strong> El momento en que todo cambió: qué pasó, cuándo, dónde y quién estaba contigo.</li>
      <li><strong>Hoy.</strong> Cómo es tu vida ahora y qué aprendiste de Dios en el camino.</li>
    </ul>
    <p class="soft">Si solo recuerdas esto, ya tienes un buen testimonio.</p>

    <h2><span class="num">2</span>Cuenta los detalles que solo tú viviste</h2>
    <p>Fechas aproximadas, lugares, lo que sentiste, lo que oraste, lo que te dijeron. Los detalles concretos hacen que una historia se crea y se recuerde. En lugar de «me sentía muy mal», cuenta que llevabas tres semanas sin poder dormir.</p>

    <h2><span class="num">3</span>Pon a Cristo en el centro</h2>
    <p>El protagonista no eres tú ni el milagro: es Dios. Cuenta también lo que aprendiste de Él, no solo lo que recibiste. Como dijo el hombre que Jesús sanó: «una cosa sé, que habiendo yo sido ciego, ahora veo» (Juan 9:25).</p>

    <h2><span class="num">4</span>Sé honesto, sin exagerar</h2>
    <ul>
      <li>Cuenta lo que pasó tal como pasó. Si un médico, un tratamiento o una persona fueron parte de la historia, inclúyelos: Dios también obra a través de ellos.</li>
      <li>Si el proceso fue lento, dilo. Si hay cosas que todavía no entiendes, también.</li>
      <li>Si tienes algo que respalde tu historia (estudios médicos, documentos o alguien que lo vivió contigo), menciónalo. Antes de contar un testimonio, buscamos ese respaldo.</li>
    </ul>
    <p class="small">Compartir un testimonio de sanidad no sustituye la atención médica. Si estás en tratamiento, sigue las indicaciones de tu médico.</p>

    <h2><span class="num">5</span>Usa tus propias palabras</h2>
    <p>No necesitas sonar como predicador. Cuéntalo como se lo contarías a un amigo en la mesa. Evita las palabras que solo entiende quien va a la iglesia: quien te escuche quizá nunca ha pisado una.</p>

    <h2><span class="num">6</span>Cuida a los demás</h2>
    <p>Si en tu historia aparecen otras personas, cuida su privacidad: no des nombres completos sin su permiso y no expongas detalles que les puedan doler. Con menores de edad, todavía más cuidado. Tú también puedes pedir que cambiemos tu nombre o que tu historia sea anónima.</p>

    <h2>¿Cuánto debe durar?</h2>
    <ul>
      <li><strong>Escrito:</strong> una o dos páginas bastan.</li>
      <li><strong>En audio:</strong> entre 3 y 5 minutos.</li>
      <li>Si tu historia es más larga, no te preocupes: si la elegimos para el podcast, te contactamos para conversarla con calma.</li>
    </ul>

    <h2>Preguntas que te pueden ayudar a empezar</h2>
    <ul>
      <li>¿Qué estaba pasando en tu vida antes del milagro?</li>
      <li>¿Cuál fue el momento más difícil?</li>
      <li>¿Qué le pediste a Dios? ¿Quién oró contigo?</li>
      <li>¿Cuándo te diste cuenta de que Dios estaba obrando?</li>
      <li>¿Qué cambió en ti, además de la situación?</li>
      <li>¿Qué le dirías a alguien que hoy está pasando por lo mismo?</li>
    </ul>

    <h2>Un ejemplo</h2>
    <div class="card">
      <span class="label">Ejemplo ilustrativo · no es un testimonio real</span>
      <p><strong>Antes:</strong> En 2019 me quedé sin trabajo, con dos hijos en la escuela. Pasaron cuatro meses y ya debíamos dos meses de renta.</p>
      <p><strong>Lo que Dios hizo:</strong> Una noche, mi esposa y yo oramos juntos por primera vez en años. Le dijimos a Dios que ya no sabíamos qué hacer. Dos días después me llamó un hermano de la iglesia: en su empresa buscaban a alguien con mi experiencia.</p>
      <p><strong>Hoy:</strong> Tengo ese trabajo desde hace cinco años. Pero lo que más cambió fue mi casa: ahora oramos juntos cada noche. Aprendí que Dios no llega tarde.</p>
    </div>

    <h2>Cómo compartirlo con Hacedor de Milagros</h2>
    <ol class="steps">
      <li>Llena el formulario: escribe tu historia, grábala con tu voz (hasta 5 minutos) o sube un archivo de Word o PDF.</li>
      <li>La leemos o la escuchamos con respeto y en oración.</li>
      <li>Si necesitamos más detalles, te contactamos por el medio que nos dejaste.</li>
      <li>Buscamos respaldo: documentos, testigos o el aval de tu pastor cuando es posible.</li>
      <li>Solo se publica con tu consentimiento. No todas las historias se publican, pero todas las valoramos.</li>
    </ol>
    <div class="btns">
      <a class="btn btn-gold" href="/#testimonio">Comparte tu testimonio</a>
      <a class="btn btn-ghost" href="/iglesias/">¿Eres pastor? Lee esto</a>
    </div>

    <h2>Preguntas frecuentes</h2>
{faq_html}

    <hr>
    <p class="small">Texto bíblico tomado de la Santa Biblia, versión Reina-Valera 1960 © Sociedades Bíblicas en América Latina, 1960. Renovado © Sociedades Bíblicas Unidas, 1988. Utilizado con permiso.</p>'''

html = pagina(ruta=RUTA,
              titulo='Cómo contar tu testimonio cristiano | Hacedor de Milagros',
              descripcion=DESC,
              og_titulo='Cómo contar tu testimonio — Hacedor de Milagros',
              jsonld=jsonld, cuerpo=cuerpo)
import os
os.makedirs(str(REPO) + '/como-contar-tu-testimonio', exist_ok=True)
open(str(REPO) + '/como-contar-tu-testimonio/index.html', 'w', encoding='utf-8').write(html)
print('guia ok', len(DESC))
