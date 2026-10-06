#!/usr/bin/env python3
import subprocess
from gpiozero import MotionSensor
pir=MotionSensor(23)
while True:
    pir.wait_for_motion()
    subprocess.run(["wlopm","--on","*"],check=False,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    pir.wait_for_no_motion()
