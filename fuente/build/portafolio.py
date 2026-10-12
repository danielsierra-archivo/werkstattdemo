# Genera portafolio-daniel/index.html con los proyectos reales.
# Parte de la version anterior (con proyectos de ejemplo) guardada en git (commit d56f185).
# Uso, desde la raiz del repo: python3 fuente/build/portafolio.py
import re,subprocess,html
R=subprocess.check_output(["git","rev-parse","--show-toplevel"],text=True).strip()
old=subprocess.check_output(["git","show","d56f185:portafolio-daniel/index.html"],cwd=R,text=True)
s=old
E=html.escape

def sub1(pat,rep,flags=re.S,lit=False):
    # lit=True inserta el texto tal cual; si no, se expanden las referencias \\1 de los grupos
    global s
    n=len(re.findall(pat,s,flags))
    assert n==1,(pat,n)
    s=re.sub(pat,(lambda m:rep) if lit else (lambda m:m.expand(rep)),s,flags=flags)

# ---------- datos ----------
# fig: (archivo, ancho, alto, alt, leyenda)
def F(f,w,h,alt,cap): return dict(f=f,w=w,h=h,alt=alt,cap=cap)
P=[
dict(id="p01",n="P-01",titulo="Edificio departamental 01",sub="Vivienda vertical: material y ritmo",
 caj=[("Tipo","Vivienda vertical"),("Niveles","5"),("Materiales","Concreto, madera y vidrio")],imgs="renders, planta, alzados y cortes",
 textos=["Un edificio que nace de la tensión entre lo colectivo y lo privado. Cinco niveles que se apilan con orden pero respiran hacia el exterior a través de balcones, celosías de madera y grandes ventanales. La materialidad, concreto, madera y vidrio, no es decoración: es el argumento del proyecto."],
 ctx=("Contexto urbano","En una ciudad que crece sin parar, el edificio propone una alternativa contemporánea a la vivienda urbana. Cinco niveles que optimizan el suelo sin renunciar a la calidad espacial: una respuesta compacta, digna y bien resuelta para quienes eligen vivir en la ciudad."),
 media=F("p01-render-fachada-bn.webp",704,1521,"Render en blanco y negro de la fachada: cinco niveles con celosías de madera, balcones y grandes ventanales","Render · fachada"),
 media_cls="tall",
 filas=[
  [F("p01-render-posterior.webp",1513,636,"Render de la fachada posterior: muro central de ladrillo y, a los lados, niveles con celosías de madera","Render · fachada posterior")],
  [F("p01-planta.webp",2400,1109,"Planta arquitectónica del edificio con ejes, muros, mobiliario y núcleo de escaleras","Planta arquitectónica")],
  [F("p01-render-alzado-color.webp",480,787,"Render a color de un alzado con ejes de referencia","Render · alzado"),
   F("p01-fachada-lineas.webp",585,947,"Alzado de la fachada en líneas, con ejes y cotas","Alzado en líneas"),
   F("p01-corte-lineas.webp",468,768,"Corte transversal en líneas","Corte")],
  [F("p01-corte-escaleras.webp",1266,585,"Corte longitudinal con el núcleo de escaleras al centro","Corte · núcleo de escaleras")],
 ]),
dict(id="p02",n="P-02",titulo="Casa de cultura 02",sub="Espacio público, luz y silencio",
 caj=[("Tipo","Cultural"),("Programa","Auditorio, sala de proyección, taquilla y servicios"),("Partido","Volúmenes horizontales alrededor de patios")],imgs="renders, plantas y cortes",
 textos=["Un edificio que no compite con quien lo habita. Volúmenes puros y horizontales organizados alrededor de patios interiores que traen la naturaleza al centro de la vida cultural. La blancura no es ausencia sino invitación: cada vano, cada sombra, cada árbol plantado adentro forma parte del proyecto."],
 ctx=("Contexto y programa","El programa articula usos diversos, auditorio, sala de proyección, taquilla y áreas de servicio, sin perder la coherencia espacial del conjunto. La planta se lee como un recorrido: entras, el edificio te guía, y en cada giro aparece un patio, una pausa, una vista."),
 media=F("p02-isometrico-bn.webp",1354,768,"Vista isométrica en blanco y negro: volúmenes blancos alrededor de patios con vegetación","Render · isométrico"),
 media_cls="wide",
 filas=[
  [F("p02-isometrico-color.webp",1354,768,"Vista isométrica a color de los volúmenes blancos, patios y vegetación","Render · isométrico a color"),
   F("p02-planta-conjunto.webp",819,600,"Planta de conjunto con ejes y los volúmenes en gris","Planta de conjunto")],
  [F("p02-planta-muros.webp",1292,608,"Planta de muros con ejes de referencia","Planta de muros")],
  [F("p02-corte-entorno.webp",1976,346,"Corte en render con el entorno y la vegetación","Corte · con entorno")],
  [F("p02-corte-lineas.webp",2026,355,"Corte en líneas del conjunto","Corte")],
 ]),
dict(id="p03",n="P-03",titulo="Vivienda unifamiliar",sub="Documentación técnica",
 caj=[("Tipo","Vivienda unifamiliar"),("Niveles","1"),("Enfoque","Dibujo técnico")],imgs="planta y cortes",
 textos=["Ejercicio de representación arquitectónica enfocado en la precisión del dibujo técnico. Planta arquitectónica y cortes transversales que documentan la distribución interior de una vivienda unifamiliar de un solo nivel."],
 ctx=None,
 media=F("p03-planta.webp",988,1217,"Planta arquitectónica de la vivienda con mobiliario y cotas","Planta arquitectónica"),
 media_cls="plan",
 filas=[
  [F("p03-corte-superior.webp",1266,517,"Corte de la vivienda, titulado Cortes","Corte"),
   F("p03-corte-inferior.webp",1176,418,"Segundo corte de la vivienda","Corte")],
 ]),
]

