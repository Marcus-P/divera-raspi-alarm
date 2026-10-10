import html,json,secrets,socket,subprocess,time
from pathlib import Path
import paho.mqtt.publish as publish
from fastapi import FastAPI,HTTPException,Depends,Form,Request
from fastapi.responses import HTMLResponse,RedirectResponse
from .settings import load_settings,save_settings,secret_present
from .divera import users
from .updater import latest,download,installed_version

app=FastAPI(title="DIVERA Raspberry Alarm",docs_url=None,redoc_url=None)
CSRF=secrets.token_urlsafe(32)
SESSIONS={}
LOGIN_TOKENS={}
SESSION_COOKIE="dra_admin_session"
ADMIN_FILE=Path("/var/lib/divera-raspi-alarm/admin-user")
DAYS={"monday":"Mo","tuesday":"Di","wednesday":"Mi","thursday":"Do","friday":"Fr","saturday":"Sa","sunday":"So"}

def admin_user(): return ADMIN_FILE.read_text().strip() if ADMIN_FILE.exists() else ""
def verify_os_password(username:str,password:str)->bool:
 # The web process is intentionally unprivileged. PAM needs access to
 # /etc/shadow, so a tightly scoped root-owned UNIX socket handles verification.
 if not password or len(password)>1024:return False
 try:
  with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as sock:
   sock.settimeout(5)
   sock.connect("/run/divera-raspi-alarm/auth.sock")
   sock.sendall(json.dumps({"username":username,"password":password}).encode("utf-8")+b"\n")
   sock.shutdown(socket.SHUT_WR)
   return sock.recv(32)==b"OK\n"
 except (OSError,ValueError):
  return False
def auth(request:Request):
 token=request.cookies.get(SESSION_COOKIE,"")
 now=time.monotonic()
 expiry=SESSIONS.get(token) if token else None
 if not expiry or expiry<=now:
  if token:SESSIONS.pop(token,None)
  if request.url.path.startswith("/api/"):
   raise HTTPException(401,"Nicht angemeldet")
  raise HTTPException(303,headers={"Location":"/login"})
 SESSIONS[token]=now+load_settings().administration.session_idle_minutes*60
 return admin_user()

def login_page(error=""):
 now=time.monotonic()
 for token,expires in list(LOGIN_TOKENS.items()):
  if expires<=now:LOGIN_TOKENS.pop(token,None)
 if len(LOGIN_TOKENS)>128:LOGIN_TOKENS.clear()
 token=secrets.token_urlsafe(32)
 LOGIN_TOKENS[token]=now+300
 message=f'<p class="warn">{esc(error)}</p>' if error else ""
 body=(f'<section class="login-card"><div class="login-mark">DR</div>'
       f'<h1>Willkommen zurück</h1>'
       f'<p class="login-subtitle">Melde dich an, um die Alarmanlage zu verwalten.</p>{message}'
       f'<form method="post" action="/login" class="login-form">'
       f'<input type="hidden" name="csrf" value="{token}">'
       f'<label for="login-user">Benutzername</label>'
       f'<input id="login-user" name="username" autocomplete="username" required autofocus>'
       f'<label for="login-password">Passwort</label>'
       f'<input id="login-password" type="password" name="password" autocomplete="off" required>'
       f'<button type="submit">Anmelden</button></form>'
       f'<p class="login-footnote">Geschützter Administrationsbereich</p></section>')
 return f'<!doctype html><html lang="de"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Anmeldung · DIVERA Raspberry Alarm</title>{CSS}<body class="login-page"><header class="login-header"><b>DIVERA</b><span>Raspberry Alarm</span></header><main class="login-main">{body}</main></body></html>'

@app.get("/login",response_class=HTMLResponse)
def login_get():
 return HTMLResponse(login_page())

@app.post("/login")
def login_post(request:Request,csrf_token:str=Form(alias="csrf"),username:str=Form(),password:str=Form()):
 expires=LOGIN_TOKENS.pop(csrf_token,None)
 if not expires or expires<=time.monotonic():
  return HTMLResponse(login_page("Anmeldeformular abgelaufen. Bitte erneut versuchen."),status_code=403)
 if username!=admin_user() or not verify_os_password(username,password):
  return HTMLResponse(login_page("Anmeldung fehlgeschlagen."),status_code=401)
 token=secrets.token_urlsafe(32)
 SESSIONS[token]=time.monotonic()+load_settings().administration.session_idle_minutes*60
 response=RedirectResponse("/",status_code=303)
 response.set_cookie(SESSION_COOKIE,token,httponly=True,samesite="strict",secure=request.url.scheme=="https",path="/")
 return response

