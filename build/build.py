"""Genera el sitio estático de Santander Equipos en docs/.

Uso:  python3 build/build.py
Lee las fichas técnicas desde html/project_*.html (sitio original) y escribe
todas las páginas en docs/. Los estilos y scripts viven en docs/assets/.
"""
import html as H
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs"
SITE = "https://santanderequipos.cl"
PHONE = "+56 9 9558 6223"
PHONE_RAW = "56995586223"
WA = f"https://wa.me/{PHONE_RAW}"
MAP_EMBED = ("https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d1667.182884956782!2d-70.70505987418422"
             "!3d-33.309251785807476!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x276d39b80489b6fe!2sSantander"
             "%20Equipos!5e0!3m2!1ses!2scl!4v1675971369099!5m2!1ses!2scl")
MAP_LINK = "https://www.google.com/maps/search/?api=1&query=Santander+Equipos&query_place_id=0x0:0x276d39b80489b6fe"
SOCIAL = {
    "instagram": ("Instagram", "https://www.instagram.com/santander_equipos/"),
    "facebook": ("Facebook", "https://www.facebook.com/profile.php?id=100088722630884"),
    "x": ("X", "https://x.com/santander_equip"),
    "linkedin": ("LinkedIn", "https://www.linkedin.com/search/results/all/?keywords=Log%C3%ADstica%20Santander"),
}
YEAR = date.today().year
VERSION = "1"

# --------------------------------------------------------------------------- iconos
ICONS = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "close": '<path d="M6 6l12 12M18 6L6 18"/>',
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4a2 2 0 01-2 2A16 16 0 013 6a2 2 0 012-2"/>',
    "pin": '<path d="M12 21s-7-6.2-7-12a7 7 0 0114 0c0 5.8-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/>',
    "download": '<path d="M12 4v11M7 10l5 5 5-5M5 20h14"/>',
    "file": '<path d="M14 3H7a2 2 0 00-2 2v14a2 2 0 002 2h10a2 2 0 002-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>',
    "play": '<path d="M8 5.5v13l11-6.5z" fill="currentColor" stroke="none"/>',
    "weight": '<path d="M6 8h12l2 12H4z"/><circle cx="12" cy="5" r="2.2"/><path d="M9.5 14h5"/>',
    "shield": '<path d="M12 3l8 3v6c0 4.5-3.4 8.3-8 9-4.6-.7-8-4.5-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    "award": '<circle cx="12" cy="9" r="6"/><path d="M8.5 14L7 21l5-3 5 3-1.5-7"/>',
    "steel": '<path d="M3 17l9 4 9-4M3 12l9 4 9-4M3 7l9 4 9-4-9-4z"/>',
    "brake": '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="3"/><path d="M12 3.5v3M12 17.5v3M3.5 12h3M17.5 12h3"/>',
    "law": '<path d="M12 3v18M5 7h14M7 7l-3 7a3 3 0 006 0zM17 7l-3 7a3 3 0 006 0zM8 21h8"/>',
    "paint": '<path d="M4 4h13v5H4z"/><path d="M17 6.5h3V12h-8v3"/><rect x="10" y="15" width="4" height="6" rx="1"/>',
    "gear": '<circle cx="12" cy="12" r="3"/><path d="M12 2.5v3M12 18.5v3M21.5 12h-3M5.5 12h-3M18.7 5.3l-2.1 2.1M7.4 16.6l-2.1 2.1M18.7 18.7l-2.1-2.1M7.4 7.4L5.3 5.3"/>',
    "ruler": '<path d="M3 17L17 3l4 4L7 21z"/><path d="M7 13l2 2M10 10l2 2M13 7l2 2"/>',
    "truck": '<path d="M2 6h12v10H2zM14 10h4l3 3v3h-7z"/><circle cx="6" cy="17.5" r="2"/><circle cx="17" cy="17.5" r="2"/>',
    "wrench": '<path d="M14.5 6.5a4 4 0 00-5.4 5.1L3.5 17.2a1.8 1.8 0 002.5 2.5l5.6-5.6a4 4 0 005.1-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/>',
    "body": '<path d="M2 15V6h13v9M15 9h4l3 4v2h-7M2 15h20"/><circle cx="6" cy="17.5" r="1.8"/><circle cx="18" cy="17.5" r="1.8"/>',
    "bolt": '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "chat": '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 10h8M8 13h5"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0113 0M16 4.5a3.5 3.5 0 010 7M18 14a6 6 0 013.5 6"/>',
    "box": '<path d="M3 7.5L12 3l9 4.5v9L12 21l-9-4.5z"/><path d="M3 7.5l9 4.5 9-4.5M12 12v9"/>',
    "tree": '<path d="M12 3l6 8h-3l4 6H5l4-6H6z"/><path d="M12 17v4"/>',
    "mountain": '<path d="M2 20l7-12 4 6 3-4 6 10z"/>',
    "calc": '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8M8 12h2M12 12h0M16 12h0M8 16h2M12 16h0M16 16h0"/>',
}
BRAND_ICONS = {
    "whatsapp": '<path fill="currentColor" d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 004.74 1.21c5.46 0 9.91-4.45 9.91-9.91C21.95 6.45 17.5 2 12.04 2zm5.8 14.03c-.25.69-1.44 1.32-1.98 1.37-.51.05-1.15.07-1.86-.12-.43-.13-.98-.32-1.69-.62-2.97-1.28-4.9-4.27-5.05-4.47-.15-.2-1.2-1.6-1.2-3.05s.76-2.16 1.03-2.46c.27-.3.59-.37.79-.37h.57c.18 0 .43-.07.67.51.25.59.84 2.04.91 2.19.07.15.12.32.02.52-.1.2-.15.32-.3.49-.15.17-.31.39-.45.52-.15.15-.3.31-.13.61.17.3.77 1.27 1.65 2.06 1.13 1.01 2.09 1.32 2.39 1.47.3.15.47.12.64-.07.17-.2.74-.86.94-1.16.2-.3.39-.25.67-.15.27.1 1.73.82 2.03.97.3.15.49.22.57.35.07.12.07.71-.18 1.4z"/>',
    "instagram": '<rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="17.5" cy="6.5" r="1.2" fill="currentColor"/>',
    "facebook": '<path fill="currentColor" d="M13.5 21v-7.5h2.6l.4-3h-3V8.6c0-.9.3-1.5 1.5-1.5h1.6V4.4c-.3 0-1.2-.1-2.3-.1-2.3 0-3.9 1.4-3.9 4v2.2H7.8v3h2.6V21z"/>',
    "x": '<path fill="currentColor" d="M17.8 3h3.1l-6.8 7.8 8 10.2h-6.3l-4.9-6.4L5.3 21H2.2l7.3-8.3L1.8 3h6.4l4.4 5.9zm-1.1 16.2h1.7L7.4 4.7H5.6z"/>',
    "linkedin": '<path fill="currentColor" d="M4.98 3.5a2.5 2.5 0 110 5 2.5 2.5 0 010-5zM3 9.5h4V21H3zM9.5 9.5h3.8v1.6h.1c.5-1 1.8-2 3.8-2 4 0 4.8 2.6 4.8 6V21h-4v-5.1c0-1.2 0-2.8-1.7-2.8s-2 1.3-2 2.7V21h-4z"/>',
}


def icon(name, cls="ico"):
    if name in BRAND_ICONS:
        return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{BRAND_ICONS[name]}</svg>'
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


def esc(s):
    return H.escape(s, quote=True)


def wa_link(text):
    from urllib.parse import quote
    return f"{WA}?text={quote(text)}"


# --------------------------------------------------------------------------- fichas técnicas
LABELS = [
    "Aplicación", "Tipo de Acero", "Dimensiones", "Estructura de la Plataforma", "Piso", "Teleras", "Viga Central",
    "Vigas rectas o rebajadas", "Faja Lateral", "Faldon Trasero", "Estructura Panel Frontal",
    "Estructura Panel Trasero", "Estructura lateral", "Puertas Traseras", "Cubiertas", "Techo", "Doble Piso",
    "Pilares intermedios", "Izaje", "Estacas", "Suspensión y Rodados", "Cortinas", "Sistema Eléctrico",
    "Sistema de Frenos Normales", "Sistema EBS", "Perno Rey", "Porta Repuesto", "Gatas de Apoyo",
    "Estanque de Aire", "Pintura y tratamiento anticorrosivo", "Accesorios.",
]
LABEL_FIX = {"Faldon Trasero": "Faldón trasero", "Faja Lateral": "Faja lateral", "Accesorios.": "Accesorios", "Tipo de Acero": "Tipo de acero",
             "Estructura de la Plataforma": "Estructura de la plataforma", "Viga Central": "Viga central",
             "Estructura Panel Frontal": "Panel frontal", "Estructura Panel Trasero": "Panel trasero",
             "Estructura lateral": "Paneles laterales", "Puertas Traseras": "Puertas traseras",
             "Doble Piso": "Doble piso", "Suspensión y Rodados": "Suspensión y rodados",
             "Sistema Eléctrico": "Sistema eléctrico", "Sistema de Frenos Normales": "Frenos convencionales",
             "Sistema EBS": "Frenos EBS (opcional)", "Perno Rey": "Perno rey", "Porta Repuesto": "Porta repuesto",
             "Gatas de Apoyo": "Gatas de apoyo", "Estanque de Aire": "Estanque de aire",
             "Pintura y tratamiento anticorrosivo": "Pintura y anticorrosivo", "Vigas rectas o rebajadas":
             "Vigas (rectas o rebajadas)", "Pilares intermedios": "Pilares intermedios"}
