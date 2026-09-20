#!/usr/bin/env python3
"""Adapt pinned upstream VS2 Explosion mixin to Minecraft 26.2 Level client accessor.

Minecraft 26.2 no longer permits direct access to Level.isClientSide from this
mixin. Use isClientSide() while preserving every upstream VS2 explosion,
ship/reference-space, splitting, clipping, and force-application authority.
"""

from pathlib import Path
import sys

TARGET = Path(
    "common/src/main/java/org/valkyrienskies/mod/mixin/feature/explosions/MixinExplosion.java"
)


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {sys.argv[0]} <upstream-vs2-root>")

    path = Path(sys.argv[1]) / TARGET
    if not path.is_file():
        raise SystemExit(f"fail-closed: pinned Explosion mixin missing: {path}")

    text = path.read_text(encoding="utf-8")
    old = "if (this.level.isClientSide) {"
    new = "if (this.level.isClientSide()) {"

    if text.count(old) != 1:
        raise SystemExit(
            f"fail-closed: expected exactly one pinned Explosion Level.isClientSide field-access anchor, found {text.count(old)}"
        )
    if new in text:
        raise SystemExit("fail-closed: 26.2 Explosion client accessor adaptation already present")

    required = (
        "private void doExplodeForce() {",
        "final LoadedServerShip ship = VSGameUtilsKt.getLoadedShipManagingPos((ServerLevel) this.level, blockPos);",
        "ValkyrienSkiesMod.splitHandler.split(level, ship.getId(),",
        "forceApplier.applyWorldForceToModelPos(ship.getId(), forceVector,",
        "VSGameUtilsKt.transformToNearbyShipsAndWorld(this.level, this.x, this.y, this.z, this.radius, (x, y, z) -> {",
        "private static ClipContext getSeenPercent$ClipContext$new(",
        "private List<Entity> noRayTrace(final Level instance, final Entity entity, final AABB aabb,",
        "return Collections.emptyList();",
        "return getEntities.call(instance, entity, aabb);",
    )
    for anchor in required:
        if anchor not in text:
            raise SystemExit(f"fail-closed: upstream VS2 Explosion semantic anchor changed: {anchor}")

    text = text.replace(old, new, 1)

    if old in text:
        raise SystemExit("fail-closed: old Explosion Level client field access remains")
    if text.count(new) != 1:
        raise SystemExit("fail-closed: Explosion Level client accessor replacement count mismatch")
    for anchor in required:
        if anchor not in text:
            raise SystemExit(f"fail-closed: VS2 Explosion authority changed after adaptation: {anchor}")

    path.write_text(text, encoding="utf-8")
    print("P1_EXPLOSION_CLIENT_ACCESSOR_26_2_OVERLAY_APPLIED")


if __name__ == "__main__":
    main()
