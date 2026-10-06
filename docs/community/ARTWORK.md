# Independently generated HD fantasy assets

The user approved the castle/bronze/navy concept and explicitly rejected extracting assets from its screenshot. Every production PNG in `launcher/artwork/hd-fantasy/` was separately generated from a text brief with the approved concept used only as a style reference. No atlas was split and no concept pixels were used. The model identifier is provider-managed and is not exposed by the built-in image-generation tool; no unverified model-version claim is made.

Common brief: original classic Heroes III inspired high-definition painted medieval game interface, warm top-left light, sapphire shadows, restrained aged bronze, readable silhouettes, no text/status bar/device/UI screenshot, one standalone part per generation. Icons and plates have real alpha transparency. Runtime text and all system time content remain live.

| Asset | Generation brief |
| --- | --- |
| castle-background | New full-bleed 3:2 castle/valley/mountain painting; blue-roof white-stone citadel on right, quiet shaded navy woodland at left; no UI. |
| navy-surface | Newly painted uniform dark sapphire velvet/leather tile; quiet grain, no frame, objects or text. Runtime opacity is 22% over navy. |
| primary-normal | One wide raised gold plaque with restrained griffin endcaps and sapphire enamel, empty center, top-left light. |
| primary-pressed | Separately generated same plaque geometry; recessed darker center, upper shadow and reflected lower highlight. |
| primary-active | Separately generated same plaque geometry; slightly brighter bronze relief and restrained warm edge light. |
| primary-disabled | Separately generated same plaque geometry; subdued desaturated gunmetal/brown, no glow. |
| secondary-normal | One wide dark sapphire inset plate with subtle cast metal bevel, empty center. |
| secondary-pressed | Separately generated same plate geometry; sunk enamel center and inset upper/left shadows. |
| secondary-active | Separately generated same plate geometry; richer sapphire and warm edge illumination. |
| secondary-disabled | Separately generated same plate geometry; desaturated dark blue-gray metal, low emphasis. |
| nav-game | Independently painted crossed steel swords with warm bronze hilts, transparent, no frame. |
| nav-mods | Independently painted oxblood leather spellbook with bronze clasp, transparent, no frame. |
| nav-settings | Independently painted bronze astronomical astrolabe with sapphire center, transparent, no frame. |
| nav-help | Independently painted scholar scroll with navy ribbon, transparent, no frame. |
| crest | Independently painted griffin relief on sapphire heraldic shield with bronze rim. |
| data-folio | Independently painted document/map folio stack with blue wax seal; no readable map words. |
| hd-crystal | Independently painted sapphire crystal on bronze sun-relief pedestal. |

`ARTWORK_MANIFEST.json` records unchanged source files, hashes and byte counts. Native rendering uses alpha bounds to ignore transparent padding and nine-slice sampling to preserve the endcaps; it does not create cropped or modified source images. No Heroes III/Ubisoft commercial resource was copied into these materials.

The active app icon is a separately generated square golden griffin bust with curved wings on sapphire. Thirteen scale-only opaque PNG derivatives cover the native icon slots. The old tall shield image is retained only as a concept. All community-generated artwork is provided under GPL-2.0-or-later. Noto font bytes retain OFL-1.1 and their own notices; upstream and bundled third-party assets retain their original licenses. The retained launcher screenshot is an unedited native Simulator capture, with original orientation metadata and no gameplay.

Earlier community-generated material tiles and drawn check/chevron glyphs remain in the Qt resource catalog and are included in the manifest under the same community artwork license.
