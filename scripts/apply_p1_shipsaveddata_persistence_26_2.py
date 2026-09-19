#!/usr/bin/env python3
"""Adapt only the real VS2 ShipSavedData persistence boundary to Minecraft 26.2.

Pinned upstream VS2 stores the ship pipeline in overworld SavedData using the old
SavedData.Factory + computeIfAbsent(factory, string-id) API and an overridden
save(CompoundTag, HolderLookup.Provider) method. Minecraft 26.2 moves SavedData
serialization into SavedDataType<T> + Codec<T>, with computeIfAbsent(type).

This fail-closed overlay preserves the real VS2 persistence authority and data
semantics: overworld data storage remains the single owner; the existing
vs_ship_data identity is namespaced for the current Identifier API; the same
three NBT payload keys and pipeline/legacy load fallback remain; serialization
still writes only the existing vs_pipeline byte array; loadingException remains
fatal at the same MinecraftServer initialization boundary. It does not change
ship lifecycle, allocation, transforms, physics, collision, entity dragging,
rendering, networking/gameplay authority, camera behavior, or Create integration.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
saved_path = root / "common/src/main/kotlin/org/valkyrienskies/mod/common/ShipSavedData.kt"
mixin_path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/server/MixinMinecraftServer.java"

saved = saved_path.read_text(encoding="utf-8")
mixin = mixin_path.read_text(encoding="utf-8")

# This overlay is intentionally sequenced after the already-frozen 26.2
# CompoundTag.getByteArray Optional adaptation. Refuse to operate on another
# serialization shape so that the prior proof cannot be silently bypassed.
for needle in (
    "compoundTag.getByteArray(QUERYABLE_SHIP_DATA_NBT_KEY).orElse(byteArrayOf())",
    "compoundTag.getByteArray(CHUNK_ALLOCATOR_NBT_KEY).orElse(byteArrayOf())",
    "compoundTag.getByteArray(PIPELINE_NBT_KEY).orElse(byteArrayOf())",
):
    if saved.count(needle) != 1:
        raise SystemExit(f"expected exactly one frozen ShipSavedData byte-array site: {needle}")

# Current Minecraft SavedData is codec-owned. Replace only the old persistence
# imports; the VS2 pipeline type and all payload logic remain untouched.
imports_old = """import net.minecraft.nbt.CompoundTag
import net.minecraft.core.HolderLookup
import net.minecraft.world.level.saveddata.SavedData
"""
imports_new = """import com.mojang.serialization.Codec
import net.minecraft.nbt.CompoundTag
import net.minecraft.resources.Identifier
import net.minecraft.util.datafix.DataFixTypes
import net.minecraft.world.level.saveddata.SavedData
import net.minecraft.world.level.saveddata.SavedDataType
"""
if saved.count(imports_old) != 1:
    raise SystemExit("unexpected ShipSavedData persistence imports; refusing broader rewrite")
saved = saved.replace(imports_old, imports_new)

# Define exactly one current persistence descriptor. The codec delegates decode
# to the existing real-VS2 load function and encode to the same pipeline-byte
# payload formerly emitted by SavedData.save(). DataFixTypes.LEVEL is preserved
# from the upstream Factory registration.
type_anchor = '        private const val PIPELINE_NBT_KEY = "vs_pipeline"\n'
type_insert = """        private const val PIPELINE_NBT_KEY = \"vs_pipeline\"

        @JvmField
        val CODEC: Codec<ShipSavedData> = CompoundTag.CODEC.xmap(::load, ShipSavedData::saveToTag)

        @JvmField
        val TYPE: SavedDataType<ShipSavedData> = SavedDataType(
            Identifier.fromNamespaceAndPath(ValkyrienSkiesMod.MOD_ID, SAVED_DATA_ID),
            ::createEmpty,
            CODEC,
            DataFixTypes.LEVEL
        )
