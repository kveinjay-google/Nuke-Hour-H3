# Building Nuke Hour H3 for iOS

Use macOS, Xcode, CMake 3.21+ and Conan 2, with the Xcode generator. Clone recursively so the pinned dependency recipes and other submodules are available. Follow the retained [upstream guide](../developers/Building_iOS.md) for detailed platform configuration.

```sh
git clone --recurse-submodules https://github.com/kveinjay-google/Nuke-Hour-H3.git
cd Nuke-Hour-H3
conan profile detect
conan install . \
  --output-folder=conan-generated \
  --build=missing \
  --profile=dependencies/conan_profiles/ios-arm64 \
  --profile=dependencies/conan_profiles/base/apple-system \
  -s "&:build_type=Debug" \
  -c tools.build:jobs=4
cmake --preset ios-device-conan \
  -B out/build/ios-device-conan \
  -D CMAKE_TOOLCHAIN_FILE="$PWD/conan-generated/conan_toolchain.cmake" \
  -D APP_DISPLAY_NAME="Nuke Hour H3" \
  -D BUNDLE_IDENTIFIER_PREFIX=com.example.nukehour \
  -D CMAKE_XCODE_ATTRIBUTE_DEVELOPMENT_TEAM=YOUR_TEAM_ID
cmake --build out/build/ios-device-conan \
  --target vcmiclient --config Debug -- -jobs 4
```

Replace the example bundle prefix and signing team with your own values. Keep dependency and app build configurations consistent. If you restore an official VCMI iOS dependency cache, use the upstream instructions and `--build=never` where appropriate. Building missing dependencies can take substantially longer than building the launcher. Inspect resource pressure first and reduce job counts when other builds are active.

The active app icon catalog is `NukeHourAppIcon`; the launch storyboard is `NukeLaunchScreen`. The app uses the existing native VCMI importer. Supply owned Complete/SoD data through the app's folder picker; HD Edition data is optional after the base is present. No game files are fetched by these build instructions.

For Simulator builds, use the corresponding upstream dependency configuration and `iphonesimulator` SDK. Do not reuse device-only dependency binaries for a Simulator. The source-only publication does not contain the developer's local toolchains, signing profile, dependency caches, signed app or test-device identifiers.

## Source/package checks

```sh
python3 tools/check_community_package.py
# Optional, with fontTools installed in your Python environment:
python3 tools/check_cjk_fonts.py
```

The first check validates embedded resource paths, original artwork digests, opaque icon dimensions, active icon/startup settings and required licenses. The second verifies font provenance and selected glyph coverage; it is not a rendering or game-content test.

Before distributing an app binary, reconcile exact linked dependency licenses and corresponding-source/relinking obligations, including Qt, FFmpeg and scaling libraries, for the chosen distribution channel. This repository publishes sources and original community assets; it does not publish a signed binary release.
