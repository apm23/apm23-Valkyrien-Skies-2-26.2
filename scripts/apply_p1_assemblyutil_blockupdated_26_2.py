#!/usr/bin/env python3
"""Adapt only AssemblyUtil.updateBlock()'s removed Level.blockUpdated boundary to Minecraft 26.2.

Pinned upstream 1.21.1 calls Level.blockUpdated(BlockPos, Block) twice inside updateBlock().
For a normal ServerLevel that boundary forwards to neighbor notification while suppressing the
notification in debug worlds; client Level does not own the equivalent server neighbor-update
authority. Minecraft 26.2 no longer exposes the old blockUpdated call at this source boundary but
retains Level.isClientSide, Level.isDebug(), and updateNeighborsAt(BlockPos, Block).

This fail-closed overlay preserves the old runtime dispatch by forwarding those two exact sites to
updateNeighborsAt only for non-client, non-debug levels. It deliberately leaves sendBlockUpdated,
setBlocksDirty, neighbour-shape propagation, light checks, analog-output notification, assembly,
relocation, transforms, physics, networking, gameplay authority, and camera behavior unchanged.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
path = root / "common/src/main/kotlin/org/valkyrienskies/mod/common/assembly/AssemblyUtil.kt"
text = path.read_text(encoding="utf-8")

old_from = (
    "        level.setBlocksDirty(fromPos, toState, AIR)\n"
    "        level.sendBlockUpdated(fromPos, toState, AIR, flags)\n"
    "        level.blockUpdated(fromPos, AIR.block)\n"
    "        // This handles the update for neighboring blocks in worldspace\n"
)
new_from = (
    "        level.setBlocksDirty(fromPos, toState, AIR)\n"
    "        level.sendBlockUpdated(fromPos, toState, AIR, flags)\n"
    "        if (!level.isClientSide && !level.isDebug()) {\n"
    "            level.updateNeighborsAt(fromPos, AIR.block)\n"
    "        }\n"
    "        // This handles the update for neighboring blocks in worldspace\n"
)

old_to = (
    "        level.setBlocksDirty(toPos, AIR, toState)\n"
    "        level.sendBlockUpdated(toPos, AIR, toState, flags)\n"
    "        level.blockUpdated(toPos, toState.block)\n"
    "        if (!level.isClientSide && toState.hasAnalogOutputSignal()) {\n"
)
new_to = (
    "        level.setBlocksDirty(toPos, AIR, toState)\n"
    "        level.sendBlockUpdated(toPos, AIR, toState, flags)\n"
    "        if (!level.isClientSide && !level.isDebug()) {\n"
    "            level.updateNeighborsAt(toPos, toState.block)\n"
    "        }\n"
    "        if (!level.isClientSide && toState.hasAnalogOutputSignal()) {\n"
)

for label, old, new in (
    ("fromPos neighbor update", old_from, new_from),
    ("toPos neighbor update", old_to, new_to),
):
    count = text.count(old)
    if count != 1:
        raise SystemExit(
            f"expected exactly one pinned upstream AssemblyUtil {label} context in {path}, found {count}"
        )
    text = text.replace(old, new)

required_once = (
    "level.updateNeighborsAt(fromPos, AIR.block)",
    "level.updateNeighborsAt(toPos, toState.block)",
)
for needle in required_once:
    if text.count(needle) != 1:
        raise SystemExit(f"expected exactly one Minecraft 26.2 AssemblyUtil neighbor-update call {needle!r} in {path}")

server_debug_guard = "if (!level.isClientSide && !level.isDebug()) {"
if text.count(server_debug_guard) != 2:
    raise SystemExit(
        f"expected exactly two server/non-debug AssemblyUtil neighbor-update guards in {path}, found {text.count(server_debug_guard)}"
    )

if "level.blockUpdated(" in text:
    raise SystemExit(f"legacy AssemblyUtil level.blockUpdated call remains in {path}")

# Guard adjacent upstream update phases so this overlay cannot silently absorb them.
adjacent = (
    "level.sendBlockUpdated(fromPos, toState, AIR, flags)",
    "AIR.updateIndirectNeighbourShapes(level, fromPos, flags, recursionLeft - 1)",
    "AIR.updateNeighbourShapes(level, fromPos, flags, recursionLeft)",
    "level.chunkSource.lightEngine.checkBlock(fromPos)",
    "level.sendBlockUpdated(toPos, AIR, toState, flags)",
    "if (!level.isClientSide && toState.hasAnalogOutputSignal()) {",
    "level.updateNeighbourForOutputSignal(toPos, toState.block)",
    "level.chunkSource.lightEngine.checkBlock(toPos)",
)
for needle in adjacent:
    if text.count(needle) != 1:
        raise SystemExit(f"adjacent AssemblyUtil update phase changed unexpectedly in {path}: {needle}")

path.write_text(text, encoding="utf-8")
print("P1_ASSEMBLYUTIL_BLOCKUPDATED_26_2_OVERLAY_APPLIED")
