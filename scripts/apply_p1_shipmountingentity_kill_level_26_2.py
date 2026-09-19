#!/usr/bin/env python3
"""Adapt only ShipMountingEntity's server-side self-removal call to Minecraft 26.2.

Pinned upstream VS2 calls Entity.kill() only inside the existing !level().isClientSide guard
when the mounting entity has no passengers. Minecraft 26.2 requires Entity.kill(ServerLevel),
so this overlay passes the same entity level through that already-server-only branch. It does
not change mounting/controller state, ship/reference-space behavior, damage handling,
persistence, networking, passenger handling, removal timing, or gameplay authority.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
path = root / "common/src/main/kotlin/org/valkyrienskies/mod/common/entity/ShipMountingEntity.kt"
text = path.read_text(encoding="utf-8")

if text.count("import net.minecraft.server.level.ServerLevel\n") != 1:
    raise SystemExit(
        f"expected exactly one frozen ServerLevel import from the hurtServer overlay in {path}"
    )

old = (
    "        if (!level().isClientSide && passengers.isEmpty()) {\n"
    "            // Kill this entity if nothing is riding it\n"
    "            kill()\n"
    "            return\n"
    "        }\n"
)
new = (
    "        if (!level().isClientSide && passengers.isEmpty()) {\n"
    "            // Kill this entity if nothing is riding it\n"
    "            kill(level() as ServerLevel)\n"
    "            return\n"
    "        }\n"
)

count = text.count(old)
if count != 1:
    raise SystemExit(f"expected exactly one pinned upstream server-side kill block in {path}, found {count}")
text = text.replace(old, new)

if text.count("kill(level() as ServerLevel)") != 1:
    raise SystemExit(f"expected exactly one Minecraft 26.2 ServerLevel kill call in {path}")
if "            kill()\n" in text:
    raise SystemExit(f"legacy zero-argument ShipMountingEntity kill call remains in {path}")

path.write_text(text, encoding="utf-8")
print("P1_SHIPMOUNTINGENTITY_KILL_LEVEL_26_2_OVERLAY_APPLIED")
