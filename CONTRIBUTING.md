# Contributing to the EmuCoreV cheat catalog

Thanks for helping other players. This repository only accepts per-title
FinalCheat/VitaCheat `.psv` packs and the generated catalog around them.

## Adding or updating a pack

1. Name the file after the game title id: `files/PCSA00147.psv`.
   The title id must be four letters followed by five digits.
2. Keep the upstream header comments at the top of the file (`# Title:`,
   `# Region:`, `# Version:`, `# Code Author:`, `# Source:`). They are the
   attribution shown in the app and recorded in `cheats.json`.
3. Keep the original cheat names. `_V0` declares a cheat that is off by
   default, `_V1` declares one that is on when the game boots. New submissions
   should use `_V0`.
4. Regenerate the catalog and validate it:

   ```bash
   python scripts/build_catalog.py
   python scripts/validate_catalog.py
   ```

5. Commit the pack, `cheats.json` and `build-report.json` together. Do not
   hand-edit `cheats.json`; the script owns it.

## Rules

- One pack per title id. Regional variants use their own title id, not the
  same file.
- Do not rename or relicense other people's packs. If you are not the author,
  keep the original credits and sources in the header.
- Remove a pack when its author asks. Open an issue and it will be removed from
  `files/` and `cheats.json` in the next commit.
- Packs must be plain text, UTF-8, with no binary payloads.

## Testing a pack

The EmuCoreV app reads the catalog from the `main` branch. To try a pack before
merging, copy it to the emulator data folder manually:

```
Android/data/com.sbro.emucorev/files/cheats/<TITLEID>.psv
```

and open the in-game Cheats tab or the cheat manager screen.
