#!/usr/bin/env python3
"""Adapt only RelocationUtil's pending loot-table clear call to Minecraft 26.2.

Pinned upstream VS2 clears a RandomizableContainerBlockEntity's pending loot table before removing
and relocating the block entity so the source container cannot generate/drop its deferred loot.
The legacy call uses setLootTable(null, 0). In current Minecraft the two-argument overload requires
a non-null ResourceKey, while the one-argument setLootTable(@Nullable ResourceKey<LootTable>) is
the API boundary that clears the pending loot-table key. Preserve that exact upstream intent by
changing only setLootTable(null, 0) to setLootTable(null).

This overlay deliberately does not alter contents, loot generation, seeds for a non-null table,
block-entity ValueInput/ValueOutput/component loading, relocation ordering, direct chunk writes,
neighbor updates, lighting, ship/reference-space logic, physics, networking, gameplay authority,
or camera behavior.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
path = root / "common/src/main/kotlin/org/valkyrienskies/mod/util/RelocationUtil.kt"
text = path.read_text(encoding="utf-8")

old = "            it.setLootTable(null, 0)\n"
new = "            it.setLootTable(null)\n"
count = text.count(old)
if count != 1:
    raise SystemExit(f"expected exactly one pinned RelocationUtil two-argument loot clear in {path}, found {count}")
text = text.replace(old, new)

if text.count(new) != 1:
    raise SystemExit(f"expected exactly one Minecraft 26.2 RelocationUtil nullable loot clear in {path}")
if "it.setLootTable(null, 0)" in text:
    raise SystemExit(f"legacy RelocationUtil two-argument null loot clear remains in {path}")

# Guard all adjacent, independently frozen or still-unmigrated semantics against accidental absorption.
required_unchanged = (
    "blockEntity.loadWithComponents(emptyTag, level.registryAccess())",
    "level.removeBlockEntity(from)",
    "fromChunk.setBlockState(from, AIR, 0)",
    "toChunk.setBlockState(to, state, 0)",
    "if (doUpdate) {\n        updateBlock(level, from, to, state)\n    }",
    "be.loadWithComponents(it, toChunk.level.registryAccess())",
    "level.updateNeighborsAt(fromPos, AIR.block)",
    "level.updateNeighborsAt(toPos, toState.block)",
    "level.chunkSource.lightEngine.checkBlock(fromPos)",
    "level.chunkSource.lightEngine.checkBlock(toPos)",
)
for marker in required_unchanged:
    if text.count(marker) != 1:
        raise SystemExit(f"expected unchanged RelocationUtil semantic marker exactly once in {path}: {marker!r}")

path.write_text(text, encoding="utf-8")
print("P1_RELOCATIONUTIL_LOOT_CLEAR_26_2_OVERLAY_APPLIED")
