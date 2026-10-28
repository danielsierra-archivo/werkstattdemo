/* Werkstatt Dashboard: núcleo compartido.
   Construye el menú a partir de las carpetas con seccion.json, y ofrece a cada sección
   un cliente de datos, utilidades y una tabla editable. Cada sección sigue siendo independiente. */
(function () {
  'use strict';

  /* ---------- utilidades ---------- */
  function h(tag, attrs) {
    var e = document.createElement(tag);
    var diferidos = {};
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        var v = attrs[k];
        if (v === null || v === undefined || v === false) return;
        if (k === 'class') e.className = v;
        else if (k === 'value' || k === 'checked' || k === 'disabled') diferidos[k] = v;
        else if (k.indexOf('on') === 0) e.addEventListener(k.slice(2), v);
        else e.setAttribute(k, v === true ? '' : v);
      });
    }
    for (var i = 2; i < arguments.length; i++) agregar(e, arguments[i]);
    Object.keys(diferidos).forEach(function (k) { e[k] = diferidos[k]; });
    return e;
  }
  function agregar(padre, hijo) {
    if (hijo === null || hijo === undefined || hijo === false) return;
    if (Array.isArray(hijo)) { hijo.forEach(function (x) { agregar(padre, x); }); return; }
    padre.append(hijo.nodeType ? hijo : document.createTextNode(String(hijo)));
  }

  var MESES = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'];
  function fecha(s) {
    var m = /^(\d{4})-(\d{2})-(\d{2})/.exec(s || '');
    if (!m) return s || '';
    return Number(m[3]) + ' ' + MESES[Number(m[2]) - 1] + ' ' + m[1];
  }
  function hoy() {
    var d = new Date(), p = function (n) { return String(n).padStart(2, '0'); };
    return d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate());
  }
  function inicioSemana(s) { // lunes de la semana de s (YYYY-MM-DD)
    var m = /^(\d{4})-(\d{2})-(\d{2})/.exec(s); if (!m) return null;
    var d = new Date(Number(m[1]), Number(m[2]) - 1, Number(m[3]));
    var dia = (d.getDay() + 6) % 7;
    d.setDate(d.getDate() - dia);
    var p = function (n) { return String(n).padStart(2, '0'); };
    return d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate());
  }
  function moneda(n) {
    if (n === null || n === undefined || n === '') return '';
    return Number(n).toLocaleString('es-MX', { style: 'currency', currency: 'MXN', maximumFractionDigits: 0 });
  }
  function urlSegura(u) { return /^https?:\/\//i.test(u || ''); }

  /* ---------- datos ---------- */
  function pedir(metodo, ruta, cuerpo) {
    var opciones = { method: metodo, headers: { 'X-Werkstatt': '1' } };
    if (cuerpo !== undefined) { opciones.headers['Content-Type'] = 'application/json'; opciones.body = JSON.stringify(cuerpo); }
    return fetch('/api' + ruta, opciones).then(function (r) {
      if (r.status === 204) return null;
      return r.json().catch(function () { return {}; }).then(function (j) {
        if (!r.ok) throw new Error(j.error || ('Error ' + r.status));
        return j;
      });
    });
  }
  var datos = {
    lista: function (c) { return pedir('GET', '/c/' + c); },
    crear: function (c, o) { return pedir('POST', '/c/' + c, o); },
    actualizar: function (c, id, o) { return pedir('PUT', '/c/' + c + '/' + id, o); },
    borrar: function (c, id) { return pedir('DELETE', '/c/' + c + '/' + id); }
  };

  /* ---------- avisos ---------- */
  var cajaAvisos;
  function aviso(texto, mal) {
    if (!cajaAvisos) { cajaAvisos = h('div', { class: 'avisos', role: 'status', 'aria-live': 'polite' }); document.body.append(cajaAvisos); }
    var a = h('div', { class: 'aviso' + (mal ? ' mal' : '') }, texto);
    cajaAvisos.append(a);
    setTimeout(function () { a.remove(); }, mal ? 6000 : 3200);
  }
  function fallo(e) { aviso(e && e.message ? e.message : 'Algo falló.', true); }

  /* ---------- tabla editable ---------- */
  function normalizar(opciones) {
    return (opciones || []).map(function (o) { return typeof o === 'string' ? { v: o } : o; });
  }
  function opcionDe(campo, valor) {
    return normalizar(campo.opciones).filter(function (o) { return o.v === valor; })[0];
  }

  function tabla(cfg) {
    var campos = cfg.campos;
    var porClave = {};
    campos.forEach(function (c) { porClave[c.k] = c; });
    var columnas = (cfg.columnas || campos.map(function (c) { return c.k; })).map(function (c) {
      return typeof c === 'string' ? { k: c } : c;
    });
    var estado = { lista: [], q: '', filtros: {} };
    var raiz = h('div', { class: 'crud' });
    var cuerpoTabla = h('tbody');
    var vacio = h('div', { class: 'vacio', hidden: true }, cfg.vacio || 'Sin registros todavía.');
    var buscar = h('input', { type: 'search', placeholder: 'Buscar', 'aria-label': 'Buscar', oninput: function (e) { estado.q = e.target.value.toLowerCase(); pintar(); } });
    var barra = h('div', { class: 'barra-filtros' }, buscar);
    (cfg.filtros || []).forEach(function (k) {
      var campo = porClave[k];
      var sel = h('select', { 'aria-label': campo.etiqueta, onchange: function (e) { estado.filtros[k] = e.target.value; pintar(); } },
        h('option', { value: '' }, campo.etiqueta + ': todos'),
        normalizar(campo.opciones).map(function (o) { return h('option', { value: o.v }, o.v); }));
      barra.append(sel);
    });
    barra.append(h('button', { class: 'btn espacio', type: 'button', onclick: function () { editar(null); } }, cfg.etiquetaAgregar || 'Agregar'));

    var tabla = h('table', { class: 'tabla' },
      h('thead', null, h('tr', null, columnas.map(function (c) {
        var campo = porClave[c.k] || {};
        return h('th', { class: campo.tipo === 'numero' ? 'num' : '' }, c.etiqueta || campo.etiqueta || c.k);
      }))), cuerpoTabla);
    raiz.append(barra, h('div', { class: 'tabla-caja' }, tabla), vacio);

    function coincide(fila) {
      for (var k in estado.filtros) { if (estado.filtros[k] && fila[k] !== estado.filtros[k]) return false; }
      if (!estado.q) return true;
      return Object.keys(fila).some(function (k) { return k !== 'id' && String(fila[k]).toLowerCase().indexOf(estado.q) >= 0; });
    }

    function celda(columna, fila) {
      var campo = porClave[columna.k] || {};
      var v = fila[columna.k];
      var td = h('td', { class: campo.tipo === 'numero' ? 'num' : '' });
      if (columna.render) { agregar(td, columna.render(v, fila)); return td; }
      if (v === undefined || v === null || v === '') return td;
      if (campo.tipo === 'select' && campo.pill !== false) {
        var op = opcionDe(campo, v);
        var tono = op && op.tono ? op.tono : 'idle';
        if (campo.ciclo) {
          agregar(td, h('button', { type: 'button', class: 'estado', 'data-tono': tono, title: 'Cambiar estado', onclick: function (e) { e.stopPropagation(); avanzar(fila, campo); } }, v));
        } else {
          agregar(td, h('span', { class: 'estado', 'data-tono': tono }, v));
        }
      } else if (campo.tipo === 'url') {
        agregar(td, urlSegura(v) ? h('a', { class: 'enlace', href: v, target: '_blank', rel: 'noopener noreferrer', onclick: function (e) { e.stopPropagation(); } }, 'Abrir') : v);
      } else if (campo.tipo === 'numero') {
        td.textContent = campo.formato === 'moneda' ? moneda(v) : String(v);
      } else if (campo.tipo === 'fecha') {
        td.textContent = fecha(v);
      } else if (campo.tipo === 'check') {
        td.textContent = v ? 'Sí' : '';
      } else {
        td.textContent = String(v);
        if (campo.tipo === 'area') td.className = 'recorte';
        if (campo.codigo) td.className = 'cod';
        if (campo.fuerte) td.className = 'fuerte';
      }
      return td;
    }

    function pintar() {
      var filas = estado.lista.filter(coincide);
      if (cfg.orden) filas = filas.slice().sort(cfg.orden);
      cuerpoTabla.replaceChildren.apply(cuerpoTabla, filas.map(function (fila) {
        return h('tr', { tabindex: '0', onclick: function () { editar(fila); }, onkeydown: function (e) { if (e.key === 'Enter') editar(fila); } },
          columnas.map(function (c) { return celda(c, fila); }));
      }));
      vacio.hidden = filas.length > 0;
      tabla.hidden = filas.length === 0;
    }

    function recargar() {
      return datos.lista(cfg.coleccion).then(function (l) { estado.lista = l; pintar(); if (cfg.alCambiar) cfg.alCambiar(l); }).catch(fallo);
    }

    function avanzar(fila, campo) {
      var ops = normalizar(campo.opciones);
      var i = ops.findIndex(function (o) { return o.v === fila[campo.k]; });
      var cambio = {}; cambio[campo.k] = ops[(i + 1) % ops.length].v;
      datos.actualizar(cfg.coleccion, fila.id, cambio).then(recargar).catch(fallo);
    }

    function editar(fila) {
      var nuevo = !fila;
      var valores = nuevo ? Object.assign({}, cfg.nuevo ? cfg.nuevo() : {}) : fila;
      var entradas = {};
      var dlg = h('dialog', { class: 'modal', 'aria-label': nuevo ? 'Agregar' : 'Editar' });
      var rejilla = h('div', { class: 'form-rejilla' });
      campos.forEach(function (c) {
        var v = valores[c.k]; if (v === undefined || v === null) v = '';
        var el;
        if (c.tipo === 'area') el = h('textarea', { id: 'f-' + c.k, value: v });
        else if (c.tipo === 'select') {
          el = h('select', { id: 'f-' + c.k }, h('option', { value: '' }, '—'), normalizar(c.opciones).map(function (o) { return h('option', { value: o.v }, o.v); }));
          el.value = v;
        } else if (c.tipo === 'check') el = h('input', { id: 'f-' + c.k, type: 'checkbox', checked: !!v });
        else el = h('input', { id: 'f-' + c.k, type: c.tipo === 'numero' ? 'number' : (c.tipo === 'fecha' ? 'date' : (c.tipo === 'url' ? 'url' : 'text')), step: c.tipo === 'numero' ? 'any' : null, value: v, required: c.req ? true : null });
        entradas[c.k] = el;
        var clases = 'campo' + ((c.tipo === 'area' || c.ancho) ? ' ancho' : '') + (c.tipo === 'check' ? ' marca-check' : '');
        rejilla.append(h('div', { class: clases }, c.tipo === 'check' ? [el, h('label', { for: 'f-' + c.k }, c.etiqueta)] : [h('label', { for: 'f-' + c.k }, c.etiqueta), el]));
      });
      var botonBorrar = null;
      if (!nuevo) {
        var armado = false;
        botonBorrar = h('button', { type: 'button', class: 'btn sec chico espacio', onclick: function () {
          if (!armado) { armado = true; botonBorrar.textContent = 'Confirmar eliminar'; botonBorrar.classList.add('peligro'); return; }
          datos.borrar(cfg.coleccion, fila.id).then(function () { dlg.close(); aviso('Eliminado'); return recargar(); }).catch(fallo);
        } }, 'Eliminar');
      }
      var forma = h('form', { method: 'dialog' },
        h('h3', null, nuevo ? (cfg.tituloNuevo || 'Agregar') : (cfg.tituloEditar || 'Editar')),
        rejilla,
        h('div', { class: 'acciones' },
          h('button', { type: 'submit', class: 'btn' }, 'Guardar'),
          h('button', { type: 'button', class: 'btn sec', onclick: function () { dlg.close(); } }, 'Cancelar'),
          botonBorrar));
      forma.addEventListener('submit', function (e) {
        e.preventDefault();
        var salida = {};
        campos.forEach(function (c) {
          var el = entradas[c.k];
          if (c.tipo === 'check') salida[c.k] = el.checked;
          else if (c.tipo === 'numero') salida[c.k] = el.value === '' ? null : Number(el.value);
          else salida[c.k] = el.value.trim();
        });
        var promesa = nuevo ? datos.crear(cfg.coleccion, salida) : datos.actualizar(cfg.coleccion, fila.id, salida);
        promesa.then(function () { dlg.close(); aviso('Guardado'); return recargar(); }).catch(fallo);
      });
      dlg.append(forma);
      document.body.append(dlg);
      if (typeof dlg.showModal === 'function') {
        dlg.showModal();
      } else { // Safari antiguo sin <dialog>
        dlg.setAttribute('open', '');
        dlg.style.cssText = 'position:fixed;top:5vh;left:50%;transform:translateX(-50%);z-index:60';
        dlg.close = function () { dlg.removeAttribute('open'); dlg.dispatchEvent(new Event('close')); };
      }
      dlg.addEventListener('close', function () { dlg.remove(); });
      dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
      var primero = rejilla.querySelector('input, select, textarea'); if (primero) primero.focus();
    }

    if (cfg.contenedor) cfg.contenedor.append(raiz);
    recargar();
    return { el: raiz, recargar: recargar, lista: function () { return estado.lista; } };
  }

  /* ---------- lista rápida (una línea de texto + casilla), para pendientes ---------- */
  function pendientes(cfg) {
    var raiz = h('div');
    var lista = h('div');
    var campo = h('input', { type: 'text', placeholder: cfg.placeholder || 'Nuevo pendiente', 'aria-label': 'Nuevo pendiente', maxlength: '300' });
    var formulario = h('form', { class: 'agregar-rapido', onsubmit: function (e) {
      e.preventDefault();
      var t = campo.value.trim(); if (!t) return;
      datos.crear(cfg.coleccion, { texto: t, hecho: false }).then(function () { campo.value = ''; return recargar(); }).catch(fallo);
    } }, campo, h('button', { class: 'btn', type: 'submit' }, 'Agregar'));
    raiz.append(formulario, lista);
    function recargar() {
      return datos.lista(cfg.coleccion).then(function (l) {
        l.sort(function (a, b) { return (a.hecho ? 1 : 0) - (b.hecho ? 1 : 0); });
        lista.replaceChildren.apply(lista, l.map(function (t) {
          return h('div', { style: 'display:flex;gap:.7rem;align-items:center;padding:.55rem 0;border-bottom:1px solid var(--anillo)' },
            h('input', { type: 'checkbox', checked: !!t.hecho, 'aria-label': 'Hecho', onchange: function (e) { datos.actualizar(cfg.coleccion, t.id, { hecho: e.target.checked }).then(recargar).catch(fallo); } }),
            h('span', { style: t.hecho ? 'text-decoration:line-through;color:var(--gris);flex:1' : 'flex:1' }, t.texto),
            h('button', { class: 'btn sec chico', type: 'button', onclick: function () { datos.borrar(cfg.coleccion, t.id).then(recargar).catch(fallo); } }, 'Quitar'));
        }));
        if (!l.length) lista.append(h('div', { class: 'vacio' }, 'Nada pendiente.'));
        if (cfg.alCambiar) cfg.alCambiar(l);
      }).catch(fallo);
    }
    if (cfg.contenedor) cfg.contenedor.append(raiz);
    recargar();
    return { el: raiz, recargar: recargar };
  }

  /* ---------- armazón: menú, cabecera ---------- */
  var cola = [];
  var listo = false;
  var principal = null;

  function armar() {
    principal = document.getElementById('contenido');
    var idActual = document.body.getAttribute('data-seccion');
    var nav = h('nav', { class: 'nav', 'aria-label': 'Secciones' });
    var lateral = h('aside', { class: 'lateral' },
      h('a', { class: 'marca', href: '/inicio/', 'aria-label': 'Werkstatt Dashboard' }, h('img', { src: '/shared/logo/werkstatt-positivo.svg', alt: 'Werkstatt' })),
      h('span', { class: 'pill rotulo' }, 'Dashboard'),
      nav,
      h('div', { class: 'pie' },
        h('button', { class: 'btn sec chico', type: 'button', onclick: function () {
          pedir('POST', '/respaldo', {}).then(function (r) { aviso('Respaldo en ' + r.carpeta); }).catch(fallo);
        } }, 'Respaldar datos'),
        h('a', { class: 'btn sec chico', href: '/api/exportar', download: '' }, 'Exportar todo')),
      h('p', { class: 'nota' }, 'Uso interno. Los datos viven solo en esta computadora.'));
    var cabecera = h('header', { class: 'cabecera aparece' });
    var app = h('div', { class: 'app' }, lateral);
    principal.classList.add('contenido');
    principal.parentNode.insertBefore(app, principal);
    app.append(principal);
    principal.prepend(cabecera);
    // el contenido de la sección va dentro de un contenedor propio, debajo de la cabecera
    var cuerpo = h('div', { id: 'cuerpo' });
    principal.append(cuerpo);
    W.main = cuerpo;

    return fetch('/api/secciones').then(function (r) { return r.json(); }).then(function (secciones) {
      secciones.forEach(function (s, i) {
        var a = h('a', { href: '/' + s.id + '/' }, h('span', { class: 'n' }, String(i + 1).padStart(2, '0')), s.titulo);
        if (s.id === idActual) a.setAttribute('aria-current', 'page');
        nav.append(a);
        if (s.id === idActual) {
          document.title = s.titulo + ' · Werkstatt Dashboard';
          cabecera.append(h('span', { class: 'pill' }, 'Sección ' + String(i + 1).padStart(2, '0')), h('h1', null, s.titulo), s.descripcion ? h('p', null, s.descripcion) : null);
        }
      });
    }).catch(function () { fallo(new Error('No se pudo cargar el menú.')); });
  }

  var W = {
    h: h, agregar: agregar, fecha: fecha, hoy: hoy, inicioSemana: inicioSemana, moneda: moneda,
    datos: datos, aviso: aviso, fallo: fallo, tabla: tabla, pendientes: pendientes,
    main: null,
    iniciar: function (fn) { if (listo) fn(W.main); else cola.push(fn); }
  };
  window.W = W;

  function arrancar() {
    armar().then(function () {
      listo = true;
      cola.splice(0).forEach(function (fn) { try { fn(W.main); } catch (e) { fallo(e); } });
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', arrancar); else arrancar();
})();
