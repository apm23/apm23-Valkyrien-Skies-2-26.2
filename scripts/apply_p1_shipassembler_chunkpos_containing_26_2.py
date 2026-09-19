#!/usr/bin/env python3
"""Adapt only ShipAssembler's BlockPos -> ChunkPos conversion to Minecraft 26.2.

Pinned upstream VS2 uses ChunkPos(blockPos) while collecting the distinct chunks that contain
an assembly block set. Minecraft 26.2 exposes ChunkPos.containing(BlockPos) for that same
conversion and no longer accepts BlockPos in the public ChunkPos constructor. This overlay
changes only that conversion helper. It does not change ship allocation, assembly ordering,
block movement, tickets, persistence, processors, transforms, physics, or gameplay authority.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
path = root / "common/src/main/kotlin/org/valkyrienskies/mod/common/assembly/ShipAssembler.kt"
text = path.read_text(encoding="utf-8")

old = (
    "    @JvmStatic\n"
    "    private fun getDistinctChunksFromBlockPosSet(blocks: Set<BlockPos>): Set<ChunkPos> {\n"
    "        val chunkSet = hashSetOf<ChunkPos>()\n"
    "        for (blockPos in blocks) {\n"
    "            val chunkPos = ChunkPos(blockPos)\n"
    "            chunkSet.add(chunkPos)\n"
    "        }\n"
    "        return chunkSet\n"
    "    }\n"
)
new = (
    "    @JvmStatic\n"
    "    private fun getDistinctChunksFromBlockPosSet(blocks: Set<BlockPos>): Set<ChunkPos> {\n"
    "        val chunkSet = hashSetOf<ChunkPos>()\n"
    "        for (blockPos in blocks) {\n"
    "            val chunkPos = ChunkPos.containing(blockPos)\n"
    "            chunkSet.add(chunkPos)\n"
    "        }\n"
    "        return chunkSet\n"
    "    }\n"
)

count = text.count(old)
if count != 1:
    raise SystemExit(
        f"expected exactly one pinned upstream ShipAssembler distinct-chunk helper in {path}, found {count}"
    )
text = text.replace(old, new)

if text.count("ChunkPos.containing(blockPos)") != 1:
    raise SystemExit(f"expected exactly one Minecraft 26.2 ChunkPos.containing call in {path}")
if "val chunkPos = ChunkPos(blockPos)" in text:
    raise SystemExit(f"legacy ShipAssembler ChunkPos(BlockPos) conversion remains in {path}")

path.write_text(text, encoding="utf-8")
print("P1_SHIPASSEMBLER_CHUNKPOS_CONTAINING_26_2_OVERLAY_APPLIED")
