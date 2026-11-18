"""Cabecera (con menú en celular) y pie compartidos por todas las páginas de hacedordemilagros.com.

- comun.py los usa para las páginas generadas (guía, iglesias, madrugada, testimonios, 404).
- aplicar_cabecera.py los inserta en index.html y aviso-de-privacidad.html (entre marcas).
Si cambias el menú o el pie aquí, corre:  python3 _build/aplicar_cabecera.py  y los generadores.
"""

MENU = [
    ('/#escuchalo', 'Escúchalo', None),
    ('/madrugada-de-oracion/', 'Madrugada de Oración', 'madrugada'),
    ('/#testimonio', 'Tu testimonio', None),
    ('/iglesias/', 'Iglesias', 'iglesias'),
    ('/#nosotros', 'Nosotros', None),
]

PIE_ENLACES = [
    ('/', 'Inicio'),
    ('/#escuchalo', 'Escúchalo'),
    ('/#testimonio', 'Tu testimonio'),
    ('/madrugada-de-oracion/', 'Madrugada de Oración'),
    ('/iglesias/', 'Iglesias'),
    ('/#nosotros', 'Nosotros'),
    ('/como-contar-tu-testimonio/', 'Cómo contar tu testimonio'),
    ('/aviso-de-privacidad.html', 'Aviso de Privacidad'),
]

ICONO_MENU = ('<svg class="ico-abrir" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'
              '<svg class="ico-cerrar" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>')


def cabecera(actual=None):
    """actual: 'inicio', 'madrugada', 'iglesias' o None."""
    marca = '#inicio' if actual == 'inicio' else '/'
    enlaces = []
    for href, texto, clave in MENU:
        cur = ' aria-current="page"' if clave and clave == actual else ''
        enlaces.append(f'      <a href="{href}"{cur}>{texto}</a>')
    return f"""<!-- cabecera:inicio -->
<a class="skip" href="#contenido">Saltar al contenido</a>
<header class="nav">
  <div class="nav-in">
    <a class="brand" href="{marca}" aria-label="Hacedor de Milagros, inicio"><svg aria-hidden="true"><use href="#burst"/></svg> Hacedor de Milagros</a>
    <nav class="nav-menu" id="menu" aria-label="Principal">
{chr(10).join(enlaces)}
      <a class="btn btn-gold menu-cta" href="/#avisame">Avísame del estreno</a>
    </nav>
    <div class="nav-acc">
      <a class="btn btn-gold nav-cta" href="/#avisame"><span class="lg">Avísame del estreno</span><span class="sm">Avísame</span></a>
      <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">{ICONO_MENU}<span class="t">Menú</span></button>
    </div>
  </div>
</header>
<!-- cabecera:fin -->"""


