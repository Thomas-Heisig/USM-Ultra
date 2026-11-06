"""Local-only MasterVisor development interface; do not expose publicly."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .core import Lab

app=FastAPI(title="USM MasterVisor",version="0.2.0")
lab=Lab()
class Access(BaseModel):
    cpu: str = "cpu0"
    address: int = Field(ge=0,le=0xFFFFFFFF)
    width: int = 1
    write: bool = False
    value: int = Field(default=0,ge=0,le=0xFFFFFFFF)

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
    return HTMLResponse("""<!doctype html><html lang="de"><meta charset="utf-8"><title>USM MasterVisor</title>
<style>body{font:16px system-ui;background:#101827;color:#e8efff;margin:30px}header{font-size:28px;font-weight:700}section{background:#1b2940;padding:20px;border-radius:12px;margin:18px 0}button{padding:10px;border-radius:7px;background:#54a6d9;border:0}pre{white-space:pre-wrap;overflow-wrap:anywhere}</style>
<header>USM ULTRA / MASTER VISOR</header><p>Virtual-first v0.2 - keine physische Hardware verbunden</p>
<section><h2>Virtuelle Matrix und Slots</h2><pre id="status"></pre></section>
<section><h2>USP Bus-Trace</h2><button onclick="demo()">68000-Demozugriff</button><pre id="trace"></pre></section>
<script>async function refresh(){document.getElementById('status').textContent=JSON.stringify(await (await fetch('/api/status')).json(),null,2);document.getElementById('trace').textContent=JSON.stringify(await (await fetch('/api/trace')).json(),null,2)}async function demo(){await fetch('/api/access',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({cpu:'cpu0',address:256,width:2,write:true,value:48879})});refresh()}refresh()</script></html>""")
