/* Marca: referencia de la skill estructura-marca (jerarquía, logos, paleta, tipografía) y registro de decisiones. */
(function () {
  'use strict';
  var h = W.h;

  var PALETA = [
    { grupo: 'Web y paneles', colores: [
      ['Crema', '#FDFBF7'], ['Lino', '#F5EFE4'], ['Núcleo', '#FFFEFB'], ['Espresso', '#2A211B'],
      ['Gris cálido', '#6B5E52'], ['Salvia', '#8E9C86'], ['Salvia profundo', '#566451'], ['Arena', '#E3C9A8']] },
    { grupo: 'Documentos', colores: [
      ['Off-white', '#FAFAF8'], ['Crema', '#F5EFE8'], ['Pearl Bush', '#E3DED1'], ['Pale Oyster', '#969286'],
      ['Pablo', '#736A59'], ['Chive', '#4F533A'], ['Negro profundo', '#1A1A1A']] }
  ];

  var TIPOGRAFIA = [
    ['Inter', 'Cuerpo y etiquetas', "font:400 1.05rem var(--sans)"],
    ['Cormorant', 'Títulos de tarjeta y cartas', "font:500 1.5rem var(--serif)"],
    ['Archivo Black', 'Solo titulares grandes de la web', "font:400 1.2rem var(--titulo);text-transform:uppercase;letter-spacing:-.03em"]
  ];

  function nucleo(contenido) { return h('div', { class: 'bisel aparece' }, h('div', { class: 'nucleo' }, contenido)); }
  function bloque(titulo, hijo) { return h('div', { class: 'bloque' }, h('div', { class: 'encabezado' }, h('h2', { class: 't' }, titulo)), hijo); }

  W.iniciar(function (main) {
    /* jerarquía: las líneas se leen de su colección */
    var lineas = h('div', { style: 'display:flex;flex-wrap:wrap;gap:.5rem' });
    W.datos.lista('lineas').then(function (l) {
      lineas.replaceChildren.apply(lineas, l.map(function (x) { return h('span', { class: 'pill' }, x.nombre); }));
    }).catch(function () {});

    var nivel = function (rotulo, titulo, texto, extra) {
      return h('div', { style: 'padding:1rem 0;border-bottom:1px solid var(--anillo);display:grid;grid-template-columns:9rem 1fr;gap:1rem' },
        h('span', { class: 'pill', style: 'align-self:start;justify-self:start' }, rotulo),
        h('div', null, h('h3', { class: 't' }, titulo), h('div', { class: 'apoyo' }, texto), extra ? h('div', { style: 'margin-top:.6rem' }, extra) : null));
    };
    main.append(bloque('Estructura', nucleo([
      nivel('Estudio', 'Werkstatt', 'Apellido compartido. Arquitectura, construcción, interiorismo, muebles y ropa de obra.'),
      nivel('Líneas', 'Nombre propio delante del apellido', 'Cada enfoque se llama [nombre] Werkstatt. Una colaboración se escribe con "x".', lineas),
      nivel('Persona', 'Daniel Sierra', 'Marca personal y autor. Contenido, presencia en redes y firma. El contenido no es una línea de Werkstatt.'),
      nivel('Ramificación', '@derstahlbeton', 'Identidad propia, sin los logos del estudio.')
    ])));

    /* logos */
    var logo = function (src, rotulo, ancho) {
      return h('div', { style: 'display:flex;flex-direction:column;gap:.8rem;align-items:flex-start;padding:1.25rem;border-radius:1.25rem;background:var(--crema);border:1px solid var(--anillo);min-width:12rem;flex:1' },
        h('img', { src: src, alt: rotulo, style: 'height:' + ancho + ';width:auto' }), h('span', { class: 'pill' }, rotulo));
    };
    main.append(bloque('Logos', nucleo([h('div', { style: 'display:flex;flex-wrap:wrap;gap:1rem;align-items:stretch' },
      logo('/shared/logo/werkstatt-positivo.svg', 'Madre', '1.9rem'),
      logo('/shared/logo/marca-positivo.svg', 'Marca sola', '2.6rem'),
      h('div', { style: 'display:flex;flex-direction:column;gap:.8rem;align-items:flex-start;padding:1.25rem;border-radius:1.25rem;background:var(--crema);border:1px solid var(--anillo);min-width:12rem;flex:1' },
        h('span', { style: 'font:500 1.6rem/1.2 var(--serif)' }, 'Palabra ', h('span', { style: 'color:var(--gris)' }, '|'), ' ', h('span', { style: 'font:500 .8rem var(--sans);letter-spacing:.2em' }, 'WERKSTATT')),
        h('span', { class: 'pill' }, 'De línea'))),
      h('p', { class: 'apoyo', style: 'margin:1rem 0 0' }, 'Los archivos SVG y PNG de cada logo, en sus cuatro temas, viven en la skill estructura-marca.')])));

    /* paleta */
    main.append(bloque('Paleta', nucleo(PALETA.map(function (g, i) {
      return h('div', { style: i ? 'margin-top:1.4rem' : '' },
        h('span', { class: 'pill' }, g.grupo),
        h('div', { style: 'display:grid;grid-template-columns:repeat(auto-fill,minmax(8.5rem,1fr));gap:.8rem;margin-top:.8rem' }, g.colores.map(function (c) {
          return h('div', null,
            h('div', { style: 'height:3.2rem;border-radius:1rem;border:1px solid var(--anillo);background:' + c[1] }),
            h('div', { style: 'font-size:.8125rem;font-weight:500;margin-top:.4rem' }, c[0]),
            h('div', { class: 'apoyo', style: 'font-size:.75rem' }, c[1]));
        })));
    }))));

    /* tipografía */
    main.append(bloque('Tipografía', nucleo(h('div', { class: 'rejilla' }, TIPOGRAFIA.map(function (t) {
      return h('div', null, h('div', { style: t[2] }, t[0]), h('div', { class: 'apoyo', style: 'margin-top:.3rem' }, t[1]));
    }).concat([h('div', null, h('div', { style: 'font:400 1.05rem var(--sans)' }, 'Nothing You Could Do'), h('div', { class: 'apoyo', style: 'margin-top:.3rem' }, 'Solo la firma de los documentos'))])))));

    /* decisiones */
    var caja = h('div', { class: 'bisel aparece' }, h('div', { class: 'nucleo' }));
    main.append(bloque('Decisiones', caja));
    W.tabla({
      coleccion: 'marca-decisiones',
      contenedor: caja.firstChild,
      campos: [
        { k: 'fecha', etiqueta: 'Fecha', tipo: 'fecha', req: true },
        { k: 'tema', etiqueta: 'Tema', tipo: 'texto', req: true, fuerte: true },
        { k: 'decision', etiqueta: 'Decisión', tipo: 'area', req: true }
      ],
      columnas: ['fecha', 'tema', 'decision'],
      etiquetaAgregar: 'Registrar decisión',
      tituloNuevo: 'Nueva decisión',
      tituloEditar: 'Editar decisión',
      nuevo: function () { return { fecha: W.hoy() }; },
      orden: function (a, b) { return String(b.fecha).localeCompare(String(a.fecha)); },
      vacio: 'Sin decisiones registradas.'
    });
  });
})();
