#!/usr/bin/env python3
"""Root-owned, socket-activated broker for explicitly allowed system actions.

The web server stays unprivileged with NoNewPrivileges=true. The only callers
are local processes with access to the divera-alarm group socket. Credentials
are never logged or echoed back.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ADMIN_FILE = Path("/var/lib/divera-raspi-alarm/admin-user")
SCRIPTS = Path("/usr/local/sbin")


def run(request):
    if not isinstance(request, dict):
        return False
    action = request.get("action")
    if action == "recovery":
        if set(request) != {"action"}:
            return False
        command = [str(SCRIPTS / "divera-apply-recovery-policy")]
        payload = None
    elif action == "set_credential":
        name = request.get("name")
        value = request.get("value")
        if (set(request) != {"action", "name", "value"}
                or name not in ("divera_access_key", "divera_system_key")
                or not isinstance(value, str) or not 4 <= len(value) <= 8192
                or "\n" in value or "\r" in value):
            return False
        command = [str(SCRIPTS / "divera-set-credential"), name]
        payload = value + "\n"
    elif action == "change_password":
        username = request.get("username")
        password = request.get("password")
        if (set(request) != {"action", "username", "password"}
                or not isinstance(username, str) or username != ADMIN_FILE.read_text().strip()
                or not isinstance(password, str) or not 10 <= len(password) <= 1024
                or "\n" in password or "\r" in password):
            return False
        command = [str(SCRIPTS / "divera-change-admin-password"), username]
        payload = password + "\n"
    elif action == "start_update":
        stage = request.get("stage")
        version = request.get("version")
        digest = request.get("digest")
        if (set(request) != {"action", "stage", "version", "digest"}
                or not all(isinstance(x, str) for x in (stage, version, digest))
                or not re.fullmatch(r"/var/lib/divera-raspi-alarm/updates/v[A-Za-z0-9._/-]+", stage)
                or ".." in Path(stage).parts
                or not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+([.-][A-Za-z0-9.-]+)?", version)
                or not re.fullmatch(r"[0-9a-fA-F]{64}", digest)):
            return False
        command = [str(SCRIPTS / "divera-start-update"), stage, version, digest]
        payload = None
    else:
        return False

    result = subprocess.run(command, input=payload, text=True,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                            timeout=75, check=False)
    if result.returncode != 0:
        print(f"Control action {action} failed (exit={result.returncode})", file=sys.stderr)
    return result.returncode == 0


def main():
    success = False
    try:
        line = sys.stdin.buffer.readline(16385)
        if line.endswith(b"\n") and len(line) <= 16384:
            success = run(json.loads(line))
    except Exception:
        pass  # Fail closed, without exposing passwords, tokens, or keys.
    sys.stdout.write("OK\n" if success else "DENIED\n")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
