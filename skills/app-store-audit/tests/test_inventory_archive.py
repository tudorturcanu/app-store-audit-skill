"""Run with python3 -m unittest discover -s tests -v from the skill directory."""
import hashlib
import importlib.util
import json
from pathlib import Path
import plistlib
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/inventory_archive.py'
spec = importlib.util.spec_from_file_location('inventory_archive', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'Release with spaces.xcarchive'
        self.app = self.root / 'Products/Applications/Example.app'
        self.app.mkdir(parents=True)
        self.write(self.root / 'Info.plist', {'ApplicationProperties': {
            'ApplicationPath': 'Applications/Example.app', 'CFBundleVersion': '42',
            'PrivateMetadata': b'DO_NOT_EMIT'}})
        self.write(self.app / 'Info.plist', {'CFBundleIdentifier': 'test.example',
                   'CFBundleVersion': '42', 'NSCameraUsageDescription': 'Scan',
                   'PRIVATE_API_TOKEN': 'DO_NOT_EMIT'})

    def write(self, path, data, binary=False):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(plistlib.dumps(data, fmt=plistlib.FMT_BINARY if binary else plistlib.FMT_XML))

    def cli(self, artifact=None):
        return subprocess.run([sys.executable, str(SCRIPT), str(artifact or self.root)],
                              capture_output=True, text=True)

    def test_nested_bundles_manifests_hashes_and_no_mutation(self):
        extension = self.app / 'PlugIns/Scanner.appex'
        self.write(extension / 'Info.plist', {'CFBundleIdentifier': 'test.example.scanner'}, True)
        manifest = extension / 'SDK.bundle/PrivacyInfo.xcprivacy'
        self.write(manifest.parent / 'Info.plist', {'CFBundleIdentifier': 'test.sdk'})
        self.write(manifest, {'NSPrivacyTracking': False, 'NSPrivacyAccessedAPITypes': []}, True)
        before = {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        run = self.cli()
        self.assertEqual(run.returncode, 0, run.stderr)
        report = json.loads(run.stdout)
        self.assertEqual(len(report['bundles']), 3)
        self.assertEqual(len(report['manifests']), 1)
        self.assertEqual(report['manifests'][0]['sha256'], hashlib.sha256(manifest.read_bytes()).hexdigest())
        self.assertNotIn('DO_NOT_EMIT', run.stdout)
        self.assertEqual(report['bundles'][0]['info']['purpose_string_keys'], ['NSCameraUsageDescription'])
        self.assertEqual(before, {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()})

    def test_missing_and_malformed_plists_preserve_partial_inventory(self):
        (self.app / 'Info.plist').unlink()
        (self.app / 'PrivacyInfo.xcprivacy').write_text('<plist><broken>')
        run = self.cli()
        self.assertEqual(run.returncode, 1, run.stderr)
        report = json.loads(run.stdout)
        self.assertEqual(len(report['collection_errors']), 2)
        self.assertEqual(len(report['bundles']), 1)
        self.assertEqual(len(report['manifests']), 1)

    def test_external_symlinks_are_not_followed(self):
        outside = Path(self.temp.name) / 'Outside.app'
        self.write(outside / 'Info.plist', {'CFBundleIdentifier': 'DO_NOT_EMIT'})
        (self.app / 'Linked.app').symlink_to(outside, target_is_directory=True)
        (self.app / 'PrivacyInfo.xcprivacy').symlink_to(outside / 'Info.plist')
        run = self.cli()
        self.assertEqual(run.returncode, 1)
        report = json.loads(run.stdout)
        self.assertEqual(len(report['skipped_symlinks']), 2)
        self.assertEqual(len(report['bundles']), 1)
        self.assertNotIn('DO_NOT_EMIT', run.stdout)

    def test_malformed_date_preserves_other_evidence(self):
        broken = self.app / 'Info.plist'
        broken.write_bytes(b'<plist><dict><key>BuildDate</key>'
                           b'<date>invalid</date></dict></plist>')
        manifest = self.app / 'PrivacyInfo.xcprivacy'
        self.write(manifest, {'NSPrivacyTracking': False})
        before = broken.read_bytes()
        run = self.cli()
        self.assertEqual(run.returncode, 1, run.stderr)
        report = json.loads(run.stdout)
        self.assertEqual(len(report['collection_errors']), 1)
        self.assertEqual(report['collection_errors'][0]['path'],
                         'Products/Applications/Example.app/Info.plist')
        self.assertNotIn('fields', report['bundles'][0]['info'])
        self.assertEqual(report['bundles'][0]['info']['sha256'],
                         hashlib.sha256(before).hexdigest())
        self.assertEqual(report['manifests'][0]['fields'], {'NSPrivacyTracking': False})
        self.assertEqual(broken.read_bytes(), before)

    def test_deeply_nested_fields_preserve_partial_inventory(self):
        manifest = self.app / 'PrivacyInfo.xcprivacy'
        manifest.write_bytes(b'<plist><dict><key>NSPrivacyAccessedAPITypes</key>'
                             + b'<array>' * 2000 + b'<string>test</string>'
                             + b'</array>' * 2000 + b'</dict></plist>')
        run = self.cli()
        self.assertEqual(run.returncode, 1, run.stderr)
        report = json.loads(run.stdout)
        self.assertEqual(len(report['collection_errors']), 1)
        self.assertNotIn('fields', report['manifests'][0])
        self.assertEqual(report['bundles'][0]['info']['fields']['CFBundleVersion'], '42')
        self.assertEqual(report['archive_metadata']['fields']['ApplicationProperties']['CFBundleVersion'], '42')

    def test_direct_app_and_invalid_input(self):
        self.assertEqual(self.cli(self.app).returncode, 0)
        self.assertEqual(self.cli(Path(self.temp.name) / 'Missing.xcarchive').returncode, 2)
        self.assertEqual(self.cli(Path(self.temp.name)).returncode, 2)

    def test_non_dictionary_and_oversized_manifest(self):
        manifest = self.app / 'PrivacyInfo.xcprivacy'
        self.write(manifest, ['not', 'dictionary'])
        self.assertEqual(self.cli().returncode, 1)
        manifest.write_bytes(b'x' * (module.MAX_PLIST_BYTES + 1))
        run = self.cli()
        self.assertEqual(run.returncode, 1)
        self.assertIn('exceeds 4 MiB', run.stdout)

    def test_unsupported_selected_values_and_root_symlink(self):
        self.write(self.app / 'Info.plist', {'CFBundleIdentifier': b'not-a-string'})
        run = self.cli()
        self.assertEqual(run.returncode, 1)
        self.assertIn('non-JSON values', run.stdout)
        linked = Path(self.temp.name) / 'Linked.xcarchive'
        linked.symlink_to(self.root, target_is_directory=True)
        self.assertEqual(self.cli(linked).returncode, 2)

    def test_empty_archive_is_not_success(self):
        (self.app / 'Info.plist').unlink()
        self.app.rmdir()
        report = json.loads(self.cli().stdout)
        self.assertTrue(any('No app bundle' in e['reason'] for e in report['collection_errors']))


if __name__ == '__main__':
    unittest.main()
