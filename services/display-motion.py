#!/usr/bin/env python3
import json
import subprocess
import time
import urllib.request

from gpiozero import MotionSensor

# The desktop user cannot read the protected alarm state. The local admin
# service exposes only the non-secret settings needed by the display.
try:
    with urllib.request.urlopen("http://127.0.0.1:8765/api/display-config", timeout=5) as response:
        config = json.load(response)
except Exception as exc:
    print(f"Display settings unavailable; using safe defaults: {exc}", flush=True)
    config = {}

gpio = int(config.get("pir_bcm_gpio", 23))
idle = int(config.get("display_idle_minutes", 10)) * 60
pir = MotionSensor(gpio)
last = time.monotonic()
off = False

def power(on):
    subprocess.run(["wlopm", "--on" if on else "--off", "*"],
                   check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

while True:
    if pir.motion_detected:
        last = time.monotonic()
        if off:
            power(True)
            off = False
    elif not off and time.monotonic() - last >= idle:
        power(False)
        off = True
    time.sleep(.25)
