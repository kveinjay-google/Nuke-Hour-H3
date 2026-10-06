#!/usr/bin/env python3
"""Read-only cmap and resource-overlay checks. This is NOT a runtime rendering test.

Requires fontTools. --font may be repeated to test the union of baseline fonts.
With no --font, checks the Phase 1 overlay and its recorded upstream hashes.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re

from fontTools import __version__ as fonttools_version
from fontTools.ttLib import TTFont

PROBES = ("英雄无敌 III", "新游戏", "载入游戏", "设置", "战役", "多人游戏", "简体中文")
SUPPLEMENTAL = "，。！？：；（）【】《》“”‘’、…—中文 ABC abc 0123456789\ufffd"


def read_json(path):
    # Repository config/fonts.json uses line comments; strict overlay JSON does not.
    return json.loads(re.sub(r"//[^\n]*", "", path.read_text(encoding="utf-8")))


def inspect_font(path, root):
    with TTFont(path, lazy=True) as font:
        cmap = font.getBestCmap() or {}
        # .notdef is a mapped-but-missing glyph, not useful coverage.
        codepoints = {cp for cp, glyph in cmap.items() if glyph != ".notdef"}
        record = {
            "path": str(path.relative_to(root)) if path.is_relative_to(root) else str(path),
            "bytes": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "sfnt_version": font.sfntVersion,
            "has_CFF": "CFF " in font,
            "has_fvar": "fvar" in font,
            "family": font["name"].getDebugName(1),
            "version": font["name"].getDebugName(5),
            "unicode_cmap_codepoints": len(codepoints),
        }
    return record, codepoints


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font", action="append", type=Path, default=[])
    parser.add_argument("--json", type=Path, help="Write a machine-readable evidence report")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    overlay = root / "Mods/vcmi-zh-cn-fonts"
    errors = []
    overlay_mode = not args.font
    paths = list(args.font)
    if overlay_mode:
        config = json.loads((overlay / "Content/config/fonts.json").read_text())
        builtin = read_json(root / "config/fonts.json")
        if config.get("bitmap") != builtin["bitmap"]:
            errors.append("Bitmap role order must match the original nine engine roles")
        if config.get("lowPriority") is not True:
            errors.append("CJK font must be a lowPriority fallback")
        if set(config.get("trueType", {})) != set(builtin["bitmap"]):
            errors.append("CJK fallback must cover all nine font roles")
        for role in builtin["bitmap"]:
            fallback = config.get("trueType", {}).get(role, {})
            original = builtin["trueType"][role]
            for key in ("size", "outline", "noShadow"):
                if fallback.get(key) != original.get(key):
                    errors.append(f"{role}: original {key} must be preserved")
            filename = fallback.get("file", "")
            if not filename or Path(filename).name != filename or not filename.lower().endswith(".ttf"):
                errors.append(f"{role}: expected direct Data/*.ttf resource (existing VCMI font type)")
            paths.append(overlay / "Content/Data" / filename)
        paths = sorted(set(paths))
    records, union = [], set()
    for path in paths:
        record, codepoints = inspect_font(path.resolve(), root)
        records.append(record)
        union.update(codepoints)
    if overlay_mode:
        provenance = json.loads((overlay / "PROVENANCE.json").read_text())
        expected = provenance["font"]
        if len(records) != 1 or records[0]["sha256"] != expected["sha256"]:
            errors.append("Font hash does not match pinned provenance")
        for record, path in zip(records, paths):
            data = path.read_bytes()
            blob_sha1 = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
            if blob_sha1 != expected["upstream_git_blob_sha1"]:
                errors.append("Font does not match the official upstream Git blob")
        if any(record["has_fvar"] for record in records):
            errors.append("Expected an upstream static font, not a variable font")
        license_path = overlay / "LICENSE.OFL.txt"
        if hashlib.sha256(license_path.read_bytes()).hexdigest() != provenance["license"]["sha256"]:
            errors.append("License hash does not match pinned provenance")
    probe_results = []
    for probe in PROBES:
        missing = sorted({char for char in probe if ord(char) not in union})
        probe_results.append({"text": probe, "status": "FAIL" if missing else "PASS", "missing": missing})
    supplemental_missing = sorted({char for char in SUPPLEMENTAL if ord(char) not in union})
    result = {
        "tool": "fontTools.ttLib.TTFont.getBestCmap", "fonttools_version": fonttools_version,
        "mode": "phase1_overlay" if overlay_mode else "explicit_font_union",
        "fonts": records, "required_probes": probe_results,
        "supplemental_probe": {"text": SUPPLEMENTAL, "missing": supplemental_missing},
        "overlay_errors": errors,
        "status": "PASS" if not errors and all(p["status"] == "PASS" for p in probe_results) else "FAIL",
        "runtime_rendering": "NOT_RUN",
        "limitations": "cmap coverage does not prove SDL3_ttf load, rasterization, shaping, wrapping, metrics, memory or iOS UI layout.",
    }
    output = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(output, encoding="utf-8")
    print(output, end="")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
