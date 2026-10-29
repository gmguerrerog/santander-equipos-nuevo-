# Análisis exhaustivo — santanderequipos.cl

Fecha del análisis: 29-10-2026. Fuente: HTML de 14 páginas descargado en `html/`.

## 1. Resumen ejecutivo

- **Qué es:** sitio corporativo/catálogo de **Santander Equipos**, fabricante y reparador de equipamiento para transporte terrestre (semirremolques) en Chile. Lema: *"Ingeniería en Movimiento"*. Fundada en 2009, certificación ISO 9001 (el sitio dice "2008").
- **Tecnología:** WordPress 6.9.11 + tema **Divi** (Elegant Themes) con 35 referencias al tema; sin JSON-LD, sin analytics detectables.
- **Estado general:** sitio funcional pero con contenido desactualizado/incompleto (texto "Lorem Ipsum" en home, blog vacío, página "pruebas" y "sitio-en-mantencion" indexables, sin H1 en la mayoría de páginas, sin meta description).
- **Conversión principal:** WhatsApp (+56 9 9558 6223), formulario de contacto Divi y widget Joinchat.

## 2. Estructura del sitio (sitemap)

Menú: Inicio · Sobre Santander · Equipos · Artículos · Contacto

Páginas (wp-sitemap-posts-page):
`/`, `/sobre-santander/`, `/equipos/`, `/articulos/`, `/contacto/`, `/certificacion-iso/`, `/certificados-clientes-y-proveedores/`, `/premios/`, **`/sitio-en-mantencion/`**, **`/pruebas/`** (las dos últimas son páginas internas que no deberían estar publicadas).

Portafolio (CPT `project`, categoría `semirremolques`):
`/project/minero/`, `/project/speed-sider/`, `/project/plano/`, `/project/forestal/`, `/project/carga-seca/`, `/project/botellero/`

Sitemap: `https://santanderequipos.cl/wp-sitemap.xml` (nativo de WordPress; incluye también `wp-sitemap-users-1.xml`, que expone autores). `robots.txt` mínimo (solo bloquea `/wp-admin/`).

## 3. Contenido por página

| Página | Contenido clave |
|---|---|
| **Inicio** | Pantalla de carga con GIF (`forestal.gif`), hero "SANTANDER EQUIPOS – Ingeniería en Movimiento", botón "Nuestros Equipos", grilla filtrable de 6 semirremolques, banner "EQUIPOS — % MÁS LIVIANOS" (versión desktop y móvil), "Nuestra Visión", 4 pilares (Leyes, ISO 9001, Volumen, Light), "Nuestros Clientes" (DAF, FAW, Hino, Scania, International), bloque Artículos/Noticias (vacío), mapa Google. |
| **Sobre Santander** | Historia (fundada 2009), misión, ISO, homologación con la mayoría de marcas de camiones; accesos a "Ver Leyes" y "Ver Certificado". |
| **Equipos** | Misma grilla de 6 semirremolques con filtro All / Semirremolques. |
| **Ficha de equipo** | "Descripción Técnica": aplicación, tipo de acero, dimensiones, estructura, piso, suspensión, cortinas, sistema eléctrico, frenos (normal y EBS), perno rey… + botón "descargar ficha técnica" (PDF). |
| **Artículos** | "Artículos, Noticias y Novedades": **sin entradas** ("No Results Found"), dos banners de webinar y formulario. |
| **Contacto** | Formulario (Nombre, Correo, Mensaje), 3 botones WhatsApp (Ventas, Proveedores, Contabilidad — los tres apuntan al **mismo número**), mapa Google. |
| **Certificación ISO / Certificados / Premios** | Textos cortos; enlaces a 7 PDFs normativos y al certificado ISO 9001; 3 imágenes de premios (escaneos CamScanner). |

### Productos (semirremolques)
Minero · Speed Sider · Plano · Forestal · Carga Seca · Botellero.
Especificaciones destacadas (de Minero y Botellero): acero **STRENX 700** (SSAB, Suecia), ejes de disco europeos 13.000 kg, suspensiones Suspensys, frenos Bendix, opción **EBS**, cortinas PVC 900 g/m², LED multivoltaje. Dimensiones Minero: 12.400–15.800 mm largo, 2.600 ancho, 2.700–3.000 alto. Botellero: 14.400–15.800 largo, 4.200 alto, piso aluminio diamantado 3 mm. Las 6 fichas completas están en `assets/pdfs/`.

## 4. Datos de contacto y redes

- WhatsApp / tel: **+56 9 9558 6223**
- Mapa: ficha Google "Santander Equipos", coordenadas aprox. **-33.3093, -70.7051** (zona poniente de Santiago). No se publica dirección en texto ni correo visible.
- Facebook: facebook.com/profile.php?id=100088722630884
- Instagram: @santander_equipos
- X/Twitter: @santander_equip
- LinkedIn: perfil personal "Logística Santander" (no página de empresa)
- Chat: Joinchat ("Hola, dígame en qué lo puedo ayudar?")

## 5. Diseño y marca

- **Logo:** `assets/logo/Logo.png` (316×78 PNG transparente). Favicon: 512 px y variantes 270/192/180/32.
- **Colores detectados en el CSS:** azul `#2ea3f2` (acento por defecto de Divi, 16 usos), azul corporativo `#2f5599`, negro `#0a0a0a`/`#000000`, grises `#828282`, `#2a2a2a`, `#eeeff3`, blanco `#ffffff`. Revisar el logo para confirmar la paleta de marca real.
- **Tipografías:** Open Sans (cuerpo), Sarabun (todos los pesos, pesada) y Muli 700; iconos ETmodules y FontAwesome.
- **Estilo:** fotos de producto 700×400 sobre fondos oscuros, banners con porcentaje "% más livianos", pantalla de carga con GIF.

