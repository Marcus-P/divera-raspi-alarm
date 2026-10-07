from fastapi import FastAPI,HTTPException
from fastapi.responses import HTMLResponse
from .settings import load_settings,secret_present
from .divera import users
app=FastAPI(title="DIVERA Raspberry Alarm",docs_url=None,redoc_url=None)
CSS="""<style>:root{font-family:Inter,system-ui,sans-serif;color:#18202a;background:#eef1f4}*{box-sizing:border-box}body{margin:0}.top{background:#18202a;color:white;padding:18px 28px}.wrap{max-width:1180px;margin:auto;padding:24px}.test{background:#f7c948;color:#3d2c00;padding:12px 18px;font-weight:800}.nav{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 20px}.nav a{background:white;padding:10px 13px;border-radius:9px;text-decoration:none;color:#18202a}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}.card{background:white;border-radius:12px;padding:18px;box-shadow:0 1px 3px #0001}.ok{color:#18794e}.warn{color:#a15c00}.muted{color:#68737d}.badge{display:inline-block;border-radius:99px;padding:4px 9px;background:#e7f5ed;color:#18794e;font-weight:700}button,select,input{font:inherit;padding:9px;border:1px solid #ccd3da;border-radius:7px}button{background:#243b53;color:white;border:0}h1,h2,h3{margin-top:0}</style>"""
NAV='<div class="nav"><a href="/">Übersicht</a><a href="/divera">DIVERA & Routing</a><a href="/zigbee">Rauchmelder</a><a href="/tests">Geplante Tests</a><a href="/display">Anzeige</a><a href="/system">System</a></div>'
def page(title,body):
 c=load_settings(); b='<div class="test">TESTMODUS AKTIV · Alarme ausschließlich an ausgewählte Testempfänger</div>' if c.routing.test_mode else ''
 return f'<!doctype html><html lang="de"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>{title}</title>{CSS}<body><div class="top"><b>DIVERA Raspberry Alarm</b> · {c.site.name}</div>{b}<main class="wrap">{NAV}<h1>{title}</h1>{body}</main></body></html>'
@app.get("/health")
def health():return {"ok":True,"component":"admin-api"}
@app.get("/api/status")
def status():
 c=load_settings();return {"test_mode":c.routing.test_mode,"divera_key":secret_present("DIVERA_ACCESS_KEY"),"pir_gpio":23,"weekly_test":c.weekly_test.model_dump()}
@app.get("/api/divera/users")
async def api_users():
 try:return await users()
 except Exception as e:raise HTTPException(502,"DIVERA-Benutzer konnten nicht geladen werden") from e
@app.get("/",response_class=HTMLResponse)
def home():return page("Übersicht",'<div class="grid"><div class="card"><h3>Alarmweg</h3><span class="badge">Bereit</span><p class="muted">MQTT → Alarmdienst → DIVERA</p></div><div class="card"><h3>Zigbee</h3><b>Coordinator</b><p class="muted">Status und Rauchmelder</p></div><div class="card"><h3>DIVERA</h3><b>Testmodus</b><p class="muted">Empfänger werden vor Versand begrenzt.</p></div><div class="card"><h3>Anzeige</h3><b>PIR GPIO23</b><p class="muted">Kiosk und Display-Wakeup</p></div></div>')
@app.get("/divera",response_class=HTMLResponse)
def d():return page("DIVERA & Routing",'<div class="card"><h3>Verbindung</h3><p>Access-Key wird nur lokal gespeichert.</p><button>Verbindung prüfen</button></div><div class="card"><h3>Testempfänger</h3><p>Personen aus DIVERA laden und gezielt auswählen. Ohne gültige Auswahl wird kein Testalarm gesendet.</p></div>')
@app.get("/zigbee",response_class=HTMLResponse)
def z():return page("Rauchmelder / Zigbee",'<div class="card"><h3>SONOFF ZBDongle-P</h3><span class="badge">Automatische Erkennung</span><p>Pairing wird zeitlich begrenzt freigeschaltet.</p><button>Pairing 3 Minuten öffnen</button></div>')
@app.get("/tests",response_class=HTMLResponse)
def t():
 days=" ".join(f'<label><input type=checkbox {"checked" if d=="So" else ""}> {d}</label>' for d in ["Mo","Di","Mi","Do","Fr","Sa","So"]);times="".join(f'<option {"selected" if (h,m)==(12,0) else ""}>{h:02d}:{m:02d}</option>' for h in range(24) for m in (0,15,30,45))
 return page("Geplante Tests",f'<div class="card"><h3>Automatischer Systemtest</h3><p>{days}</p><select>{times}</select><p class="muted">Standard: Sonntag 12:00 · SYSTEMTEST – KEIN EINSATZ</p></div>')
@app.get("/display",response_class=HTMLResponse)
def di():return page("Anzeige / Kiosk",'<div class="card"><h3>Kiosk</h3><p>Tab 1: DIVERA · Tab 2: Administration · Wechsel mit Strg+Tab.</p><p>PIR: BCM GPIO23 / Pin 16</p></div>')
@app.get("/system",response_class=HTMLResponse)
def s():return page("System / Administration",'<div class="grid"><div class="card"><h3>Dienste</h3><p>Mosquitto · Zigbee2MQTT · Alarmdienst · Kiosk</p></div><div class="card"><h3>Wiederherstellung</h3><p>Healthchecks und gezielte Neustarts.</p></div></div>')
