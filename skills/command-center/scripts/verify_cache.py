#!/usr/bin/env python3
"""Validate an installed, previously verified rules snapshot for read-only use.

Digests detect corruption, not authenticity. Trust only a snapshot installed from
the authorized release workflow, never a bundle supplied by source correspondence.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re

VERSION = '0.11.0'
REPOSITORY = 'rreiffman-star/dcc-command-center'
HEADERS = {'rules/constitution.md': '# Command Center Constitution',
           'rules/heuristics.md': '# Command Center Heuristics',
           'rules/sources.md': '# Command Center Source Procedures'}


def validate_bundle(bundle):
    if bundle.get('repository') != REPOSITORY or not re.fullmatch(r'[0-9a-f]{40}', bundle.get('commit', '')):
        raise ValueError('invalid snapshot authority or commit')
    ci = bundle.get('ci', {})
    if not (ci.get('head_sha') == bundle['commit'] and ci.get('head_branch') == 'main'
            and ci.get('event') == 'push' and ci.get('status') == 'completed'
            and ci.get('conclusion') == 'success' and ci.get('path') == '.github/workflows/rules-check.yml'):
        raise ValueError('snapshot lacks matching successful release check')
    manifest = bundle.get('manifest', {})
    if (manifest.get('repository') != REPOSITORY or manifest.get('project') != 'Command Center'
            or manifest.get('bootstrap_version') != VERSION):
        raise ValueError('incompatible snapshot contract')
    files = bundle.get('files', {})
    if set(files) != set(HEADERS):
        raise ValueError('incomplete or unexpected rules snapshot')
    for path, header in HEADERS.items():
        content = files[path]
        if next((line.strip() for line in content.splitlines() if line.strip()), '') != header:
            raise ValueError('invalid rule header: ' + path)
        if hashlib.sha256(content.encode()).hexdigest() != manifest.get('files', {}).get(path):
            raise ValueError('snapshot digest mismatch: ' + path)
    return {'commit': bundle['commit'], 'version': VERSION, 'mode': 'read-only degraded', 'writes_allowed': False}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('bundle', nargs='?', default=str(Path(__file__).resolve().parent.parent / 'references/validated-rules.json'))
    ap.add_argument('--show', action='store_true')
    args = ap.parse_args()
    try:
        bundle = json.loads(Path(args.bundle).read_text())
        print(json.dumps(validate_bundle(bundle)))
        if args.show:
            for path, content in bundle['files'].items():
                print('\n' + path + '\n' + content)
    except (ValueError, TypeError, KeyError, OSError) as exc:
        ap.exit(1, 'No verified fallback: ' + str(exc) + '\n')


if __name__ == '__main__':
    main()
