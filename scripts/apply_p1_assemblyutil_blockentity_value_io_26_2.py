#!/usr/bin/env python3
"""Adapt only AssemblyUtil.copyBlock() block-entity transfer to Minecraft 26.2 Value I/O.

Pinned upstream VS2 serializes the source block entity with saveWithId(registryAccess), keeps the
existing setBlockEntity/order, then loads the same CompoundTag into the destination block entity with
loadWithComponents(tag, registryAccess). Minecraft 26.2 retains saveWithId(ValueOutput) and
loadWithComponents(ValueInput), while the old CompoundTag convenience signatures are gone.

This fail-closed overlay bridges only that API boundary using vanilla TagValueOutput/TagValueInput
with the existing registry context. It preserves the upstream saveWithId payload (including id,
custom data and components), the same CompoundTag handoff, null guard, setBlockEntity call/order,
destination lookup, TODO, and loadWithComponents semantics. It does not alter scheduled ticks,
neighbor updates, assembly/relocation, ship allocation, transforms, physics, networking, gameplay
authority, or camera behavior.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
path = root / "common/src/main/kotlin/org/valkyrienskies/mod/common/assembly/AssemblyUtil.kt"
text = path.read_text(encoding="utf-8")

old_import = "import net.minecraft.nbt.CompoundTag\n"
new_import = (
    "import net.minecraft.util.ProblemReporter\n"
    "import net.minecraft.world.level.storage.TagValueInput\n"
    "import net.minecraft.world.level.storage.TagValueOutput\n"
)
if text.count(old_import) != 1:
    raise SystemExit(
        f"expected exactly one pinned upstream CompoundTag import in {path}, found {text.count(old_import)}"
    )

old = (
    "        // Transfer block-entity data\n"
    "        if (state.hasBlockEntity() && blockentity != null) {\n"
    "            val data: CompoundTag = blockentity.saveWithId(level.registryAccess())\n"
    "            level.setBlockEntity(blockentity)\n"
    "            val newBlockentity = level.getBlockEntity(to)\n"
    "            // TODO: Do we invoke LevelChunk.promotePendingBlockEntity()?\n"
    "            newBlockentity?.loadWithComponents(data, level.registryAccess())\n"
    "        }\n"
)
new = (
    "        // Transfer block-entity data\n"
    "        if (state.hasBlockEntity() && blockentity != null) {\n"
    "            val output = TagValueOutput.createWithContext(ProblemReporter.DISCARDING, level.registryAccess())\n"
    "            blockentity.saveWithId(output)\n"
    "            val data = output.buildResult()\n"
    "            level.setBlockEntity(blockentity)\n"
    "            val newBlockentity = level.getBlockEntity(to)\n"
    "            // TODO: Do we invoke LevelChunk.promotePendingBlockEntity()?\n"
    "            newBlockentity?.loadWithComponents(\n"
    "                TagValueInput.create(ProblemReporter.DISCARDING, level.registryAccess(), data)\n"
    "            )\n"
    "        }\n"
)

count = text.count(old)
if count != 1:
    raise SystemExit(
        f"expected exactly one pinned upstream AssemblyUtil block-entity transfer context in {path}, found {count}"
    )

text = text.replace(old_import, new_import)
text = text.replace(old, new)

required = (
    "TagValueOutput.createWithContext(ProblemReporter.DISCARDING, level.registryAccess())",
    "blockentity.saveWithId(output)",
    "val data = output.buildResult()",
    "TagValueInput.create(ProblemReporter.DISCARDING, level.registryAccess(), data)",
)
for needle in required:
    if text.count(needle) != 1:
        raise SystemExit(f"expected exactly one Minecraft 26.2 AssemblyUtil Value I/O bridge fragment {needle!r} in {path}")

legacy = (
    "val data: CompoundTag = blockentity.saveWithId(level.registryAccess())",
    "newBlockentity?.loadWithComponents(data, level.registryAccess())",
    "import net.minecraft.nbt.CompoundTag",
)
for needle in legacy:
    if needle in text:
        raise SystemExit(f"legacy AssemblyUtil block-entity Value I/O fragment remains in {path}: {needle}")

# Guard the upstream lifecycle/order around the adapted serialization boundary.
ordered = (
    "blockentity.saveWithId(output)",
    "val data = output.buildResult()",
    "level.setBlockEntity(blockentity)",
    "val newBlockentity = level.getBlockEntity(to)",
    "TagValueInput.create(ProblemReporter.DISCARDING, level.registryAccess(), data)",
)
positions = [text.index(needle) for needle in ordered]
if positions != sorted(positions):
    raise SystemExit(f"AssemblyUtil block-entity transfer ordering changed unexpectedly in {path}")

path.write_text(text, encoding="utf-8")
print("P1_ASSEMBLYUTIL_BLOCKENTITY_VALUE_IO_26_2_OVERLAY_APPLIED")
