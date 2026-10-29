"""Genera imágenes WebP optimizadas y PDFs comprimidos para el sitio nuevo (docs/)."""
import shutil, zlib
from pathlib import Path
from PIL import Image
import pikepdf
from pikepdf import PdfImage, Name

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets"
OUT = ROOT / "docs" / "assets"
IMG = OUT / "img"; PDF = OUT / "pdf"
IMG.mkdir(parents=True, exist_ok=True); PDF.mkdir(parents=True, exist_ok=True)

def webp(src, dst, crop=None, size=None, q=82):
    im = Image.open(SRC / "images" / src)
    im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB")
    if crop: im = im.crop(crop)
    if size: im.thumbnail(size, Image.LANCZOS)
    im.save(IMG / dst, "WEBP", quality=q, method=6)

# Portadas de producto: se recorta la franja inferior con el logo para una imagen limpia
covers = {"minero": "minero.jpg", "speed-sider": "speed-sider-portada.jpg", "plano": "Plano.jpg",
          "forestal": "Forestal.jpg", "carga-seca": "Semi-Remolque-Carga-Seca.jpg",
          "botellero": "semirremolque-Botellero.jpg"}
for slug, f in covers.items():
    webp(f, f"{slug}.webp", crop=(0, 0, 700, 300))
for f in ["sider01", "sider02", "srbt1", "srbt2", "srf1", "srf2"]:
    webp(f + ".jpg", f + ".webp")
for f in ["daf2", "faw2", "hino2", "scania2", "international2"]:
    webp(f + ".png", f.replace("2", "") + ".webp", q=90)
webp("equiposportada.png", "flota.webp", q=85)
webp("fondo-blog.jpg", "ruta.webp", q=70)
webp("CamScanner-03-02-2023-12.44.jpg", "premio-swedish-steel-prize-2014.webp", size=(700, 1000))
webp("CamScanner-03-02-2023-12.45-1.jpg", "certificado-my-inner-strenx.webp", size=(700, 1000))
webp("CamScanner-03-02-2023-12.45-2.jpg", "certificado-iso-9001.webp", size=(700, 1000))
for f in ["Logo.png", "favicon.png", "favicon-32x32.png", "favicon-180x180.png", "favicon-192x192.png"]:
    shutil.copy(SRC / "logo" / f, IMG / f.lower())

# Logo en blanco para fondos oscuros
lg = Image.open(SRC / "logo" / "Logo.png").convert("RGBA")
r, g, b, a = lg.split()
lum = Image.merge("RGB", (r, g, b)).convert("L")
alpha = Image.eval(lum, lambda v: 255 - v)  # oscuro -> opaco
from PIL import ImageChops
alpha = ImageChops.multiply(alpha, a)
alpha = Image.eval(alpha, lambda v: min(255, int(v * 1.6)))
white = Image.new("RGBA", lg.size, (255, 255, 255, 0)); white.putalpha(alpha)
white.save(IMG / "logo-blanco.png")

def compress_pdf(src, dst, max_px=1600, q=68):
    pdf = pikepdf.open(src)
    # Quita los datos privados de Illustrator (PieceInfo), que no se ven pero pesan MB
    for d in [pdf.Root] + [pg.obj for pg in pdf.pages]:
        if "/PieceInfo" in d: del d["/PieceInfo"]
    for page in pdf.pages:
        for name, raw in list(page.images.items()):
            try:
                pimg = PdfImage(raw)
                if raw.get("/SMask") is not None or raw.get("/ImageMask"):
                    continue
                im = pimg.as_pil_image()
                if im.mode not in ("RGB", "L"): im = im.convert("RGB")
                im.thumbnail((max_px, max_px), Image.LANCZOS)
                import io
                buf = io.BytesIO(); im.save(buf, "JPEG", quality=q, optimize=True)
                new = buf.getvalue()
                if len(new) >= len(raw.read_raw_bytes()):
                    continue
                raw.write(new, filter=Name.DCTDecode)
                raw.Width, raw.Height = im.size
                raw.ColorSpace = Name.DeviceRGB if im.mode == "RGB" else Name.DeviceGray
                raw.BitsPerComponent = 8
                for k in ("/DecodeParms", "/Decode"):
                    if k in raw: del raw[k]
            except Exception as e:
                print("  skip", name, e)
    pdf.save(dst, compress_streams=True, object_stream_mode=pikepdf.ObjectStreamMode.generate)

for p in sorted((SRC / "pdfs").glob("*.pdf")):
    dst = PDF / p.name
    if p.stat().st_size > 1_000_000:
        compress_pdf(p, dst)
        if dst.stat().st_size >= p.stat().st_size: shutil.copy(p, dst)
    else:
        shutil.copy(p, dst)
    print(f"{p.name}: {p.stat().st_size//1024} KB -> {dst.stat().st_size//1024} KB")
