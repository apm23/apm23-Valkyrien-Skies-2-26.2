#!/usr/bin/env python3
"""Adapt only MixinLevelChunk SerializableChunkData.parse context to Minecraft 26.2.

The canonical P1 overlay chain has already migrated pinned VS2 chunk serialization to
SerializableChunkData. Minecraft 26.2 requires SerializableChunkData.parse's second argument to
be a PalettedContainerFactory rather than the legacy RegistryAccess context. Level exposes the
matching palettedContainerFactory() used for current chunk palette construction.

This fail-closed overlay changes only that one parse argument. It preserves the serialized tag,
read parameters, section copying/filling, tick containers, heightmaps, light state, dirty marking,
final blending-data ownership, and all real VS2 ship lifecycle/reference-space authority.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/world/chunk/MixinLevelChunk.java"
if not path.is_file():
    raise SystemExit(f"fail-closed: expected pinned VS2 MixinLevelChunk source missing: {path}")

text = path.read_text(encoding="utf-8")

old = "SerializableChunkData.parse((ServerLevel) level, level.registryAccess(), compoundTag)"
new = "SerializableChunkData.parse((ServerLevel) level, level.palettedContainerFactory(), compoundTag)"

if text.count(old) != 1:
    raise SystemExit(
        f"fail-closed: expected exactly one legacy SerializableChunkData.parse registry context, found {text.count(old)}"
    )
if text.count(new) != 0:
    raise SystemExit("fail-closed: LevelChunk SerializableChunkData.parse factory adaptation already present")

preserved = {
    "public void copyChunkFromOtherDimension(@NotNull final VSLevelChunk srcChunkVS) {": 1,
    "final CompoundTag compoundTag = SerializableChunkData.copyOf((ServerLevel) srcChunk.getLevel(), srcChunk).write();": 1,
    "final RegionStorageInfo dummyInfo = new RegionStorageInfo(\"dummy\", level.dimension(), \"dummy\");": 1,
    "final ProtoChunk protoChunk = SerializableChunkData.parse((ServerLevel) level, level.registryAccess(), compoundTag)\n            .read((ServerLevel) level, ((ServerLevel) level).getPoiManager(), dummyInfo, chunkPos);": 1,
    "this.blockTicks = protoChunk.unpackBlockTicks();": 1,
    "this.fluidTicks = protoChunk.unpackFluidTicks();": 1,
    "this.blendingData = protoChunk.getBlendingData();": 1,
    "this.markUnsaved();": 2,
    "palettedContainerFactory = level.palettedContainerFactory();": 2,
}
for needle, expected in preserved.items():
    actual = text.count(needle)
    if actual != expected:
        raise SystemExit(
            f"fail-closed: preserved LevelChunk parse/copy anchor {needle!r} count={actual} expected={expected}"
        )

text = text.replace(old, new)

if old in text:
    raise SystemExit("fail-closed: legacy SerializableChunkData.parse RegistryAccess context remains")
if text.count(new) != 1:
    raise SystemExit(
        f"fail-closed: expected exactly one SerializableChunkData.parse PalettedContainerFactory context, found {text.count(new)}"
    )

post_preserved = {
    "public void copyChunkFromOtherDimension(@NotNull final VSLevelChunk srcChunkVS) {": 1,
    "final CompoundTag compoundTag = SerializableChunkData.copyOf((ServerLevel) srcChunk.getLevel(), srcChunk).write();": 1,
    "final RegionStorageInfo dummyInfo = new RegionStorageInfo(\"dummy\", level.dimension(), \"dummy\");": 1,
    "final ProtoChunk protoChunk = SerializableChunkData.parse((ServerLevel) level, level.palettedContainerFactory(), compoundTag)\n            .read((ServerLevel) level, ((ServerLevel) level).getPoiManager(), dummyInfo, chunkPos);": 1,
    "this.blockTicks = protoChunk.unpackBlockTicks();": 1,
    "this.fluidTicks = protoChunk.unpackFluidTicks();": 1,
    "this.blendingData = protoChunk.getBlendingData();": 1,
    "this.markUnsaved();": 2,
    "palettedContainerFactory = level.palettedContainerFactory();": 2,
}
for needle, expected in post_preserved.items():
    actual = text.count(needle)
    if actual != expected:
        raise SystemExit(
            f"fail-closed: LevelChunk parse/copy anchor changed after adaptation: {needle!r} count={actual} expected={expected}"
        )

path.write_text(text, encoding="utf-8")
print("P1_LEVELCHUNK_SERIALIZABLE_PARSE_FACTORY_26_2_OVERLAY_APPLIED")
