# Simplified Chinese font fallback

Install this entire directory as `Mods/vcmi-zh-cn-fonts` under a VCMI data root. Keep `mod.json`, `Content`, `LICENSE.OFL.txt`, `NOTICE.md` and `PROVENANCE.json` together. Enable **Simplified Chinese Fonts** in the launcher's mod manager and restart the client. Existing installs must enable the mod explicitly; a new engine preset contains only `vcmi` by default. If preparing a controlled test data root without the launcher, preserve its existing `config/modSettings.json` and append `vcmi-zh-cn-fonts` to `presets[activePreset].mods` (with `vcmi` present); do not replace the rest of the user's preset. This mod provides fonts, not translated text or proprietary Heroes III assets.

The ordinary non-Android CMake install copies the source `Mods` directory when a client or server is enabled. A Phase 1 iOS package must carry this folder in its actual VCMI data root or import it there; source inclusion alone does not establish that an app bundle or active preset uses it. Preserve notices in either layout.

`Content/config/fonts.json` supplies all nine bitmap role names in their original order and a `lowPriority: true` TrueType entry for each. The original `config/fonts.json` and the four bundled Latin TTFs remain unchanged. Existing `FontChain` selects the first font with the character, so Latin uses the original configured fonts and missing Chinese characters use this fallback. The original role sizes, outlines and TINY shadow setting are preserved. Existing `video.fontsType` bitmap/scalable/automatic behavior still applies; line height and ascent use the maximum across the entire chain and can change with this larger-coverage font.

This is one full, static Noto Sans CJK SC Regular 2.004 face (16,437,364 bytes). The `.ttf` resource name is a byte-identical alias for the upstream `.otf` file; its actual outlines are CFF, and it has no variable-font `fvar` table. See `NOTICE.md` and `PROVENANCE.json`. Bold Latin roles continue using original faces; fallback Han characters use Regular, without synthetic bold. Font sizes are baseline settings, not a claim of finished CJK layout tuning.

Reproduce the static check from the repository root:

```sh
python3 tools/check_cjk_fonts.py
```

Requires `fontTools`. A passing cmap test proves seven requested strings are covered by non-`.notdef` glyphs. It does not prove VCMI resource activation, SDL3_ttf decoding/rasterization, target iOS layout, wrapping, clipping, touch interaction or acceptable memory use. Those require separate runtime evidence in `docs/community/STATUS.md`.
