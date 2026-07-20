#!/usr/bin/env python3

"""Run upload-oriented static validation on a reconstructed WeChat project."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


RESERVED_DIR_RE = re.compile(r"^__.*__$")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--skip-js", action="store_true", help="skip node --check")
    parser.add_argument("--max-js-mb", type=float, default=16.0, help="skip syntax checks above this file size")
    args = parser.parse_args()

    root = args.root.resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")

    errors: list[str] = []
    warnings: list[str] = []

    reserved = [path for path in root.rglob("*") if path.is_dir() and RESERVED_DIR_RE.match(path.name)]
    errors.extend(f"reserved directory: {path.relative_to(root)}" for path in reserved)

    json_files = sorted(root.rglob("*.json"))
    for path in json_files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"invalid JSON {path.relative_to(root)}: {exc}")

    js_files = sorted(root.rglob("*.js"))
    checked_js = 0
    skipped_js = 0
    node = shutil.which("node")
    if args.skip_js:
        skipped_js = len(js_files)
    elif not node:
        warnings.append("Node.js not found; JavaScript syntax checks skipped")
        skipped_js = len(js_files)
    else:
        max_bytes = int(args.max_js_mb * 1024 * 1024)
        for path in js_files:
            if path.stat().st_size > max_bytes:
                warnings.append(f"large JavaScript skipped ({path.stat().st_size} bytes): {path.relative_to(root)}")
                skipped_js += 1
                continue
            result = subprocess.run([node, "--check", str(path)], capture_output=True, text=True)
            checked_js += 1
            if result.returncode:
                detail = (result.stderr or result.stdout).strip().replace("\n", " | ")
                errors.append(f"invalid JavaScript {path.relative_to(root)}: {detail}")

    project_configs = [root / "project.config.json", root / "project.private.config.json"]
    if not project_configs[0].exists():
        warnings.append("project.config.json is missing")

    if not ((root / "app.js").exists() or (root / "game.js").exists()):
        errors.append("no app.js or game.js at project root")
    if not ((root / "app.json").exists() or (root / "game.json").exists()):
        errors.append("no app.json or game.json at project root")

    print(f"Root: {root}")
    print(f"JSON: {len(json_files)} checked")
    print(f"JavaScript: {checked_js} checked, {skipped_js} skipped")
    for warning in warnings:
        print("WARN: " + warning)
    for error in errors:
        print("ERROR: " + error)
    print(f"Result: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

