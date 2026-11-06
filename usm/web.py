"""Local-only MasterVisor development interface; do not expose publicly."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .core import Lab
from .catalog import components, component, summary
from .settings import SettingsStore, SettingsError
from collections import deque

app=FastAPI(title="USM MasterVisor",version="0.2.0")
lab=Lab()
settings_store=SettingsStore()
try:
    lab.matrix.trace = deque(lab.matrix.trace, maxlen=settings_store.read()['trace_capacity'])
except (OSError, ValueError):
    pass
class Access(BaseModel):
    cpu: str = "cpu0"
    address: int = Field(ge=0,le=0xFFFFFFFF)
    width: int = 1
    write: bool = False
    value: int = Field(default=0,ge=0,le=0xFFFFFFFF)

class SettingsUpdate(BaseModel):
    mode: str | None = None
    hardware_policy: str | None = None
    trace_capacity: int | None = Field(default=None, ge=256, le=1048576)
    theme: str | None = None
    locale: str | None = None
    default_cpu: str | None = None
    auto_fallback: bool | None = None

@app.get("/api/settings")
def get_settings():
    try:
        return settings_store.read()
    except (OSError, ValueError) as exc:
        raise HTTPException(500, f"settings read error: {exc}")

@app.put("/api/settings")
def put_settings(changes: SettingsUpdate):
    payload=changes.model_dump(exclude_none=True)
    try:
        updated=settings_store.update(payload)
    except (SettingsError, ValueError) as exc:
        raise HTTPException(422, str(exc))
    except OSError as exc:
        raise HTTPException(500, f"settings write error: {exc}")
    lab.matrix.trace=deque(lab.matrix.trace,maxlen=updated["trace_capacity"])
    return updated

@app.get("/api/capabilities")
def capabilities():
    return {
        "virtual_matrix": True,
        "component_catalog": True,
        "settings": True,
        "trace": True,
        "full_m68000": False,
        "musashi": False,
        "machine_boot": False,
        "hardware_discovery": False,
        "hybrid_mode": False,
        "physical_mode": False,
        "timing_t0": False,
    }

@app.get("/api/docs-index")
def docs_index():
    return [
        {"title":"Projektstatus","path":"STATUS.md","url":"https://github.com/Thomas-Heisig/USM-Ultra/blob/main/STATUS.md"},
        {"title":"Einstellungen","path":"docs/SETTINGS.md","url":"https://github.com/Thomas-Heisig/USM-Ultra/blob/main/docs/SETTINGS.md"},
        {"title":"Chipkatalog","path":"docs/CHIP_CATALOG.md","url":"https://github.com/Thomas-Heisig/USM-Ultra/blob/main/docs/CHIP_CATALOG.md"},
        {"title":"Virtual-First Architektur","path":"docs/VIRTUAL_FIRST.md","url":"https://github.com/Thomas-Heisig/USM-Ultra/blob/main/docs/VIRTUAL_FIRST.md"},
        {"title":"Zeitklassen und Modi","path":"docs/MODES_AND_TIMING.md","url":"https://github.com/Thomas-Heisig/USM-Ultra/blob/main/docs/MODES_AND_TIMING.md"},
        {"title":"V7-Studie (Kapitelübersicht)","path":"docs/STUDIE_V7.md","url":"https://github.com/Thomas-Heisig/USM-Ultra/blob/main/docs/STUDIE_V7.md"},
    ]

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
<section class="panel"><h2>Einstellungen</h2><p class="muted">Lokale Konfiguration. Hardware-Modi sind gesperrt, solange keine Hardwareintegration existiert.</p>
<div class="controls">
<label>Modus <select id="mode"><option value="virtual">Virtual (aktiv)</option><option value="hybrid" disabled>Hybrid – nicht verfügbar</option><option value="physical" disabled>Physical – nicht verfügbar</option></select></label>
<label>Trace-Kapazität <input type="number" id="traceCapacity" min="256" max="1048576" step="256"></label>
<label>Sprache <select id="locale"><option value="de">Deutsch</option><option value="en">English</option></select></label>
<label>Design <select id="theme"><option value="dark">Dunkel</option><option value="light">Hell (gespeichert)</option></select></label>
<label>CPU <select id="defaultCpu"><option value="cpu0">CPU 0 · 68000 Stub</option><option value="cpu1">CPU 1 · Z80 Stub</option></select></label>
<button id="saveSettings">Einstellungen speichern</button>
</div><p id="settingsMessage" role="status" class="muted"></p></section>
<section class="panel"><h2>Dokumentation</h2><div id="docsLinks" class="controls"></div><p class="muted">V7-Volltext-DOCX ist noch nicht im Repository. Die Studienübersicht ist abrufbar.</p></section>
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
async function loadSettings(){
 const s=await (await fetch("/api/settings")).json();
 document.getElementById("mode").value=s.mode;
 document.getElementById("traceCapacity").value=s.trace_capacity;
 document.getElementById("locale").value=s.locale;
 document.getElementById("theme").value=s.theme;
 document.getElementById("defaultCpu").value=s.default_cpu;
}
async function loadDocs(){
 const docs=await (await fetch("/api/docs-index")).json();
 const box=document.getElementById("docsLinks");box.replaceChildren();
 for(const d of docs){const a=element("a","badge",d.title);a.href=d.url;a.target="_blank";a.rel="noopener noreferrer";box.append(a)}
}
document.getElementById("saveSettings").addEventListener("click",async()=>{
 const data={mode:document.getElementById("mode").value,trace_capacity:Number(document.getElementById("traceCapacity").value),locale:document.getElementById("locale").value,theme:document.getElementById("theme").value,default_cpu:document.getElementById("defaultCpu").value};
 const response=await fetch("/api/settings",{method:"PUT",headers:{"Content-Type":"application/json"},body:JSON.stringify(data)});
 const body=await response.json();
 document.getElementById("settingsMessage").textContent=response.ok?"Einstellungen lokal gespeichert.":"Fehler: "+JSON.stringify(body);
});
async function load(){
 const [a,b]=await Promise.all([fetch("/api/components"),fetch("/api/components/summary")]);
 inventory=await a.json();const totals=await b.json();
 document.getElementById("summary").textContent=totals.total+" Komponenten erfasst · "+totals.emulated+" Softwaremodelle · "+totals.stub+" Stubs · "+totals.not_implemented+" nicht implementiert";
 const select=document.getElementById("family");
 for(const family of [...new Set(inventory.map(x=>x.family))].sort()){const o=document.createElement("option");o.value=family;o.textContent=family;select.append(o)}
 render();refresh();loadSettings();loadDocs();
}
for(const id of ["search","family","filter"])document.getElementById(id).addEventListener("input",render);
document.getElementById("demo").addEventListener("click",async()=>{
 await fetch("/api/access",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({cpu:"cpu0",address:256,width:2,write:true,value:48879})});refresh()});
load().catch(e=>document.getElementById("summary").textContent="API nicht erreichbar: "+e.message);
</script></body></html>""")
