#!/usr/bin/env python3
"""Adapt the pinned VS2 ClientChunkCache section-range accessors to Minecraft 26.2.

Minecraft 26.2 exposes LevelHeightAccessor section bounds as getMinSectionY()/getMaxSectionY().
This helper changes only the two accessor calls in the existing ship render-section invalidation loop.
It deliberately leaves RenderSection.setDirty(boolean) untouched because that renderer-dirty API needs
separate architecture-sensitive evidence.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/client/world/MixinClientChunkCache.java"
if not path.is_file():
    raise SystemExit(f"fail-closed: expected pinned VS2 MixinClientChunkCache source missing: {path}")

text = path.read_text(encoding="utf-8")

old_min = "level.getMinSection()"
old_max = "level.getMaxSection()"
new_min = "level.getMinSectionY()"
new_max = "level.getMaxSectionY()"

if text.count(old_min) != 1:
    raise SystemExit(f"fail-closed: expected one legacy getMinSection call, found {text.count(old_min)}")
if text.count(old_max) != 1:
    raise SystemExit(f"fail-closed: expected one legacy getMaxSection call, found {text.count(old_max)}")
if new_min in text or new_max in text:
    raise SystemExit("fail-closed: ClientChunkCache section-range adaptation already partially present")

# Require the two previously proven ClientChunkCache units before this one.
if text.count("ChunkPos.pack(") != 6 or "ChunkPos.asLong(" in text:
    raise SystemExit("fail-closed: expected frozen six-site packed-key adaptation before section-range unit")
if text.count("final Map<Heightmap.Types, long[]> heightmaps,") != 1:
    raise SystemExit("fail-closed: expected frozen packet-heightmap parameter before section-range unit")
if text.count("replaceWithPacketData(buf, heightmaps, consumer);") != 2:
    raise SystemExit("fail-closed: expected two frozen packet-heightmap forwarding calls before section-range unit")

anchors = {
    "if (ValkyrienCommonMixinConfigPlugin.getVSRenderer() != VSRenderer.SODIUM) {": 1,
    "final IVSViewAreaMethods viewArea = (IVSViewAreaMethods)": 1,
    "for (int dx = -1; dx <= 1; dx++) {": 1,
    "for (int dz = -1; dz <= 1; dz++) {": 1,
    "viewArea.vs$getShipRenderSection(x + dx, sy, z + dz);": 1,
    "renderSection.setDirty(true);": 1,
    "relightChunk(worldChunk);": 1,
    "this.level.onChunkLoaded(pos);": 1,
}
for anchor, expected in anchors.items():
    count = text.count(anchor)
    if count != expected:
        raise SystemExit(f"fail-closed: preserved ClientChunkCache renderer/lifecycle anchor changed: {anchor!r} count={count} expected={expected}")

text = text.replace(old_min, new_min, 1)
text = text.replace(old_max, new_max, 1)

if old_min in text or text.count(new_min) != 1:
    raise SystemExit("fail-closed: getMinSectionY adaptation did not converge exactly once")
if old_max in text or text.count(new_max) != 1:
    raise SystemExit("fail-closed: getMaxSectionY adaptation did not converge exactly once")
if text.count("renderSection.setDirty(true);") != 1:
    raise SystemExit("fail-closed: renderer-dirty call changed unexpectedly")
for anchor, expected in anchors.items():
    count = text.count(anchor)
    if count != expected:
        raise SystemExit(f"fail-closed: ClientChunkCache renderer/lifecycle anchor changed after adaptation: {anchor!r} count={count} expected={expected}")

path.write_text(text, encoding="utf-8")
print("P1_CLIENTCHUNKCACHE_SECTION_RANGE_26_2_OVERLAY_APPLIED calls=2")
