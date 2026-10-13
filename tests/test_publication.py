"""Clone-portable preservation and publication-scope checks, not hardware tests."""
import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def test_imported_files_are_byte_identical_to_recorded_sources():
    manifest = json.loads((ROOT / 'docs/import-manifest.json').read_text(encoding='utf-8-sig'))
    assert manifest['source_commit'] == '74d44b09c65e2a839b74d834756f0d178207d679'
    assert len(manifest['files']) == 77
    for item in manifest['files']:
        path = ROOT / item['destination']
        assert path.stat().st_size == item['bytes'], item['destination']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256'], item['destination']


def test_import_excludes_physical_flight_helpers_and_raw_recordings():
    manifest = json.loads((ROOT / 'docs/import-manifest.json').read_text(encoding='utf-8-sig'))
    destinations = [row['destination'] for row in manifest['files']]
    assert not any('/controller/' in path or 'bench_io' in path for path in destinations)
    assert not any(path.endswith(('.ulg', '.h264', '.px4', '.so', '.exe')) for path in destinations)
    assert not any('credentials' in path or 'id_rsa' in path for path in destinations)


def test_new_entry_document_links_are_clone_local_or_explicit_web_links():
    paths = ['README.md', 'HANDOFF.md', 'docs/MAIXCAM2_START.md', 'docs/STATUS.md',
             'docs/PROVENANCE.md', 'docs/VALIDATION.md', 'tools/maixcam2/README.md',
             'examples/calibration/README.md']
    for name in paths:
        document = ROOT / name
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', document.read_text(encoding='utf-8')):
            if target.startswith(('https://', 'http://', '#')):
                continue
            assert (document.parent / target.split('#', 1)[0]).exists(), (name, target)
