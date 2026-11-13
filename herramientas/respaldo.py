# Genera el Excel privado de respaldo desde el inventario interno. El Excel NUNCA va al repositorio.
import json,re,datetime,subprocess
from openpyxl import Workbook
from openpyxl.styles import Font,PatternFill,Alignment,Border,Side
SALIDA='/home/claude/respaldo/TFC_respaldo.xlsx'
RECALC='/root/.claude/skills/synced/80aa62b3-abbc-4421-82e7-be94e650ed33_3afba3f1-a753-40d7-9806-963fb0b43bf8/xlsx/scripts/recalc.py'
d=json.load(open('/home/claude/perfumes/data.json'))
F='Arial';N=Font(name=F,size=11);B=Font(name=F,size=11,bold=True);H=Font(name=F,size=11,bold=True,color='FBF8F4');T=Font(name=F,size=18,bold=True);S=Font(name=F,size=10,color='625E59');AZ=Font(name=F,size=11,color='0000FF')
FH=PatternFill('solid',fgColor='141312');L=Side(style='thin',color='D2CCC4')
M='$#,##0;($#,##0);-';P='0%'
fe=lambda s:datetime.date.fromisoformat(s)
def tabla(ws,cab,filas,anchos,fmt={},entrada=()):
    for j,c in enumerate(cab,1):
        x=ws.cell(1,j,c);x.font=H;x.fill=FH;x.alignment=Alignment(horizontal='center',vertical='center',wrap_text=True)
    ws.row_dimensions[1].height=32
    for i,f in enumerate(filas,2):
        for j,v in enumerate(f,1):
            x=ws.cell(i,j,v);x.font=AZ if j in entrada else N;x.border=Border(bottom=L)
            if j in fmt:x.number_format=fmt[j]
    for j,a in enumerate(anchos):ws.column_dimensions[chr(65+j)].width=a
    ws.freeze_panes='A2'
    if filas: ws.auto_filter.ref=f"A1:{chr(64+len(cab))}{len(filas)+1}"
wb=Workbook();R=wb.active;R.title='Resumen';Pf=wb.create_sheet('Perfumes');C=wb.create_sheet('Compras');V=wb.create_sheet('Ventas');Cl=wb.create_sheet('Clientes')
PS=sorted(d['productos'],key=lambda p:p['id']);nom={p['id']:p['nombre'] for p in PS}
n=len(PS);fin=n+1
tabla(C,['Fecha','ID','Perfume','Piezas','Costo por pieza','Total','Plataforma','Pedido'],[[fe(c['fecha']),c['producto'],nom[c['producto']],c['piezas'],c['costo'],f'=D{i}*E{i}',c.get('plataforma') or 'Sin registrar',c.get('origen','')] for i,c in enumerate(d['compras'],2)],[12,6,46,8,12,12,16,20],{1:'dd/mm/yyyy',5:M,6:M},entrada=(4,5))
filas=[]
for i,v in enumerate(d['ventas'],2):
    filas.append([fe(v['fecha']),v.get('pedido',''),v['producto'],nom.get(v['producto'],'Producto'),v['piezas'],v['tipo'],v['precio'],f'=E{i}*G{i}',v.get('envio',0),v.get('otros',0),f'=H{i}-E{i}*INDEX(Perfumes!$I$2:$I${fin},MATCH(C{i},Perfumes!$A$2:$A${fin},0))-J{i}',v.get('cliente',''),v.get('telefono',''),v.get('pago',''),v.get('vendedor',''),v.get('nota',''),v.get('promo','')])
tabla(V,['Fecha','Pedido','ID','Perfume','Piezas','Tipo','Precio','Total','Envío cobrado','Otros costos','Ganancia','Cliente','Teléfono','Pago','Vendedor','Nota','Promo'],filas,[12,12,6,46,8,10,10,12,10,10,12,24,14,16,14,40,14],{1:'dd/mm/yyyy',7:M,8:M,9:M,10:M,11:M},entrada=(5,7,9,10))
if not filas: V['A2']='Todavía no hay ventas.';V['A2'].font=S
fp=[[p['id'],p['nombre'],p['categoria'],p['menudeo'],p['mayoreo'],f'=SUMIFS(Compras!$D$2:$D$5000,Compras!$B$2:$B$5000,A{i})',f'=SUMIFS(Ventas!$E$2:$E$5000,Ventas!$C$2:$C$5000,A{i})',f'=F{i}-G{i}',f'=IFERROR(SUMPRODUCT((Compras!$B$2:$B$5000=A{i})*Compras!$D$2:$D$5000*Compras!$E$2:$E$5000)/F{i},0)',f'=D{i}-I{i}',f'=E{i}-I{i}',f'=IFERROR(J{i}/I{i},0)',f'=IFERROR(K{i}/I{i},0)'] for i,p in enumerate(PS,2)]
tabla(Pf,['ID','Perfume','Categoría','Menudeo','Mayoreo','Compradas','Vendidas','Stock','Costo promedio','Ganancia menudeo','Ganancia mayoreo','Rendimiento menudeo','Rendimiento mayoreo'],fp,[6,46,11,11,11,11,10,8,12,12,12,13,13],{4:M,5:M,9:M,10:M,11:M,12:P,13:P},entrada=(4,5))
m={}
for v in d['ventas']:
    k=re.sub(r'\D','',str(v.get('telefono','')))[-10:] or v.get('cliente','')
    if not k: continue
    o=m.setdefault(k,{'n':v.get('cliente',''),'t':v.get('telefono',''),'pz':0,'tot':0,'u':v['fecha']})
    o['n']=v.get('cliente') or o['n'];o['pz']+=v['piezas'];o['tot']+=v['piezas']*v['precio'];o['u']=max(o['u'],v['fecha'])
