#!/usr/bin/env python3
"""Adapt only RelocationUtil.updateBlock()'s removed Level.blockUpdated boundary to Minecraft 26.2.

Pinned upstream VS2 calls Level.blockUpdated(BlockPos, Block) twice inside RelocationUtil.updateBlock().
At the pinned 1.21.1 baseline the server implementation of that legacy boundary is the neighbor-update
entrypoint; current Minecraft exposes that semantic boundary as updateNeighborsAt instead. Because
RelocationUtil's receiver remains typed as Level, preserve the old runtime dispatch explicitly: only
server-side, non-debug levels forward the two calls to updateNeighborsAt.

This fail-closed overlay is independently scoped to RelocationUtil. It assumes the already-proven
RelocationUtil direct LevelChunk writes have been adapted to integer zero flags and guards those calls.
It deliberately leaves block-entity ValueInput/ValueOutput/component loading, Clearable handling,
loot-table semantics, sendBlockUpdated/setBlocksDirty phases, neighbour-shape propagation, analog
output notification, lighting, rotation, relocation ordering, ship/reference-space logic, physics,
networking, gameplay authority, and camera behavior unchanged.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
path = root / "common/src/main/kotlin/org/valkyrienskies/mod/util/RelocationUtil.kt"
text = path.read_text(encoding="utf-8")

old_from = (
    "    level.setBlocksDirty(fromPos, toState, AIR)\n"
    "    level.sendBlockUpdated(fromPos, toState, AIR, flags)\n"
    "    level.blockUpdated(fromPos, AIR.block)\n"
    "    // This handles the update for neighboring blocks in worldspace\n"
)
new_from = (
    "    level.setBlocksDirty(fromPos, toState, AIR)\n"
    "    level.sendBlockUpdated(fromPos, toState, AIR, flags)\n"
    "    if (!level.isClientSide && !level.isDebug()) {\n"
    "        level.updateNeighborsAt(fromPos, AIR.block)\n"
    "    }\n"
    "    // This handles the update for neighboring blocks in worldspace\n"
)

old_to = (
    "    level.setBlocksDirty(toPos, AIR, toState)\n"
    "    level.sendBlockUpdated(toPos, AIR, toState, flags)\n"
    "    level.blockUpdated(toPos, toState.block)\n"
    "    if (!level.isClientSide && toState.hasAnalogOutputSignal()) {\n"
)
new_to = (
    "    level.setBlocksDirty(toPos, AIR, toState)\n"
    "    level.sendBlockUpdated(toPos, AIR, toState, flags)\n"
    "    if (!level.isClientSide && !level.isDebug()) {\n"
    "        level.updateNeighborsAt(toPos, toState.block)\n"
    "    }\n"
    "    if (!level.isClientSide && toState.hasAnalogOutputSignal()) {\n"
)

for label, old, new in (
    ("fromPos neighbor update", old_from, new_from),
    ("toPos neighbor update", old_to, new_to),
):
    count = text.count(old)
    if count != 1:
        raise SystemExit(
            f"expected exactly one pinned RelocationUtil {label} context in {path}, found {count}"
        )
    text = text.replace(old, new)

required_once = (
    "level.updateNeighborsAt(fromPos, AIR.block)",
    "level.updateNeighborsAt(toPos, toState.block)",
)
for needle in required_once:
    if text.count(needle) != 1:
        raise SystemExit(f"expected exactly one Minecraft 26.2 RelocationUtil neighbor-update call {needle!r} in {path}")

server_debug_guard = "if (!level.isClientSide && !level.isDebug()) {"
if text.count(server_debug_guard) != 2:
    raise SystemExit(
        f"expected exactly two server/non-debug RelocationUtil neighbor-update guards in {path}, found {text.count(server_debug_guard)}"
    )

if "level.blockUpdated(" in text:
    raise SystemExit(f"legacy RelocationUtil level.blockUpdated call remains in {path}")

# Guard the already-frozen direct chunk writes and all adjacent update phases so this overlay cannot absorb them.
required_unchanged = (
    "fromChunk.setBlockState(from, AIR, 0)",
    "toChunk.setBlockState(to, state, 0)",
    "if (doUpdate) {\n        updateBlock(level, from, to, state)\n    }",
    "blockEntity.loadWithComponents(emptyTag, level.registryAccess())",
    "it.setLootTable(null, 0)",
    "be.loadWithComponents(it, toChunk.level.registryAccess())",
    "level.sendBlockUpdated(fromPos, toState, AIR, flags)",
    "AIR.updateIndirectNeighbourShapes(level, fromPos, flags, recursionLeft - 1)",
    "AIR.updateNeighbourShapes(level, fromPos, flags, recursionLeft)",
    "level.chunkSource.lightEngine.checkBlock(fromPos)",
    "level.sendBlockUpdated(toPos, AIR, toState, flags)",
    "if (!level.isClientSide && toState.hasAnalogOutputSignal()) {",
    "level.updateNeighbourForOutputSignal(toPos, toState.block)",
    "level.chunkSource.lightEngine.checkBlock(toPos)",
)
for marker in required_unchanged:
    if text.count(marker) != 1:
        raise SystemExit(f"expected unchanged RelocationUtil semantic marker exactly once in {path}: {marker!r}")

path.write_text(text, encoding="utf-8")
print("P1_RELOCATIONUTIL_BLOCKUPDATED_26_2_OVERLAY_APPLIED")