def fig(d,extra="",lazy=True):
    a=d["w"]/d["h"]
    extra=(extra+(" wide" if a>1.5 else "")).strip()
    return (f'<figure class="fig {extra}" style="--a:{a:.3f}"><button class="zoom" type="button" data-full="img/{d["f"]}" data-cap="{E(d["cap"])}" aria-label="Ampliar: {E(d["cap"])}">'
            f'<span class="bezel"><span class="core"><img src="img/{d["f"]}" width="{d["w"]}" height="{d["h"]}" alt="{E(d["alt"])}" loading="lazy" decoding="async"></span></span></button>'
            f'<figcaption>{E(d["cap"])}</figcaption></figure>')

def caso(i,p):
    rev="rev" if i%2 else ""
    n_img=1+sum(len(f) for f in p["filas"])
    caj="".join(f'<div><dt>{E(a)}</dt><dd>{E(b)}</dd></div>' for a,b in p["caj"]+[("Imágenes",f'{n_img} · {p["imgs"]}')])
    ctx=f'<div class="ctx"><span class="tag">{E(p["ctx"][0])}</span><p>{E(p["ctx"][1])}</p></div>' if p["ctx"] else ""
    txt="".join(f"<p>{E(t)}</p>" for t in p["textos"])
    filas="".join('<div class="row reveal '+("multi" if len(fila)>1 else "one")+'">'+"".join(fig(f) for f in fila)+'</div>' for fila in p["filas"])
    return f'''
      <article class="case" id="{p["id"]}" aria-labelledby="{p["id"]}-t">
        <i class="gl" aria-hidden="true"></i>
        <div class="case-top {rev}">
          <div class="case-media {p["media_cls"]} reveal">{fig(p["media"])}</div>
          <div class="case-text reveal">
            <b class="pn">{p["n"]}</b>
            <h3 id="{p["id"]}-t">{E(p["titulo"])}</h3>
            <p class="sub">{E(p["sub"])}</p>
            {txt}
            <dl class="caj">{caj}</dl>
            {ctx}
          </div>
        </div>
        <div class="gal">{filas}</div>
      </article>'''

casos="".join(caso(i,p) for i,p in enumerate(P))
proyectos=f'''<section class="sec" id="proyectos" aria-labelledby="proyectos-t" style="padding-top:0">
    <div class="wrap">
      <div class="head reveal">
        <i class="gl" aria-hidden="true"></i>
        <span class="tag">Proyectos</span>
        <h2 id="proyectos-t">Tres proyectos, del volumen al plano.</h2>
        <p>Cada uno con sus imágenes y su documentación técnica. Toca cualquier imagen para verla más grande.</p>
        <a class="arrow-link" href="#marcas">Ver cómo se ordenan mis marcas <svg viewBox="0 0 24 8" aria-hidden="true"><path d="M0 4H22M18 1l4 3-4 3"/></svg></a>
      </div>
      {casos}
    </div>
  </section>'''

# ---------- CSS: quitar lo de los planos SVG de ejemplo ----------
for pat in [r'\n\.bleed\{.*?\}',r'\n@media \(max-width:900px\)\{\.bleed\{[^\n]*\}\}',r'\n/\* 2026 de puntos[^\n]*\*/',r'\n\.p1\{[^\n]*',r'\n\.p2,\.p3\{[^\n]*',r'\n\.sheet\{[^\n]*',r'\n\.p1 \.sheet\{[^\n]*',r'\nsvg\.plan\{[^\n]*',r'\n\.plan \.[a-z]+\{[^\n]*',r'\n/\* C-04[^\n]*\n\.plan \.ghost[^\n]*',r'\n\.bento\{[^\n]*']:
    s=re.sub(pat,'',s,flags=re.S if 'bleed{' in pat and 'media' not in pat else 0)
s=s.replace('/* Bento asimétrico de proyectos */','/* Proyectos */')
s=s.replace('.bento,.areas{grid-template-columns:minmax(0,1fr);gap:1rem}','.areas{grid-template-columns:minmax(0,1fr);gap:1rem}')
s=s.replace('.p1,.p2,.p3,.a1,.a2,.a3,.a4,.a5{grid-column:auto;grid-row:auto}','.a1,.a2,.a3,.a4,.a5{grid-column:auto;grid-row:auto}')
assert '.p1' not in s and 'svg.plan' not in s

