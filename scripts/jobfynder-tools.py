#!/usr/bin/env python3
"""
Jobfynder Tools Registry CLI

Centralized management of /opt/jobfynder-docs/tools/jobfynder-tools.json.

Commands:
  list                 Print all tools in canonical display format (grouped by category).
  add <name> <url> [category] [description]   Add a tool (auto-id, dedupe by URL).
  check                Validate registry integrity (unique ids, required fields).
  reindex              Re-sort by category/name and re-assign sequential ids.

Exit codes: 0 ok, 1 error.
"""
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone

TOOLS_FILE = "/opt/jobfynder-docs/tools/jobfynder-tools.json"


def load():
    with open(TOOLS_FILE) as f:
        return json.load(f)


def save(data):
    data["updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(TOOLS_FILE, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def clean_url(url):
    url = url.strip().rstrip("/")
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url


def display_url(url):
    return url.replace("https://", "").replace("http://", "").replace("www.", "").rstrip("/")


def reindex(data):
    data["tools"].sort(key=lambda t: (t.get("category", "").lower(), t.get("name", "").lower()))
    for i, t in enumerate(data["tools"], 1):
        t["id"] = f"tool-{i:03d}"
    return data


def check(data):
    errors = []
    ids = [t["id"] for t in data["tools"]]
    if len(ids) != len(set(ids)):
        errors.append("duplicate ids")
    if ids != [f"tool-{i:03d}" for i in range(1, len(ids) + 1)]:
        errors.append("ids not sequential 1..N")
    for t in data["tools"]:
        for k in ("name", "url", "category", "description", "id"):
            if k not in t or not str(t[k]).strip():
                errors.append(f"{t.get('id','?')} missing {k}")
    return errors


def cmd_list(data):
    cats = defaultdict(list)
    for t in data["tools"]:
        cats[t["category"]].append(t)
    out = []
    for cat in sorted(cats):
        out.append(f"## {cat}\n")
        for t in sorted(cats[cat], key=lambda x: x["name"].lower()):
            out.append(f"{t['id']}")
            out.append(f"• Tool: {t['name']}")
            out.append(f"• URL: {display_url(t['url'])}")
            out.append(f"• Category: {t['category']}")
            out.append("")
            out.append(f"Description: {t['description']}")
            out.append("")
    return "\n".join(out).rstrip() + "\n"


def cmd_add(data, name, url, category, description):
    url = clean_url(url)
    norm = lambda u: u.rstrip("/").replace("www.", "").lower()
    if any(norm(t["url"]) == norm(url) for t in data["tools"]):
        print(f"error: tool already exists for {url}")
        return 1
    data["tools"].append({
        "name": name,
        "url": url,
        "category": category or "Uncategorized",
        "description": description or "",
    })
    reindex(data)
    save(data)
    print(f"added: {name} ({display_url(url)})")
    return 0


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    cmd = argv[0]
    data = load()
    if cmd == "list":
        print(cmd_list(data))
        return 0
    if cmd == "check":
        errs = check(data)
        if errs:
            print("FAIL:" + "\nFAIL:".join(errs))
            return 1
        print(f"OK: {len(data['tools'])} tools, valid")
        return 0
    if cmd == "reindex":
        reindex(data)
        save(data)
        print("reindexed")
        return 0
    if cmd == "add":
        if len(argv) < 3:
            print("usage: jobfynder-tools add <name> <url> [category] [description]")
            return 1
        return cmd_add(data, argv[1], argv[2], argv[3] if len(argv) > 3 else None,
                       " ".join(argv[4:]) if len(argv) > 4 else None)
    print(f"unknown command: {cmd}")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