"""
if saved.count(type_anchor) != 1:
    raise SystemExit("unexpected ShipSavedData payload-key declaration")
saved = saved.replace(type_anchor, type_insert)

save_old = """    override fun save(compoundTag: CompoundTag, provider: HolderLookup.Provider): CompoundTag {
        val logger = org.slf4j.LoggerFactory.getLogger(\"VS2\")
        val bytes = vsCore.serializePipeline(pipeline)
        logger.info(\" ShipSavedData.save(): pipeline bytes = {} KB\", bytes.size / 1024)
        compoundTag.putByteArray(PIPELINE_NBT_KEY, bytes)

        return compoundTag
    }
"""
save_new = """    private fun saveToTag(): CompoundTag {
        val compoundTag = CompoundTag()
        val logger = org.slf4j.LoggerFactory.getLogger(\"VS2\")
        val bytes = vsCore.serializePipeline(pipeline)
        logger.info(\" ShipSavedData.save(): pipeline bytes = {} KB\", bytes.size / 1024)
        compoundTag.putByteArray(PIPELINE_NBT_KEY, bytes)

        return compoundTag
    }
"""
if saved.count(save_old) != 1:
    raise SystemExit(f"expected exactly one legacy ShipSavedData save override, found {saved.count(save_old)}")
saved = saved.replace(save_old, save_new)

# MinecraftServer must acquire that same single persistence type from the same
# overworld storage used by upstream VS2. Do not introduce server-global or
# secondary storage authority.
for import_line in (
    "import net.minecraft.util.datafix.DataFixTypes;\n",
    "import net.minecraft.world.level.saveddata.SavedData;\n",
):
    if mixin.count(import_line) != 1:
        raise SystemExit(f"unexpected MixinMinecraftServer legacy persistence import: {import_line.strip()}")
    mixin = mixin.replace(import_line, "")

factory_old = """        final SavedData.Factory<ShipSavedData> factory =
            new SavedData.Factory<>(ShipSavedData.Companion::createEmpty, (tag, provider) -> ShipSavedData.load(tag),
                DataFixTypes.LEVEL);
        // Load ship data from the world storage
        final ShipSavedData shipSavedData = overworld().getDataStorage()
            .computeIfAbsent(factory, ShipSavedData.SAVED_DATA_ID);
"""
factory_new = """        // Load ship data from the same overworld persistence authority used by upstream VS2.
        final ShipSavedData shipSavedData = overworld().getDataStorage()
            .computeIfAbsent(ShipSavedData.TYPE);
"""
if mixin.count(factory_old) != 1:
    raise SystemExit(f"expected exactly one legacy ShipSavedData Factory registration, found {mixin.count(factory_old)}")
mixin = mixin.replace(factory_old, factory_new)

# Fail closed on accidental dual persistence or payload redesign.
for text, needle, label in (
    (saved, "HolderLookup", "legacy ShipSavedData HolderLookup persistence signature"),
    (saved, "override fun save(", "legacy ShipSavedData save override"),
    (mixin, "SavedData.Factory", "legacy MixinMinecraftServer SavedData.Factory"),
    (mixin, "computeIfAbsent(factory", "legacy factory/id computeIfAbsent"),
):
    if needle in text:
        raise SystemExit(f"{label} remains after adaptation")

if saved.count("val CODEC: Codec<ShipSavedData>") != 1 or saved.count("val TYPE: SavedDataType<ShipSavedData>") != 1:
    raise SystemExit("ShipSavedData current codec/type descriptor was not installed exactly once")
if saved.count("Identifier.fromNamespaceAndPath(ValkyrienSkiesMod.MOD_ID, SAVED_DATA_ID)") != 1:
    raise SystemExit("ShipSavedData current Identifier identity was not installed exactly once")
if saved.count("DataFixTypes.LEVEL") != 1:
    raise SystemExit("ShipSavedData must preserve the upstream LEVEL data-fix type")
if saved.count("compoundTag.putByteArray(PIPELINE_NBT_KEY, bytes)") != 1:
    raise SystemExit("ShipSavedData pipeline payload writer changed unexpectedly")
for key in ("queryable_ship_data", "chunk_allocator", "vs_pipeline"):
    if saved.count(f'\"{key}\"') != 1:
        raise SystemExit(f"ShipSavedData payload key changed unexpectedly: {key}")
if mixin.count("overworld().getDataStorage()") != 1:
    raise SystemExit("ShipSavedData must retain exactly one overworld storage acquisition")
if mixin.count("computeIfAbsent(ShipSavedData.TYPE)") != 1:
    raise SystemExit("MixinMinecraftServer current ShipSavedData registration was not installed exactly once")
if mixin.count("shipSavedData.getLoadingException()") != 1 or mixin.count("shipSavedData.getPipeline()") != 1:
    raise SystemExit("MixinMinecraftServer ShipSavedData fatal-load/pipeline handoff changed unexpectedly")

saved_path.write_text(saved, encoding="utf-8")
mixin_path.write_text(mixin, encoding="utf-8")
print("P1_SHIPSAVEDDATA_PERSISTENCE_26_2_OVERLAY_APPLIED")