@app.post("/logout")
def logout(request:Request,csrf_token:str=Form(alias="csrf")):
 csrf(csrf_token)
 token=request.cookies.get(SESSION_COOKIE,"")
 if token:SESSIONS.pop(token,None)
 response=RedirectResponse("/login",status_code=303)
 response.delete_cookie(SESSION_COOKIE,path="/")
 return response

@app.middleware("http")
async def security_headers(request:Request,call_next):
 response=await call_next(request)
 response.headers["Cache-Control"]="no-store"
 response.headers["X-Content-Type-Options"]="nosniff"
 response.headers["X-Frame-Options"]="DENY"
 response.headers["Referrer-Policy"]="no-referrer"
 return response
def csrf(v:str):
 if not secrets.compare_digest(v,CSRF): raise HTTPException(403,"Ungültige Formularanforderung")
def esc(v):return html.escape(str(v),quote=True)
def ids(v):return [int(x.strip()) for x in v.split(",") if x.strip().isdigit()]
def form(action,body,button="Speichern"):
 return f'<form method="post" action="{action}"><input type="hidden" name="csrf" value="{CSRF}">{body}<p><button>{button}</button></p></form>'

CSS="""<style>:root{font-family:Inter,system-ui,sans-serif;color:#18202a;background:#eef1f4}*{box-sizing:border-box}body{margin:0}.top{background:#18202a;color:white;padding:18px 28px}.wrap{max-width:1180px;margin:auto;padding:24px}.test{background:#f7c948;color:#3d2c00;padding:12px 18px;font-weight:800}.nav{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 20px}.nav a{background:white;padding:10px 13px;border-radius:9px;text-decoration:none;color:#18202a}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}.card{background:white;border-radius:12px;padding:18px;box-shadow:0 1px 3px #0001;margin-bottom:14px}.ok{color:#18794e}.warn{color:#a15c00}.muted{color:#68737d}.badge{display:inline-block;border-radius:99px;padding:4px 9px;background:#e7f5ed;color:#18794e;font-weight:700}button,select,input{font:inherit;padding:9px;border:1px solid #ccd3da;border-radius:7px}button{background:#243b53;color:white;border:0}label{display:inline-block;margin:6px}h1,h2,h3{margin-top:0}.nav form,.nav form p{margin:0}.nav button{padding:10px 13px}.login-page{min-height:100vh;background:radial-gradient(ellipse at 50% 0%,#e7eef5 0%,#f4f6f9 65%);display:flex;flex-direction:column}.login-header{display:flex;align-items:center;gap:12px;padding:24px clamp(20px,4vw,56px);color:#243b53}.login-header b{font-size:20px;letter-spacing:.06em}.login-header span{border-left:1px solid #bac7d4;padding-left:12px;color:#607181;font-size:14px}.login-main{flex:1;display:flex;align-items:center;justify-content:center;padding:24px 18px 10vh}.login-card{width:100%;max-width:420px;background:#fff;padding:38px;border:1px solid #e2e8f0;border-radius:18px;box-shadow:0 18px 48px #1c344814}.login-mark{width:48px;height:48px;border-radius:13px;background:#243b53;color:#fff;display:grid;place-items:center;font-weight:800;letter-spacing:.04em;margin-bottom:25px}.login-card h1{font-size:26px;letter-spacing:-.035em;margin:0 0 9px}.login-subtitle{font-size:14px;line-height:1.55;color:#66788a;margin:0 0 30px}.login-form{display:flex;flex-direction:column;gap:0}.login-form label{display:block;margin:0 0 7px;font-size:13px;font-weight:650;color:#34485b}.login-form input{display:block;width:100%;height:45px;margin:0 0 19px;border:1px solid #cbd5df;border-radius:9px;padding:0 13px;background:#fff;color:#18202a}.login-form input:focus{outline:2px solid #89a6c6;outline-offset:1px;border-color:#5b7da1}.login-form button{height:46px;width:100%;margin-top:6px;border-radius:9px;font-weight:700;cursor:pointer}.login-form button:hover{background:#304d6c}.login-footnote{margin:24px 0 0;text-align:center;font-size:12px;color:#84919d}@media(max-width:480px){.login-card{padding:28px 22px}.login-main{align-items:flex-start;padding-top:48px}}
</style>"""
NAV='<div class="nav"><a href="/">Übersicht</a><a href="/divera">DIVERA & Routing</a><a href="/zigbee">Rauchmelder</a><a href="/tests">Geplante Tests</a><a href="/display">Anzeige</a><a href="/system">System</a>'+form("/logout","","Abmelden")+'</div>'
def page(title,body):
 c=load_settings();b='<div class="test">TESTMODUS AKTIV · Alarme ausschließlich an ausgewählte Testempfänger</div>' if c.routing.test_mode else ''
 # Client hides the page after inactivity; the server enforces expiry too.
 script=('<script>const idleMs='+str(c.administration.session_idle_minutes*60000)
         +';const csrf='+json.dumps(CSRF)
         +''';let idleTimer;
 function logOut(){fetch("/logout",{method:"POST",credentials:"same-origin",headers:{"Content-Type":"application/x-www-form-urlencoded"},body:"csrf="+encodeURIComponent(csrf)}).finally(()=>location.replace("/login"));}
 let lastPing=0;
 async function checkSession(){
  try{
   const response=await fetch("/api/session",{credentials:"same-origin",cache:"no-store"});
   if(!response.ok)location.replace("/login");
  }catch(error){location.replace("/login");}
 }
 function resetIdle(){
  clearTimeout(idleTimer);idleTimer=setTimeout(logOut,idleMs);
  const now=Date.now();
  if(now-lastPing>30000){lastPing=now;void checkSession();}
 }
 for(const eventName of ["pointermove","pointerdown","keydown","touchstart","scroll"])document.addEventListener(eventName,resetIdle,{passive:true});
 resetIdle();</script>''')
 return f'<!doctype html><html lang="de"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>{esc(title)}</title>{CSS}<body><div class="top"><b>DIVERA Raspberry Alarm</b> · {esc(c.site.name)}</div>{b}<main class="wrap">{NAV}<h1>{esc(title)}</h1>{body}</main>{script}</body></html>'

