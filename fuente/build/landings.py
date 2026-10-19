# Genera landings-demo/*.html (tres landings de muestra con el sistema Werkstatt).
# Uso: python3 fuente/build/landings.py   (desde la raíz del repositorio)
import os, html
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'landings-demo')

ARROW = '<span class="ico"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4.5 11.5 11.5 4.5M5.5 4.5h6v6"/></svg></span>'
PLUS = '<span class="plus"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 3v10M3 8h10"/></svg></span>'

def cotas(w, h, wl, hl):
    # cota superior y lateral para un recinto de 40..(40+w) x 50..(50+h)
    x1, x2, y1, y2 = 40, 40 + w, 50, 50 + h
    return f'''<g class="c"><line x1="{x1}" y1="28" x2="{x2}" y2="28"/><line x1="{x1-4}" y1="32" x2="{x1+4}" y2="24"/><line x1="{x2-4}" y1="32" x2="{x2+4}" y2="24"/>
<line x1="{x1}" y1="24" x2="{x1}" y2="46"/><line x1="{x2}" y1="24" x2="{x2}" y2="46"/>
<line x1="18" y1="{y1}" x2="18" y2="{y2}"/><line x1="14" y1="{y1+4}" x2="22" y2="{y1-4}"/><line x1="14" y1="{y2+4}" x2="22" y2="{y2-4}"/>
<line x1="14" y1="{y1}" x2="36" y2="{y1}"/><line x1="14" y1="{y2}" x2="36" y2="{y2}"/></g>
<text class="tx" x="{(x1+x2)//2}" y="21" text-anchor="middle">{wl}</text>
<text class="tx" x="10" y="{(y1+y2)//2}" text-anchor="middle" transform="rotate(-90 10 {(y1+y2)//2})">{hl}</text>'''

PLAN_HOY = f'''<svg class="plan" viewBox="0 0 400 300" role="img" aria-label="Planta de un departamento de ejemplo como está hoy: sala-comedor, cocina cerrada, dos recámaras y un baño">
{cotas(320,220,"8.00 m","5.50 m")}
<path class="w" d="M40 50 H360 V270 H40 Z"/>
<path class="t" d="M200 50 V150 M40 150 H200 M200 150 H360 M280 150 V270 M200 210 H280 M120 150 V270"/>
<text class="tl" x="120" y="104" text-anchor="middle">Sala</text><text class="tl" x="280" y="104" text-anchor="middle">Cocina</text>
<text class="tl" x="80" y="214" text-anchor="middle">Rec. 1</text><text class="tl" x="160" y="214" text-anchor="middle">Rec. 2</text>
<text class="tl" x="240" y="244" text-anchor="middle">Baño</text><text class="tl" x="320" y="214" text-anchor="middle">Bodega</text></svg>'''

PLAN_PROP = f'''<svg class="plan" viewBox="0 0 400 300" role="img" aria-label="Planta del mismo departamento de ejemplo con propuesta: cocina abierta a la sala, dos recámaras y baño completo">
{cotas(320,220,"8.00 m","5.50 m")}
<path class="w" d="M40 50 H360 V270 H40 Z"/>
<path class="t" d="M40 170 H150 M150 170 V270 M230 170 H360 M230 170 V270 M230 220 H360"/>
<rect class="t d" x="250" y="62" width="100" height="26"/>
<text class="tl" x="200" y="116" text-anchor="middle">Sala, comedor y cocina abiertos</text>
<text class="tl" x="95" y="226" text-anchor="middle">Rec. 1</text><text class="tl" x="190" y="226" text-anchor="middle">Rec. 2</text>
<text class="tl" x="295" y="200" text-anchor="middle">Baño</text><text class="tl" x="295" y="250" text-anchor="middle">Lavado</text></svg>'''

