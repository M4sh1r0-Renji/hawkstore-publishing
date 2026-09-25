#!/usr/bin/env python3
"""Validate and package a Hawkstore mod directory without external dependencies."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path, PurePosixPath

ID_RE = re.compile(r"^[a-z0-9]+(?:[._-][a-z0-9]+)+$")
SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:[-+][0-9A-Za-z.-]+)?$")


def validate(source: Path) -> dict:
    manifest_path = source / "manifest.json"
    readme_path = source / "README.md"
    if not manifest_path.is_file():
        raise ValueError("manifest.json is required")
    if not readme_path.is_file():
        raise ValueError("README.md is required")
    with manifest_path.open("r", encoding="utf-8") as stream:
        manifest = json.load(stream)
    required = {"schemaVersion", "id", "name", "version", "author", "owners", "description", "categories", "game", "bepInEx", "plugin"}
    missing = required - manifest.keys()
    if missing:
        raise ValueError(f"manifest is missing: {', '.join(sorted(missing))}")
    if manifest["schemaVersion"] != 1:
        raise ValueError("only schemaVersion 1 is supported")
    if not ID_RE.fullmatch(manifest["id"]):
        raise ValueError("manifest id is invalid")
    if not SEMVER_RE.fullmatch(manifest["version"]):
        raise ValueError("manifest version must use semantic versioning")
    if not manifest["owners"]:
        raise ValueError("at least one owner is required")
    plugin = manifest["plugin"]
    install_directory = plugin.get("installDirectory", "")
    entry_dll = plugin.get("entryDll", "")
    if not install_directory or "/" in install_directory or "\\" in install_directory:
        raise ValueError("plugin.installDirectory must be a single path component")
    if not entry_dll.lower().endswith(".dll") or "/" in entry_dll or "\\" in entry_dll:
        raise ValueError("plugin.entryDll must be a DLL filename")
    plugin_root = source / "BepInEx" / "plugins"
    if not plugin_root.is_dir() or not any(plugin_root.rglob("*.dll")):
        raise ValueError("at least one DLL is required below BepInEx/plugins")
    expected_dll = plugin_root / install_directory / entry_dll
    if not expected_dll.is_file():
        raise ValueError(f"entry DLL is missing: {expected_dll.relative_to(source)}")
    return manifest


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def build(source: Path, output_dir: Path) -> Path:
    manifest = validate(source)
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f"{manifest['id']}-{manifest['version']}.zip"
    files = sorted(path for path in source.rglob("*") if path.is_file())
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            relative = PurePosixPath(path.relative_to(source).as_posix())
            if ".." in relative.parts:
                raise ValueError("unsafe relative path")
            info = zipfile.ZipInfo(str(relative), date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())
    digest = sha256(output)
    output.with_suffix(output.suffix + ".sha256").write_text(f"{digest}  {output.name}\n", encoding="utf-8")
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a validated Hawkstore package")
    parser.add_argument("source", type=Path)
    parser.add_argument("--out", type=Path, default=Path("artifacts"))
    args = parser.parse_args()
    try:
        output = build(args.source.resolve(), args.out.resolve())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"Created {output}")
    print(f"SHA-256 {sha256(output)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