SOCIAL = """    <div class="foot-social">
      <a href="https://www.facebook.com/podcasthacedordemilagros" target="_blank" rel="noopener" aria-label="Facebook"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.6 21v-7.6h2.6l.4-3h-3V8.5c0-.87.25-1.46 1.5-1.46h1.6V4.36c-.28-.04-1.22-.12-2.32-.12-2.3 0-3.88 1.4-3.88 3.98v2.2H7.9v3h2.6V21h3.1z" fill="currentColor" stroke="none"/></svg><span>Facebook</span></a>
      <a href="https://www.instagram.com/podcasthacedordemilagros/" target="_blank" rel="noopener" aria-label="Instagram"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="2.8" y="2.8" width="18.4" height="18.4" rx="5.4" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="17.4" cy="6.6" r="1.25" fill="currentColor" stroke="none"/></svg><span>Instagram</span></a>
      <a href="https://www.tiktok.com/@podcasthacedordemilagros" target="_blank" rel="noopener" aria-label="TikTok"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16.5 3c.35 2.1 1.7 3.6 3.7 3.85V9.4c-1.3 0-2.55-.4-3.6-1.1v6.35c0 3.2-2.6 5.55-5.65 5.55S5.3 17.85 5.3 14.9c0-2.75 2.05-5 4.8-5.25v2.65c-1.25.25-2.2 1.2-2.2 2.6 0 1.5 1.2 2.7 2.7 2.7s2.7-1.2 2.7-2.75V3h3.2z" fill="currentColor" stroke="none"/></svg><span>TikTok</span></a>
      <a href="https://www.youtube.com/@podcasthacedordemilagros" target="_blank" rel="noopener" aria-label="YouTube"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M22 8.2a3 3 0 0 0-2.1-2.12C18 5.55 12 5.55 12 5.55s-6 0-7.9.53A3 3 0 0 0 2 8.2 31.3 31.3 0 0 0 1.7 12 31.3 31.3 0 0 0 2 15.8a3 3 0 0 0 2.1 2.12c1.9.53 7.9.53 7.9.53s6 0 7.9-.53A3 3 0 0 0 22 15.8 31.3 31.3 0 0 0 22.3 12 31.3 31.3 0 0 0 22 8.2zM10 15.1V8.9l5.3 3.1-5.3 3.1z" fill="currentColor" stroke="none"/></svg><span>YouTube</span></a>
      <a href="https://www.threads.com/@podcasthacedordemilagros" target="_blank" rel="noopener" aria-label="Threads"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.3 11.3c-.1-.05-.2-.1-.3-.14-.18-3.2-1.95-5.04-4.9-5.06-1.78-.01-3.27.73-4.18 2.1l1.64 1.12c.68-1 1.73-1.22 2.53-1.22h.03c1 .01 1.76.3 2.25.87.36.41.6.98.72 1.7-.9-.15-1.86-.19-2.9-.12-2.9.17-4.77 1.86-4.64 4.2.06 1.2.66 2.22 1.68 2.88.86.55 1.97.82 3.12.76 1.52-.08 2.72-.66 3.55-1.72.63-.8 1.03-1.85 1.2-3.16.72.43 1.25 1 1.54 1.68.5 1.17.53 3.08-1.03 4.64-1.36 1.36-3 1.95-5.48 1.97-2.75-.02-4.83-.9-6.18-2.6C3.48 15.76 3 13.88 3 12s.48-3.76 1.26-4.68C5.6 5.62 7.69 4.74 10.44 4.72c2.77.02 4.9.9 6.32 2.62.7.84 1.22 1.9 1.57 3.13l1.9-.5c-.42-1.52-1.08-2.83-1.98-3.9C16.4 3.9 13.77 2.8 10.45 2.78h-.01C7.13 2.8 4.5 3.9 2.75 6c-1.56 1.87-2.36 4.47-2.39 7.73v.01c.03 3.26.83 5.86 2.39 7.73 1.75 2.1 4.38 3.2 7.69 3.22h.01c2.94-.02 5.02-.79 6.73-2.5 2.24-2.24 2.17-5.05 1.43-6.78-.53-1.24-1.54-2.25-2.92-2.94zm-5 6.37c-1.27.07-2.6-.5-2.66-1.72-.05-.9.64-1.9 2.74-2.02.24-.01.48-.02.71-.02.76 0 1.48.07 2.13.21-.24 3.03-1.66 3.48-2.92 3.55z" fill="currentColor" stroke="none"/></svg><span>Threads</span></a>
    </div>"""


def pie():
    enlaces = '\n'.join(f'      <a href="{h}">{t}</a>' for h, t in PIE_ENLACES)
    return f"""<!-- pie:inicio -->
<footer>
  <div class="wrap">
    <div class="foot-brand"><svg aria-hidden="true"><use href="#burst"/></svg> Hacedor de Milagros</div>
    <div class="foot-plat">Escríbenos: <a class="g" href="mailto:hola@hacedordemilagros.com">hola@hacedordemilagros.com</a></div>
{SOCIAL}
    <div class="foot-links">
{enlaces}
    </div>
    <div class="foot-copy">© 2026 Hacedor de Milagros · Historias reales de fe</div>
  </div>
</footer>
<!-- pie:fin -->"""