PLAN_VIV = f'''<svg class="plan" viewBox="0 0 400 300" role="img" aria-label="Planta de una vivienda de ejemplo, 9.00 por 6.00 metros, con sala, cocina, comedor, recámara y baño">
{cotas(320,210,"9.00 m","6.00 m")}
<path class="w" d="M40 50 H360 V260 H40 Z"/>
<path class="t" d="M40 150 H170 M170 50 V150 M170 150 V260 M170 210 H360 M270 150 H360 M270 150 V210"/>
<text class="tl" x="105" y="104" text-anchor="middle">Sala</text><text class="tl" x="265" y="104" text-anchor="middle">Cocina y comedor</text>
<text class="tl" x="105" y="208" text-anchor="middle">Recámara</text><text class="tl" x="315" y="184" text-anchor="middle">Baño</text>
<text class="tl" x="265" y="240" text-anchor="middle">Patio de servicio</text></svg>'''

PLAN_LOC = f'''<svg class="plan" viewBox="0 0 400 300" role="img" aria-label="Planta de un local de ejemplo, 7.00 por 5.00 metros, con área de atención, trabajo y bodega">
{cotas(320,220,"7.00 m","5.00 m")}
<path class="w" d="M130 270 H40 V50 H360 V270 H200"/>
<rect class="t" x="60" y="80" width="150" height="22"/>
<rect class="t" x="40" y="130" width="14" height="110"/>
<path class="t" d="M270 50 V190 H360"/>
<text class="tl" x="135" y="124" text-anchor="middle">Atención</text>
<text class="tl" x="315" y="130" text-anchor="middle">Trabajo</text>
<text class="tl" x="315" y="236" text-anchor="middle">Bodega</text>
<text class="tl" x="165" y="288" text-anchor="middle">Entrada</text></svg>'''

