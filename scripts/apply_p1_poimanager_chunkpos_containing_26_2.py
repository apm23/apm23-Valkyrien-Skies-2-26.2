#!/usr/bin/env python3
"""Adapt only MixinPOIManager's BlockPos -> ChunkPos construction to Minecraft 26.2.

Pinned upstream VS2 centers the POI chunk search around the ChunkPos containing the supplied
BlockPos via the old ChunkPos(BlockPos) constructor. Minecraft 26.2 exposes
ChunkPos.containing(BlockPos) for the same coordinate conversion. This overlay changes only
that constructor vocabulary. It does not change the range radius, POI occupancy/filtering,
ship active-chunk bounds, world/ship transforms, AI behavior, or POI authority.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/feature/poi/MixinPOIManager.java"
text = path.read_text(encoding="utf-8")

old = "        Stream<ChunkPos> chunkRange = ChunkPos.rangeClosed(new ChunkPos(blockPos), j);\n"
new = "        Stream<ChunkPos> chunkRange = ChunkPos.rangeClosed(ChunkPos.containing(blockPos), j);\n"

count = text.count(old)
if count != 1:
    raise SystemExit(
        f"expected exactly one pinned upstream POI BlockPos ChunkPos construction in {path}, found {count}"
    )
text = text.replace(old, new)

if text.count(new) != 1:
    raise SystemExit(f"expected exactly one Minecraft 26.2 POI ChunkPos.containing call in {path}")
if "ChunkPos.rangeClosed(new ChunkPos(blockPos), j)" in text:
    raise SystemExit(f"legacy POI ChunkPos(BlockPos) construction remains in {path}")

# Preserve the existing semantic authorities around this mechanical conversion.
for anchor in (
    "int j = Math.floorDiv(i, 16) + 1;",
    "final AABB aABB = new AABB(blockPos).inflate((double) i + 1);",
    "VSGameUtilsKt.getShipObjectWorld(sLevel).getLoadedShips().getIntersecting(",
    "POIChunkSearcher.INSTANCE.shipChunkBounds(ship.getActiveChunksSet())",
    "this.getInChunk(predicate, chunkPos, occupancy)",
    "VSGameUtilsKt.toWorldCoordinates(valkyrienskies$sLevel",
):
    if text.count(anchor) != 1:
        raise SystemExit(f"expected preserved POI semantic anchor exactly once: {anchor!r}")

path.write_text(text, encoding="utf-8")
print("P1_POIMANAGER_CHUNKPOS_CONTAINING_26_2_OVERLAY_APPLIED")