@app.get("/health")
def health():return {"ok":True,"component":"admin-api"}

@app.get("/api/display-config")
def display_config():
 # Kiosk and motion monitor run under the desktop account, not divera-alarm.
 # Only expose non-secret display settings on the loopback-bound admin service.
 c=load_settings()
 return {"divera_url":c.kiosk.divera_url,"admin_url":c.kiosk.admin_url,
         "display_idle_minutes":c.kiosk.display_idle_minutes,
         "pir_bcm_gpio":c.hardware.pir_bcm_gpio}
@app.get("/api/session",dependencies=[Depends(auth)])
def session_status():return {"ok":True}

@app.get("/api/status",dependencies=[Depends(auth)])
def status():
 c=load_settings();return {"test_mode":c.routing.test_mode,"divera_key":secret_present("DIVERA_ACCESS_KEY"),"pir_gpio":23,"weekly_test":c.weekly_test.model_dump()}
@app.get("/api/divera/users",dependencies=[Depends(auth)])
async def api_users():
 try:return await users()
 except Exception as e:raise HTTPException(502,"DIVERA-Benutzer konnten nicht geladen werden") from e

def observed_devices():
 # This state is populated only after the alarm worker receives Zigbee MQTT
 # messages. It is not a definitive list of paired Zigbee devices.
 try:
  devices=json.loads(Path("/var/lib/divera-raspi-alarm/detectors.json").read_text())
  return devices if isinstance(devices,dict) else {}
 except (OSError,ValueError):
  return {}

