# Release updates

The appliance is updated from **published GitHub Releases**, never by pulling an arbitrary development branch.

## Layout

- `/opt/divera-raspi-alarm/releases/<version>/`: immutable installed release
- `/opt/divera-raspi-alarm/current`: symlink to active release
- `/etc/divera-raspi-alarm/`: persistent site configuration
- `/etc/credstore.encrypted/`: persistent encrypted credentials
- `/var/lib/divera-raspi-alarm/`: persistent application state
- `/var/lib/zigbee2mqtt/`: persistent Zigbee state

Release installation must not overwrite persistent configuration, credentials or Zigbee state.

## Web UI

System → Updates shows installed version, latest available stable release, release notes and an explicit install action. Updates never install silently by default.

## Verification and rollback

A release is downloaded to a staging directory. The updater verifies the expected checksum/signature before extraction. It installs into a new versioned directory, switches `current` atomically, restarts affected services and runs functional health checks. The previous release remains available.

If the post-update health check fails, the updater switches `current` back to the previous release and restarts the services. A failed release is recorded so the UI can explain the rollback.

Database/configuration migrations must be backward-safe or provide an explicit rollback migration before a release is eligible for unattended rollback.

## Channels

Only stable GitHub Releases are offered by default. Development commits on `develop` are never offered to an installed appliance.
