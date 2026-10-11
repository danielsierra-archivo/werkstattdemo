import re,pathlib
R=pathlib.Path('/home/claude/werkstattdemo')
t=(R/'demo-v2-b/index.html').read_text()
def rep(a,b,count=1):
    global t
    assert a in t,a[:80]
    t=t.replace(a,b) if count==0 else t.replace(a,b,count)
rep('<title>Werkstatt | Demo v2 B</title>','<title>Werkstatt | Demo v3</title>')
t=re.sub(r'<meta name="description" content="[^"]*">','<meta name="description" content="Demo v3 de la web de Werkstatt: opción B de la v2 más las piezas elegidas del catálogo. Contenido de ejemplo.">',t,count=1)
ARR='<svg viewBox="0 0 24 8" aria-hidden="true"><path d="M0 4H22M18 1l4 3-4 3"/></svg>'
css='''
/* ===== v3: piezas del catálogo (códigos entre paréntesis) ===== */
/* M-03 manchas flotantes */
.blobs{position:absolute;inset:0;z-index:0;pointer-events:none;overflow:hidden}
.blobs i{position:absolute;width:46vw;max-width:640px;aspect-ratio:1;border-radius:50%;filter:blur(60px);opacity:.38}
.blobs i:nth-child(1){background:var(--sage);left:-8%;top:-10%;animation:blob1 18s ease-in-out infinite alternate}
.blobs i:nth-child(2){background:#E3C9A8;right:-6%;top:25%;animation:blob2 22s ease-in-out infinite alternate}
@keyframes blob1{to{transform:translate(30%,25%) scale(1.15)}}@keyframes blob2{to{transform:translate(-35%,-15%) scale(1.2)}}
/* A-08 capas con profundidad: el 2026 responde al cursor */
.hero{--dx:0;--dy:0}
.bleed{transform:translate(calc(var(--dx)*26px),calc(var(--dy)*16px));transition:transform .5s cubic-bezier(.16,1,.3,1)}
/* T-04 revelado por letras en el titular */
.hero h1 .wd{display:inline-block;white-space:nowrap}
.hero h1 .l{display:inline-block}
.letters-on .hero h1 .l{transition:transform 1s cubic-bezier(.16,1,.3,1),opacity 1s cubic-bezier(.16,1,.3,1);transition-delay:calc(var(--i)*28ms)}
.letters-on:not(.letters-go) .hero h1 .l{transform:translateY(55%) rotate(5deg);opacity:0}
/* B-03 botón magnético */
.btn[data-mag]{transition:transform .25s ease-out,background-color .7s var(--ease)}
/* B-05 enlace con flecha deslizante */
.arrow-link{grid-column:1/-1;justify-self:start;display:inline-flex;align-items:center;gap:.8rem;text-decoration:none;font:500 1rem var(--sans);margin-top:.5rem}
.arrow-link svg{width:2.2rem;height:.7rem;fill:none;stroke:currentColor;stroke-width:1.2;transition:transform .5s var(--ease),width .5s var(--ease)}
.arrow-link:hover svg,.arrow-link:focus-visible svg{width:3.4rem;transform:translateX(2px)}
/* A-06 línea que crece sobre cada encabezado */
.head .gl{grid-column:1/-1;display:block;height:1px;background:rgba(42,33,27,.55);transform-origin:left;transition:transform 1.4s cubic-bezier(.16,1,.3,1) .1s;margin-bottom:.5rem}
.js .head:not(.in) .gl{transform:scaleX(0)}
/* N-05 contadores */
.stats{display:flex;gap:clamp(1.5rem,5vw,4rem);margin-top:2.5rem}
.stats b{display:block;font:400 clamp(3rem,6vw,5rem)/1 var(--macro);letter-spacing:-.05em;font-variant-numeric:tabular-nums}
.stats span{font:500 .6875rem var(--sans);letter-spacing:.16em;text-transform:uppercase;color:var(--soft)}
.tag b{font-weight:600;font-variant-numeric:tabular-nums;margin-right:.45em}
/* N-09 número de proyecto */
.pn{display:block;font:400 clamp(2.6rem,4vw,3.6rem)/1 var(--macro);letter-spacing:-.05em;margin:0 0 .25rem}
/* A-03 cota que crece */
.gcota{display:flex;align-items:center;gap:1rem;font-size:.8125rem;color:var(--sage-deep)}
.gcota i{flex:1;position:relative;height:1px;background:var(--sage-deep);transform-origin:left;transition:transform 1.6s cubic-bezier(.16,1,.3,1) .3s}
.gcota i::before,.gcota i::after{content:"";position:absolute;top:-7px;width:1px;height:15px;background:var(--sage-deep)}
.gcota i::before{left:0}.gcota i::after{right:0}
.gcota span{flex:none;font-variant-numeric:tabular-nums}
.js .reveal:not(.in) .gcota i{transform:scaleX(0)}
/* C-04 plano que se vuelve a trazar al pasar el cursor, con trazo fantasma debajo */
.plan .ghost *{fill:none!important;stroke:rgba(42,33,27,.13)!important;stroke-dasharray:none!important;stroke-dashoffset:0!important;transition:none!important}
/* F-01 campos con etiqueta flotante (en el bisel oscuro) */
.ff{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:2rem;max-width:720px}
.fl{position:relative;display:block}
.fl input{width:100%;border:0;border-bottom:1px solid rgba(253,251,247,.45);background:transparent;padding:1.5rem 0 .5rem;font:400 1rem var(--sans);color:var(--cream);outline:0;border-radius:0}
.fl span{position:absolute;left:0;top:1.4rem;color:rgba(253,251,247,.6);transition:transform .4s var(--ease);transform-origin:left top;pointer-events:none}
.fl input:focus+span,.fl input:not(:placeholder-shown)+span{transform:translateY(-1.1rem) scale(.78)}
.fl input:focus{border-bottom:2px solid var(--sage)}
.ffnote{font-size:.8125rem;color:rgba(253,251,247,.55);margin:0}
@media (max-width:700px){.ff{grid-template-columns:1fr}}
/* N-08 cuadrícula de puntos reactiva en el contacto */
.contact .core{position:relative;overflow:hidden}
.contact .core>*:not(canvas){position:relative;z-index:1}
canvas.dotgrid{position:absolute;inset:0;width:100%;height:100%;z-index:0;pointer-events:none}
'''
rep('</style>',css+'</style>')
# hero: blobs, botón magnético
rep('<span class="bleed" aria-hidden="true">2026</span>','<div class="blobs" aria-hidden="true"><i></i><i></i></div>\n    <span class="bleed" aria-hidden="true">2026</span>')
rep('<a class="btn" href="#obra">Ver obra','<a class="btn" href="#obra" data-mag>Ver obra')
rep('<a class="btn" href="#contacto">Contacto','<a class="btn" href="#contacto" data-mag>Contacto')
# encabezados: línea que crece
t=t.replace('<div class="head reveal">\n        <span class="tag">','<div class="head reveal">\n        <i class="gl" aria-hidden="true"></i>\n        <span class="tag">')
assert t.count('class="gl"')==4,t.count('class="gl"')
# obra: contadores y números de proyecto
rep('Las fotos entran cuando existan y con permiso de quien habita la obra.</p>\n      </div>','Las fotos entran cuando existan y con permiso de quien habita la obra.</p>\n        <div class="stats" style="grid-column:1/-1"><div><b data-count="3">3</b><span>Proyectos</span></div><div><b data-count="5">5</b><span>Áreas</span></div><div><b data-count="4">4</b><span>Pasos</span></div></div>\n      </div>')
rep('<div class="meta"><span class="tag">Vivienda</span><span class="tag">51 m²</span>','<b class="pn">P-01</b>\n          <div class="meta"><span class="tag">Vivienda</span><span class="tag"><b data-count="51">51</b> m²</span>')
rep('<div class="meta"><span class="tag">Mueble</span>','<b class="pn">P-02</b>\n          <div class="meta"><span class="tag">Mueble</span>')
rep('<div class="meta"><span class="tag">Interiorismo</span><span class="tag">36 m²</span>','<b class="pn">P-03</b>\n          <div class="meta"><span class="tag">Interiorismo</span><span class="tag"><b data-count="36">36</b> m²</span>')
rep('<p class="cap">Planta. Cotas generales. Fotografía propia, pendiente.</p>','<div class="gcota"><i></i><span><b data-count="9.6" data-dec="2">9.60</b> m · planta general</span></div>\n          <p class="cap">Fotografía propia, pendiente.</p>',1)
# áreas: enlace con flecha
rep('<h2 id="areas-t">Un mismo taller para lo que se dibuja y lo que se toca.</h2>','<h2 id="areas-t">Un mismo taller para lo que se dibuja y lo que se toca.</h2>\n        <a class="arrow-link" href="#proceso">Ver el proceso '+ARR+'</a>')
# contacto: campos y nota
rep('<dl class="cf">','<div class="ff"><label class="fl"><input type="text" placeholder=" " autocomplete="off"><span>Tu nombre</span></label><label class="fl"><input type="text" placeholder=" " autocomplete="off"><span>Qué quieres resolver</span></label></div>\n        <p class="ffnote">Campos de muestra: aún no envían nada.</p>\n        <dl class="cf">')
rep('<div class="bezel dark reveal"><div class="core">\n        <span class="tag" style="background:rgba(253,251,247,.08)','<div class="bezel dark reveal"><div class="core">\n        <canvas class="dotgrid" aria-hidden="true"></canvas>\n        <span class="tag" style="background:rgba(253,251,247,.08)')
# pie
t=re.sub(r'(<footer>.*?<p>).*?(</p>)',r'\1Demo v3. Los proyectos, textos y datos son de ejemplo y provisionales. Piezas tomadas del catálogo de efectos, escritas desde cero con ideas de Taste Skill (MIT) e Impeccable (Apache-2.0), sin copiar su texto ni su código.\2',t,flags=re.S,count=1)
js='''
<script>
(function(){
  var rm=matchMedia('(prefers-reduced-motion: reduce)').matches,root=document.documentElement;
  var $=function(s,c){return Array.prototype.slice.call((c||document).querySelectorAll(s))};
  var ease=function(t){return t>=1?1:1-Math.pow(2,-10*t)};
  // T-04: letras del titular
  try{
    var h=document.querySelector('.hero h1');
    if(h&&!rm){
      h.setAttribute('aria-label',h.textContent.replace(/\\s+/g,' ').trim());
      var n=0;
      (function walk(node){
        Array.prototype.slice.call(node.childNodes).forEach(function(c){
          if(c.nodeType===3){
            var f=document.createDocumentFragment();
            c.textContent.split(/(\\s+)/).forEach(function(p){
              if(!p)return;
              if(/^\\s+$/.test(p)){f.appendChild(document.createTextNode(' '));return}
              var w=document.createElement('span');w.className='wd';w.setAttribute('aria-hidden','true');
              p.split('').forEach(function(ch){var l=document.createElement('span');l.className='l';l.style.setProperty('--i',n++);l.textContent=ch;w.appendChild(l)});
              f.appendChild(w);
            });
            node.replaceChild(f,c);
          }else if(c.nodeType===1){walk(c)}
        });
      })(h);
      root.classList.add('letters-on');
      requestAnimationFrame(function(){requestAnimationFrame(function(){root.classList.add('letters-go')})});
    }
  }catch(e){root.classList.remove('letters-on')}
  // A-08: el 2026 responde al cursor
  var hero=document.querySelector('.hero');
  if(hero&&!rm){
    hero.addEventListener('pointermove',function(e){var r=hero.getBoundingClientRect();hero.style.setProperty('--dx',((e.clientX-r.left)/r.width-.5)*2);hero.style.setProperty('--dy',((e.clientY-r.top)/r.height-.5)*2)});
    hero.addEventListener('pointerleave',function(){hero.style.setProperty('--dx',0);hero.style.setProperty('--dy',0)});
  }
  // B-03: botones magnéticos
  if(!rm)$('[data-mag]').forEach(function(b){
    b.addEventListener('pointermove',function(e){var r=b.getBoundingClientRect();b.style.transform='translate('+((e.clientX-r.left-r.width/2)*.25)+'px,'+((e.clientY-r.top-r.height/2)*.35)+'px)'});
    b.addEventListener('pointerleave',function(){b.style.transform=''});
  });
  // N-05: contadores al entrar en pantalla
  function count(el){
    var to=parseFloat(el.dataset.count),dec=+(el.dataset.dec||0),t0=null;
    if(rm){el.textContent=to.toFixed(dec);return}
    el.textContent=(0).toFixed(dec);
    function f(t){if(!t0)t0=t;var p=Math.min((t-t0)/1600,1);el.textContent=(to*ease(p)).toFixed(dec);if(p<1)requestAnimationFrame(f)}
    requestAnimationFrame(f);
  }
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){count(e.target);io.unobserve(e.target)}})},{threshold:.6});
    $('[data-count]').forEach(function(el){io.observe(el)});
  }
  // C-04: trazo fantasma y nuevo trazado al pasar el cursor
  $('.sheet.draw').forEach(function(sheet){
    var svg=sheet.querySelector('svg');if(!svg)return;
    var g=document.createElementNS('http://www.w3.org/2000/svg','g');g.setAttribute('class','ghost');g.setAttribute('aria-hidden','true');
    $('.w,.t',svg).forEach(function(p){var c=p.cloneNode(false);c.removeAttribute('style');c.removeAttribute('pathLength');c.removeAttribute('class');g.appendChild(c)});
    svg.insertBefore(g,svg.firstChild);
    var busy=false;
    if(rm)return;
    sheet.addEventListener('pointerenter',function(){
      if(busy)return;busy=true;
      var ps=$('.w,.t:not(.d)',svg).filter(function(p){return p.closest('.ghost')===null});
      ps.forEach(function(p,i){p.style.transition='none';p.style.strokeDashoffset='1';void p.getBoundingClientRect();p.style.transition='stroke-dashoffset 1.4s cubic-bezier(.32,.72,0,1) '+(i*0.06).toFixed(2)+'s';p.style.strokeDashoffset='0'});
      setTimeout(function(){busy=false},2200);
    });
  });
  // N-08: cuadrícula de puntos reactiva
  $('canvas.dotgrid').forEach(function(c){
    var core=c.parentNode,d,w,h,mx=-999,my=-999,step=20,run=false,g=c.getContext('2d');
    function size(){var r=c.getBoundingClientRect();d=Math.min(devicePixelRatio||1,2);c.width=Math.max(1,r.width*d);c.height=Math.max(1,r.height*d);w=c.width;h=c.height}
    function frame(){
      g.clearRect(0,0,w,h);var S=step*d,R=130*d;
      for(var y=S/2;y<h;y+=S)for(var x=S/2;x<w;x+=S){
        var k=Math.max(0,1-Math.hypot(x-mx,y-my)/R);
        g.fillStyle='rgba(253,251,247,'+(.14+.5*k*k)+')';
        g.beginPath();g.arc(x,y,S*(.07+.3*k*k),0,6.283);g.fill();
      }
      if(run)requestAnimationFrame(frame);
    }
    size();frame();
    addEventListener('resize',function(){size();frame()});
    if(rm)return;
    core.addEventListener('pointermove',function(e){var r=c.getBoundingClientRect();mx=(e.clientX-r.left)*d;my=(e.clientY-r.top)*d;if(!run){run=true;requestAnimationFrame(frame)}});
    core.addEventListener('pointerleave',function(){mx=my=-999;run=false;frame()});
  });
})();
</script>
</body>'''
rep('</body>',js)
d=R/'demo-v3'; d.mkdir(exist_ok=True); (d/'index.html').write_text(t); print('ok')
