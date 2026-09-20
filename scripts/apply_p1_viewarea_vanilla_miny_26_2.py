#!/usr/bin/env python3
"""Adapt only pinned VS2 ViewArea minimum build-height vocabulary to Minecraft 26.2.

Minecraft 26.2 exposes the same minimum block Y through Level#getMinY(). This overlay
changes exactly one ship RenderSection lookup coordinate expression and leaves dirty
scheduling, section construction, custom map/array ownership, and disposal untouched.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/vanilla_renderer/MixinViewAreaVanilla.java"
if not path.is_file():
    raise SystemExit(f"fail-closed: expected transformed VS2 ViewArea source missing: {path}")

text = path.read_text(encoding="utf-8")
old = "level.getMinBuildHeight()"
new = "level.getMinY()"

# Require both independently frozen ViewArea vocabulary units first.
if text.count("level.getMinSectionY()") != 3 or "level.getMinSection()" in text:
    raise SystemExit("fail-closed: frozen ViewArea section-index unit missing before minY adaptation")
if text.count("ChunkPos.pack(") != 5 or "ChunkPos.asLong(" in text:
    raise SystemExit("fail-closed: frozen ViewArea packed-key unit missing before minY adaptation")

anchors = {
    "private final Long2ObjectMap<SectionRenderDispatcher.RenderSection[]> vs$shipRenderChunks": 1,
    "renderChunksArray[yIndex].setDirty(important);": 1,
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
            f"fail-closed: preserved ViewArea lifecycle anchor changed: {anchor!r} count={count} expected={expected}"
        )

if text.count(old) != 1:
    raise SystemExit(f"fail-closed: expected exactly one legacy ViewArea minimum-height call, found {text.count(old)}")
if new in text:
    raise SystemExit("fail-closed: ViewArea minY adaptation already partially present")

new_text = text.replace(old, new, 1)
if old in new_text or new_text.count(new) != 1:
    raise SystemExit("fail-closed: ViewArea minY adaptation did not converge exactly once")
if new_text.count("level.getMinSectionY()") != 3 or new_text.count("ChunkPos.pack(") != 5:
    raise SystemExit("fail-closed: frozen ViewArea vocabulary units changed during minY adaptation")
for anchor, expected in anchors.items():
    count = new_text.count(anchor)
    if count != expected:
        raise SystemExit(
            f"fail-closed: ViewArea lifecycle anchor changed after minY adaptation: {anchor!r} count={count} expected={expected}"
        )

path.write_text(new_text, encoding="utf-8")
print("P1_VIEWAREA_VANILLA_MINY_26_2_OVERLAY_APPLIED sites=1")
