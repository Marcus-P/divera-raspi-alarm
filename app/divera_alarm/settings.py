from pathlib import Path
import os,tomllib
from pydantic import BaseModel,Field
CONFIG_PATH=Path(os.getenv("DRA_CONFIG","/etc/divera-raspi-alarm/config.toml")); SECRET_PATH=Path(os.getenv("DRA_SECRETS","/etc/divera-raspi-alarm/secrets.env"))
class Site(BaseModel): name:str="Feuerwehr"; timezone:str="Europe/Berlin"
class Kiosk(BaseModel): divera_url:str=""; admin_url:str="http://127.0.0.1:8765/"; display_idle_minutes:int=Field(10,ge=1,le=240)
class Routing(BaseModel): test_mode:bool=True; test_recipient_ids:list[int]=[]; production_status_ids:list[int]=[]
class WeeklyTest(BaseModel): enabled:bool=True; weekdays:list[str]=["sunday"]; time:str="12:00"; label:str="SYSTEMTEST - KEIN EINSATZ"; recipient_ids:list[int]=[]
class Monitoring(BaseModel): detector_offline_after_hours:int=24; service_recovery_attempts:int=3
class Zigbee(BaseModel): permit_join_seconds:int=180
class Hardware(BaseModel): pir_bcm_gpio:int=23
class Settings(BaseModel): site:Site=Site(); kiosk:Kiosk=Kiosk(); routing:Routing=Routing(); weekly_test:WeeklyTest=WeeklyTest(); monitoring:Monitoring=Monitoring(); zigbee:Zigbee=Zigbee(); hardware:Hardware=Hardware()
def load_settings():
 if not CONFIG_PATH.exists(): return Settings()
 with CONFIG_PATH.open("rb") as h:return Settings.model_validate(tomllib.load(h))
def secrets():
 out={}
 if SECRET_PATH.exists():
  for raw in SECRET_PATH.read_text().splitlines():
   line=raw.strip()
   if line and not line.startswith("#") and "=" in line:
    k,v=line.split("=",1);out[k.strip()]=v.strip()
 return out
def secret_present(n):return bool(secrets().get(n))
