#!/usr/bin/env python3
"""Adapt only ShipMountingEntity's inherited generic Entity damage contract to Minecraft 26.2.

Pinned upstream VS2 does not override Entity.hurt/damage. In Minecraft 1.21.1 the inherited
Entity implementation rejects invulnerable damage, otherwise marks the entity hurt for
velocity synchronization, and still returns false. Minecraft 26.2 moved that server-side
contract into abstract Entity.hurtServer(ServerLevel, DamageSource, float), while exposing
the same base invulnerability predicate as isInvulnerableToBase() and retaining markHurt().
This overlay implements only that exact inherited behavior. It does not change mounting,
controller state, ship/reference-space behavior, construction, persistence, networking,
removal, passenger handling, or gameplay authority.
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
    "import net.minecraft.server.level.ServerEntity\n",
    "import net.minecraft.server.level.ServerEntity\n"
    "import net.minecraft.server.level.ServerLevel\n"
    "import net.minecraft.world.damagesource.DamageSource\n",
)
replace_once(
    "    override fun readAdditionalSaveData(input: ValueInput) {}\n",
    "    override fun hurtServer(level: ServerLevel, source: DamageSource, damage: Float): Boolean {\n"
    "        if (isInvulnerableToBase(source)) {\n"
    "            return false\n"
    "        }\n"
    "        markHurt()\n"
    "        return false\n"
    "    }\n\n"
    "    override fun readAdditionalSaveData(input: ValueInput) {}\n",
)

expected = "override fun hurtServer(level: ServerLevel, source: DamageSource, damage: Float): Boolean"
if text.count(expected) != 1:
    raise SystemExit(f"expected exactly one Minecraft 26.2 hurtServer override in {path}")
if text.count("isInvulnerableToBase(source)") != 1:
    raise SystemExit(f"expected exactly one base invulnerability check in {path}")
if text.count("markHurt()") != 1:
    raise SystemExit(f"expected exactly one inherited Entity hurt-sync mark in {path}")

path.write_text(text, encoding="utf-8")
print("P1_SHIPMOUNTINGENTITY_HURTSERVER_26_2_OVERLAY_APPLIED")
