# (codigo, categoria, nombre, nota, origen, en_v2, replay, html)
PLAN='<svg class="mini" viewBox="0 0 160 100" aria-hidden="true"><path class="w" d="M20 20H140V60H95V85H20Z"/><path class="t" d="M80 20V45M20 60H55M70 60H95M50 60V85"/></svg>'
ARR='<span class="ico"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4.5 11.5 11.5 4.5M5.5 4.5h6v6"/></svg></span>'
I=[]
def add(code,cat,name,note,origin,v2,replay,html): I.append((code,cat,name,note,origin,v2,replay,html))

# ---------- N: NUMEROS Y TEXTURAS
add('N-01','N','Número de puntos (relleno de texto)','Número gigante hecho de puntos uniformes. Funciona como adorno de fondo, nunca como texto que se lee.','brutalist',True,False,'<span class="dots-text">2026</span>')
add('N-02','N','Número de puntos con degradado','Los puntos crecen de izquierda a derecha, como una trama de impresión.','nuevo',False,False,'<canvas class="halftone" data-text="2026" data-mode="fade"></canvas>')
add('N-03','N','Número rayado','Relleno de líneas diagonales, como un sombreado de plano.','nuevo',False,False,'<span class="hatch-text">2026</span>')
add('N-04','N','Número en contorno','Solo el trazo. Al pasar el cursor se rellena.','nuevo',False,False,'<span class="outline-text">2026</span>')
add('N-05','N','Contador que sube','Cuenta hasta su valor al entrar en pantalla.','nuevo',False,True,'<div class="stats"><div><b data-count="51" data-dec="0">51</b><span>m²</span></div><div><b data-count="9.6" data-dec="2">9.60</b><span>m</span></div><div><b data-count="2026" data-dec="0">2026</b><span>año</span></div></div>')
add('N-06','N','Número de rodillo','Cada dígito gira en su columna hasta llegar al valor, como un odómetro.','nuevo',False,True,'<div class="odo" data-odo="2026"></div>')
add('N-07','N','Cota de plano','Línea de cota con topes y medida. La línea se traza y la medida aparece después.','impeccable',False,True,'<div class="cota"><svg viewBox="0 0 300 40" aria-hidden="true"><g class="c"><line x1="10" y1="22" x2="290" y2="22"/><line x1="10" y1="12" x2="10" y2="32"/><line x1="290" y1="12" x2="290" y2="32"/><line x1="4" y1="28" x2="16" y2="16"/><line x1="284" y1="28" x2="296" y2="16"/></g></svg><span>9.60 m</span></div>')
add('N-08','N','Cuadrícula de puntos reactiva','Los puntos crecen cerca del cursor.','nuevo',False,False,'<canvas class="dotgrid" aria-hidden="true"></canvas>')
add('N-09','N','Número de proyecto','Numeral grande con etiqueta pequeña para índices (P-01, P-02).','brutalist',False,False,'<div class="pnum"><b>P-01</b><span>Vivienda · 51 m²</span></div>')

# ---------- T: TEXTO
add('T-01','T','Titular gigante en mayúsculas','Archivo Black, interlínea .9, tracking negativo. El peso de la opción B.','brutalist',True,False,'<p class="macro-t">La obra se piensa en el plano.</p>')
add('T-02','T','Titular editorial con itálica','Cormorant grande y una frase en itálica verde para el énfasis.','high-end',True,False,'<p class="serif-t">La obra se piensa en el plano y <em>se entiende en la mano.</em></p>')
add('T-03','T','Revelado por líneas','Cada línea sube desde una máscara.','nuevo',False,True,'<p class="lines-t"><span><i>Se dibuja,</i></span><span><i>se construye</i></span><span><i>y se prueba.</i></span></p>')
add('T-04','T','Revelado por letras','Las letras entran escalonadas.','nuevo',False,True,'<p class="letters-t" data-split>Werkstatt</p>')
add('T-05','T','Subrayado que se dibuja','Enlace con línea que crece desde la izquierda al pasar el cursor.','nuevo',False,False,'<a class="ul-link" href="#">Ver proyectos de ejemplo</a>')
add('T-06','T','Marcador que barre','Resalte que se traza detrás de una palabra clave.','nuevo',False,True,'<p class="mark-t">Lo que funciona y lo que se ve bien casi nunca son <span class="mk">cosas distintas</span>.</p>')
add('T-07','T','Marquesina infinita','Texto que corre sin parar. Se detiene al pasar el cursor.','nuevo',False,False,'<div class="marq"><div><span>Arquitectura</span><span>Construcción</span><span>Interiorismo</span><span>Muebles</span><span>Ropa de obra</span><span>Arquitectura</span><span>Construcción</span><span>Interiorismo</span><span>Muebles</span><span>Ropa de obra</span></div></div>')
add('T-08','T','Firma que se escribe','Nothing You Could Do con una máscara que la escribe de izquierda a derecha.','high-end',True,True,'<p class="sig-t">Daniel Sierra</p>')
add('T-09','T','Texto que se llena al bajar','El texto pasa de gris a tinta conforme avanzas por la página.','nuevo',False,False,'<p class="fill-t" data-fill>Primero escucho cómo se va a usar un espacio y solo después decido cómo se ve.</p>')