TEXT_FIX = [
    (r"Provceso", "Proceso"), (r"traserasdobles", "traseras dobles"), (r"traseras\s+dobles", "traseras dobles"),
    (r"\belectrico\b", "eléctrico"), (r"\bvias\b", "vías"), (r"\bplastica\b", "plástica"),
    (r"\bplasticas\b", "plásticas"), (r"SSAB\s*O\s*THYSSENGROUP|SSAB OTHYSSENGROUP", "SSAB o Thyssen Group"),
    (r"THYSSENGROUP", "Thyssen Group"), (r"Estructura de fija", "Estructura fija"), (r"Sueca", "sueca"),
    (r"espesor\.Alma", "espesor. Alma"), (r"ancho\.Suspensiones", "ancho. Suspensiones"), (r"8 \"", "8\""),
    (r"Mecánica o Neumática", "mecánicas o neumáticas"), (r"Mecánicas o Neumáticas", "mecánicas o neumáticas"),
    (r"Super estructura", "Superestructura"), (r"\s+,", ","), (r"\s+\.", "."), (r"Pintura poliuretano",
    "pintura poliuretano"), (r"Proceso Electrostático", "proceso electrostático"),
    (r"Proceso electrostático", "proceso electrostático"), (r"Sistema led", "Sistema LED"),
    (r"gr m2|gr/m2|grs / m2", "g/m²"), (r"12.400 a 15.800", "12.400 a 15.800"), (r"\bmm\.\s*(?=[A-Z])", "mm. "),
    (r"STRENX 700", "Strenx 700"), (r"(\d) Kg\b", r"\1 kg"), (r"\. Galvanizada", ". galvanizada"),
    (r"Según Normativa", "Según normativa"), (r"Perfil Canal", "Perfil canal"), (r"Carga en Pallets", "Carga en pallets"),
    (r"Sistema LED multivoltaje", "sistema LED multivoltaje"),
    (r"22\.5 x 8\. 25", "22,5\" x 8,25\""), (r"22\.5”? x 8\.25\"?”?", "22,5\" x 8,25\""),
]


def clean(t):
    t = re.sub(r"\s+", " ", t).strip()
    for a, b in TEXT_FIX:
        t = re.sub(a, b, t)
    return t


def page_text(path):
    s = path.read_text(encoding="utf-8", errors="ignore")
    s = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"(?i)<br\s*/?>|</p>|</li>|</h\d>|</div>", "\n", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = H.unescape(s)
    lines = [re.sub(r"\s+", " ", l).strip() for l in s.split("\n")]
    out = []
    for l in lines:
        if l and (not out or out[-1] != l):
            out.append(l)
    t = "\n".join(out)
    a = t.find("Descripción Técnica\nAplicación")
    b = t.find("Descargar Ficha", a)
    return t[a + len("Descripción Técnica\n"):b].strip().split("\n")


def parse_specs(slug):
    lines = page_text(ROOT / "html" / f"project_{slug}.html")
    lab_low = {l.lower(): l for l in LABELS}
    specs, cur = [], None
    for ln in lines:
        key = lab_low.get(ln.strip().lower())
        if key:
            cur = [key, []]
            specs.append(cur)
        elif cur:
            cur[1].append(ln)
    data = {}
    for key, vals in specs:
        if key == "Dimensiones":
            d = {}
            for i in range(0, len(vals) - 1, 2):
                d[vals[i]] = clean(vals[i + 1])
            data[key] = d
        elif key == "Pintura y tratamiento anticorrosivo":
            data[key] = [(vals[i], clean(vals[i + 1])) for i in range(0, len(vals) - 1, 2)]
        elif key == "Accesorios.":
            data[key] = [clean(v.lstrip("- ").rstrip(".")) for v in vals if v.strip()]
        elif key == "Sistema Eléctrico":
            text = clean(" ".join(v for v in vals if not v.startswith("-")))
            bullets = [clean(v.lstrip("- ").rstrip(".")) for v in vals if v.startswith("-")]
            data[key] = (text, bullets)
        else:
            data[key] = clean(" ".join(vals))
    if "Alto" in data.get("Dimensiones", {}):
        data["Dimensiones"]["Alto"] = data["Dimensiones"]["Alto"].replace("4.700 a 3.000", "3.000 a 4.700")
    return data


SPEC_GROUPS = [
    ("Estructura", "steel", ["Tipo de Acero", "Estructura de la Plataforma", "Viga Central", "Vigas rectas o rebajadas",
                             "Piso", "Teleras", "Faja Lateral", "Faldon Trasero", "Estructura Panel Frontal",
                             "Estructura Panel Trasero", "Estructura lateral", "Puertas Traseras", "Cubiertas",
                             "Techo", "Doble Piso", "Pilares intermedios", "Izaje", "Estacas", "Cortinas"]),
    ("Rodado y frenos", "brake", ["Suspensión y Rodados", "Sistema de Frenos Normales", "Sistema EBS", "Perno Rey",
                                  "Gatas de Apoyo", "Estanque de Aire", "Porta Repuesto"]),
    ("Sistema eléctrico", "bolt", ["Sistema Eléctrico"]),
    ("Pintura y accesorios", "paint", ["Pintura y tratamiento anticorrosivo", "Accesorios."]),
]

PRODUCTS = [
    dict(slug="speed-sider", name="Speed Sider", short="Sider de carga lateral rápida",
         tags=["general"], app="Carga general",
         lead="Cortinas laterales de PVC de 900 g/m² que abren todo el costado del equipo: carga y descarga con grúa horquilla en minutos, sin perder protección para tu carga.",
         highlights=["Cortinas PVC 900 g/m² sellado por alta frecuencia", "Pilares intermedios desmontables", "Ejes europeos de 13.000 kg"],
         photos=["sider01", "sider02"], pdf="Semiremolque-Speed-Sider.pdf", videos=[]),
    dict(slug="botellero", name="Botellero", short="Doble piso para carga paletizada",
         tags=["pallets"], app="Carga en pallets",
         lead="Equipo de doble piso pensado para la distribución de bebidas y carga paletizada: piso de aluminio diamantado, techo aerodinámico y estructura fija en acero Strenx® 700.",
         highlights=["Doble piso fijo en Strenx® 700", "Piso de aluminio diamantado 3 mm", "Techo aerodinámico con rieles de aluminio"],
         photos=["srbt1", "srbt2"], pdf="Semiremolque-Botellero.pdf", videos=["9ALYfot6nqA", "BcWajCSjfSg"]),
    dict(slug="forestal", name="Forestal", short="Transporte de madera en trozos",
         tags=["forestal"], app="Carga de madera en trozos",
         lead="Construido para la exigencia del rubro forestal: estacas de alta resistencia modelo ULTRAXX y cabezal de izaje reforzado, todo sobre una superestructura de acero Strenx® 700.",
         highlights=["Estacas modelo ULTRAXX", "Cabezal de izaje reforzado", "Largo de 10.500 a 13.500 mm"],
         photos=["srf1", "srf2"], pdf="Semiremolque-Forestal.pdf", videos=[]),
    dict(slug="minero", name="Minero", short="Robusto para faenas exigentes",
         tags=["mineria", "general"], app="Carga en general y faenas mineras",
         lead="Un equipo robusto para operar en faenas y rutas de alta exigencia, con superestructura en acero sueco de alta resistencia y configuración de pilares desmontables.",
         highlights=["Vigas rectas o rebajadas", "Piso de acero diamantado 3 o 5 mm", "Opción de frenos EBS antivuelco"],
         photos=[], pdf="Semiremolque-Minero.pdf", videos=[]),
    dict(slug="carga-seca", name="Carga Seca", short="Furgón cerrado de aluminio",
         tags=["general"], app="Carga general protegida",
         lead="Furgón cerrado con paneles estructurados en aluminio: tu carga viaja protegida del clima y del polvo, con puertas traseras tipo container o Roll-Up.",
         highlights=["Paneles de aluminio estructurado", "Puertas tipo container o Roll-Up", "Piso de acero soldado longitudinal"],
         photos=[], pdf="Semiremolque-Carga-Seca.pdf", videos=[]),
    dict(slug="plano", name="Plano", short="Plataforma para carga general",
         tags=["general"], app="Carga en general",
         lead="Plataforma plana versátil para maquinaria, estructuras y carga general, con piso de acero diamantado y faja lateral en perfil Strenx® 700.",
         highlights=["Piso de acero diamantado", "Teleras alas delta estampadas", "Largo de 12.400 a 15.800 mm"],
         photos=[], pdf="Semiremolque-Sider.pdf", videos=[]),
]
FILTERS = [("all", "Todos"), ("general", "Carga general"), ("pallets", "Pallets y bebidas"),
           ("forestal", "Forestal"), ("mineria", "Minería")]

