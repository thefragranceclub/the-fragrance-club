# Genera favicon, páginas por perfume y colección, sitemap y datos para Google.
# Solo usa datos públicos de tienda/data.json. Lo corre sync.py en cada cambio.
import json,re,unicodedata,datetime,html,os,shutil,urllib.parse
from PIL import Image,ImageDraw
R='/home/claude/the-fragrance-club';W='https://thefragranceclub.studio'
d=json.load(open('/home/claude/tienda/data.json'));PS=d['productos'];TEL=d['whatsapp']
BR=["Carolina Herrera","Emporio Armani","Lattafa","Armaf","Afnan","Azzaro","Halloween","Scandal"]
AR={"Lattafa","Armaf","Afnan"};IG="https://www.instagram.com/theefragranceclub/"
e=html.escape;mx=lambda n:f"${n:,.0f}"
def j(l):
    l=list(l);return l[0] if len(l)==1 else ', '.join(l[:-1])+' y '+l[-1]
def slug(s):
    s=unicodedata.normalize('NFD',s.lower());s=''.join(c for c in s if not unicodedata.combining(c));return re.sub(r'[^a-z0-9]+','-',s).strip('-')
def lista(v): return v if isinstance(v,list) else [x.strip() for x in re.split(r'[·,]',v) if x.strip()]
def uso_txt(u):
    E=[('invierno','invierno'),('primavera','primavera'),('verano','verano'),('otono','otoño')]
    t=max(u[k] for k,_ in E);es=[n for k,n in E if u[k]>=t*.8]
    a,b=u['dia'],u['noche'];h='de día o de noche' if min(a,b)>=max(a,b)*.8 else ('de día' if a>b else 'de noche')
    return j(es),h
for p in PS:
    m=re.match(r'^(.*?)\s+(\d+ ml.*)$',p['nombre']);full,ml=(m[1],m[2]) if m else (p['nombre'],'')
    b=next((x for x in BR if full.startswith(x)),'')
    p['marca']='Jean Paul Gaultier' if b=='Scandal' else b;p['ml']=ml
    p['corto']=full if b in('Scandal','Halloween') else full[len(b):].strip()
    p['tit']=(p['marca']+' '+p['corto']) if b not in('Halloween',) else p['corto']
    p['slug']=slug(p['tit']);p['url']=f"/perfumes/{p['slug']}/"
    p['arabe']=p['marca'] in AR;p['tipo']='árabe' if p['arabe'] else 'de diseñador';p['para']=p['categoria'].lower()
