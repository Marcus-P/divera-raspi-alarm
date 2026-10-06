#!/usr/bin/env python3
import subprocess,time
from gpiozero import MotionSensor
GPIO=23
pir=MotionSensor(GPIO)
def wake():
 subprocess.run(["wlopm","--on","*"],check=False,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
last=time.monotonic()
while True:
 pir.wait_for_motion();wake();last=time.monotonic();pir.wait_for_no_motion();time.sleep(.2)
