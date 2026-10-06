# Architecture

## Goal

A simple, self-healing Raspberry Pi appliance for fire stations. Normal administration is performed through a local browser-based UI; shell access is for maintenance only.

## Runtime path

Zigbee smoke detector -> SONOFF ZBDongle-P -> Zigbee2MQTT -> Mosquitto -> Alarm service -> DIVERA 24/7 API.

The smoke detector's local acoustic alarm remains autonomous. The Raspberry Pi path is supplemental remote reporting.

## User interface

The local setup/admin UI will cover:
- DIVERA configuration without exposing stored secrets
- Zigbee pairing and human-readable room/device names
- detector status, last seen, battery/low-battery, fault state
- system/service health
- weekly end-to-end test configuration and manual test
- kiosk/display settings and diagnostics

No normal setup step should require editing YAML, Python, systemd units, or MQTT topics manually.

## Kiosk

After boot, Chromium starts automatically in borderless kiosk mode and displays the configured DIVERA web page. The Pi remains powered. Display blanking/wake is handled separately from application uptime.

## Self-healing

Critical components are supervised in layers:
1. systemd restart policy for processes
2. functional health checks for alive-but-stuck components
3. targeted recovery of the failed component
4. bounded retry/escalation
5. controlled reboot when local recovery repeatedly fails
6. Raspberry Pi hardware watchdog for severe OS hangs

A running PID is not considered sufficient proof of health.

## Monitoring

Monitor at least:
- alarm service
- Mosquitto
- Zigbee2MQTT
- Zigbee coordinator availability
- detector availability/last-seen
- battery-low and detector fault states
- network reachability required for DIVERA
- kiosk/browser health

Technical faults must never be emitted as fire alarms.

## Weekly functional test

Default schedule: Sunday 12:00 local time, configurable in the UI.

A synthetic event is injected as early as practical into the software path and sent to a separately configurable DIVERA test recipient set. It must be unmistakably labelled as a system test / no deployment.

This validates the software/MQTT/Internet/DIVERA path but does not prove smoke chamber, siren, detector battery under load, or detector-to-coordinator RF operation. Those are monitored/tested separately where the hardware permits.

## Storage durability

Target medium: 128 GB endurance-class microSD.

Writes are deliberately bounded:
- journald hard size/retention limits
- bounded Docker/container logs if containers are used
- bounded Zigbee2MQTT and Mosquitto logging
- no unbounded application log files
- browser cache/crash-report policy
- avoid unnecessary swap writes
- disk-space monitoring

Useful recent diagnostics remain available; the filesystem is not made read-only.

## Security

No deployment secrets are stored in Git. Local secrets are root-readable only where practical. The appliance requires outbound connectivity; inbound Internet exposure is not required.