MIN=min(p['menudeo'] for p in PS);MAX=max(p['menudeo'] for p in PS);MINM=min(p['mayoreo'] for p in PS)
COL=[
('perfumes-originales-torreon','Perfumes originales en Torreón',lambda p:True,f"Perfumes originales en Torreón desde {mx(MIN)} | The Fragrance Club",f"Perfumes originales en Torreón, árabes y de diseñador, desde {mx(MIN)}. Pick up o envío a domicilio en Torreón. Pide por WhatsApp.",f"The Fragrance Club es una perfumería en línea en Torreón, Coahuila. Aquí encuentras perfumes originales para hombre y mujer de casas árabes como Lattafa, Armaf y Afnan, y de diseñador como Carolina Herrera, Azzaro, Jean Paul Gaultier y Emporio Armani, desde {mx(MIN)}."),
('perfumes-arabes-torreon','Perfumes árabes en Torreón',lambda p:p['arabe'],f"Perfumes árabes en Torreón: Lattafa, Armaf y Afnan | TFC",f"Perfumes árabes originales en Torreón: Lattafa Yara, Asad, Club de Nuit, Odyssey y Afnan 9pm desde {mx(MIN)}. Menudeo y mayoreo.",f"Los perfumes árabes son famosos por su duración y por sus notas intensas de vainilla, ámbar y especias, a un precio mucho más accesible que el de muchos perfumes de diseñador. Tenemos Lattafa, Armaf y Afnan en Torreón desde {mx(MIN)}."),
('perfumes-a-mayoreo-torreon','Perfumes a mayoreo en Torreón',lambda p:True,f"Perfumes a mayoreo en Torreón desde {mx(MINM)} | The Fragrance Club",f"Compra perfumes originales a mayoreo en Torreón desde {d['mayoreoMin']} piezas, combinando modelos. Precios desde {mx(MINM)} por pieza.",f"Desde {d['mayoreoMin']} piezas, combinadas como quieras, todo tu pedido pasa a precio de mayoreo. Es la forma más barata de comprar perfumes originales con nosotros, ya sea para ti, para regalar o para revender, con precios desde {mx(MINM)} por pieza."),
('perfumes-para-hombre-torreon','Perfumes para hombre en Torreón',lambda p:p['categoria']=='Hombre',"Perfumes para hombre originales en Torreón | The Fragrance Club","Perfumes para hombre originales en Torreón: Stronger With You, Scandal, 212 VIP Black, Asad, 9pm y más. Menudeo y mayoreo.","Perfumes de hombre árabes y de diseñador, para la oficina, para salir de noche o para el frío de invierno. Cada perfume incluye sus notas y la temporada en la que mejor funciona."),
('perfumes-para-mujer-torreon','Perfumes para mujer en Torreón',lambda p:p['categoria']=='Mujer',"Perfumes para mujer originales en Torreón | The Fragrance Club","Perfumes para mujer originales en Torreón: Lattafa Yara, Yara Candy, Yara Tous y Club de Nuit Woman. Menudeo y mayoreo.","Perfumes de mujer dulces, frutales y florales, entre ellos la línea Yara de Lattafa y Club de Nuit Woman de Armaf, con precio de menudeo y de mayoreo."),
]
CSS=""":root{--bg:#EFEBE6;--panel:#F8F5F1;--ink:#141312;--soft:#625E59;--line:#D2CCC4;--ok:#2F5D46;--serif:"Bodoni Moda","Bodoni 72","Didot",Georgia,serif;--sans:"Jost","Futura","Avenir Next","Segoe UI",system-ui,sans-serif}
*{box-sizing:border-box}html{-webkit-font-smoothing:antialiased}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.55 var(--sans);overflow-x:clip}a{color:inherit}img{max-width:100%}
.top{background:var(--panel);border-bottom:1px solid var(--line)}.in{width:min(1040px,100%);margin:auto;padding-inline:20px}.top .in{display:flex;align-items:center;justify-content:space-between;min-height:68px}.top img{display:block;height:46px;width:auto}.top a.cat{font-size:15px;font-weight:500}
.ruta{font-size:14px;color:var(--soft);padding-block:20px 0}.ruta a{color:inherit}
h1{font:500 clamp(36px,6vw,54px)/1.08 var(--serif);margin:10px 0 8px;text-wrap:balance}h2{font:500 28px/1.15 var(--serif);margin:0 0 10px}
.sub{color:var(--soft);margin:0 0 22px}.intro{max-width:720px;margin:0 0 26px}
.ficha{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);gap:36px;padding-block:8px 44px;align-items:start}.foto{border-radius:12px;overflow:hidden;background:#6E5848 url(/img/fondo-perfume.webp) left 62%/cover;display:grid;place-items:center;aspect-ratio:1.08}.foto img{width:84%;height:80%;object-fit:contain;filter:drop-shadow(0 14px 12px rgba(30,26,20,.42))}
.pre{display:flex;gap:36px;margin:18px 0}.pre span{display:block;font-size:14px;color:var(--soft)}.pre b{font-weight:500;font-size:28px}.disp{color:var(--ok);font-weight:500}.agot{color:#A63B32;font-weight:500}
.btn{display:block;text-align:center;text-decoration:none;font-weight:500;padding:14px 18px;margin-top:10px;border:1px solid var(--ink);border-radius:8px}.btn.a{background:var(--ink);color:#FBF8F4}
.notas{padding:0;list-style:none;margin:0}.notas li{padding:9px 0;border-top:1px solid var(--line)}.notas b{font-weight:500}
.bloque{padding-block:30px;border-top:1px solid var(--line)}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;padding-bottom:44px}.card{background:var(--panel);text-decoration:none;display:block;border-radius:12px;overflow:hidden}.card .ph{height:190px;background:#6E5848 url(/img/fondo-perfume.webp) left 62%/cover;display:grid;place-items:center}.card img{width:84%;height:150px;object-fit:contain}.card div.t{padding:12px 14px 15px}.card small{display:block;color:var(--soft);font-size:13px}.card b{font:500 21px/1.18 var(--serif);display:block}.card span{font-size:15px}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin:0;padding:0;list-style:none}.chips a{display:block;border:1px solid var(--line);border-radius:6px;padding:6px 12px;font-size:15px;text-decoration:none}
footer{text-align:center;color:var(--soft);font-size:14px;padding:30px 20px 44px;border-top:1px solid var(--line)}
@media(max-width:760px){.ficha{grid-template-columns:1fr;gap:20px}.grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.card .ph{height:150px}.card img{height:118px}.card b{font-size:18px}}"""
def icons():
    logo=Image.open('/home/claude/img/tfc-k.png').convert('RGBA');logo=logo.crop(logo.getbbox())
    def ic(n,pad=.15,rad=.2,s=4):
        N=n*s;c=Image.new('RGBA',(N,N),(0,0,0,0));ImageDraw.Draw(c).rounded_rectangle([0,0,N-1,N-1],radius=int(N*rad),fill=(245,241,236,255))
        k=N*(1-2*pad)/max(logo.size);l=logo.resize((int(logo.width*k),int(logo.height*k)),Image.LANCZOS);c.alpha_composite(l,((N-l.width)//2,(N-l.height)//2));return c.resize((n,n),Image.LANCZOS)
    wh,tr=open('/home/claude/tienda/tfc-trazo.txt').read().split('\n',1);w,h=map(int,wh.split());L=max(w,h);ox,oy=(L-w)/2,(L-h)/2;M=L*.05
    open(f'{R}/favicon.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-M} {-M} {L+2*M} {L+2*M}"><style>path{{fill:#141312;fill-rule:evenodd;stroke:#141312;stroke-width:7;stroke-linejoin:round}}.h{{fill:none;stroke:#F5F1EC;stroke-width:26}}@media (prefers-color-scheme:dark){{path{{fill:#fff;stroke:#fff}}.h{{display:none}}}}</style><g transform="translate({ox} {oy})"><path class="h" d="{tr}"/><path d="{tr}"/></g></svg>')
    def tr_ic(n):
        k=n*4;c=Image.new('RGBA',(k,k),(0,0,0,0));q=k*.92/max(logo.size);l=logo.resize((int(logo.width*q),int(logo.height*q)),Image.LANCZOS);c.alpha_composite(l,((k-l.width)//2,(k-l.height)//2));return c.resize((n,n),Image.LANCZOS)
    tr_ic(48).save(f'{R}/favicon.ico',sizes=[(16,16),(32,32),(48,48)],append_images=[tr_ic(32),tr_ic(16)])
    if os.path.exists(f'{R}/favicon-96.png'): os.remove(f'{R}/favicon-96.png')
    ic(192).save(f'{R}/icon-192.png');ic(512).save(f'{R}/icon-512.png')
    ic(180,pad=.17,rad=0).convert('RGB').save(f'{R}/apple-touch-icon.png')
    json.dump({"name":"The Fragrance Club","short_name":"TFC","icons":[{"src":"/icon-192.png","sizes":"192x192","type":"image/png"},{"src":"/icon-512.png","sizes":"512x512","type":"image/png"}],"theme_color":"#141312","background_color":"#F5F1EC","display":"standalone","start_url":"/"},open(f'{R}/site.webmanifest','w'))
    m=Image.open('/home/claude/img/muro.webp').convert('RGB');k=630/m.height;m=m.resize((int(m.width*k),630),Image.LANCZOS).crop((0,0,1200,630)).convert('RGBA')
    m.alpha_composite(Image.new('RGBA',m.size,(20,13,9,70)))
    w=Image.open('/home/claude/img/logo-w.png').convert('RGBA');w=w.resize((760,int(760*w.height/w.width)),Image.LANCZOS);m.alpha_composite(w,((1200-760)//2,(630-w.height)//2))
    m.convert('RGB').save(f'{R}/img/og.jpg',quality=86)
ICONOS='<link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" type="image/svg+xml" href="/favicon.svg"><link rel="apple-touch-icon" href="/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest"><meta name="theme-color" content="#141312">'
TIENDA={"@context":"https://schema.org","@type":"Store","@id":W+"/#tienda","name":"The Fragrance Club","url":W+"/","logo":W+"/icon-512.png","image":W+"/img/og.jpg","telephone":"+"+TEL,"priceRange":f"{mx(MINM)} - {mx(MAX)} MXN","currenciesAccepted":"MXN","paymentAccepted":"Transferencia, depósito en OXXO","description":"Perfumes originales árabes y de diseñador en Torreón, a menudeo y mayoreo.","address":{"@type":"PostalAddress","addressLocality":"Torreón","addressRegion":"Coahuila","addressCountry":"MX"},"areaServed":{"@type":"City","name":"Torreón"},"sameAs":[IG]}
def ld(o): return '<script type="application/ld+json">'+json.dumps(o,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')+'</script>'
def ofer(p): return {"@type":"Offer","url":W+p['url'],"price":p['menudeo'],"priceCurrency":"MXN","availability":"https://schema.org/"+("InStock" if p['stock']>0 else "OutOfStock"),"itemCondition":"https://schema.org/NewCondition","seller":{"@id":W+"/#tienda"}}
def wa(t): return f"https://wa.me/{TEL}?text="+urllib.parse.quote(t)
def base(titulo,desc,ruta,cuerpo,datos,img='/img/og.jpg',tipo='website'):
    return f"""<!doctype html><html lang="es-MX"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(titulo)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{W}{ruta}">{ICONOS}
<meta property="og:type" content="{tipo}"><meta property="og:site_name" content="The Fragrance Club"><meta property="og:locale" content="es_MX"><meta property="og:title" content="{e(titulo)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{W}{ruta}"><meta property="og:image" content="{W}{img}"><meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:opsz,wght@6..96,400;6..96,500&family=Jost:wght@400;500;600&display=swap"><link rel="stylesheet" href="/pagina.css">
{''.join(ld(x) for x in datos)}</head><body><header class="top"><div class="in"><a href="/" aria-label="The Fragrance Club, inicio"><img src="/img/tfc-k.png" alt="The Fragrance Club" width="43" height="46"></a><a class="cat" href="/#catalogo">Ver catálogo</a></div></header><main class="in">{cuerpo}</main><footer>{pie()}</footer></body></html>"""
def pie(): return f'The Fragrance Club · Perfumes originales en Torreón, Coahuila · <a href="/">Inicio</a> · <a href="{IG}" rel="noopener">Instagram</a>'
def tarjeta(p): return f'<a class="card" href="{p["url"]}"><div class="ph"><img src="/{e(p["img"])}" alt="{e(p["tit"])} {e(p["ml"])} original" loading="lazy"></div><div class="t"><small>{e(p["marca"])}</small><b>{e(p["corto"])}</b><span>{mx(p["menudeo"])} · mayoreo {mx(p["mayoreo"])}</span></div></a>'
def enlaces():
    return ''.join(f'<li><a href="/{c[0]}/">{e(c[1])}</a></li>' for c in COL)
ENTREGA="<p>Recoge tu perfume con pick up en Torreón o pide envío a domicilio en Torreón por $%d. Pagas por transferencia o depósito en OXXO y confirmamos tu pedido por WhatsApp.</p>"%d['costoEnvio']
def pag_prod(p):
    st=p['stock'];pi=p.get('piramide');u=p.get('uso');temp,hora=uso_txt(u) if u else ('','')
    nt=''
    txt=f"{p['tit']} {p['ml']} es un perfume {p['tipo']} original para {p['para']}"
    if u: txt+=f" que funciona mejor en {temp}, {hora}"
    txt+='.'
    if pi:
        s,c,b=[j(x.lower() for x in lista(pi[k])) for k in('salida','corazon','base')]
        txt+=f" Abre con {s}, sigue con {c} y termina con {b}."
        nt=f'<ul class="notas"><li><b>Salida:</b> {e(j(lista(pi["salida"])))}</li><li><b>Corazón:</b> {e(j(lista(pi["corazon"])))}</li><li><b>Base:</b> {e(j(lista(pi["base"])))}</li></ul>'
    desc=f"{p['tit']} {p['ml']} original en Torreón: {mx(p['menudeo'])} menudeo y {mx(p['mayoreo'])} mayoreo. Pick up o envío a domicilio. Pide por WhatsApp."
    rel=[x for x in PS if x['id']!=p['id'] and x['categoria']==p['categoria']]
    rel=sorted(rel,key=lambda x:(x['marca']!=p['marca'],abs(x['menudeo']-p['menudeo'])))[:3]
    disp=f'<p class="disp">Disponible</p>' if st>1 else (f'<p class="disp">Quedan pocas piezas</p>' if st==1 else '<p class="agot">Agotado</p>')
    col=COL[3] if p['categoria']=='Hombre' else COL[4]
    btn=(f'<a class="btn a" href="/#perfume-{p["id"]}">Agregar al carrito</a>' if st>0 else '')+f'<a class="btn" href="{e(wa("Hola, me interesa el "+p["nombre"]+"."))}" rel="noopener">Preguntar por WhatsApp</a>'
    cu=f"""<nav class="ruta"><a href="/">Inicio</a> › <a href="/{col[0]}/">{e(col[1])}</a> › {e(p['tit'])}</nav>
<div class="ficha" style="margin-top:18px"><div class="foto"><img src="/{e(p['img'])}" alt="Perfume {e(p['tit'])} {e(p['ml'])} original" width="800" height="650"></div><div><h1>{e(p['tit'])}</h1><p class="sub">{e(p['ml'])} · Perfume {e(p['tipo'])} para {e(p['para'])}</p>{disp}<div class="pre"><div><span>Menudeo</span><b>{mx(p['menudeo'])}</b></div><div><span>Mayoreo, desde {d['mayoreoMin']} piezas</span><b>{mx(p['mayoreo'])}</b></div></div>{btn}</div></div>
<section class="bloque"><h2>Cómo huele</h2><p class="intro">{e(txt)}</p>{nt}</section>
<section class="bloque"><h2>Entrega en Torreón</h2>{ENTREGA}<ul class="chips">{enlaces()}</ul></section>
<section class="bloque"><h2>También te puede gustar</h2><div class="grid">{''.join(tarjeta(x) for x in rel)}</div></section>"""
    prod={"@context":"https://schema.org","@type":"Product","name":f"{p['tit']} {p['ml']}","image":W+'/'+p['img'],"brand":{"@type":"Brand","name":p['marca']},"sku":f"TFC-{p['id']}","category":"Perfumes","description":txt,"offers":ofer(p)}
    bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Inicio","item":W+"/"},{"@type":"ListItem","position":2,"name":col[1],"item":f"{W}/{col[0]}/"},{"@type":"ListItem","position":3,"name":p['tit']}]}
    return base(f"{p['tit']} {p['ml']} original en Torreón | TFC",desc,p['url'],cu,[TIENDA,prod,bc],'/'+p['img'],'product')
def pag_col(c):
    sl,nom,f,tit,desc,intro=c;ps=sorted([p for p in PS if f(p)],key=lambda x:((x['stock']<=0),x['menudeo']))
    cu=f"""<nav class="ruta"><a href="/">Inicio</a> › {e(nom)}</nav><h1>{e(nom)}</h1><p class="intro">{e(intro)}</p><div class="grid">{''.join(tarjeta(p) for p in ps)}</div><section class="bloque"><h2>Entrega en Torreón</h2>{ENTREGA}<ul class="chips">{enlaces()}</ul></section>"""
    il={"@context":"https://schema.org","@type":"ItemList","name":nom,"itemListElement":[{"@type":"ListItem","position":i+1,"url":W+p['url'],"name":p['tit']} for i,p in enumerate(ps)]}
    return base(tit,desc,f'/{sl}/',cu,[TIENDA,il])
def home():
    f=f'{R}/index.html';s=open(f,encoding='utf8').read()
    # Todo lo de Google y el logo debe ir dentro de <head>; el cuerpo empieza en la barra superior.
    s=s.replace('</head><body>\n','').replace('</head><body>','').replace('<div class="top"><div><div class="logo">','</head><body>\n<div class="top"><div><div class="logo">',1)
    tit="Perfumes originales en Torreón | The Fragrance Club"
    desc=f"Perfumes originales en Torreón, árabes y de diseñador, desde {mx(MIN)}. Lattafa, Armaf, Afnan, Armani y más. Mayoreo desde {d['mayoreoMin']} piezas."
    s=re.sub(r'<title>.*?</title>',f'<title>{e(tit)}</title>',s,count=1)
    s=s.replace('<h1><img src="img/logo-w.png" alt="The Fragrance Club">','<h1><img src="img/logo-w.png" alt="The Fragrance Club, perfumes originales en Torreón">')
    s=re.sub(r'<meta name="description" content="[^"]*">',f'<meta name="description" content="{e(desc)}">',s,count=1)
    s=re.sub(r'<!--seo:head-->.*?<!--/seo:head-->\n?','',s,flags=re.S)
    prods=[{"@type":"Product","name":f"{p['tit']} {p['ml']}","image":W+'/'+p['img'],"brand":{"@type":"Brand","name":p['marca']},"url":W+p['url'],"offers":ofer(p)} for p in PS]
    cab=f"""<!--seo:head--><link rel="canonical" href="{W}/">{ICONOS}<meta property="og:type" content="website"><meta property="og:site_name" content="The Fragrance Club"><meta property="og:locale" content="es_MX"><meta property="og:title" content="{e(tit)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{W}/"><meta property="og:image" content="{W}/img/og.jpg"><meta name="twitter:card" content="summary_large_image">{ld(TIENDA)}{ld({"@context":"https://schema.org","@type":"WebSite","name":"The Fragrance Club","alternateName":"TFC","url":W+"/"})}{ld({"@context":"https://schema.org","@type":"ItemList","name":"Catálogo de perfumes","itemListElement":[{"@type":"ListItem","position":i+1,"item":x} for i,x in enumerate(prods)]})}<!--/seo:head-->
"""
    s=s.replace('<title>',cab+'<title>',1)
    bloque=f"""<!--seo--><section class="seo" aria-labelledby="seoT"><style>.seo{{padding:44px 0 8px;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:26px 44px}}.seo h2{{font-size:clamp(28px,4vw,38px);grid-column:1/-1}}.seo h3{{font-family:var(--sans);font-size:16px;font-weight:600;margin:0 0 3px}}.seo p{{margin:0 0 15px;color:var(--soft);font-size:16px}}.seo ul{{list-style:none;margin:0 0 18px;padding:0;display:flex;flex-wrap:wrap;gap:7px}}.seo li a{{display:block;border:1px solid var(--line);padding:5px 11px;border-radius:6px;font-size:14px;text-decoration:none;color:var(--ink)}}.seo li a:hover{{background:var(--panel)}}@media(max-width:760px){{.seo{{grid-template-columns:1fr}}}}</style>
<h2 id="seoT">Perfumes originales en Torreón</h2>
<div><p>The Fragrance Club es una perfumería en línea en Torreón, Coahuila. Vendemos perfumes originales para hombre y mujer, árabes y de diseñador, desde {mx(MIN)}. Si buscas perfumes baratos sin renunciar a que sean originales, empieza por los árabes de Lattafa, Armaf y Afnan.</p>
<h3>¿Venden a mayoreo?</h3><p>Sí. Desde {d['mayoreoMin']} piezas, combinadas como quieras, todo tu pedido pasa a precio de mayoreo, desde {mx(MINM)} por pieza.</p>
<h3>¿Cómo los recibo?</h3><p>Con pick up en Torreón o con envío a domicilio en Torreón por ${d['costoEnvio']}. Si estás en La Laguna, puedes recogerlo con pick up.</p>
<h3>¿Cómo pago?</h3><p>Por transferencia o depósito en OXXO. Confirmamos tu pedido por WhatsApp.</p></div>
<div><h3>Explora</h3><ul>{enlaces()}</ul><h3>Perfumes árabes</h3><ul>{''.join(f'<li><a href="{p["url"]}">{e(p["tit"])}</a></li>' for p in PS if p['arabe'])}</ul><h3>Perfumes de diseñador</h3><ul>{''.join(f'<li><a href="{p["url"]}">{e(p["tit"])}</a></li>' for p in PS if not p['arabe'])}</ul></div></section><!--/seo-->
"""
    s=re.sub(r'<!--seo-->.*?<!--/seo-->\n?','',s,flags=re.S)
    a=' <footer><img src="img/tfc-k.png"';assert s.count(a)==1
    s=s.replace(a,bloque+a)
    open(f,'w',encoding='utf8').write(s)
def main():
    icons();open(f'{R}/pagina.css','w',encoding='utf8').write(CSS)
    for x in ['perfumes']+[c[0] for c in COL]: shutil.rmtree(f'{R}/{x}',ignore_errors=True)
    rutas=['/']
    for p in PS:
        os.makedirs(R+p['url']);open(R+p['url']+'index.html','w',encoding='utf8').write(pag_prod(p));rutas.append(p['url'])
    for c in COL:
        os.makedirs(f'{R}/{c[0]}');open(f'{R}/{c[0]}/index.html','w',encoding='utf8').write(pag_col(c));rutas.append(f'/{c[0]}/')
    home()
    hoy=datetime.date.today().isoformat()
    open(f'{R}/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{W}{r}</loc><lastmod>{hoy}</lastmod></url>\n' for r in rutas)+'</urlset>\n')
    open(f'{R}/robots.txt','w').write(f'User-agent: *\nAllow: /\nDisallow: /herramientas/\n\nSitemap: {W}/sitemap.xml\n')
    print('seo:',len(rutas),'páginas')
main()
