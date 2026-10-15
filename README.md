# Project Afterlight

<p align="center"><img src="assets/branding/afterlight-curseforge-title-v7.png" width="320" alt="Project Afterlight"></p>

A Minecraft **1.21.1 / NeoForge 21.1.251 / Java 21** skyblock pack
with connected industry and magic, a large quest book, and late ProjectE.

Version: **0.1.1**. Back up worlds before updating.

**Early public release:** balance, performance and multiplayer testing are ongoing.
See [CREDITS.md](CREDITS.md) for provenance and third-party terms.

## Play

Import the release's CurseForge ZIP into CurseForge. Allocate around 8 GB if your
computer has enough memory. The source ZIP itself is not launcher-importable.

Create a Skyblock Builder world, read the lobby signs, and open `/skyblock gui`.
Choose **Default** for a grassy island or **Skyfactory** for one Dirt block and an
Oak tree. Each island team receives its own island. Friends sharing a base should
join both its Skyblock Builder island team and its FTB Teams party. FTB Chunks
provides claims; the FTB Teams party shares quest progress.

**Create, Aeronautics, Oritech, Psi, Occultism, and space are optional.**
There is no ATM Star or Kappa mode.

[Progression](docs/PROGRESSION.md) · [Mods](MODLIST.md) ·
[Server setup](docs/SERVER.md) · [Performance](docs/PERFORMANCE.md)

[Download 0.1.1](https://github.com/fctechlabs/project-afterlight/releases/tag/v0.1.1) ·
[Release notes](docs/RELEASE_0_1_1.md) · [Release files](releases/0.1.1/)

## Source

- `config/`: quests, islands, mod settings, and menu assets.
- `defaultconfigs/`: defaults copied into new worlds.
- `kubejs/`: recipes, compatibility data, items, and client behavior.
- `manifest.json` and `pack/`: exact publisher downloads and loader identity.
- `tools/`: three scripts for exporting and installing the pack.

With Python 3.10+, run `python3 tools/build_pack.py` to build the CurseForge client
and server ZIPs under `builds/0.1.1/artifacts/`. Mod jars are downloaded from
their publishers by the launcher or server installer and are excluded from Git.

For a CurseForge website submission, export the final client profile from the
CurseForge app, as required by its submission policy. The scripted client archive
is useful for reproducible builds and local imports; the GitHub source ZIP is not
a launcher-importable pack.

Report problems through GitHub Issues with the pack version and reproduction
steps. Review logs for personal information before posting. See
[CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), and [LICENSE](LICENSE).
