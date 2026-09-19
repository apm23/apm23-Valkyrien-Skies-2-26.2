#!/usr/bin/env python3
"""Adapt only ShipAssembler.ICopyableProcessor to Minecraft 26.2's StructureProcessor API.

Pinned upstream VS2 uses ICopyableProcessor only as a programmatically-created processor while
copying ship structures. Its behavior depends on the already-processed block's world position,
state, and NBT; it does not depend on the removed original/new block-info pair beyond those values.
Minecraft 26.2 changed StructureProcessor from an abstract class to an interface, changed
processBlock to receive templateRelativePos plus a single processedBlockInfo, and replaced
getType() with codec(). The 26.2 StructureTemplate call site constructs processedBlockInfo with
the transformed+offset world position before invoking processors, so processedBlockInfo.pos is
the direct semantic replacement for upstream newBPos here.

The processor remains runtime-only/non-datapack just like upstream's nullable getType(): the unit
codec is intentionally instance-bound and is not registered. This overlay does not touch ship
transforms, assembly allocation, block-entity/component transfer, tickets, physics, collision,
networking, gameplay authority, rendering, or camera behavior.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
path = root / "common/src/main/kotlin/org/valkyrienskies/mod/common/assembly/ShipAssembler.kt"
text = path.read_text(encoding="utf-8")

old_blockpos_import = "import net.minecraft.core.BlockPos\n"
new_blockpos_import = "import com.mojang.serialization.MapCodec\nimport net.minecraft.core.BlockPos\n"
if text.count(old_blockpos_import) != 1:
    raise SystemExit(f"expected exactly one BlockPos import in {path}")
if "import com.mojang.serialization.MapCodec\n" in text:
    raise SystemExit(f"MapCodec import already present in {path}; refusing to stack an unknown adaptation")
text = text.replace(old_blockpos_import, new_blockpos_import, 1)

old_type_import = "import net.minecraft.world.level.levelgen.structure.templatesystem.StructureProcessorType\n"
if text.count(old_type_import) != 1:
    raise SystemExit(f"expected exactly one legacy StructureProcessorType import in {path}")
text = text.replace(old_type_import, "", 1)

old_decl = "    ): StructureProcessor() {\n"
new_decl = "    ): StructureProcessor {\n"
if text.count(old_decl) != 1:
    raise SystemExit(f"expected exactly one legacy ICopyableProcessor StructureProcessor superclass form in {path}")
text = text.replace(old_decl, new_decl, 1)

old_method = """        override fun processBlock(
            levelReader: LevelReader, oldBPos: BlockPos, newBPos: BlockPos,
            oldStructureBlockInfo: StructureTemplate.StructureBlockInfo,
            newStructureBlockInfo: StructureTemplate.StructureBlockInfo, structurePlaceSettings: StructurePlaceSettings
        ): StructureTemplate.StructureBlockInfo? {
            val block = newStructureBlockInfo.state.block
            if (block !is ICopyableBlock) return newStructureBlockInfo
            block.onPaste((levelReader as ServerLevelAccessor).level, newBPos, newStructureBlockInfo.state, oldShipIdToNewShipId, centerPositions, newStructureBlockInfo.nbt)
            return newStructureBlockInfo
        }

        // getType is used for referencing this processor from a datapack, which we don't need
        override fun getType(): StructureProcessorType<*>? = null
"""
new_method = """        override fun processBlock(
            levelReader: LevelReader, targetPosition: BlockPos, referencePos: BlockPos,
            templateRelativePos: BlockPos,
            processedBlockInfo: StructureTemplate.StructureBlockInfo, structurePlaceSettings: StructurePlaceSettings
        ): StructureTemplate.StructureBlockInfo? {
            val block = processedBlockInfo.state.block
            if (block !is ICopyableBlock) return processedBlockInfo
            block.onPaste((levelReader as ServerLevelAccessor).level, processedBlockInfo.pos, processedBlockInfo.state, oldShipIdToNewShipId, centerPositions, processedBlockInfo.nbt)
            return processedBlockInfo
        }

        // Upstream intentionally does not expose this runtime-only processor to datapacks.
        // 26.2 requires a codec() implementation; keep it instance-bound and unregistered.
        override fun codec(): MapCodec<out StructureProcessor> = MapCodec.unit(this)
"""
if text.count(old_method) != 1:
    raise SystemExit(f"expected exactly one pinned upstream ICopyableProcessor method block in {path}")
text = text.replace(old_method, new_method, 1)

for invariant in (
    "val oldShipIdToNewShipId: Map<ShipId, ShipId>",
    "val centerPositions: Map<Long, Pair<Vector3d, Vector3d>>",
    "block.onPaste((levelReader as ServerLevelAccessor).level, processedBlockInfo.pos, processedBlockInfo.state, oldShipIdToNewShipId, centerPositions, processedBlockInfo.nbt)",
    "override fun codec(): MapCodec<out StructureProcessor> = MapCodec.unit(this)",
):
    if text.count(invariant) != 1:
        raise SystemExit(f"expected adapted ICopyableProcessor invariant exactly once in {path}: {invariant!r}")

for legacy in (
    "StructureProcessorType<*>",
    "): StructureProcessor() {",
    "oldStructureBlockInfo: StructureTemplate.StructureBlockInfo",
    "newStructureBlockInfo: StructureTemplate.StructureBlockInfo",
):
    if legacy in text:
        raise SystemExit(f"legacy ICopyableProcessor StructureProcessor API remains in {path}: {legacy!r}")

path.write_text(text, encoding="utf-8")
print("P1_SHIPASSEMBLER_STRUCTURE_PROCESSOR_26_2_OVERLAY_APPLIED")
