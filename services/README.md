# Services

Service definitions and health/recovery logic live here.

Design rule: restart the smallest failed component first. Reboot the Raspberry Pi only after bounded targeted recovery fails. Severe OS hangs are covered by the hardware watchdog.
