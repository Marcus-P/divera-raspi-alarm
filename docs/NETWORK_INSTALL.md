# Network installation strategy

## Important distinction

Raspberry Pi 4 Network Install can download and run Raspberry Pi Imager over wired Ethernet. It does not natively accept an arbitrary GitHub repository URL as an operating-system installer.

For this project the supported low-friction path will therefore be:

1. Raspberry Pi firmware Network Install starts Raspberry Pi Imager over Ethernet.
2. Install the supported 64-bit Raspberry Pi OS release to the local endurance microSD.
3. On first boot, run a small bootstrap entry point that retrieves this project's versioned installer.
4. The installer configures the appliance and then exposes all site-specific setup through the local graphical UI.

A future advanced option can provide a signed custom HTTP-boot image from infrastructure controlled by the project owner. That is deliberately separate from a plain GitHub URL because Raspberry Pi HTTP boot requires signed boot artifacts and has bootloader/security constraints.

## Production target

- Raspberry Pi 4 Model B
- wired Ethernet required during installation
- local 128 GB endurance microSD remains the normal root filesystem
- Raspberry Pi OS 64-bit
- installation is reproducible and versioned
- no secrets in repository, image, bootstrap URL, command line, or logs
- first-run secrets and site settings are entered in the graphical UI

## Bootstrap UX target

After the base OS is installed, deployment should require one obvious action, ultimately exposed as a desktop/first-run launcher where practical. The bootstrap performs prerequisite checks, installs the application/services, enables watchdog/recovery policies, and reboots into the DIVERA kiosk.

The installer must refuse unsupported hardware/OS combinations rather than silently creating a partially working appliance.
