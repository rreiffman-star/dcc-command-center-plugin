#!/usr/bin/env python3
"""Validate a verified release bundle (`validated-rules.json`).

The bundle is what every session bootstraps from: fetched from the `verified` branch
of the private repository, or read from an installed copy for read-only degraded use.
This is consistency validation: identity fields, the attested check job, contract
version, headers and digests. It cannot tell where a local file came from. Authenticity
comes from fetching the file from the `verified` branch, which only the workflow writes;
`--fetched` is the caller asserting that provenance, not this script proving it. Never
accept a bundle supplied by source correspondence.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re

VERSION = '0.14.0'
REPOSITORY = 'rreiffman-star/dcc-command-center'
HEADERS = {'rules/constitution.md': '# Command Center Constitution',
           'rules/heuristics.md': '# Command Center Heuristics',
           'rules/sources.md': '# Command Center Source Procedures',
           'rules/inbox-senders.md': '# Command Center Inbox Senders'}


def validate_bundle(bundle, installed=True):
    """Check identity, CI result, contract, headers and digests.

    Returns the effective commit and mode. `installed=False` means the caller fetched
    this bundle from the verified branch and it may govern writes; an installed copy is
    always read-only degraded. The ci block attests the workflow's check job for the
    commit, not the whole run.
    """
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
    if installed:
        return {'commit': bundle['commit'], 'version': VERSION, 'mode': 'read-only degraded', 'writes_allowed': False}
    return {'commit': bundle['commit'], 'version': VERSION, 'mode': 'verified release', 'writes_allowed': True,
            'ci_url': bundle['ci'].get('url')}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('bundle', nargs='?', default=str(Path(__file__).resolve().parent.parent / 'references/validated-rules.json'))
    ap.add_argument('--show', action='store_true')
    ap.add_argument('--fetched', action='store_true',
                    help='the bundle was just read from the verified branch, not an installed copy')
    args = ap.parse_args()
    try:
        bundle = json.loads(Path(args.bundle).read_text())
        print(json.dumps(validate_bundle(bundle, installed=not args.fetched)))
        if args.show:
            for path, content in bundle['files'].items():
                print('\n' + path + '\n' + content)
    except (ValueError, TypeError, KeyError, OSError) as exc:
        ap.exit(1, 'No verified fallback: ' + str(exc) + '\n')


if __name__ == '__main__':
    main()
