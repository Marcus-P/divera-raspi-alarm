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


## Non-breaking release contract

Published releases MUST be backward compatible with already installed stable releases.

A release must never require the operator to reinstall the Raspberry Pi, re-pair Zigbee devices, re-enter credentials, manually rewrite configuration files, or lose site-specific settings merely because the software was updated.

Rules:

1. Existing configuration remains readable. New settings receive safe defaults.
2. Persistent state and Zigbee data are preserved.
3. Encrypted credentials keep their stable credential names and storage locations unless an automatic compatible migration is provided.
4. Data/configuration schema changes require automatic, idempotent migrations.
5. Migrations must preserve enough information for rollback. Destructive one-way migrations are not permitted in a stable release.
6. Existing MQTT topics and interpreted detector semantics may only be extended or compatibly migrated, never silently redefined.
7. Existing systemd/service integration and the web updater itself must remain upgradeable from prior stable versions.
8. Before publishing a stable release, CI/release testing must include an upgrade test from supported previous stable releases and a rollback test.
9. If a proposed feature cannot satisfy this contract, it is not eligible for a normal stable release. It must be redesigned rather than shipped as a breaking update.

This project therefore does not use a major-version bump as permission for breaking appliance updates. The installed appliance is expected to remain continuously upgradeable.


## Release documentation gate

Every stable release must update both `docs/ANWENDERDOKUMENTATION.md` and `docs/INSTALLATION.md`. Both files carry a `Dokumentationsstand` matching `VERSION`. The GitHub release workflow rejects a tag when either document does not match the release version, and from the second release onward also rejects a release if either document was unchanged since the previous tag.

Stable releases require GitHub release immutability. The appliance refuses to install a release whose GitHub API metadata does not report `immutable: true`, and verifies the downloaded asset against GitHub's published SHA-256 asset digest before privileged installation. Release creation is draft-first so all assets exist before publication/immutability.