for p in PRODUCTS:
    p["specs"] = parse_specs(p["slug"])
    if p["slug"] == "plano":  # en el original la ficha de Plano es copia de la de Sider
        for k in ("Cortinas",):
            p["specs"].pop(k, None)

# --------------------------------------------------------------------------- layout
NAV = [("index.html", "Inicio"), ("equipos.html", "Equipos"), ("nosotros.html", "Nosotros"),
       ("calidad.html", "Calidad y premios"), ("contacto.html", "Contacto")]


def org_jsonld():
    return {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": SITE + "/#empresa",
        "name": "Santander Equipos",
        "legalName": "Sociedad Comercial Santander Ltda.",
        "slogan": "Ingeniería en Movimiento",
        "description": "Fabricación y reparación de semirremolques y equipamiento para el transporte terrestre en Chile. Acero Strenx® 700 y certificación ISO 9001.",
        "url": SITE + "/",
        "logo": SITE + "/assets/img/logo.png",
        "image": SITE + "/assets/img/sider01.webp",
        "telephone": PHONE,
        "foundingDate": "2009",
        "award": ["Swedish Steel Prize 2014 – Segundo lugar (SSAB)", "My Inner Strenx (SSAB)"],
        "address": {"@type": "PostalAddress", "addressRegion": "Región Metropolitana", "addressCountry": "CL"},
        "geo": {"@type": "GeoCoordinates", "latitude": -33.3093, "longitude": -70.7051},
        "areaServed": "CL",
        "sameAs": [v[1] for k, v in SOCIAL.items() if k != "linkedin"],
    }


def header(active):
    links = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == active else ""
        if href == "equipos.html":
            sub = "".join(
                f'<a href="equipo-{p["slug"]}.html"><img src="assets/img/{p["slug"]}.webp" alt="" width="70" height="30" loading="lazy">'
                f'<span><b>{p["name"]}</b><small>{p["short"]}</small></span></a>' for p in PRODUCTS)
            links.append(
                f'<li class="has-sub"><a href="{href}"{cur}>{label}</a>'
                f'<button class="sub-toggle" aria-label="Ver equipos" aria-expanded="false">{icon("chev")}</button>'
                f'<div class="sub"><div class="sub-grid">{sub}</div>'
                f'<a class="sub-all" href="equipos.html">Comparar todos los equipos {icon("arrow")}</a></div></li>')
        else:
            links.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    return f'''
<a class="skip" href="#contenido">Saltar al contenido</a>
<div class="topbar"><div class="wrap">
  <span>{icon("award")} Swedish Steel Prize 2014 · Certificación ISO 9001 · Fabricamos en Chile desde 2009</span>
  <a href="tel:+{PHONE_RAW}">{icon("phone")} {PHONE}</a>
</div></div>
<header class="site-header" id="top">
  <div class="wrap nav-row">
    <a class="brand" href="index.html" aria-label="Santander Equipos, inicio"><img src="assets/img/logo.png" alt="Santander Equipos" width="190" height="47"></a>
    <nav class="main-nav" id="menu" aria-label="Principal"><ul>{"".join(links)}</ul>
      <div class="nav-mobile-cta"><a class="btn btn-primary" href="contacto.html#cotizar">Cotizar equipo</a>
      <a class="btn btn-wa" href="{WA}" target="_blank" rel="noopener">{icon("whatsapp")} WhatsApp</a></div>
    </nav>
    <div class="nav-actions">
      <a class="btn btn-ghost hide-sm" href="{WA}" target="_blank" rel="noopener">{icon("whatsapp")} WhatsApp</a>
      <a class="btn btn-primary hide-sm" href="contacto.html#cotizar">Cotizar {icon("arrow")}</a>
      <button class="menu-btn" aria-controls="menu" aria-expanded="false" aria-label="Abrir menú">{icon("menu")}{icon("close")}</button>
    </div>
  </div>
</header>'''


def footer():
    eq = "".join(f'<li><a href="equipo-{p["slug"]}.html">Semirremolque {p["name"]}</a></li>' for p in PRODUCTS)
    soc = "".join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="{n}">{icon(k)}</a>'
                  for k, (n, u) in SOCIAL.items())
    return f'''
<section class="cta-band"><div class="wrap cta-inner reveal">
  <div><p class="eyebrow light">¿Listo para renovar tu flota?</p>
  <h2>Cuéntanos qué transportas y te proponemos el equipo ideal.</h2></div>
  <div class="cta-actions"><a class="btn btn-light btn-lg" href="contacto.html#cotizar">Solicitar cotización {icon("arrow")}</a>
  <a class="btn btn-wa btn-lg" href="{wa_link("Hola, quiero cotizar un semirremolque Santander.")}" target="_blank" rel="noopener">{icon("whatsapp")} Hablar por WhatsApp</a></div>
</div></section>
<footer class="site-footer">
  <div class="wrap foot-grid">
    <div class="foot-brand">
      <img src="assets/img/logo-blanco.png" alt="Santander Equipos" width="210" height="52">
      <p>Ingeniería en Movimiento. Fabricamos y reparamos semirremolques y equipamiento para el transporte terrestre en Chile desde 2009.</p>
      <div class="social">{soc}</div>
    </div>
    <div><h3>Equipos</h3><ul>{eq}</ul></div>
    <div><h3>Empresa</h3><ul>
      <li><a href="nosotros.html">Nosotros</a></li><li><a href="nosotros.html#servicios">Servicios</a></li>
      <li><a href="calidad.html">Certificación ISO 9001</a></li><li><a href="calidad.html#premios">Premios</a></li>
      <li><a href="calidad.html#normativa">Normativa de transporte</a></li><li><a href="contacto.html">Contacto</a></li></ul></div>
    <div><h3>Contacto</h3><ul class="foot-contact">
      <li><a href="tel:+{PHONE_RAW}">{icon("phone")} {PHONE}</a></li>
      <li><a href="{WA}" target="_blank" rel="noopener">{icon("whatsapp")} WhatsApp ventas</a></li>
      <li><a href="{MAP_LINK}" target="_blank" rel="noopener">{icon("pin")} Región Metropolitana, Chile</a></li></ul>
      <div class="foot-badges"><span>ISO 9001</span><span>Strenx® 700</span><span>Bureau Veritas</span></div>
    </div>
  </div>
  <div class="wrap foot-bottom"><span>© {YEAR} Santander Equipos · Sociedad Comercial Santander Ltda.</span>
  <a href="#top">Volver arriba ↑</a></div>
</footer>
<a class="wa-float" href="{wa_link("Hola, necesito información sobre sus equipos.")}" target="_blank" rel="noopener" aria-label="Escríbenos por WhatsApp">{icon("whatsapp")}<span>¿Hablamos?</span></a>
<nav class="mobile-bar" aria-label="Acciones rápidas">
  <a href="tel:+{PHONE_RAW}">{icon("phone")}<span>Llamar</span></a>
  <a href="{WA}" target="_blank" rel="noopener">{icon("whatsapp")}<span>WhatsApp</span></a>
  <a href="contacto.html#cotizar" class="hl">{icon("file")}<span>Cotizar</span></a>
</nav>
<div class="lightbox" hidden><button class="lb-close" aria-label="Cerrar">{icon("close")}</button><img alt=""><p></p></div>'''


def page(path, title, desc, body, active="", jsonld=None, og_image="assets/img/sider01.webp"):
    url = SITE + "/" + ("" if path == "index.html" else path)
    lds = [org_jsonld()] + (jsonld or [])
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)
    doc = f'''<!doctype html>
<html lang="es-CL" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0052a6">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_CL">
<meta property="og:site_name" content="Santander Equipos">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@santander_equip">
<link rel="icon" href="assets/img/favicon-32x32.png" sizes="32x32">
<link rel="icon" href="assets/img/favicon-192x192.png" sizes="192x192">
<link rel="apple-touch-icon" href="assets/img/favicon-180x180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/styles.css?v={VERSION}">
{ld}
</head>
<body>
{header(active)}
<main id="contenido">
{body}
</main>
{footer()}
<script src="assets/js/main.js?v={VERSION}" defer></script>
</body>
</html>
'''
    (OUT / path).write_text(doc, encoding="utf-8")


