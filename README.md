# Hawkstore Publishing

[简体中文](README.zh-CN.md) · English

Author-facing packaging and validation tools for the Hawkstore ecosystem. This repository deliberately contains no repository-wide credential and does not let the desktop client push to the registry default branch.

## Package layout

```text
MyMod-1.2.0/
  manifest.json
  README.md
  CHANGELOG.md
  icon.png
  BepInEx/
    plugins/
      MyMod/
        MyMod.dll
        assets/
```

Required files are `manifest.json`, `README.md`, and at least one DLL below `BepInEx/plugins`.

## Create a package

```bash
python tools/package_mod.py path/to/MyMod-1.2.0 --out artifacts
```

The command validates the basic contract, builds a deterministic ZIP, and writes its SHA-256 beside it.

## Planned hosted workflow

1. Author signs in through a least-privilege GitHub App.
2. Author uploads a ZIP through Hawkstore.
3. A service validates the archive, manifest, DLL metadata, ownership, dependencies, and malware scan result.
4. The service creates a submission branch and registry pull request.
5. GitHub Actions repeats deterministic validation.
6. A first-time publisher receives manual review.
7. Merge creates an immutable Release asset and updates the registry index.

Personal access tokens must not be requested from authors or embedded in the client.
