#!/usr/bin/env python3
"""Adapt only ShipMountingEntity's empty entity-persistence hook signatures to Minecraft 26.2.

Pinned upstream VS2 intentionally persists no ShipMountingEntity-specific payload: both
readAdditionalSaveData and addAdditionalSaveData bodies are empty. Minecraft 26.2 keeps the
same entity lifecycle hooks but changes their transport types from CompoundTag to
ValueInput/ValueOutput. This overlay changes only those two empty signatures/imports. It does
not touch mounting, controller state, ship/reference-space behavior, hurt handling, entity
construction, networking, or gameplay logic.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
path = root / "common/src/main/kotlin/org/valkyrienskies/mod/common/entity/ShipMountingEntity.kt"
text = path.read_text(encoding="utf-8")


def replace_once(old: str, new: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"expected exactly one occurrence of {old!r} in {path}, found {count}")
    text = text.replace(old, new)


replace_once(
    "import net.minecraft.nbt.CompoundTag\n",
    "import net.minecraft.world.level.storage.ValueInput\n"
    "import net.minecraft.world.level.storage.ValueOutput\n",
)
replace_once(
    "    override fun readAdditionalSaveData(compound: CompoundTag) {}\n",
    "    override fun readAdditionalSaveData(input: ValueInput) {}\n",
)
replace_once(
    "    override fun addAdditionalSaveData(compound: CompoundTag) {}\n",
    "    override fun addAdditionalSaveData(output: ValueOutput) {}\n",
)

if "CompoundTag" in text:
    raise SystemExit(f"legacy CompoundTag persistence hook remains in {path}")
if text.count("override fun readAdditionalSaveData(input: ValueInput) {}") != 1:
    raise SystemExit(f"expected exactly one empty ValueInput read hook in {path}")
if text.count("override fun addAdditionalSaveData(output: ValueOutput) {}") != 1:
    raise SystemExit(f"expected exactly one empty ValueOutput write hook in {path}")

path.write_text(text, encoding="utf-8")
print("P1_SHIPMOUNTINGENTITY_VALUE_IO_26_2_OVERLAY_APPLIED")
