from pathlib import Path
import os,tomllib,tempfile
from pydantic import BaseModel,Field
import tomli_w

CONFIG_PATH=Path(os.getenv("DRA_CONFIG","/var/lib/divera-raspi-alarm/config.toml"))
CREDENTIALS_DIRECTORY=Path(os.getenv("CREDENTIALS_DIRECTORY","/run/credentials"))

class Site(BaseModel): name:str="Feuerwehr"; timezone:str="Europe/Berlin"
class Kiosk(BaseModel): divera_url:str=""; admin_url:str="http://127.0.0.1:8765/"; display_idle_minutes:int=Field(10,ge=1,le=240)
class Routing(BaseModel):
 test_mode:bool=True
 test_recipient_ids:list[int]=Field(default_factory=list)
 technical_recipient_ids:list[int]=Field(default_factory=list)
 production_status_ids:list[int]=Field(default_factory=list)
 production_commissioned:bool=False
class WeeklyTest(BaseModel):
 enabled:bool=True
 weekdays:list[str]=Field(default_factory=lambda:["sunday"])
 time:str="12:00"
 label:str="SYSTEMTEST - KEIN EINSATZ"
 recipient_ids:list[int]=Field(default_factory=list)
class Monitoring(BaseModel): detector_offline_after_hours:int=24; service_recovery_attempts:int=3; reboot_escalation_enabled:bool=False
class Zigbee(BaseModel): permit_join_seconds:int=Field(180,ge=30,le=600)
class Hardware(BaseModel): pir_bcm_gpio:int=23
class Settings(BaseModel):
 site:Site=Site(); kiosk:Kiosk=Kiosk(); routing:Routing=Routing(); weekly_test:WeeklyTest=WeeklyTest()
 monitoring:Monitoring=Monitoring(); zigbee:Zigbee=Zigbee(); hardware:Hardware=Hardware()

def load_settings():
 if not CONFIG_PATH.exists(): return Settings()
 with CONFIG_PATH.open("rb") as h:return Settings.model_validate(tomllib.load(h))

def save_settings(settings:Settings):
 CONFIG_PATH.parent.mkdir(parents=True,exist_ok=True)
 data=tomli_w.dumps(settings.model_dump()).encode()
 fd,tmp=tempfile.mkstemp(prefix=".config.",dir=CONFIG_PATH.parent)
 try:
  os.fchmod(fd,0o640)
  with os.fdopen(fd,"wb") as h:
   h.write(data);h.flush();os.fsync(h.fileno())
  os.replace(tmp,CONFIG_PATH)
 finally:
  try:os.unlink(tmp)
  except FileNotFoundError:pass

def credential(name:str)->str:
 p=CREDENTIALS_DIRECTORY/name
 return p.read_text(encoding="utf-8").strip() if p.is_file() else ""
def secrets(): return {"DIVERA_ACCESS_KEY":credential("divera_access_key"),"DIVERA_SYSTEM_KEY":credential("divera_system_key")}
def secret_present(n): return bool(secrets().get(n))
