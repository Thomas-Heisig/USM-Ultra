"""Local-only MasterVisor development interface; do not expose publicly."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .core import Lab
from .catalog import components, component, summary

app=FastAPI(title="USM MasterVisor",version="0.2.0")
lab=Lab()
class Access(BaseModel):
    cpu: str = "cpu0"
    address: int = Field(ge=0,le=0xFFFFFFFF)
    width: int = 1
    write: bool = False
    value: int = Field(default=0,ge=0,le=0xFFFFFFFF)

@app.get("/api/components")
def list_components(family: str | None = None):
    return components(family)

@app.get("/api/components/summary")
def component_summary():
    return summary()

@app.get("/api/components/{component_id}")
def get_component(component_id: str):
    item = component(component_id)
    if item is None:
        raise HTTPException(404, "unknown component")
    return item

@app.get("/api/status")
def status():
    return lab.status()
@app.get("/api/trace")
def trace():
    return list(lab.matrix.trace)
@app.post("/api/access")
def access(request: Access):
    cpu=lab.cpus.get(request.cpu)
    if not cpu:
        raise HTTPException(404,"unknown CPU")
    return vars(cpu.access(request.address,request.width,request.write,request.value))
@app.get("/")
def home():
    from fastapi.responses import HTMLResponse
    return HTMLResponse("""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>USM-Ultra MasterVisor</title><style>
:root{color-scheme:dark}*{box-sizing:border-box}body{font:15px system-ui,sans-serif;background:#0d1524;color:#e9f1ff;margin:0}
header{background:#14233a;border-bottom:1px solid #34445f;padding:20px 28px;display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
h1{margin:0;font-size:24px}small,.muted{color:#9eb0c9}main{max-width:1400px;margin:auto;padding:24px}
.panel{background:#18263b;border:1px solid #34445f;border-radius:12px;padding:18px;margin:0 0 20px}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(245px,1fr));gap:12px}
.chip{background:#101d31;border:1px solid #334760;border-radius:10px;padding:14px}
.chip h3{margin:0 0 5px;font-size:16px}.chip p{margin:8px 0;color:#b2c2d8;font-size:13px}
.badge{display:inline-block;font-size:12px;border-radius:20px;padding:4px 9px;background:#3b4758;color:#e7efff}
.emulated{background:#164f3b;color:#aaf5cf}.stub{background:#695024;color:#ffe3a1}.not_implemented{background:#49323b;color:#f6becb}
.controls{display:flex;gap:10px;flex-wrap:wrap;margin:12px 0}input,select,button{padding:10px;border-radius:8px;background:#233651;border:1px solid #506482;color:white}
button{cursor:pointer;background:#236da3}pre{white-space:pre-wrap;overflow-wrap:anywhere;max-height:270px;overflow:auto}
</style></head><body>
<header><div><h1>USM-ULTRA / MASTER VISOR</h1><small>Virtual-first · Komponenten- und Chip-Matrix</small></div>
<div><span class="badge emulated">Softwarebetrieb möglich</span> <span class="badge">Hardware nicht geprüft</span></div></header>
<main>
<section class="panel"><h2>Systemübersicht</h2><p class="muted">Katalogeinträge sind keine funktionsfähigen Emulatoren. Stubs und geplante Chips sind ausdrücklich markiert.</p>
<div id="summary">Lade Komponenten…</div></section>
<section class="panel"><h2>Chip- und Komponenten-Katalog</h2>
<div class="controls"><input id="search" placeholder="Chip suchen (z. B. 68000, Paula, SID)" aria-label="Komponente suchen">
<select id="family" aria-label="Chipfamilie"><option value="">Alle Kategorien</option></select>
<select id="filter" aria-label="Implementierungsstand"><option value="">Alle Status</option><option value="emulated">Emuliert</option><option value="stub">Stub</option><option value="not_implemented">Nicht implementiert</option></select></div>
<div class="cards" id="chips"></div></section>
<section class="panel"><h2>Virtuelle USP-Matrix</h2><pre id="status"></pre></section>
<section class="panel"><h2>Bus-Trace</h2><button id="demo">68000-Demozugriff</button><pre id="trace"></pre></section>
</main><script>
let inventory=[];
const labels={emulated:"Emuliert",stub:"Stub / unvollständig",not_implemented:"Nicht implementiert"};
const hardware={not_probed:"Hardware nicht geprüft",not_present:"Hardware nicht vorhanden",present:"Hardware erkannt"};
function element(tag,cls,txt){const e=document.createElement(tag);if(cls)e.className=cls;if(txt!==undefined)e.textContent=txt;return e}
function render(){
 const q=document.getElementById("search").value.toLowerCase(),family=document.getElementById("family").value,filter=document.getElementById("filter").value;
 const grid=document.getElementById("chips");grid.replaceChildren();
 const filtered=inventory.filter(x=>(!family||x.family===family)&&(!filter||x.implementation===filter)&&[x.name,x.id,x.role].join(" ").toLowerCase().includes(q));
 for(const x of filtered){
 const card=element("article","chip");
 card.append(element("h3","",x.name),element("small","",x.family+" · "+x.id));
 card.append(element("p","",x.role));
 card.append(element("span","badge "+x.implementation,labels[x.implementation]||x.implementation));
 card.append(element("p","",hardware[x.hardware]||x.hardware));
 if(x.notes)card.append(element("p","",x.notes));
 if(x.dependencies.length)card.append(element("small","", "Abhängigkeiten: "+x.dependencies.join(", ")));
 grid.append(card)}
 if(!filtered.length)grid.append(element("p","muted","Keine Komponenten gefunden."));
}
async function refresh(){
 const [s,t]=await Promise.all([fetch("/api/status"),fetch("/api/trace")]);
 document.getElementById("status").textContent=JSON.stringify(await s.json(),null,2);
 document.getElementById("trace").textContent=JSON.stringify(await t.json(),null,2);
}
async function load(){
 const [a,b]=await Promise.all([fetch("/api/components"),fetch("/api/components/summary")]);
 inventory=await a.json();const totals=await b.json();
 document.getElementById("summary").textContent=totals.total+" Komponenten erfasst · "+totals.emulated+" Softwaremodelle · "+totals.stub+" Stubs · "+totals.not_implemented+" nicht implementiert";
 const select=document.getElementById("family");
 for(const family of [...new Set(inventory.map(x=>x.family))].sort()){const o=document.createElement("option");o.value=family;o.textContent=family;select.append(o)}
 render();refresh();
}
for(const id of ["search","family","filter"])document.getElementById(id).addEventListener("input",render);
document.getElementById("demo").addEventListener("click",async()=>{
 await fetch("/api/access",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({cpu:"cpu0",address:256,width:2,write:true,value:48879})});refresh()});
load().catch(e=>document.getElementById("summary").textContent="API nicht erreichbar: "+e.message);
</script></body></html>""")
