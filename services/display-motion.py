#!/usr/bin/env python3
import subprocess
from gpiozero import MotionSensor
pir=MotionSensor(23)
def wake(): subprocess.run(["wlopm","--on","*"],check=False,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
while True:
 pir.wait_for_motion();wake();pir.wait_for_no_motion()
