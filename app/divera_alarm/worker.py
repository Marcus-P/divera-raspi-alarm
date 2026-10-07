import asyncio,json,logging,time
from datetime import datetime
from pathlib import Path
import paho.mqtt.client as mqtt
from .settings import load_settings
from .divera import send_alarm

log=logging.getLogger("divera-alarm");logging.basicConfig(level=logging.INFO)
STATE=Path("/var/lib/divera-raspi-alarm/detectors.json")
last_alarm={};fault_sent=set();queue=None;loop=None
def load_state():
 try:return json.loads(STATE.read_text())
 except Exception:return {}
state=load_state()
def save_state():
 tmp=STATE.with_suffix(".tmp");tmp.write_text(json.dumps(state,separators=(",",":")));tmp.replace(STATE)

def recipients(c):
 if c.routing.test_mode:
  if not c.routing.test_recipient_ids:raise RuntimeError("Test mode active but no test recipients selected")
  return c.routing.test_recipient_ids
 if not c.routing.production_commissioned:raise RuntimeError("Production routing is not commissioned")
 raise RuntimeError("Production status routing awaits validated DIVERA status mapping")

async def technical(device,kind,text):
 c=load_settings();key=f"{device}:{kind}"
 if key in fault_sent:return
 if not c.routing.technical_recipient_ids:
  log.error("Technical fault has no configured recipients: %s %s",device,kind);return
 await send_alarm(f"TECHNISCHE STÖRUNG · {device}",text,c.routing.technical_recipient_ids);fault_sent.add(key)
 log.warning("Technical notification sent: %s",key)

async def handle_zigbee(topic,payload):
 parts=topic.split("/")
 if len(parts)<2 or parts[0]!="zigbee2mqtt":return
 device=parts[1]
 if device=="bridge":return
 now=time.time();entry=state.setdefault(device,{})
 if topic.endswith("/availability"):
  val=payload.strip().lower();online=val in ("online","true",'{"state":"online"}')
  entry["online"]=online;entry["last_seen"]=now;save_state()
  if not online:await technical(device,"offline",f"{device} ist nicht erreichbar.")
  else:fault_sent.discard(f"{device}:offline")
  return
 try:data=json.loads(payload)
 except Exception:return
 entry["last_seen"]=now;entry["online"]=True
 for k in ("battery","battery_low","fault","smoke","test"):
  if k in data:entry[k]=data[k]
 save_state()
 if data.get("battery_low") is True:await technical(device,"battery_low",f"Batteriewarnung von {device}.")
 else:fault_sent.discard(f"{device}:battery_low")
 if data.get("fault") is True:await technical(device,"fault",f"Gerätefehler von {device}.")
 else:fault_sent.discard(f"{device}:fault")
 if data.get("test") is True:return
 if data.get("smoke") is not True:return
 mono=time.monotonic()
 if mono-last_alarm.get(device,0)<120:return
 c=load_settings();target=recipients(c)
 await send_alarm(f"RAUCHALARM · {device}",f"Rauch erkannt durch {device}",target);last_alarm[device]=mono
 log.warning("Smoke alarm forwarded for %s to %d explicit recipient(s)",device,len(target))

async def handle_systemtest(device):
 c=load_settings()
 if not c.weekly_test.recipient_ids:raise RuntimeError("Scheduled test has no recipients")
 await send_alarm(c.weekly_test.label,f"Automatischer Systemtest · {device}",c.weekly_test.recipient_ids)
 log.info("System test delivered for %s",device)

async def consume():
 while True:
  topic,payload=await queue.get()
  try:
   if topic.startswith("divera/systemtest/"):await handle_systemtest(topic.rsplit("/",1)[-1])
   else:await handle_zigbee(topic,payload)
  except Exception as e:log.error("Event not forwarded: %s",e)

async def monitor(client):
 last_schedule=None
 while True:
  await asyncio.sleep(30);c=load_settings();now=datetime.now().astimezone()
  cutoff=time.time()-c.monitoring.detector_offline_after_hours*3600
  for device,e in list(state.items()):
   if e.get("last_seen",0)<cutoff:await technical(device,"offline",f"{device} hat sich seit mehr als {c.monitoring.detector_offline_after_hours} Stunden nicht gemeldet.")
  slot=f"{now.date()} {now:%H:%M}"
  if c.weekly_test.enabled and now.strftime("%A").lower() in c.weekly_test.weekdays and now.strftime("%H:%M")==c.weekly_test.time and slot!=last_schedule:
   devices=list(state) or ["alarmweg"]
   for device in devices:client.publish(f"divera/systemtest/{device}","{}")
   last_schedule=slot

def on_connect(client,userdata,flags,reason_code,properties):
 client.subscribe("zigbee2mqtt/#");client.subscribe("divera/systemtest/#")
def on_message(client,userdata,msg):
 if loop and queue:loop.call_soon_threadsafe(queue.put_nowait,(msg.topic,msg.payload.decode("utf-8","replace")))

async def main():
 global queue,loop
 loop=asyncio.get_running_loop();queue=asyncio.Queue()
 client=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,client_id="divera-alarm-worker");client.on_connect=on_connect;client.on_message=on_message
 client.connect("127.0.0.1",1883,60);client.loop_start()
 try:await asyncio.gather(consume(),monitor(client))
 finally:client.loop_stop();client.disconnect()
if __name__=="__main__":asyncio.run(main())
