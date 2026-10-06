# DIVERA recipient routing

## Test mode

Test mode is a hard routing guard, not merely a label.

The application fetches the unit's users from DIVERA and presents human-readable personnel names in the local UI. The operator selects one or more test recipients. Internally the application uses stable DIVERA identifiers rather than names for alarm addressing.

While Test mode is enabled, all detector alarm events are restricted to those selected test recipients. Production status/group routing is bypassed. Failure to resolve a selected recipient must fail closed; it must never broaden an alarm to all personnel.

The UI shows a permanent prominent test-mode state. Test mode is the default during commissioning and persists across reboot.

## DIVERA API capabilities to use

Current DIVERA documentation provides a users endpoint that returns unit users, foreign IDs and current status. Alarm creation supports targeted persons using the person's foreign key or user-cluster-relation IDs.

Exact response schemas and account/license permissions will be validated against the real unit before enabling live alarm transmission.

## Production routing

After commissioning, production mode may target personnel according to current DIVERA readiness/status. The allowed statuses are configuration, not assumptions in code. The application will refresh/validate status data immediately before routing and will define explicit fail-safe behavior for unavailable/stale DIVERA status data.

## Safety invariant

There must be no code path in Test mode that omits recipient restriction and thereby falls back to DIVERA's default recipients.
