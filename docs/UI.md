# Administration UI information architecture

The UI is intentionally split into focused areas.

## Overview
System health, alarm path health, Internet/DIVERA reachability, Zigbee coordinator, detector summary, current Test-mode state and recent bounded diagnostics.

## DIVERA and routing
DIVERA credential setup, refresh personnel list, select Test-mode recipients, prominent persistent Test-mode toggle/state, and later production readiness/status routing.

## Smoke detectors / Zigbee
Pairing window, paired devices, room/name assignment, battery, battery-low, fault, availability and last-seen.

## Scheduled tests
- enable/disable automatic end-to-end test
- weekday picker with independent checkboxes for Monday through Sunday
- one time selector using 15-minute increments (00:00, 00:15, 00:30, 00:45 ... 23:45)
- default: Sunday at 12:00
- select dedicated DIVERA test recipients
- label remains clearly non-operational: SYSTEMTEST - KEIN EINSATZ
- manual test action kept separate from the recurring schedule

Multiple selected weekdays use the same configured time. A future requirement for different times per weekday would be a separate schedule model.

## Display / kiosk
DIVERA URL, display idle time, PIR status/diagnostics and kiosk/browser state.

## System / administration
Service health/recovery information, software/version information and local administrative password change.

### Password change
The page asks for current password, new password and confirmation. Password fields are never prefilled or displayed after submission. Password values are never written to application logs or configuration.

The unprivileged web service calls a purpose-built privileged helper with a narrowly defined password-change operation. It must not be granted arbitrary sudo command execution. Authentication/authorization and CSRF protection are required before this action is enabled.