# ---------- CSS nuevo ----------
css_new='''
/* ===== Portafolio con proyectos reales ===== */
/* Portada: el render de la presentación, mezclado con el fondo crema para que el degradado blanco se disuelva en la página */
.hero-img{position:absolute;right:0;bottom:0;width:min(56vw,900px);height:auto;z-index:1;mix-blend-mode:multiply;pointer-events:none;user-select:none;
  -webkit-mask-image:linear-gradient(90deg,transparent 0,#000 30%),linear-gradient(180deg,transparent 0,#000 30%,#000 92%,transparent 100%);-webkit-mask-composite:source-in;
  mask-image:linear-gradient(90deg,transparent 0,#000 30%),linear-gradient(180deg,transparent 0,#000 30%,#000 92%,transparent 100%);mask-composite:intersect}
/* Degradado general de puntos: más denso abajo a la izquierda y se desvanece hacia arriba a la derecha. Se mueve apenas con el cursor (A-08) */
.hero::before{content:"";position:absolute;inset:-24px;z-index:0;pointer-events:none;
  background:radial-gradient(circle,rgba(86,100,81,.6) 1.1px,transparent 1.7px) 0 0/16px 16px;
  -webkit-mask-image:linear-gradient(35deg,#000 0,rgba(0,0,0,.55) 38%,transparent 78%);mask-image:linear-gradient(35deg,#000 0,rgba(0,0,0,.55) 38%,transparent 78%);
  opacity:.55;transform:translate(calc(var(--dx)*8px),calc(var(--dy)*6px));transition:transform .6s var(--ease)}
.hero .side{grid-column:1/8;justify-self:start;margin-top:.5rem}
html{scroll-padding-top:5.5rem}

/* Caso de proyecto */
.case{margin-bottom:clamp(6rem,11vw,10rem)}
.case:last-child{margin-bottom:0}
.case>.gl{display:block;height:1px;background:rgba(42,33,27,.55);transform-origin:left;transition:transform 1.4s cubic-bezier(.16,1,.3,1) .1s;margin-bottom:clamp(2rem,4vw,3.5rem)}
.js .case:not(.in)>.gl{transform:scaleX(0)}
.case-top{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:clamp(1.5rem,3vw,3rem);align-items:start}
.case-media{grid-column:1/7}
.case-text{grid-column:8/-1;display:flex;flex-direction:column;gap:1.25rem;padding-top:.5rem}
.case-top.rev .case-media{grid-column:7/-1;grid-row:1}
.case-top.rev .case-text{grid-column:1/6;grid-row:1}
.case-media.tall{grid-column:1/6}
.case-media.plan{grid-column:1/6}
.case-top.rev .case-media.wide{grid-column:6/-1}
.case-text h3{margin:0;font:400 clamp(2rem,3.6vw,3.4rem)/1.02 var(--serif);letter-spacing:-.02em;font-weight:500;text-wrap:balance}
.case-text .sub{margin:0;padding-bottom:.9rem;border-bottom:1px solid rgba(42,33,27,.55);font:italic 400 clamp(1.25rem,1.8vw,1.6rem)/1.2 var(--serif);color:var(--espresso);max-width:none}
.case-text p{margin:0;color:var(--soft);max-width:54ch}
.case-text .ctx{display:flex;flex-direction:column;align-items:flex-start;gap:.75rem;margin-top:.75rem}
.case .pn{margin:0}

/* Figuras y galería */
.fig{margin:0;display:flex;flex-direction:column;gap:.6rem;min-width:0}
.fig figcaption{font:500 .625rem/1 var(--sans);letter-spacing:.2em;text-transform:uppercase;color:var(--soft);padding-left:.35rem}
.zoom{display:block;width:100%;padding:0;border:0;background:none;cursor:zoom-in;text-align:left;border-radius:var(--r-out);flex:1}
.zoom .bezel{display:block;height:100%;transition:transform .8s var(--ease),box-shadow .8s var(--ease)}
.zoom .core{display:flex;align-items:center;justify-content:center;padding:clamp(.5rem,1vw,.9rem);gap:0;background:var(--core)}
.zoom:hover .bezel,.zoom:focus-visible .bezel{transform:translateY(-4px);box-shadow:0 0 0 1px var(--ring),0 36px 60px -40px rgba(42,33,27,.4)}
.zoom img{display:block;width:100%;height:auto;border-radius:calc(var(--r-in) - .6rem);mix-blend-mode:multiply}
.case-media .zoom .core{background:var(--linen)}
.case-media.tall img{aspect-ratio:7/10;object-fit:cover;object-position:50% 88%}
.case-media.tall img,.case-media.wide img{border-radius:calc(var(--r-in) - .5rem)}
.case{scroll-margin-top:6rem}
.gal{display:grid;gap:1.5rem;margin-top:clamp(1.5rem,3vw,2.5rem)}
.row{display:flex;gap:1.5rem;align-items:stretch}
.row .fig{flex:var(--a) 1 0}
.row .zoom .core{background:var(--linen)}
.row .zoom img{height:100%;object-fit:contain}

/* C-08 imagen ampliable (propuesto, pendiente de aprobar) */
dialog.lb{border:0;padding:0;background:transparent;max-width:none;max-height:none;width:100vw;height:100dvh;overflow:hidden;color:var(--cream)}
dialog.lb::backdrop{background:rgba(42,33,27,.78);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px)}
dialog.lb[open]{display:grid;place-items:center;animation:lbin .5s var(--ease)}
@keyframes lbin{from{opacity:0}to{opacity:1}}
.lb .frame{position:relative;max-width:min(94vw,1500px);max-height:88dvh;display:flex;flex-direction:column;gap:.75rem;align-items:center}
.lb img{display:block;max-width:100%;max-height:calc(88dvh - 2.5rem);width:auto;height:auto;background:var(--core);border-radius:1rem;padding:clamp(.5rem,1.5vw,1.25rem)}
.lb .lc{font:500 .6875rem/1 var(--sans);letter-spacing:.2em;text-transform:uppercase;color:rgba(253,251,247,.75)}
.lb .x{position:fixed;top:1.25rem;right:1.25rem;width:2.75rem;height:2.75rem;border-radius:50%;border:0;background:rgba(253,251,247,.14);color:var(--cream);cursor:pointer;display:grid;place-items:center;transition:background-color .6s var(--ease),transform .6s var(--ease)}
.lb .x:hover{background:rgba(253,251,247,.26);transform:rotate(90deg)}
.lb .x svg{width:1rem;height:1rem;stroke:currentColor;stroke-width:1.2;fill:none;stroke-linecap:round}

/* Cierre: el boceto de la presentación, en línea clara sobre el bisel oscuro */
.contact .core>.sketch{position:absolute;right:0;bottom:0;width:min(62%,820px);height:auto;filter:invert(1);opacity:.34;z-index:0;pointer-events:none;user-select:none;
  -webkit-mask-image:linear-gradient(90deg,transparent 0,#000 34%),linear-gradient(180deg,#000 80%,transparent 100%);-webkit-mask-composite:source-in;
  mask-image:linear-gradient(90deg,transparent 0,#000 34%),linear-gradient(180deg,#000 80%,transparent 100%);mask-composite:intersect}
.cf{grid-template-columns:repeat(3,minmax(0,1fr))}
.cf dd a{color:inherit;text-decoration-color:rgba(253,251,247,.4);text-underline-offset:.2em}

@media (max-width:900px){
  .case-top,.case-top.rev{grid-template-columns:minmax(0,1fr);gap:1.75rem}
  .case-top .case-media,.case-top .case-text,.case-top.rev .case-media,.case-top.rev .case-text,.case-media.tall,.case-media.plan,.case-top.rev .case-media.wide{grid-column:1/-1;grid-row:auto}
  .case-media.tall{max-width:26rem}
  .case-media.plan{max-width:30rem}
  .row{flex-direction:column}
  .row .fig{flex:none}
  .row .zoom img{height:auto}
  .contact .core>.sketch{width:100%;opacity:.24}
  .lb .frame{max-width:100vw;overflow:auto;-webkit-overflow-scrolling:touch}
  .lb img{max-width:none;max-height:none;width:auto;height:min(70dvh,calc(200vw / var(--a,1)))}
  .cf{grid-template-columns:repeat(2,minmax(0,1fr))}
}


/* C-06 cajetín de plano: ficha de cada proyecto */
.caj{margin:.5rem 0 0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));border:1px solid rgba(42,33,27,.55)}
.caj div{padding:.75rem .9rem;border-right:1px solid rgba(42,33,27,.2);border-bottom:1px solid rgba(42,33,27,.2)}
.caj div:nth-child(2n){border-right:0}
.caj div:nth-last-child(-n+2){border-bottom:0}
.caj dt{font:500 .5625rem/1 var(--sans);letter-spacing:.2em;text-transform:uppercase;color:var(--soft);margin:0 0 .45rem}
.caj dd{margin:0;font:400 .9rem/1.35 var(--sans);color:var(--espresso)}

/* Perfil: listas de nivel y trayectoria */
.skills{list-style:none;margin:0;padding:0}
.skills li{display:flex;justify-content:space-between;gap:1rem;padding:.65rem 0;border-bottom:1px solid rgba(42,33,27,.14);font-size:.9375rem}
.skills li:last-child{border-bottom:0}
.skills em{font-style:normal;color:var(--soft);text-align:right}
.areas .a1{grid-column:span 5}.areas .a2{grid-column:span 3}.areas .a3{grid-column:span 4}
.areas .core{min-height:0;justify-content:flex-start;gap:1rem}
.tl-t{grid-column:1/9;margin:1.25rem 0 0;font:500 clamp(1.8rem,3vw,2.7rem)/1.05 var(--serif);letter-spacing:-.02em;text-wrap:balance}
.tl{list-style:none;margin:0;padding:0}
.tl li{display:grid;grid-template-columns:11rem minmax(0,1fr);gap:1.5rem;padding:1.5rem 0;border-top:1px solid rgba(42,33,27,.2)}
.tl li:last-child{border-bottom:1px solid rgba(42,33,27,.2)}
.tl .yr{font:400 clamp(1rem,1.5vw,1.25rem)/1.15 var(--macro);letter-spacing:-.03em}
.tl .where{display:block;font:500 .625rem/1 var(--sans);letter-spacing:.18em;text-transform:uppercase;color:var(--sage-deep);margin-bottom:.55rem}
.tl h4{margin:0 0 .35rem;font:500 1.0625rem/1.3 var(--sans)}
.tl p{margin:0;color:var(--soft);max-width:62ch}

/* D-06 hueco de foto pendiente + D-03 marcas de registro: espacio para el archivo físico escaneado */
.archive{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:2.75rem 1.5rem;align-items:start;padding-top:1rem}
.paper{margin:0;position:relative;transform:rotate(var(--r,0deg));transition:transform .8s var(--ease)}
.paper:hover{transform:rotate(0deg) translateY(-4px)}
.paper .scan{position:relative;display:grid;place-items:center;aspect-ratio:var(--ar,4/5);background:#FBF8F0;border-radius:2px;
  box-shadow:0 0 0 1px rgba(42,33,27,.08),0 20px 36px -24px rgba(42,33,27,.5)}
.paper .scan::before{content:"";position:absolute;inset:.75rem;border:1px dashed rgba(42,33,27,.28)}
.paper .scan::after{content:"";position:absolute;inset:1.1rem;pointer-events:none;
  background:
   linear-gradient(rgba(42,33,27,.5),rgba(42,33,27,.5)) left top/11px 1px no-repeat,linear-gradient(rgba(42,33,27,.5),rgba(42,33,27,.5)) left top/1px 11px no-repeat,
   linear-gradient(rgba(42,33,27,.5),rgba(42,33,27,.5)) right top/11px 1px no-repeat,linear-gradient(rgba(42,33,27,.5),rgba(42,33,27,.5)) right top/1px 11px no-repeat,
   linear-gradient(rgba(42,33,27,.5),rgba(42,33,27,.5)) left bottom/11px 1px no-repeat,linear-gradient(rgba(42,33,27,.5),rgba(42,33,27,.5)) left bottom/1px 11px no-repeat,
   linear-gradient(rgba(42,33,27,.5),rgba(42,33,27,.5)) right bottom/11px 1px no-repeat,linear-gradient(rgba(42,33,27,.5),rgba(42,33,27,.5)) right bottom/1px 11px no-repeat}
.paper .lab{position:relative;z-index:1;text-align:center;font:italic 400 clamp(1.1rem,1.7vw,1.45rem)/1.2 var(--serif);color:var(--soft);padding:0 1rem}
.paper .lab small{display:block;margin-top:.6rem;font:500 .5625rem/1 var(--sans);font-style:normal;letter-spacing:.2em;text-transform:uppercase}
.paper figcaption{margin-top:.85rem;font:500 .625rem/1 var(--sans);letter-spacing:.2em;text-transform:uppercase;color:var(--soft);padding-left:.25rem}
.tape{position:absolute;left:50%;top:-.8rem;width:5.5rem;height:1.6rem;translate:-50% 0;rotate:-3deg;background:rgba(227,201,168,.7);box-shadow:0 1px 2px rgba(42,33,27,.12);z-index:2}
.paper img.scan{display:block;width:100%;height:auto;aspect-ratio:auto;background:none;mix-blend-mode:multiply}
.paper img.scan::before,.paper img.scan::after{display:none}
.paper.s1{grid-column:1/6;--ar:4/5}
.paper.s2{grid-column:6/10;--ar:1/1;margin-top:3.5rem}
.paper.s3{grid-column:10/13;--ar:3/4;margin-top:1rem}
.paper.s4{grid-column:1/5;--ar:4/3;margin-top:1rem}
.paper.s5{grid-column:5/13;--ar:16/7}

/* Firma al final de la página (T-08: se escribe al entrar en pantalla) */
footer .foot-top{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:1.5rem}
.sigwrap{margin-top:3.5rem;padding-top:2rem;border-top:1px solid rgba(42,33,27,.2)}
.sign{font:400 clamp(2.6rem,9vw,5rem)/1.15 var(--sign);margin:0;clip-path:inset(0 0 0 0);transition:clip-path 2.4s cubic-bezier(.16,1,.3,1) .2s}
.js .sigwrap:not(.in) .sign{clip-path:inset(0 100% 0 0)}

@media (max-width:900px){
  .caj{margin-top:.25rem}
  .areas .a1,.areas .a2,.areas .a3{grid-column:auto}
  .tl li{grid-template-columns:minmax(0,1fr);gap:.6rem;padding:1.25rem 0}
  .tl-t{grid-column:1/-1}
  .archive{grid-template-columns:repeat(2,minmax(0,1fr));gap:2.25rem 1rem}
  .paper.s1,.paper.s4,.paper.s5{grid-column:1/-1}
  .paper.s2{grid-column:1/2;margin-top:0}
  .paper.s3{grid-column:2/3;margin-top:0}
  .paper.s5{--ar:16/9}
}

/* ===== Móvil: portada completa, más aire, carruseles y toques ===== */
@media (hover:none){
  .zoom .core{position:relative}
  .zoom .core::after{content:"";position:absolute;right:.7rem;top:.7rem;width:2rem;height:2rem;border-radius:50%;background:rgba(253,251,247,.92) url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'><path d='M8 3.5v9M3.5 8h9' stroke='%232A211B' stroke-width='1.2' stroke-linecap='round' fill='none'/></svg>") center/.9rem no-repeat;box-shadow:0 0 0 1px var(--ring);pointer-events:none}
}
@media (max-width:900px){
  /* Portada: título y render primero (de borde a borde); el texto, más chico, va debajo */
  .hero{display:flex;flex-direction:column;align-items:stretch;min-height:0;padding-block:6rem 0}
  .hero>.wrap,.hero .grid{display:contents}
  .hero .tag,.hero h1,.hero .lead,.hero .side{position:relative;z-index:2;margin-inline:1.5rem}
  .hero .tag{order:1;align-self:flex-start;line-height:1.6;padding:.5rem .9rem;border-radius:1rem;margin-top:0}
  .hero h1{order:2;margin-top:1.1rem;max-width:none}
  .hero picture{order:3;display:block;position:relative;z-index:1;margin-top:-.25rem}
  .hero-img{position:relative;right:auto;bottom:auto;display:block;width:100%;height:auto;opacity:1;
    -webkit-mask-image:linear-gradient(90deg,transparent 0,#000 12%),linear-gradient(180deg,transparent 0,#000 18%,#000 94%,transparent 100%);-webkit-mask-composite:source-in;
    mask-image:linear-gradient(90deg,transparent 0,#000 12%),linear-gradient(180deg,transparent 0,#000 18%,#000 94%,transparent 100%);mask-composite:intersect}
  .hero .lead{order:4;margin-top:.75rem;font-size:.9375rem;line-height:1.6;max-width:none}
  .hero .side{order:5;margin-top:1.5rem;margin-bottom:3.5rem;align-self:flex-start}
  .hero::before{opacity:.45}

  /* Ritmo: más aire entre secciones y menos huecos dentro de las tarjetas */
  .sec{padding-block:5rem}
  .head{gap:1rem;margin-bottom:2.25rem}
  .areas .core{min-height:0;justify-content:flex-start;gap:.75rem}
  .areas{gap:1rem}
  .steps{padding-bottom:0!important;gap:1rem}
  .case{margin-bottom:5.5rem}
  .case-top,.case-top.rev{gap:1.75rem}
  .case-text{gap:1rem;padding-top:0}
  .case-text .sub{padding-bottom:.75rem}

  /* Galería: las filas con varias imágenes pasan a carrusel horizontal */
  .gal{gap:1.5rem;margin-top:2rem}
  .row.multi{flex-direction:row;gap:1rem;overflow-x:auto;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch;scrollbar-width:none;
    margin:-.5rem -1.5rem;padding:.5rem 1.5rem 1rem;scroll-padding-inline:1.5rem;overscroll-behavior-x:contain}
  .row.multi::-webkit-scrollbar{display:none}
  .row.multi .fig{flex:0 0 min(74%,19rem);scroll-snap-align:start}
  .row.multi .fig.wide{flex-basis:min(88%,26rem)}
  .row.multi{align-items:flex-start}
  .row.multi .zoom{flex:none}
  .row.multi .zoom .bezel,.row.multi .zoom .core{height:auto}
  .row.multi .zoom img{height:auto}

  /* Contacto: una columna para que el correo no se encime */
  .contact .core{padding:2rem 1.5rem}
  .cf{grid-template-columns:minmax(0,1fr);gap:1.5rem}
  .cf dd{overflow-wrap:anywhere;font-size:1.25rem}
  .ff{gap:1.25rem}
  footer{padding-block:2.5rem 3.5rem}
}
@media (max-width:480px){
  .island .logo{white-space:nowrap;font-size:1.1rem}
  .island{padding-left:1rem}
  .wrap{width:calc(100% - 2.5rem)}
  .hero .tag,.hero h1,.hero .lead,.hero .side{margin-inline:1.25rem}
  .row.multi{margin-inline:-1.25rem;padding-inline:1.25rem;scroll-padding-inline:1.25rem}
  .stats{gap:1.5rem;flex-wrap:wrap}
  .stats b{font-size:clamp(2.4rem,11vw,3rem)}
}
'''
sub1(r'\n</style>',css_new+'</style>',lit=True)