CSS = """
.skip{position:absolute;left:12px;top:-80px;z-index:100;background:var(--gold);color:var(--deep);font-family:'Outfit',sans-serif;font-weight:700;padding:12px 18px;border-radius:12px;text-decoration:none!important}
.skip:focus{top:12px}
a:focus-visible,button:focus-visible,summary:focus-visible,[tabindex]:focus-visible{outline:3px solid var(--goldb);outline-offset:3px}
input:focus-visible,textarea:focus-visible,select:focus-visible{outline:none;border-color:var(--gold)!important;box-shadow:0 0 0 3px rgba(244,183,64,.4)}
header.nav{position:sticky;top:0;z-index:50;backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);background:rgba(10,21,48,.88);border-bottom:1px solid rgba(247,241,227,.08)}
header.nav .nav-in{display:flex;align-items:center;justify-content:space-between;gap:16px;height:68px;max-width:1120px;margin:0 auto;padding:0 20px}
header.nav .brand{display:flex;align-items:center;gap:11px;font-family:'Outfit',sans-serif;font-weight:700;font-size:18px;color:var(--cream);flex:none;text-decoration:none!important;min-height:44px}
header.nav .brand svg{width:34px;height:34px}
.nav-menu{display:flex;align-items:center;gap:24px;font-size:15px;color:var(--muted);font-weight:500}
.nav-menu a{display:inline-flex;align-items:center;min-height:44px;color:inherit;text-decoration:none}
.nav-menu a:hover{color:var(--goldb)}
.nav-menu a[aria-current="page"]{color:var(--goldb);text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:8px}
header.nav .nav-menu .menu-cta{display:none}
.nav-acc{display:flex;align-items:center;gap:10px;flex:none}
header.nav .btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;font-family:'Outfit',sans-serif;font-weight:700;font-size:15px;line-height:1.2;padding:12px 22px;min-height:44px;border:none;border-radius:999px;cursor:pointer;text-decoration:none!important;transition:background .15s}
header.nav .btn-gold{background:var(--gold);color:var(--deep)}
header.nav .btn-gold:hover{background:var(--goldb);transform:none}
.nav-cta .sm{display:none}
.menu-btn{display:none;align-items:center;gap:8px;min-height:44px;padding:0 16px;border-radius:999px;border:1.5px solid rgba(247,241,227,.3);background:transparent;color:var(--cream);font:600 15px 'Outfit',sans-serif;cursor:pointer}
.menu-btn:hover{border-color:var(--gold)}
.menu-btn svg{width:20px;height:20px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round}
.menu-btn .ico-cerrar,header.nav.abierto .menu-btn .ico-abrir{display:none}
header.nav.abierto .menu-btn .ico-cerrar{display:block}
@media(max-width:1079px){
  .menu-btn{display:inline-flex}
  .nav-menu{display:none;position:absolute;left:0;right:0;top:100%;flex-direction:column;align-items:stretch;gap:0;background:#0a1530;border-bottom:1px solid rgba(247,241,227,.12);box-shadow:0 18px 30px rgba(0,0,0,.4);padding:6px max(20px,calc((100% - 1080px)/2)) 22px;font-size:17px;color:var(--cream)}
  header.nav.abierto .nav-menu{display:flex;animation:menuIn .18s ease-out}
  .nav-menu a{min-height:54px;border-bottom:1px solid rgba(247,241,227,.08)}
  .nav-menu a[aria-current="page"]{text-decoration:none;box-shadow:inset 3px 0 0 var(--gold);padding-left:14px}
}
@keyframes menuIn{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:none}}
@media(max-width:560px){header.nav .nav-cta{padding:12px 18px}.nav-cta .lg{display:none}.nav-cta .sm{display:inline}}
@media(max-width:480px){
  header.nav .nav-acc .nav-cta{display:none}
  header.nav .nav-menu .menu-cta{display:inline-flex;justify-content:center;margin-top:18px;border-bottom:0;min-height:52px}
}
@media(max-width:360px){header.nav .brand{font-size:16px;gap:8px}header.nav .brand svg{width:30px;height:30px}.menu-btn{padding:0;width:44px;justify-content:center}.menu-btn .t{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}}
@media (prefers-reduced-motion:reduce){header.nav.abierto .nav-menu{animation:none}}
"""

CSS_PIE = """
footer{background:var(--deep);border-top:1px solid rgba(247,241,227,.08);padding:52px 0 34px;text-align:center;color:var(--muted2);font-size:15px}
.foot-brand{display:inline-flex;align-items:center;gap:11px;font-family:'Outfit',sans-serif;font-weight:700;font-size:18px;margin-bottom:12px;color:var(--cream)}
.foot-brand svg{width:40px;height:40px}
.foot-links{display:flex;gap:6px 20px;justify-content:center;flex-wrap:wrap;color:var(--muted);font-size:15px;margin:14px 0}
.foot-links a{color:var(--muted)}
.foot-links a:hover{color:var(--goldb)}
.foot-links a,.foot-social a,.foot-plat a{display:inline-flex;align-items:center;min-height:44px;padding:0 4px}
.foot-plat{color:var(--muted2);font-size:15px;margin-top:8px}
.foot-plat a.g{color:var(--gold)}
.foot-social{display:flex;flex-wrap:wrap;gap:18px;justify-content:center;margin:14px 0;color:var(--muted)}
.foot-social a{gap:7px;font-size:15px;font-weight:600;color:var(--muted)}
.foot-social svg{width:18px;height:18px;flex:none}
.foot-social a:hover{color:var(--goldb)}
.foot-copy{color:#9fb0cf;font-size:14px;margin-top:20px}
"""

JS = """
(function(){
  var h=document.querySelector('header.nav'),b=h&&h.querySelector('.menu-btn'),m=document.getElementById('menu');
  if(!b||!m)return;
  function poner(abrir){h.classList.toggle('abierto',abrir);b.setAttribute('aria-expanded',abrir?'true':'false');b.querySelector('.t').textContent=abrir?'Cerrar':'Menú';}
  b.addEventListener('click',function(){poner(!h.classList.contains('abierto'));});
  m.addEventListener('click',function(e){if(e.target.closest('a'))poner(false);});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&h.classList.contains('abierto')){poner(false);b.focus();}});
  document.addEventListener('click',function(e){if(h.classList.contains('abierto')&&!h.contains(e.target))poner(false);});
  window.addEventListener('resize',function(){if(window.innerWidth>=1080&&h.classList.contains('abierto'))poner(false);});
})();
"""

THEME = '<meta name="theme-color" content="#0a1530">'
