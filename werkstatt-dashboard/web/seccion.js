/* Web: estado de las webs y demos, y pendientes de la web. */
(function () {
  'use strict';
  var h = W.h;

  var SITIOS = [
    { k: 'nombre', etiqueta: 'Sitio', tipo: 'texto', req: true, fuerte: true },
    { k: 'tipo', etiqueta: 'Tipo', tipo: 'select', pill: false, opciones: ['Principal', 'Demo', 'Borrador'] },
    { k: 'estado', etiqueta: 'Estado', tipo: 'select', ciclo: true, opciones: [
      { v: 'Borrador', tono: 'idle' }, { v: 'En desarrollo', tono: 'curso' }, { v: 'Publicado', tono: 'ok' }] },
    { k: 'url', etiqueta: 'Dirección del sitio', tipo: 'url' },
    { k: 'repo', etiqueta: 'Repositorio', tipo: 'url' },
    { k: 'nota', etiqueta: 'Nota', tipo: 'area' }
  ];
  var PENDIENTES = [
    { k: 'texto', etiqueta: 'Pendiente', tipo: 'texto', req: true, fuerte: true, ancho: true },
    { k: 'estado', etiqueta: 'Estado', tipo: 'select', ciclo: true, opciones: [
      { v: 'Pendiente', tono: 'idle' }, { v: 'En curso', tono: 'curso' }, { v: 'Hecho', tono: 'ok' }] },
    { k: 'nota', etiqueta: 'Nota', tipo: 'area' }
  ];

  W.iniciar(function (main) {
    var cajaSitios = h('div', { class: 'bisel aparece' }, h('div', { class: 'nucleo' }));
    var cajaPend = h('div', { class: 'bisel aparece' }, h('div', { class: 'nucleo' }));
    main.append(
      h('div', { class: 'encabezado bloque', style: 'margin-top:0' }, h('h2', { class: 't' }, 'Sitios')), cajaSitios,
      h('div', { class: 'bloque' }, h('div', { class: 'encabezado' }, h('h2', { class: 't' }, 'Pendientes de la web')), cajaPend));

    W.tabla({
      coleccion: 'sitios',
      contenedor: cajaSitios.firstChild,
      campos: SITIOS,
      columnas: ['nombre', 'tipo', 'estado', 'url', 'repo', 'nota'],
      filtros: ['estado'],
      etiquetaAgregar: 'Agregar sitio',
      tituloNuevo: 'Nuevo sitio',
      tituloEditar: 'Editar sitio',
      nuevo: function () { return { tipo: 'Demo', estado: 'Borrador' }; },
      vacio: 'Sin sitios.'
    });

    W.tabla({
      coleccion: 'web-pendientes',
      contenedor: cajaPend.firstChild,
      campos: PENDIENTES,
      columnas: ['texto', 'estado', 'nota'],
      filtros: ['estado'],
      etiquetaAgregar: 'Agregar pendiente',
      tituloNuevo: 'Nuevo pendiente',
      tituloEditar: 'Editar pendiente',
      nuevo: function () { return { estado: 'Pendiente' }; },
      vacio: 'Sin pendientes.'
    });
  });
})();