# ---------- cabecera ----------
sub1(r'<title>.*?</title>','<title>Daniel Sierra | Portafolio</title>')
sub1(r'<meta name="description"[^>]*>','<meta name="description" content="Portafolio de Daniel Sierra, egresado de Arquitectura: edificio departamental, casa de cultura y vivienda unifamiliar, con renders, plantas y cortes.">')

# ---------- portada ----------
sub1(r'<span class="bleed" aria-hidden="true">2026</span>','<picture><source media="(max-width:900px)" srcset="img/portada-m.webp" width="740" height="893"><img class="hero-img" src="img/portada.webp" width="960" height="893" alt="Render del edificio departamental de cinco niveles con celosías de madera, entre árboles, con el cielo claro de fondo" decoding="async" fetchpriority="high"></picture>')
sub1(r'\n\s*<p class="sign">Daniel Sierra</p>','')


# ---------- proyectos ----------
sub1(r'<section class="sec" id="proyectos".*?</section>',proyectos,lit=True)

# ---------- preguntas ----------
sub1(r'<span>¿Dónde puedo ver proyectos reales\?</span>(.*?)<p>.*?</p></div></details>',r'<span>¿Qué incluye cada proyecto?</span>\1<p>Imágenes del proyecto y su documentación técnica: plantas, cortes y alzados. Toca cualquier imagen para verla más grande.</p></div></details>')
sub1(r'<p>Los datos de contacto aún están por definir en esta demo\. Mientras tanto, mi diario está en @derstahlbeton\.</p>','<p>Por correo, desde la sección de contacto. Mi diario está en @derstahlbeton, en Instagram.</p>')

