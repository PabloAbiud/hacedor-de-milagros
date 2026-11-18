"""Genera 404.html: la página que GitHub Pages muestra cuando una dirección no existe."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import pagina, REPO

cuerpo = '''    <div class="kicker">Error 404</div>
    <h1>No encontramos esta página</h1>
    <p class="intro">Puede que el enlace esté mal escrito o que la página haya cambiado de lugar. Desde aquí puedes seguir:</p>
    <div class="btns">
      <a class="btn btn-gold" href="/">Ir al inicio</a>
      <a class="btn btn-ghost" href="/madrugada-de-oracion/">Madrugada de Oración</a>
      <a class="btn btn-ghost" href="/#testimonio">Comparte tu testimonio</a>
    </div>
    <p class="small">¿Llegaste aquí desde un enlace nuestro? Avísanos a <a class="mail" href="mailto:hola@hacedordemilagros.com?subject=Enlace%20roto">hola@hacedordemilagros.com</a> para arreglarlo.</p>'''

html = pagina(ruta='/404.html', titulo='Página no encontrada | Hacedor de Milagros',
              descripcion='Esta página no existe o cambió de lugar.',
              og_titulo='Página no encontrada — Hacedor de Milagros',
              jsonld=json.dumps({'@context': 'https://schema.org', '@type': 'WebPage',
                                 'name': 'Página no encontrada', 'inLanguage': 'es'}, ensure_ascii=False),
              cuerpo=cuerpo)
# Una página de error no se indexa ni tiene dirección canónica
html = html.replace('<meta name="robots" content="index, follow">', '<meta name="robots" content="noindex">', 1)
html = html.replace('<link rel="canonical" href="https://hacedordemilagros.com/404.html">\n', '', 1)
(REPO / '404.html').write_text(html, encoding='utf-8')
print('404 ok')
