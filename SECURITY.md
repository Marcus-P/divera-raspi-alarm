# Security

## Secrets

DIVERA access keys, passwords, tokens and other credentials must never be committed **or stored persistently in plaintext on the Raspberry Pi**.

Persistent application credentials use systemd encrypted credentials. The encrypted blobs live under `/etc/credstore.encrypted/`. Services receive decrypted values only at runtime through systemd's per-service credential directory under `/run/credentials/…`; application code reads them there and must never log them.

The installer removes the obsolete `/etc/divera-raspi-alarm/secrets.env` path if present. No production `.env` secret store is supported.

On a Raspberry Pi without a TPM, encryption at rest protects against casual/offline disclosure but cannot provide the same hardware-bound key protection as a TPM-backed design. This limitation must be documented rather than hidden.

If a credential is ever exposed, revoke/rotate it immediately.

## Reporting

Report security issues privately to the project maintainer. Never put credentials or exploitable details in a public issue.