# ---------- contacto ----------
sub1(r'<canvas class="dotgrid" aria-hidden="true"></canvas>',r'<canvas class="dotgrid" aria-hidden="true"></canvas>'+'\n        <img class="sketch" src="img/cierre-boceto.webp" width="1376" height="768" alt="" aria-hidden="true" loading="lazy" decoding="async">')
sub1(r'<p class="ffnote">.*?</p>','<p class="ffnote">Al escribir, se abre tu correo con el mensaje listo.</p>')
sub1(r'<dl class="cf">.*?</dl>','<dl class="cf">\n          <div><dt>Correo</dt><dd><a href="mailto:danielsierrayanez@icloud.com">danielsierrayanez@icloud.com</a></dd></div>\n          <div><dt>Ubicación</dt><dd>Ciudad de México</dd></div>\n          <div><dt>Redes</dt><dd>@derstahlbeton</dd></div>\n        </dl>')
sub1(r'<span class="btn off".*?</span></span>','<a class="btn" id="mailto" href="mailto:danielsierrayanez@icloud.com?subject=Portafolio%20Daniel%20Sierra" style="align-self:flex-start" data-mag>Escribir<span class="ico"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4.5 11.5 11.5 4.5M5.5 4.5h6v6"/></svg></span></a>')
sub1(r'<span>Tu nombre</span>','<span>Tu nombre</span>')
s=s.replace('<div class="ff"><label class="fl"><input type="text"','<div class="ff"><label class="fl"><input type="text" id="f-nombre" name="nombre"').replace('</span></label><label class="fl"><input type="text" placeholder=" " autocomplete="off">','</span></label><label class="fl"><input type="text" id="f-msg" name="mensaje" placeholder=" " autocomplete="off">')
assert 'id="f-msg"' in s and 'id="f-nombre"' in s

