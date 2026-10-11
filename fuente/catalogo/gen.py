import sys,pathlib,html
S=pathlib.Path(sys.argv[1]); R=pathlib.Path('/home/claude/werkstattdemo')
exec((S/'cat/items.py').read_text())
cats={'N':'Números y texturas','T':'Texto','B':'Botones','C':'Tarjetas y superficies','A':'Animaciones de entrada','V':'Navegación','F':'Formularios','M':'Ambiente y fondos','D':'Decoración'}
star='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3.5l2.6 5.6 6.1.7-4.5 4.2 1.2 6-5.4-3-5.4 3 1.2-6L3.3 9.8l6.1-.7z"/></svg>'
rep='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 12a8 8 0 1 1-2.5-5.8M20 4v4.5h-4.5"/></svg>'
codes=[i[0] for i in I]; assert len(codes)==len(set(codes))
filters='<button type="button" data-cat="*" aria-pressed="true">Todo ('+str(len(I))+')</button>'+''.join(f'<button type="button" data-cat="{k}" aria-pressed="false">{v}</button>' for k,v in cats.items())
secs=[]
for k,v in cats.items():
    its=[i for i in I if i[1]==k]
    cards=[]
    for code,_,name,note,origin,v2,replay,h in its:
        r=f'<button class="rep" type="button" aria-label="Repetir {html.escape(name)}">{rep}</button>' if replay else ''
        st=' data-rep' if replay else ''
        meta=f'<span>Origen: {origin}</span>'+('<span class="v2">en demo v2</span>' if v2 else '')
        cards.append(f'<article class="spec" id="{code}"><header><span class="code">{code}</span><h3>{html.escape(name)}</h3>{r}<button class="fav" type="button" data-code="{code}" aria-pressed="false" aria-label="Favorito {code}">{star}</button></header><div class="stage"{st}>{h}</div><p class="note">{html.escape(note)}</p><div class="meta">{meta}</div></article>')
    secs.append(f'<section class="cat" data-cat="{k}" id="cat-{k}"><h2>{v}<small>{k}-01 a {k}-{len(its):02d}</small></h2><div class="grid">{"".join(cards)}</div></section>')
t=(S/'cat/template.html').read_text().replace('{{FILTERS}}',filters).replace('{{SECTIONS}}','\n'.join(secs))
d=R/'catalogo'; d.mkdir(exist_ok=True); (d/'index.html').write_text(t)
md=['# Códigos del catálogo','','Los códigos no se renumeran. Lo nuevo entra con el siguiente número de su letra.','']
for k,v in cats.items():
    md.append(f'## {k}: {v}'); 
    for code,_,name,note,origin,v2,_,_ in [i for i in I if i[1]==k]:
        md.append(f'- {code} {name}'+(' (en demo v2)' if v2 else ''))
    md.append('')
(d/'CODIGOS.md').write_text('\n'.join(md))
print(len(I),'piezas')
