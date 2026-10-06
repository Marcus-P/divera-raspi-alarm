# First installation target

Do not use this document as a production approval. It defines the first commissioning run.

## Prerequisites
- Raspberry Pi 4
- fresh supported Raspberry Pi OS 64-bit Desktop installation
- wired Ethernet with Internet access
- 128 GB endurance microSD
- optional at first boot: SONOFF ZBDongle-P; it may also be inserted later

## Coordinator behavior
The installer and udev/systemd hook scan stable Linux USB serial identities under /dev/serial/by-id. A matching SONOFF/ITead/CP2102-family serial device is recorded as the zstack adapter. Replugging or first insertion triggers discovery again and restarts Zigbee2MQTT when installed.

The stable by-id path is preferred over ttyUSB0 because enumeration numbers may change across reboots.

If no coordinator is connected, the rest of the appliance must remain operational and report the missing coordinator as a technical/setup state.

## Repository bootstrap
A public repository can be cloned directly by bootstrap-public.sh. A private repository cannot be anonymously cloned by a fresh Pi. Do not put a GitHub PAT in a command line, URL, image, repository or log.

For the current private-development phase, installation requires an authenticated Git checkout/deploy mechanism or a deliberately published release/bootstrap artifact. Before the user is instructed to wipe/install the production card, one of those paths must be finalized.

## Commissioning safety
Test mode remains ON by default. Live production recipient routing is not enabled merely by installing the appliance.