PAGES = [
 dict(file='airbnb.html', code='A', nav='Departamento para renta corta',
  title='Remodelar tu departamento para rentarlo por noches',
  desc='Landing de muestra A: remodelación de departamentos pensada para renta de corta estancia. Contenido de ejemplo.',
  tag='Remodelación de departamentos · renta por noches',
  h1='Tu departamento, listo para recibir huéspedes <em>sin dolores de cabeza.</em>',
  lead='Distribución que se entiende al entrar, materiales que aguantan el uso y un plan de obra con fechas claras. Empezamos escuchando cómo quieres rentarlo y qué reglas aplican en tu ciudad.',
  cta='Pedir una conversación',
  chips=['Respuesta en [plazo por definir]','Primera conversación sin costo [por confirmar]','Contenido de ejemplo'],
  hd_problema='Lo que suele complicar un departamento de renta corta.',
  problemas=[('Se ve bien, pero no funciona','Una distribución pensada para vivirse no siempre sirve para rotar huéspedes: falta guardado, ropa de cama, un lugar para las maletas.'),
             ('Materiales que no aguantan','El uso intenso gasta pisos, muebles y herrajes. Elegir bien al principio cuesta menos que reponer cada temporada.'),
             ('Reglas que no se revisaron','Cada ciudad tiene sus propias reglas para rentas de corta estancia. Conviene revisarlas antes de gastar, con la autoridad local y el reglamento del edificio.')],
  hd_incluye='Qué incluye el trabajo.',
  incluye=[('Diagnóstico del espacio','Visita, medidas y una lista de lo que sí conviene tocar y de lo que no.'),
           ('Planos y propuesta','Distribución nueva dibujada a escala, con materiales a la vista antes de decidir.'),
           ('Obra con seguimiento','Calendario, avances y cambios acordados por escrito.'),
           ('Entrega y guía de cuidados','Acta de entrega, planos finales y cómo mantener cada acabado.')],
  plan_t='Antes y después, sobre el plano.', plan_p='Un ejemplo ilustrativo: la misma planta de un departamento de ejemplo hoy y con una propuesta. No es una obra real.',
  planes=[('Hoy',PLAN_HOY),('Propuesta',PLAN_PROP)],
  pasos=[('Escuchar','Cómo piensas rentarlo, cuántos huéspedes, qué presupuesto y qué plazo.'),
         ('Dibujar','Planos y materiales a la vista. Se ajusta en papel antes que en obra.'),
         ('Construir','Obra con seguimiento. Todo cambio de alcance se acuerda antes.'),
         ('Entregar','Acta, planos finales y guía de cuidados.')],
  faq=[('¿Me pueden decir cuánto voy a ganar con la renta?','No. Los ingresos dependen de la zona, la temporada y cómo lo administres; aquí no se prometen cifras. Lo que sí se puede es proyectar el espacio para que rote bien.'),
       ('¿Ven los permisos de renta de mi ciudad?','Te decimos qué conviene preguntar y a quién. El trámite lo confirmas con la autoridad local y con el reglamento de tu edificio.'),
       ('¿Cuánto tarda una remodelación?','Depende del alcance. En la propuesta se escribe un calendario con fechas y se actualiza si algo cambia.'),
       ('¿Cómo se acuerdan los pagos?','Cada proyecto se cotiza por separado y los pagos se definen en la propuesta. Cada pago recibido lleva su recibo.')],
  campos=[('Tu nombre','text','name'),('WhatsApp o correo','text','contact'),('Ciudad y colonia del departamento','text','loc'),('Metros cuadrados aproximados','text','m2')],
  cierre='Cuéntame cómo quieres rentarlo.'),
 dict(file='vivienda.html', code='B', nav='Remodelar mi vivienda',
  title='Remodelar tu vivienda',
  desc='Landing de muestra B: remodelación de vivienda. Contenido de ejemplo.',
  tag='Remodelación de vivienda',
  h1='Una casa que se acomoda a como <em>vives hoy.</em>',
  lead='Cocina que se usa, espacios que se conectan y una obra que no te quita la tranquilidad. Primero escuchamos cómo se vive la casa y solo después decidimos qué mover.',
  cta='Pedir una conversación',
  chips=['Respuesta en [plazo por definir]','Visita inicial [por confirmar]','Contenido de ejemplo'],
  hd_problema='Lo que casi siempre se quiere resolver.',
  problemas=[('Espacios que ya no sirven','La casa se pensó para otra familia o para otra época. Mover un muro a veces resuelve más que ampliar.'),
             ('Miedo a la obra','Polvo, retrasos y costos que crecen. Se baja con un plan claro, fechas por escrito y cambios acordados antes de ejecutarse.'),
             ('No saber por dónde empezar','Antes de contratar a nadie conviene tener un plano y una prioridad: qué primero, qué después, qué puede esperar.')],
  hd_incluye='Qué incluye el trabajo.',
  incluye=[('Levantamiento y diagnóstico','Medidas reales de la casa y una lista de lo que conviene resolver primero.'),
           ('Proyecto','Planos, cortes y materiales a la vista, con alternativas cuando las hay.'),
           ('Obra con seguimiento','Calendario, avances y orden de cambio para todo lo que se salga del alcance.'),
           ('Entrega','Acta de entrega, planos finales y guía de cuidados.')],
  plan_t='Así se ve un proyecto en el plano.', plan_p='Una planta de ejemplo con cotas y espacios nombrados. No es una obra real.',
  planes=[('Planta de ejemplo',PLAN_VIV)],
  pasos=[('Escuchar','Cómo se vive la casa hoy, qué estorba y qué presupuesto hay.'),
         ('Dibujar','Planos y materiales a la vista antes de decidir.'),
         ('Construir','Obra con seguimiento y cambios por escrito.'),
         ('Entregar','Acta, planos finales y guía de cuidados.')],
  faq=[('¿Tengo que salirme de la casa durante la obra?','Depende del alcance. Se plantea desde el inicio y la obra se organiza por etapas cuando es posible.'),
       ('¿Qué pasa si durante la obra cambio de idea?','Se documenta en una orden de cambio y se acuerda antes de ejecutarlo, para que nadie se entere del costo al final.'),
       ('¿Puedo remodelar por partes?','Sí. Un buen plano permite avanzar por etapas sin deshacer lo anterior.'),
       ('¿Cómo se acuerdan los pagos?','Cada proyecto se cotiza por separado y los pagos se definen en la propuesta. Cada pago recibido lleva su recibo.')],
  campos=[('Tu nombre','text','name'),('WhatsApp o correo','text','contact'),('Ciudad y colonia de la vivienda','text','loc'),('Qué quieres cambiar','text','que')],
  cierre='Cuéntame qué quieres cambiar de tu casa.'),
 dict(file='local.html', code='C', nav='Local u oficina',
  title='Remodelar tu local u oficina',
  desc='Landing de muestra C: remodelación de locales y oficinas. Contenido de ejemplo.',
  tag='Locales y oficinas',
  h1='Un espacio de trabajo que se entiende <em>de un vistazo.</em>',
  lead='Un local que invita a entrar, una oficina donde se trabaja a gusto y una obra que respeta tus fechas de apertura. Empezamos por cómo se usa el espacio.',
  cta='Pedir una conversación',
  chips=['Respuesta en [plazo por definir]','Visita inicial [por confirmar]','Contenido de ejemplo'],
  hd_problema='Lo que un espacio de trabajo tiene que resolver.',
  problemas=[('Que se entienda al entrar','Quien llega debe saber dónde ir sin preguntar. El mostrador, la entrada y la circulación mandan.'),
             ('Que el equipo trabaje a gusto','Luz, ruido y distancias cambian el día a día más que la decoración.'),
             ('Que la obra no frene el negocio','Se planea por etapas y con fechas por escrito para cerrar lo menos posible.')],
  hd_incluye='Qué incluye el trabajo.',
  incluye=[('Levantamiento','Medidas reales, instalaciones existentes y reglas del inmueble.'),
           ('Distribución y diseño','Plano a escala con circulaciones, mobiliario y materiales a la vista.'),
           ('Obra con seguimiento','Calendario por etapas, avances y cambios acordados por escrito.'),
           ('Entrega','Acta de entrega, planos finales y guía de mantenimiento.')],
  plan_t='Un local, visto desde arriba.', plan_p='Una planta de ejemplo con atención, trabajo y bodega. No es una obra real.',
  planes=[('Planta de ejemplo',PLAN_LOC)],
  pasos=[('Escuchar','Qué haces en el espacio, cuánta gente lo usa y para cuándo lo necesitas.'),
         ('Dibujar','Distribución y materiales a la vista antes de decidir.'),
         ('Construir','Obra por etapas con seguimiento.'),
         ('Entregar','Acta, planos finales y guía de mantenimiento.')],
  faq=[('¿Pueden trabajar sin cerrar el negocio?','Muchas veces sí, por etapas u horarios. Se define en el proyecto según el alcance.'),
       ('¿Ven permisos y requisitos del inmueble?','Te decimos qué revisar y con quién. El trámite lo confirmas con la autoridad local y con el arrendador o la administración.'),
       ('¿Es un local propio o rentado?','Si es rentado, conviene revisar el contrato antes de obra. Podemos ayudarte a listar qué preguntar.'),
       ('¿Cómo se acuerdan los pagos?','Cada proyecto se cotiza por separado y los pagos se definen en la propuesta. Cada pago recibido lleva su recibo.')],
  campos=[('Tu nombre','text','name'),('WhatsApp o correo','text','contact'),('Tipo de espacio (local u oficina)','text','tipo'),('Metros cuadrados aproximados','text','m2')],
  cierre='Cuéntame qué hace tu espacio.'),
]