# ---------- pie ----------
sub1(r'<p>Portafolio personal, demo\..*?</p>\n  </div>\n</footer>','<p>Portafolio personal de Daniel Sierra. Piezas tomadas del catálogo de efectos, escritas desde cero con ideas de Taste Skill (MIT) e Impeccable (Apache-2.0), sin copiar su texto ni su código. Tipografías con licencia SIL OFL 1.1.</p>\n  </div>\n</footer>')


# ---------- metadatos sociales ----------
U="https://danielsierra-archivo.github.io/werkstattdemo/portafolio-daniel/"
sub1(r'(<meta name="description"[^>]*>)',r'\1'+f'\n<meta property="og:title" content="Daniel Sierra | Portafolio">\n<meta property="og:description" content="Egresado de Arquitectura. Edificio departamental, casa de cultura y vivienda unifamiliar.">\n<meta property="og:type" content="website">\n<meta property="og:image" content="{U}img/og.jpg">\n<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:image" content="{U}img/og.jpg">',lit=False)

# ---------- navegacion ----------
sub1(r'<a href="#proyectos">Proyectos</a><a href="#marcas">Marcas</a><a href="#preguntas">Preguntas</a>\n  </nav>',r'<a href="#proyectos">Proyectos</a><a href="#archivo">Archivo</a><a href="#marcas">Marcas</a><a href="#preguntas">Preguntas</a>\n  </nav>')
sub1(r'<a href="#proyectos">Proyectos</a><a href="#marcas">Marcas</a><a href="#preguntas">Preguntas</a><a href="#contacto">Contacto</a>',r'<a href="#proyectos">Proyectos</a><a href="#archivo">Archivo</a><a href="#marcas">Marcas</a><a href="#preguntas">Preguntas</a><a href="#contacto">Contacto</a>')
sub1(r'(body\.open \.sheetnav a:nth-child\(5\)\{transition-delay:\.3s\})',r'\1\nbody.open .sheetnav a:nth-child(6){transition-delay:.35s}')

