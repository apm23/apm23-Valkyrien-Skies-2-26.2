#!/usr/bin/env python3
"""Preserve the VS2 shipyard BlendingData invariant on Minecraft 26.2.

Pinned upstream VS2 live-copies a shipyard LevelChunk across dimensions and assigns the parsed
ProtoChunk blendingData onto the already-live destination chunk. Minecraft 26.2 makes
ChunkAccess.blendingData constructor-owned/final, so that post-construction assignment is no
longer legal.

For the VS2 shipyard path this metadata is invariantly null: vanilla empty ProtoChunk construction
uses null BlendingData, and pinned VS2 cancels shipyard worldgen stages that could require terrain
blending. Because the 26.2 field is final, a normal live shipyard LevelChunk therefore remains null.

This fail-closed overlay removes only the now-illegal null-to-null assignment. It explicitly rejects
any source or destination chunk carrying non-null BlendingData rather than silently dropping
metadata or mutating a final field. All other original VS2 cross-dimension live-copy state and
authority remain unchanged.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/world/chunk/MixinLevelChunk.java"
if not path.is_file():
    raise SystemExit(f"fail-closed: expected pinned VS2 MixinLevelChunk source missing: {path}")

text = path.read_text(encoding="utf-8")

old = "        this.blendingData = protoChunk.getBlendingData();\n"
new = (
    "        if (protoChunk.getBlendingData() != null || this.blendingData != null) {\n"
    "            throw new IllegalStateException(\n"
    "                \"VS2 MC 26.2 cross-dimension shipyard chunk transfer encountered non-null BlendingData; \"\n"
    "                    + \"BlendingData is constructor-owned in 26.2 and cannot be replaced on a live LevelChunk\"\n"
    "            );\n"
    "        }\n"
)

if text.count(old) != 1:
    raise SystemExit(
        f"fail-closed: expected exactly one pinned VS2 live blendingData assignment, found {text.count(old)}"
    )
if "VS2 MC 26.2 cross-dimension shipyard chunk transfer encountered non-null BlendingData" in text:
    raise SystemExit("fail-closed: LevelChunk BlendingData invariant adaptation already present")

required_before = {
    "public void copyChunkFromOtherDimension(@NotNull final VSLevelChunk srcChunkVS) {": 1,
    "final LevelChunk srcChunk = (LevelChunk) srcChunkVS;": 1,
    "final CompoundTag compoundTag = SerializableChunkData.copyOf((ServerLevel) srcChunk.getLevel(), srcChunk).write();": 1,
    "SerializableChunkData.parse((ServerLevel) level, level.palettedContainerFactory(), compoundTag)": 1,
    "this.blockTicks = protoChunk.unpackBlockTicks();": 1,
    "this.fluidTicks = protoChunk.unpackFluidTicks();": 1,
    "this.markUnsaved();": 2,
}
for needle, expected in required_before.items():
    actual = text.count(needle)
    if actual != expected:
        raise SystemExit(
            f"fail-closed: preserved LevelChunk live-copy anchor {needle!r} count={actual} expected={expected}"
        )

text = text.replace(old, new)

if old in text:
    raise SystemExit("fail-closed: illegal live blendingData assignment remains")
if text.count("protoChunk.getBlendingData() != null || this.blendingData != null") != 1:
    raise SystemExit("fail-closed: expected exactly one BlendingData invariant guard after adaptation")

required_after = {
    "public void copyChunkFromOtherDimension(@NotNull final VSLevelChunk srcChunkVS) {": 1,
    "final LevelChunk srcChunk = (LevelChunk) srcChunkVS;": 1,
    "final CompoundTag compoundTag = SerializableChunkData.copyOf((ServerLevel) srcChunk.getLevel(), srcChunk).write();": 1,
    "SerializableChunkData.parse((ServerLevel) level, level.palettedContainerFactory(), compoundTag)": 1,
    "this.blockTicks = protoChunk.unpackBlockTicks();": 1,
    "this.fluidTicks = protoChunk.unpackFluidTicks();": 1,
    "this.markUnsaved();": 2,
    "BlendingData is constructor-owned in 26.2 and cannot be replaced on a live LevelChunk": 1,
}
for needle, expected in required_after.items():
    actual = text.count(needle)
    if actual != expected:
        raise SystemExit(
            f"fail-closed: LevelChunk live-copy anchor changed after adaptation: {needle!r} count={actual} expected={expected}"
        )

path.write_text(text, encoding="utf-8")
print("P1_LEVELCHUNK_BLENDINGDATA_INVARIANT_26_2_OVERLAY_APPLIED")
