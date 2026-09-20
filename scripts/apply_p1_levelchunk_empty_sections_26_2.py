#!/usr/bin/env python3
"""Adapt only MixinLevelChunk empty-section construction to Minecraft 26.2.

Pinned upstream VS2 clears/fills LevelChunk sections using a biome Registry context and
LevelChunkSection(Registry<Biome>). Minecraft 26.2 constructs an empty LevelChunkSection from a
PalettedContainerFactory, and Level exposes the matching palettedContainerFactory() context.

This fail-closed overlay changes only the two empty-section fill sites in clearChunk() and
copyChunkFromOtherDimension(). It preserves section counts/null checks, copy ordering,
tick-container ordering, heightmaps, light state, deserialization, blending-data ownership,
dirty-save marking, and all ship lifecycle/reference-space authority.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/world/chunk/MixinLevelChunk.java"
if not path.is_file():
    raise SystemExit(f"fail-closed: expected pinned VS2 MixinLevelChunk source missing: {path}")

text = path.read_text(encoding="utf-8")

old_registry = "        final Registry<Biome> registry = level.registryAccess().registryOrThrow(Registries.BIOME);"
new_factory = "        final var palettedContainerFactory = level.palettedContainerFactory();"
old_ctor = "            sections[i] = new LevelChunkSection(registry);"
new_ctor = "            sections[i] = new LevelChunkSection(palettedContainerFactory);"

if text.count(old_registry) != 2:
    raise SystemExit(
        f"fail-closed: expected two legacy LevelChunk biome-registry contexts, found {text.count(old_registry)}"
    )
if text.count(old_ctor) != 2:
    raise SystemExit(
        f"fail-closed: expected two legacy LevelChunkSection registry constructors, found {text.count(old_ctor)}"
    )
if "palettedContainerFactory = level.palettedContainerFactory();" in text:
    raise SystemExit("fail-closed: LevelChunk empty-section factory adaptation already present")

preserved = {
    "public void clearChunk() {": 1,
    "public void copyChunkFromOtherDimension(@NotNull final VSLevelChunk srcChunkVS) {": 1,
    "Arrays.fill(sections, null);": 2,
    "if (sections[i] != null) continue;": 2,
    "registerTickContainerInLevel((ServerLevel) level);": 2,
    "this.markUnsaved();": 2,
    "SerializableChunkData.parse((ServerLevel) level, level.registryAccess(), compoundTag)": 1,
    "this.blendingData = protoChunk.getBlendingData();": 1,
}
for needle, expected in preserved.items():
    actual = text.count(needle)
    if actual != expected:
        raise SystemExit(
            f"fail-closed: preserved LevelChunk semantic anchor {needle!r} count={actual} expected={expected}"
        )

for import_line in (
    "import net.minecraft.core.Registry;\n",
    "import net.minecraft.core.registries.Registries;\n",
    "import net.minecraft.world.level.biome.Biome;\n",
):
    if text.count(import_line) != 1:
        raise SystemExit(f"fail-closed: expected exactly one obsolete import {import_line.strip()!r}")

text = text.replace(old_registry, new_factory)
text = text.replace(old_ctor, new_ctor)
for import_line in (
    "import net.minecraft.core.Registry;\n",
    "import net.minecraft.core.registries.Registries;\n",
    "import net.minecraft.world.level.biome.Biome;\n",
):
    text = text.replace(import_line, "")

if old_registry in text or old_ctor in text:
    raise SystemExit("fail-closed: legacy LevelChunk empty-section registry API remains")
if text.count(new_factory) != 2:
    raise SystemExit(
        f"fail-closed: expected two PalettedContainerFactory contexts, found {text.count(new_factory)}"
    )
if text.count(new_ctor) != 2:
    raise SystemExit(
        f"fail-closed: expected two PalettedContainerFactory LevelChunkSection constructors, found {text.count(new_ctor)}"
    )
for needle, expected in preserved.items():
    actual = text.count(needle)
    if actual != expected:
        raise SystemExit(
            f"fail-closed: LevelChunk semantic anchor changed after empty-section adaptation: {needle!r} count={actual} expected={expected}"
        )

path.write_text(text, encoding="utf-8")
print("P1_LEVELCHUNK_EMPTY_SECTIONS_26_2_OVERLAY_APPLIED")
