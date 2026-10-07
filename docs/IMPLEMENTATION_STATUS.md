# Implementation status

## First-installable development appliance

The `develop` branch now has a public, token-free first-install path for a fresh Raspberry Pi OS 64-bit Desktop system.

Implemented for the first hardware commissioning:
- native Mosquitto
- Zigbee2MQTT 2.14.2 pinned with Node.js 24 and systemd watchdog
- automatic SONOFF/CP210x stable by-id discovery and zstack configuration
- local FastAPI administration UI and health endpoint
- two-tab Chromium kiosk under labwc with browser respawn
- PIR contract BCM GPIO23 / physical pin 16 and display power control
- bounded persistent journald
- MQTT smoke worker with deduplication and fail-closed Test-mode recipient guard
- encrypted systemd credential storage; no persistent plaintext secret file
- periodic functional service checks
- install-time self-test
- release/update architecture with rollback and non-breaking release contract
- UI reference images under `docs/images/`

## Commissioning gates

A successful software installation is not yet approval for operational fire-alarm forwarding. Test mode remains enabled.

During the first real-hardware commissioning we still deliberately validate:
- the purchased smoke detector's actual Zigbee2MQTT payload for real smoke versus detector self-test
- the real DIVERA account's personnel/status identifiers and desired production recipient mapping
- the DIVERA access key through encrypted credential enrollment
- display/PIR behavior on the actual monitor
- end-to-end test delivery to explicitly selected test recipients

Production routing stays locked until those observations are complete. No guessed identifier is used to bypass these gates.
