#!/usr/bin/env python3
"""Apply the isolated Minecraft 26.2 GetGravityCommand permission adaptation.

This fail-closed overlay is intentionally separate so exact P1 run 35355388045's
GetAirCommand proof remains preserved before the next compiler-driven change.
It adapts only the removed CommandSourceStack.hasPermission(Int) API and must not
change VS2 ship-space, physics, collision, entity/player/camera, networking, or rendering.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
rel = "common/src/main/kotlin/org/valkyrienskies/mod/common/command/commands/GetGravityCommand.kt"
path = root / rel
text = path.read_text(encoding="utf-8")


def replace_count(old: str, new: str, expected: int = 1) -> None:
    global text
    count = text.count(old)
    if count != expected:
        raise SystemExit(f"expected {expected} matches in {rel}: {old!r}; found {count}")
    text = text.replace(old, new)


# Run 35355388045 reports exactly one compile error in GetGravityCommand.kt: the removed
# CommandSourceStack.hasPermission(Int) call. Pinned baseline f39132148e... and current
# upstream 1.21.1/main are byte-identical at blob c5266aefbc3f3970ea21daf6a3cf50a0b277390e.
# getAirValuesPerms is the same explicit 0..4 threshold already proven for GetAirCommand.
# Preserve gravity/aerodynamic lookup, dimension handling, messages, and return semantics.
replace_count(
    "import net.minecraft.network.chat.Component.translatable\n",
    "import net.minecraft.network.chat.Component.translatable\nimport net.minecraft.server.permissions.Permission\nimport net.minecraft.server.permissions.PermissionLevel\n",
)
replace_count(
    "literal(\"get-gravity\").requires { it.hasPermission(VSGameConfig.SERVER.Commands.getAirValuesPerms)}",
    "literal(\"get-gravity\").requires { it.permissions().hasPermission(Permission.HasCommandLevel(PermissionLevel.byId(VSGameConfig.SERVER.Commands.getAirValuesPerms)))}",
)

path.write_text(text, encoding="utf-8")
print("P1_GET_GRAVITY_PERMISSION_26_2_OVERLAY_APPLIED")
