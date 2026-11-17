# Cómo publicar un testimonio en hacedordemilagros.com

Escrito el 16 de noviembre de 2026.

Cada testimonio tiene su propia página en `hacedordemilagros.com/testimonios/nombre-del-testimonio/`, con el video, un resumen, el versículo, la transcripción y cómo se verificó. La página "Testimonios" (`/testimonios/`) y las tarjetas del inicio se arman solas con los testimonios que haya.

Las carpetas que empiezan con guion bajo (`_build` y `_testimonios`) no se publican en el sitio: son las herramientas y los datos.

## Lo más fácil

Pídeselo a Claude: "Publica el testimonio de María", y dale lo que dice la lista de abajo. Claude llena el archivo, revisa la página y la publica.

## Lo que se necesita de cada testimonio

Antes de publicar:

1. **Permiso por escrito** de la persona para publicar su historia (un correo o mensaje basta). Sin esto no se publica: el archivo debe decir `"consentimiento": true`.
2. **Cómo quiere aparecer:** con su nombre, con otro nombre o anónima.
3. **El respaldo:** qué se revisó (documentos, testigos, su pastor). Va en la sección "Cómo verificamos esta historia".
4. **El video ya subido a YouTube**, en la lista "Testimonios" del canal.

## Los pasos (si se hace a mano)

1. Copia `_build/2026-11-16-plantilla-testimonio.json` a la carpeta `_testimonios/` con el nombre `AAAA-MM-DD-nombre.json` (la fecha es la de publicación).
2. Llena los campos (abajo se explica cada uno) y **borra la línea `"borrador": true`**.
3. Desde la carpeta del sitio, corre: `python3 _build/testimonios.py`
4. Revisa la página en tu computadora y súbela con git (ver `2026-11-14-como-actualizar-la-web.md`).

## Los campos

| Campo | Qué va | ¿Obligatorio? |
|---|---|---|
| `slug` | La parte final de la dirección: minúsculas, sin acentos, con guiones. Ej. `sanidad-de-cancer-maria` | Sí |
| `publicado` | Fecha de publicación `AAAA-MM-DD`. Si es una fecha futura, no se publica hasta ese día (hay que volver a correr el programa ese día). | Sí |
| `categoria` | `sanidad`, `provision`, `familia` o `liberacion` | Sí |
| `titulo` | El título grande de la página | Sí |
| `titulo_seo` | Versión corta para Google (máx. 60 caracteres) | No |
| `descripcion` | Texto para Google y WhatsApp (máx. 155 caracteres) | Sí |
| `persona` | Nombre como quiere aparecer | No |
| `anonimo` | `true` si no quiere nombre | No |
| `nombre_cambiado` | `true` si se usó otro nombre (la página lo aclara) | No |
| `pais` | País de la persona | Sí |
| `youtube_id` | Los 11 caracteres del video: en `youtube.com/watch?v=AbCdEfGhIjK` es `AbCdEfGhIjK` | Sí |
| `duracion` | Duración del video: `PT18M32S` = 18 min 32 s; `PT1H5M` = 1 h 5 min | Sí |
| `spotify`, `apple` | Enlaces al episodio cuando el podcast esté en esas plataformas | No |
| `resumen` | Dos o tres párrafos | Sí |
| `versiculo` | Texto exacto en Reina-Valera 1960 y la cita | No |
| `momentos` | Minutos importantes del video (Google los muestra en los resultados) | No |
| `verificacion` | Cómo se respaldó la historia | Sí |
| `transcripcion` | El texto completo del episodio, en párrafos | No, pero ayuda mucho en Google |
| `og_imagen` | Imagen para compartir; si no se pone, usa la miniatura de YouTube | No |
| `consentimiento` | `true` solo si hay permiso por escrito | Sí |
| `borrador` | `true` para guardarlo sin publicar | No |

## Si alguien retira su permiso

Borra su archivo de `_testimonios/` y vuelve a correr `python3 _build/testimonios.py`. El programa quita su página, la saca del índice, del inicio y del sitemap. Después hay que pedir a Google que la retire (Search Console → Retirada de URLs) y bajar el video de YouTube.

## Las otras páginas

En `_build/` también están los programas que generan las demás páginas: `guia.py` (Cómo contar tu testimonio), `iglesias.py` (Para iglesias) y `madrugada.py` (Madrugada de Oración). Todos usan `comun.py`, que tiene el diseño compartido.
