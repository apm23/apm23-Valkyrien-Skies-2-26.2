#!/usr/bin/env python3
"""Apply the isolated Minecraft 26.2 GetShipCommand permission adaptation.

Exact P1 run 35375165938 proved DeleteCommand's permission migration clean and
reports two independent errors in GetShipCommand.kt: removed
CommandSourceStack.hasPermission(Int) and nullable ship.slug in a translated
message vararg. This fail-closed overlay changes only the permission predicate
and imports; ray trace, ship lookup, messages, IDs, branching and return values
remain unchanged. The nullable slug is intentionally left untouched.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
rel = "common/src/main/kotlin/org/valkyrienskies/mod/common/command/commands/GetShipCommand.kt"
path = root / rel
text = path.read_text(encoding="utf-8")


def replace_count(old: str, new: str, expected: int = 1) -> None:
    global text
    count = text.count(old)
    if count != expected:
        raise SystemExit(f"expected {expected} matches in {rel}: {old!r}; found {count}")
    text = text.replace(old, new)


# Pinned baseline f39132148e... and current 1.21.1/main are byte-identical at
# blob 056766bf1ee40ebd266d88a3e28c8f6b87d22a7d. getShipCommandPerms is
# documented as 0..4 and defaults to 0. Preserve that configured threshold via
# Minecraft 26.2 Permission.HasCommandLevel without changing get-ship semantics.
replace_count(
    "import net.minecraft.network.chat.Component.translatable\n",
    "import net.minecraft.network.chat.Component.translatable\nimport net.minecraft.server.permissions.Permission\nimport net.minecraft.server.permissions.PermissionLevel\n",
)
replace_count(
    ".requires{ it.hasPermission(VSGameConfig.SERVER.Commands.getShipCommandPerms)}",
    ".requires{ it.permissions().hasPermission(Permission.HasCommandLevel(PermissionLevel.byId(VSGameConfig.SERVER.Commands.getShipCommandPerms)))}",
)

path.write_text(text, encoding="utf-8")
print("P1_GETSHIP_PERMISSION_26_2_OVERLAY_APPLIED")
