(function(){
  var b=document.body;
  var burger=document.querySelector('.burger'),menu=document.getElementById('menu');
  function toggle(open){
    var o=typeof open==='boolean'?open:!b.classList.contains('open');
    b.classList.toggle('open',o);burger.setAttribute('aria-expanded',o);
    burger.setAttribute('aria-label',o?'Cerrar menú':'Abrir menú');
  }
  burger.addEventListener('click',function(){toggle()});
  menu.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){toggle(false)})});
  document.addEventListener('keydown',function(e){if(e.key==='Escape')toggle(false)});
  try{
    if(matchMedia('(prefers-reduced-motion: reduce)').matches||!('IntersectionObserver' in window))return;
    document.querySelectorAll('.draw svg').forEach(function(svg){
      var i=0;svg.querySelectorAll('.w,.t:not(.d)').forEach(function(el){
        el.setAttribute('pathLength','1');el.style.strokeDasharray='1';el.style.strokeDashoffset='1';
        el.style.transition='stroke-dashoffset 1.6s cubic-bezier(.32,.72,0,1) '+(i*0.08).toFixed(2)+'s';i++;
      });
    });
    document.documentElement.classList.add('js');
    var io=new IntersectionObserver(function(es){es.forEach(function(e){
      if(!e.isIntersecting)return;
      e.target.classList.add('in');
      e.target.querySelectorAll('.draw svg .w,.draw svg .t').forEach(function(el){el.style.strokeDashoffset='0'});
      io.unobserve(e.target);
    })},{threshold:.15,rootMargin:'0px 0px -6% 0px'});
    document.querySelectorAll('.reveal').forEach(function(el){io.observe(el)});
  }catch(err){document.documentElement.classList.remove('js')}
})();

(function(){
  var rm=matchMedia('(prefers-reduced-motion: reduce)').matches,root=document.documentElement;
  var $=function(s,c){return Array.prototype.slice.call((c||document).querySelectorAll(s))};
  var ease=function(t){return t>=1?1:1-Math.pow(2,-10*t)};
  // T-04: letras del titular
  try{
    var h=document.querySelector('.hero h1');
    if(h&&!rm){
      h.setAttribute('aria-label',h.textContent.replace(/\s+/g,' ').trim());
      var n=0;
      (function walk(node){
        Array.prototype.slice.call(node.childNodes).forEach(function(c){
          if(c.nodeType===3){
            var f=document.createDocumentFragment();
            c.textContent.split(/(\s+)/).forEach(function(p){
              if(!p)return;
              if(/^\s+$/.test(p)){f.appendChild(document.createTextNode(' '));return}
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

/* Formulario de muestra: no envía nada */
(function(){
  document.querySelectorAll('form[data-demo]').forEach(function(f){
    var out=f.querySelector('.ok');
    f.addEventListener('submit',function(e){
      e.preventDefault();
      if(!f.checkValidity()){f.reportValidity();return}
      if(out){out.hidden=false;out.textContent='Formulario de muestra: no se envió ni se guardó nada.'}
    });
  });
})();
