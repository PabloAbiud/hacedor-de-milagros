"""Pone la cabecera (con menú en celular) y el pie compartidos en las páginas escritas a mano:
index.html (solo cabecera; su pie es propio) y aviso-de-privacidad.html (cabecera y pie).

Uso:  python3 _build/aplicar_cabecera.py
Se puede correr varias veces: reemplaza lo que esté entre las marcas.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cabecera as cab
from comun import REPO

PAGINAS = [
    # archivo, página actual, ¿lleva el pie compartido?
    ('index.html', 'inicio', False),
    ('aviso-de-privacidad.html', None, True),
]


def reemplazar_bloque(s, patron_viejo, ini, fin, nuevo):
    """Reemplaza lo que hay entre marcas; si no hay marcas, reemplaza el primer patron_viejo."""
    if ini in s:
        return re.sub(re.escape(ini) + r'.*?' + re.escape(fin), lambda m: nuevo, s, count=1, flags=re.S)
    m = re.search(patron_viejo, s, re.S)
    if not m:
        sys.exit(f'No encontré el bloque a reemplazar ({patron_viejo[:30]}…)')
    return s[:m.start()] + nuevo + s[m.end():]


def poner_etiqueta(s, etiqueta, contenido, antes_de):
    """<style id=…> o <script id=…>: reemplaza si existe; si no, lo agrega antes de `antes_de`."""
    tag = 'style' if etiqueta.endswith('css') else 'script'
    bloque = f'<{tag} id="{etiqueta}">{contenido}</{tag}>'
    # Solo al inicio de una línea, para no confundirlo con un comentario que lo mencione
    patron = rf'^<{tag} id="{etiqueta}">.*?</{tag}>'
    if re.search(patron, s, re.S | re.M):
        return re.sub(patron, lambda m: bloque, s, count=1, flags=re.S | re.M)
    return s.replace(antes_de, bloque + '\n' + antes_de, 1)


for archivo, actual, con_pie in PAGINAS:
    p = REPO / archivo
    s = p.read_text(encoding='utf-8')
    s = reemplazar_bloque(s, r'<header class="nav">.*?</header>', '<!-- cabecera:inicio -->',
                          '<!-- cabecera:fin -->', cab.cabecera(actual))
    if con_pie:
        s = reemplazar_bloque(s, r'<footer>.*?</footer>', '<!-- pie:inicio -->', '<!-- pie:fin -->', cab.pie())
    s = s.replace('<main>', '<main id="contenido">', 1)
    if 'name="theme-color"' not in s:
        s = s.replace('<meta name="viewport" content="width=device-width, initial-scale=1">',
                      '<meta name="viewport" content="width=device-width, initial-scale=1">\n' + cab.THEME, 1)
    s = poner_etiqueta(s, 'cabecera-css', cab.CSS + cab.CSS_PIE, '</head>')
    s = poner_etiqueta(s, 'cabecera-js', cab.JS, '</body>')
    p.write_text(s, encoding='utf-8')
    print('Listo:', archivo)
