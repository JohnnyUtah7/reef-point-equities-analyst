/* One calculation engine shared by generation checks and the browser. USD millions. */
const ReefModel = (() => {
  const finite = (v, name) => { if (typeof v !== 'number' || !Number.isFinite(v)) throw Error(name + ' must be a finite number'); return v; };
  const defaults = m => ({growth_delta:0, margin_delta:0, capex_scale:100, wacc:m.wacc_pct, g:m.terminal_growth_pct, dilution:0, debt_delta:0});
  function validate(m) {
    if (!m || !Array.isArray(m.forecast) || m.forecast.length < 2) throw Error('At least two forecast years are required');
    ['base_revenue_m','net_debt_m','shares_m','wacc_pct','terminal_growth_pct','expected_dcf_price'].forEach(k=>finite(m[k],k));
    if (m.base_revenue_m<=0 || m.shares_m<=0) throw Error('Base revenue and valuation shares must be positive');
    if (!m.share_basis || !m.source) throw Error('Model source and share_basis are required');
    const years = new Set();
    m.forecast.forEach(r=>{
      if (!r.year || years.has(String(r.year))) throw Error('Forecast year labels must be unique'); years.add(String(r.year));
      ['revenue_m','ebit_margin_pct','tax_rate_pct','da_pct','capex_pct','nwc_pct'].forEach(k=>finite(r[k],r.year+' '+k));
      if(r.revenue_m<0 || r.tax_rate_pct<0 || r.tax_rate_pct>100 || r.da_pct<0 || r.capex_pct<0 || r.nwc_pct<0) throw Error('Invalid forecast rate or revenue');
    });
    calculate(m,defaults(m)); return m;
  }
  function calculate(m, input={}) {
    const k={...defaults(m),...input};Object.keys(defaults(m)).forEach(n=>finite(k[n],n));
    if(k.wacc<=0 || k.wacc>=100 || k.g<=-100 || k.g>=k.wacc) throw Error('Require 0 < WACC < 100% and terminal growth < WACC');
    if(k.dilution<0 || k.capex_scale<0 || k.growth_delta<=-100) throw Error('Invalid dilution, capex or growth adjustment');
    let previous=m.base_revenue_m, previousBase=m.base_revenue_m;
    const rows=m.forecast.map((r,i)=>{
      const baseGrowth=previousBase===0?null:r.revenue_m/previousBase-1;
      if(baseGrowth===null)throw Error("Cannot apply growth adjustment after zero baseline revenue");
      const revenue=previous*(1+baseGrowth+k.growth_delta/100);previousBase=r.revenue_m;
      if(revenue<0)throw Error("Scenario produces negative revenue");
      const ebit=revenue*(r.ebit_margin_pct+k.margin_delta)/100;
      const tax=Math.max(ebit,0)*r.tax_rate_pct/100;
      const da=revenue*r.da_pct/100, capex=revenue*r.capex_pct/100*k.capex_scale/100;
      const nwc=(revenue-previous)*r.nwc_pct/100;previous=revenue;
      const fcff=ebit-tax+da-capex-nwc, pv=fcff/Math.pow(1+k.wacc/100,i+1);
      return {year:r.year,revenue,ebit,tax,nopat:ebit-tax,da,capex,nwc,fcff,pv};
    });
    const n=rows.length,last=rows[n-1],terminalFCFF=last.fcff*(1+k.g/100);
    const tv=terminalFCFF/((k.wacc-k.g)/100),pvTV=tv/Math.pow(1+k.wacc/100,n);
    const pvForecast=rows.reduce((s,r)=>s+r.pv,0),ev=pvForecast+pvTV;
    const debt=m.net_debt_m+k.debt_delta,shares=m.shares_m*(1+k.dilution/100),equity=ev-debt;
    const result={rows,terminalFCFF,tv,pvTV,pvForecast,ev,debt,shares,equity,price:equity/shares,tv_pct:ev===0?null:pvTV/ev*100,knobs:k};
    if(!Number.isFinite(result.price))throw Error('Non-finite model result');return result;
  }
  function reconcile(m) { validate(m);const v=calculate(m);if(Math.abs(v.price-m.expected_dcf_price)>.02)throw Error('Base DCF does not reconcile: calculated '+v.price.toFixed(4)+' vs supplied '+m.expected_dcf_price);return v; }
  function shock(m,k,risks) {
    const next={...defaults(m),...k};
    (risks||[]).forEach(r=>{Object.entries(r.shocks||{}).forEach(([key,v])=>{if(!(key in next))throw Error('Unknown risk control '+key);finite(v,key);next[key]+=v;});});return next;
  }
  function median(a){if(!a.length)return null;const s=[...a].sort((a,b)=>a-b),i=Math.floor(s.length/2);return s.length%2?s[i]:(s[i-1]+s[i])/2;}
  function comps(spec, selected, metric, shares, debt) {
    const vals=(spec.peers||[]).filter(p=>selected.includes(p.ticker)).map(p=>p[metric]).filter(v=>typeof v==='number'&&Number.isFinite(v)&&v>0);
    const med=median(vals),basis=(spec.comps_basis||{})[{pe:'net_income_m',ps:'revenue_m',ev_sales:'revenue_m',ev_ebitda:'ebitda_m'}[metric]];
    if(med===null || !(basis>0) || !(shares>0))return {multiple:med,price:null,count:vals.length};
    return {multiple:med,price:(med*basis-(metric.startsWith('ev_')?debt:0))/shares,count:vals.length};
  }
  function fundamental(spec,key){const f=spec.fundamentals?.[key];return f&&typeof f.value==='number'&&Number.isFinite(f.value)?f.value:null;}
  function statementBridge(spec){const v=k=>fundamental(spec,k),cash=v('cash_m'),debt=v('debt_m'),leases=v('lease_debt_m'),adjust=v('net_debt_adjustments_m');return {revenue:v('revenue_m'),ebitda:v('ebit_m')===null||v('da_m')===null?null:v('ebit_m')+v('da_m'),net_income:v('net_income_m'),net_debt:[cash,debt,leases,adjust].some(x=>x===null)?null:debt+leases-cash+adjust,levered_fcf:v('cfo_m')===null||v('capex_m')===null?null:v('cfo_m')-v('capex_m'),book:v('book_equity_m'),ppe:v('ppe_m')};}
  function otherMethod(spec,method,shares,debt){
    const f=statementBridge(spec),key=method.kind;let lows,mids,highs,trace='';
    if(key==='sotp'){
      const s=spec.sotp;if(!s?.segments?.length)return null;
      const sum=k=>s.segments.reduce((a,r)=>a+r.metric_m*r[k],0);const discount=1-(s.discount_pct||0)/100;const cost=s.holdco_value_m||0;
      lows=(sum('multiple_low')-cost)*discount-debt;mids=(sum('multiple_base')-cost)*discount-debt;highs=(sum('multiple_high')-cost)*discount-debt;trace='Sum segment EV − holdco value; apply conglomerate discount; subtract scenario net debt.';
    }else if(key==='precedents'){
      const t=(spec.transactions||[]).filter(r=>r.metric===method.metric&&r.multiple>0&&r.include!==false);if(!t.length)return null;
      const basis=method.metric==='ev_ebitda'?f.ebitda:method.metric==='ev_sales'?f.revenue:null;if(!(basis>0))return null;const a=t.map(r=>r.multiple);lows=Math.min(...a)*basis-debt;mids=median(a)*basis-debt;highs=Math.max(...a)*basis-debt;trace='Observed transaction multiples × target statement metric − scenario net debt. No automatic control premium.';
    }else if(key==='book'){
      if(f.book===null)return null;lows=mids=highs=f.book;trace='Balance-sheet book equity / scenario shares. Debt is already reflected in equity.';
    }else if(key==='ppe'){
      if(f.ppe===null)return null;lows=mids=highs=f.ppe-debt;trace='Net PPE − scenario net debt, divided by scenario shares; an asset floor, not earnings value.';
    }else if(key==='replacement'){
      const a=spec.replacement;if(!a?.layers?.length)return null;const sum=k=>a.layers.reduce((s,r)=>s+r[k],0);lows=sum('low_m')-debt;mids=sum('base_m')-debt;highs=sum('high_m')-debt;trace='Sourced replacement-cost layers − scenario net debt. Not a cash-flow valuation.';
    }else return null;
    return {lo:lows/shares,mid:mids/shares,hi:highs/shares,trace,dynamic:true};
  }
  function methods(spec,k,selected,metric,weights) {
    const model=spec.model;const calc=model?calculate(model,k):null;
    return (spec.methods||[]).map((a,i)=>{
      let r={...a,weight:a.circular?0:Math.max(0,weights?.[i]??a.weight??0)};
      if(r.kind==='dcf'&&calc){r.mid=calc.price;const ends=[-1,1].map(d=>{try{return calculate(model,{...k,wacc:k.wacc+d}).price;}catch{return null;}}).filter(Number.isFinite);r.lo=Math.min(r.mid,...ends);r.hi=Math.max(r.mid,...ends);r.range_incomplete=ends.length<2;r.dynamic=true;}
      else if(r.kind==='comps'&&calc){const c=comps(spec,selected,metric,calc.shares,calc.debt);r.multiple=c.multiple;if(c.price===null){r.unavailable=true;r.weight=0;}else{r.lo=r.mid=r.hi=c.price;r.dynamic=true;}}
      else if(['sotp','precedents','book','ppe','replacement'].includes(r.kind)&&calc){const o=otherMethod(spec,r,calc.shares,calc.debt);if(o)Object.assign(r,o);else{r.unavailable=true;r.weight=0;}}
      else if(calc){const ratio=model.shares_m/calc.shares;r.lo*=ratio;r.mid*=ratio;r.hi*=ratio;r.dynamic=false;}
      return r;
    });
  }
  function blend(rows){const on=rows.filter(r=>!r.circular&&!r.unavailable&&r.weight>0&&Number.isFinite(r.mid));const sum=on.reduce((s,r)=>s+r.weight,0);return sum?on.reduce((s,r)=>s+r.mid*r.weight,0)/sum:null;}
  function sensitivity(m,k){return [-1,-.5,0,.5,1].map(dw=>[-.5,-.25,0,.25,.5].map(dg=>{try{return calculate(m,{...k,wacc:k.wacc+dw,g:k.g+dg}).price;}catch{return null;}}));}
  function tornado(m,k){return [['Growth +/− 2pp','growth_delta',2],['Margin +/− 2pp','margin_delta',2],['Capex scale +/− 10pp','capex_scale',10],['WACC +/− 1pp','wacc',1],['Terminal growth +/− 0.5pp','g',.5],['Extra dilution +10pp','dilution',10]].map(([name,key,d])=>{const vals=[-d,d].map(v=>{try{return calculate(m,{...k,[key]:Math.max(key==='dilution'?0:-Infinity,k[key]+v)}).price;}catch{return null;}});return {name,low:vals[0],high:vals[1]};});}
  return {defaults,validate,calculate,reconcile,shock,median,comps,fundamental,statementBridge,otherMethod,methods,blend,sensitivity,tornado};
})();
if (typeof module !== 'undefined') module.exports=ReefModel;