@app.get("/",response_class=HTMLResponse)
def home(_=Depends(auth)):
 c=load_settings()
 devices=observed_devices()
 if devices:
  device_rows="".join(
   f'<li><b>{esc(name)}</b> · {("online" if data.get("online") is True else "offline" if data.get("online") is False else "Status unbekannt") if isinstance(data,dict) else "Status unbekannt"}</li>'
   for name,data in sorted(devices.items())
  )
  zigbee_summary=f'<b>{len(devices)} Gerät(e) vom Alarmdienst erfasst</b><ul>{device_rows}</ul>'
 else:
  zigbee_summary='<p class="muted">Noch keine Geräte vom Alarmdienst erfasst.</p>'
 display_summary=(f'<b>Bildschirmsteuerung per Bewegungssensor (PIR)</b>'
                  f'<p>Bildschirm aus nach {c.kiosk.display_idle_minutes} Minuten ohne Bewegung.</p>'
                  f'<p class="muted">Anschluss: GPIO {c.hardware.pir_bcm_gpio} (BCM). Funktion noch nicht geprüft.</p>')
 body=(f'<div class="grid">'
       f'<div class="card"><h3>Alarmweg</h3><span class="badge">Dienst aktiv</span><p class="muted">MQTT → Alarmdienst → DIVERA</p></div>'
       f'<div class="card"><h3>Zigbee</h3>{zigbee_summary}<p><a href="/zigbee">Rauchmelder verwalten</a></p></div>'
       f'<div class="card"><h3>DIVERA</h3><b>{"Testmodus" if c.routing.test_mode else "Produktivmodus"}</b><p>Access-Key: {"vorhanden" if secret_present("DIVERA_ACCESS_KEY") else "noch nicht eingerichtet"}</p></div>'
       f'<div class="card"><h3>Anzeige</h3>{display_summary}<p><a href="/display">Anzeige konfigurieren</a></p></div>'
       f'</div>')
 return page("Übersicht",body)

@app.get("/divera",response_class=HTMLResponse)
def div_page(_=Depends(auth)):
 c=load_settings()
 keyform=form("/divera/key",'<label>Neuer DIVERA Alarm-Access-Key <input name="key" type="password" autocomplete="new-password" required></label>',"Alarm-Key verschlüsselt speichern")
 systemform=form("/divera/system-key",'<label>DIVERA Systemnutzer-Key <input name="key" type="password" autocomplete="new-password" required></label>',"Systemnutzer-Key verschlüsselt speichern")
 routing=form("/divera/routing",f'<label>Testempfänger-IDs <input name="test_ids" value="{esc(",".join(map(str,c.routing.test_recipient_ids)))}"></label><br><label>Technikempfänger-IDs <input name="technical_ids" value="{esc(",".join(map(str,c.routing.technical_recipient_ids)))}"></label>',"Empfänger speichern")
 return page("DIVERA & Routing",f'<div class="card"><h3>Verbindung</h3><p>Access-Key: {"eingerichtet" if secret_present("DIVERA_ACCESS_KEY") else "nicht eingerichtet"}</p>{keyform}{systemform}</div><div class="card"><h3>Empfänger</h3><p class="muted">Die endgültige Namensauswahl wird nach Validierung der realen DIVERA-Antwortstruktur aktiviert. Bis dahin werden keine Produktionsstatus angenommen.</p>{routing}</div>')

@app.post("/divera/key")
def set_key(csrf_token:str=Form(alias="csrf"),key:str=Form(),_=Depends(auth)):
 csrf(csrf_token)
 if len(key.strip())<4:raise HTTPException(400,"Access-Key ist leer/zu kurz")
 subprocess.run(["sudo","/usr/local/sbin/divera-set-credential","divera_access_key"],input=key.strip()+"\n",text=True,check=True)
 return RedirectResponse("/divera",303)

@app.post("/divera/system-key")
def set_system_key(csrf_token:str=Form(alias="csrf"),key:str=Form(),_=Depends(auth)):
 csrf(csrf_token)
 if len(key.strip())<4:raise HTTPException(400,"Systemnutzer-Key ist leer/zu kurz")
 subprocess.run(["sudo","/usr/local/sbin/divera-set-credential","divera_system_key"],input=key.strip()+"\n",text=True,check=True)
 return RedirectResponse("/divera",303)

@app.post("/divera/routing")
def set_routing(csrf_token:str=Form(alias="csrf"),test_ids:str=Form(""),technical_ids:str=Form(""),_=Depends(auth)):
 csrf(csrf_token);c=load_settings();c.routing.test_recipient_ids=ids(test_ids);c.routing.technical_recipient_ids=ids(technical_ids);save_settings(c)
 return RedirectResponse("/divera",303)

@app.get("/zigbee",response_class=HTMLResponse)
def zigbee(_=Depends(auth)):
 c=load_settings()
 try:detectors=json.loads(Path("/var/lib/divera-raspi-alarm/detectors.json").read_text())
 except Exception:detectors={}
 rows="".join(f'<div class="card"><b>{esc(name)}</b><p>Online: {esc(data.get("online","unbekannt"))} · Batterie: {esc(data.get("battery","unbekannt"))} · Batterie niedrig: {esc(data.get("battery_low",False))} · Fehler: {esc(data.get("fault",False))}</p></div>' for name,data in detectors.items()) or '<p class="muted">Noch keine Rauchmelder beobachtet.</p>'
 body=form("/zigbee/pair",f'<p>Pairing wird für {c.zigbee.permit_join_seconds} Sekunden geöffnet.</p>',"Pairing öffnen")
 return page("Rauchmelder / Zigbee",'<div class="card"><h3>SONOFF ZBDongle-P</h3><span class="badge">Automatische Erkennung</span>'+body+'</div><h2>Geräte</h2>'+rows)