## 6. Tecnología

- WordPress 6.9.11, tema **Divi** (builder `et_pb_*`), formulario nativo de Divi (`et_pb_contact_form`).
- Plugins detectados: Divi Essential, Supreme Modules Pro for Divi, Popups for Divi, Page Loader by Bonfire, Creame WhatsApp Me (Joinchat), WP-PageNavi.
- Sin Google Analytics / GTM / Pixel detectados en el HTML.
- Recursos remotos: Google Fonts, Google Maps embed.

## 7. Auditoría SEO / calidad

**Problemas encontrados (por prioridad):**
1. **Sin `<meta name="description">` ni Open Graph/Twitter** en las páginas revisadas.
2. **Sin H1** en Inicio, Sobre Santander, Equipos y Contacto (sí lo tienen Artículos y fichas de producto).
3. **Sin datos estructurados** (JSON-LD): faltan `Organization`/`LocalBusiness` y `Product`.
4. **Lorem Ipsum** visible en el pilar "Volumen" del home.
5. **Imágenes sin `alt`**: 9 de 21 `<img>` del home sin texto alternativo útil.
6. **Páginas de prueba/mantención publicadas** (`/pruebas/`, `/sitio-en-mantencion/`) y `wp-sitemap-users` expuesto.
7. **Blog vacío** con mensaje "No Results Found" visible y bloque de noticias vacío en el home.
8. **Enlaces mixtos http/https** (logo y menú Inicio con `http://`).
9. **Texto con errores:** "ISO 9001-2008" (norma obsoleta; vigente 9001:2015), "poveedores", "insumosy", "ontener", "fabricación y reparación e todo tipo".
10. **Tres botones WhatsApp con el mismo número** (Ventas, Proveedores, Contabilidad); el rótulo "LLAMAR A VENTAS" apunta a WhatsApp.
11. **Peso:** fichas técnicas PDF de hasta 19 MB (Speed Sider); imágenes en PNG/JPG sin WebP; carga de Sarabun con todos los pesos; viewport con `maximum-scale=1, user-scalable=0` (perjudica accesibilidad).
12. **Títulos `<title>`** genéricos ("Equipos – Santander Equipos") sin palabras clave (semirremolques, Chile).
13. Pantalla de carga con mensaje "Taking too long? Close loading screen." en inglés.

**Fortalezas:** sitemap nativo, URLs limpias, HTTPS, contenido técnico real y detallado por producto, fichas PDF descargables, certificaciones y documentos legales publicados.

## 8. Recomendaciones para la reconstrucción / mejora

1. Reescribir el home con H1 claro ("Fabricación de semirremolques en Chile…") y CTA de cotización.
2. Añadir meta descriptions, OG, JSON-LD (`Organization`, `Product`) y alt descriptivos.
3. Reemplazar Lorem Ipsum, corregir ortografía y actualizar a ISO 9001:2015 si corresponde.
4. Unificar contactos: números/correos distintos por área, dirección en texto, correo visible.
5. Optimizar imágenes (WebP, tamaños responsive) y comprimir PDFs.
6. Despublicar `/pruebas/` y `/sitio-en-mantencion/`; llenar o eliminar el blog.
7. Añadir analytics (GA4) y eventos de clic en WhatsApp/formulario.
8. Páginas por equipo con galería real (`sider01/02`, `srbt1/2`, `srf1/2` ya existen) y fichas dentro de la página, no solo PDF.

## 9. Inventario de assets

- `assets/logo/` — logo y favicons.
- `assets/images/` — **35 imágenes originales** (tamaño completo, sin miniaturas). Detalle en `assets/images_manifest.csv`.
- `assets/pdfs/` — 13 PDFs (6 fichas técnicas, 6 normativas, certificado ISO).
- `html/` — HTML original de 14 páginas + `robots.txt` y `sitemap.xml`.
- `image_urls_orig.txt` / `image_urls_all.txt` — URLs de origen de las imágenes (originales / incluidas variantes redimensionadas).

### Mapa de imágenes por uso
| Archivo | Uso |
|---|---|
| Logo.png | Logo del header y footer |
| cropped-favicon.png | Favicon / icono de app |
| forestal.gif | Pantalla de carga |
| equiposportada.png / EQUIPOS-PORTADAS-CEL.png | Banner "% más livianos" (desktop / móvil) |
| minero, speed-sider-portada, Plano, Forestal, Semi-Remolque-Carga-Seca, semirremolque-Botellero (.jpg) | Portadas de cada equipo |
| sider01/02, srbt1/2, srf1/2 (.jpg) | Galerías de fichas de producto |
| daf2, faw2, hino2, scania2, international2 (.png) | Logos de clientes |
| iso, leyes, m3 (.png) · iso_widget.png | Íconos de pilares / sello ISO del footer |
| imagen.jpg | Cabecera "Sobre Santander" |
| Contact-us.png | Ilustración de Contacto |
| fondo-blog.jpg / fondocel.jpg | Fondos (blog / móvil) |
| webinar-4/7.png | Banners en Artículos |
| CamScanner-…(3).jpg | Fotos de premios |
