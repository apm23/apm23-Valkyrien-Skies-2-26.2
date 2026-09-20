#!/usr/bin/env python3
"""Adapt the pinned VS2 ClientChunkCache section-range loop to Minecraft 26.2.

Minecraft 1.21.1 getMaxSection() is an exclusive upper bound, while Minecraft 26.2
getMaxSectionY() is the inclusive maximum section Y. Preserve the exact upstream loop
coverage by adapting:
    sy = getMinSection(); sy < getMaxSection()
to:
    sy = getMinSectionY(); sy <= getMaxSectionY()

This helper changes only that loop header. It deliberately leaves RenderSection.setDirty(boolean)
untouched because renderer-dirty propagation needs separate architecture-sensitive evidence.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/client/world/MixinClientChunkCache.java"
if not path.is_file():
    raise SystemExit(f"fail-closed: expected pinned VS2 MixinClientChunkCache source missing: {path}")

text = path.read_text(encoding="utf-8")

old_loop = "for (int sy = level.getMinSection(); sy < level.getMaxSection(); sy++) {"
new_loop = "for (int sy = level.getMinSectionY(); sy <= level.getMaxSectionY(); sy++) {"

if text.count(old_loop) != 1:
    raise SystemExit(f"fail-closed: expected one pinned legacy section-range loop, found {text.count(old_loop)}")
if new_loop in text:
    raise SystemExit("fail-closed: ClientChunkCache section-range loop already adapted")
if text.count("level.getMinSection()") != 1 or text.count("level.getMaxSection()") != 1:
    raise SystemExit("fail-closed: legacy section-range accessors changed outside the pinned loop")
if "level.getMinSectionY()" in text or "level.getMaxSectionY()" in text:
    raise SystemExit("fail-closed: section-range adaptation already partially present")

# Require the two previously proven ClientChunkCache units before this one.
if text.count("ChunkPos.pack(") != 6 or "ChunkPos.asLong(" in text:
    raise SystemExit("fail-closed: expected frozen six-site packed-key adaptation before section-range unit")
if text.count("final Map<Heightmap.Types, long[]> heightmaps,") != 1:
    raise SystemExit("fail-closed: expected frozen packet-heightmap parameter before section-range unit")
if text.count("replaceWithPacketData(buf, heightmaps, consumer);") != 2:
    raise SystemExit("fail-closed: expected two frozen packet-heightmap forwarding calls before section-range unit")

anchors = {
    "final IVSViewAreaMethods viewArea = (IVSViewAreaMethods)": 1,
    "for (int dx = -1; dx <= 1; dx++) {": 2,
    "for (int dz = -1; dz <= 1; dz++) {": 2,
    "viewArea.vs$getShipRenderSection(x + dx, sy, z + dz);": 1,
    "renderSection.setDirty(true);": 1,
    "relightChunk(worldChunk);": 1,
    "this.level.onChunkLoaded(pos);": 1,
}
for anchor, expected in anchors.items():
    count = text.count(anchor)
    if count != expected:
        raise SystemExit(f"fail-closed: preserved ClientChunkCache renderer/lifecycle anchor changed: {anchor!r} count={count} expected={expected}")

text = text.replace(old_loop, new_loop, 1)

if old_loop in text or text.count(new_loop) != 1:
    raise SystemExit("fail-closed: section-range loop adaptation did not converge exactly once")
if "level.getMinSection()" in text or "level.getMaxSection()" in text:
    raise SystemExit("fail-closed: legacy section-range accessor remains after adaptation")
if text.count("level.getMinSectionY()") != 1 or text.count("level.getMaxSectionY()") != 1:
    raise SystemExit("fail-closed: 26.2 section-range accessors did not converge exactly once")
if text.count("renderSection.setDirty(true);") != 1:
    raise SystemExit("fail-closed: renderer-dirty call changed unexpectedly")
for anchor, expected in anchors.items():
    count = text.count(anchor)
    if count != expected:
        raise SystemExit(f"fail-closed: ClientChunkCache renderer/lifecycle anchor changed after adaptation: {anchor!r} count={count} expected={expected}")

path.write_text(text, encoding="utf-8")
print("P1_CLIENTCHUNKCACHE_SECTION_RANGE_26_2_OVERLAY_APPLIED loop=exclusive-to-inclusive")
