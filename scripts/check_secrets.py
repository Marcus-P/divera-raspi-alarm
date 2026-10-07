#!/usr/bin/env python3
from pathlib import Path
import re,sys
ROOT=Path(__file__).resolve().parents[1]
SKIP={".git"}
patterns=[
 re.compile(r'(?i)(?:access[_-]?key|api[_-]?key|token|password)\s*[=:]\s*["\']?([A-Za-z0-9_\-]{20,})'),
 re.compile(r'ghp_[A-Za-z0-9]{20,}'),
 re.compile(r'github_pat_[A-Za-z0-9_]{20,}'),
 re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
]
bad=[]
for p in ROOT.rglob("*"):
 if not p.is_file() or any(x in p.parts for x in SKIP):continue
 try:text=p.read_text(errors="ignore")
 except Exception:continue
 for n,line in enumerate(text.splitlines(),1):
  if "__UNCONFIGURED__" in line:continue
  if any(rx.search(line) for rx in patterns):bad.append(f"{p.relative_to(ROOT)}:{n}")
if bad:
 print("Potential secrets found:\n"+"\n".join(bad));sys.exit(1)
print("No obvious plaintext secrets found.")
