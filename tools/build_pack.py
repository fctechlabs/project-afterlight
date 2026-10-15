"""Build launcher and server archives from modpack source without internal development files."""
import hashlib
import html
import json
from pathlib import Path
import urllib.request
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


def manifest_for(lock, side='client'):
    """Reference hosted files and exclude approved external jars from CurseForge's file-ID resolver."""
    files=[]
    for row in lock['files']:
        if side=='server' and row.get('distribution')=='Client':continue
        if row.get('curseforge_external'):
            if not row['curseforge_external'].get('approved_list_url'):
                raise ValueError('Missing external-mod approval evidence: '+row['filename'])
            continue
        if not row.get('curseforge_project_id') or not row.get('curseforge_file_id'):
            raise ValueError('Missing CurseForge file identity: '+row['filename'])
        files.append({'projectID':row['curseforge_project_id'],'fileID':row['curseforge_file_id'],'required':True})
    if len({(r['projectID'],r['fileID']) for r in files})!=len(files):raise ValueError('Duplicate CurseForge file identity')
    return {'minecraft':{'version':lock['minecraft'],'modLoaders':[{'id':lock['loader']+'-'+lock['loader_version'],'primary':True}]},
        'manifestType':'minecraftModpack','manifestVersion':1,'name':lock['name'],'version':lock['version'],
        'author':'FC Tech Labs','files':files,'overrides':'overrides'}


def external_files(root, lock, side='client'):
    """Cache approved external binaries and verify every recorded hash before packaging them."""
    result=[]
    for row in lock['files']:
        if not row.get('curseforge_external') or (side=='server' and row.get('distribution')=='Client'):continue
        name=row['filename']
        if Path(name).name!=name or not name.endswith('.jar'):raise ValueError('Unsafe external filename')
        if not row['curseforge_external'].get('approved_list_url'):raise ValueError('External approval not recorded')
        if not all(key in row['hashes'] for key in ('sha1','sha512')):raise ValueError('External jar lacks strong hashes')
        path=root/'work/mods-cache'/name;path.parent.mkdir(parents=True,exist_ok=True)
        if not path.exists():
            request=urllib.request.Request(row['download_url'],headers={'User-Agent':'ProjectAfterlight/pack-builder'})
            with urllib.request.urlopen(request,timeout=90) as response:payload=response.read()
        else:payload=path.read_bytes()
        if len(payload)!=row['size'] or any(hashlib.new(k,payload).hexdigest()!=v.lower() for k,v in row['hashes'].items()):
            raise ValueError('External jar differs from its published hashes: '+name)
        if not path.exists():path.write_bytes(payload)
        result.append((path,'mods/'+name))
    return result


def modlist_html(lock, side='client'):
    """Identify the publisher of each installed mod, including approved external downloads."""
    rows=[]
    for row in lock['files']:
        if side=='server' and row.get('distribution')=='Client':continue
        url=row['project_url'] if row.get('curseforge_external') else 'https://www.curseforge.com/projects/'+str(row['curseforge_project_id'])+'/files/'+str(row['curseforge_file_id'])
        rows.append('<li><a href="'+html.escape(url,quote=True)+'">'+html.escape(row['name'])+'</a></li>')
    return '<!doctype html><html lang="en"><meta charset="utf-8"><title>Project Afterlight mods</title><ul>'+''.join(rows)+'</ul></html>\n'


def validate_archive(path, manifest, bundled_hashes):
    """Reject missing root manifests, nested-only overrides, duplicate entries and undeclared jars."""
    with zipfile.ZipFile(path) as archive:
        names=archive.namelist()
        if names.count('manifest.json')!=1:raise ValueError('Exactly one root manifest.json is required')
        if len(names)!=len(set(names)):raise ValueError('Duplicate archive entry')
        if json.loads(archive.read('manifest.json'))!=manifest:raise ValueError('Archive manifest differs from selected files')
        if manifest.get('manifestType')!='minecraftModpack' or manifest.get('manifestVersion')!=1:raise ValueError('Invalid modpack manifest type')
        if manifest.get('overrides')!='overrides' or not any(n.startswith('overrides/') for n in names):raise ValueError('Missing overrides directory')
        if 'modlist.html' not in names:raise ValueError('Missing modlist.html')
        actual={n for n in names if n.endswith('.jar')}
        if actual!=set(bundled_hashes):raise ValueError('Unexpected or missing bundled jar')
        for name,digest in bundled_hashes.items():
            if hashlib.sha512(archive.read(name)).hexdigest()!=digest:raise ValueError('Bundled jar hash mismatch: '+name)
        if archive.testzip() is not None:raise ValueError('Corrupt ZIP entry')


