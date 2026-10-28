/* Tienda: piezas del borrador y su forma de venta (directa o por mensaje). */
(function () {
  'use strict';
  var h = W.h;

  var CAMPOS = [
    { k: 'codigo', etiqueta: 'Código', tipo: 'texto', req: true, codigo: true },
    { k: 'nombre', etiqueta: 'Pieza', tipo: 'texto', req: true, fuerte: true },
    { k: 'familia', etiqueta: 'Familia', tipo: 'select', pill: false, opciones: ['Gorras', 'Chamarras', 'Calcetas'] },
    { k: 'tallas', etiqueta: 'Tallas', tipo: 'texto' },
    { k: 'precio', etiqueta: 'Precio', tipo: 'numero', formato: 'moneda' },
    { k: 'estado', etiqueta: 'Estado', tipo: 'select', ciclo: true, opciones: [
      { v: 'Próximamente', tono: 'idle' }, { v: 'Disponible', tono: 'ok' }, { v: 'Agotado', tono: 'curso' }] },
    { k: 'venta', etiqueta: 'Venta', tipo: 'select', pill: false, opciones: ['Directa', 'Mensaje'] },
    { k: 'nota', etiqueta: 'Nota', tipo: 'area' }
  ];

  function dato(i, etiqueta, valor, detalle) {
    return h('div', { class: 'bisel aparece', style: '--i:' + i }, h('div', { class: 'nucleo' },
      h('span', { class: 'pill' }, etiqueta),
      h('div', { style: 'font:500 2.4rem/1 var(--serif);margin:.8rem 0 .3rem' }, valor),
      h('div', { class: 'apoyo' }, detalle)));
  }

  W.iniciar(function (main) {
    var resumen = h('div', { class: 'rejilla' });
    var caja = h('div', { class: 'bisel aparece' }, h('div', { class: 'nucleo' }));
    main.append(resumen, h('div', { class: 'bloque' }, caja));

    W.tabla({
      coleccion: 'tienda',
      contenedor: caja.firstChild,
      campos: CAMPOS,
      columnas: ['codigo', 'nombre', 'familia', 'precio', 'estado', 'venta'],
      filtros: ['familia', 'estado', 'venta'],
      etiquetaAgregar: 'Agregar pieza',
      tituloNuevo: 'Nueva pieza',
      tituloEditar: 'Editar pieza',
      nuevo: function () { return { estado: 'Próximamente', venta: 'Directa' }; },
      orden: function (a, b) { return String(a.codigo).localeCompare(String(b.codigo), 'es', { numeric: true }); },
      vacio: 'Sin piezas.',
      alCambiar: function (lista) {
        var directa = lista.filter(function (p) { return p.venta === 'Directa'; }).length;
        var disp = lista.filter(function (p) { return p.estado === 'Disponible'; }).length;
        var valor = lista.reduce(function (s, p) { return s + (Number(p.precio) || 0); }, 0);
        var familias = {};
        lista.forEach(function (p) { familias[p.familia || 'Sin familia'] = (familias[p.familia || 'Sin familia'] || 0) + 1; });
        resumen.replaceChildren(
          dato(0, 'Piezas', String(lista.length), Object.keys(familias).map(function (f) { return familias[f] + ' ' + f.toLowerCase(); }).join(', ') || 'Sin piezas'),
          dato(1, 'Venta', directa + ' directa', (lista.length - directa) + ' por mensaje'),
          dato(2, 'Disponibles', String(disp), 'de ' + lista.length + ' piezas'),
          dato(3, 'Valor de lista', W.moneda(valor), 'Suma de precios capturados'));
      }
    });
  });
})();
