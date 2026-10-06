from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from .settings import load_settings, secret_present
app=FastAPI(title="DIVERA Raspberry Alarm",docs_url=None,redoc_url=None)
@app.get("/health")
def health(): return {"ok":True,"component":"admin-api"}
@app.get("/api/status")
def status():
    c=load_settings()
    return {"site":c.site.name,"divera_key_configured":secret_present("DIVERA_ACCESS_KEY"),"pir":{"bcm_gpio":23,"physical_pin":16},"weekly_test":{"enabled":c.weekly_test.enabled,"weekday":c.weekly_test.weekday,"time":c.weekly_test.time}}
@app.get("/",response_class=HTMLResponse)
def index():
    return """<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DIVERA Raspberry Alarm</title><style>body{font-family:system-ui,sans-serif;max-width:900px;margin:2rem auto;padding:0 1rem;background:#f5f6f7;color:#17191c}header,section{background:white;border-radius:12px;padding:1.25rem;margin:1rem 0;box-shadow:0 1px 4px #0002}.muted{color:#59636e}</style></head><body><header><h1>DIVERA Raspberry Alarm</h1><p class="muted">Lokale Administration</p></header><section><h2>System</h2><p><b>Administrationsdienst läuft.</b></p><p>Einrichtung, Geräte und Diagnose werden hier verwaltet.</p></section></body></html>"""