# ---------- perfil ----------
arrow='<svg viewBox="0 0 24 8" aria-hidden="true"><path d="M0 4H22M18 1l4 3-4 3"/></svg>'
tl=[("2022 – 2025","Universidad Lucerna","Licenciatura en Arquitectura","Egreso de la carrera de Arquitectura."),
("2023","Trabajo en equipo","Proyecto Aula Lúdica","Proyecto desarrollado en equipo durante la carrera."),
("2024","Talleres","Normativa Urbana y Licencias · Análisis de Riesgo y Topografía","Dos talleres que acercan el proyecto a lo que se pide en trámite y en terreno."),
("Jun – Ago 2024","Experiencia","Coordinación de operaciones","Seguimiento de actividades y recursos de operación."),
("Ago 2024 – Ago 2025","Experiencia","Auxiliar en compras y suministros","Compras, abastecimiento e inventario: la parte de la obra que se decide antes de construir."),
("2026","Formación","Diplomado en Proyectos a Escala","Formación complementaria en proyecto.")]
tlh="".join(f'<li class="reveal"><div class="yr">{a}</div><div><span class="where">{b}</span><h4>{c}</h4><p>{d}</p></div></li>' for a,b,c,d in tl)
perfil=f"""<section class="sec" id="perfil" aria-labelledby="perfil-t">
    <div class="wrap">
      <div class="head reveal">
        <i class="gl" aria-hidden="true"></i>
        <span class="tag">Perfil</span>
        <h2 id="perfil-t">Quién soy, sin adornos.</h2>
        <p>Egresado de Arquitectura por la Universidad Lucerna. Me interesan los proyectos donde el diseño, la planificación y la administración de recursos se piensan juntos, porque un edificio también se decide en la compra, en el inventario y en el calendario.</p>
        <div class="stats" style="grid-column:1/-1"><div><b data-count="3">3</b><span>Proyectos</span></div><div><b data-count="2">2</b><span>Talleres</span></div><div><b data-count="2">2</b><span>Idiomas</span></div></div>
      </div>
      <div class="areas">
        <div class="bezel sage a1 reveal"><div class="core"><h3>Herramientas</h3><ul class="skills"><li>AutoCAD<em>Intermedio</em></li><li>Revit<em>Intermedio</em></li><li>Photoshop<em>Nociones básicas</em></li><li>Canva<em>Presentaciones</em></li><li>Office y Google Workspace<em>Paquetería</em></li><li>Planos digitales y físicos<em>Lectura y gestión</em></li></ul></div></div>
        <div class="bezel a2 reveal"><div class="core"><h3>Idiomas</h3><ul class="skills"><li>Español<em>Nativo</em></li><li>Inglés<em>B2</em></li></ul></div></div>
        <div class="bezel dark a3 reveal"><div class="core"><h3 style="color:var(--cream)">Mirada</h3><p>Documento la ciudad con el celular, desde la ventana de un tren o desde la calle. Fotografío piedras, etiquetas y espacios, sin personas y sin pulir de más.</p></div></div>
        <h3 class="tl-t reveal">Trayectoria. De la formación al oficio.</h3>
        <ol class="tl" style="grid-column:1/-1">{tlh}</ol>
      </div>
    </div>
  </section>"""
