"""Install the exact Afterlight mod files and verify their published identities."""
import argparse
import concurrent.futures
import hashlib
import json
import shutil
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    """Return portable hashes for a completed file without trusting its filename."""
    hashes = {name: hashlib.new(name) for name in ('sha1', 'sha512')}
    with path.open('rb') as source:
        for chunk in iter(lambda: source.read(1048576), b''):
            for value in hashes.values():
                value.update(chunk)
    return {name: value.hexdigest() for name, value in hashes.items()}


def verify(path, entry):
    """Reject truncated files and files that differ from a recorded publisher hash."""
    if path.stat().st_size != entry['size']:
        raise ValueError(f"Unexpected size for {entry['filename']}")
    hashes = digest(path)
    for algorithm, expected in entry['hashes'].items():
        actual = hashes.get(algorithm)
        if actual is None:
            actual = hashlib.new(algorithm, path.read_bytes()).hexdigest()
        if actual.lower() != expected.lower():
            raise ValueError(f"{algorithm} mismatch for {entry['filename']}")
    return hashes


def install(entry, destination, offline):
    """Reuse a verified local file or atomically replace a completed download."""
    target = destination / entry['filename']
    try:
        if target.exists():
            return {'filename': entry['filename'], 'hashes': verify(target, entry), 'status': 'verified'}
        cache = ROOT / 'work/mods-cache' / entry['filename']
        temporary = target.with_suffix(target.suffix + '.part')
        if cache.exists():
            verify(cache, entry)
            shutil.copyfile(cache, temporary)
        elif offline:
            raise FileNotFoundError(f"Not installed: {entry['filename']}")
        else:
            for attempt in range(3):
                try:
                    request = urllib.request.Request(entry['download_url'], headers={'User-Agent': 'AfterlightPackBuild/0.1'})
                    with urllib.request.urlopen(request, timeout=90) as response, temporary.open('wb') as output:
                        shutil.copyfileobj(response, output)
                    break
                except Exception:
                    if attempt == 2:
                        raise
                    time.sleep(2 ** attempt)
        hashes = verify(temporary, entry)
        temporary.replace(target)
        return {'filename': entry['filename'], 'hashes': hashes, 'status': 'installed'}
    except Exception as exc:
        return {'filename': entry['filename'], 'error': str(exc)}


def main():
    """Install one locked file set and save a complete, inspectable verification report."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', type=Path, default=ROOT / 'mods')
    parser.add_argument('--offline', action='store_true', help='Verify installed files without downloading.')
    parser.add_argument('--workers', type=int, default=5)
    parser.add_argument('--side', choices=('client', 'server'), default='client')
    args = parser.parse_args()
    lock = json.loads((ROOT / 'pack/mods.lock.json').read_text(encoding='utf-8'))
    entries = [entry for entry in lock['files']
               if args.side != 'server' or entry.get('distribution') != 'Client']
    args.destination.mkdir(parents=True, exist_ok=True)
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        tasks = [pool.submit(install, entry, args.destination, args.offline) for entry in entries]
        for task in concurrent.futures.as_completed(tasks):
            results.append(task.result())
            if len(results) % 25 == 0 or 'error' in results[-1]:
                print(json.dumps({'completed': len(results), 'total': len(tasks), 'latest': results[-1]}), flush=True)
    report = {'pack_version': lock['version'], 'side': args.side, 'destination': str(args.destination), 'files': results,
              'unexpected_jars': sorted(path.name for path in args.destination.glob('*.jar')
                                        if path.name not in {row['filename'] for row in entries})}
    (ROOT / 'work').mkdir(exist_ok=True)
    report_name = 'install-report-server.json' if args.side == 'server' else 'install-report.json'
    (ROOT / 'work' / report_name).write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    failures = [row for row in results if 'error' in row]
    print(json.dumps({'verified': len(results) - len(failures), 'failures': failures,
                      'unexpected_jars': report['unexpected_jars']}, indent=2), flush=True)
    raise SystemExit(bool(failures or report['unexpected_jars']))


if __name__ == '__main__':
    main()
