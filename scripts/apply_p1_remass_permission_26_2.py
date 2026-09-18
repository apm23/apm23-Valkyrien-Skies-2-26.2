#!/usr/bin/env python3
"""Apply the isolated Minecraft 26.2 RemassCommand permission adaptation.

Exact P1 run 35377209937 leaves two independent RemassCommand.kt errors:
removed CommandSourceStack.hasPermission(Int) and nullable ship.slug in a
translated-message vararg. This fail-closed overlay changes only the permission
predicate and imports; remass behavior and the nullable slug remain untouched.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
rel = "common/src/main/kotlin/org/valkyrienskies/mod/common/command/commands/RemassCommand.kt"
path = root / rel
text = path.read_text(encoding="utf-8")


def replace_count(old: str, new: str, expected: int = 1) -> None:
    global text
    count = text.count(old)
    if count != expected:
        raise SystemExit(f"expected {expected} matches in {rel}: {old!r}; found {count}")
    text = text.replace(old, new)


# Pinned baseline f39132148e... and current 1.21.1/main are byte-identical at
# blob 616c1d8071da930729ee1610834c3d5a23f988c9. remassShipCommandPerms is
# documented as 0..4 and defaults to 2. Preserve that configured threshold via
# Minecraft 26.2 Permission.HasCommandLevel without changing remass semantics.
replace_count(
    "import net.minecraft.network.chat.Component.translatable\n",
    "import net.minecraft.network.chat.Component.translatable\nimport net.minecraft.server.permissions.Permission\nimport net.minecraft.server.permissions.PermissionLevel\n",
)
replace_count(
    ".requires{ it.hasPermission(VSGameConfig.SERVER.Commands.remassShipCommandPerms)}",
    ".requires{ it.permissions().hasPermission(Permission.HasCommandLevel(PermissionLevel.byId(VSGameConfig.SERVER.Commands.remassShipCommandPerms)))}",
)

path.write_text(text, encoding="utf-8")
print("P1_REMASS_PERMISSION_26_2_OVERLAY_APPLIED")
