# Architecture

## Goal
A hardware-bound, appliance-like Raspberry Pi system for this installation. It displays DIVERA 24/7, bridges Zigbee smoke-detector events to DIVERA, and is operable by non-IT personnel through a local browser UI.

## Runtime alarm path
frient/Develco smoke detector -> Zigbee -> SONOFF ZBDongle-P -> Zigbee2MQTT -> Mosquitto -> local alarm/routing service -> HTTPS over Ethernet/router -> DIVERA 24/7.

The detector's local siren remains autonomous.

## Network
Built-in Ethernet only, external router, DHCP default. No SIM/LTE configuration. No inbound Internet port. Loss of required connectivity is a technical fault.

## Browser appliance
Chromium starts automatically in kiosk mode with two URLs in fixed order:
1. configured DIVERA status/availability page
2. local admin UI

DIVERA must be the first visible tab after every boot/browser recovery. The kiosk tab bar stays hidden, but an attached keyboard can use Ctrl+Tab to reach administration and Ctrl+Tab again to return. Normal operation needs no keyboard/mouse.

## PIR/display
The Pi never powers down for inactivity. BCM GPIO23 wakes/cancels display blanking. Display idle time is configurable. This service is isolated from the alarm path.

## Administration
The local UI owns site configuration, secrets entry, Test mode, DIVERA personnel/test-recipient selection, later production status routing, Zigbee pairing/naming, detector health, system health and tests.

## Routing boundary
Test mode and production mode are separate routing policies. Test mode is default and fail-closed. A single central routing guard must apply recipient restrictions before any DIVERA alarm request is constructed, so individual event handlers cannot accidentally bypass Test mode.

## Self-healing
Layered recovery: systemd restart -> functional health checks -> targeted restart -> bounded escalation -> controlled reboot -> hardware watchdog. Running PID alone is not health.

## Storage
128 GB endurance microSD is not treated as unlimited. Persistent diagnostics remain available under hard retention/size limits. Unnecessary writes are minimized.

## Installation
Raspberry Pi firmware Network Install is used to obtain/install the supported 64-bit OS over wired Ethernet. A versioned bootstrap then installs this project. Plain firmware Network Install cannot directly treat a GitHub repository URL as an OS image; see NETWORK_INSTALL.md.
