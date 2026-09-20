#!/usr/bin/env python3
"""Adapt only StructureTemplateMixin block-entity saveWithId to Minecraft 26.2 ValueOutput.

Pinned upstream VS2 captures a block entity into the CompoundTag carried by
StructureTemplate.StructureBlockInfo via blockEntity.saveWithId(level.registryAccess()). Minecraft
26.2 keeps saveWithId semantics but requires a ValueOutput. This fail-closed overlay wraps the same
registry context in vanilla TagValueOutput, invokes the same block entity saveWithId operation, and
passes output.buildResult() to the same StructureBlockInfo constructor.

It does not change ICopyableBlock/onCopy, voxel iteration, block state/template authority,
addToLists/buildInfoList, palette construction, entity list clearing, ship lookup/copy behavior,
transforms, physics, collision, rendering, networking, or any runtime movement authority.
"""
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/feature/structure_template/StructureTemplateMixin.java"
text = path.read_text(encoding="utf-8")

old_import_anchor = "import net.minecraft.server.level.ServerLevel;\n"
new_import_anchor = (
    "import net.minecraft.server.level.ServerLevel;\n"
    "import net.minecraft.util.ProblemReporter;\n"
    "import net.minecraft.world.level.storage.TagValueOutput;\n"
)
if text.count(old_import_anchor) != 1:
    raise SystemExit(
        f"expected exactly one ServerLevel import anchor in {path}, found {text.count(old_import_anchor)}"
    )
if "import net.minecraft.util.ProblemReporter;" in text or "import net.minecraft.world.level.storage.TagValueOutput;" in text:
    raise SystemExit(f"StructureTemplate ValueOutput imports already present in {path}")

old = (
    "            } else if (blockEntity != null) {\n"
    "                blockInfo = new StructureTemplate.StructureBlockInfo(relativePos, blockState, blockEntity.saveWithId(level.registryAccess()));\n"
    "            } else {\n"
)
new = (
    "            } else if (blockEntity != null) {\n"
    "                TagValueOutput output = TagValueOutput.createWithContext(ProblemReporter.DISCARDING, level.registryAccess());\n"
    "                blockEntity.saveWithId(output);\n"
    "                blockInfo = new StructureTemplate.StructureBlockInfo(relativePos, blockState, output.buildResult());\n"
    "            } else {\n"
)
count = text.count(old)
if count != 1:
    raise SystemExit(
        f"expected exactly one pinned upstream StructureTemplate block-entity save branch in {path}, found {count}"
    )

# Freeze the surrounding real VS2 StructureTemplate semantics before changing the API vocabulary.
required_before = {
    "CompoundTag customTag = null;": 1,
    "((ICopyableBlock) block).onCopy((ServerLevel) level, currentWorldPos, blockState, blockEntity, shipsBeingCopied, centerPositions)": 1,
    "new StructureTemplate.StructureBlockInfo(relativePos, blockState, customTag)": 1,
    "addToLists(blockInfo, basicBlocks, blocksWithEntities, specialBlocks);": 1,
    "List<StructureTemplate.StructureBlockInfo> finalBlockList = buildInfoList(basicBlocks, blocksWithEntities, specialBlocks);": 1,
    "this.entityInfoList.clear();": 1,
    "this.palettes.clear();": 1,
    "this.palettes.add(PaletteInvoker.invokeInit(finalBlockList));": 1,
}
for needle, expected in required_before.items():
    actual = text.count(needle)
    if actual != expected:
        raise SystemExit(f"authority guard {needle!r} expected {expected} occurrence(s) in {path}, found {actual}")

text = text.replace(old_import_anchor, new_import_anchor)
text = text.replace(old, new)

required_after = {
    "import net.minecraft.nbt.CompoundTag;": 1,
    "import net.minecraft.util.ProblemReporter;": 1,
    "import net.minecraft.world.level.storage.TagValueOutput;": 1,
    "TagValueOutput.createWithContext(ProblemReporter.DISCARDING, level.registryAccess())": 1,
    "blockEntity.saveWithId(output);": 1,
    "new StructureTemplate.StructureBlockInfo(relativePos, blockState, output.buildResult())": 1,
}
for needle, expected in required_after.items():
    actual = text.count(needle)
    if actual != expected:
        raise SystemExit(f"ValueOutput bridge fragment {needle!r} expected {expected} occurrence(s) in {path}, found {actual}")

if "blockEntity.saveWithId(level.registryAccess())" in text:
    raise SystemExit(f"legacy StructureTemplate registryAccess saveWithId call remains in {path}")

for needle, expected in required_before.items():
    actual = text.count(needle)
    if actual != expected:
        raise SystemExit(f"authority guard changed after overlay: {needle!r} expected {expected}, found {actual}")

path.write_text(text, encoding="utf-8")
print("P1_STRUCTURE_TEMPLATE_VALUE_OUTPUT_26_2_OVERLAY_APPLIED")

# Transport-only chaining from a workflow-watched canonical helper. The semantic adaptation
# remains isolated in its own fail-closed helper and assumes the already-frozen hand overlay
# has run earlier in the canonical chain.
standing_helper = Path(__file__).with_name("apply_p1_clientlevel_standing_dimensions_26_2.py")
if not standing_helper.is_file():
    raise SystemExit(f"fail-closed: required ClientLevel standing-dimensions overlay helper missing: {standing_helper}")
subprocess.run([sys.executable, str(standing_helper), str(root)], check=True)
print("P1_CLIENTLEVEL_STANDING_DIMENSIONS_26_2_CHAINED")
