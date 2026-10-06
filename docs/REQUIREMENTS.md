# Requirements

## Operator experience
The target operator is a non-IT firefighter. Initial and ongoing configuration must be graphical and clear. Routine operation must not require shell access, YAML editing, MQTT topic editing, Python changes or systemd editing. Console access is reserved for installation/recovery, with the target of a single bootstrap action.

## Hardware baseline
- Raspberry Pi 4 Model B Rev 1.5, approximately 4 GB RAM
- 128 GB SanDisk High Endurance microSDXC, intended for years of 24/7 operation
- built-in Ethernet to an external router, DHCP by default; no SIM/LTE configuration
- SONOFF ZBDongle-P, CC2652P / zstack
- purchased frient/Develco smoke detector from the selected SMSZB-120 family; real identifiers/payloads verified during commissioning
- existing PIR: grey physical pin 2/+5 V, black pin 6/GND, white pin 16/BCM GPIO23

## Boot, kiosk and display
- unattended boot after power restoration
- supported Raspberry Pi OS 64-bit
- graphical session and Chromium start automatically
- DIVERA is always the first visible operational page in borderless fullscreen kiosk mode
- Chromium opens two kiosk tabs: first DIVERA, second the local administration UI
- the hidden tab strip is not required; an attached keyboard can switch tabs with Ctrl+Tab
- after browser restart/reboot DIVERA is again the first visible tab
- browser crash is recovered automatically
- Pi remains powered continuously
- display blanks after configurable inactivity and wakes immediately on PIR activity
- PIR/display failure is isolated from alarm forwarding

## Graphical administration
The local browser UI must provide:
- DIVERA access-key/settings entry without exposing stored secrets
- explicit persistent commissioning Test mode
- DIVERA personnel refresh/list and test-recipient selection by human-readable name
- later production readiness/status-routing configuration
- Zigbee pairing without console use
- detector/room naming
- detector battery, battery-low, fault, availability and last-seen
- system/service/network health
- manual tests and weekly test configuration/recipients
- kiosk URL, display/PIR settings and diagnostics

## Alarm behavior
- local detector siren remains autonomous; Raspberry Pi reporting is supplemental
- real smoke events are forwarded with device/room identity
- deduplication/cooldown prevents repeated alarm creation
- detector test events must never accidentally become real fire events
- battery-low, fault and offline conditions are technical notifications, never fire alarms
- technical notifications are deduplicated/rate-limited
- actual MQTT semantics for smoke/test are verified on the purchased detector before live production forwarding

## Commissioning Test mode
Test mode is a hard routing guard and defaults ON.
- every alarm event, including a real smoke event, is restricted to explicitly selected DIVERA test recipient(s)
- personnel are loaded from DIVERA and displayed by name; stable DIVERA IDs are stored internally
- production recipient/status logic is bypassed
- TEST MODE is unmistakably visible in the UI
- state and selected recipients survive reboot/update
- disabling Test mode requires explicit confirmation
- unresolved/unavailable recipient data fails closed; never fall back to all users
- no code path may omit recipient restriction while Test mode is active

## Production routing
After deliberate Test-mode exit, production routing can address personnel according to current DIVERA readiness/status. Exact status mapping is configurable and validated against the unit's real DIVERA setup; stale/unavailable status data gets explicit fail-safe behavior rather than guessed routing.

## Weekly end-to-end test
- schedule is fully configurable in the UI: one or more weekdays can be selected independently and the execution time is selected from 15-minute increments
- default is Sunday 12:00 local time
- synthetic per-configured-detector events exercise MQTT/alarm processing/Internet/DIVERA as far as practical
- unmistakable label: SYSTEMTEST - KEIN EINSATZ
- separate configurable test recipients
- records compact success/failure; failure becomes a technical fault where possible
- does not claim to test smoke chamber, siren or physical Zigbee RF path

## Zigbee
- Zigbee2MQTT plus Mosquitto, auto-starting
- ZBDongle-P uses zstack
- stable /dev/serial/by-id coordinator path discovered on real hardware
- permit_join false except for bounded pairing windows from the UI
- meaningful room/device names
- short USB extension recommended to reduce USB 3 interference

## Self-healing and monitoring
Critical components include alarm service, admin UI, Mosquitto, Zigbee2MQTT, coordinator, kiosk/Chromium and relevant network functions.
1. systemd restart/backoff
2. functional checks, not PID-only checks
3. targeted component/dependency restart
4. bounded retry/escalation
5. controlled Pi reboot after repeated recovery failure
6. Raspberry Pi hardware watchdog for severe OS hangs
Reboot must restore the complete appliance unattended and return to DIVERA fullscreen. Health checks themselves must not create write/log storms.

## Storage durability
Keep useful recent diagnostics, but strictly bound writes and disk use:
- journald hard size/retention limits
- bounded container logs if containers are used
- bounded Zigbee2MQTT/Mosquitto/application/watchdog logs
- normal operation without debug logging
- controlled Chromium cache/crash reporting
- avoid unnecessary swap writes; evaluate zram on the pinned OS
- disk-space monitoring
- filesystem remains writable; no blanket read-only design

## Security
- no DIVERA keys, passwords, Wi-Fi/network credentials, tokens, private keys or other deployment secrets in Git
- DIVERA key stored locally with restrictive permissions and never printed in logs/UI after entry
- admin UI local/LAN only and authenticated as appropriate; never Internet-exposed
- outbound HTTPS is sufficient; no inbound Internet port required


## Administration UI structure
The administration UI is divided into clear sections/pages rather than one overloaded dashboard. At minimum: Overview/System health, DIVERA & routing/Test mode, Smoke detectors/Zigbee, Scheduled tests, Display/Kiosk, and System/Administration.

## Local sudo password management
The graphical administration UI provides a dedicated password-change workflow for the appliance's local administrative Linux user. It must never store, echo, log, transmit to DIVERA, or commit the password. The UI asks for the current password plus new password and confirmation, uses a narrowly scoped privileged helper to perform the change, and returns only success/failure. The web application itself must not run as root and must not receive unrestricted sudo capability.
