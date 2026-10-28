/* Inicio: resumen leído de las demás secciones (solo lectura) y pendientes propios. */
(function () {
  'use strict';
  var h = W.h;

  function kpi(i, href, etiqueta, numero, detalle, progreso) {
    var barra = null;
    if (progreso !== null && progreso !== undefined) {
      barra = h('i');
      requestAnimationFrame(function () { requestAnimationFrame(function () { barra.style.width = Math.max(0, Math.min(100, progreso)) + '%'; }); });
    }
    return h('a', { class: 'kpi aparece', href: href, style: '--i:' + i },
      h('div', { class: 'bisel' }, h('div', { class: 'nucleo' },
        h('span', { class: 'pill' }, etiqueta),
        h('div', { class: 'num' }, numero),
        h('div', { class: 'detalle' }, detalle),
        barra ? h('div', { class: 'barra' }, barra) : null)));
  }

  function leer(c) { return W.datos.lista(c).catch(function () { return []; }); }

  W.iniciar(function (main) {
    var kpis = h('div', { class: 'rejilla' });
    var pend = h('div', { class: 'nucleo' }, h('h2', { class: 't' }, 'Pendientes'));
    main.append(
      h('p', { class: 'apoyo', style: 'margin:0 0 1.25rem' }, 'Hoy es ' + W.fecha(W.hoy()) + '.'),
      kpis,
      h('div', { class: 'bloque' }, h('div', { class: 'bisel' }, pend)),
      h('p', { class: 'apoyo', style: 'margin-top:2rem' }, 'Los datos de la tienda, el contenido y los pendientes iniciales son de ejemplo: edítalos o elimínalos desde su sección.'));

    W.pendientes({ coleccion: 'tareas', contenedor: pend, placeholder: 'Nuevo pendiente de la semana' });

    Promise.all(['documentos', 'lineas', 'tienda', 'contenido', 'contenido-ritmo', 'sitios', 'web-pendientes'].map(leer)).then(function (r) {
      var docs = r[0], lineas = r[1], tienda = r[2], contenido = r[3], ritmo = r[4], sitios = r[5], wpend = r[6];

      var listos = docs.filter(function (d) { return d.estado === 'Implementado'; }).length;
      var revisar = docs.filter(function (d) { return d.estado === 'Por revisar'; }).length;
      kpis.append(kpi(0, '/documentos/', 'Documentos', listos + ' de ' + docs.length,
        revisar ? revisar + ' por revisar antes de usarse con un cliente.' : 'Sin documentos por revisar.',
        docs.length ? listos / docs.length * 100 : 0));

      kpis.append(kpi(1, '/lineas/', 'Líneas', String(lineas.length),
        lineas.map(function (l) { return l.nombre; }).join(', ') || 'Aún sin líneas.'));

      var disp = tienda.filter(function (p) { return p.estado === 'Disponible'; }).length;
      kpis.append(kpi(2, '/tienda/', 'Tienda', String(tienda.length), disp + ' disponibles de ' + tienda.length + ' piezas.',
        tienda.length ? disp / tienda.length * 100 : 0));

      var semana = W.inicioSemana(W.hoy());
      var meta = ritmo.filter(function (x) { return x.cuenta === '@derstahlbeton'; })[0];
      var objetivo = meta && meta.porSemana ? Number(meta.porSemana) : 0;
      var hechas = contenido.filter(function (p) {
        return p.cuenta === '@derstahlbeton' && p.estado === 'Publicada' && p.tipo !== 'Historia' && W.inicioSemana(p.fecha) === semana;
      }).length;
      kpis.append(kpi(3, '/contenido/', 'Contenido', objetivo ? hechas + ' de ' + objetivo : String(hechas),
        'Publicaciones de @derstahlbeton esta semana.', objetivo ? hechas / objetivo * 100 : null));

      var publicados = sitios.filter(function (s) { return s.estado === 'Publicado'; }).length;
      var abiertos = wpend.filter(function (p) { return p.estado !== 'Hecho'; }).length;
      kpis.append(kpi(4, '/web/', 'Web', publicados + ' de ' + sitios.length,
        abiertos + (abiertos === 1 ? ' pendiente abierto.' : ' pendientes abiertos.'),
        sitios.length ? publicados / sitios.length * 100 : 0));
    });
  });
})();
