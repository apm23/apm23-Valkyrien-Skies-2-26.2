#!/usr/bin/env python3
"""Adapt pinned upstream VS2 submarine WaterFluid mixin to Minecraft 26.2 Level client accessor.

Minecraft 26.2 no longer permits direct access to Level.isClientSide from this
mixin. Use isClientSide() while preserving upstream VS2 sealed-position,
ship-intersection, transform, connectivity, and animation-cancel semantics.
"""

from pathlib import Path
import sys

TARGET = Path(
    "common/src/main/java/org/valkyrienskies/mod/mixin/feature/submarines/MixinWaterFluid.java"
)


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {sys.argv[0]} <upstream-vs2-root>")

    path = Path(sys.argv[1]) / TARGET
    if not path.is_file():
        raise SystemExit(f"fail-closed: pinned WaterFluid mixin missing: {path}")

    text = path.read_text(encoding="utf-8")
    old = "ValkyrienSkies.isConnectivityEnabled(level.isClientSide)"
    new = "ValkyrienSkies.isConnectivityEnabled(level.isClientSide())"

    count = text.count(old)
    if count != 1:
        raise SystemExit(
            f"fail-closed: expected exactly one pinned Level.isClientSide field-access anchor, found {count}"
        )
    if text.count(new):
        raise SystemExit("fail-closed: 26.2 WaterFluid client accessor adaptation already present")

    text = text.replace(old, new, 1)

    required = (
        "ValkyrienSkies.isBlockInShipyard(level, blockPos)",
        "ValkyrienSkies.getShipsIntersecting(level, blockPos.getX(), blockPos.getY(), blockPos.getZ())",
        "ship.getWorldToShip().transformPosition",
        "VSGameUtilsKt.isPositionMaybeSealed(level, blockPosInShip)",
        "ci.cancel();",
    )
    for anchor in required:
        if anchor not in text:
            raise SystemExit(f"fail-closed: upstream VS2 WaterFluid semantic anchor changed: {anchor}")

    if text.count(new) != 1:
        raise SystemExit("fail-closed: WaterFluid Level client accessor replacement count mismatch")

    path.write_text(text, encoding="utf-8")
    print("P1_WATERFLUID_CLIENT_ACCESSOR_26_2_OVERLAY_APPLIED")


if __name__ == "__main__":
    main()
