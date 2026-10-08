# Source review — 2026-10-08

The existing 676 packs were compared to the pinned `r0ah/vitacheat` input and its current `master`. The filenames and text match after newline normalization; that source supplies no additional pack in this review.

| Source | Result |
| --- | --- |
| [CrossOut4/vitacheat](https://github.com/CrossOut4/vitacheat) | All 676 packs match the existing catalog; no extra title or code variant. |
| [vaass95/vitacheat](https://github.com/vaass95/vitacheat) | 312 packs, all existing IDs. 76 content differences come from a divergent partial snapshot, often lacking revision metadata. Not merged over newer attributed packs. |
| [ShumnoT/VitaCheatDatabase](https://github.com/ShumnoT/VitaCheatDatabase) | 119 `.psv` filenames. `PCSE00007(VPK).psv` refers to an existing ID. `PCSE00899.psv` is absent here, but has only two codes with no region, revision or author header; retained as a testing lead. |

Additional leads:

- [PCSE00360 attachment on GBAtemp](https://gbatemp.net/threads/vitacheat-finalcheat-database.485343/page-68): indexed post lists a 536-byte attachment, but ordinary public retrieval returned a challenge. The attachment contents and game revision were not inspected.
- [2025 PCSE00360 post](https://www.reddit.com/r/vitahacks/comments/1mak273): discusses slot-specific codes and crashes with all-character variants; its file link was unavailable. No file imported.
- [2025 Vita cheat files thread](https://gbatemp.net/threads/psvita-cheat-files-2025.577811/): advertises archives and `PCSG01326` codes, but archive contents were unavailable and the posted codes were described as potentially non-static. No file imported.

These are research leads, not compatibility claims. Existing regional releases must not be substituted for an absent title ID. A candidate needs its actual file, source/author attribution and a clearly recorded game revision or explicit unknown revision before it can be evaluated for addition. No new pack was added by this review.

The review did find a catalog integrity defect: hashes were generated before Git normalized the pack line endings, so none matched the published LF files. The builder and validator now use canonical LF bytes; the regenerated index validates all 676 packs. Native-compatible counting also includes bare `_V0`/`_V1` declarations, bringing the declared block total to 7,990.