# --------------------------------------------------------------------------- bloques reutilizables
def product_card(p, i=0):
    d = p["specs"].get("Dimensiones", {})
    return f'''
<article class="p-card reveal" data-tags="{" ".join(p["tags"])}" style="--d:{i * 60}ms">
  <a class="p-media" href="equipo-{p["slug"]}.html" tabindex="-1">
    <img src="assets/img/{p["slug"]}.webp" alt="Semirremolque {p["name"]} Santander Equipos" width="700" height="300" loading="lazy">
    <span class="p-tag">{esc(p["app"])}</span>
  </a>
  <div class="p-body">
    <h3><a href="equipo-{p["slug"]}.html">{p["name"]}</a></h3>
    <p>{esc(p["short"])}</p>
    <dl class="p-dims"><div><dt>Largo</dt><dd>{esc(d.get("Largo", "—"))}</dd></div>
    <div><dt>Alto</dt><dd>{esc(d.get("Alto", "—"))}</dd></div></dl>
    <ul class="p-hl">{"".join(f"<li>{icon('check')}{esc(h)}</li>" for h in p["highlights"][:2])}</ul>
    <div class="p-actions"><a class="btn btn-primary btn-sm" href="equipo-{p["slug"]}.html">Ver ficha {icon("arrow")}</a>
    <a class="btn btn-ghost btn-sm" href="{wa_link(f'Hola, quiero cotizar el semirremolque {p["name"]}.')}" target="_blank" rel="noopener">Cotizar</a></div>
  </div>
</article>'''


def catalog(heading=True):
    chips = "".join(f'<button class="chip{" is-on" if k == "all" else ""}" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{v}</button>'
                    for k, v in FILTERS)
    head = f'''<div class="sec-head reveal"><p class="eyebrow">Nuestros equipos</p>
<h2>Seis líneas de semirremolques, <span class="hl-text">una misma obsesión por la calidad</span></h2>
<p>Cada equipo se fabrica con acero sueco Strenx® 700, ejes europeos y componentes de marcas líderes. Elige por tipo de carga:</p></div>''' if heading else ""
    return f'''{head}
<div class="chips reveal" role="group" aria-label="Filtrar por tipo de carga">{chips}</div>
<div class="p-grid">{"".join(product_card(p, i) for i, p in enumerate(PRODUCTS))}</div>'''


def video_embed(vid, title):
    return (f'<button class="yt" data-id="{vid}" aria-label="Reproducir video: {esc(title)}">'
            f'<img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="" loading="lazy" width="480" height="360">'
            f'<span class="yt-play">{icon("play")}</span><span class="yt-title">{esc(title)}</span></button>')


ANATOMY = [
    (16, 77, "Perno rey JOST 2\"", "Perno rey marca JOST de 2\" con sistema apernado: acople seguro y reemplazable."),
    (30, 87, "Gatas de apoyo 25 t", "Gatas JOST o similar con capacidad estática de levante de 25 toneladas y doble velocidad."),
    (50, 40, "Cortinas PVC 900 g/m²", "Tela PVC sellada por alta frecuencia, catracas tensoras sin fin y tubos laterales de aluminio."),
    (44, 73, "Vigas en acero Strenx® 700", "Superestructura en acero de alta resistencia de procedencia sueca (SSAB): más rigidez con menos peso."),
    (54, 82, "Estanque de aire 120 L", "Depósitos de aire de 120 litros y líneas blindadas de alta presión de 8 y 10 mm."),
    (75, 86, "Ejes europeos 13.000 kg", "Ejes de disco europeo y suspensión mecánica o neumática Suspensys de 13.000 kg por puente."),
    (86, 70, "Frenos Bendix / EBS", "Válvulas Bendix y opción EBS con control de estabilidad antivuelco y frenado según carga."),
    (95, 62, "Iluminación LED", "Focos laterales, traseros y de patente LED multivoltaje, arnés sellado de 7 vías con sistema CLIP."),
]


def anatomy_svg():
    straps = "".join(f'<line x1="{x}" y1="62" x2="{x}" y2="238"/>' for x in range(150, 940, 46))
    wheels = "".join(f'<g class="wheel"><circle cx="{x}" cy="300" r="36"/><circle cx="{x}" cy="300" r="15"/></g>'
                     for x in (700, 780, 860))
    spots = "".join(
        f'<button class="spot" style="left:{x}%;top:{y}%" data-i="{i}" aria-label="{esc(t)}"><span>{i + 1}</span></button>'
        for i, (x, y, t, _) in enumerate(ANATOMY))
    return f'''
<div class="anatomy-stage">
<svg viewBox="0 0 1000 360" class="blueprint" role="img" aria-label="Esquema lateral de un semirremolque Santander con sus componentes">
  <defs><pattern id="g" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="rgba(120,180,255,.08)"/></pattern></defs>
  <rect width="1000" height="360" fill="url(#g)"/>
  <g class="bp-lines">
    <rect x="80" y="55" width="870" height="190" rx="4"/>
    <g class="straps">{straps}</g>
    <text x="515" y="168" text-anchor="middle" class="bp-brand">SANTANDER</text>
    <path d="M80 245 H950 V262 H80z"/>
    <path d="M110 262 h120 l20 14 h-160z"/>
    <line x1="160" y1="276" x2="160" y2="290"/>
    <path d="M290 262 v58 M330 262 v58 M276 322 h28 M316 322 h28"/>
    <rect x="470" y="268" width="110" height="26" rx="13"/>
    <path d="M640 262 h260 v12 h-260z"/>
    {wheels}
    <path d="M940 225 h14 v14 h-14z"/>
  </g>
  <g class="bp-dims"><line x1="80" y1="30" x2="950" y2="30"/><path d="M80 24v12M950 24v12"/>
  <text x="515" y="22" text-anchor="middle">12.400 – 15.800 mm</text>
  <line x1="972" y1="55" x2="972" y2="262"/><path d="M966 55h12M966 262h12"/>
  <text x="990" y="160" text-anchor="middle" transform="rotate(90 990 160)">2.700 – 3.000 mm</text></g>
</svg>
{spots}
</div>'''


