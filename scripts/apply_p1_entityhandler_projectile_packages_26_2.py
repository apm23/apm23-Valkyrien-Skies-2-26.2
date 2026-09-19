#!/usr/bin/env python3
"""Fail-closed Minecraft 26.2 projectile package adaptation for VS2 entity handlers.

This overlay changes only the package imports for AbstractArrow and
AbstractHurtingProjectile in the pinned upstream AbstractShipyardEntityHandler
and WorldEntityHandler. It does not alter projectile movement, rotation,
velocity transfer, entity dragging, ship transforms, rendering, networking,
or authority semantics.
"""

from pathlib import Path
import sys


FILES = (
    Path("common/src/main/kotlin/org/valkyrienskies/mod/common/entity/handling/AbstractShipyardEntityHandler.kt"),
    Path("common/src/main/kotlin/org/valkyrienskies/mod/common/entity/handling/WorldEntityHandler.kt"),
)

REPLACEMENTS = (
    (
        "import net.minecraft.world.entity.projectile.AbstractArrow",
        "import net.minecraft.world.entity.projectile.arrow.AbstractArrow",
    ),
    (
        "import net.minecraft.world.entity.projectile.AbstractHurtingProjectile",
        "import net.minecraft.world.entity.projectile.hurtingprojectile.AbstractHurtingProjectile",
    ),
)


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {sys.argv[0]} <upstream-vs2-root>")

    root = Path(sys.argv[1])
    for relative_path in FILES:
        path = root / relative_path
        text = path.read_text(encoding="utf-8")

        for old, new in REPLACEMENTS:
            count = text.count(old)
            if count != 1:
                raise SystemExit(
                    f"fail-closed: expected exactly one {old!r} in {relative_path}, found {count}"
                )
            if new in text:
                raise SystemExit(
                    f"fail-closed: target import already present unexpectedly in {relative_path}: {new!r}"
                )
            text = text.replace(old, new, 1)

        path.write_text(text, encoding="utf-8")

    print("Applied Minecraft 26.2 AbstractArrow/AbstractHurtingProjectile package overlay to 2 VS2 entity handlers")


if __name__ == "__main__":
    main()
