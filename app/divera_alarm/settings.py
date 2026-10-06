from pathlib import Path
import os, tomllib
from pydantic import BaseModel, Field
CONFIG_PATH=Path(os.getenv("DRA_CONFIG","/etc/divera-raspi-alarm/config.toml"))
SECRET_PATH=Path(os.getenv("DRA_SECRETS","/etc/divera-raspi-alarm/secrets.env"))
class Site(BaseModel): name:str="Feuerwehr"; timezone:str="Europe/Berlin"
class Kiosk(BaseModel): divera_url:str=""; display_idle_minutes:int=Field(default=10,ge=1,le=240)
class WeeklyTest(BaseModel): enabled:bool=True; weekday:str="sunday"; time:str="12:00"; label:str="SYSTEMTEST - KEIN EINSATZ"
class Monitoring(BaseModel): detector_offline_after_hours:int=Field(default=24,ge=1,le=720); service_recovery_attempts:int=Field(default=3,ge=1,le=10)
class Zigbee(BaseModel): permit_join_seconds:int=Field(default=180,ge=30,le=600)
class Settings(BaseModel):
    site:Site=Site(); kiosk:Kiosk=Kiosk(); weekly_test:WeeklyTest=WeeklyTest(); monitoring:Monitoring=Monitoring(); zigbee:Zigbee=Zigbee()
def load_settings():
    if not CONFIG_PATH.exists(): return Settings()
    with CONFIG_PATH.open("rb") as h: return Settings.model_validate(tomllib.load(h))
def secret_present(name:str)->bool:
    if not SECRET_PATH.exists(): return False
    for raw in SECRET_PATH.read_text(encoding="utf-8").splitlines():
        line=raw.strip()
        if line and not line.startswith("#") and line.partition("=")[0]==name: return bool(line.partition("=")[2].strip())
    return False
