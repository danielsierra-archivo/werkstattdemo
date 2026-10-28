/* Documentos: biblioteca de tipos de documento de la skill Werkstatt y su estado. */
(function () {
  'use strict';
  var h = W.h;

  var ESTADOS = [
    { v: 'Implementado', tono: 'ok' },
    { v: 'Por revisar', tono: 'curso' },
    { v: 'Pendiente', tono: 'idle' }
  ];
  var CAMPOS = [
    { k: 'nombre', etiqueta: 'Documento', tipo: 'texto', req: true, fuerte: true },
    { k: 'alias', etiqueta: 'También se pide como', tipo: 'texto' },
    { k: 'grupo', etiqueta: 'Grupo', tipo: 'select', pill: false, opciones: ['Estudio', 'Cliente', 'Obra', 'Muebles'] },
    { k: 'logo', etiqueta: 'Logo que lleva', tipo: 'select', pill: false, opciones: ['Madre', 'Rohbau', 'Rohholz', 'Rohleinen', 'Rohmappe', 'Sin logo'] },
    { k: 'estado', etiqueta: 'Estado', tipo: 'select', opciones: ESTADOS, ciclo: true },
    { k: 'nota', etiqueta: 'Nota', tipo: 'area' }
  ];

  W.iniciar(function (main) {
    var resumen = h('p', { class: 'apoyo', style: 'margin:0 0 1.25rem' });
    var caja = h('div', { class: 'bisel aparece' }, h('div', { class: 'nucleo' }));
    main.append(resumen, caja);

    W.tabla({
      coleccion: 'documentos',
      contenedor: caja.firstChild,
      campos: CAMPOS,
      columnas: ['nombre', 'grupo', 'logo', 'estado', 'nota'],
      filtros: ['grupo', 'estado'],
      etiquetaAgregar: 'Agregar documento',
      tituloNuevo: 'Nuevo documento',
      tituloEditar: 'Editar documento',
      nuevo: function () { return { estado: 'Pendiente' }; },
      vacio: 'Sin documentos.',
      alCambiar: function (lista) {
        var n = function (e) { return lista.filter(function (d) { return d.estado === e; }).length; };
        resumen.textContent = lista.length + ' documentos: ' + n('Implementado') + ' implementados, ' + n('Por revisar') + ' por revisar, ' + n('Pendiente') + ' pendientes. Toca el estado para cambiarlo.';
      }
    });
  });
})();
