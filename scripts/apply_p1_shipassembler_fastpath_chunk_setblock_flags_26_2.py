#!/usr/bin/env python3
"""Adapt only ShipAssembler's small-set fast-path direct LevelChunk writes to Minecraft 26.2 flags.

Pinned upstream VS2's <=8-block assembly fast path deliberately writes source AIR and destination
state directly through LevelChunk.setBlockState(BlockPos, BlockState, false) to bypass normal
Level neighbor/update machinery while source/destination chunks are stalled. The same direct
LevelChunk API boundary is already proven in this port to use an integer flag word on Minecraft
26.2; legacy false therefore maps to 0, preserving no moved-by-piston bit and no additional update
bits. This overlay is intentionally limited to the two fast-path calls and does not touch block
entity/component transfer, tryClear, ship allocation, structure processors, tickets, transforms,
physics, collision, networking, gameplay authority, or camera behavior.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
path = root / "common/src/main/kotlin/org/valkyrienskies/mod/common/assembly/ShipAssembler.kt"
text = path.read_text(encoding="utf-8")

old_source = (
    "                    val srcChunk = level.getChunkAt(srcPos)\n"
    "                    srcChunk.setBlockState(srcPos, Blocks.AIR.defaultBlockState(), false)\n"
)
new_source = (
    "                    val srcChunk = level.getChunkAt(srcPos)\n"
    "                    srcChunk.setBlockState(srcPos, Blocks.AIR.defaultBlockState(), 0)\n"
)

old_destination = (
    "                    val destChunk = level.getChunkAt(destPos)\n"
    "                    destChunk.setBlockState(destPos, state, false)\n"
)
new_destination = (
    "                    val destChunk = level.getChunkAt(destPos)\n"
    "                    destChunk.setBlockState(destPos, state, 0)\n"
)

for label, old, new in (
    ("source AIR fast-path write", old_source, new_source),
    ("destination state fast-path write", old_destination, new_destination),
):
    count = text.count(old)
    if count != 1:
        raise SystemExit(
            f"expected exactly one pinned upstream ShipAssembler {label} context in {path}, found {count}"
        )
    text = text.replace(old, new)

expected_new = (
    "srcChunk.setBlockState(srcPos, Blocks.AIR.defaultBlockState(), 0)",
    "destChunk.setBlockState(destPos, state, 0)",
)
for call in expected_new:
    if text.count(call) != 1:
        raise SystemExit(f"expected exactly one Minecraft 26.2 zero-flag ShipAssembler fast-path call {call!r} in {path}")

legacy = (
    "srcChunk.setBlockState(srcPos, Blocks.AIR.defaultBlockState(), false)",
    "destChunk.setBlockState(destPos, state, false)",
)
for call in legacy:
    if call in text:
        raise SystemExit(f"legacy boolean ShipAssembler fast-path LevelChunk.setBlockState call remains in {path}: {call}")

for invariant in (
    "// neighbor update machinery. Skip sendBlockUpdated since source chunks",
    "// Place at destination using chunk-level setBlockState directly.",
    "val removeFlags = Block.UPDATE_CLIENTS or Block.UPDATE_KNOWN_SHAPE or Block.UPDATE_SUPPRESS_DROPS or Block.UPDATE_MOVE_BY_PISTON",
):
    if text.count(invariant) != 1:
        raise SystemExit(f"expected pinned ShipAssembler fast-path invariant exactly once in {path}: {invariant!r}")

path.write_text(text, encoding="utf-8")
print("P1_SHIPASSEMBLER_FASTPATH_CHUNK_SETBLOCK_FLAGS_26_2_OVERLAY_APPLIED")
