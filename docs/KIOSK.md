# Kiosk and local administration

## Browser layout
Chromium is launched in kiosk/fullscreen mode with two tabs in this exact order:
1. DIVERA operational/status page
2. local administration UI at the appliance-local address

The first tab is the normal visible screen. Chromium's tab strip and browser controls remain hidden.

## Administration access
For deliberate local maintenance, connect/use a keyboard and press **Ctrl+Tab** to switch to the administration tab. Pressing **Ctrl+Tab** again returns to DIVERA when only these two tabs are open.

The design must not depend on exposing browser chrome or leaving kiosk mode.

## Recovery invariant
Every fresh browser launch, crash recovery and system boot must recreate the two tabs and make DIVERA tab 1/current. Administration must never become the unattended default display.

## Display blanking
Inactivity blanks/powers down the display only. PIR activity on BCM GPIO23 wakes it immediately while both browser tabs and services remain alive.
