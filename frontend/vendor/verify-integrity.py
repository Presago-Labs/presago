#!/usr/bin/env python3
"""Verify frontend/vendor/integrity.json against the vendored files.

Recomputes sha256/sha384 digests and byte sizes, and compares them
to the recorded values. Exits 0 on success, 1 on any mismatch.
"""

import base64
import binascii
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(HERE, "integrity.json")

ALGOS = {
    "sha256": hashlib.sha256,
    "sha384": hashlib.sha384,
}


def main() -> int:
    with open(MANIFEST) as f:
        data = json.load(f)

    failures = []
    for name, pkg in data.get("packages", {}).items():
        path = os.path.join(os.path.dirname(HERE), os.path.basename(pkg["vendored_file"]))
        # vendored_file is relative to repo root, e.g. frontend/vendor/stellar-sdk.js
        repo_root = os.path.dirname(os.path.dirname(HERE))
        path = os.path.join(repo_root, pkg["vendored_file"])

        if not os.path.exists(path):
            failures.append(f"{name}: file not found: {pkg['vendored_file']}")
            continue

        with open(path, "rb") as f:
            content = f.read()

        if len(content) != pkg.get("size"):
            failures.append(
                f"{name}: size mismatch: recorded {pkg.get('size')}, actual {len(content)}"
            )

        for algo, hasher in ALGOS.items():
            recorded = pkg.get(algo, "")
            prefix = f"{algo}-"
            if not recorded.startswith(prefix):
                failures.append(f"{name}: {algo} missing '{prefix}' prefix")
                continue
            b64 = recorded[len(prefix):]
            try:
                base64.b64decode(b64, validate=True)
            except binascii.Error:
                failures.append(f"{name}: {algo} payload is not valid base64")
                continue
            expected = prefix + base64.b64encode(hasher(content).digest()).decode("ascii")
            if recorded != expected:
                failures.append(f"{name}: {algo} digest mismatch")

    if failures:
        for msg in failures:
            print(f"FAIL: {msg}", file=sys.stderr)
        return 1

    print(f"OK: verified {len(data.get('packages', {}))} packages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
