# Genera el catálogo público desde el inventario interno. Solo copia datos públicos.
import json
d=json.load(open('/home/claude/perfumes/data.json'))
try: old=json.load(open('/home/claude/tienda/data.json'))
except Exception: old={}
sold={}
for v in d['ventas']: sold[v['producto']]=sold.get(v['producto'],0)+v['piezas']
buy={}
for c in d['compras']: buy[c['producto']]=buy.get(c['producto'],0)+c['piezas']
pub={"marca":old.get("marca",""),"whatsapp":old.get("whatsapp",""),"comunidad":old.get("comunidad",""),"mayoreoMin":old.get("mayoreoMin",4),"costoEnvio":old.get("costoEnvio",100),"actualizado":d['actualizado'],
"productos":[{"id":p['id'],"nombre":p['nombre'],"categoria":p['categoria'],"menudeo":p['menudeo'],"mayoreo":p['mayoreo'],"img":p.get('img',''),"notas":p.get('notas',''),**({k:p[k] for k in ('piramide','uso') if k in p}),"stock":buy.get(p['id'],0)-sold.get(p['id'],0)} for p in d['productos']]}
json.dump(pub,open('/home/claude/tienda/data.json','w'),ensure_ascii=False,indent=1)
print(len(pub['productos']),sum(p['stock'] for p in pub['productos']),set(k for p in pub['productos'] for k in p))

# Actualiza páginas de Google (precios y disponibilidad). Después: git add -A en el-repo, no solo data.json.
import shutil,subprocess
shutil.copy('/home/claude/tienda/data.json','/home/claude/the-fragrance-club/data.json')
subprocess.run(['python3','/home/claude/tienda/seo.py'],check=True)
# Respaldo de herramientas en el repositorio (sin datos privados).
import os
os.makedirs('/home/claude/the-fragrance-club/herramientas',exist_ok=True)
subprocess.run(['python3','/home/claude/tienda/respaldo.py'],check=True)
for x in ('sync.py','seo.py','respaldo.py','tfc-trazo.txt'): shutil.copy('/home/claude/tienda/'+x,'/home/claude/the-fragrance-club/herramientas/'+x)
