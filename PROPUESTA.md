# Propuesta de rediseño — santanderequipos.cl

**Para:** Santander Equipos · Sociedad Comercial Santander Ltda.
**Qué es:** un sitio web nuevo, moderno y listo para publicar, construido con los textos, fotos y fichas técnicas reales de la empresa. Está en la carpeta `docs/` de este repositorio.

## El problema con el sitio actual

| Sitio actual | Por qué le cuesta clientes |
|---|---|
| Texto de relleno "Lorem Ipsum" en la portada | Da imagen de sitio abandonado o sin terminar |
| Sección de artículos con "No Results Found" | Un comprador ve una página rota |
| Los premios de SSAB están escondidos como escaneos sin explicación | El mayor diferenciador de la empresa no se ve |
| Sin títulos ni descripciones para Google, sin datos estructurados | Aparece poco en búsquedas como "semirremolques Chile" |
| Ficha técnica Speed Sider de 19 MB | Tarda o no descarga en el celular |
| Tres botones de WhatsApp al mismo número, formulario genérico | El cliente no sabe qué pasa con su consulta |
| Mensaje en inglés en la pantalla de carga, faltas de ortografía | Resta profesionalismo |
| Páginas de prueba publicadas (`/pruebas/`, `/sitio-en-mantencion/`) | Google las indexa |

## Lo que trae el sitio nuevo

**Para vender más**
- Portada con mensaje claro: *semirremolques de acero sueco, hechos en Chile para cargar más y durar más*, y botones de cotización visibles en todo momento.
- **Premio Swedish Steel Prize 2014 (2.º lugar, SSAB) y sello My Inner Strenx** como sección destacada: pocos fabricantes chilenos pueden mostrar esto.
- **Simulador de carga útil**: el cliente mueve unos controles y ve cuántas toneladas e ingresos extra le daría un equipo más liviano. Convierte el "somos más livianos" en dinero.
- **Anatomía interactiva** de un semirremolque: se toca cada componente (perno rey JOST, ejes de 13.000 kg, Suspensys, Bendix/EBS, LED, cortinas de PVC de 900 g/m²).
- **Formulario de cotización que llega directo a WhatsApp**, ya ordenado (tipo de equipo, modelo, cantidad, datos del cliente). No requiere servidor ni costo mensual.
- Barra fija en el celular con Llamar / WhatsApp / Cotizar.

**Catálogo**
- Las 6 líneas con filtro por tipo de carga, **comparador** en tabla y una página por equipo con galería, especificaciones en pestañas, video y ficha PDF.
- Fichas PDF comprimidas sin perder calidad: **Speed Sider de 19 MB a 1,9 MB** y las demás de 4 a 6 MB a entre 1 y 2 MB.

**Confianza y contenido**
- Página *Nosotros* con historia, línea de tiempo, servicios (fabricación, carrocerías, reparación) y homologación con marcas de camiones.
- Página *Calidad y premios* con ISO 9001, los certificados en grande y la normativa chilena para descargar.
- Preguntas frecuentes.

**Técnico**
- Cada página tiene su título, descripción para Google, imagen para compartir en redes y datos estructurados (empresa, productos, preguntas frecuentes, ruta de navegación). También incluye `sitemap.xml` y `robots.txt`.
- Imágenes en WebP, sitio ligero, sin WordPress ni plugins que mantener ni pagar.
- Se adapta al celular y es accesible: navegable con teclado, textos alternativos y respeta la opción de reducir animaciones.

## Antes de publicar, confirmar con el cliente
1. Dirección escrita y correo de contacto (hoy no se publican).
2. ¿Hay números distintos para Ventas, Proveedores y Contabilidad? Hoy los tres apuntan al +56 9 9558 6223.
3. Vigencia de la certificación ISO (el sitio actual dice 9001-2008; la versión vigente de la norma es la 9001:2015). El sitio nuevo dice solo "ISO 9001".
4. En el sitio actual las fichas de Minero, Plano y Speed Sider son casi idénticas y Plano enlaza el PDF "Sider": revisar los datos de cada equipo. En Plano se quitó el ítem "Cortinas".
5. Los valores por defecto del simulador (800 kg menos de tara, $25.000 por tonelada) son un ejemplo: conviene reemplazarlos por datos reales.
6. Permiso para usar los logos de marcas de camiones (Scania, DAF, Hino, FAW, International).
7. URL de la página de LinkedIn de la empresa (hoy es un perfil personal).

## Cómo verlo y publicarlo
- **Verlo en el computador:** abrir `docs/index.html` en el navegador.
- **Vista previa en línea gratis:** en GitHub ir a *Settings → Pages*, elegir la rama `main` y la carpeta `/docs`.
- **Publicarlo en santanderequipos.cl:** subir el contenido de `docs/` a cualquier hosting (o usar GitHub Pages con el dominio propio).
- **Editar contenidos:** los textos y datos están en `build/build.py`. Después de un cambio se ejecuta `python3 build/build.py`.
