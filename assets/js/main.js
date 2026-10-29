/* Santander Equipos — interacciones */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.remove("no-js");
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var PHONE = "56995586223";
  var fmt = function (n) { return Math.round(n).toLocaleString("es-CL"); };

  // Header con sombra al hacer scroll
  var header = $(".site-header");
  var onScroll = function () { if (header) header.classList.toggle("scrolled", window.scrollY > 8); };
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();

  // Menú móvil
  var menuBtn = $(".menu-btn");
  if (menuBtn) {
    var closeMenu = function () { document.body.classList.remove("nav-open"); menuBtn.setAttribute("aria-expanded", "false"); menuBtn.setAttribute("aria-label", "Abrir menú"); };
    menuBtn.addEventListener("click", function () {
      var open = document.body.classList.toggle("nav-open");
      menuBtn.setAttribute("aria-expanded", String(open));
      menuBtn.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú");
    });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeMenu(); });
    document.addEventListener("click", function (e) {
      if (document.body.classList.contains("nav-open") && !e.target.closest(".main-nav") && !e.target.closest(".menu-btn")) closeMenu();
    });
  }
  $$(".sub-toggle").forEach(function (b) {
    b.addEventListener("click", function () {
      var sub = b.nextElementSibling, open = sub.classList.toggle("open");
      b.setAttribute("aria-expanded", String(open));
    });
  });

  // Aparición al hacer scroll
  var reveals = $$(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else { reveals.forEach(function (el) { el.classList.add("in"); }); }

  // Contadores
  var years = $("[data-years]");
  if (years) years.textContent = "+" + (new Date().getFullYear() - 2009);
  var counters = $$("[data-count]");
  if (counters.length && "IntersectionObserver" in window && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var co = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target, end = +el.dataset.count, t0 = performance.now(), dur = 1400;
        (function tick(t) {
          var p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3);
          el.textContent = fmt(end * e);
          if (p < 1) requestAnimationFrame(tick);
        })(t0);
        co.unobserve(el);
      });
    }, { threshold: 0.6 });
    counters.forEach(function (el) { co.observe(el); });
  }

  // Filtro de catálogo
  $$(".chips").forEach(function (group) {
    var grid = group.nextElementSibling;
    group.addEventListener("click", function (e) {
      var chip = e.target.closest(".chip"); if (!chip) return;
      $$(".chip", group).forEach(function (c) { c.classList.toggle("is-on", c === chip); c.setAttribute("aria-pressed", String(c === chip)); });
      var f = chip.dataset.filter;
      $$(".p-card", grid).forEach(function (card) {
        var show = f === "all" || card.dataset.tags.split(" ").indexOf(f) > -1;
        card.classList.toggle("is-hidden", !show);
        if (show) card.classList.add("in");
      });
    });
  });

  // Anatomía interactiva
  var spots = $$(".spot"), items = $$(".an-list li");
  var setSpot = function (i) {
    spots.forEach(function (s) { s.classList.toggle("is-on", +s.dataset.i === i); });
    items.forEach(function (li) { li.classList.toggle("is-on", +li.dataset.i === i); });
  };
  spots.forEach(function (s) { s.addEventListener("click", function () { setSpot(+s.dataset.i); }); });
  items.forEach(function (li) { $("button", li).addEventListener("click", function () { setSpot(+li.dataset.i); }); });
  if (spots.length) setSpot(0);

  // Simulador de carga útil
  var calc = $(".calc");
  if (calc) {
    var g = function (id) { return $("#" + id); };
    var run = function () {
      var kg = +g("c-kg").value, trips = +g("c-trips").value, rate = +g("c-rate").value, units = +g("c-units").value;
      g("o-kg").textContent = fmt(kg) + " kg";
      g("o-trips").textContent = trips;
      g("o-rate").textContent = "$" + fmt(rate);
      g("o-units").textContent = units;
      var tons = kg * trips * 12 * units / 1000;
      g("r-ton").textContent = fmt(tons) + " t";
      g("r-clp").textContent = "$" + fmt(tons * rate);
    };
    $$("input", calc).forEach(function (i) { i.addEventListener("input", run); });
    run();
  }

  // Videos de YouTube (se cargan al hacer clic)
  $$(".yt").forEach(function (b) {
    b.addEventListener("click", function () {
      var f = document.createElement("iframe");
      f.src = "https://www.youtube-nocookie.com/embed/" + b.dataset.id + "?autoplay=1&rel=0";
      f.title = b.getAttribute("aria-label");
      f.allow = "accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture";
      f.allowFullscreen = true;
      b.innerHTML = ""; b.appendChild(f);
    }, { once: true });
  });

  // Galería de producto
  var main = $("#g-main");
  $$(".thumb").forEach(function (t) {
    t.addEventListener("click", function () {
      main.style.opacity = 0;
      setTimeout(function () { main.src = t.dataset.src; main.style.opacity = 1; }, 150);
      $$(".thumb").forEach(function (x) { x.classList.toggle("is-on", x === t); });
    });
  });

  // Pestañas de especificaciones
  $$("[role=tablist]").forEach(function (list) {
    var tabs = $$("[role=tab]", list);
    var select = function (tab) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.classList.toggle("is-on", on); t.setAttribute("aria-selected", String(on)); t.tabIndex = on ? 0 : -1;
        document.getElementById(t.getAttribute("aria-controls")).hidden = !on;
      });
    };
    tabs.forEach(function (t, i) {
      t.tabIndex = i === 0 ? 0 : -1;
      t.addEventListener("click", function () { select(t); });
      t.addEventListener("keydown", function (e) {
        var d = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
        if (d) { var n = tabs[(i + d + tabs.length) % tabs.length]; select(n); n.focus(); }
      });
    });
  });

  // Lightbox
  var lb = $(".lightbox");
  if (lb) {
    var lbImg = $("img", lb), lbCap = $("p", lb), last;
    var closeLb = function () { lb.hidden = true; if (last) last.focus(); };
    $$("[data-lightbox]").forEach(function (b) {
      b.addEventListener("click", function () {
        last = b; lbImg.src = b.dataset.lightbox; lbImg.alt = b.dataset.caption || ""; lbCap.textContent = b.dataset.caption || "";
        lb.hidden = false; $(".lb-close", lb).focus();
      });
    });
    lb.addEventListener("click", function (e) { if (e.target === lb || e.target.closest(".lb-close")) closeLb(); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !lb.hidden) closeLb(); });
  }

  // Formulario de cotización -> WhatsApp
  var form = $("#quote");
  if (form) {
    var params = new URLSearchParams(location.search);
    if (params.get("equipo")) form.equipo.value = params.get("equipo");
    var tipo = params.get("tipo");
    if (tipo) {
      var map = { carroceria: "Carrocería", reparacion: "Reparación" };
      $$("input[name=tipo]", form).forEach(function (r) { r.checked = r.value === map[tipo]; });
    }
    var eqField = $(".eq-field", form);
    var syncTipo = function () { eqField.style.display = form.tipo.value === "Semirremolque" ? "" : "none"; };
    $$("input[name=tipo]", form).forEach(function (r) { r.addEventListener("change", syncTipo); });
    syncTipo();
    var msg = $(".form-msg", form);
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = true;
      ["nombre", "telefono"].forEach(function (n) {
        var f = form[n], bad = !f.value.trim();
        f.classList.toggle("invalid", bad); if (bad && ok) { f.focus(); ok = false; }
      });
      if (!ok) { msg.textContent = "Completa tu nombre y teléfono para continuar."; msg.className = "form-msg err"; return; }
      var eqSel = form.equipo, eqName = eqSel.value ? eqSel.options[eqSel.selectedIndex].text : "";
      var lines = [
        "Hola Santander Equipos, quiero solicitar una cotización.",
        "• Tipo: " + form.tipo.value,
        form.tipo.value === "Semirremolque" && eqName ? "• Equipo: " + eqName : "",
        "• Cantidad: " + (form.cantidad.value || 1),
        "• Nombre: " + form.nombre.value.trim(),
        form.empresa.value.trim() ? "• Empresa: " + form.empresa.value.trim() : "",
        "• Teléfono: " + form.telefono.value.trim(),
        form.correo.value.trim() ? "• Correo: " + form.correo.value.trim() : "",
        form.mensaje.value.trim() ? "• Detalle: " + form.mensaje.value.trim() : ""
      ].filter(Boolean).join("\n");
      msg.textContent = "¡Listo! Abriendo WhatsApp con tu solicitud…"; msg.className = "form-msg";
      window.open("https://wa.me/" + PHONE + "?text=" + encodeURIComponent(lines), "_blank", "noopener");
    });
  }
})();