# --------------------------------------------------------------------------- páginas
def build_home():
    faqs = [
        ("¿Qué acero utilizan en sus semirremolques?",
         "Fabricamos la superestructura con acero de alta resistencia Strenx® 700 de procedencia sueca (SSAB). SSAB nos certificó con el sello «My Inner Strenx», que acredita el uso de acero Strenx genuino según sus estándares técnicos y de calidad."),
        ("¿Los equipos cumplen con la normativa chilena?",
         "Sí. Todos nuestros desarrollos se diseñan según la legislación de transporte vigente: pesos y dimensiones máximas, luces y frenos, parachoques y cintas reflectantes. Puedes revisar la normativa en nuestra sección de Calidad."),
        ("¿Puedo configurar el equipo a la medida de mi operación?",
         "Sí. Según el modelo puedes elegir largo (de 10.500 a 15.800 mm), suspensión mecánica o neumática, llantas de acero o aluminio, frenos convencionales o EBS, piso de 3 o 5 mm y accesorios. Nuestro departamento de ingeniería te asesora."),
        ("¿Qué es el sistema de frenos EBS?",
         "Es un sistema de frenado electrónico según normativa internacional CE: ajusta la fuerza de frenado según la carga, incorpora control de estabilidad antivuelco, control inteligente de eje elevable y control de flota."),
        ("¿También reparan equipos?",
         "Sí. Somos especialistas en la fabricación y reparación de todo tipo de equipamiento para el transporte terrestre, y estamos homologados con la mayoría de las marcas de camiones."),
        ("¿Cómo solicito una cotización?",
         f"Completa el formulario de cotización o escríbenos por WhatsApp al {PHONE}. Cuéntanos qué transportas, la ruta y tu camión, y te proponemos la configuración ideal."),
    ]
    faq_html = "".join(f'<details class="faq reveal"><summary>{esc(q)}{icon("chev")}</summary><p>{esc(a)}</p></details>' for q, a in faqs)
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
    benefits = [
        ("weight", "Más carga útil por viaje", "El acero de alta resistencia permite estructuras más livianas sin perder rigidez. Menos tara significa más kilos pagados en cada viaje."),
        ("steel", "Acero sueco certificado", "Superestructura en Strenx® 700 de SSAB. Contamos con el sello «My Inner Strenx», la garantía de rendimiento, ahorro y vida útil."),
        ("brake", "Seguridad activa", "Válvulas Bendix y opción de frenos EBS con control de estabilidad antivuelco y frenado variable según carga."),
        ("law", "100% normativa chilena", "Diseñamos según la legislación vigente: dimensiones y pesos máximos, luces, frenos, parachoques y cintas reflectantes."),
        ("paint", "Protección anticorrosiva", "Limpieza química con fosfatizante, dos capas de anticorrosivo epóxico y dos de poliuretano en proceso electrostático."),
        ("gear", "Ingeniería propia", "Departamento de ingeniería y personal técnico propio. Integramos acero, aluminio y plástico para equipos funcionales y durables."),
    ]
    ben_html = "".join(f'<article class="b-card reveal" style="--d:{i * 70}ms"><span class="b-ico">{icon(ic)}</span><h3>{t}</h3><p>{d}</p></article>'
                       for i, (ic, t, d) in enumerate(benefits))
    steps = [("Diagnóstico", "Analizamos tu carga, rutas y camión para definir la configuración óptima."),
             ("Ingeniería y diseño", "Nuestro equipo de ingeniería diseña el equipo según normativa y tus requerimientos."),
             ("Fabricación certificada", "Fabricamos en acero Strenx® 700 bajo un sistema de calidad ISO 9001."),
             ("Entrega y postventa", "Te entregamos el equipo listo para trabajar y te acompañamos con reparación y mantención.")]
    step_html = "".join(f'<li class="reveal" style="--d:{i * 90}ms"><span class="st-n">0{i + 1}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(steps))
    an_list = "".join(f'<li data-i="{i}"{" class=is-on" if i == 0 else ""}><button><span>{i + 1}</span>{esc(t)}</button><p>{esc(d)}</p></li>'
                      for i, (_, _, t, d) in enumerate(ANATOMY))
    logos = "".join(f'<img src="assets/img/{b}.webp" alt="{n}" width="140" height="70" loading="lazy">'
                    for b, n in [("scania", "Scania"), ("daf", "DAF"), ("hino", "Hino"), ("faw", "FAW"), ("international", "International")])
    body = f'''
<section class="hero">
  <div class="hero-bg" aria-hidden="true"><span class="road"></span></div>
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <p class="eyebrow light"><span class="dot"></span> Ingeniería en Movimiento · Desde 2009</p>
      <h1>Semirremolques de <em>acero sueco</em>, hechos en Chile para cargar más y durar más.</h1>
      <p class="lead">Diseñamos y fabricamos equipos Sider, Plano, Forestal, Minero, Carga Seca y Botellero con acero Strenx® 700, ejes europeos y certificación ISO 9001.</p>
      <div class="hero-cta">
        <a class="btn btn-primary btn-lg" href="contacto.html#cotizar">Cotiza tu equipo {icon("arrow")}</a>
        <a class="btn btn-outline-light btn-lg" href="#equipos">Ver equipos</a>
      </div>
      <ul class="hero-trust">
        <li>{icon("award")} Swedish Steel Prize 2014</li>
        <li>{icon("shield")} ISO 9001 · Bureau Veritas</li>
        <li>{icon("steel")} My Inner Strenx®</li>
      </ul>
    </div>
    <div class="hero-visual">
      <figure class="hv-main"><img src="assets/img/sider01.webp" alt="Semirremolque Speed Sider Santander con cortinas azules" width="600" height="400" fetchpriority="high"></figure>
      <figure class="hv-sm hv-a"><img src="assets/img/srf1.webp" alt="Semirremolque Forestal Santander con estacas verdes" width="600" height="400"></figure>
      <figure class="hv-sm hv-b"><img src="assets/img/srbt2.webp" alt="Semirremolque Botellero Santander de doble piso" width="600" height="400"></figure>
      <div class="hv-badge"><span class="hv-medal">{icon("award")}</span><div><b>2.º lugar</b><small>Swedish Steel Prize 2014 · SSAB</small></div></div>
    </div>
  </div>
  <div class="wrap stats">
    <div class="stat"><b><span data-years>+{YEAR - 2009}</span></b><span>años fabricando en Chile</span></div>
    <div class="stat"><b data-count="6">6</b><span>líneas de semirremolques</span></div>
    <div class="stat"><b><span data-count="13000">13.000</span> kg</b><span>capacidad por eje</span></div>
    <div class="stat"><b><span data-count="700">700</span> MPa</b><span>límite elástico del acero Strenx® 700</span></div>
  </div>
</section>

<section class="logos" aria-label="Marcas de camiones con las que trabajamos">
  <div class="wrap logos-row"><p>Trabajamos con las principales marcas de camiones</p>
  <div class="marquee"><div class="marquee-track">{logos}{logos}</div></div></div>
</section>

<section class="sec" id="equipos"><div class="wrap">{catalog()}
<div class="center reveal"><a class="btn btn-ghost" href="equipos.html">Comparar todos los equipos {icon("arrow")}</a></div>
</div></section>

<section class="sec award">
  <div class="wrap award-grid">
    <div class="award-docs reveal">
      <button class="doc doc-1" data-lightbox="assets/img/premio-swedish-steel-prize-2014.webp" data-caption="Swedish Steel Prize 2014 · Segundo lugar · SSAB"><img src="assets/img/premio-swedish-steel-prize-2014.webp" alt="Diploma Swedish Steel Prize 2014, segundo lugar para Santander Equipos" width="700" height="985" loading="lazy"></button>
      <button class="doc doc-2" data-lightbox="assets/img/certificado-my-inner-strenx.webp" data-caption="Certificado My Inner Strenx · SSAB"><img src="assets/img/certificado-my-inner-strenx.webp" alt="Certificado My Inner Strenx otorgado por SSAB" width="700" height="996" loading="lazy"></button>
    </div>
    <div class="award-copy reveal">
      <p class="eyebrow light">Reconocimiento internacional</p>
      <h2>Premiados en Suecia por la cuna del acero de alta resistencia</h2>
      <p>En 2014 Santander Equipos obtuvo el <strong>segundo lugar del Swedish Steel Prize</strong>, el premio con que SSAB distingue a las empresas que mejor aprovechan los aceros de alta resistencia en el mundo.</p>
      <blockquote>“El ganador del Swedish Steel Prize ha aprovechado, de manera inteligente e innovadora, el potencial de los aceros modernos de alta resistencia para crear algo nuevo y mejor, en beneficio de la industria y la sociedad.”<cite>— Jurado Swedish Steel Prize, SSAB</cite></blockquote>
      <p>Además, SSAB nos certifica con el sello <strong>My Inner Strenx</strong>: la garantía de que cada equipo usa acero Strenx genuino.</p>
      <a class="btn btn-light" href="calidad.html#premios">Ver premios y certificaciones {icon("arrow")}</a>
    </div>
  </div>
</section>

<section class="sec"><div class="wrap">
  <div class="sec-head reveal"><p class="eyebrow">Por qué Santander</p><h2>Equipos que <span class="hl-text">rinden más</span> en cada kilómetro</h2>
  <p>Nuestra visión del transporte: equipos con valor agregado en peso, seguridad y durabilidad.</p></div>
  <div class="b-grid">{ben_html}</div>
</div></section>

<section class="sec anatomy" id="anatomia"><div class="wrap">
  <div class="sec-head reveal light"><p class="eyebrow light">Ingeniería al detalle</p><h2>Anatomía de un semirremolque Santander</h2>
  <p>Toca cada punto para conocer los componentes que hacen la diferencia.</p></div>
  <div class="anatomy-grid reveal">{anatomy_svg()}<ol class="an-list">{an_list}</ol></div>
</div></section>

<section class="sec calc-sec" id="simulador"><div class="wrap calc-grid">
  <div class="reveal"><p class="eyebrow">Simulador</p><h2>¿Cuánto vale cada kilo que le quitas a tu equipo?</h2>
  <p>Un equipo más liviano te permite transportar más carga útil dentro del peso máximo legal. Ajusta los valores y mira el impacto en tu operación.</p>
  <p class="fine">Valores referenciales de ejemplo. Pide a nuestro equipo la tara exacta de tu configuración.</p></div>
  <form class="calc reveal" onsubmit="return false">
    <label>Kilos menos de tara <output id="o-kg">800 kg</output><input type="range" id="c-kg" min="200" max="2500" step="50" value="800"></label>
    <label>Viajes al mes por equipo <output id="o-trips">20</output><input type="range" id="c-trips" min="4" max="60" step="1" value="20"></label>
    <label>Tarifa por tonelada (CLP) <output id="o-rate">$25.000</output><input type="range" id="c-rate" min="5000" max="80000" step="1000" value="25000"></label>
    <label>Número de equipos <output id="o-units">1</output><input type="range" id="c-units" min="1" max="30" step="1" value="1"></label>
    <div class="calc-out"><div><small>Carga extra al año</small><b id="r-ton">192 t</b></div>
    <div><small>Ingresos potenciales al año</small><b id="r-clp">$4.800.000</b></div></div>
  </form>
</div></section>

<section class="sec soft"><div class="wrap">
  <div class="sec-head reveal"><p class="eyebrow">Cómo trabajamos</p><h2>De la idea a la ruta, en cuatro pasos</h2></div>
  <ol class="steps">{step_html}</ol>
  <div class="video-row reveal">
    {video_embed("5EFBjY9szrk", "Santander Equipos: así fabricamos")}
    <div><h3>Mira nuestros equipos en acción</h3><p>Conoce nuestra planta, nuestros procesos y el resultado final: equipos funcionales, estéticos y durables, fabricados con acero, aluminio y plástico de primera línea.</p>
    <a class="btn btn-primary" href="nosotros.html">Conoce la empresa {icon("arrow")}</a></div>
  </div>
</div></section>

<section class="sec"><div class="wrap faq-grid">
  <div class="sec-head left reveal"><p class="eyebrow">Preguntas frecuentes</p><h2>Resolvemos tus dudas</h2>
  <p>¿No encuentras lo que buscas? Escríbenos y un especialista te responde.</p>
  <a class="btn btn-wa" href="{WA}" target="_blank" rel="noopener">{icon("whatsapp")} Preguntar por WhatsApp</a></div>
  <div class="faqs">{faq_html}</div>
</div></section>
'''
    page("index.html", "Santander Equipos | Fabricación de semirremolques en Chile · Acero Strenx® 700",
         "Fabricantes de semirremolques en Chile desde 2009: Sider, Plano, Forestal, Minero, Carga Seca y Botellero en acero sueco Strenx® 700. ISO 9001 y Swedish Steel Prize 2014. Cotiza hoy.",
         body, "index.html", [faq_ld])


def page_hero(eyebrow, title, text, crumbs, bg="ruta.webp"):
    cr = "".join(f'<li><a href="{h}">{t}</a></li>' if h else f'<li aria-current="page">{t}</li>' for h, t in crumbs)
    return f'''<section class="page-hero" style="--bg:url(../img/{bg})"><div class="wrap">
<nav aria-label="Ruta de navegación"><ol class="crumbs">{cr}</ol></nav>
<p class="eyebrow light">{eyebrow}</p><h1>{title}</h1><p class="lead">{text}</p></div></section>'''


def build_equipos():
    rows = [("Aplicación", lambda p: p["specs"].get("Aplicación", p["app"])),
            ("Largo", lambda p: p["specs"].get("Dimensiones", {}).get("Largo", "—")),
            ("Ancho", lambda p: p["specs"].get("Dimensiones", {}).get("Ancho", "—")),
            ("Alto", lambda p: p["specs"].get("Dimensiones", {}).get("Alto", "—")),
            ("Acero", lambda p: "Strenx® 700"),
            ("Piso", lambda p: p["specs"].get("Piso", "—")),
            ("Ejes", lambda p: "Disco europeo 13.000 kg"),
            ("Frenos EBS", lambda p: "Opcional" if "Sistema EBS" in p["specs"] else "—")]
    th = "".join(f'<th scope="col"><a href="equipo-{p["slug"]}.html">{p["name"]}</a></th>' for p in PRODUCTS)
    tr = "".join(f'<tr><th scope="row">{lab}</th>{"".join(f"<td>{esc(f(p))}</td>" for p in PRODUCTS)}</tr>' for lab, f in rows)
    services = [("body", "Carrocerías", "Diseñamos y fabricamos carrocerías a medida para camiones de todas las marcas."),
                ("wrench", "Reparación", "Reparamos todo tipo de equipamiento para el transporte terrestre, propio o de otras marcas."),
                ("ruler", "Proyectos especiales", "¿Tu carga no calza con un modelo estándar? Nuestro departamento de ingeniería lo desarrolla.")]
    sv = "".join(f'<article class="b-card reveal"><span class="b-ico">{icon(i)}</span><h3>{t}</h3><p>{d}</p></article>' for i, t, d in services)
    body = f'''{page_hero("Catálogo", "Semirremolques para cada tipo de carga",
        "Sider, Plano, Forestal, Minero, Carga Seca y Botellero: todos en acero Strenx® 700, con ejes europeos de 13.000 kg y configuraciones a la medida de tu operación.",
        [("index.html", "Inicio"), (None, "Equipos")])}
<section class="sec"><div class="wrap">{catalog(False)}</div></section>
<section class="sec soft"><div class="wrap">
  <div class="sec-head reveal"><p class="eyebrow">Comparador</p><h2>Compara nuestros equipos de un vistazo</h2></div>
  <div class="table-wrap reveal" tabindex="0"><table class="compare"><thead><tr><th></th>{th}</tr></thead><tbody>{tr}</tbody></table></div>
  <p class="fine center">Desliza la tabla horizontalmente en tu teléfono. Medidas en milímetros.</p>
</div></section>
<section class="sec"><div class="wrap"><div class="sec-head reveal"><p class="eyebrow">Además</p><h2>Más que semirremolques</h2></div>
<div class="b-grid three">{sv}</div></div></section>'''
    ld = {"@context": "https://schema.org", "@type": "ItemList", "name": "Semirremolques Santander Equipos",
          "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{SITE}/equipo-{p['slug']}.html", "name": p["name"]}
                              for i, p in enumerate(PRODUCTS)]}
    page("equipos.html", "Semirremolques Sider, Plano, Forestal, Minero y más | Santander Equipos",
         "Catálogo de semirremolques Santander Equipos: Speed Sider, Botellero, Forestal, Minero, Carga Seca y Plano. Compara medidas y especificaciones y cotiza en línea.",
         body, "equipos.html", [ld])


