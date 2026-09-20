#!/usr/bin/env python3
"""Adapt pinned VS2 vanilla ship-render section bounds to Minecraft 26.2.

Pinned 1.21.1 Level#getMaxSection() is an exclusive upper bound. Minecraft 26.2
Level#getMaxSectionY() is the inclusive maximum section Y. Preserve the exact upstream
ship-section coverage while changing only the section-height vocabulary:

    y = getMinSection(); y < getMaxSection()
becomes
    y = getMinSectionY(); y <= getMaxSectionY()

The LevelChunk section-array index remains relative to the minimum section, now using
getMinSectionY(). No ship visibility, transform, frustum, render-list, or camera authority
is changed by this overlay.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/vanilla_renderer/MixinLevelRendererVanilla.java"
if not path.is_file():
    raise SystemExit(f"fail-closed: expected transformed VS2 vanilla renderer source missing: {path}")

text = path.read_text(encoding="utf-8")
old_loop = "for (int y = level.getMinSection(); y < level.getMaxSection(); y++) {"
new_loop = "for (int y = level.getMinSectionY(); y <= level.getMaxSectionY(); y++) {"
old_index = "final LevelChunkSection section = levelChunk.getSection(y - level.getMinSection());"
new_index = "final LevelChunkSection section = levelChunk.getSection(y - level.getMinSectionY());"

# Require the exact already-proven vanilla renderer architecture before touching section bounds.
anchors = {
    "public void vs$addShipVisibleChunks(final Frustum frustum)": 1,
    "VSGameUtilsKt.getShipObjectWorld(level).getLoadedShips()": 1,
    "ShipRendererKt.getShipRenderer(shipObject) != ShipRenderer.VANILLA": 1,
    "shipObject.getActiveChunksSet().forEach((x, z) -> {": 1,
    "shipViewArea.vs$getShipRenderSection(x, y, z)": 1,
    "shipViewArea.vs$getOrCreateShipRenderSection(x, y, z)": 1,
    "shipObject.getRenderTransform().getShipToWorld()": 1,
    "visibleSections.add(renderChunk);": 1,
    "VSClientGameUtils.transformRenderWithShip(": 2,
}
for anchor, expected in anchors.items():
    count = text.count(anchor)
    if count != expected:
        raise SystemExit(
            f"fail-closed: preserved vanilla renderer authority anchor changed: {anchor!r} count={count} expected={expected}"
        )

if text.count(old_loop) != 1:
    raise SystemExit(f"fail-closed: expected one legacy vanilla-renderer section loop, found {text.count(old_loop)}")
if text.count(old_index) != 1:
    raise SystemExit(f"fail-closed: expected one legacy vanilla-renderer section index, found {text.count(old_index)}")
if text.count("level.getMinSection()") != 2 or text.count("level.getMaxSection()") != 1:
    raise SystemExit(
        "fail-closed: legacy vanilla-renderer section accessors changed outside the proven loop/index boundary"
    )
if "level.getMinSectionY()" in text or "level.getMaxSectionY()" in text:
    raise SystemExit("fail-closed: vanilla-renderer section-range adaptation already partially present")

new_text = text.replace(old_loop, new_loop, 1).replace(old_index, new_index, 1)

if old_loop in new_text or old_index in new_text:
    raise SystemExit("fail-closed: legacy vanilla-renderer section range remains after adaptation")
if "level.getMinSection()" in new_text or "level.getMaxSection()" in new_text:
    raise SystemExit("fail-closed: legacy vanilla-renderer section accessor remains after adaptation")
if new_text.count("level.getMinSectionY()") != 2 or new_text.count("level.getMaxSectionY()") != 1:
    raise SystemExit("fail-closed: 26.2 vanilla-renderer section accessors did not converge to 2 min / 1 max")
if new_text.count(new_loop) != 1 or new_text.count(new_index) != 1:
    raise SystemExit("fail-closed: 26.2 vanilla-renderer section loop/index did not converge exactly once")
for anchor, expected in anchors.items():
    count = new_text.count(anchor)
    if count != expected:
        raise SystemExit(
            f"fail-closed: vanilla renderer authority anchor changed after section adaptation: {anchor!r} count={count} expected={expected}"
        )

path.write_text(new_text, encoding="utf-8")
print("P1_LEVELRENDERER_VANILLA_SECTION_RANGE_26_2_OVERLAY_APPLIED loop=exclusive-to-inclusive min_sites=2 max_sites=1")
