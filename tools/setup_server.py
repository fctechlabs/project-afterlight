"""Install the locked server distribution and pinned NeoForge runtime with verified downloads."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def main():
    """Prepare a server without starting it or accepting the host's EULA implicitly."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--accept-eula', action='store_true', help='Use only after the host accepts https://aka.ms/MinecraftEULA.')
    args = parser.parse_args()
    if not shutil.which('java'):
        raise SystemExit('Java 21 is required. Install Java 21 and run this setup again.')
    subprocess.run([sys.executable, str(ROOT / 'tools/install_mods.py'), '--side', 'server', '--destination', str(ROOT / 'mods')], check=True, cwd=ROOT)
    runtime = json.loads((ROOT / 'pack/server-runtime.json').read_text())
    installer = ROOT / 'neoforge-installer.jar'
    if not installer.exists() or hashlib.sha512(installer.read_bytes()).hexdigest() != runtime['sha512']:
        request = urllib.request.Request(runtime['url'], headers={'User-Agent': 'AfterlightServerSetup/0.1'})
        with urllib.request.urlopen(request, timeout=120) as response:
            payload = response.read()
        if hashlib.sha512(payload).hexdigest() != runtime['sha512']:
            raise SystemExit('NeoForge installer hash mismatch. Setup stopped.')
        installer.write_bytes(payload)
    subprocess.run(['java', '-jar', str(installer), '--installServer'], check=True, cwd=ROOT)
    (ROOT / 'user_jvm_args.txt').write_text('-Xms2G\n-Xmx8G\n')
    if args.accept_eula:
        (ROOT / 'eula.txt').write_text('# Accepted explicitly by the host through --accept-eula.\neula=true\n')
    elif not (ROOT / 'eula.txt').exists():
        (ROOT / 'eula.txt').write_text('# Read https://aka.ms/MinecraftEULA before setting this to true.\neula=false\n')
    print('Server installed. Review eula.txt and server.properties, then use run.bat or run.sh.')


if __name__ == '__main__':
    main()
