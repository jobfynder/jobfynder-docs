#!/usr/bin/env python3
"""
Jobfynder Links Registry CLI

Centralized management of /opt/jobfynder-docs/links/jobfynder-links.json.

Commands:
  list                 Print all links in canonical display format (grouped by category).
  add <name> <url> <category> [purpose] [status]   Add a link (auto-id, dedupe by URL).
  check                Validate registry integrity (unique ids, required fields).
  reindex              Re-sort by category/name and re-assign sequential ids.

Exit codes: 0 ok, 1 error.
"""
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone

LINKS_FILE = "/opt/jobfynder-docs/links/jobfynder-links.json"

CATEGORY_EMOJI = {
    "api": "🔌",
    "public site": "🌐",
    "external source": "🌍",
    "external tool": "🧩",
    "internal": "🛠",
}
CATEGORY_ORDER = ["API", "Public Site", "External Source", "External Tool", "Internal"]


def load():
    with open(LINKS_FILE) as f:
        return json.load(f)


def save(data):
    data["updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(LINKS_FILE, "w") as f:
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
    data["links"].sort(key=lambda l: (l.get("category", "").lower(), l.get("name", "").lower()))
    for i, l in enumerate(data["links"], 1):
        l["id"] = f"link-{i:03d}"
    return data


def check(data):
    errors = []
    ids = [l["id"] for l in data["links"]]
    if len(ids) != len(set(ids)):
        errors.append("duplicate ids")
    if ids != [f"link-{i:03d}" for i in range(1, len(ids) + 1)]:
        errors.append("ids not sequential 1..N")
    for l in data["links"]:
        for k in ("name", "url", "category"):
            if k not in l or not str(l[k]).strip():
                errors.append(f"{l.get('id','?')} missing {k}")
    return errors


def cmd_list(data):
    servers = data.get("servers", [])
    cats = defaultdict(list)
    for l in data["links"]:
        cats[l["category"]].append(l)

    out = []
    # Servers block
    if servers:
        out.append("## 🗄 Servers")
        for s in sorted(servers, key=lambda x: x.get("name", "")):
            out.append(f"{s['id']} · {s['name']} · {s.get('ip','')} · {s.get('role','')}")
        out.append("")

    # Category ordering (unknown categories appended alphabetically)
    known = [c for c in CATEGORY_ORDER if c in cats]
    unknown = sorted(c for c in cats if c not in CATEGORY_ORDER)
    for cat in known + unknown:
        items = sorted(cats[cat], key=lambda x: x["name"].lower())
        emoji = CATEGORY_EMOJI.get(cat.lower(), "")
        out.append(f"{emoji} {cat}".strip())
        out.append("")
        for l in items:
            out.append(f"{l['id']}")
            out.append(f"• Name: {l['name']}")
            out.append(f"• URL: {display_url(l['url'])}")
            out.append(f"• Category: {l['category']}")
            out.append(f"• Purpose: {l.get('purpose','')}")
            if l.get("ip"):
                out.append(f"• IP: {l['ip']}")
            if l.get("server"):
                sid = l["server"]
                sname = next((s.get("name", "") for s in servers if s.get("id") == sid), "")
                label = f"{sid} ({sname})" if sname else sid
                out.append(f"• Server: {label}")
            if l.get("access"):
                out.append(f"• Access: {l['access']}")
            out.append(f"• Status: {l.get('status','')}")
            out.append("")
    return "\n".join(out).rstrip() + "\n"


def cmd_add(data, name, url, category, purpose, status):
    url = clean_url(url)
    norm = lambda u: u.rstrip("/").replace("www.", "").lower()
    if any(norm(l["url"]) == norm(url) for l in data["links"]):
        print(f"error: link already exists for {url}")
        return 1
    data["links"].append({
        "name": name,
        "url": url,
        "category": category or "Uncategorized",
        "purpose": purpose or "",
        "status": status or "active",
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
        print(f"OK: {len(data['links'])} links, valid")
        return 0
    if cmd == "reindex":
        reindex(data)
        save(data)
        print("reindexed")
        return 0
    if cmd == "add":
        if len(argv) < 4:
            print("usage: jobfynder-links add <name> <url> <category> [purpose] [status]")
            return 1
        return cmd_add(data, argv[1], argv[2], argv[3],
                       " ".join(argv[4:6]) if len(argv) > 4 else None,
                       argv[5] if len(argv) > 5 else None)
    print(f"unknown command: {cmd}")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
