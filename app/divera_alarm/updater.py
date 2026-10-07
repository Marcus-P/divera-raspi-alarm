from pathlib import Path
import httpx
from packaging.version import Version

API="https://api.github.com/repos/Marcus-P/divera-raspi-alarm/releases/latest"
STATE=Path("/var/lib/divera-raspi-alarm/updates")
def installed_version():
 try:return Path("/opt/divera-raspi-alarm/current/VERSION").read_text().strip()
 except Exception:return "0.0.0"
async def latest():
 async with httpx.AsyncClient(timeout=20,follow_redirects=True,headers={"Accept":"application/vnd.github+json","X-GitHub-Api-Version":"2026-03-10"}) as c:
  r=await c.get(API);r.raise_for_status();d=r.json()
 tag=d["tag_name"];version=tag.removeprefix("v")
 asset=next((a for a in d.get("assets",[]) if a.get("name")==f"divera-raspi-alarm-{tag}.tar.gz"),None)
 if not asset or not asset.get("digest","").startswith("sha256:"):raise RuntimeError("Release asset has no GitHub SHA-256 digest")
 return {"tag":tag,"version":version,"newer":Version(version)>Version(installed_version()),"immutable":bool(d.get("immutable")),"notes":d.get("body") or "","asset":asset}
async def download(info):
 if not info["immutable"]:raise RuntimeError("Refusing mutable GitHub release")
 a=info["asset"];dest=STATE/info["tag"];dest.mkdir(parents=True,exist_ok=True);out=dest/"release.tar.gz"
 async with httpx.AsyncClient(timeout=120,follow_redirects=True) as c:
  async with c.stream("GET",a["browser_download_url"]) as r:
   r.raise_for_status()
   with out.open("wb") as h:
    async for chunk in r.aiter_bytes():h.write(chunk)
 return dest,a["digest"].split(":",1)[1]
