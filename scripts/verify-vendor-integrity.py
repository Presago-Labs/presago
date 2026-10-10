#!/usr/bin/env python3
"""Verify vendored frontend bundles against integrity.json."""

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "frontend" / "vendor" / "integrity.json"


def verify():
    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        packages = manifest["packages"]

        if not isinstance(packages, dict) or not packages:
            raise ValueError("Manifest has no valid packages")

    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"FAIL: Invalid integrity manifest: {exc}")
        return 1

    failures = 0
    vendor_root = (ROOT / "frontend" / "vendor").resolve()

    for package, info in packages.items():
        try:
            relative = info["vendored_file"]
            if not isinstance(relative, str):
                raise ValueError("Invalid vendored_file")

            path = (ROOT / relative).resolve()

            if not path.is_relative_to(vendor_root):
                raise ValueError("Bundle path is outside vendor directory")

            if not path.is_file():
                raise FileNotFoundError(relative)

            content = path.read_bytes()

            if len(content) != info["size"]:
                raise ValueError(
                    f"Size mismatch: expected {info['size']}, "
                    f"got {len(content)}"
                )

            for algorithm in ("sha256", "sha384"):
                expected = info[algorithm]
                digest = hashlib.new(algorithm, content).hexdigest()

                if not isinstance(expected, str) or not re.fullmatch(
                    rf"{algorithm}-[0-9a-f]{{{len(digest)}}}",
                    expected,
                ):
                    raise ValueError(f"Invalid {algorithm} manifest value")

                if expected != f"{algorithm}-{digest}":
                    raise ValueError(f"{algorithm} mismatch")

            print(f"PASS: {package} ({relative})")

        except (OSError, ValueError, KeyError, TypeError) as exc:
            failures += 1
            print(f"FAIL: {package}: {exc}")

    if failures:
        print(f"Vendor integrity verification failed: {failures} package(s)")
        return 1

    print("All vendored frontend bundles verified successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(verify())
