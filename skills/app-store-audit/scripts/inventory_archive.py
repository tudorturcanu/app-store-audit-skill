#!/usr/bin/env python3
"""Read-only inventory of an unpacked .xcarchive or .app; no compliance verdicts."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import plistlib
import sys
from xml.parsers.expat import ExpatError

BUNDLE_SUFFIXES = {'.app', '.appex', '.framework', '.bundle'}
INFO_KEYS = {
    'CFBundleIdentifier', 'CFBundleShortVersionString', 'CFBundleVersion',
    'CFBundleExecutable', 'CFBundlePackageType', 'MinimumOSVersion',
    'UIDeviceFamily', 'DTSDKName', 'DTXcode', 'DTXcodeBuild',
}
PRIVACY_KEYS = {
    'NSPrivacyTracking', 'NSPrivacyTrackingDomains',
    'NSPrivacyCollectedDataTypes', 'NSPrivacyAccessedAPITypes',
}
MAX_PLIST_BYTES = 4 * 1024 * 1024


def inventory(root):
    root = Path(root).absolute()
    if root.is_symlink() or not root.is_dir() or root.suffix not in {'.app', '.xcarchive'}:
        raise ValueError('Input must be an existing, non-symlink .app or .xcarchive directory.')
    result = {
        'schema_version': 1, 'input': str(root), 'bundles': [], 'manifests': [],
        'archive_metadata': None, 'skipped_symlinks': [], 'collection_errors': [],
        'limits': [
            'Inventory only: no compliance, signing, runtime, upload, or SDK-completeness verdict.',
            'Hashes identify inspected plist bytes only, not the entire archive or source revision.',
            'Symlinks are not followed. Localized strings and non-plist configuration are not inspected.',
            'Only selected Info.plist and privacy keys are emitted; review before sharing.',
        ],
    }

    def relative(path):
        return str(path.relative_to(root))

    def error(path, reason):
        result['collection_errors'].append({'path': relative(path), 'reason': reason})

    def read_plist(path, keys, purpose_strings=False):
        record = {'path': relative(path)}
        if path.is_symlink():
            if relative(path) not in result['skipped_symlinks']:
                result['skipped_symlinks'].append(relative(path))
            error(path, 'Symlink not inspected.')
            return record
        try:
            with path.open('rb') as stream:
                raw = stream.read(MAX_PLIST_BYTES + 1)
            if len(raw) > MAX_PLIST_BYTES:
                error(path, 'Plist exceeds 4 MiB inspection limit.')
                return record
            record['sha256'] = hashlib.sha256(raw).hexdigest()
            try:
                data = plistlib.loads(raw)
            except (AttributeError, RecursionError) as exc:
                # plistlib can raise AttributeError for malformed XML dates and
                # RecursionError for deeply nested binary containers.
                error(path, f'Unable to parse plist ({type(exc).__name__}).')
                return record
            if not isinstance(data, dict):
                error(path, 'Plist root is not a dictionary.')
                return record
            selected = {key: value for key, value in data.items() if key in keys}
            props = selected.get('ApplicationProperties')
            if isinstance(props, dict):
                selected['ApplicationProperties'] = {k: v for k, v in props.items()
                                                     if k in INFO_KEYS | {'ApplicationPath'}}
            # Preserve malformed types as collection errors, never stringify arbitrary bytes.
            try:
                json.dumps(selected, allow_nan=False)
            except (TypeError, ValueError):
                error(path, 'Selected fields contain non-JSON values; inspect original plist.')
                return record
            except RecursionError:
                error(path, 'Selected fields exceed JSON nesting limits; inspect original plist.')
                return record
            record['fields'] = selected
            if purpose_strings:
                record['purpose_string_keys'] = sorted(k for k in data
                                                      if k.startswith('NS') and k.endswith('UsageDescription'))
        except (OSError, ValueError, plistlib.InvalidFileException, OverflowError, ExpatError) as exc:
            error(path, f'Unable to read plist ({type(exc).__name__}).')
        return record

    if root.suffix == '.xcarchive':
        result['archive_metadata'] = read_plist(root / 'Info.plist', {'ApplicationProperties', 'ArchiveVersion'})

    def walk_error(exc):
        path = Path(exc.filename) if exc.filename else root
        error(path, f'Directory traversal failed ({type(exc).__name__}).')

    for directory, dirs, files in os.walk(root, followlinks=False, onerror=walk_error):
        base = Path(directory)
        dirs.sort()
        files.sort()
        for name in list(dirs):
            path = base / name
            if path.is_symlink():
                result['skipped_symlinks'].append(relative(path))
                dirs.remove(name)
        for name in files:
            path = base / name
            if path.is_symlink():
                result['skipped_symlinks'].append(relative(path))
        if base.suffix in BUNDLE_SUFFIXES:
            plist = base / 'Info.plist'
            record = read_plist(plist, INFO_KEYS, purpose_strings=True)
            result['bundles'].append({'bundle_path': relative(base), 'info': record})
        for name in files:
            if name == 'PrivacyInfo.xcprivacy':
                result['manifests'].append(read_plist(base / name, PRIVACY_KEYS))
    result['skipped_symlinks'] = sorted(set(result['skipped_symlinks']))
    if not any(Path(b['bundle_path']).suffix == '.app' or b['bundle_path'] == '.'
               for b in result['bundles']):
        error(root, 'No app bundle found; confirm the intended artifact.')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('artifact', help='Unpacked .xcarchive or .app directory')
    args = parser.parse_args()
    try:
        report = inventory(args.artifact)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(report, indent=2, sort_keys=True, allow_nan=False))
    return 1 if report['collection_errors'] or report['skipped_symlinks'] else 0


if __name__ == '__main__':
    sys.exit(main())
