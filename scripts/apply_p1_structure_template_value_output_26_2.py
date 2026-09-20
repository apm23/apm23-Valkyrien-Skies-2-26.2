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

# Transport-only chaining from a workflow-watched canonical helper. Each semantic unit
# remains isolated in its own fail-closed helper. The canonical chain has already applied
# the frozen ClientLevel hand adaptation before these calls.
standing_helper = Path(__file__).with_name("apply_p1_clientlevel_standing_dimensions_26_2.py")
if not standing_helper.is_file():
    raise SystemExit(f"fail-closed: required ClientLevel standing-dimensions overlay helper missing: {standing_helper}")
subprocess.run([sys.executable, str(standing_helper), str(root)], check=True)
print("P1_CLIENTLEVEL_STANDING_DIMENSIONS_26_2_CHAINED")

packet_create_helper = Path(__file__).with_name("apply_p1_clientpacketlistener_entity_create_26_2.py")
if not packet_create_helper.is_file():
    raise SystemExit(f"fail-closed: required ClientPacketListener entity-create overlay helper missing: {packet_create_helper}")
subprocess.run([sys.executable, str(packet_create_helper), str(root)], check=True)
print("P1_CLIENTPACKETLISTENER_ENTITY_CREATE_26_2_CHAINED")

packet_snap_helper = Path(__file__).with_name("apply_p1_clientpacketlistener_entity_snap_26_2.py")
if not packet_snap_helper.is_file():
    raise SystemExit(f"fail-closed: required ClientPacketListener entity-snap overlay helper missing: {packet_snap_helper}")
subprocess.run([sys.executable, str(packet_snap_helper), str(root)], check=True)
print("P1_CLIENTPACKETLISTENER_ENTITY_SNAP_26_2_CHAINED")

levelchunk_mark_unsaved_helper = Path(__file__).with_name("apply_p1_levelchunk_mark_unsaved_26_2.py")
if not levelchunk_mark_unsaved_helper.is_file():
    raise SystemExit(f"fail-closed: required LevelChunk mark-unsaved overlay helper missing: {levelchunk_mark_unsaved_helper}")
subprocess.run([sys.executable, str(levelchunk_mark_unsaved_helper), str(root)], check=True)
print("P1_LEVELCHUNK_MARK_UNSAVED_26_2_CHAINED_V2")

levelchunk_empty_sections_helper = Path(__file__).with_name("apply_p1_levelchunk_empty_sections_26_2.py")
if not levelchunk_empty_sections_helper.is_file():
    raise SystemExit(f"fail-closed: required LevelChunk empty-sections overlay helper missing: {levelchunk_empty_sections_helper}")
subprocess.run([sys.executable, str(levelchunk_empty_sections_helper), str(root)], check=True)
print("P1_LEVELCHUNK_EMPTY_SECTIONS_26_2_CHAINED")

levelchunk_parse_factory_helper = Path(__file__).with_name("apply_p1_levelchunk_serializable_parse_factory_26_2.py")
if not levelchunk_parse_factory_helper.is_file():
    raise SystemExit(f"fail-closed: required LevelChunk SerializableChunkData.parse factory helper missing: {levelchunk_parse_factory_helper}")
subprocess.run([sys.executable, str(levelchunk_parse_factory_helper), str(root)], check=True)
print("P1_LEVELCHUNK_SERIALIZABLE_PARSE_FACTORY_26_2_CHAINED")
