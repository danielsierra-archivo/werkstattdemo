import re,sys,pathlib
S=pathlib.Path(sys.argv[1]); R=pathlib.Path('/home/claude/werkstattdemo')
base=(S/'tpl/taste-high-end.html').read_text()
plans=re.findall(r'<svg class="plan".*?</svg>',(S/'v1/index.html').read_text(),flags=re.S)
def build(variant):
    t=base
    def rep(a,b):
        nonlocal t
        assert a in t,a[:70]; t=t.replace(a,b)
    # fuentes
    t=re.sub(r'@font-face\{font-family:"Instrument Serif".*?\n','',t)
    t=re.sub(r'@font-face\{font-family:"Instrument Serif".*?\n','',t)
    ff='''@font-face{font-family:"Cormorant";src:url("../fonts/cormorant-latin-400-normal.woff2") format("woff2");font-weight:400;font-style:normal;font-display:swap}
@font-face{font-family:"Cormorant";src:url("../fonts/cormorant-latin-400-italic.woff2") format("woff2");font-weight:400;font-style:italic;font-display:swap}
@font-face{font-family:"Cormorant";src:url("../fonts/cormorant-latin-500-normal.woff2") format("woff2");font-weight:500;font-style:normal;font-display:swap}
@font-face{font-family:"Cormorant";src:url("../fonts/cormorant-latin-500-italic.woff2") format("woff2");font-weight:500;font-style:italic;font-display:swap}
@font-face{font-family:"Inter";src:url("../fonts/inter-latin-wght-normal.woff2") format("woff2");font-weight:100 900;font-display:swap}
@font-face{font-family:"Nothing You Could Do";src:url("../fonts/nothing-you-could-do-latin-400-normal.woff2") format("woff2");font-weight:400;font-display:swap}
@font-face{font-family:"Archivo Black";src:url("../fonts/archivo-black-latin-400-normal.woff2") format("woff2");font-weight:400;font-display:swap}
'''
    t=re.sub(r'@font-face\{font-family:"Geist".*?\n',lambda m:ff,t,count=1)
    assert 'Instrument' not in t.split('</style>')[0].split('--serif')[0]
    rep('--serif:"Instrument Serif","Iowan Old Style","Palatino Linotype",Georgia,serif;','--serif:"Cormorant","Cormorant Garamond",Georgia,serif;\n  --macro:"Archivo Black","Arial Black",Impact,sans-serif;\n  --sign:"Nothing You Could Do","Segoe Script",cursive;')
    rep('--sans:"Geist",ui-sans-serif,system-ui,sans-serif;','--sans:"Inter",ui-sans-serif,system-ui,sans-serif;')
    rep('<title>Werkstatt | Demo Taste: high-end visual design</title>',f'<title>Werkstatt | Demo v2{" B" if variant=="b" else " A"}</title>')
    rep('content="Demo de práctica. Página hecha siguiendo el método de la skill high-end-visual-design (Taste Skill, licencia MIT). Contenido de ejemplo."','content="Demo v2 de la web de Werkstatt: estructura y movimiento de la prueba high-end, títulos grandes y 2026 de puntos de la prueba brutalista, regla con centímetros de la prueba Impeccable, tipografías propias. Contenido de ejemplo."')
    # firma y titulares
    rep('.sign{font:italic 400 2.4rem/1 var(--serif);margin:0;letter-spacing:-.01em}','.sign{font:400 2.1rem/1.1 var(--sign);margin:0}')
    if variant=='a':
        rep('font:400 clamp(3.1rem,9.4vw,9.4rem)/.92 var(--serif);letter-spacing:-.035em;text-wrap:balance;max-width:14ch','font:400 clamp(3.4rem,11vw,11.4rem)/.88 var(--serif);letter-spacing:-.025em;text-wrap:balance;max-width:12ch')
        rep('font:400 clamp(2.3rem,5.4vw,4.8rem)/1 var(--serif);letter-spacing:-.03em;text-wrap:balance','font:400 clamp(2.7rem,6.4vw,6rem)/.95 var(--serif);letter-spacing:-.02em;text-wrap:balance')
    else:
        rep('font:400 clamp(3.1rem,9.4vw,9.4rem)/.92 var(--serif);letter-spacing:-.035em;text-wrap:balance;max-width:14ch','font:400 clamp(2.5rem,8vw,8.4rem)/.92 var(--macro);text-transform:uppercase;letter-spacing:-.045em;text-wrap:balance;max-width:13ch')
        rep('font:400 clamp(2.3rem,5.4vw,4.8rem)/1 var(--serif);letter-spacing:-.03em;text-wrap:balance','font:400 clamp(1.9rem,4.6vw,4.4rem)/.95 var(--macro);text-transform:uppercase;letter-spacing:-.045em;text-wrap:balance')
        rep('.hero h1 em{font-style:italic;color:var(--sage-deep)}','.hero h1 em{font-style:normal;color:var(--sage-deep)}')
    extra='''
/* 2026 de puntos (de la prueba brutalista), en verde salvia y detrás del contenido */
.hero{position:relative;overflow:hidden}
.hero .wrap{position:relative;z-index:2}
.bleed{position:absolute;right:-3vw;bottom:-.2em;font:400 min(44vw,40rem)/1 var(--macro);letter-spacing:-.06em;color:transparent;
  background:radial-gradient(circle,var(--sage) 34%,transparent 36%) 0 0/9px 9px;-webkit-background-clip:text;background-clip:text;opacity:.4;z-index:1;user-select:none;pointer-events:none}
@media (max-width:900px){.bleed{font-size:72vw;right:-10vw;opacity:.4}}
.core h3{font-weight:500}

/* Regla lateral (de la prueba Impeccable): marcas cada milímetro, número cada centímetro, se desplaza con la página. 1 cm = 37.795 px de CSS. */
.ruler{display:none}
@media (min-width:900px){
  body{padding-left:40px}
  .ruler{display:block;position:fixed;left:0;top:0;bottom:0;width:40px;z-index:45;background-color:var(--cream);box-shadow:1px 0 0 var(--ring);
    background-image:linear-gradient(var(--espresso) 1px,transparent 1px),linear-gradient(var(--soft) 1px,transparent 1px);
    background-size:16px 37.795px,8px 3.7795px;background-repeat:repeat-y;background-position:right calc(var(--y,0px) * -1),right calc(var(--y,0px) * -1)}
  .ruler output{position:absolute;left:0;bottom:1.25rem;width:40px;padding:.6rem 0;background:var(--cream);color:var(--sage-deep);font:500 .6875rem/1 var(--sans);letter-spacing:.04em;writing-mode:vertical-rl;transform:rotate(180deg);text-align:center;font-variant-numeric:tabular-nums}
}
'''
    rep('</style>',extra+'</style>')
    rep('<main id="inicio">','<div class="ruler" aria-hidden="true"><output id="cm">0.0 cm</output></div>\n<main id="inicio">')
    rep('  <section class="hero">\n','  <section class="hero">\n    <span class="bleed" aria-hidden="true">2026</span>\n')
    # JS regla
    rep('<script>\n(function(){','<script>\n(function(){\n  var rl=document.querySelector(".ruler"),cm=document.getElementById("cm"),tick=false;\n  function upd(){tick=false;var y=window.scrollY;rl.style.setProperty("--y",y+"px");cm.textContent=(y/37.795).toFixed(1)+" cm"}\n  addEventListener("scroll",function(){if(!tick){tick=true;requestAnimationFrame(upd)}},{passive:true});upd();',)
    # pie
    t=re.sub(r'(<footer>.*?<p>).*?(</p>)',r'\1Demo v2. Los proyectos, textos y datos son de ejemplo y provisionales. Estructura y movimiento tomados del método de la skill high-end-visual-design (Taste Skill, MIT); la regla del método de Impeccable (Apache-2.0). Sin texto ni código copiados.\2',t,flags=re.S,count=1)
    for i,p in enumerate(plans,1): t=t.replace(f'[[PLAN{i}]]',p)
    assert '[[' not in t
    d=R/('demo-v2-b' if variant=='b' else 'demo-v2'); d.mkdir(exist_ok=True); (d/'index.html').write_text(t)
build('a'); build('b'); print('ok')
