from fastapi import FastAPI,HTTPException
from fastapi.responses import HTMLResponse
from .settings import load_settings,secret_present
from .divera import users
app=FastAPI(title="DIVERA Raspberry Alarm",docs_url=None,redoc_url=None)
NAV='<nav><a href="/">Übersicht</a><a href="/divera">DIVERA & Routing</a><a href="/zigbee">Rauchmelder</a><a href="/tests">Geplante Tests</a><a href="/display">Anzeige</a><a href="/system">System</a></nav>'
CSS='''<style>body{font-family:system-ui,sans-serif;max-width:1000px;margin:2rem auto;padding:0 1rem;background:#f3f5f7;color:#18202a}nav{display:flex;gap:.6rem;flex-wrap:wrap}nav a{padding:.6rem .8rem;background:#fff;border-radius:8px;text-decoration:none;color:#18202a}section{background:#fff;padding:1.2rem;margin-top:1rem;border-radius:12px}.test{background:#ffe4a8;padding:.8rem;border-radius:8px;font-weight:700}</style>'''
def page(title,body):
 c=load_settings();banner='<div class="test">TESTMODUS AKTIV – Alarme nur an ausgewählte Testempfänger</div>' if c.routing.test_mode else ''
 return f'<!doctype html><html lang="de"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>{title}</title>{CSS}<body><h1>DIVERA Raspberry Alarm</h1>{banner}{NAV}<section><h2>{title}</h2>{body}</section></body></html>'
@app.get("/health")
def health():return {"ok":True,"component":"admin-api"}
@app.get("/api/status")
def status():
 c=load_settings();return {"site":c.site.name,"test_mode":c.routing.test_mode,"divera_key_configured":secret_present("DIVERA_ACCESS_KEY"),"pir":{"bcm_gpio":23,"physical_pin":16},"weekly_test":{"enabled":c.weekly_test.enabled,"weekdays":c.weekly_test.weekdays,"time":c.weekly_test.time}}
@app.get("/api/divera/users")
async def api_users():
 try:return await users()
 except Exception as e:raise HTTPException(502,"DIVERA-Benutzer konnten nicht geladen werden") from e
@app.get("/",response_class=HTMLResponse)
def home():return page("Übersicht","<p>Systemübersicht und Gesundheitszustand.</p>")
@app.get("/divera",response_class=HTMLResponse)
def divera_page():return page("DIVERA & Routing","<p>Access-Key, Testempfänger und später Produktivstatus werden hier konfiguriert.</p>")
@app.get("/zigbee",response_class=HTMLResponse)
def zigbee_page():return page("Rauchmelder / Zigbee","<p>Pairing, Namen, Räume, Batterie, Fehler und Erreichbarkeit.</p>")
@app.get("/tests",response_class=HTMLResponse)
def tests_page():
 days=" ".join(f'<label><input type="checkbox">{d}</label>' for d in ["Mo","Di","Mi","Do","Fr","Sa","So"])
 times="".join(f'<option>{h:02d}:{m:02d}</option>' for h in range(24) for m in (0,15,30,45))
 return page("Geplante Tests",f"<p>{days}</p><select>{times}</select><p>Standard: Sonntag 12:00. Speicherung wird im Einrichtungsassistenten aktiviert.</p>")
@app.get("/display",response_class=HTMLResponse)
def display():return page("Anzeige / Kiosk","<p>DIVERA ist Tab 1, Administration Tab 2. Wechsel lokal mit Strg+Tab.</p>")
@app.get("/system",response_class=HTMLResponse)
def system():return page("System / Administration","<p>Dienste, Diagnose und sichere Passwortänderung.</p>")
