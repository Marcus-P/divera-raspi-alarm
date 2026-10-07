# DIVERA Raspberry Alarm

A robust Raspberry Pi appliance for displaying DIVERA 24/7 and forwarding Zigbee smoke-detector events to DIVERA.

> Status: early development on the `develop` branch. Not for operational fire-safety use yet.

## Design goals

- simple enough for non-IT fire-service personnel
- browser-based graphical setup and administration
- unattended recovery after power loss or software failure
- layered watchdog/self-healing behavior
- battery, fault and detector-availability monitoring
- weekly end-to-end functional test
- endurance-friendly, strictly bounded logging
- no deployment credentials or secrets in Git

## Documentation

- [Anwenderdokumentation](docs/ANWENDERDOKUMENTATION.md)
- [Vollständige Installation und Inbetriebnahme](docs/INSTALLATION.md)
- [Weboberfläche mit Referenzansichten](docs/UI.md)
- [Update- und Rollbackkonzept](docs/UPDATES.md)
- [Anforderungen](docs/REQUIREMENTS.md)
- [Architektur](docs/ARCHITECTURE.md)

## Security

Never commit DIVERA keys, passwords, network credentials or private keys. See `SECURITY.md`.

## Development

All work currently lands on `develop`. The `main` branch is reserved for reviewed/stable milestones.
