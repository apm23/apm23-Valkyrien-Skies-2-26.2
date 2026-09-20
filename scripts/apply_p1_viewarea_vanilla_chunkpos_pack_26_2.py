#!/usr/bin/env python3
"""Adapt only pinned VS2 ViewArea ship-chunk packed-key vocabulary to Minecraft 26.2.

Minecraft 26.2 exposes the same x/z packed chunk key through ChunkPos.pack(int,int).
This overlay renames exactly the five pinned ViewArea map-key calls from ChunkPos.asLong
without changing arguments, map ownership, renderer lifecycle, dirty scheduling, section
construction, or buffer disposal.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/vanilla_renderer/MixinViewAreaVanilla.java"
if not path.is_file():
    raise SystemExit(f"fail-closed: expected transformed VS2 ViewArea source missing: {path}")

text = path.read_text(encoding="utf-8")
old = "ChunkPos.asLong("
new = "ChunkPos.pack("

# Require the independently frozen three-site section-index unit first.
if text.count("level.getMinSectionY()") != 3 or "level.getMinSection()" in text:
    raise SystemExit("fail-closed: frozen ViewArea section-index unit missing before packed-key adaptation")

# Lock every remaining lifecycle-sensitive frontier while changing only the packed-key API name.
anchors = {
    "private final Long2ObjectMap<SectionRenderDispatcher.RenderSection[]> vs$shipRenderChunks": 1,
    "private SectionRenderDispatcher vs$sectionRenderDispatcher;": 1,
    "renderChunksArray[yIndex].setDirty(important);": 1,
    "level.getMinBuildHeight()": 1,
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

if text.count(old) != 5:
    raise SystemExit(f"fail-closed: expected exactly five legacy ViewArea packed-key calls, found {text.count(old)}")
if new in text:
    raise SystemExit("fail-closed: ViewArea packed-key adaptation already partially present")

new_text = text.replace(old, new)

if old in new_text or new_text.count(new) != 5:
    raise SystemExit("fail-closed: ViewArea packed-key adaptation did not converge exactly five times")
if new_text.count("level.getMinSectionY()") != 3:
    raise SystemExit("fail-closed: frozen ViewArea section-index unit changed during packed-key adaptation")
for anchor, expected in anchors.items():
    count = new_text.count(anchor)
    if count != expected:
        raise SystemExit(
            f"fail-closed: ViewArea renderer/lifecycle anchor changed after packed-key adaptation: {anchor!r} count={count} expected={expected}"
        )

path.write_text(new_text, encoding="utf-8")
print("P1_VIEWAREA_VANILLA_CHUNKPOS_PACK_26_2_OVERLAY_APPLIED sites=5")
