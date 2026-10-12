/* Tienda de Werkstatt, borrador. Lee window.TIENDA (productos.js), generado desde la tabla de productos.
   El botón y su enlace vienen de la tabla (columnas Botón y Enlace del botón); aquí no se decide nada de negocio. */
(function () {
  "use strict";
  var T = window.TIENDA || { familias: [], productos: [], correo: "" };
  var P = T.productos || [];
  var rm = matchMedia("(prefers-reduced-motion: reduce)").matches;
  var root = document.documentElement;
  var hasIO = "IntersectionObserver" in window;
  var $ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var ease = function (t) { return t >= 1 ? 1 : 1 - Math.pow(2, -10 * t); };
  var MXN = new Intl.NumberFormat("es-MX", { style: "currency", currency: "MXN", maximumFractionDigits: 0 });
  var ICO = '<span class="ico"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4.5 11.5 11.5 4.5M5.5 4.5h6v6"/></svg></span>';

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  /* ---------- A-01: aparición al entrar ---------- */
  var io = null;
  if (hasIO && !rm) {
    root.classList.add("js");
    io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add("in");
        io.unobserve(e.target);
      });
    }, { threshold: 0.15, rootMargin: "0px 0px -6% 0px" });
  }
  function reveal(scope) {
    $(".reveal", scope).forEach(function (el) {
      if (io && !el.classList.contains("in")) io.observe(el); else el.classList.add("in");
    });
  }

  /* ---------- N-05: contadores ---------- */
  function count(el) {
    var to = parseFloat(el.dataset.count) || 0, t0 = null;
    if (rm) { el.textContent = to; return; }
    el.textContent = "0";
    function f(t) {
      if (!t0) t0 = t;
      var p = Math.min((t - t0) / 1600, 1);
      el.textContent = Math.round(to * ease(p));
      if (p < 1) requestAnimationFrame(f);
    }
    requestAnimationFrame(f);
  }
  function counters() {
    var els = $("[data-count]");
    if (!hasIO) { els.forEach(function (e) { e.textContent = e.dataset.count; }); return; }
    var co = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { count(e.target); co.unobserve(e.target); } });
    }, { threshold: 0.6 });
    els.forEach(function (el) { co.observe(el); });
  }

  /* ---------- B-03: botón magnético ---------- */
  function mag(b) {
    if (rm || b.__mag) return;
    b.__mag = true;
    b.addEventListener("pointermove", function (e) {
      var r = b.getBoundingClientRect();
      b.style.transform = "translate(" + ((e.clientX - r.left - r.width / 2) * 0.25) + "px," + ((e.clientY - r.top - r.height / 2) * 0.35) + "px)";
    });
    b.addEventListener("pointerleave", function () { b.style.transform = ""; });
  }

  /* ---------- Aviso breve (enlaces de pago de ejemplo) ---------- */
  var toast = null, toastTimer = 0;
  function say(msg) {
    if (!toast) {
      toast = document.createElement("div");
      toast.className = "toast";
      toast.setAttribute("role", "status");
      document.body.appendChild(toast);
    }
    toast.textContent = msg;
    void toast.offsetWidth;
    toast.classList.add("on");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toast.classList.remove("on"); }, 3600);
  }
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("[data-demo]");
    if (!a) return;
    e.preventDefault();
    say("Enlace de pago de ejemplo: aquí iría el pago de la pieza.");
  });

  /* ---------- Piezas ---------- */
  function etiqueta(p) {
    if (p.estado === "Disponible" && p.venta === "Mensaje") return "Por mensaje";
    return p.estado || "Por definir";
  }
  function btn(p) {
    var texto = p.boton || "Por definir";
    if (!p.enlace) {
      return '<button class="btn off" type="button" disabled>' + esc(texto) + ICO + "</button>";
    }
    var demo = /^https?:\/\/example\.com/.test(p.enlace);
    return '<a class="btn" href="' + esc(p.enlace) + '"' + (demo ? ' data-demo="pago"' : "") + " data-mag>" + esc(texto) + ICO + "</a>";
  }
  function card(p, i) {
    var m = p.venta === "Mensaje";
    var cap = esc(p.familiaNombre) + (p.precio != null ? " · " + MXN.format(p.precio) : "");
    return '<article class="bezel' + (m ? " sage" : "") + ' card reveal" style="--i:' + (i % 6) + '"><div class="core">' +
      '<div class="ph" role="img" aria-label="Foto pendiente de ' + esc(p.codigo) + '">Foto pendiente</div>' +
      '<div class="row"><b class="pn">' + esc(p.codigo) + '</b><span class="tag">' + esc(etiqueta(p)) + "</span></div>" +
      '<h3><a href="producto.html?c=' + encodeURIComponent(p.codigo) + '">' + esc(p.nombre || "Por definir") + "</a></h3>" +
      '<p class="cap">' + cap + "</p>" +
      "</div></article>";
  }

  function initIndex() {
    var chips = document.getElementById("chips"), grid = document.getElementById("cards");
    var fam = "*";
    var nd = P.filter(function (p) { return p.venta === "Directa"; }).length;
    var nm = P.filter(function (p) { return p.venta === "Mensaje"; }).length;
    [["s-total", P.length], ["s-directa", nd], ["s-mensaje", nm]].forEach(function (x) {
      var el = document.getElementById(x[0]);
      if (el) { el.dataset.count = x[1]; el.textContent = x[1]; }
    });
    var bleed = document.getElementById("bleed");
    if (bleed) bleed.textContent = P.length;

    var opts = [{ letra: "*", nombre: "Todas", n: P.length }].concat((T.familias || []).map(function (f) {
      return { letra: f.letra, nombre: f.nombre, n: P.filter(function (p) { return p.familia === f.letra; }).length };
    }));
    chips.innerHTML = opts.map(function (o, i) {
      return '<button type="button" data-fam="' + esc(o.letra) + '" aria-pressed="' + (i === 0) + '">' + esc(o.nombre) + "<small>" + o.n + "</small></button>";
    }).join("");

    function draw() {
      var list = P.filter(function (p) { return fam === "*" || p.familia === fam; });
      grid.innerHTML = list.length ? list.map(card).join("") : '<p class="empty">No hay piezas en esta familia.</p>';
      reveal(grid);
    }
    chips.addEventListener("click", function (e) {
      var b = e.target.closest("button[data-fam]");
      if (!b) return;
      fam = b.dataset.fam;
      $("button", chips).forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      draw();
    });
    draw();
  }

  function nota(p) {
    switch (p.boton) {
      case "Comprar": return "Te lleva al enlace de pago.";
      case "Consultar": return "Se abre un correo con el código " + p.codigo + " en el asunto.";
      case "Avísame": return "Se abre un correo con el código " + p.codigo + " en el asunto; te aviso cuando esté lista.";
      case "Agotado": return "Esta pieza está agotada por ahora.";
      default: return "Esta pieza todavía no tiene los datos completos.";
    }
  }

  function initFicha() {
    var host = document.getElementById("ficha");
    var c = (new URLSearchParams(location.search).get("c") || "").toUpperCase();
    var p = P.filter(function (x) { return String(x.codigo).toUpperCase() === c; })[0];
    if (!p) {
      host.innerHTML = '<div class="bezel gal"><div class="core"><h3>No encontré esa pieza.</h3><p>Revisa el código o vuelve a las piezas.</p></div></div>';
      return;
    }
    document.title = "Werkstatt | " + (p.nombre || p.codigo) + " (" + p.codigo + ")";
    var filas = "";
    if (p.materiales) filas += "<div><dt>Materiales</dt><dd>" + esc(p.materiales) + "</dd></div>";
    if (p.tallas) filas += "<div><dt>Tallas o medidas</dt><dd>" + esc(p.tallas) + "</dd></div>";
    filas += "<div><dt>Estado</dt><dd>" + esc(p.estado || "Por definir") + "</dd></div>";
    filas += "<div><dt>Venta</dt><dd>" + (p.venta === "Mensaje" ? "Por mensaje" : p.venta === "Directa" ? "Compra directa" : "Por definir") + "</dd></div>";
    var precio = p.precio != null
      ? '<p class="price">' + MXN.format(p.precio) + "<small>MXN</small></p>"
      : (p.venta === "Mensaje" ? '<p class="price"><small>Precio por mensaje</small></p>' : "");
    host.innerHTML =
      '<div class="gal reveal"><div class="bezel"><div class="core"><div class="ph" role="img" aria-label="Foto pendiente de ' + esc(p.codigo) + '">Foto pendiente</div></div></div>' +
      '<div class="thumbs" aria-hidden="true"><div class="ph">Foto 2</div><div class="ph">Foto 3</div><div class="ph">Foto 4</div></div></div>' +
      '<div class="info reveal"><div class="meta"><b class="pn">' + esc(p.codigo) + '</b><span class="tag">' + esc(p.familiaNombre) + '</span><span class="tag">' + esc(etiqueta(p)) + "</span></div>" +
      "<h1>" + esc(p.nombre || "Por definir") + "</h1>" +
      (p.descripcion ? '<p class="lead">' + esc(p.descripcion) + "</p>" : "") +
      '<dl class="spec">' + filas + "</dl>" + precio + btn(p) +
      '<p class="note">' + esc(nota(p)) + "</p></div>";
    $("[data-mag]", host).forEach(mag);
    reveal(host);

    var otras = P.filter(function (x) { return x.familia === p.familia && x.codigo !== p.codigo; }).slice(0, 3);
    if (otras.length) {
      var sec = document.getElementById("mas"), cards = document.getElementById("cards");
      var t = document.getElementById("mas-t");
      if (t) t.textContent = "También en " + p.familiaNombre.toLowerCase() + ".";
      cards.innerHTML = otras.map(card).join("");
      sec.hidden = false;
      reveal(sec);
    }
  }

  /* ---------- T-04: revelado por letras en el titular ---------- */
  try {
    var h = document.querySelector(".hero h1");
    if (h && !rm) {
      h.setAttribute("aria-label", h.textContent.replace(/\s+/g, " ").trim());
      var n = 0;
      (function walk(node) {
        Array.prototype.slice.call(node.childNodes).forEach(function (c) {
          if (c.nodeType === 3) {
            var f = document.createDocumentFragment();
            c.textContent.split(/(\s+)/).forEach(function (part) {
              if (!part) return;
              if (/^\s+$/.test(part)) { f.appendChild(document.createTextNode(" ")); return; }
              var w = document.createElement("span");
              w.className = "wd"; w.setAttribute("aria-hidden", "true");
              part.split("").forEach(function (ch) {
                var l = document.createElement("span");
                l.className = "l"; l.style.setProperty("--i", n++); l.textContent = ch;
                w.appendChild(l);
              });
              f.appendChild(w);
            });
            node.replaceChild(f, c);
          } else if (c.nodeType === 1) { walk(c); }
        });
      })(h);
      root.classList.add("letters-on");
      requestAnimationFrame(function () { requestAnimationFrame(function () { root.classList.add("letters-go"); }); });
    }
  } catch (e) { root.classList.remove("letters-on"); }

  /* ---------- A-08: el número de la portada responde al cursor ---------- */
  var hero = document.querySelector(".hero");
  if (hero && !rm) {
    hero.addEventListener("pointermove", function (e) {
      var r = hero.getBoundingClientRect();
      hero.style.setProperty("--dx", ((e.clientX - r.left) / r.width - 0.5) * 2);
      hero.style.setProperty("--dy", ((e.clientY - r.top) / r.height - 0.5) * 2);
    });
    hero.addEventListener("pointerleave", function () { hero.style.setProperty("--dx", 0); hero.style.setProperty("--dy", 0); });
  }

  /* ---------- V-03: regla lateral en centímetros ---------- */
  var rl = document.querySelector(".ruler"), cm = document.getElementById("cm"), tick = false;
  function upd() {
    tick = false;
    var y = window.scrollY;
    rl.style.setProperty("--y", y + "px");
    cm.textContent = (y / 37.795).toFixed(1) + " cm";
  }
  if (rl && cm) {
    addEventListener("scroll", function () { if (!tick) { tick = true; requestAnimationFrame(upd); } }, { passive: true });
    upd();
  }

  /* ---------- Arranque ---------- */
  if (document.getElementById("chips")) initIndex();
  if (document.getElementById("ficha")) initFicha();
  $("[data-mag]").forEach(mag);
  reveal(document);
  counters();
})();