def spec_value(key, val):
    if key == "Sistema Eléctrico":
        text, bullets = val
        return f'<p>{esc(text)}</p><ul class="ticks">{"".join(f"<li>{icon("check")}{esc(b)}</li>" for b in bullets)}</ul>'
    if key == "Pintura y tratamiento anticorrosivo":
        return "<dl class='mini'>" + "".join(f"<div><dt>{esc(a)}</dt><dd>{esc(b)}</dd></div>" for a, b in val) + "</dl>"
    if key == "Accesorios.":
        return f'<ul class="ticks">{"".join(f"<li>{icon("check")}{esc(b)}</li>" for b in val)}</ul>'
    return f"<p>{esc(val)}</p>"


def build_product(p):
    s = p["specs"]
    d = s.get("Dimensiones", {})
    tiles = [("ruler", "Largo", d.get("Largo", "—")), ("ruler", "Ancho", d.get("Ancho", "—")),
             ("ruler", "Alto", d.get("Alto", "—")), ("steel", "Acero", "Strenx® 700 (SSAB)"),
             ("truck", "Ejes", "Europeos 13.000 kg"), ("brake", "Frenos", "Bendix · EBS opcional")]
    tiles_html = "".join(f'<div class="tile">{icon(i)}<small>{t}</small><b>{esc(v)}</b></div>' for i, t, v in tiles)
    imgs = [p["slug"]] + p["photos"]
    main_img = imgs[1] if len(imgs) > 1 else imgs[0]
    thumbs = "".join(
        f'<button class="thumb{" is-on" if im == main_img else ""}" data-src="assets/img/{im}.webp" aria-label="Ver imagen {n + 1}"><img src="assets/img/{im}.webp" alt="" loading="lazy" width="120" height="70"></button>'
        for n, im in enumerate(imgs)) if len(imgs) > 1 else ""
    tabs, panels = [], []
    for gi, (gname, gicon, keys) in enumerate(SPEC_GROUPS):
        items = [(k, s[k]) for k in keys if k in s]
        if not items:
            continue
        on = gi == 0
        tabs.append(f'<button role="tab" id="t{gi}" aria-controls="p{gi}" aria-selected="{"true" if on else "false"}"{" class=is-on" if on else ""}>{icon(gicon)}{gname}</button>')
        rows = "".join(f'<div class="spec-row"><h4>{esc(LABEL_FIX.get(k, k))}</h4><div>{spec_value(k, v)}</div></div>' for k, v in items)
        panels.append(f'<div role="tabpanel" id="p{gi}" aria-labelledby="t{gi}"{"" if on else " hidden"}>{rows}</div>')
    videos = ""
    if p["videos"]:
        videos = f'''<section class="sec soft"><div class="wrap"><div class="sec-head reveal"><p class="eyebrow">Video</p><h2>El {p["name"]} en acción</h2></div>
<div class="video-grid reveal">{"".join(video_embed(v, f"Semirremolque {p['name']} Santander") for v in p["videos"])}</div></div></section>'''
    others = [o for o in PRODUCTS if o["slug"] != p["slug"]][:3]
    wa = wa_link(f"Hola, quiero cotizar el semirremolque {p['name']}. ¿Me pueden enviar información?")
    pdf_kb = (OUT / "assets" / "pdf" / p["pdf"]).stat().st_size / 1024 / 1024
    body = f'''
<section class="prod-hero"><div class="wrap">
  <nav aria-label="Ruta de navegación"><ol class="crumbs dark"><li><a href="index.html">Inicio</a></li><li><a href="equipos.html">Equipos</a></li><li aria-current="page">{p["name"]}</li></ol></nav>
  <div class="prod-grid">
    <div class="gallery reveal">
      <figure class="g-main"><img id="g-main" src="assets/img/{main_img}.webp" alt="Semirremolque {p["name"]} Santander Equipos" width="700" height="400" fetchpriority="high"></figure>
      <div class="thumbs">{thumbs}</div>
    </div>
    <div class="prod-info reveal">
      <p class="eyebrow">Semirremolque · {esc(p["app"])}</p>
      <h1>Semirremolque {p["name"]}</h1>
      <p class="lead">{esc(p["lead"])}</p>
      <ul class="ticks big">{"".join(f"<li>{icon('check')}{esc(h)}</li>" for h in p["highlights"])}</ul>
      <div class="prod-cta">
        <a class="btn btn-primary btn-lg" href="contacto.html?equipo={p["slug"]}#cotizar">Cotizar este equipo {icon("arrow")}</a>
        <a class="btn btn-wa btn-lg" href="{wa}" target="_blank" rel="noopener">{icon("whatsapp")} WhatsApp</a>
      </div>
      <a class="pdf-link" href="assets/pdf/{p["pdf"]}" target="_blank" rel="noopener">{icon("download")} Descargar ficha técnica (PDF, {pdf_kb:.1f} MB)</a>
    </div>
  </div>
  <div class="tiles reveal">{tiles_html}</div>
</div></section>
<section class="sec"><div class="wrap">
  <div class="sec-head reveal"><p class="eyebrow">Descripción técnica</p><h2>Especificaciones completas</h2></div>
  <div class="spec-tabs reveal"><div role="tablist" aria-label="Grupos de especificaciones">{"".join(tabs)}</div>{"".join(panels)}</div>
  <p class="fine">Las especificaciones pueden variar según la configuración solicitada. Confirma los detalles con nuestro equipo comercial.</p>
</div></section>
{videos}
<section class="sec soft"><div class="wrap"><div class="sec-head reveal"><p class="eyebrow">Sigue explorando</p><h2>Otros equipos que te pueden interesar</h2></div>
<div class="p-grid">{"".join(product_card(o, i) for i, o in enumerate(others))}</div></div></section>'''
    ld = [{
        "@context": "https://schema.org", "@type": "Product", "name": f"Semirremolque {p['name']}",
        "description": p["lead"], "image": [f"{SITE}/assets/img/{im}.webp" for im in imgs],
        "brand": {"@type": "Brand", "name": "Santander Equipos"}, "category": "Semirremolques",
        "manufacturer": {"@id": SITE + "/#empresa"},
        "material": "Acero de alta resistencia Strenx 700",
        "additionalProperty": [{"@type": "PropertyValue", "name": k, "value": v} for k, v in d.items()],
    }, {
        "@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Equipos", "item": SITE + "/equipos.html"},
            {"@type": "ListItem", "position": 3, "name": p["name"], "item": f"{SITE}/equipo-{p['slug']}.html"}]}]
    page(f"equipo-{p['slug']}.html", f"Semirremolque {p['name']} en acero Strenx® 700 | Santander Equipos",
         f"Semirremolque {p['name']} ({p['app'].lower()}): {p['short'].lower()}. Largo {d.get('Largo', '')}, acero Strenx® 700, ejes europeos 13.000 kg. Ficha técnica y cotización.",
         body, "equipos.html", ld, og_image=f"assets/img/{main_img}.webp")


