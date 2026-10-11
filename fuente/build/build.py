import re,sys,pathlib
S=pathlib.Path(sys.argv[1]); R=pathlib.Path('/home/claude/werkstattdemo')
v1=(S/'v1/index.html').read_text()
plans=re.findall(r'<svg class="plan".*?</svg>',v1,flags=re.S)
assert len(plans)==3
def inject(t):
    for i,p in enumerate(plans,1): t=t.replace(f'[[PLAN{i}]]',p)
    assert '[[' not in t
    return t
for tpl,out in [('taste-high-end','taste-high-end'),('taste-brutalist','taste-brutalist'),('impeccable','impeccable')]:
    (R/out).mkdir(exist_ok=True)
    (R/out/'index.html').write_text(inject((S/'tpl'/f'{tpl}.html').read_text()))

# Rediseño de v1: se parte del HTML original y se aplican los cambios de la auditoría.
h=v1
def rep(a,b,n=1):
    global h
    assert h.count(a)>=1,a[:60]
    h=h.replace(a,b)
# 1 fuentes locales (sin CDN), Inter -> Geist
h=re.sub(r'<link rel="preconnect"[^>]*>\s*','',h)
h=re.sub(r'<link rel="stylesheet" href="https://fonts.googleapis.com[^>]*>','<link rel="icon" href="../assets/logo/marca-positivo.svg" type="image/svg+xml">',h)
rep("<title>Werkstatt</title>","<title>Werkstatt | Rediseño de la demo v1</title>")
rep("Demo v1 de la web portafolio de Werkstatt. Contenido de ejemplo.","Rediseño de la demo v1 aplicando la auditoría de la skill redesign-existing-projects (Taste Skill, MIT). Contenido de ejemplo.")
fonts='''<style>
@font-face{font-family:"Cormorant";src:url("../fonts/cormorant-latin-400-normal.woff2") format("woff2");font-weight:400;font-style:normal;font-display:swap}
@font-face{font-family:"Cormorant";src:url("../fonts/cormorant-latin-400-italic.woff2") format("woff2");font-weight:400;font-style:italic;font-display:swap}
@font-face{font-family:"Cormorant";src:url("../fonts/cormorant-latin-500-normal.woff2") format("woff2");font-weight:500;font-style:normal;font-display:swap}
@font-face{font-family:"Geist";src:url("../fonts/geist-latin-wght-normal.woff2") format("woff2");font-weight:100 900;font-display:swap}
@font-face{font-family:"Nothing You Could Do";src:url("../fonts/nothing-you-could-do-latin-400-normal.woff2") format("woff2");font-weight:400;font-display:swap}
'''
rep("<style>\n",fonts,1)
rep("--f-body:'Inter',Arial,Helvetica,sans-serif;","--f-body:'Geist',Arial,Helvetica,sans-serif;")
# 2 limpieza de color: el gris de línea pasa a un tono cálido, el texto secundario sube de contraste
rep("--line:#CCCCCC;","--line:#D9D4C8;")
rep("--muted:#736A59;","--muted:#6A6150;")
# 3 CSS de la auditoría
extra='''
/* Auditoría aplicada (redesign-existing-projects):
   1 tipografía: Inter cambia por Geist; cuerpo con text-wrap pretty y números tabulares.
   2 color: línea cálida en vez de gris neutro; texto secundario con más contraste.
   3 estados: hover, foco y presionado en enlaces, filas y resumen de preguntas.
   4 estructura: encabezado fijo con línea fina, etiqueta de sección pegajosa, enlace de salto.
   5 huecos de contenido: recuadros de foto con diseño propio en lugar de un cuadro gris vacío.
   6 detalles: selección de texto en el color del acento, barra de desplazamiento y cursor de campo con tema. */
body{font-variant-numeric:tabular-nums;font-feature-settings:"ss01"}
p{text-wrap:pretty}
::selection{background:var(--accent);color:var(--bg)}
html{scroll-behavior:smooth;scrollbar-color:var(--muted) var(--bg);scroll-padding-top:80px}
.skip{position:absolute;left:12px;top:-60px;background:var(--ink);color:var(--bg);padding:8px 12px;font-size:14px;z-index:30}
.skip:focus{top:12px}
.top{position:sticky;top:0;z-index:20;background:color-mix(in srgb,var(--bg) 94%,transparent);border-bottom:1px solid var(--line);padding-block:14px;margin-inline:calc(var(--gutter) * -1);padding-inline:var(--gutter)}
.hero{border-top:0}
.lab{position:sticky;top:96px;align-self:start}
.row.proj .fields{position:sticky;top:96px;align-self:start}
@media (max-width:820px){.lab,.row.proj .fields{position:static}.top{position:static}}
.row.tight{transition:background-color .35s var(--ease),padding-left .35s var(--ease)}
.row.tight:hover{background:var(--tone);padding-left:12px}
.top nav a[aria-current],.top nav a:active{background-size:100% 1px}
a:active{opacity:.7}
summary{transition:color .25s var(--ease);min-height:48px;align-items:center}
summary:hover{color:var(--accent)}
summary::after{transition:transform .4s var(--ease)}
.box.photo{background:repeating-linear-gradient(135deg,var(--tone2) 0 1px,var(--tone) 1px 14px);color:var(--muted);letter-spacing:.02em}
.todo{border-bottom:1px dashed var(--line);display:inline-block;padding-bottom:2px}
.cfields dd{min-height:1.6em}
.hero-copy .lead{max-width:36em}
@media (hover:hover){.proj:hover h3{color:var(--accent);transition:color .3s var(--ease)}}
'''
rep("</style>",extra+"</style>")
rep('<body>\n','<body>\n<a class="skip" href="#inicio">Saltar al contenido</a>\n')
rep('<div class="wrap">\n  <header class="top">','<div class="wrap">\n  <header class="top">')
rep("Demo v1. Los proyectos","Rediseño de la demo v1. Los proyectos")
(R/'rediseno-demo-v1').mkdir(exist_ok=True)
(R/'rediseno-demo-v1'/'index.html').write_text(h)
print('ok')
