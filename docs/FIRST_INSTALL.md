# First installation

Target: Raspberry Pi 4 with a fresh current Raspberry Pi OS 64-bit Desktop installation on the endurance microSD, wired Ethernet and SSH enabled.

The repository is public, so the initial bootstrap needs no GitHub account, token or stored repository credential.

## Bootstrap

Run from the freshly installed Pi:

```bash
git clone --depth 1 --branch develop https://github.com/Marcus-P/divera-raspi-alarm.git /tmp/divera-raspi-alarm
sudo mkdir -p /opt/divera-raspi-alarm
sudo cp -a /tmp/divera-raspi-alarm/. /opt/divera-raspi-alarm/
sudo bash /opt/divera-raspi-alarm/installer/install.sh
```

The installer aborts on errors and finishes with `installer/verify-install.sh`. Only a passed self-test is considered a successful first installation.

## What is persistent

Site configuration, encrypted systemd credential blobs, Zigbee2MQTT state and paired-device state live outside replaceable application releases. No plaintext `.env` secret store is used. A reboot does not require credential entry.

## First reboot

After a successful self-test run `sudo reboot`. Desktop autologin starts the labwc session; Chromium opens the local administration UI until a DIVERA kiosk URL is configured. Once configured, DIVERA is tab 1 and the local UI tab 2.

The SONOFF ZBDongle-P may be present during installation or plugged in later. Its stable `/dev/serial/by-id` identity is detected and Zigbee2MQTT is configured for `zstack`.

## Safety state

Test mode is ON by default. Production recipient routing remains locked until the real DIVERA account status mapping and the purchased detector's real MQTT payloads have been observed during commissioning.
