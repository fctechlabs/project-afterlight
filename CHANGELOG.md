# Changelog

# Project Afterlight 0.1.2 — Pebble gathering fix

- Fixed the missing starter pebble interaction described in Chapter 1.
- Hold Shift and right-click Dirt, Grass, or another block in the dirt tag with an empty main hand. Pebbles drop from the clicked face, matching ATM10Sky's starter interaction.
- Half of the drops are Stone Pebbles. The other half is split evenly between Andesite, Basalt, Blackstone, Diorite, Granite, and Deepslate Pebbles.
- Gathering leaves the block intact and respects canceled interactions, including claim and spawn protection. No empty offhand is required.
- Clarified the pebble and first Cobblestone quests. Existing quest progress and recipes are preserved.

Minecraft **1.21.1** · NeoForge **21.1.251** · Java **21**.

Use `Afterlight-0.1.2.zip` for the client or `Afterlight-0.1.2-server.zip` for the server. Update clients and servers together. No new world is required. Squat Grow's Mystical Agriculture and AE2 exclusions remain in place.


# Project Afterlight 0.1.1 — Starter growth fix

- Added **Squat Grow 21.1.4** for Minecraft 1.21.1 NeoForge. Repeatedly crouch near saplings and ordinary crops to accelerate their growth.
- Uses a **3-block radius**, **50% activation chance**, and **no held tool or equipment requirement**.
- **Mystical Agriculture crops and AE2 crystal growth are excluded.** Both integrations are disabled, and the blacklist prevents generic growth actions from affecting these blocks.
- Existing quests, recipes, world options and progression remain unchanged. This update adds one mod to both client and server; all players and the server must use the same pack version.
- Retains the corrected manifests, approved CC: Tweaked external jar, mod lists and license notices in both ZIPs.

**Minecraft 1.21.1 · NeoForge 21.1.251 · Java 21.** The client installs 380 mod jars and the server installs 337. Balance, performance and multiplayer testing continue; back up worlds before updating.

Download `Afterlight-0.1.1.zip` for the client or `Afterlight-0.1.1-server.zip` for the server. Import the client ZIP in CurseForge. For website submission, export the installed profile from the CurseForge app, select file type **Release**, and attach the server ZIP as an **Additional File**.


# Project Afterlight 0.1.0 — First public release

Build industry and magic above the void in Minecraft 1.21.1 with NeoForge.

- Choose a Default grassy island or a Skyfactory Dirt block and Oak tree from the signed lobby using `/skyblock gui`.
- Follow five connected main chapters, individual mod tutorials, and Tips and Tricks: 3,612 quests across 72 chapters.
- Connect material production through Immersive Engineering, PneumaticCraft, Mekanism, Industrial Foregoing, AE2, Ars Nouveau, Extended Crafting, and late ProjectE.
- Explore Create, Create Aeronautics, Oritech, Psi, Occultism and space as optional branches.
- Obtain resources normally found in Overworld structures through targeted skyblock recipes and encounters.
- Play together with separate islands, FTB Teams, shared quest progress, FTB Chunks claims and a matching dedicated-server package.
- Earn normal quest rewards with a separate 25% chance for a bonus Chance Cube.
- Use the custom title and loading screens built around the approved Afterlight artwork.

**Requirements:** Minecraft 1.21.1, NeoForge 21.1.251 and Java 21. The client installs 379 mod jars; the server installs 336. Start with 8 GB allocated to the client if your computer has enough available RAM.

**Testing continues.** This is the first public version. Expect balance changes and bugs, back up worlds before updating, and keep all players and the server on the same pack version. When reporting a problem, include the version, steps to reproduce it, and relevant logs or crash reports.

The version transition from the tested 0.1.0-alpha.14 build changes release identity, menu labels and documentation; the mods, crafting recipes, quest identities, layouts and rewards remain the same.

## Packaging correction — October 15, 2026

Both ZIPs now include a root `manifest.json`, `modlist.html` and manifest-relative `overrides/` content. The server ZIP retains its original root configuration and installer scripts.

Removed the unavailable CC Tweaked Compat file reference. The same tested CC: Tweaked 1.120.2 jar is now included as an approved Non-CurseForge mod with its publisher's license notices. Mod versions, gameplay settings, quests and recipes are unchanged. Download the corrected ZIPs again before submitting them; their checksums have changed.

## Downloads and installation

Download `Afterlight-0.1.0.zip` and use **Import** in the CurseForge app. GitHub's automatic source archives are not launcher-importable modpacks. For a server, extract `Afterlight-0.1.0-server.zip` into a separate folder and follow its included `docs/SERVER.md`.

For CurseForge website submission, use **Export Profile** on the installed client and upload the app-exported ZIP with file type **Release**, Minecraft **1.21.1**, and **NeoForge** where offered. Attach the server ZIP as an **Additional File**. GitHub publication does not automatically upload to CurseForge.
