import httpx
from .settings import credential
BASE="https://app.divera247.com/api"
def alarm_key():
 k=credential("divera_access_key")
 if not k:raise RuntimeError("DIVERA alarm access key missing")
 return k
def system_key():
 k=credential("divera_system_key")
 if not k:raise RuntimeError("DIVERA system user key missing")
 return k
async def users():
 async with httpx.AsyncClient(timeout=15,follow_redirects=True) as c:
  r=await c.get(f"{BASE}/users",params={"accesskey":system_key()});r.raise_for_status();return r.json()
async def send_alarm(title,text,recipient_ids):
 if not recipient_ids:raise RuntimeError("Refusing alarm without explicit recipients")
 data=[("accesskey",alarm_key()),("type",title),("text",text)]
 for rid in recipient_ids:data.append(("user_cluster_relation_ids[]",str(rid)))
 async with httpx.AsyncClient(timeout=15,follow_redirects=True) as c:
  r=await c.post(f"{BASE}/alarm",data=data);r.raise_for_status();return r.json() if r.content else {"ok":True}

async def send_news(title,text,recipient_ids):
 if not recipient_ids:raise RuntimeError("Refusing notification without explicit recipients")
 data=[("accesskey",alarm_key()),("type",title),("text",text)]
 for rid in recipient_ids:data.append(("user_cluster_relation_ids[]",str(rid)))
 async with httpx.AsyncClient(timeout=15,follow_redirects=True) as c:
  r=await c.post(f"{BASE}/news",data=data);r.raise_for_status();return r.json() if r.content else {"ok":True}
