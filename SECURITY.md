# Security

## Secrets

Never commit DIVERA access keys, passwords, MQTT credentials, Wi-Fi credentials, SIM credentials, private keys, or site-specific tokens.

The appliance stores secrets only on the Raspberry Pi with restrictive permissions. The repository contains examples/placeholders only.

If a secret is committed accidentally, revoke/rotate it immediately and remove it from Git history before sharing the repository.

## Reporting

Please report security issues privately to the project maintainer rather than opening a public issue containing credentials or exploitable details.
