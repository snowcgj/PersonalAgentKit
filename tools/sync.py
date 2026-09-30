"""Single-source distribution. Default is read-only plan; --apply writes with backups."""
import argparse
import hashlib
import json
from pathlib import Path
from datetime import datetime

BEGIN = '<!-- AGENTKIT:BEGIN -->'
END = '<!-- AGENTKIT:END -->'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def merge(existing, body):
    if existing.count(BEGIN) != existing.count(END) or existing.count(BEGIN) > 1:
        raise ValueError('Malformed AgentKit markers')
    block = BEGIN + '\n' + body.rstrip() + '\n' + END
    if BEGIN in existing:
        left, rest = existing.split(BEGIN, 1)
        _, right = rest.split(END, 1)
        return left + block + right
    return existing + ('\n\n' if existing else '') + block + '\n'

def managed(text):
    if BEGIN not in text:
        return None
    merge(text, '')  # validate markers
    return text.split(BEGIN, 1)[1].split(END, 1)[0].replace('\r\n', '\n')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    config = json.loads((root / 'adapters/clients.json').read_text(encoding='utf-8'))
    statefile = root / 'adapters/state.json'
    state = json.loads(statefile.read_text(encoding='utf-8')) if statefile.exists() else {}
    body = (root / 'rules/common.md').read_text(encoding='utf-8')
    plans = []
    targets = set()
    for client, settings in config.items():
        dest = Path(settings['rules'])
        old = dest.read_bytes() if dest.exists() else None
        text = old.decode('utf-8-sig') if old is not None else ''
        current = managed(text)
        record = state.get(str(dest))
        if current is not None:
            if not record or digest(current.encode()) != record.get('managed_hash'):
                raise RuntimeError(f'Rule conflict: {dest}')
        elif record:
            raise RuntimeError(f'Managed rules removed: {dest}')
        newtext = merge(text, body)
        new = newtext.encode('utf-8')
        plans.append((dest, old, new, {'managed_hash': digest(managed(newtext).encode())}))
        for skill in sorted((root / 'skills').iterdir()):
            if not skill.is_dir() or not (skill / 'SKILL.md').is_file():
                continue
            if not skill.name.startswith('agentkit-'):
                raise RuntimeError(f'Use agentkit- prefix for shared skills: {skill}')
            for source in sorted(skill.rglob('*')):
                if source.is_symlink():
                    raise RuntimeError(f'Symlink source unsupported: {source}')
                if not source.is_file():
                    continue
                target = Path(settings['skills']) / skill.name / source.relative_to(skill)
                previous = target.read_bytes() if target.exists() else None
                data = source.read_bytes()
                saved = state.get(str(target))
                if previous is not None and (not saved or digest(previous) != saved.get('hash')):
                    raise RuntimeError(f'Skill conflict: {target}')
                if previous is None and saved:
                    raise RuntimeError(f'Managed skill removed: {target}')
                plans.append((target, previous, data, {'hash': digest(data)}))
    for dest, old, new, record in plans:
        if str(dest) in targets:
            raise RuntimeError(f'Duplicate target: {dest}')
        targets.add(str(dest))
        print(('UNCHANGED ' if old == new else 'WRITE     ') + str(dest))
    stale = set(state) - targets
    if stale:
        raise RuntimeError('Source removed; review stale distributed files manually: ' + ', '.join(sorted(stale)))
    if not args.apply:
        print('Preview only. Use --apply to write.')
        return
    stamp = datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    backup = root / 'backups' / stamp
    changes = []
    for index, (dest, old, new, record) in enumerate(plans):
        if old == new:
            state[str(dest)] = record
            continue
        # Recheck to avoid overwriting a concurrent edit after planning.
        live = dest.read_bytes() if dest.exists() else None
        if live != old:
            raise RuntimeError(f'Concurrent modification: {dest}')
        backup.mkdir(parents=True, exist_ok=True)
        saved = None
        if old is not None:
            saved = str(backup / f'{index}.bin')
            Path(saved).write_bytes(old)
        changes.append({'path': str(dest), 'backup': saved, 'new_hash': digest(new)})
        (backup / 'manifest.json').write_text(json.dumps(changes, ensure_ascii=False, indent=2), encoding='utf-8')
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(new)
        state[str(dest)] = record
        statefile.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Applied {len(changes)} changes; backups: {backup if changes else "none"}')

if __name__ == '__main__':
    main()
