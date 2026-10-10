import base64
"""Regression tests for vendored frontend integrity verification."""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parent / "verify-vendor-integrity.py"

spec = importlib.util.spec_from_file_location("vendor_integrity", SCRIPT)
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


class VendorIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)

        self.root = Path(self.temp.name)
        self.vendor = self.root / "frontend" / "vendor"
        self.vendor.mkdir(parents=True)

        self.bundle = self.vendor / "test.js"
        self.bundle.write_bytes(b"original bundle")

        import hashlib

        content = self.bundle.read_bytes()

        self.package = {
            "vendored_file": "frontend/vendor/test.js",
            "size": len(content),
            "sha256": "sha256-" + base64.b64encode(hashlib.sha256(content).digest()).decode("ascii"),
            "sha384": "sha384-" + base64.b64encode(hashlib.sha384(content).digest()).decode("ascii"),
        }

        self.manifest = self.vendor / "integrity.json"
        self.save_manifest()

    def save_manifest(self):
        self.manifest.write_text(
            json.dumps({"packages": {"test": self.package}}),
            encoding="utf-8",
        )

    def run_verifier(self):
        with patch.object(verifier, "ROOT", self.root):
            with patch.object(verifier, "MANIFEST", self.manifest):
                return verifier.verify()

    def test_valid_bundle(self):
        self.assertEqual(self.run_verifier(), 0)

    def test_modified_bundle(self):
        self.bundle.write_bytes(b"tampered bundle!")
        self.assertEqual(self.run_verifier(), 1)

    def test_wrong_size(self):
        self.package["size"] += 1
        self.save_manifest()
        self.assertEqual(self.run_verifier(), 1)

    def test_wrong_sha256(self):
        self.package["sha256"] = "sha256-" + "0" * 64
        self.save_manifest()
        self.assertEqual(self.run_verifier(), 1)

    def test_wrong_sha384(self):
        self.package["sha384"] = "sha384-" + "0" * 96
        self.save_manifest()
        self.assertEqual(self.run_verifier(), 1)

    def test_missing_bundle(self):
        self.bundle.unlink()
        self.assertEqual(self.run_verifier(), 1)

    def test_invalid_manifest(self):
        self.manifest.write_text("{invalid", encoding="utf-8")
        self.assertEqual(self.run_verifier(), 1)

    def test_path_outside_vendor(self):
        self.package["vendored_file"] = "../outside.js"
        self.save_manifest()
        self.assertEqual(self.run_verifier(), 1)


if __name__ == "__main__":
    unittest.main()