def build_nosotros():
    timeline = [
        ("2009", "Nace Santander Equipos", "Con la misión de satisfacer las diferentes necesidades del rubro transporte, entregando trabajo y compromiso a nuestros clientes."),
        ("ISO 9001", "Calidad certificada", "Nuestra producción y área de servicios se certifican bajo la norma ISO 9001 con Bureau Veritas."),
        ("2014", "Swedish Steel Prize", "SSAB nos otorga el segundo lugar del Swedish Steel Prize por el uso innovador del acero de alta resistencia."),
        ("My Inner Strenx", "Sello de SSAB", "SSAB certifica que nuestros productos usan acero Strenx genuino, según sus estándares técnicos y de calidad."),
        ("Hoy", "Seis líneas de equipos", "Fabricamos y reparamos equipos para carga general, pallets, forestal y minería, homologados con la mayoría de las marcas de camiones."),
    ]
    tl = "".join(f'<li class="reveal"><span class="tl-y">{y}</span><div><h3>{t}</h3><p>{d}</p></div></li>' for y, t, d in timeline)
    values = [("users", "Compromiso con el cliente", "La prioridad es satisfacer todos los requerimientos de nuestros clientes."),
              ("gear", "Innovación continua", "Seguimos innovando y mejorando continuamente nuestros procesos, servicios y productos."),
              ("box", "Materiales de primera", "Además del acero, integramos el aluminio y el plástico como elementos principales de fabricación."),
              ("shield", "Calidad y estética", "Equipos funcionales y de calidad, pero también estéticos y durables.")]
    vv = "".join(f'<article class="b-card reveal"><span class="b-ico">{icon(i)}</span><h3>{t}</h3><p>{d}</p></article>' for i, t, d in values)
    services = [("truck", "Fabricación de semirremolques", "Seis líneas de equipos en acero Strenx® 700, configurables a la medida de tu operación.", "equipos.html", "Ver equipos"),
                ("body", "Carrocerías", "Carrocerías para camiones de todas las marcas, con ingeniería propia y homologación del fabricante.", "contacto.html?tipo=carroceria#cotizar", "Cotizar carrocería"),
                ("wrench", "Reparación y mantención", "Reparamos todo tipo de equipamiento para el transporte terrestre con técnicos certificados por nuestros proveedores.", "contacto.html?tipo=reparacion#cotizar", "Agendar reparación")]
    sv = "".join(f'<article class="svc reveal"><span class="b-ico">{icon(i)}</span><h3>{t}</h3><p>{d}</p><a href="{h}">{c} {icon("arrow")}</a></article>' for i, t, d, h, c in services)
    body = f'''{page_hero("Sobre Santander", "Ingeniería en movimiento desde 2009",
        "Somos especialistas en la fabricación y reparación de todo tipo de equipamiento para el transporte terrestre. Nuestro departamento de ingeniería y nuestro personal técnico hacen la diferencia.",
        [("index.html", "Inicio"), (None, "Nosotros")])}
<section class="sec"><div class="wrap split">
  <div class="reveal"><p class="eyebrow">Nuestra historia</p><h2>Equipos de calidad, funcionales y durables</h2>
  <p>Santander Equipos fue creada el año 2009 con la misión de satisfacer las diferentes necesidades del rubro transporte. Nuestra producción y área de servicios están respaldadas por un sistema de gestión de calidad ISO 9001, lo que nos permite entregar un servicio de excelencia, equipos de primera calidad, innovación y tecnología.</p>
  <p>Para nosotros la prioridad es satisfacer todos los requerimientos de nuestros clientes. Por eso estamos continuamente creando y produciendo equipos de calidad y funcionales, pero también dotados de estética y que aportan durabilidad.</p>
  <div class="mini-stats"><div><b>+{YEAR - 2009}</b><span>años</span></div><div><b>6</b><span>líneas de equipos</span></div><div><b>ISO</b><span>9001</span></div></div></div>
  <figure class="split-img reveal"><img src="assets/img/sider02.webp" alt="Semirremolque Santander estacionado frente a la planta" width="600" height="400" loading="lazy">
  <img class="split-img-2" src="assets/img/srbt1.webp" alt="Semirremolque Botellero Santander" width="600" height="400" loading="lazy"></figure>
</div></section>
<section class="sec soft"><div class="wrap"><div class="sec-head reveal"><p class="eyebrow">Trayectoria</p><h2>Hitos que nos respaldan</h2></div><ol class="timeline">{tl}</ol></div></section>
<section class="sec" id="servicios"><div class="wrap"><div class="sec-head reveal"><p class="eyebrow">Servicios</p><h2>Todo lo que tu flota necesita, en un solo lugar</h2></div><div class="svc-grid">{sv}</div></div></section>
<section class="sec dark-sec"><div class="wrap split">
  <div class="reveal"><p class="eyebrow light">Homologación</p><h2>Respaldados por los fabricantes de camiones</h2>
  <p>Para entregar una mejor atención, servicio y mejores equipos, hemos homologado nuestra empresa con la mayoría de las marcas de camiones. Esto respalda nuestra intervención en cada camión, con la confianza y seguridad avalada por el propio fabricante.</p>
  <p>Además, invitamos a nuestros proveedores a participar de nuestros procesos certificando a nuestros técnicos, para obtener el mejor aprovechamiento de sus insumos.</p>
  <a class="btn btn-light" href="calidad.html#normativa">Ver normativa {icon("arrow")}</a></div>
  <div class="brand-wall reveal">{"".join(f'<img src="assets/img/{b}.webp" alt="{n}" width="140" height="70" loading="lazy">' for b, n in [("scania", "Scania"), ("daf", "DAF"), ("hino", "Hino"), ("faw", "FAW"), ("international", "International")])}</div>
</div></section>
<section class="sec"><div class="wrap"><div class="sec-head reveal"><p class="eyebrow">Nuestros valores</p><h2>Lo que nos mueve</h2></div><div class="b-grid four">{vv}</div></div></section>'''
    page("nosotros.html", "Nosotros: fabricantes de semirremolques desde 2009 | Santander Equipos",
         "Conoce Santander Equipos: fabricación y reparación de semirremolques y carrocerías en Chile desde 2009, con ingeniería propia, ISO 9001 y premio Swedish Steel Prize.",
         body, "nosotros.html", og_image="assets/img/sider02.webp")


