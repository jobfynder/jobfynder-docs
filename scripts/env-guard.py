#!/usr/bin/env python3
"""
env-guard.py — secret-safe .env integrity guard for Jobfynder.

Prevents the MoA/context "runaway" failure mode by giving a single,
idempotent, secret-safe way to verify and repair .env files.

Operations (all print PRESENCE ONLY, never secret values):
  check <path>     Report each KEY= line count + which required keys are missing.
  dedupe <path>    Keep only the FIRST occurrence of each KEY= line.
  repair <path> --set KEY=VAL ...   Ensure each given KEY appears exactly once.

Usage examples:
  python3 scripts/env-guard.py check  /opt/jobfynder-infra/intelligence/.env
  python3 scripts/env-guard.py dedupe /opt/jobfynder-infra/intelligence/.env
  python3 scripts/env-guard.py repair /opt/jobfynder-infra/intelligence/.env \
      PORTKEY_API_KEY=... LANGFUSE_SECRET_KEY=...

Exit codes: 0 ok, 1 verify failed, 2 file/system error.
"""
import sys
from pathlib import Path


def _load(path):
    p = Path(path)
    if not p.exists():
        print(f"error: {path} not found")
        sys.exit(2)
    return p


def _counts(path) -> dict:
    p = _load(path)
    counts = {}
    for raw in p.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key = line.split("=", 1)[0].strip()
        counts[key] = counts.get(key, 0) + 1
    return counts


def cmd_check(path, required=()):
    counts = _counts(path)
    missing = [k for k in required if counts.get(k, 0) == 0]
    dupes = {k: v for k, v in counts.items() if v > 1}
    print(f"=== {path} ===")
    for k in sorted(counts):
        print(f"  {k}: {counts[k]} line(s)")
    if missing:
        print(f"  MISSING required: {missing}")
    if dupes:
        print(f"  DUPLICATES: {dupes}")
    if missing or dupes:
        print("  VERDICT: NOT CLEAN")
        return 1
    print("  VERDICT: CLEAN")
    return 0


def cmd_dedupe(path):
    p = _load(path)
    seen = set()
    out = []
    dropped = 0
    for raw in p.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            out.append(raw)
            continue
        key = line.split("=", 1)[0].strip()
        if key in seen:
            dropped += 1
            continue
        seen.add(key)
        out.append(raw)
    p.write_text("\n".join(out) + "\n")
    print(f"dedup: removed {dropped} duplicate line(s)")
    return 0


def cmd_repair(path, pairs):
    p = _load(path)
    lines = p.read_text().splitlines()
    counts = {}
    for raw in lines:
        line = raw.strip()
        if line and not line.startswith("#") and "=" in line:
            counts[line.split("=", 1)[0].strip()] = True
    changed = False
    for k, v in pairs:
        lines = [l for l in lines if not l.strip().startswith(k + "=")]
        lines.append(f'{k}="{v}"')
        changed = True
    if changed:
        p.write_text("\n".join(lines) + "\n")
    print("repair: each managed key set exactly once (values hidden)")
    return 0


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd, path = argv[0], argv[1]
    if cmd == "check":
        return cmd_check(path, required=argv[2:])
    if cmd == "dedupe":
        return cmd_dedupe(path)
    if cmd == "repair":
        # parse --set-style KEY=VAL pairs after the path
        pairs = []
        for a in argv[2:]:
            if "=" in a:
                k, v = a.split("=", 1)
                pairs.append((k.strip(), v.strip()))
        if not pairs:
            print("repair: no KEY=VAL pairs provided")
            return 2
        return cmd_repair(path, pairs)
    print(f"unknown command: {cmd}")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
