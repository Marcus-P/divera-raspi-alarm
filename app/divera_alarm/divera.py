import httpx
from .settings import secrets
BASE="https://www.divera247.com/api"
def key():
 k=secrets().get("DIVERA_ACCESS_KEY","")
 if not k: raise RuntimeError("DIVERA access key missing")
 return k
async def users():
 async with httpx.AsyncClient(timeout=15) as c:
  r=await c.get(f"{BASE}/users",params={"accesskey":key()});r.raise_for_status();return r.json()
async def send_alarm(title,text,recipient_ids):
 if not recipient_ids: raise RuntimeError("Refusing alarm without explicit recipients")
 data=[("accesskey",key()),("title",title),("text",text)]
 for rid in recipient_ids:data.append(("user_cluster_relation_ids[]",str(rid)))
 async with httpx.AsyncClient(timeout=15) as c:
  r=await c.post(f"{BASE}/alarm",data=data);r.raise_for_status();return r.json() if r.content else {"ok":True}
