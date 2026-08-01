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


def _table(headers, rows):
    """Render a markdown-style table with aligned columns."""
    widths = [len(h) for h in headers]
    for r in rows:
        for i, c in enumerate(r):
            widths[i] = max(widths[i], len(c))
    out = []
    out.append("| " + " | ".join(h.ljust(widths[i]) for i, h in enumerate(headers)) + " |")
    out.append("|-" + "-|-".join("-" * w for w in widths) + "-|")
    for r in rows:
        out.append("| " + " | ".join(c.ljust(widths[i]) for i, c in enumerate(r)) + " |")
    return out


def _md_link(name, url):
    """Return a clickable markdown link."""
    return f"[{name}]({url})"


def cmd_list(data):
    servers = data.get("servers", [])
    links = data["links"]
    srv_by_id = {s["id"]: s for s in servers}
    out = []

    # ---- Clickable Index (Table of Contents) ----
    out.append("## 📑 Index")
    tocs = []
    if servers:
        tocs.append("- [Infrastructure](#infrastructure)")
    sections = [
        ("Services — Public", "#services--public"),
        ("Services — Internal (INTEL)", "#services--internal-intel"),
        ("Services — Internal (Other hosts)", "#services--internal-other-hosts"),
        ("External", "#external"),
    ]
    for label, anchor in sections:
        tocs.append(f"- [{label}]({anchor})")
    out.extend(tocs)
    out.append("")

    # ---- Servers / Infrastructure ----
    if servers:
        out.append("<a name='infrastructure'></a>")
        out.append("## 🗄 Infrastructure")
        rows = []
        for s in sorted(servers, key=lambda x: x.get("name", "")):
            rows.append([s["id"], s.get("name", ""), s.get("ip", ""), s.get("role", "")])
        out.extend(_table(["ID", "Server", "IP", "Role"], rows))
        out.append("")

    def bucket(pred):
        return [l for l in links if pred(l)]

    # Public
    pub = bucket(lambda l: l["category"] in ("Public Site", "API"))
    if pub:
        out.append("<a name='services--public'></a>")
        out.append("## 🌐 Services — Public")
        rows = []
        for l in sorted(pub, key=lambda x: x["name"].lower()):
            rows.append([l["id"], _md_link(l["name"], l["url"]), display_url(l["url"]),
                         l.get("description", "—")])
        out.extend(_table(["ID", "Service", "URL", "Description"], rows))
        out.append("")

    # Internal on INTEL server
    intel = [l for l in links if l.get("server") == "srv-001"]
    if intel:
        out.append("<a name='services--internal-intel'></a>")
        out.append("## 🛠 Services — Internal (INTEL · " + (srv_by_id.get("srv-001", {}).get("ip", "")) + ")")
        rows = []
        for l in sorted(intel, key=lambda x: x["name"].lower()):
            rows.append([l["id"], _md_link(l["name"], l["url"]), display_url(l["url"]),
                         l.get("description", "—"), l.get("note", "")])
        out.extend(_table(["ID", "Service", "URL / Port", "Description", "Notes"], rows))
        out.append("")

    # Internal on other hosts
    other_int = [l for l in links if l["category"] == "Internal" and l.get("server") != "srv-001"]
    if other_int:
        out.append("<a name='services--internal-other-hosts'></a>")
        out.append("## 🛠 Services — Internal (Other hosts)")
        rows = []
        for l in sorted(other_int, key=lambda x: x["name"].lower()):
            rows.append([l["id"], _md_link(l["name"], l["url"]), display_url(l["url"]),
                         l.get("description", "—")])
        out.extend(_table(["ID", "Service", "URL", "Description"], rows))
        out.append("")

    # External
    ext = [l for l in links if l["category"] in ("External Source", "External Tool")]
    if ext:
        out.append("<a name='external'></a>")
        out.append("## 🌍 External")
        rows = []
        for l in sorted(ext, key=lambda x: x["name"].lower()):
            rows.append([l["id"], _md_link(l["name"], l["url"]), display_url(l["url"]),
                         l.get("description", "—"), l.get("status", "")])
        out.extend(_table(["ID", "Service", "URL", "Description", "Status"], rows))
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
