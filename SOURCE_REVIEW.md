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

The review found and fixed a catalog integrity defect: hashes were generated before Git normalized pack line endings, so they did not match the published LF files. The builder and validator now use canonical LF bytes. Block counts now include only declarations with at least one code line accepted by Vita3K's native parser. Of 7,990 `_V0`/`_V1` declarations, 73 are instruction-only or have no parseable code line, leaving 7,917 usable blocks across the 676 packs.

Four packs had a `# ID:` header that conflicted with their filename and game title. Vita3K's compatibility records distinguish [Ratchet & Clank 3 (PCSF00486)](https://github.com/Vita3K/compatibility/issues/257) from [Ratchet & Clank (PCSF00484)](https://github.com/Vita3K/compatibility/issues/255); [VitaGrafix's patchlist](https://github.com/Electry/VitaGrafixPatchlist/blob/master/patchlist.txt) likewise lists them separately. Upstream file history shows the PCSF00486 header was correct in 2019, then changed to PCSF00484 in CrossOut4's 2023 upload while the filename and title remained Ratchet & Clank 3 ([history](https://api.github.com/repos/r0ah/vitacheat/commits?path=db/PCSF00486.psv), [2023 change](https://github.com/r0ah/vitacheat/commit/21fbde4dce8933fea5b8d1379acabec90360d2ab)). The other corrected headers were introduced in 2023 uploads: [PCSB00859](https://github.com/r0ah/vitacheat/commit/f010cd7ad457258cb1b436b175d5f749660ab0a6), [PCSB01108](https://github.com/r0ah/vitacheat/commit/02c094a28d1e135b92d81ee672f26db730ffaa1f), and [PCSG00947](https://github.com/r0ah/vitacheat/commit/21fbde4dce8933fea5b8d1379acabec90360d2ab). Only the conflicting ID header was changed; code lines and author attribution were preserved. These metadata corrections do not independently verify cheat behavior.
