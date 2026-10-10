#!/usr/bin/env python3
"""Minimal PAM verifier, invoked per connection by a root-owned systemd socket.

Only the divera-alarm group may connect. The application never reads /etc/shadow.
No credentials are logged or persisted.
"""
import json
import sys
from pathlib import Path

import pam

ADMIN_FILE = Path("/var/lib/divera-raspi-alarm/admin-user")

def main():
    result = False
    try:
        line = sys.stdin.buffer.readline(4097)
        if not line.endswith(b"\n") or len(line) > 4096:
            raise ValueError("Invalid request length")
        request = json.loads(line)
        username = request.get("username")
        password = request.get("password")
        allowed = ADMIN_FILE.read_text(encoding="utf-8").strip()
        if (isinstance(username, str) and isinstance(password, str)
                and username == allowed and 0 < len(username) <= 128
                and 0 < len(password) <= 1024):
            result = bool(pam.pam().authenticate(username, password, service="login"))
    except Exception:
        pass  # Fail closed, without printing secrets or PAM details.
    sys.stdout.write("OK\n" if result else "DENIED\n")
    sys.stdout.flush()

if __name__ == "__main__":
    main()