tabla(Cl,['Cliente','Teléfono','Piezas','Total comprado','Última compra'],[[o['n'],o['t'],o['pz'],o['tot'],fe(o['u'])] for o in sorted(m.values(),key=lambda o:-o['tot'])],[28,16,9,14,14],{4:M,5:'dd/mm/yyyy'})
if not m: Cl['A2']='Todavía no hay clientes.';Cl['A2'].font=S
R['A1']='The Fragrance Club';R['A1'].font=T
R['A2']=f"Respaldo privado · datos al {datetime.date.today().strftime('%d/%m/%Y')}. No compartir: incluye costos y clientes.";R['A2'].font=S
K=[('Inversión','=SUM(Compras!F2:F5000)',M),('Ventas cobradas','=SUM(Ventas!H2:H5000)',M),('Ganancia real','=SUM(Ventas!K2:K5000)',M),('Gastos','=SUM(Gastos!C2:C5000)',M),('Ganancia neta','=B6-B7',M),('Entró por envíos','=SUM(Ventas!I2:I5000)',M),('Piezas compradas',f'=SUM(Perfumes!F2:F{fin})','0'),('Piezas vendidas',f'=SUM(Perfumes!G2:G{fin})','0'),('Piezas en stock',f'=SUM(Perfumes!H2:H{fin})','0'),('Ganancia posible a menudeo',f'=SUMPRODUCT(Perfumes!H2:H{fin},Perfumes!J2:J{fin})',M),('Ganancia posible a mayoreo',f'=SUMPRODUCT(Perfumes!H2:H{fin},Perfumes!K2:K{fin})',M)]
for i,(a,f,x) in enumerate(K,4):
    R.cell(i,1,a).font=N;c=R.cell(i,2,f);c.font=B;c.number_format=x
R.column_dimensions['A'].width=34;R.column_dimensions['B'].width=16
V2=[]
for n in d.get('vendedores',[]):V2.append(n)
R['A18']='Ventas por vendedor';R['A18'].font=B
for i,n in enumerate(V2,19):
    R.cell(i,1,n).font=N;c=R.cell(i,2,f'=SUMIFS(Ventas!H2:H5000,Ventas!O2:O5000,A{i})');c.font=B;c.number_format=M
R['A16']='Los envíos cobrados van aparte de la ganancia. Los números en azul son datos capturados; el resto se calcula solo.';R['A16'].font=S
G=wb.create_sheet('Gastos')
tabla(G,['Fecha','Concepto','Monto','Nota'],[[fe(g['fecha']),g['concepto'],g['monto'],g.get('nota','')] for g in d.get('gastos',[])],[12,20,12,30],{1:'dd/mm/yyyy',3:M},entrada=(3,))
Rb=wb.create_sheet('Reembolsos')
tabla(Rb,['Fecha compra','ID','Perfume','Piezas','Costo por pieza','Total','Plataforma','Fecha reembolso','Motivo'],[[fe(c['fecha']),c['producto'],nom[c['producto']],c['piezas'],c['costo'],f'=D{i}*E{i}',c.get('plataforma',''),fe(c['reembolso']),c.get('motivo','')] for i,c in enumerate(d.get('reembolsos',[]),2)],[12,6,46,8,12,12,16,14,40],{1:'dd/mm/yyyy',5:M,6:M,8:'dd/mm/yyyy'})
wb.save(SALIDA)
r=json.loads(subprocess.run(['python3',RECALC,SALIDA,'60'],capture_output=True,text=True).stdout)
assert r.get('status')=='success',r
print('respaldo:',r['total_formulas'],'fórmulas',r['total_errors'],'errores')
