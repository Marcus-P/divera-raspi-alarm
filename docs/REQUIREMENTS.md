# Requirements

## Operator experience

The target operator is a non-IT firefighter. Initial and ongoing configuration must be graphical and clear. Console work is limited to installation/recovery, with the long-term goal of a single bootstrap action.

## Required behavior

- Raspberry Pi boots unattended after power restoration.
- DIVERA web interface is the first operational screen, fullscreen/borderless.
- Browser and critical services recover automatically.
- Zigbee devices can be paired and named from the local web UI.
- Smoke events are forwarded to DIVERA with device/room identity and deduplication.
- Test events cannot be mistaken for real fire events.
- Battery-low and detector fault conditions create technical notifications, not fire alarms.
- Detector availability/last-seen is monitored.
- Weekly synthetic end-to-end test defaults to Sunday 12:00 and uses configurable test recipients.
- Health monitoring distinguishes process health from functional health.
- Repeated failed local recovery escalates to a controlled Pi reboot.
- Hardware watchdog provides a final recovery layer.
- Logs and other writes are strictly bounded for long-term SD-card operation.
- Secrets are never committed to the repository.

## Hardware baseline

- Raspberry Pi 4 Model B Rev 1.5, approximately 4 GB RAM
- 128 GB SanDisk High Endurance microSDXC
- SONOFF ZBDongle-P (CC2652P / zstack)
- frient/Develco Zigbee smoke detector from the selected SMSZB-120 family; exact identifiers and MQTT payload semantics will be verified on the purchased unit during commissioning
- motion sensor interface to be confirmed before implementation
- Internet: built-in Ethernet connected by LAN cable to an external router; DHCP expected; no SIM/modem configuration on the Pi
- motion sensor GPIO/interface: to be fixed from the actual wiring/photo before implementation


## Mandatory commissioning / test mode

The appliance has an explicit, persistent **Test mode** switch in the graphical UI.

When Test mode is enabled:
- every alarm event, including a real smoke event received from a detector, is routed only to the explicitly selected DIVERA test recipient(s)
- production recipient/status logic is not allowed to run
- the UI must show an unmistakable persistent TEST MODE warning
- the selected recipients are chosen by human-readable names loaded from DIVERA, while stable DIVERA relation IDs/foreign IDs are stored internally
- disabling Test mode requires an explicit confirmation; production routing is never enabled merely by rebooting or updating
- if the recipient list cannot be refreshed/resolved, fail safe: do not fall back to "all users"

Commissioning default: Test mode ON.

The later production mode will support status-dependent routing to personnel who are currently marked appropriately/einsatzbereit in DIVERA. Exact status mapping remains configurable and must be validated against the unit's DIVERA configuration.
