#!/usr/bin/env python3
"""Adapt only AssemblyUtil's direct LevelChunk block writes to Minecraft 26.2 flags.

Pinned upstream VS2 calls LevelChunk.setBlockState(BlockPos, BlockState, false) in exactly two
places: removeBlock() and copyBlock(). In the 1.21.1 API the third parameter is the boolean
isMoving/moved flag. Minecraft 26.2 replaces that direct chunk-write parameter with an integer
block-update flag word. Because upstream explicitly passes false, the behavior-preserving 26.2
value is 0: no moved-by-piston bit and no additional update bits. This overlay deliberately does
not change VS2's explicit updateBlock() notification flow, scheduled ticks, block-entity transfer,
assembly ordering, relocation, ship allocation, transforms, physics, networking, or authority.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
path = root / "common/src/main/kotlin/org/valkyrienskies/mod/common/assembly/AssemblyUtil.kt"
text = path.read_text(encoding="utf-8")

old_remove = (
    "    fun removeBlock(level: Level, pos: BlockPos) {\n"
    "        level.removeBlockEntity(pos)\n"
    "        level.getChunk(pos).setBlockState(pos, Blocks.AIR.defaultBlockState(), false)\n"
    "    }\n"
)
new_remove = (
    "    fun removeBlock(level: Level, pos: BlockPos) {\n"
    "        level.removeBlockEntity(pos)\n"
    "        level.getChunk(pos).setBlockState(pos, Blocks.AIR.defaultBlockState(), 0)\n"
    "    }\n"
)

old_copy_prefix = (
    "    fun copyBlock(level: Level, from: BlockPos, to: BlockPos) {\n"
    "        val state = level.getBlockState(from)\n"
    "        val blockentity = level.getBlockEntity(from)\n"
    "        level.getChunk(to).setBlockState(to, state, false)\n"
    "\n"
    "        // Transfer pending schedule-ticks\n"
)
new_copy_prefix = (
    "    fun copyBlock(level: Level, from: BlockPos, to: BlockPos) {\n"
    "        val state = level.getBlockState(from)\n"
    "        val blockentity = level.getBlockEntity(from)\n"
    "        level.getChunk(to).setBlockState(to, state, 0)\n"
    "\n"
    "        // Transfer pending schedule-ticks\n"
)

for label, old, new in (
    ("removeBlock", old_remove, new_remove),
    ("copyBlock", old_copy_prefix, new_copy_prefix),
):
    count = text.count(old)
    if count != 1:
        raise SystemExit(
            f"expected exactly one pinned upstream AssemblyUtil {label} chunk-write context in {path}, found {count}"
        )
    text = text.replace(old, new)

expected_new = (
    "level.getChunk(pos).setBlockState(pos, Blocks.AIR.defaultBlockState(), 0)",
    "level.getChunk(to).setBlockState(to, state, 0)",
)
for call in expected_new:
    if text.count(call) != 1:
        raise SystemExit(f"expected exactly one Minecraft 26.2 zero-flag chunk write {call!r} in {path}")

legacy = (
    "level.getChunk(pos).setBlockState(pos, Blocks.AIR.defaultBlockState(), false)",
    "level.getChunk(to).setBlockState(to, state, false)",
)
for call in legacy:
    if call in text:
        raise SystemExit(f"legacy boolean LevelChunk.setBlockState call remains in {path}: {call}")

path.write_text(text, encoding="utf-8")
print("P1_ASSEMBLYUTIL_CHUNK_SETBLOCK_FLAGS_26_2_OVERLAY_APPLIED")
