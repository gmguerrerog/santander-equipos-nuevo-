# Brief para Claude Code — Santander Equipos

Contexto: este paquete contiene el análisis y los assets del sitio https://santanderequipos.cl/ (WordPress + Divi), para rediseñarlo o reconstruirlo.

## Cómo usar este paquete
1. Lee primero `ANALISIS.md` (estructura, contenidos, SEO, marca, tecnología, mapa de imágenes).
2. Usa `assets/logo/` y `assets/images/` como biblioteca de imágenes (originales a tamaño completo). Detalle de dimensiones en `assets/images_manifest.csv`.
3. Las fichas técnicas y normativas están en `assets/pdfs/` (se pueden enlazar tal cual; Speed Sider pesa 19 MB, conviene comprimirlo).
4. El HTML original de cada página está en `html/` para extraer textos exactos.

## Tarea sugerida
Construir un sitio nuevo (estático Astro/Next o landing multipágina) con las mismas secciones: Inicio, Sobre Santander, Equipos (6 semirremolques con ficha técnica), Certificaciones/Leyes, Premios, Artículos, Contacto.

Mejoras obligatorias respecto al original: H1 por página, meta description + Open Graph, JSON-LD (`Organization`, `Product`), alt en todas las imágenes, imágenes en WebP responsive, sin Lorem Ipsum, ortografía corregida, botón WhatsApp +56 9 9558 6223, mapa de ubicación, redes (Instagram @santander_equipos, Facebook, X @santander_equip, LinkedIn).

Datos de marca: nombre "Santander Equipos", lema "Ingeniería en Movimiento", fundada 2009, ISO 9001. Colores observados: `#2f5599`, `#2ea3f2`, `#0a0a0a`, `#ffffff`. Tipografías: Open Sans / Sarabun. Confirmar la paleta final con el logo.

## Pendientes a confirmar con el cliente
- Dirección postal y correo de contacto (el sitio no los publica).
- Números de WhatsApp separados para Ventas / Proveedores / Contabilidad (hoy es uno solo).
- Vigencia de la certificación ISO (el sitio cita 9001-2008).
- Contenido real del bloque "Volumen" y de los artículos/noticias.
- Derecho de uso de las fotos de producto y de los logos de clientes (DAF, FAW, Hino, Scania, International).