# ---------- B: BOTONES
add('B-01','B','Píldora con ícono anidado','El botón de la v2. El ícono vive en su propio círculo y se mueve al pasar el cursor.','high-end',True,False,'<a class="btn" href="#">Ver obra'+ARR+'</a>')
add('B-02','B','Relleno que sube','Un color sube desde abajo y cambia el texto.','nuevo',False,False,'<a class="btn-wipe" href="#"><span>Ver obra</span></a>')
add('B-03','B','Botón magnético','Sigue al cursor unos píxeles antes de soltarlo.','nuevo',False,False,'<a class="btn mag" href="#" data-mag>Escribir'+ARR+'</a>')
add('B-04','B','Rectángulo con sombra dura','Esquinas rectas y sombra sólida que se hunde al presionar.','brutalist',False,False,'<a class="btn-hard" href="#">Ver obra</a>')
add('B-05','B','Enlace con flecha deslizante','La flecha se estira y avanza al pasar el cursor.','nuevo',False,False,'<a class="arrow-link" href="#">Ver el proceso<svg viewBox="0 0 24 8" aria-hidden="true"><path d="M0 4H22M18 1l4 3-4 3"/></svg></a>')
add('B-06','B','Texto que rueda','El texto sube y entra una copia desde abajo.','nuevo',False,False,'<a class="btn-roll" href="#"><span data-t="Contacto">Contacto</span></a>')
add('B-07','B','Estado por definir','Botón desactivado con línea discontinua. Sirve para contenido pendiente.','high-end',True,False,'<span class="btn off" role="link" aria-disabled="true">Escribir (por definir)'+ARR+'</span>')
add('B-08','B','Borde que se dibuja','El contorno se traza alrededor del botón al pasar el cursor.','nuevo',False,False,'<a class="btn-draw" href="#"><svg aria-hidden="true"><rect x="1" y="1" width="calc(100% - 2px)" height="calc(100% - 2px)" rx="999" pathLength="1"/></svg><span>Ver obra</span></a>')
add('B-09','B','Botón con estados','Reposo, cargando y listo. Pulsa para verlo.','nuevo',False,False,'<button class="btn-state" type="button" data-state><span class="s0">Enviar</span><span class="s1" aria-hidden="true"><i></i></span><span class="s2">Listo</span></button>')

