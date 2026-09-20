#!/usr/bin/env python3
"""Adapt only pinned VS2 ViewArea ship-section index origins to Minecraft 26.2.

Minecraft 26.2 exposes the minimum section coordinate as Level#getMinSectionY().
The three pinned ViewArea usages are array-index origins only; there is no max-bound loop
in this unit. Preserve all custom ship ViewArea storage, dirty scheduling, section creation,
unload, and buffer-disposal behavior for later independently evidenced adaptations.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/vanilla_renderer/MixinViewAreaVanilla.java"
if not path.is_file():
    raise SystemExit(f"fail-closed: expected pinned VS2 ViewArea source missing: {path}")

text = path.read_text(encoding="utf-8")
old = "level.getMinSection()"
new = "level.getMinSectionY()"

# Lock this unit to the exact current pinned ViewArea shape and leave every other known
# 26.2 frontier class untouched for separate proof.
anchors = {
    "private final Long2ObjectMap<SectionRenderDispatcher.RenderSection[]> vs$shipRenderChunks": 1,
    "private SectionRenderDispatcher vs$sectionRenderDispatcher;": 1,
    "private void preScheduleRebuild": 1,
    "renderChunksArray[yIndex].setDirty(important);": 1,
    "level.getMinBuildHeight()": 1,
    "ChunkPos.asLong(": 5,
    "vs$getShipRenderSection": 1,
    "vs$getOrCreateShipRenderSection": 1,
    "vs$sectionRenderDispatcher.new RenderSection(0, chunkX << 4, sectionY << 4, chunkZ << 4)": 1,
    "arr[yIndex].setDirty(true);": 1,
    ".releaseBuffers();": 2,
}
for anchor, expected in anchors.items():
    count = text.count(anchor)
    if count != expected:
        raise SystemExit(
            f"fail-closed: preserved ViewArea renderer/lifecycle anchor changed: {anchor!r} count={count} expected={expected}"
        )

if text.count(old) != 3:
    raise SystemExit(f"fail-closed: expected exactly three legacy ViewArea section-index origins, found {text.count(old)}")
if new in text:
    raise SystemExit("fail-closed: ViewArea section-index adaptation already partially present")

new_text = text.replace(old, new)

if old in new_text or new_text.count(new) != 3:
    raise SystemExit("fail-closed: ViewArea section-index adaptation did not converge exactly three times")
for anchor, expected in anchors.items():
    count = new_text.count(anchor)
    if count != expected:
        raise SystemExit(
            f"fail-closed: ViewArea renderer/lifecycle anchor changed after section-index adaptation: {anchor!r} count={count} expected={expected}"
        )

path.write_text(new_text, encoding="utf-8")
print("P1_VIEWAREA_VANILLA_SECTION_INDEX_26_2_OVERLAY_APPLIED min_section_sites=3")