sub1(r'<section class="sec" id="perfil".*?</section>',perfil,lit=True)

# ---------- archivo ----------
slots=[("s1","A-01","Croquis","Escaneo pendiente","-1.2deg"),("s2","A-02","Libreta","Escaneo pendiente","1deg"),("s3","A-03","Notas de obra","Escaneo pendiente","-.6deg"),("s4","A-04","Maqueta","Escaneo pendiente","1.4deg"),("s5","A-05","Dibujo a mano","Escaneo pendiente","-.5deg")]
sl="\n        ".join(f'<figure class="paper {c} reveal" style="--r:{r}"><i class="tape" aria-hidden="true"></i><div class="scan" role="img" aria-label="Espacio reservado para {n.lower()} escaneado"><span class="lab">{n}<small>{m}</small></span></div><figcaption>{code}</figcaption></figure>' for c,code,n,m,r in slots)
archivo=f"""<section class="sec" id="archivo" aria-labelledby="archivo-t" style="padding-top:0">
    <div class="wrap">
      <div class="head reveal">
        <i class="gl" aria-hidden="true"></i>
        <span class="tag">Archivo</span>
        <h2 id="archivo-t">Lo que se queda en papel.</h2>
        <p>Croquis, notas de obra, maquetas y esos dibujos que no llegaron a plano. Aquí irán, escaneados tal cual, con sus dobleces y tachones.</p>
      </div>
      <!-- Para llenar un espacio: sustituye el div.scan por <img class="scan" src="img/archivo-xx.webp" width=".." height=".." alt="descripción" loading="lazy"> dentro de la misma figure. -->
      <div class="archive">
        {sl}
      </div>
    </div>
  </section>

  """
sub1(r'(  <section class="sec" id="preguntas")',archivo+r'\1',lit=False)

# ---------- preguntas (CV) ----------
sub1(r'(<span>¿Con qué programas trabajas\?</span>.*?<div class="ans"><p>).*?(</p></div></details>)',r'\1AutoCAD y Revit en nivel intermedio para dibujo y modelado, Photoshop en nociones básicas, Canva para presentaciones y Office y Google Workspace para documentos. También leo y gestiono planos digitales y físicos.\2')
sub1(r'(<details class="bezel reveal"><summary><span>¿Cómo te contacto\?</span>)',r'<details class="bezel reveal"><summary><span>¿Hay proyectos hechos en equipo?</span><span class="plus"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 3v10M3 8h10"/></svg></span></summary><div class="ans"><p>Sí. El proyecto Aula Lúdica, de 2023, lo desarrollé en equipo durante la carrera.</p></div></details>\n        \1')

# ---------- contacto / pie ----------
sub1(r'<dd>Ciudad de México</dd>','<dd>Zona metropolitana de la Ciudad de México</dd>')
sub1(r'<footer>\s*<div class="wrap row">\s*<span class="nm">Daniel Sierra</span>\s*<p>(.*?)</p>\s*</div>\s*</footer>',r'<footer>\n  <div class="wrap">\n    <div class="foot-top row">\n      <span class="nm">Daniel Sierra</span>\n      <p>\1</p>\n    </div>\n    <div class="sigwrap reveal"><p class="sign">Daniel Sierra</p></div>\n  </div>\n</footer>')

# ---------- JS: quitar C-04 de planos SVG, agregar lightbox y correo ----------
sub1(r'  // C-04: trazo fantasma.*?(  // N-08)',r'\1')
js_new='''
<dialog class="lb" id="lb" aria-label="Imagen ampliada">
  <button class="x" type="button" aria-label="Cerrar"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3.5 3.5l9 9M12.5 3.5l-9 9"/></svg></button>
  <div class="frame"><img alt=""><span class="lc"></span></div>
</dialog>
<script>
(function(){
  // C-08: imagen ampliable con <dialog>
  var lb=document.getElementById('lb'),img=lb.querySelector('img'),lc=lb.querySelector('.lc');
  document.querySelectorAll('.zoom').forEach(function(b){
    b.addEventListener('click',function(){
      var im=b.querySelector('img');img.src=b.dataset.full;img.alt=im?im.alt:'';if(im)img.style.setProperty('--a',(im.getAttribute('width')/im.getAttribute('height')).toFixed(3));lc.textContent=b.dataset.cap||'';
      if(typeof lb.showModal==='function')lb.showModal();else window.open(b.dataset.full,'_blank');
    });
  });
  lb.addEventListener('click',function(e){if(e.target===lb||e.target.classList.contains('frame')||e.target.closest('.x'))lb.close()});
  lb.addEventListener('close',function(){img.removeAttribute('src')});
  // Correo con el mensaje listo
  var a=document.getElementById('mailto'),n=document.getElementById('f-nombre'),m=document.getElementById('f-msg');
  function mk(){
    var body='Hola, soy '+(n.value.trim()||'[tu nombre]')+'.'+(m.value.trim()?'\\n\\n'+m.value.trim():'');
    a.href='mailto:danielsierrayanez@icloud.com?subject='+encodeURIComponent('Portafolio Daniel Sierra')+'&body='+encodeURIComponent(body);
  }
  if(a&&n&&m){n.addEventListener('input',mk);m.addEventListener('input',mk)}
})();
</script>
</body>'''
sub1(r'\n</body>',js_new,lit=True)
open(R+"/portafolio-daniel/index.html","w",encoding="utf8").write(s)
print("ok",len(s))