# ---------- C: TARJETAS
add('C-01','C','Doble bisel','Carcasa exterior y núcleo interior, como una pieza de hardware.','high-end',True,False,'<div class="bezel"><div class="core"><span class="tag">Vivienda</span><h4>Casa en barranca</h4><p>Se acomoda al terreno.</p></div></div>')
add('C-02','C','Tarjeta con inclinación','Se inclina en 3D siguiendo el cursor.','nuevo',False,False,'<div class="tilt" data-tilt><div class="core"><h4>Mesa de taller 240</h4><p>Mueve el cursor.</p></div></div>')
add('C-03','C','Tarjeta con luz','Un haz de luz sigue al cursor sobre la superficie.','nuevo',False,False,'<div class="spot" data-spot><h4>Local de refacciones</h4><p>Pasa el cursor.</p></div>')
add('C-04','C','Plano que se traza al pasar','El plano dentro de la tarjeta se dibuja al pasar el cursor.','nuevo',False,False,'<div class="hoverplan"><div class="core">'+PLAN.replace('<path class="w"','<g class="ghost"><path class="w" d="M20 20H140V60H95V85H20Z"/><path class="t" d="M80 20V45M20 60H55M70 60H95M50 60V85"/></g><g class="live"><path class="w"').replace('</svg>','</g></svg>')+'<h4>Planta</h4></div></div>')
add('C-05','C','Acordeón con más animado','Pregunta y respuesta. El signo se gira y la respuesta se abre con suavidad.','high-end',True,False,'<div class="acc"><details><summary>¿Cómo empieza un proyecto?</summary><p>Con una conversación para entender qué necesitas.</p></details><details><summary>¿Cómo se acuerdan los pagos?</summary><p>Cada proyecto se cotiza por separado.</p></details></div>')
add('C-06','C','Cajetín de plano','Ficha con medidas y estado, como el cuadro de datos de una lámina.','impeccable',False,False,'<div class="caj"><span class="n">P-02</span><h4>Mesa de taller 240</h4><dl><dt>Tipo</dt><dd>Mueble</dd><dt>Medidas</dt><dd>240 × 90 × 76 cm</dd><dt>Estado</dt><dd>Ejemplo</dd></dl></div>')
add('C-07','C','Bisel oscuro','Variante oscura para contacto o llamadas a la acción.','high-end',True,False,'<div class="bezel dark"><div class="core"><h4>Cuéntame qué quieres resolver.</h4><p>Casa, local o mueble.</p></div></div>')

# ---------- A: ANIMACIONES DE ENTRADA
add('A-01','A','Aparición con desenfoque','Sube, se enfoca y se hace visible. Escalonado.','high-end',True,True,'<div class="blurrise"><p>Escuchar</p><p>Dibujar</p><p>Construir</p><p>Entregar</p></div>')
add('A-02','A','Plano que se traza','Los muros se dibujan y después aparecen cotas y textos.','high-end',True,True,'<div class="drawplan">'+PLAN+'</div>')
add('A-03','A','Cota que crece','La línea de cota se extiende y la medida cuenta hasta su valor.','nuevo',False,True,'<div class="growcota"><div class="bar"></div><b data-count="9.6" data-dec="2">9.60</b><span> m</span></div>')
add('A-04','A','Lista escalonada','Cada fila entra con un pequeño retraso.','nuevo',False,True,'<ul class="stag"><li>Arquitectura</li><li>Construcción</li><li>Interiorismo</li><li>Muebles</li></ul>')
add('A-05','A','Cortina','Un bloque se revela con una máscara que se abre.','nuevo',False,True,'<div class="curtain"><div>Foto pendiente</div></div>')
add('A-06','A','Línea que crece','Divisor que se traza de izquierda a derecha.','nuevo',False,True,'<div class="growline"><i></i><p>Sección</p></div>')
add('A-07','A','Entrada con escala','La pieza crece desde 92% con un rebote muy leve.','nuevo',False,True,'<div class="scalein"><div class="bezel"><div class="core"><h4>Obra</h4></div></div></div>')
add('A-08','A','Capas con profundidad','Dos capas se mueven distinto con el cursor.','nuevo',False,False,'<div class="depth" data-depth><div class="l1">Werk</div><div class="l2">statt</div></div>')

