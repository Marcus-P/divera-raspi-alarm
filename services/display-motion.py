#!/usr/bin/env python3
"""PIR display wake helper. Fixed signal: BCM GPIO23 / physical pin 16.
This service is isolated from the alarm path."""
GPIO=23
def main():
    raise SystemExit("GPIO backend intentionally not enabled until production OS/session is pinned")
if __name__=="__main__": main()