def write_archive(path, files, generated, manifest, bundled_hashes):
    """Write the manifest first and validate the complete archive before exposing it as a release."""
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as archive:
        archive.writestr('manifest.json',json.dumps(manifest,indent=2)+'\n')
        for source, name in files:
            archive.write(source, name)
        for name, content in generated.items():
            archive.writestr(name, content)
    validate_archive(path,manifest,bundled_hashes)
    return {'file': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    """Export exact publisher manifests and server bootstrap files without downloading or starting Minecraft."""
    lock = json.loads((ROOT / 'pack/mods.lock.json').read_text())
    manifest=manifest_for(lock)
    assert json.loads((ROOT/'manifest.json').read_text())==manifest
    version = lock['version']
    assert version and all(character.isalnum() or character in '._-' for character in version)
    out = ROOT / 'builds' / version / 'artifacts'
    out.mkdir(parents=True, exist_ok=True)
    notices = [(ROOT / name, name) for name in ('LICENSE', 'CREDITS.md')]
    notices += [(path,path.relative_to(ROOT).as_posix()) for path in sorted((ROOT/'assets/licenses').rglob('*')) if path.is_file()]
    external=external_files(ROOT,lock)
    client_files = notices + [(path, 'overrides/' + path.relative_to(ROOT).as_posix()) for path in runtime_files()]+[(path,'overrides/'+name) for path,name in external]
    hashes={'overrides/'+name:hashlib.sha512(path.read_bytes()).hexdigest() for path,name in external}
    client = write_archive(out / ('Afterlight-' + version + '-CurseForge.zip'), client_files,
                           {'modlist.html':modlist_html(lock)},manifest,hashes)
    server_runtime=list(runtime_files(server=True))
    server_external=external_files(ROOT,lock,'server')
    server_files = notices + [(path, path.relative_to(ROOT).as_posix()) for path in server_runtime]
    server_files += [(path,'overrides/'+path.relative_to(ROOT).as_posix()) for path in server_runtime]
    server_files += server_external+[(path,'overrides/'+name) for path,name in server_external]
    server_hashes={prefix+name:hashlib.sha512(path.read_bytes()).hexdigest() for path,name in server_external for prefix in ('','overrides/')}
    server_files += [(ROOT / name, name) for name in ('pack/mods.lock.json', 'pack/server-runtime.json',
                    'tools/install_mods.py', 'tools/setup_server.py', 'docs/SERVER.md')]
    server = write_archive(out / ('Afterlight-' + version + '-server.zip'), server_files, {
        'modlist.html':modlist_html(lock,'server'),
        'server.properties': 'level-type=skyblockbuilder:skyblock\nlevel-name=afterlight\nspawn-protection=0\nallow-flight=true\nmax-players=12\nview-distance=8\nsimulation-distance=6\nonline-mode=true\nmotd=Project Afterlight\n',
        'eula.txt': '# Read https://aka.ms/MinecraftEULA before accepting.\neula=false\n',
        'install-server.bat': '@echo off\r\ncd /d "%~dp0"\r\npy -3 tools\\setup_server.py\r\npause\r\n',
        'install-server.sh': '#!/usr/bin/env sh\nset -eu\ncd "$(dirname "$0")"\npython3 tools/setup_server.py\n',
    },manifest_for(lock,'server'),server_hashes)
    print(json.dumps({'version': version, 'artifacts': [client, server]}, indent=2))


if __name__ == '__main__':
    main()
