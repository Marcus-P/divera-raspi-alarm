# Fixed hardware wiring

## Raspberry Pi 4 GPIO header

The motion sensor is intentionally hardware-bound to the existing installation.

Reference orientation: "outer row" means the row nearest the PCB/case outer edge, as observed on the installed Raspberry Pi. In the standard 40-pin Raspberry Pi header this is the even-numbered physical-pin row.

Observed/user-confirmed connections, counted from the Pin 1 end along that outer row:

| Wire | Outer-row position | Physical pin | Raspberry Pi function |
|---|---:|---:|---|
| grey | 1 | 2 | +5 V |
| black | 3 | 6 | GND |
| white | 8 | 16 | GPIO23 |

Therefore the PIR signal input is **BCM GPIO23 / physical pin 16**.

## Safety

Do not move these wires while the Pi is powered.

The PIR module is powered from 5 V, but Raspberry Pi GPIO inputs are not 5 V tolerant. The existing installation is known to use the white signal lead on GPIO23. Before replacing the PIR with another model, its output voltage/interface must be verified; this documentation must not be treated as permission to connect an arbitrary 5 V signal directly to GPIO23.

## Software contract

The display-motion service will use BCM numbering and GPIO23 as the fixed PIR input. The purpose is display wake/activity detection only; failure of the PIR must not interfere with smoke-alarm forwarding or other critical alarm services.
