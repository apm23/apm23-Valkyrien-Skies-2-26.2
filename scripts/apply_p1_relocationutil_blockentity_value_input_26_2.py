#!/usr/bin/env python3
"""Adapt only RelocationUtil block-entity CompoundTag loads to Minecraft 26.2 ValueInput.

Pinned upstream VS2 keeps the original source block entity payload as a CompoundTag, loads an empty
CompoundTag into Clearable block entities before source removal so their contents/components are no
longer present there, then loads the saved full CompoundTag into the destination block entity after
relocation. Minecraft 26.2 retains BlockEntity.loadWithComponents(ValueInput), while the former
loadWithComponents(CompoundTag, HolderLookup.Provider) convenience boundary is gone.

This fail-closed overlay bridges only those two reads through vanilla TagValueInput with the exact
existing registry contexts. It preserves the saved full-metadata CompoundTag, coordinate rewrite,
Clearable handling, pending-loot clear, source block-entity removal, direct chunk writes, optional
update flow, destination lookup, component decoding, relocation ordering, lighting and neighbor
updates. It does not alter block-entity serialization output, loot semantics, tickets, ship lifecycle,
transforms, physics, collision, entity dragging, rendering, networking/gameplay authority, or camera.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
path = root / "common/src/main/kotlin/org/valkyrienskies/mod/util/RelocationUtil.kt"
text = path.read_text(encoding="utf-8")

old_import = "import net.minecraft.nbt.CompoundTag\n"
new_import = (
    "import net.minecraft.nbt.CompoundTag\n"
    "import net.minecraft.util.ProblemReporter\n"
    "import net.minecraft.world.level.storage.TagValueInput\n"
)
if text.count(old_import) != 1:
    raise SystemExit(
        f"expected exactly one pinned upstream CompoundTag import in {path}, found {text.count(old_import)}"
    )

old_clear = "            blockEntity.loadWithComponents(emptyTag, level.registryAccess())\n"
new_clear = (
    "            blockEntity.loadWithComponents(\n"
    "                TagValueInput.create(ProblemReporter.DISCARDING, level.registryAccess(), emptyTag)\n"
    "            )\n"
)
old_restore = "        be.loadWithComponents(it, toChunk.level.registryAccess())\n"
new_restore = (
    "        be.loadWithComponents(\n"
    "            TagValueInput.create(ProblemReporter.DISCARDING, toChunk.level.registryAccess(), it)\n"
    "        )\n"
)

for needle, label in ((old_clear, "Clearable empty-tag load"), (old_restore, "destination full-tag load")):
    count = text.count(needle)
    if count != 1:
        raise SystemExit(f"expected exactly one pinned upstream RelocationUtil {label} in {path}, found {count}")

# This overlay is intentionally ordered after the already-frozen RelocationUtil adapters.
frozen_guards = (
    "            it.setLootTable(null)\n",
    "    fromChunk.setBlockState(from, AIR, 0)\n",
    "    toChunk.setBlockState(to, state, 0)\n",
    "\t\tlevel.removeBlockEntity(from)\n",
    "    if (doUpdate) {\n        updateBlock(level, from, to, state)\n    }\n",
)
for needle in frozen_guards:
    if text.count(needle) != 1:
        raise SystemExit(f"expected frozen RelocationUtil context {needle!r} exactly once in {path}")

text = text.replace(old_import, new_import)
text = text.replace(old_clear, new_clear)
text = text.replace(old_restore, new_restore)

required = (
    "TagValueInput.create(ProblemReporter.DISCARDING, level.registryAccess(), emptyTag)",
    "TagValueInput.create(ProblemReporter.DISCARDING, toChunk.level.registryAccess(), it)",
)
for needle in required:
    if text.count(needle) != 1:
        raise SystemExit(f"expected exactly one Minecraft 26.2 RelocationUtil ValueInput bridge fragment {needle!r} in {path}")

legacy = (
    "blockEntity.loadWithComponents(emptyTag, level.registryAccess())",
    "be.loadWithComponents(it, toChunk.level.registryAccess())",
)
for needle in legacy:
    if needle in text:
        raise SystemExit(f"legacy RelocationUtil block-entity ValueInput fragment remains in {path}: {needle}")

# Preserve the upstream source->clear->loot-clear->remove->move->lookup->restore lifecycle.
ordered = (
    "val tag = it.saveWithFullMetadata(fromChunk.level.registryAccess())",
    "val emptyTag = CompoundTag()",
    "TagValueInput.create(ProblemReporter.DISCARDING, level.registryAccess(), emptyTag)",
    "it.setLootTable(null)",
    "level.removeBlockEntity(from)",
    "fromChunk.setBlockState(from, AIR, 0)",
    "toChunk.setBlockState(to, state, 0)",
    "val be = level.getBlockEntity(to)!!",
    "TagValueInput.create(ProblemReporter.DISCARDING, toChunk.level.registryAccess(), it)",
)
positions = [text.index(needle) for needle in ordered]
if positions != sorted(positions):
    raise SystemExit(f"RelocationUtil block-entity relocation ordering changed unexpectedly in {path}")

path.write_text(text, encoding="utf-8")
print("P1_RELOCATIONUTIL_BLOCKENTITY_VALUE_INPUT_26_2_OVERLAY_APPLIED")