# ---------- V: NAVEGACION
add('V-01','V','Isla flotante translúcida','Barra suspendida con desenfoque; deja ver lo que pasa debajo.','high-end',True,False,'<div class="islandwrap"><div class="stripes"></div><div class="island-d"><img src="../assets/logo/werkstatt-positivo.svg" alt="Werkstatt"><nav><a href="#">Obra</a><a href="#">Áreas</a><a href="#">Proceso</a></nav><a class="btn sm" href="#">Contacto'+ARR+'</a></div></div>')
add('V-02','V','Menú de pantalla completa','Botón que se vuelve cruz y enlaces que entran escalonados.','high-end',True,False,'<div class="phone" data-menu><button class="burger-d" type="button" aria-label="Abrir menú" aria-expanded="false"><i></i><i></i></button><div class="ov"><a href="#">Obra</a><a href="#">Áreas</a><a href="#">Proceso</a></div><p>Toca el botón</p></div>')
add('V-03','V','Regla lateral en centímetros','Marcas y lectura que siguen el scroll. Desplázate dentro del cuadro.','impeccable',True,False,'<div class="rulerbox" data-ruler><div class="rl"><output>0.0 cm</output></div><div class="sc"><div class="in"><p>Desplázate</p><p>Más abajo</p><p>Y más</p><p>Todavía más</p><p>Fin</p></div></div></div>')
add('V-04','V','Barra de progreso de lectura','Línea fina que avanza con el scroll.','nuevo',False,False,'<div class="progbox" data-prog><div class="pb"><i></i></div><div class="sc"><div class="in"><p>Desplázate</p><p>Más abajo</p><p>Y más</p><p>Todavía más</p><p>Fin</p></div></div></div>')
add('V-05','V','Subrayado deslizante','Un indicador se desplaza entre los enlaces.','nuevo',False,False,'<nav class="slidenav" data-slide><a href="#">Obra</a><a href="#">Áreas</a><a href="#">Proceso</a><a href="#">Contacto</a><i></i></nav>')

# ---------- F: FORMULARIOS
add('F-01','F','Campo con etiqueta flotante','La etiqueta sube al escribir.','nuevo',False,False,'<label class="fl"><input type="text" placeholder=" "><span>Tu nombre</span></label>')
add('F-02','F','Campo por definir','Caja discontinua para datos pendientes.','high-end',True,False,'<div class="todo"><small>Correo</small><span>por definir</span></div>')
add('F-03','F','Interruptor','Deslizador con resorte suave.','nuevo',False,False,'<label class="sw"><input type="checkbox" checked><i></i><span>Modo oscuro</span></label>')
add('F-04','F','Selector de opciones','Píldoras seleccionables.','nuevo',False,False,'<div class="chips" data-chips><button type="button" class="on">Casa</button><button type="button">Local</button><button type="button">Mueble</button></div>')

# ---------- M: AMBIENTE
add('M-01','M','Grano','Textura fina sobre la superficie. Hace menos digital el fondo.','high-end',True,False,'<div class="grain"><p>Superficie con grano</p></div>')
add('M-02','M','Tapete de cuadrícula','Cuadrícula fina con líneas marcadas cada 5 celdas.','impeccable',False,False,'<div class="mat"><p>Cuadrícula</p></div>')
add('M-03','M','Manchas flotantes','Colores suaves que se mueven lento detrás del contenido.','nuevo',False,False,'<div class="blobs"><i></i><i></i><p>Fondo vivo</p></div>')
add('M-04','M','Cursor personalizado','Anillo que persigue al cursor con inercia.','nuevo',False,False,'<div class="curbox" data-cursor><p>Mueve el cursor aquí</p><i class="ring"></i></div>')
add('M-05','M','Fondo de puntos que se desvanece','Puntos que se apagan hacia abajo.','nuevo',False,False,'<div class="dotfade"><p>Puntos</p></div>')

# ---------- D: DECORACION
add('D-01','D','Franja de advertencia','Rayas diagonales para separar secciones con carácter de obra.','brutalist',False,False,'<div class="warn"></div>')
add('D-02','D','Código de barras','Barras decorativas para fichas y tarjetas.','brutalist',False,False,'<div class="barcode"></div>')
add('D-03','D','Cruces de registro','Marcas de corte en las esquinas, como en una prueba de impresión.','brutalist',False,False,'<div class="reg"><i></i><i></i><i></i><i></i><p>Registro</p></div>')
add('D-04','D','Etiqueta entre corchetes','Rótulo técnico en mayúsculas pequeñas.','brutalist',False,False,'<span class="brk">[ Obra ]</span>')
add('D-05','D','Etiqueta en píldora','Microetiqueta con borde suave.','high-end',True,False,'<span class="tag">Taller · arquitectura, muebles y obra</span>')
add('D-06','D','Hueco de foto pendiente','Placeholder con rayado fino, mejor que un cuadro gris.','nuevo',False,False,'<div class="ph">Foto pendiente</div>')
