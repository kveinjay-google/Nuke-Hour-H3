# Community validation status

Baseline: VCMI `290525c5518e6fba43143d374d5262acb5c0f5ec`. Publication date: 2026-10-06. The community edition is experimental; the broader runtime status remains **PHASE1_PARTIAL / HD_IOS_ACCEPTANCE_BLOCKED**.

| Scope | Observed result |
| --- | --- |
| Device and Simulator builds | Passed on the local development setup; Xcode 26.6, SDK 26.5 |
| iPad Air 11-inch M4 installation and signature | Passed with the developer's local signing profile; signing material is not public |
| Tablet/phone launcher navigation | Bounded native Simulator checks passed; adaptive navigation, presets, scrolling, settings jumps and mod details |
| Native folder picker | Open/cancel and alternate import-method checks passed on a reversible owned Simulator fixture |
| New name and icon | Built metadata verified; new name and native rounded icon inspected on Simulator |
| Image-free startup | New compiled storyboard selected; bounded foreground launcher smoke passed |
| CJK font | Pinned OFL font hash and seven cmap probes passed; a font file is not translated game content |
| Actual Chinese gameplay | Pending; Qt labels do not establish SDL font activation or Chinese Complete/SoD text |
| Maps, town, hero, battle and save/load | Full controlled physical sequence pending |
| Official HD import and assets actually loaded on iOS | Pending |
| Five controlled physical HD/Standard A/B pairs | Pending |
| Physical performance, thermals and import storage peaks | Pending |

Track A requires owned Complete/SoD data. Track B requires that same base plus owned official HD Edition data. The latter is an optional enhancement, not an alternate base game.

Local tests used two compiler jobs per target, serialized native UI checks, an external timeout and a sampled Simulator-app thread ceiling. No new engine worker pools were introduced. These observations do not certify transient thread peaks, physical game performance or save compatibility. Screenshots in this repository show the native Qt launcher on Simulator and original generated art, not gameplay or HD A/B acceptance.

Raw command logs, local absolute paths, device identifiers, account/signing data, commercial test fixtures, screenshots of other apps and signed binaries remain outside this public source publication. Reproduce source checks using the [build guide](BUILD_IOS.md).
