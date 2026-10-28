/* Líneas: ramas del estudio, cada una con su nombre propio (patrón nombre | WERKSTATT). */
(function () {
  'use strict';
  var h = W.h;

  var CAMPOS = [
    { k: 'nombre', etiqueta: 'Nombre de la línea', tipo: 'texto', req: true, fuerte: true },
    { k: 'giro', etiqueta: 'A qué se dedica', tipo: 'texto', req: true },
    { k: 'estado', etiqueta: 'Estado', tipo: 'select', ciclo: true, opciones: [
      { v: 'Idea', tono: 'idle' }, { v: 'Nombre confirmado', tono: 'ok' }, { v: 'En desarrollo', tono: 'curso' }, { v: 'Activa', tono: 'curso' }] },
    { k: 'nota', etiqueta: 'Nota', tipo: 'area' }
  ];

  W.iniciar(function (main) {
    var rotulos = h('div', { style: 'display:flex;flex-wrap:wrap;gap:1rem 2.5rem;align-items:baseline' });
    var caja = h('div', { class: 'bisel aparece' }, h('div', { class: 'nucleo' }));
    main.append(
      h('div', { class: 'bisel aparece' }, h('div', { class: 'nucleo' },
        h('span', { class: 'pill' }, 'Así se leen'), h('div', { style: 'height:.9rem' }), rotulos)),
      h('div', { class: 'bloque' }, caja));

    W.tabla({
      coleccion: 'lineas',
      contenedor: caja.firstChild,
      campos: CAMPOS,
      columnas: ['nombre', 'giro', 'estado', 'nota'],
      filtros: ['estado'],
      etiquetaAgregar: 'Agregar línea',
      tituloNuevo: 'Nueva línea',
      tituloEditar: 'Editar línea',
      nuevo: function () { return { estado: 'Idea' }; },
      vacio: 'Sin líneas.',
      alCambiar: function (lista) {
        rotulos.replaceChildren.apply(rotulos, lista.map(function (l) {
          return h('span', { style: 'font:500 1.6rem/1 var(--serif);letter-spacing:.01em' },
            l.nombre, h('span', { style: 'color:var(--gris);margin:0 .5rem' }, '|'),
            h('span', { style: 'font:500 .8rem var(--sans);letter-spacing:.2em' }, 'WERKSTATT'));
        }));
      }
    });
  });
})();