def build_calidad():
    laws = [("Ley-18290-Dimensiones-maximas.pdf", "Dimensiones máximas", "Ley 18.290 de Tránsito"),
            ("Dec-158.1980-Peso-Maximo.pdf", "Peso máximo", "Decreto 158 / 1980"),
            ("Ley19872-Reg-Nac-Transp-Carga.pdf", "Registro Nacional de Transporte de Carga", "Ley 19.872"),
            ("Dec-22.2006-Luces-y-Frenos.pdf", "Luces y frenos", "Decreto 22 / 2006"),
            ("Resex_1463.2000-Parachoques.pdf", "Parachoques", "Resolución exenta 1.463 / 2000"),
            ("Resex_1465.2000-Cintas-reflectantes.pdf", "Cintas reflectantes", "Resolución exenta 1.465 / 2000")]
    lw = "".join(f'<a class="doc-card reveal" href="assets/pdf/{f}" target="_blank" rel="noopener">{icon("file")}<span><b>{t}</b><small>{s}</small></span>{icon("download")}</a>' for f, t, s in laws)
    awards = [("premio-swedish-steel-prize-2014.webp", "Swedish Steel Prize 2014", "Segundo lugar otorgado por SSAB (Suecia) por el uso inteligente e innovador de aceros de alta resistencia."),
              ("certificado-my-inner-strenx.webp", "My Inner Strenx", "SSAB certifica que Sociedad Comercial Santander Ltda. usa acero Strenx genuino en sus productos."),
              ("certificado-iso-9001.webp", "ISO 9001 · Bureau Veritas", "Sistema de gestión de calidad certificado para el diseño, fabricación y reparación de equipos de transporte.")]
    aw = "".join(f'<figure class="aw-card reveal"><button data-lightbox="assets/img/{f}" data-caption="{t}"><img src="assets/img/{f}" alt="{t}" width="700" height="990" loading="lazy"></button><figcaption><h3>{t}</h3><p>{d}</p></figcaption></figure>' for f, t, d in awards)
    body = f'''{page_hero("Calidad, premios y normativa", "Calidad certificada, reconocida en el mundo",
        "Un sistema de gestión ISO 9001, acero sueco certificado por SSAB y equipos diseñados según la normativa chilena de transporte.",
        [("index.html", "Inicio"), (None, "Calidad y premios")])}
<section class="sec"><div class="wrap split">
  <div class="reveal"><p class="eyebrow">Certificación ISO 9001</p><h2>Un compromiso de calidad auditado</h2>
  <p>Nuestro compromiso de calidad con el cliente está avalado por la certificación ISO 9001 de Bureau Veritas. Además, invitamos a nuestros proveedores a participar de nuestros procesos certificando a nuestros técnicos, con la finalidad de obtener el mejor aprovechamiento de sus insumos y condicionar de la mejor manera nuestros equipamientos.</p>
  <ul class="ticks big"><li>{icon("check")}Procesos de diseño, fabricación y reparación documentados</li><li>{icon("check")}Técnicos certificados por nuestros proveedores</li><li>{icon("check")}Mejora continua en procesos, servicios y productos</li></ul>
  <a class="btn btn-primary" href="assets/pdf/Certificado-ISO9001.pdf" target="_blank" rel="noopener">{icon("download")} Descargar certificado</a></div>
  <div class="iso-seal reveal"><div class="seal"><span>ISO</span><b>9001</b><small>Bureau Veritas Certification</small></div></div>
</div></section>
<section class="sec soft" id="premios"><div class="wrap"><div class="sec-head reveal"><p class="eyebrow">Premios y certificaciones</p><h2>Reconocidos por SSAB, líder mundial en aceros de alta resistencia</h2><p>Toca cada documento para verlo en grande.</p></div>
<div class="aw-grid">{aw}</div></div></section>
<section class="sec" id="normativa"><div class="wrap"><div class="sec-head reveal"><p class="eyebrow">Legislación</p><h2>Diseñados según la normativa chilena de transporte</h2>
<p>Todos nuestros desarrollos están acordes con lo que la legislación de transporte define. Descarga la normativa de referencia:</p></div>
<div class="doc-grid">{lw}</div></div></section>'''
    page("calidad.html", "Certificación ISO 9001, premios SSAB y normativa | Santander Equipos",
         "Santander Equipos: certificación ISO 9001 (Bureau Veritas), Swedish Steel Prize 2014 y sello My Inner Strenx de SSAB. Descarga la normativa chilena de transporte de carga.",
         body, "calidad.html", og_image="assets/img/premio-swedish-steel-prize-2014.webp")


def build_contacto():
    opts = "".join(f'<option value="{p["slug"]}">{p["name"]}</option>' for p in PRODUCTS)
    areas = [("Ventas", "Cotizaciones de semirremolques, carrocerías y reparaciones.", "Hola, quiero hablar con Ventas."),
             ("Proveedores", "Ofertas de insumos, materiales y servicios.", "Hola, escribo por el área de Proveedores."),
             ("Contabilidad", "Facturación, pagos y documentos tributarios.", "Hola, escribo por el área de Contabilidad.")]
    ar = "".join(f'<a class="area reveal" href="{wa_link(m)}" target="_blank" rel="noopener">{icon("whatsapp")}<span><b>{t}</b><small>{d}</small></span>{icon("arrow")}</a>' for t, d, m in areas)
    body = f'''{page_hero("Contacto", "Cotiza tu equipo en minutos",
        "Cuéntanos qué necesitas y te respondemos a la brevedad. También puedes escribirnos directo por WhatsApp.",
        [("index.html", "Inicio"), (None, "Contacto")])}
<section class="sec" id="cotizar"><div class="wrap contact-grid">
  <form class="quote reveal" id="quote" novalidate>
    <h2>Solicitud de cotización</h2>
    <p class="fine">Al enviar, se abrirá WhatsApp con tu solicitud lista para mandar.</p>
    <div class="seg" role="radiogroup" aria-label="Tipo de solicitud">
      <label><input type="radio" name="tipo" value="Semirremolque" checked><span>{icon("truck")}Semirremolque</span></label>
      <label><input type="radio" name="tipo" value="Carrocería"><span>{icon("body")}Carrocería</span></label>
      <label><input type="radio" name="tipo" value="Reparación"><span>{icon("wrench")}Reparación</span></label>
    </div>
    <div class="f-grid">
      <label>Nombre*<input name="nombre" required autocomplete="name"></label>
      <label>Empresa<input name="empresa" autocomplete="organization"></label>
      <label>Teléfono*<input name="telefono" type="tel" required autocomplete="tel" placeholder="+56 9"></label>
      <label>Correo<input name="correo" type="email" autocomplete="email"></label>
      <label class="eq-field">Equipo de interés<select name="equipo"><option value="">Selecciona un equipo</option>{opts}<option value="medida">Proyecto a medida</option></select></label>
      <label>Cantidad<input name="cantidad" type="number" min="1" value="1"></label>
      <label class="full">Mensaje<textarea name="mensaje" rows="4" placeholder="¿Qué transportas? ¿Qué camión tienes? ¿Para cuándo lo necesitas?"></textarea></label>
    </div>
    <button class="btn btn-primary btn-lg full" type="submit">{icon("whatsapp")} Enviar solicitud</button>
    <p class="form-msg" role="status" aria-live="polite"></p>
  </form>
  <aside class="contact-side">
    <div class="c-card reveal"><h3>Escríbenos por área</h3>{ar}</div>
    <div class="c-card reveal"><h3>Datos de contacto</h3>
      <ul class="c-list"><li>{icon("phone")}<a href="tel:+{PHONE_RAW}">{PHONE}</a></li>
      <li>{icon("pin")}<a href="{MAP_LINK}" target="_blank" rel="noopener">Región Metropolitana, Chile · Ver en Google Maps</a></li>
      <li>{icon("chat")}<span>Respuesta rápida por WhatsApp</span></li></ul>
      <div class="social dark">{"".join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="{n}">{icon(k)}</a>' for k, (n, u) in SOCIAL.items())}</div>
    </div>
  </aside>
</div></section>
<section class="map-sec"><iframe title="Ubicación de Santander Equipos en Google Maps" src="{MAP_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></section>'''
    page("contacto.html", "Contacto y cotización de semirremolques | Santander Equipos",
         f"Cotiza semirremolques, carrocerías o reparaciones con Santander Equipos. WhatsApp {PHONE}. Respuesta rápida, Región Metropolitana, Chile.",
         body, "contacto.html")


def build_404():
    body = f'''<section class="page-hero tall" style="--bg:url(../img/ruta.webp)"><div class="wrap">
<p class="eyebrow light">Error 404</p><h1>Esta ruta no existe</h1><p class="lead">Pero tenemos muchas otras. Vuelve al inicio o revisa nuestros equipos.</p>
<div class="hero-cta"><a class="btn btn-primary btn-lg" href="index.html">Ir al inicio</a><a class="btn btn-outline-light btn-lg" href="equipos.html">Ver equipos</a></div></div></section>'''
    page("404.html", "Página no encontrada | Santander Equipos", "La página que buscas no existe.", body)


def build_meta():
    pages = ["", "equipos.html", "nosotros.html", "calidad.html", "contacto.html"] + [f"equipo-{p['slug']}.html" for p in PRODUCTS]
    today = date.today().isoformat()
    urls = "".join(f"<url><loc>{SITE}/{u}</loc><lastmod>{today}</lastmod></url>" for u in pages)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    build_home(); build_equipos(); build_nosotros(); build_calidad(); build_contacto(); build_404()
    for p in PRODUCTS:
        build_product(p)
    build_meta()
    print("Sitio generado en", OUT)