@app.post("/zigbee/pair")
def pair(csrf_token:str=Form(alias="csrf"),_=Depends(auth)):
 csrf(csrf_token);seconds=load_settings().zigbee.permit_join_seconds
 publish.single("zigbee2mqtt/bridge/request/permit_join",payload=json.dumps({"time":seconds}),hostname="127.0.0.1")
 return RedirectResponse("/zigbee",303)

@app.get("/tests",response_class=HTMLResponse)
def tests(_=Depends(auth)):
 c=load_settings()
 days=" ".join(f'<label><input name="weekdays" type="checkbox" value="{d}" {"checked" if d in c.weekly_test.weekdays else ""}> {label}</label>' for d,label in DAYS.items())
 times="".join(f'<option {"selected" if f"{h:02d}:{mm:02d}"==c.weekly_test.time else ""}>{h:02d}:{mm:02d}</option>' for h in range(24) for mm in (0,15,30,45))
 body=form("/tests",f'<label><input type="checkbox" name="enabled" {"checked" if c.weekly_test.enabled else ""}> aktiviert</label><p>{days}</p><select name="time">{times}</select><p><label>Testempfänger-IDs <input name="recipient_ids" value="{esc(",".join(map(str,c.weekly_test.recipient_ids)))}"></label></p>')
 manual=form("/tests/run","","Systemtest jetzt ausführen")
 return page("Geplante Tests",'<div class="card"><h3>Automatischer Systemtest</h3>'+body+'<p class="muted">SYSTEMTEST – KEIN EINSATZ</p>'+manual+'</div>')

@app.post("/tests/run")
def run_test(csrf_token:str=Form(alias="csrf"),_=Depends(auth)):
 csrf(csrf_token)
 try:devices=list(json.loads(Path("/var/lib/divera-raspi-alarm/detectors.json").read_text()))
 except Exception:devices=[]
 for device in devices or ["alarmweg"]:publish.single(f"divera/systemtest/{device}",payload="{}",hostname="127.0.0.1")
 return RedirectResponse("/tests",303)

@app.post("/tests")
async def save_tests(request:Request,csrf_token:str=Form(alias="csrf"),enabled:str|None=Form(None),time:str=Form(),recipient_ids:str=Form(""),_=Depends(auth)):
 csrf(csrf_token);fd=await request.form();c=load_settings()
 c.weekly_test.enabled=enabled is not None;c.weekly_test.weekdays=[x for x in fd.getlist("weekdays") if x in DAYS];c.weekly_test.time=time;c.weekly_test.recipient_ids=ids(recipient_ids);save_settings(c)
 return RedirectResponse("/tests",303)

@app.get("/display",response_class=HTMLResponse)
def display(_=Depends(auth)):
 c=load_settings();body=form("/display",f'<label>DIVERA-Kiosk-URL <input size="60" name="url" value="{esc(c.kiosk.divera_url)}"></label><p><label>Bildschirm aus nach <input type="number" min="1" max="240" name="idle" value="{c.kiosk.display_idle_minutes}"> Minuten</label></p>')
 return page("Anzeige / Kiosk",'<div class="card"><h3>Kiosk</h3>'+body+'<p>PIR: BCM GPIO23 / Pin 16</p></div>')
@app.post("/display")
def save_display(csrf_token:str=Form(alias="csrf"),url:str=Form(""),idle:int=Form(),_=Depends(auth)):
 csrf(csrf_token);c=load_settings();c.kiosk.divera_url=url.strip();c.kiosk.display_idle_minutes=max(1,min(240,idle));save_settings(c);return RedirectResponse("/display",303)

