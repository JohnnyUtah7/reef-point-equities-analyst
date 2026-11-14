"""Validated, self-contained artifact-grade research renderer (schema version 2)."""
from pathlib import Path
import base64, copy, html, json, math, re, subprocess
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'assets'/'research-terminal'
def validate_spec(s):
    s=copy.deepcopy(s)
    def number(v,label,nullable=False):
        if nullable and v is None:return
        if isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v):raise ValueError(label+' must be a finite number')
    for key in ('ticker','rating','last','methods'):
        if key not in s:raise ValueError('Missing '+key)
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,19}',str(s['ticker'])):raise ValueError('Unsafe ticker')
    if str(s['rating']).upper() not in ('BUY','HOLD','SELL'):raise ValueError('Invalid published rating')
    s['rating']=s['rating'].upper();number(s['last'],'last')
    if s['last']<=0:raise ValueError('last must be positive')
    if s.get('target') is None and not s.get('target_open'):raise ValueError('Target required unless target_open')
    number(s.get('target'),'target',nullable=bool(s.get('target_open')))
    if s.get('stance','bull') not in ('bull','bear'):raise ValueError('stance must be bull or bear')
    if not isinstance(s['methods'],list):raise ValueError('methods must be an array')
    for m in s['methods']:
        for k in ('lo','mid','hi'):number(m.get(k),'method '+k)
        number(m.get('weight',0),'method weight')
        if not m['lo']<=m['mid']<=m['hi'] or m.get('weight',0)<0:raise ValueError('Invalid method range or weight')
        if m.get('circular') and m.get('weight',0)!=0:raise ValueError('Circular methods must have zero weight')
    controls={'growth_delta','margin_delta','capex_scale','wacc','g','dilution','debt_delta'}
    for name,values in s.get('presets',{}).items():
        if not isinstance(values,dict):raise ValueError('Preset must be an object')
        for key,v in values.items():
            if key not in controls:raise ValueError('Unknown preset control '+key)
            number(v,'preset '+key)
    for risk in s.get('risks',[]):
        if isinstance(risk,dict):
            for key,v in risk.get('shocks',{}).items():
                if key not in controls:raise ValueError('Unknown risk control '+key)
                number(v,'risk '+key)
    for peer in s.get('peers',[]):
        if not peer.get('ticker'):raise ValueError('Peer ticker required')
        for key in ('pe','ps','ev_sales','ev_ebitda'):number(peer.get(key),'peer '+key,nullable=True)
    for key,item in s.get('fundamentals',{}).items():
        if not isinstance(item,dict):raise ValueError('Fundamental must carry value and source')
        number(item.get('value'),key,nullable=True)
        for field in ('statement','period','source'):
            if not item.get(field):raise ValueError(key+' requires '+field)
    def fact(key):return s.get('fundamentals',{}).get(key,{}).get('value')
    for group,keys in [('transactions',('multiple',))]:
        for item in s.get(group,[]):
            for key in keys:number(item.get(key),group+' '+key)
            if not item.get('source'):raise ValueError(group+' source required')
    for seg in s.get('sotp',{}).get('segments',[]):
        for key in ('metric_m','multiple_low','multiple_base','multiple_high'):number(seg.get(key),'SOTP '+key)
        if not seg['multiple_low']<=seg['multiple_base']<=seg['multiple_high'] or seg['metric_m']<0 or seg['multiple_low']<0:raise ValueError('Invalid SOTP segment')
        if not seg.get('source'):raise ValueError('SOTP source required')
    sotp=s.get('sotp',{})
    for k in ('discount_pct','holdco_value_m'):
        if k in sotp:number(sotp[k],'SOTP '+k)
    if not 0<=sotp.get('discount_pct',0)<=100:raise ValueError('Invalid SOTP discount')
    for layer in s.get('replacement',{}).get('layers',[]):
        for k in ('low_m','base_m','high_m'):number(layer.get(k),'replacement '+k)
        if not layer['low_m']<=layer['base_m']<=layer['high_m']:raise ValueError('Invalid replacement range')
        if not layer.get('source'):raise ValueError('Replacement source required')
    for key,value in s.get('comps_basis',{}).items():number(value,'comps basis '+key,nullable=True)
    if s.get('model'):
        for key in ('revenue_m','cash_m','debt_m','lease_debt_m','net_debt_adjustments_m'):
            number(fact(key),'Required statement input '+key)
        nd=fact('debt_m')+fact('lease_debt_m')-fact('cash_m')+fact('net_debt_adjustments_m')
        number(s['model'].get('net_debt_m'),'model net debt')
        if abs(nd-s['model']['net_debt_m'])>.02:raise ValueError('Model net debt does not reconcile to balance-sheet inputs')
        number(s['model'].get('base_revenue_m'),'model base revenue')
        if abs(fact('revenue_m')-s['model']['base_revenue_m'])>.02:raise ValueError('Model base revenue does not reconcile to statement input')
        if not s.get('comps_basis'):
            s['comps_basis']={'revenue_m':fact('revenue_m'),'net_income_m':fact('net_income_m'),'ebitda_m':None if fact('ebit_m') is None or fact('da_m') is None else fact('ebit_m')+fact('da_m')}
        elif not s.get('comps_basis_source'):raise ValueError('Explicit comps basis requires period/source in comps_basis_source')
        result=subprocess.run(['node','-e',"const M=require(process.argv[1]);let t='';process.stdin.on('data',d=>t+=d);process.stdin.on('end',()=>{try{const s=JSON.parse(t);M.reconcile(s.model);Object.values(s.presets||{}).forEach(p=>M.calculate(s.model,p));console.log('reconciled');}catch(e){console.error(e.message);process.exit(1)}})",str(ASSETS/'model.js')],input=json.dumps(s,allow_nan=False),capture_output=True,text=True)
        if result.returncode:raise ValueError(result.stderr.strip())
    return s

def render(s):
    s=validate_spec(s)
    payload=json.dumps(s,allow_nan=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    logo=base64.b64encode((ROOT/'assets/rpc-logo.png').read_bytes()).decode()
    template=(ASSETS/'template.html').read_text()
    values={'__TITLE__':html.escape(str(s['ticker']))+' — Reef Point Research','__LOGO__':logo,'__STYLE__':(ASSETS/'style.css').read_text(),'__DATA__':payload,'__ENGINE__':(ASSETS/'model.js').read_text(),'__APP__':(ASSETS/'app.js').read_text()}
    # Single replacement pass: data cannot be interpreted as another template marker.
    return re.sub('|'.join(re.escape(k) for k in values),lambda m:values[m.group()],template)

def build(path):
    path=Path(path);s=json.loads(path.read_text());page=render(s)
    parts=path.resolve().parts;root=Path(*parts[:parts.index('artifacts')]) if 'artifacts' in parts else path.resolve().parent
    dest=root/'docs'/f"{s['ticker'].lower()}-reef-point-live.html";dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(page);return dest
