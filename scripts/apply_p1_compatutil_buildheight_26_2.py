#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/kotlin/org/valkyrienskies/mod/common/CompatUtil.kt"
text = path.read_text(encoding="utf-8")

replacements = [
    (
        "BlockPos(x, level.minBuildHeight, z)",
        "BlockPos(x, level.getMinY(), z)",
    ),
    (
        "worldHeight.y >= level.maxBuildHeight",
        "worldHeight.y >= level.getMinY() + level.getHeight()",
    ),
    (
        "level.maxBuildHeight.toDouble()",
        "(level.getMinY() + level.getHeight()).toDouble()",
    ),
]

for old, new in replacements:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"expected exactly one pinned CompatUtil expression {old!r} in {path}, found {count}")
    text = text.replace(old, new, 1)

path.write_text(text, encoding="utf-8")
print("P1_COMPATUTIL_BUILDHEIGHT_26_2_OVERLAY_APPLIED")

# Transport-only canonical P1 retrigger for the separately chained ClientChunkCache renderer-dirty bridge.
# Retriggered after correcting only the pinned three-site vanilla-renderer guard count.
# Transport-only canonical P1 retrigger for the chained vanilla-renderer section-range proof.
# Transport-only canonical P1 retrigger for the chained ViewArea ship-section index proof.
# Retriggered after correcting only the pinned one-site ViewArea ship-section method guard.
# Transport-only canonical P1 retrigger for the chained ViewArea packed-key proof.
# Transport-only canonical P1 retrigger for the chained ViewArea minimum-height proof.
# Transport-only canonical P1 retrigger for the chained ViewArea RenderSection constructor proof.
# Retriggered after correcting only the missing pinned SectionPos import guard for the ViewArea constructor proof.
# Transport-only canonical P1 retrigger for the chained ViewArea RenderSection disposal proof.
# Transport-only canonical P1 retrigger for the chained OptiFine renderer section-range proof.
# Transport-only canonical P1 retrigger for the chained OptiFine renderer dirty-authority proof.
# Transport-only canonical P1 retrigger for the chained Immersive Portals chunk-tracking build-height proof.
