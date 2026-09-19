#!/usr/bin/env python3
"""Adapt only MixinAirAndWaterRandomPos's exclusive max-build boundary to Minecraft 26.2.

Pinned upstream VS2 passes Level.getMaxBuildHeight() as the upper build-height limit to
RandomPos.moveUpOutOfSolid(...). Minecraft 26.2 no longer exposes that accessor. Existing
frozen VS2 port evidence maps the same exclusive maximum to getMinY() + getHeight(). This
overlay changes only that accessor vocabulary and preserves all pathfinding/ship logic.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/feature/ai/path_retargeting/MixinAirAndWaterRandomPos.java"
text = path.read_text(encoding="utf-8")

old = "pathfinderMob.level().getMaxBuildHeight()"
new = "pathfinderMob.level().getMinY() + pathfinderMob.level().getHeight()"

count = text.count(old)
if count != 1:
    raise SystemExit(f"expected exactly one pinned max-build accessor in {path}, found {count}")
text = text.replace(old, new, 1)

if text.count(new) != 1:
    raise SystemExit(f"expected exactly one Minecraft 26.2 exclusive max-build expression in {path}")
if old in text:
    raise SystemExit(f"legacy getMaxBuildHeight() remains in {path}")

for anchor in (
    "if (cir.getReturnValue() != null)",
    "if (blockPos2 == null)",
    "VSGameUtilsKt.getShipObjectWorld(pathfinderMob.level()).getLoadedShips().getIntersecting(",
    "ship.getWorldToShip()",
    ".transformPosition(VectorConversionsMCKt.toJOMLD(blockPos2), new Vector3d())",
    "BlockPos blockPosInShip = BlockPos.containing(VectorConversionsMCKt.toMinecraft(posInShip));",
    "!GoalUtils.isRestricted(bl, pathfinderMob, blockPosInShip)",
    "RandomPos.moveUpOutOfSolid(blockPos2,",
    "arg2 -> GoalUtils.isSolid(pathfinderMob, arg2)",
    "cir.setReturnValue(blockPosInShip);",
    "break;",
):
    if text.count(anchor) != 1:
        raise SystemExit(f"expected preserved AirAndWaterRandomPos semantic anchor exactly once: {anchor!r}")

path.write_text(text, encoding="utf-8")
print("P1_AIRWATERRANDOMPOS_BUILDHEIGHT_26_2_OVERLAY_APPLIED")