def head(title, desc, extra=''):
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)} | Werkstatt, landing de muestra</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#FDFBF7">
<link rel="icon" href="../assets/logo/marca-positivo.svg" type="image/svg+xml">
<link rel="stylesheet" href="styles.css">
</head>
'''

def island(nav_label):
    return f'''<body>
<a class="skip" href="#contacto">Saltar al formulario</a>
<header class="island" role="banner">
  <a href="#inicio" aria-label="Werkstatt, inicio"><img class="logo" src="../assets/logo/werkstatt-positivo.svg" alt="Werkstatt"></a>
  <a class="btn" href="#contacto" data-mag>Contacto{ARROW}</a>
  <button class="burger" type="button" aria-label="Abrir menú" aria-expanded="false" aria-controls="menu"><i></i><i></i></button>
</header>
<nav class="sheetnav" id="menu" aria-label="Menú"><a href="#problema">Lo que resuelve</a><a href="#proceso">Proceso</a><a href="#preguntas">Preguntas</a><a href="#contacto">Contacto</a></nav>
'''

def hd(tag, h2, idv):
    return f'''<div class="head reveal"><i class="gl" aria-hidden="true"></i><span class="tag">{tag}</span><h2 id="{idv}">{h2}</h2></div>'''

def page(p):
    o = [head(p['title'], p['desc']), island(p['nav'])]
    o.append(f'''<main id="inicio">
