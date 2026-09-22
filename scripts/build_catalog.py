#!/usr/bin/env python3
"""Build the EmuCoreV cheat catalog from the .psv packs in files/.

The catalog is consumed by the EmuCoreV Android app from
https://raw.githubusercontent.com/sashkinbro/EmuCoreV-Cheat/main/cheats.json

Requires Python 3.10+ and no third-party packages.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

REPO = "sashkinbro/EmuCoreV-Cheat"
BRANCH = "main"
SOURCE_COMMIT = "bb8158a1c696914a8ea2299889d42ab9a57a3ab2"
SOURCE_URL = f"https://github.com/r0ah/vitacheat/blob/{SOURCE_COMMIT}/db"
SOURCE_NAME = "VitaCheat database"

TITLE_ID_RE = re.compile(r"^[A-Z]{4}\d{5}$")
PACK_NAME_RE = re.compile(r"^([A-Za-z]{4}\d{5})(?:[-_](.+))?$")
BLOCK_RE = re.compile(r"^_V[01]\s+", re.IGNORECASE)
HEADER_RE = re.compile(r"^#\s*([^:]+):\s*(.*)$")


def parse_pack(path: Path) -> tuple[dict[str, str], int]:
    meta: dict[str, str] = {}
    blocks = 0
    with path.open("r", encoding="utf-8-sig", errors="replace") as handle:
        for raw in handle:
            line = raw.strip()
            if line.startswith("#"):
                match = HEADER_RE.match(line)
                if match:
                    meta[match.group(1).strip().lower()] = match.group(2).strip()
                continue
            if BLOCK_RE.match(line):
                blocks += 1
    return meta, blocks


def build_entry(path: Path, title_id: str, variant: str) -> dict:
    meta, blocks = parse_pack(path)
    data = path.read_bytes()
    title = meta.get("title", title_id)
    if variant:
        title = f"{title} ({variant.upper()})"
    return {
        "id": f"vitacheat-{path.stem.lower().replace('_', '-')}",
        "titleId": title_id,
        "title": title,
        "region": meta.get("region", ""),
        "version": meta.get("version", ""),
        "authors": meta.get("code author", meta.get("credits", "")),
        "description": meta.get("note", meta.get("type", "")),
        "blockCount": blocks,
        "packPath": f"files/{path.name}",
        "sha256": hashlib.sha256(data).hexdigest(),
        "downloadUrl": f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/files/{path.name}",
        "sourceUrl": f"{SOURCE_URL}/{path.name}",
        "sourceName": SOURCE_NAME,
        "license": "See LICENSES/NOTICE.txt",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--files", default="files", help="directory holding the .psv packs")
    parser.add_argument("--output", default="cheats.json", help="catalog to write")
    parser.add_argument("--report", default="build-report.json", help="build report to write")
    args = parser.parse_args()

    files_dir = Path(args.files)
    if not files_dir.is_dir():
        parser.error(f"pack directory not found: {files_dir}")

    entries: list[dict] = []
    skipped: list[dict] = []
    seen: set[str] = set()

    for path in sorted(files_dir.glob("*.psv")):
        match = PACK_NAME_RE.match(path.stem)
        if not match:
            skipped.append({"file": path.name, "reason": "invalid title id"})
            continue

        title_id = match.group(1).upper()
        variant = match.group(2) or ""
        if title_id in seen and not variant:
            skipped.append({"file": path.name, "reason": "duplicate title id"})
            continue

        entry = build_entry(path, title_id, variant)
        if entry["blockCount"] == 0:
            skipped.append({"file": path.name, "reason": "no _V0/_V1 cheat blocks"})
            continue

        if not variant:
            seen.add(title_id)
        entries.append(entry)

    entries.sort(key=lambda entry: (entry["titleId"], entry["packPath"]))
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    catalog = {
        "schemaVersion": 1,
        "generatedAt": generated_at,
        "source": {
            "name": SOURCE_NAME,
            "url": "https://github.com/r0ah/vitacheat",
            "commit": SOURCE_COMMIT,
        },
        "entryCount": len(entries),
        "blockCount": sum(entry["blockCount"] for entry in entries),
        "entries": entries,
    }

    Path(args.output).write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")

    report = {
        "generatedAt": generated_at,
        "sourceCommit": SOURCE_COMMIT,
        "packCount": len(entries),
        "blockCount": catalog["blockCount"],
        "skipped": skipped,
    }
    Path(args.report).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(f"catalog: {len(entries)} packs, {catalog['blockCount']} blocks, {len(skipped)} skipped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
