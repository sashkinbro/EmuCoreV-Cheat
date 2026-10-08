#!/usr/bin/env python3
"""Validate the EmuCoreV cheat catalog against the packs in files/.

Checks the catalog contract used by the Android client and verifies that every
entry matches the pack on disk byte for byte. Requires Python 3.10+.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from build_catalog import canonical_pack_bytes

TITLE_ID_RE = re.compile(r"^[A-Z]{4}\d{5}$")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", default="cheats.json")
    parser.add_argument("--files", default="files")
    args = parser.parse_args()

    problems: list[str] = []
    catalog_path = Path(args.catalog)
    if not catalog_path.is_file():
        print(f"error: catalog not found: {catalog_path}")
        return 1

    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    if catalog.get("schemaVersion") != 1:
        problems.append("schemaVersion must be 1")

    entries = catalog.get("entries")
    if not isinstance(entries, list) or not entries:
        problems.append("entries must be a non-empty array")
        entries = []

    ids: set[str] = set()
    pack_paths: set[str] = set()
    for entry in entries:
        entry_id = entry.get("id", "")
        title_id = entry.get("titleId", "")
        pack_path = entry.get("packPath", "")

        if not entry_id or entry_id in ids:
            problems.append(f"duplicate or empty id: {entry_id!r}")
        ids.add(entry_id)

        if not TITLE_ID_RE.match(title_id):
            problems.append(f"invalid titleId: {title_id!r}")

        if not entry.get("downloadUrl", "").startswith("https://"):
            problems.append(f"{title_id}: downloadUrl must be https")

        if entry.get("blockCount", 0) <= 0:
            problems.append(f"{title_id}: blockCount must be positive")

        pack_file = Path(args.files) / Path(pack_path).name
        if not pack_file.is_file():
            problems.append(f"{title_id}: pack missing on disk: {pack_file}")
            continue

        if pack_path in pack_paths:
            problems.append(f"{title_id}: duplicate packPath: {pack_path}")
        pack_paths.add(pack_path)

        digest = hashlib.sha256(canonical_pack_bytes(pack_file.read_bytes())).hexdigest()
        if entry.get("sha256") != digest:
            problems.append(f"{title_id}: sha256 mismatch")

        if entry.get("packPath") != f"files/{pack_file.name}":
            problems.append(f"{title_id}: packPath must be files/{pack_file.name}")

    on_disk = {f"files/{path.name}" for path in Path(args.files).glob("*.psv")}
    missing = on_disk - pack_paths
    if missing:
        problems.append(f"packs not in catalog: {', '.join(sorted(missing))}")

    if problems:
        for problem in problems:
            print(f"error: {problem}")
        return 1

    print(f"ok: {len(entries)} packs, {catalog.get('blockCount', 0)} blocks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