<section class="hero">
  <div class="blobs" aria-hidden="true"><i></i><i></i></div>
  <span class="bleed" aria-hidden="true">{p['code']}</span>
  <div class="wrap"><div class="grid">
    <span class="tag" style="grid-column:1/-1;justify-self:start">{p['tag']}</span>
    <h1 id="titulo">{p['h1']}</h1>
    <p class="lead">{p['lead']}</p>
    <div class="cta"><a class="btn" href="#contacto" data-mag>{p['cta']}{ARROW}</a><p class="sign">Werkstatt</p></div>
    <div class="chips">{''.join(f'<span class="tag">{html.escape(c)}</span>' for c in p['chips'])}</div>
  </div></div>
</section>
''')
    # problema
    o.append(f'''<section class="sec" id="problema" aria-labelledby="problema-t" style="padding-top:0"><div class="wrap">
{hd('Lo que resuelve', p['hd_problema'], 'problema-t')}
<div class="trio">''' + ''.join(f'<article class="bezel{" sage" if i==1 else ""} reveal"><div class="core"><span class="num">{i+1}</span><h3>{t}</h3><p>{d}</p></div></article>' for i,(t,d) in enumerate(p['problemas'])) + '''</div></div></section>
''')
    # incluye
    o.append(f'''<section class="sec" id="incluye" aria-labelledby="incluye-t" style="padding-top:0"><div class="wrap">
{hd('Qué incluye', p['hd_incluye'], 'incluye-t')}
<div class="incl">''' + ''.join(f'<article class="bezel{" sage" if i==3 else ""}{" dark" if i==1 else ""} i{i+1} reveal"><div class="core"><h3{" style=\"color:var(--cream)\"" if i==1 else ""}>{t}</h3><p>{d}</p></div></article>' for i,(t,d) in enumerate(p['incluye'])) + '''</div></div></section>
''')
    # plano
    cls = 'showcase'
    sheets = ''
    for i,(lab,svg) in enumerate(p['planes']):
        pos = ('a','b')[i] if len(p['planes'])==2 else ''
        sheets += f'<article class="bezel {pos} reveal" style="{"grid-column:1/-1" if not pos else ""}"><div class="core"><span class="tag" style="align-self:flex-start">{lab}</span><div class="sheet draw" style="{"max-height:30rem" if not pos else ""}">{svg}</div></div></article>'
    o.append(f'''<section class="sec" id="plano" aria-labelledby="plano-t" style="padding-top:0"><div class="wrap">
<div class="head reveal"><i class="gl" aria-hidden="true"></i><span class="tag">En el plano</span><h2 id="plano-t">{p['plan_t']}</h2><p>{p['plan_p']}</p></div>
<div class="{cls}">{sheets}</div></div></section>
''')
    # proceso
    n = len(p['pasos'])
    o.append(f'''<section class="sec" id="proceso" aria-labelledby="proceso-t" style="padding-top:0"><div class="wrap">
{hd('Proceso', 'Cuatro pasos, siempre con el plano a la vista.', 'proceso-t')}
<ol class="steps" style="padding-bottom:9rem">''' + ''.join(f'<li class="reveal"><div class="bezel"><div class="core"><span class="num">{i+1}</span><h3>{t}</h3><p>{d}</p></div></div></li>' for i,(t,d) in enumerate(p['pasos'])) + '''</ol></div></section>
''')
    # faq
    o.append(f'''<section class="sec" id="preguntas" aria-labelledby="preguntas-t" style="padding-top:0"><div class="wrap">
{hd('Preguntas', 'Lo que casi todos preguntan antes de empezar.', 'preguntas-t')}
<div class="faq">''' + ''.join(f'<details class="bezel reveal"><summary><span>{q}</span>{PLUS}</summary><div class="ans"><p>{a}</p></div></details>' for q,a in p['faq']) + '''</div></div></section>
''')
    # contacto
    fields = ''.join(f'<label class="fl"><input type="{t}" name="{n}" placeholder=" " autocomplete="off"{" required" if k<2 else ""}><span>{l}</span></label>' for k,(l,t,n) in enumerate(p['campos']))
    o.append(f'''<section class="sec contact" id="contacto" aria-labelledby="contacto-t" style="padding-top:0"><div class="wrap">