@app.get("/system",response_class=HTMLResponse)
def system(_=Depends(auth)):
 c=load_settings(); recovery=form("/system/recovery",f'<label><input type="checkbox" name="enabled" {"checked" if c.monitoring.reboot_escalation_enabled else ""}> Reboot-Eskalation und Hardware-Watchdog nach Inbetriebnahme aktivieren</label>',"Wiederherstellungsrichtlinie speichern")
 p=form("/system/password",'<label>Aktuelles Passwort <input type="password" name="current" required></label><br><label>Neues Passwort <input type="password" name="new" minlength="10" required></label><br><label>Wiederholen <input type="password" name="confirm" minlength="10" required></label>',"Passwort ändern")
 session_form=form("/system/session",f'<label>Automatisch abmelden nach <input type="number" min="1" max="240" name="minutes" value="{c.administration.session_idle_minutes}" required> Minuten ohne Bedienung</label>',"Zeitlimit speichern")
 update=form("/system/update/check",'<p>Installierte Version: '+esc(installed_version())+'</p>',"Nach stabilem Update suchen")
 return page("System / Administration",'<div class="grid"><div class="card"><h3>Dienste</h3><p>Mosquitto · Zigbee2MQTT · Alarmdienst · Kiosk</p></div><div class="card"><h3>Wiederherstellung</h3><p>Healthchecks und gezielte Neustarts.</p>'+recovery+'</div></div><div class="card"><h3>Administrator-Sitzung</h3>'+session_form+'</div><div class="card"><h3>Administrator-Passwort</h3>'+p+'</div><div class="card"><h3>Updates</h3>'+update+'<p class="muted">Nur unveränderliche stabile GitHub Releases mit SHA-256-Digest werden akzeptiert.</p></div>')
@app.post("/system/session")
def save_session_timeout(csrf_token:str=Form(alias="csrf"),minutes:int=Form(),_=Depends(auth)):
 csrf(csrf_token)
 c=load_settings()
 c.administration.session_idle_minutes=max(1,min(240,minutes))
 save_settings(c)
 return RedirectResponse("/system",303)

@app.post("/system/password")
def password(csrf_token:str=Form(alias="csrf"),current:str=Form(),new:str=Form(),confirm:str=Form(),user=Depends(auth)):
 csrf(csrf_token)
 if not verify_os_password(user,current):raise HTTPException(403,"Aktuelles Passwort ist falsch")
 if new!=confirm or len(new)<10:raise HTTPException(400,"Neue Passwörter stimmen nicht überein oder sind zu kurz")
 subprocess.run(["sudo","/usr/local/sbin/divera-change-admin-password",user],input=new+"\n",text=True,check=True)
 return RedirectResponse("/system",303)

@app.post("/system/recovery")
def recovery(csrf_token:str=Form(alias="csrf"),enabled:str|None=Form(None),_=Depends(auth)):
 csrf(csrf_token);c=load_settings();c.monitoring.reboot_escalation_enabled=enabled is not None;save_settings(c)
 subprocess.run(["sudo","/usr/local/sbin/divera-apply-recovery-policy"],check=True)
 return RedirectResponse("/system",303)

@app.post("/system/update/check")
async def update_check(csrf_token:str=Form(alias="csrf"),_=Depends(auth)):
 csrf(csrf_token);info=await latest()
 if not info["newer"]:return HTMLResponse(page("Updates",'<div class="card"><h3>Aktuell</h3><p>Es ist kein neueres stabiles Release verfügbar.</p></div>'))
 body=f'<div class="card"><h3>Version {esc(info["version"])}</h3><p>Unveränderliches Release: {"ja" if info["immutable"] else "nein"}</p><pre>{esc(info["notes"])}</pre>'
 if info["immutable"]:body+=form("/system/update","",f'Version {esc(info["version"])} installieren')
 else:body+='<p class="warn">Installation gesperrt: Release ist nicht unveränderlich.</p>'
 return HTMLResponse(page("Update verfügbar",body+"</div>"))

@app.post("/system/update")
async def update_system(csrf_token:str=Form(alias="csrf"),_=Depends(auth)):
 csrf(csrf_token);info=await latest()
 if not info["newer"]:return RedirectResponse("/system",303)
 if not info["immutable"]:raise HTTPException(409,"Das neueste Release ist nicht unveränderlich und wird nicht installiert.")
 stage,digest=await download(info)
 subprocess.run(["sudo","/usr/local/sbin/divera-start-update",str(stage),info["version"],digest],check=True)
 return HTMLResponse(page("Update gestartet",f'<div class="card"><h3>Version {esc(info["version"])}</h3><p>Das Update läuft im Hintergrund. Die Administration wird während des Dienstneustarts kurz nicht erreichbar sein. Bei fehlgeschlagenem Healthcheck erfolgt automatisch ein Rollback.</p></div>'))
