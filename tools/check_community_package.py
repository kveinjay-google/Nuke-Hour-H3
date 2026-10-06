#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
"""Validate portable community resource and license packaging without starting the engine."""
import hashlib
import json
from pathlib import Path
import plistlib
import struct
import xml.etree.ElementTree as ET


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "docs/community/ARTWORK_MANIFEST.json").read_text())
    for item in manifest["assets"]:
        path = (root / item["file"]).resolve()
        require(path.is_relative_to(root), "Artwork path escapes repository")
        data = path.read_bytes()
        require(hashlib.sha256(data).hexdigest() == item["sha256"], f"Artwork digest: {item['file']}")
        require(len(data) == item["bytes"], f"Artwork size: {item['file']}")
    resources = ET.parse(root / "launcher/resources.qrc")
    for item in resources.findall(".//file"):
        require((root / "launcher" / item.text).is_file(), f"Missing Qt resource: {item.text}")
    for path in (root / "launcher").rglob("*.ui"):
        ET.parse(path)
    ET.parse(root / "launcher/translation/chinese.ts")
    icon_dir = root / "clientapp/ios/Images.xcassets/NukeHourAppIcon.appiconset"
    icons = json.loads((icon_dir / "Contents.json").read_text())
    for item in icons["images"]:
        data = (icon_dir / item["filename"]).read_bytes()
        require(data[:8] == b"\x89PNG\r\n\x1a\n", "App icon must be PNG")
        expected = round(float(item["size"].split("x")[0]) * float(item["scale"][:-1]))
        require(struct.unpack(">II", data[16:24]) == (expected, expected), f"Icon dimensions: {item['filename']}")
        require(data[25] == 2, f"App icon must be opaque RGB: {item['filename']}")
        offset = 8
        while offset < len(data):
            length = struct.unpack(">I", data[offset:offset + 4])[0]
            require(data[offset + 4:offset + 8] != b"tRNS", "App icon has transparency")
            offset += 12 + length
    info = plistlib.loads((root / "clientapp/ios/Info.plist").read_bytes())
    require(info["CFBundleDisplayName"] == "$(APP_DISPLAY_NAME)", "iOS display name wiring")
    require(info["UILaunchStoryboardName"] == "NukeLaunchScreen", "Active launch storyboard")
    launch = ET.parse(root / "clientapp/ios/NukeLaunchScreen.storyboard")
    require(not launch.findall(".//imageView"), "Launch storyboard must contain no logo image")
    cmake = (root / "clientapp/CMakeLists.txt").read_text()
    require("XCODE_ATTRIBUTE_ASSETCATALOG_COMPILER_APPICON_NAME NukeHourAppIcon" in cmake, "Active app icon catalog")
    for name in ("license.txt", "AUTHORS.h", "Mods/vcmi-zh-cn-fonts/LICENSE.OFL.txt", "Mods/vcmi-zh-cn-fonts/NOTICE.md"):
        require((root / name).is_file(), f"Required notice missing: {name}")
    print(f"PASS: {len(manifest['assets'])} artwork hashes, {len(icons['images'])} icon slots, Qt resources, image-free startup and license notices")


if __name__ == "__main__":
    main()
