#!/usr/bin/env python3
"""Apply the isolated Minecraft 26.2 TestChair entity-creation/positioning adaptation.

The pinned upstream chair creates the existing VS2 ShipMountingEntity only on the
logical server, places it at the same seat offset, aims it from the block facing,
marks it as controller, adds that exact instance, then mounts the player. Minecraft
26.2 requires an EntitySpawnReason for EntityType.create(Level, ...) and renamed
Entity.moveTo(...) to Entity.snapTo(...). This fail-closed overlay changes only those
API boundaries; it does not alter VS2 mounting, riding, entity type, offset, facing,
or controller semantics.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
rel = "common/src/main/kotlin/org/valkyrienskies/mod/common/block/TestChairBlock.kt"
path = root / rel
text = path.read_text(encoding="utf-8")


def require_once(needle: str) -> None:
    count = text.count(needle)
    if count != 1:
        raise SystemExit(f"expected exactly 1 semantic needle in {rel}: {needle!r}; found {count}")


def replace_once(old: str, new: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"expected exactly 1 replacement target in {rel}: {old!r}; found {count}")
    text = text.replace(old, new, 1)


# Pin the surrounding real-VS2 behavior before mutating anything. The Direction
# accessor below is expected to have already been adapted by the earlier frozen
# TestChair Direction overlay in the P1 workflow.
for needle in (
    "if (level.isClientSide) return InteractionResult.SUCCESS",
    "ValkyrienSkiesMod.SHIP_MOUNTING_ENTITY_TYPE",
    "Vector3d(pos.x + .5, pos.y.toDouble() + .15, pos.z + .5)",
    "state.getValue(FACING).getUnitVec3i().toDoubles().add(position())",
    "isController = true",
    "level.addFreshEntity(seatEntity)",
    "player.startRiding(seatEntity)",
):
    require_once(needle)

# Minecraft 26.2 no longer has the one-argument EntityType.create(Level) overload.
# This seat is created because a player triggered the chair interaction; TRIGGERED
# records that creation cause while retaining the old create-then-configure-then-add
# lifecycle instead of switching to EntityType.spawn().
replace_once(
    "import net.minecraft.world.InteractionResult\n",
    "import net.minecraft.world.InteractionResult\nimport net.minecraft.world.entity.EntitySpawnReason\n",
)
replace_once(
    "ValkyrienSkiesMod.SHIP_MOUNTING_ENTITY_TYPE.create(level)!!",
    "ValkyrienSkiesMod.SHIP_MOUNTING_ENTITY_TYPE.create(level, EntitySpawnReason.TRIGGERED)!!",
)

# NeoForge/Minecraft's 1.21.5+ API migration explicitly renamed Entity.moveTo to
# Entity.snapTo. Preserve the exact coordinates and the subsequent lookAt call.
replace_once(
    "moveTo(seatEntityPos.x, seatEntityPos.y, seatEntityPos.z)",
    "snapTo(seatEntityPos.x, seatEntityPos.y, seatEntityPos.z)",
)

# Re-assert the semantic envelope after replacement.
for needle in (
    "if (level.isClientSide) return InteractionResult.SUCCESS",
    "ValkyrienSkiesMod.SHIP_MOUNTING_ENTITY_TYPE.create(level, EntitySpawnReason.TRIGGERED)!!",
    "snapTo(seatEntityPos.x, seatEntityPos.y, seatEntityPos.z)",
    "lookAt(EntityAnchorArgument.Anchor.EYES, state.getValue(FACING).getUnitVec3i().toDoubles().add(position()))",
    "isController = true",
    "level.addFreshEntity(seatEntity)",
    "player.startRiding(seatEntity)",
):
    require_once(needle)

path.write_text(text, encoding="utf-8")
print("P1_TESTCHAIR_ENTITY_CREATION_26_2_OVERLAY_APPLIED")
