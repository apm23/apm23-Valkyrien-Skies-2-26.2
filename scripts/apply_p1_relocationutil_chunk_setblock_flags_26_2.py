#!/usr/bin/env python3
"""Adapt only RelocationUtil's two direct LevelChunk writes to Minecraft 26.2 flags.

Pinned upstream VS2 relocateBlock() writes source AIR and destination state directly through
LevelChunk.setBlockState(BlockPos, BlockState, false), then conditionally runs its own explicit
updateBlock() flow. In the legacy API that third argument is the moved/isMoving boolean.
Minecraft 26.2 uses an integer flag word at the same direct chunk-write boundary, so upstream
false maps to 0: no moved-by-piston bit and no additional direct-write flags.

This overlay is intentionally independent from the earlier AssemblyUtil proof. It matches the
complete relocation write/update context and changes only these two third arguments. It does not
touch block-entity ValueInput/ValueOutput migration, Clearable handling, loot tables, neighbor
notification, lighting, rotation, ship/reference-space logic, physics, networking, or authority.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
path = root / "common/src/main/kotlin/org/valkyrienskies/mod/util/RelocationUtil.kt"
text = path.read_text(encoding="utf-8")

old = (
    "    state = state.rotate(rotation)\n"
    "\n"
    "    fromChunk.setBlockState(from, AIR, false)\n"
    "    toChunk.setBlockState(to, state, false)\n"
    "\n"
    "    if (doUpdate) {\n"
    "        updateBlock(level, from, to, state)\n"
    "    }\n"
)
new = (
    "    state = state.rotate(rotation)\n"
    "\n"
    "    fromChunk.setBlockState(from, AIR, 0)\n"
    "    toChunk.setBlockState(to, state, 0)\n"
    "\n"
    "    if (doUpdate) {\n"
    "        updateBlock(level, from, to, state)\n"
    "    }\n"
)

count = text.count(old)
if count != 1:
    raise SystemExit(
        f"expected exactly one pinned upstream RelocationUtil direct-write/update context in {path}, found {count}"
    )
text = text.replace(old, new)

expected_new = (
    "fromChunk.setBlockState(from, AIR, 0)",
    "toChunk.setBlockState(to, state, 0)",
)
for call in expected_new:
    if text.count(call) != 1:
        raise SystemExit(f"expected exactly one Minecraft 26.2 zero-flag relocation write {call!r} in {path}")

legacy = (
    "fromChunk.setBlockState(from, AIR, false)",
    "toChunk.setBlockState(to, state, false)",
)
for call in legacy:
    if call in text:
        raise SystemExit(f"legacy boolean LevelChunk.setBlockState call remains in {path}: {call}")

# Guard the adjacent semantics this isolated overlay must not absorb or reorder.
required_unchanged = (
    "state = state.rotate(rotation)",
    "if (doUpdate) {\n        updateBlock(level, from, to, state)\n    }",
    "blockEntity.loadWithComponents(emptyTag, level.registryAccess())",
    "it.setLootTable(null, 0)",
    "be.loadWithComponents(it, toChunk.level.registryAccess())",
    "level.blockUpdated(fromPos, AIR.block)",
    "level.blockUpdated(toPos, toState.block)",
)
for marker in required_unchanged:
    if text.count(marker) != 1:
        raise SystemExit(f"expected unchanged RelocationUtil semantic marker exactly once in {path}: {marker!r}")

path.write_text(text, encoding="utf-8")
print("P1_RELOCATIONUTIL_CHUNK_SETBLOCK_FLAGS_26_2_OVERLAY_APPLIED")
