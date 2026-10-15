"""Build launcher and server archives from modpack source without internal development files."""
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
CLIENT_CONFIGS = {'cumulus_menus-client.toml', 'create-client.toml', 'supplementaries-client.toml'}


def runtime_files(server=False):
    """Select shipped configuration and scripts while omitting client-only presentation on servers."""
    for folder in ('config', 'defaultconfigs', 'kubejs'):
        for path in sorted((ROOT / folder).rglob('*')):
            if not path.is_file() or path.suffix.lower() == '.md':
                continue
            relative = path.relative_to(ROOT)
            if server and relative.parts[:2] in (('config', 'fancymenu'), ('config', 'drippyloadingscreen')):
                continue
            if server and relative.parts[0] == 'config' and path.name in CLIENT_CONFIGS:
                continue
            yield path


def write_archive(path, files, generated):
    """Write and verify an archive containing only the explicit source and generated entries."""
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as archive:
        for source, name in files:
            archive.write(source, name)
        for name, content in generated.items():
            archive.writestr(name, content)
    with zipfile.ZipFile(path) as archive:
        assert archive.testzip() is None
        assert not any(name.endswith('.jar') for name in archive.namelist())
    return {'file': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    """Export exact publisher manifests and server bootstrap files without downloading or starting Minecraft."""
    lock = json.loads((ROOT / 'pack/mods.lock.json').read_text())
    manifest = json.loads((ROOT / 'manifest.json').read_text())
    assert manifest['version'] == lock['version']
    identities = {(row['curseforge_project_id'], row['curseforge_file_id']) for row in lock['files']}
    assert len(identities) == len(lock['files'])
    assert identities == {(row['projectID'], row['fileID']) for row in manifest['files']}
    version = lock['version']
    assert version and all(character.isalnum() or character in '._-' for character in version)
    out = ROOT / 'builds' / version / 'artifacts'
    out.mkdir(parents=True, exist_ok=True)
    notices = [(ROOT / name, name) for name in ('LICENSE', 'CREDITS.md')]
    client_files = notices + [(path, 'overrides/' + path.relative_to(ROOT).as_posix()) for path in runtime_files()]
    client = write_archive(out / ('Afterlight-' + version + '-CurseForge.zip'), client_files,
                           {'manifest.json': json.dumps(manifest, indent=2) + '\n'})
    server_files = notices + [(path, path.relative_to(ROOT).as_posix()) for path in runtime_files(server=True)]
    server_files += [(ROOT / name, name) for name in ('pack/mods.lock.json', 'pack/server-runtime.json',
                    'tools/install_mods.py', 'tools/setup_server.py', 'docs/SERVER.md')]
    server = write_archive(out / ('Afterlight-' + version + '-server.zip'), server_files, {
        'server.properties': 'level-type=skyblockbuilder:skyblock\nlevel-name=afterlight\nspawn-protection=0\nallow-flight=true\nmax-players=12\nview-distance=8\nsimulation-distance=6\nonline-mode=true\nmotd=Project Afterlight\n',
        'eula.txt': '# Read https://aka.ms/MinecraftEULA before accepting.\neula=false\n',
        'install-server.bat': '@echo off\r\ncd /d "%~dp0"\r\npy -3 tools\\setup_server.py\r\npause\r\n',
        'install-server.sh': '#!/usr/bin/env sh\nset -eu\ncd "$(dirname "$0")"\npython3 tools/setup_server.py\n',
    })
    print(json.dumps({'version': version, 'artifacts': [client, server]}, indent=2))


if __name__ == '__main__':
    main()
