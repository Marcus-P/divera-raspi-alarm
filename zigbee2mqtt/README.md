# Zigbee2MQTT

Target coordinator: SONOFF ZBDongle-P using the zstack adapter.

Production configuration will use the stable /dev/serial/by-id path and pairing will normally be disabled except for a short UI-controlled pairing window.

Device payload semantics, especially smoke test versus real smoke alarm, must be verified against the actual production smoke-detector model before enabling live DIVERA fire forwarding.
