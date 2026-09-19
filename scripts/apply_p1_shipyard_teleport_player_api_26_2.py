#!/usr/bin/env python3
"""Fail-closed Minecraft 26.2 ServerPlayer API adaptation for the shipyard teleport unit."""

from pathlib import Path
import sys

TARGET = Path("common/src/main/java/org/valkyrienskies/mod/mixin/server/command/level/MixinServerPlayer.java")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {sys.argv[0]} <upstream-vs2-root>")

    path = Path(sys.argv[1]) / TARGET
    if not path.is_file():
        raise SystemExit(f"fail-closed: target missing: {path}")

    text = path.read_text(encoding="utf-8")

    required_after_primary_overlay = (
        "import net.minecraft.world.entity.Relative;",
        "Set<Relative> set, float g, float h, boolean resetCamera",
        "this.getYRot(), this.getXRot(), false);",
        "VSGameUtilsKt.getShipManagingPos(level, x, y, z)",
        "ship.getTransform().getShipToWorld().transformDirection(lookVector)",
        "((IEntityDraggingInformationProvider)this).vs$dragImmediately(ship);",
    )
    for anchor in required_after_primary_overlay:
        if anchor not in text:
            raise SystemExit(f"fail-closed: primary teleport overlay anchor missing: {anchor}")

    old_super = "        super(level, blockPos, f, gameProfile);"
    new_super = "        super(level, gameProfile);"
    if text.count(old_super) != 1:
        raise SystemExit(f"fail-closed: expected one legacy Player constructor call, found {text.count(old_super)}")
    text = text.replace(old_super, new_super, 1)

    old_level = "ServerLevel level = ((ServerPlayer) (Object) this).serverLevel();"
    new_level = "ServerLevel level = ((ServerPlayer) (Object) this).level();"
    if text.count(old_level) != 2:
        raise SystemExit(f"fail-closed: expected two legacy ServerPlayer.serverLevel() calls, found {text.count(old_level)}")
    text = text.replace(old_level, new_level)

    if "serverLevel()" in text:
        raise SystemExit("fail-closed: obsolete ServerPlayer.serverLevel() remains")
    if text.count(new_super) != 1 or text.count(new_level) != 2:
        raise SystemExit("fail-closed: 26.2 ServerPlayer API adaptation count mismatch")

    path.write_text(text, encoding="utf-8")
    print("P1_SHIPYARD_TELEPORT_PLAYER_API_26_2_OVERLAY_APPLIED")


if __name__ == "__main__":
    main()
