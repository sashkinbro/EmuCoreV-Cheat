EmuCoreV Cheat Catalog
======================

This repository holds the cheat catalog consumed by the EmuCoreV Android
emulator (a PS Vita emulator based on Vita3K):

`https://raw.githubusercontent.com/sashkinbro/EmuCoreV-Cheat/main/cheats.json`

Every entry is a per-title FinalCheat/VitaCheat `.psv` pack. The EmuCoreV cheat
manager lists the packs that match an installed game, downloads the pack and
lets the user switch the individual cheats on and off, in the pause menu or in
the cheat manager screen. Cheats are keyed by title id, so a pack made for one
region or revision must not be installed for another.

Contents
--------

- `cheats.json` - schema version 1 catalog used by EmuCoreV.
- `files/<TITLEID>.psv` - packs sourced from the pinned upstream revision;
  Git stores them with LF line endings.
- `sources.json` - source attribution and the exact input revision.
- `schemas/cheat-catalog.schema.json` - public catalog contract.
- `scripts/build_catalog.py` - regenerates `cheats.json` and
  `build-report.json` from `files/`.
- `scripts/validate_catalog.py` - dependency-free offline validator.
- `build-report.json` - what the last build produced, including skipped packs.
- `LICENSES/NOTICE.txt` - attribution and licensing notes.
- `.gitattributes` - keeps published `*.psv` packs on LF. Catalog SHA-256
  hashes use this LF-canonical form so builds stay stable across checkouts.

Source and attribution
----------------------

The pack text comes from the `db/` folder of
[r0ah/vitacheat](https://github.com/r0ah/vitacheat) at commit
`bb8158a1c696914a8ea2299889d42ab9a57a3ab2`. That repository is the community
database for the FinalCheat/VitaCheat plugins; each pack starts with the game
title, region, version, code authors and original sources, and those headers
are preserved unchanged.

The upstream repository publishes no blanket open-source license for the cheat
data, so this catalog does not relicense it. It preserves the pack text,
headers, author credits and source notes while Git normalizes line endings to
LF. Every catalog entry records the pinned per-file source URL. If a code
author asks for a pack to be removed, it will be removed from `files/` and
`cheats.json`.

Pack format
-----------

A pack is a UTF-8 text file named after the game title id:

```text
# Title: God of War Collection
# Region: USA
# Version: 1.00
# Code Author: dask

_V0 Inf HP
$D504 8230CB50 00000000
$8201 8230CEB8 00000164
$8800 00000000 00000000
$8601 8230CEB8 00000168
$8900 00000000 00000000

_V1 Max Gold
$0200 81000000 3B9AC9FF
```

`_V0` means the cheat is off until the user turns it on, `_V1` means it is on
as soon as the game boots. The EmuCoreV core supports the FinalCheat/VitaCheat
code types `$0`, `$3`, `$4`, `$5`, `$7`, `$8`, `$A`, `$B`, `$C` and `$D`; the
full description lives in the Vita3K cheat module documentation.

Rebuild and validate
--------------------

Requires Python 3.10 or newer and no third-party packages:

```bash
python scripts/build_catalog.py
python scripts/validate_catalog.py
```

`build_catalog.py` reads the header of every pack, counts `_V0`/`_V1` blocks
that contain at least one code line accepted by Vita3K's native parser, hashes
the LF-canonical bytes and rewrites `cheats.json` and `build-report.json`. This
excludes instruction-only markers and malformed or incomplete code lines from
the displayed block count; two-token shorthand lines are not accepted by the
native parser. Git publishes `.psv` packs with LF line endings, so the catalog
digest matches the downloaded pack even when a local input uses CRLF. Packs
with an invalid title id or without a single usable cheat block are listed in
the report and skipped instead of being published broken.

Adding a pack
-------------

1. Drop the pack into `files/` named after the title id (`PCSA00147.psv`).
2. Run `python scripts/build_catalog.py`.
3. Run `python scripts/validate_catalog.py`.
4. Commit both the pack and the regenerated catalog.

Keep the original header comments of the pack; they are the attribution that
the catalog entry and the app display.
