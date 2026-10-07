import asyncio,json,logging,time
import paho.mqtt.client as mqtt
from .settings import load_settings
from .divera import send_alarm
log=logging.getLogger("divera-alarm"); logging.basicConfig(level=logging.INFO)
last={}
def recipients(c):
 if c.routing.test_mode:
  if not c.routing.test_recipient_ids: raise RuntimeError("Test mode active but no test recipients selected")
  return c.routing.test_recipient_ids
 raise RuntimeError("Production routing is locked until status mapping is explicitly commissioned")
async def handle(topic,payload):
 if topic.endswith("/availability"): return
 device=topic.split("/")[-1]
 try:data=json.loads(payload)
 except Exception:return
 if data.get("test") is True:return
 if data.get("smoke") is not True:return
 now=time.monotonic()
 if now-last.get(device,0)<120:return
 c=load_settings(); ids=recipients(c)
 await send_alarm(f"RAUCHALARM · {device}",f"Rauch erkannt durch {device}",ids);last[device]=now;log.warning("Smoke alarm forwarded for %s to %d explicit recipient(s)",device,len(ids))
def on_connect(client,userdata,flags,reason_code,properties):client.subscribe("zigbee2mqtt/+")
def on_message(client,userdata,msg):
 try:asyncio.run(handle(msg.topic,msg.payload.decode("utf-8","replace")))
 except Exception as e:log.error("Event not forwarded: %s",e)
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,client_id="divera-alarm-worker");c.on_connect=on_connect;c.on_message=on_message;c.connect("127.0.0.1",1883,60);c.loop_forever()
