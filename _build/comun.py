import re, sys, os
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cabecera as cab
# Raíz del sitio (la carpeta que contiene _build/)
REPO = Path(__file__).resolve().parent.parent
SRC = REPO / 'aviso-de-privacidad.html'
a=open(SRC,encoding='utf-8').read()
BASE_CSS=re.search(r'<style>(.*?)</style>',a,re.S).group(1)
BURST=re.search(r'(<svg width="0" height="0".*?</svg>)',a,re.S).group(1)
EXTRA_CSS='''
.btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;font-family:'Outfit',sans-serif;font-weight:700;font-size:16px;padding:14px 26px;border-radius:999px;min-height:48px;text-decoration:none!important}
.btn-gold{background:var(--gold);color:var(--deep)}
.btn-gold:hover{background:var(--goldb)}
.btn-ghost{border:1.5px solid rgba(247,241,227,.3);color:var(--cream)}
.btn-ghost:hover{border-color:var(--gold);color:var(--goldb)}
.btns{display:flex;flex-wrap:wrap;gap:12px;margin:22px 0}
.verse{border-left:3px solid var(--gold);padding:6px 0 6px 18px;margin:24px 0}
.verse p{font-family:'Outfit',sans-serif;font-size:19px;font-weight:500;color:var(--cream);margin:0}
.verse cite{display:block;margin-top:6px;font-style:normal;font-size:14px;letter-spacing:2px;text-transform:uppercase;color:var(--muted2)}
.steps{list-style:none;padding:0;margin:18px 0;counter-reset:s}
.steps li{counter-increment:s;position:relative;padding-left:46px;margin:14px 0}
.steps li::before{content:counter(s);position:absolute;left:0;top:1px;width:30px;height:30px;border-radius:50%;background:rgba(244,183,64,.15);border:1px solid rgba(244,183,64,.5);color:var(--goldb);font-family:'Outfit',sans-serif;font-weight:700;font-size:15px;display:grid;place-items:center}
.label{display:inline-block;font-family:'Outfit',sans-serif;font-size:12px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:var(--deep);background:var(--gold);padding:3px 11px;border-radius:999px;margin-bottom:10px}
details{background:rgba(22,41,79,.35);border:1px solid rgba(247,241,227,.1);border-radius:14px;padding:4px 20px;margin:12px 0}
summary{cursor:pointer;font-family:'Outfit',sans-serif;font-weight:600;font-size:17px;padding:14px 0;color:var(--cream);list-style-position:outside}
details[open] summary{color:var(--goldb)}
details p{margin:0 0 14px}
.crumbs{font-size:14px;color:var(--muted2);margin-bottom:18px}
.crumbs a{color:var(--muted2)}
code.copy{display:block;background:#0b1836;border:1px solid rgba(247,241,227,.16);border-radius:12px;padding:14px 16px;font-size:15px;color:var(--cream);white-space:normal;margin:12px 0}
.small{font-size:14px;color:var(--muted2)}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
'''
def pagina(*, ruta, titulo, descripcion, og_titulo, jsonld, cuerpo, actual=None):
    url=f'https://hacedordemilagros.com{ruta}'
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{cab.THEME}
<title>{titulo}</title>
<link rel="canonical" href="{url}">
<meta name="description" content="{descripcion}">
<meta name="robots" content="index, follow">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Hacedor de Milagros">
<meta property="og:locale" content="es_MX">
<meta property="og:title" content="{og_titulo}">
<meta property="og:description" content="{descripcion}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://hacedordemilagros.com/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{BASE_CSS}{EXTRA_CSS}{cab.CSS}{cab.CSS_PIE}</style>
<script type="application/ld+json">
{jsonld}
</script>
</head>
<body>

{BURST}

{cab.cabecera(actual)}

<main id="contenido">
  <div class="wrap">
{cuerpo}
  </div>
</main>

{cab.pie()}

<script>{cab.JS}</script>

</body>
</html>
'''