<div class="bezel dark reveal"><div class="core">
<canvas class="dotgrid" aria-hidden="true"></canvas>
<span class="tag" style="background:rgba(253,251,247,.08);color:rgba(253,251,247,.7);box-shadow:0 0 0 1px rgba(253,251,247,.14) inset;align-self:flex-start">Contacto</span>
<h2 id="contacto-t">{p['cierre']}</h2>
<p style="max-width:56ch">Cuatro datos bastan para empezar. Con eso se puede conversar y decidir si hay algo que hacer juntos.</p>
<form class="f" data-demo novalidate="false"><div class="ff three">{fields}</div>
<p class="fnote">Formulario de muestra: no envía ni guarda nada. En una versión real aquí iría el aviso de privacidad del responsable de los datos.</p>
<button class="btn light" type="submit" style="align-self:flex-start;margin-top:1rem">Enviar{ARROW}</button>
<p class="ok" role="status" hidden></p></form>
</div></div></div></section>
</main>
<footer><div class="wrap row"><img src="../assets/logo/werkstatt-positivo.svg" alt="Werkstatt">
<p>Landing de muestra {p['code']}. Textos, proyectos y datos son de ejemplo y provisionales; no hay clientes, precios ni resultados reales. <a href="./">Ver las tres landings</a>.</p></div></footer>
<script src="app.js"></script>
</body>
</html>
''')
    return ''.join(o)

def index():
    items = ''.join(f'<li><a href="{p["file"]}"><b>Landing {p["code"]}</b><span>{html.escape(p["nav"])}</span></a></li>' for p in PAGES)
    return f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Landings de muestra | Werkstatt demo</title><meta name="robots" content="noindex">
<meta name="description" content="Tres landings de muestra con el sistema de diseño de Werkstatt. Contenido de ejemplo.">
<link rel="icon" href="../assets/logo/marca-positivo.svg" type="image/svg+xml">
<style>
@font-face{{font-family:"Geist";src:url("../fonts/geist-latin-wght-normal.woff2") format("woff2");font-weight:100 900;font-display:swap}}
:root{{--bg:#FAFAF8;--ink:#1A1A1A;--muted:#5F5848;--line:#D9D4C8}}
@media (prefers-color-scheme:dark){{:root{{--bg:#1A1A1A;--ink:#EDEBE4;--muted:#A8A396;--line:#3B3A36}}}}
body{{margin:0;background:var(--bg);color:var(--ink);font:400 17px/1.6 Geist,Arial,sans-serif}}
main{{max-width:760px;margin:0 auto;padding:clamp(32px,8vw,96px) 20px}}
h1{{font-weight:600;font-size:clamp(1.8rem,5vw,2.6rem);letter-spacing:-.02em;margin:0 0 12px}}
p{{color:var(--muted);margin:0 0 32px;max-width:56ch}}
ul{{list-style:none;margin:0;padding:0}}li{{border-top:1px solid var(--line)}}li:last-child{{border-bottom:1px solid var(--line)}}
a{{display:flex;justify-content:space-between;gap:16px;align-items:baseline;padding:20px 0;color:inherit;text-decoration:none;min-height:48px}}
a:focus-visible{{outline:2px solid var(--ink);outline-offset:2px}}b{{font-weight:600}}span{{color:var(--muted);font-size:14px;text-align:right}}
small{{display:block;margin-top:32px;color:var(--muted);font-size:13px}}
</style></head><body><main>
<h1>Landings de muestra</h1>
<p>Tres landings hechas con el sistema de diseño de Werkstatt para ver cómo funciona una página de captación. Contenido de ejemplo; no hay clientes, precios ni resultados reales.</p>
<ul>{items}</ul>
<small><a href="../" style="display:inline;padding:0;min-height:0;text-decoration:underline">Volver a las demos</a></small>
</main></body></html>
'''

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for p in PAGES:
        open(os.path.join(OUT, p['file']), 'w', encoding='utf-8').write(page(p))
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(index())
    print('ok')
