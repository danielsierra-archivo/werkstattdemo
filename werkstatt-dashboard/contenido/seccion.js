/* Contenido: calendario de publicaciones y ritmo por cuenta de Instagram. */
(function () {
  'use strict';
  var h = W.h;

  var CUENTAS = ['@derstahlbeton', '@rohesarchiv'];
  var PUBLICACIONES = [
    { k: 'fecha', etiqueta: 'Fecha', tipo: 'fecha', req: true },
    { k: 'cuenta', etiqueta: 'Cuenta', tipo: 'select', pill: false, opciones: CUENTAS },
    { k: 'tipo', etiqueta: 'Tipo', tipo: 'select', pill: false, opciones: ['Publicación', 'Carrusel', 'Reel', 'Historia'] },
    { k: 'titulo', etiqueta: 'Título o idea', tipo: 'texto', req: true, fuerte: true },
    { k: 'estado', etiqueta: 'Estado', tipo: 'select', ciclo: true, opciones: [
      { v: 'Idea', tono: 'idle' }, { v: 'En preparación', tono: 'curso' }, { v: 'Programada', tono: 'curso' }, { v: 'Publicada', tono: 'ok' }] },
    { k: 'nota', etiqueta: 'Nota', tipo: 'area' }
  ];
  var RITMO = [
    { k: 'cuenta', etiqueta: 'Cuenta', tipo: 'texto', req: true, fuerte: true },
    { k: 'porSemana', etiqueta: 'Publicaciones por semana', tipo: 'numero' },
    { k: 'porMes', etiqueta: 'Publicaciones por mes', tipo: 'numero' },
    { k: 'historiasDia', etiqueta: 'Historias por día', tipo: 'numero' },
    { k: 'nota', etiqueta: 'Nota', tipo: 'area' }
  ];

  var estado = { pubs: [], ritmo: [] };
  var tarjetas;

  function hechas(pubs, cuenta, desde, comparar) {
    return pubs.filter(function (p) {
      return p.cuenta === cuenta && p.estado === 'Publicada' && p.tipo !== 'Historia' && comparar(p.fecha);
    }).length;
  }

  function pintarRitmo() {
    var semana = W.inicioSemana(W.hoy());
    var mes = W.hoy().slice(0, 7);
    tarjetas.replaceChildren.apply(tarjetas, estado.ritmo.map(function (r, i) {
      var objetivo, hecho, periodo;
      if (r.porSemana) {
        objetivo = Number(r.porSemana); periodo = 'esta semana';
        hecho = hechas(estado.pubs, r.cuenta, null, function (f) { return W.inicioSemana(f) === semana; });
      } else if (r.porMes) {
        objetivo = Number(r.porMes); periodo = 'este mes';
        hecho = hechas(estado.pubs, r.cuenta, null, function (f) { return (f || '').slice(0, 7) === mes; });
      }
      var barra = h('i');
      if (objetivo) requestAnimationFrame(function () { requestAnimationFrame(function () { barra.style.width = Math.min(100, hecho / objetivo * 100) + '%'; }); });
      return h('div', { class: 'bisel aparece', style: '--i:' + i }, h('div', { class: 'nucleo' },
        h('span', { class: 'pill' }, r.cuenta),
        objetivo ? h('div', { style: 'font:500 2.4rem/1 var(--serif);margin:.8rem 0 .3rem' }, hecho + ' de ' + objetivo) : h('div', { style: 'height:.8rem' }),
        h('div', { class: 'apoyo' }, objetivo ? 'Publicadas ' + periodo + '.' : 'Sin meta de publicaciones.',
          r.historiasDia ? ' Historias: ' + r.historiasDia + ' por día.' : ''),
        objetivo ? h('div', { class: 'barra' }, barra) : null,
        r.nota ? h('div', { class: 'apoyo', style: 'margin-top:.7rem' }, r.nota) : null));
    }));
  }

  W.iniciar(function (main) {
    tarjetas = h('div', { class: 'rejilla dos' });
    var cajaCal = h('div', { class: 'bisel aparece' }, h('div', { class: 'nucleo' }));
    var cajaRit = h('div', { class: 'bisel aparece' }, h('div', { class: 'nucleo' }));
    main.append(
      tarjetas,
      h('div', { class: 'bloque' }, h('div', { class: 'encabezado' }, h('h2', { class: 't' }, 'Calendario')), cajaCal),
      h('div', { class: 'bloque' }, h('div', { class: 'encabezado' }, h('h2', { class: 't' }, 'Ritmo por cuenta')), cajaRit));

    W.tabla({
      coleccion: 'contenido',
      contenedor: cajaCal.firstChild,
      campos: PUBLICACIONES,
      columnas: ['fecha', 'cuenta', 'tipo', 'titulo', 'estado'],
      filtros: ['cuenta', 'estado'],
      etiquetaAgregar: 'Agregar publicación',
      tituloNuevo: 'Nueva publicación',
      tituloEditar: 'Editar publicación',
      nuevo: function () { return { fecha: W.hoy(), cuenta: CUENTAS[0], tipo: 'Publicación', estado: 'Idea' }; },
      orden: function (a, b) { return String(a.fecha).localeCompare(String(b.fecha)); },
      vacio: 'Sin publicaciones planeadas.',
      alCambiar: function (l) { estado.pubs = l; pintarRitmo(); }
    });

    W.tabla({
      coleccion: 'contenido-ritmo',
      contenedor: cajaRit.firstChild,
      campos: RITMO,
      columnas: ['cuenta', 'porSemana', 'porMes', 'historiasDia', 'nota'],
      etiquetaAgregar: 'Agregar cuenta',
      tituloNuevo: 'Nueva cuenta',
      tituloEditar: 'Editar ritmo',
      vacio: 'Sin cuentas.',
      alCambiar: function (l) { estado.ritmo = l; pintarRitmo(); }
    });
  });
})();
