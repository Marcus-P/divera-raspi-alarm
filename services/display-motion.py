#!/usr/bin/env python3
import subprocess,time,tomllib
from gpiozero import MotionSensor
with open("/etc/divera-raspi-alarm/config.toml","rb") as f:c=tomllib.load(f)
gpio=int(c.get("hardware",{}).get("pir_bcm_gpio",23)); idle=int(c.get("kiosk",{}).get("display_idle_minutes",10))*60
pir=MotionSensor(gpio); last=time.monotonic(); off=False
def power(on):subprocess.run(["wlopm","--on" if on else "--off","*"],check=False,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
while True:
 if pir.motion_detected:
  last=time.monotonic()
  if off:power(True);off=False
 elif not off and time.monotonic()-last>=idle:power(False);off=True
 time.sleep(.25)
