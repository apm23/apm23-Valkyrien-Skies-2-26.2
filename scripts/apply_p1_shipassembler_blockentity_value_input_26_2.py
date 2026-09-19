#!/usr/bin/env python3
"""Adapt only ShipAssembler block-entity CompoundTag -> ValueInput load boundaries for Minecraft 26.2.

Pinned upstream VS2 still serializes the fast-path source block entity with
saveWithFullMetadata(level.registryAccess()), which Minecraft 26.2 retains and which still returns a
CompoundTag.  Minecraft 26.2 changed BlockEntity.loadWithComponents to accept only ValueInput.

This fail-closed overlay therefore wraps exactly the three existing empty CompoundTag clear fallbacks
and the one existing fast-path destination restore tag with vanilla TagValueInput.create using the
same registry context.  It preserves the upstream save payload, x/y/z rewrite, clear/remove/place
ordering, StructureTemplate path, chunk-ticket behavior, ship lifecycle, transforms, physics,
networking and gameplay authority.  It is a Minecraft 26.2 serialization API shim only.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
path = root / "common/src/main/kotlin/org/valkyrienskies/mod/common/assembly/ShipAssembler.kt"
text = path.read_text(encoding="utf-8")

compound_import = "import net.minecraft.nbt.CompoundTag\n"
problem_import = "import net.minecraft.util.ProblemReporter\n"
input_import = "import net.minecraft.world.level.storage.TagValueInput\n"

if text.count(compound_import) != 1:
    raise SystemExit(
        f"expected exactly one ShipAssembler CompoundTag import in {path}, found {text.count(compound_import)}"
    )
if problem_import in text or input_import in text:
    raise SystemExit("ShipAssembler ValueInput imports already present; refusing non-exact reapplication")

empty_old = "it.loadWithComponents(CompoundTag(), level.registryAccess())"
empty_new = (
    "it.loadWithComponents("
    "TagValueInput.create(ProblemReporter.DISCARDING, level.registryAccess(), CompoundTag())"
    ")"
)
restore_old = "level.getBlockEntity(destPos)?.loadWithComponents(tag, level.registryAccess())"
restore_new = (
    "level.getBlockEntity(destPos)?.loadWithComponents("
    "TagValueInput.create(ProblemReporter.DISCARDING, level.registryAccess(), tag)"
    ")"
)

if text.count(empty_old) != 3:
    raise SystemExit(
        f"expected exactly 3 ShipAssembler empty-tag loadWithComponents sites, found {text.count(empty_old)}"
    )
if text.count(restore_old) != 1:
    raise SystemExit(
        f"expected exactly 1 ShipAssembler fast-path restore site, found {text.count(restore_old)}"
    )

# Guard the independently inspected upstream fast-path semantics.  Saving remains a CompoundTag
# convenience API in Minecraft 26.2; only the load boundary is adapted here.
if text.count("saveWithFullMetadata(level.registryAccess())") != 1:
    raise SystemExit("unexpected ShipAssembler saveWithFullMetadata shape; refusing broader migration")
for needle in (
    'tag.putInt("x", destPos.x)',
    'tag.putInt("y", destPos.y)',
    'tag.putInt("z", destPos.z)',
):
    if text.count(needle) != 1:
        raise SystemExit(f"unexpected ShipAssembler fast-path position rewrite shape: {needle}")

text = text.replace(compound_import, compound_import + problem_import + input_import)
text = text.replace(empty_old, empty_new)
text = text.replace(restore_old, restore_new)

for needle in (empty_old, restore_old):
    if needle in text:
        raise SystemExit(f"legacy ShipAssembler BlockEntity load signature remains: {needle}")

if text.count(problem_import) != 1 or text.count(input_import) != 1:
    raise SystemExit("ShipAssembler ValueInput imports were not installed exactly once")
if text.count(
    "TagValueInput.create(ProblemReporter.DISCARDING, level.registryAccess(), CompoundTag())"
) != 3:
    raise SystemExit("expected exactly 3 adapted ShipAssembler empty-tag ValueInput sites")
if text.count(
    "TagValueInput.create(ProblemReporter.DISCARDING, level.registryAccess(), tag)"
) != 1:
    raise SystemExit("expected exactly 1 adapted ShipAssembler fast-path restore ValueInput site")
if text.count("saveWithFullMetadata(level.registryAccess())") != 1:
    raise SystemExit("ShipAssembler saveWithFullMetadata changed unexpectedly")

path.write_text(text, encoding="utf-8")
print("P1_SHIPASSEMBLER_BLOCKENTITY_VALUE_INPUT_26_2_OVERLAY_APPLIED")
