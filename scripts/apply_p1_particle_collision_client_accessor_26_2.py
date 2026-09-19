#!/usr/bin/env python3
"""Adapt pinned upstream VS2 particle-collision mixin to Minecraft 26.2 Level client accessor.

Minecraft 26.2 no longer permits direct access to Level.isClientSide from this
mixin. Use the public isClientSide() accessor while preserving the upstream VS2
particle-collision gating and collision authority exactly.
"""

from pathlib import Path
import sys

TARGET = Path(
    "common/src/main/java/org/valkyrienskies/mod/mixin/feature/particle_collision/MixinEntity.java"
)


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {sys.argv[0]} <upstream-vs2-root>")

    path = Path(sys.argv[1]) / TARGET
    if not path.is_file():
        raise SystemExit(f"fail-closed: pinned particle-collision mixin missing: {path}")

    text = path.read_text(encoding="utf-8")
    old = "if (entity != null || !level.isClientSide) {"
    new = "if (entity != null || !level.isClientSide()) {"

    count = text.count(old)
    if count != 1:
        raise SystemExit(
            f"fail-closed: expected exactly one pinned Level.isClientSide field-access anchor, found {count}"
        )
    if text.count("!level.isClientSide()"):
        raise SystemExit("fail-closed: 26.2 Level client accessor adaptation already present")

    text = text.replace(old, new, 1)

    if text.count(new) != 1:
        raise SystemExit("fail-closed: particle-collision Level client accessor replacement count mismatch")
    if text.count("EntityShipCollisionUtils.INSTANCE.adjustEntityMovementForShipCollisions") != 1:
        raise SystemExit("fail-closed: upstream VS2 particle collision authority anchor changed")

    path.write_text(text, encoding="utf-8")
    print("P1_PARTICLE_COLLISION_CLIENT_ACCESSOR_26_2_OVERLAY_APPLIED")


if __name__ == "__main__":
    main()
