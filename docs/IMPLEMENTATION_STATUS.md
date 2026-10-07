# Implementation status

## Software foundation implemented

The `develop` branch is prepared for first hardware commissioning and is continuously checked by GitHub Actions.

Implemented:
- versioned first installation under `/opt/divera-raspi-alarm/releases/<version>` with atomic `current` symlink
- persistent mutable settings under `/var/lib/divera-raspi-alarm` with backward-compatible defaults
- systemd encrypted credentials; no persistent plaintext secret store
- separate least-privilege DIVERA alarm key and system-user/directory key
- PAM-authenticated loopback-only administration UI with CSRF protection
- persistent routing, scheduled-test and display settings
- local administrator password change through a narrow privileged helper
- timed Zigbee2MQTT pairing via the documented MQTT request
- detector state display and persisted last-seen/battery/fault state
- battery-low, fault and offline technical notifications with deduplication
- manual and scheduled MQTT-path system tests
- targeted service recovery, gated reboot escalation and gated hardware watchdog
- bounded journald, non-persistent Mosquitto queue state and bounded Chromium caches
- stable GitHub Release discovery, release notes, explicit install confirmation, GitHub SHA-256 asset verification, versioned installation and automatic health-check rollback
- mandatory per-release operator and installation documentation gate
- CI syntax, compatibility and plaintext-secret checks
- kiosk respawn, PIR GPIO23 display wake contract and automatic ZBDongle-P discovery

## Deliberate commissioning gates

Production fire routing remains locked until real-world values are observed rather than guessed:
- the purchased smoke detector's actual Zigbee2MQTT payload for smoke versus self-test
- the real DIVERA `/api/users` response for the dedicated system user and the unit's actual status identifiers
- the desired production-ready status mapping
- display/PIR behavior on the physical monitor
- complete end-to-end delivery to explicitly selected test recipients

GitHub release immutability must be enabled for the repository before the first stable release. The appliance refuses mutable releases.
