# Hosting a server

Extract the server release ZIP into a dedicated folder. Install Python 3.10+ and
Java 21, then run `install-server.bat` on Windows or `sh install-server.sh` on Linux.
The installer downloads and verifies the exact server mods and NeoForge runtime.

Read https://aka.ms/MinecraftEULA and set `eula=true` in `eula.txt` if you accept it.
Review `server.properties` and `user_jvm_args.txt`, then use `run.bat` or `sh run.sh`.
The provided properties select `skyblockbuilder:skyblock` for a new `afterlight`
world. Keep `online-mode=true`. All players need the matching client release.

Open `/skyblock gui` to create islands and manage island-team invitations. Friends
sharing a base also join an FTB Teams party to share quests. Claim your base through
FTB Chunks and review fake-player permissions for machines. Back up worlds before
updates. Keep a running server separate from source and generated build folders.
