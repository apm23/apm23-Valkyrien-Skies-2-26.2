#!/usr/bin/env python3
"""Apply the isolated Minecraft 26.2 DeleteCommand permission adaptation.

Exact P1 run 35372443583 proved TeleportCommand clean and reports two compile
errors in DeleteCommand.kt: the removed CommandSourceStack.hasPermission(Int)
API and an independent nullable ship-slug message argument. This fail-closed
overlay changes only the permission predicate and imports; delete selection,
deleteBlocks behavior, ShipAssembler.deleteShip calls, messages, and return
values remain unchanged. The nullable slug is intentionally left untouched.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
rel = "common/src/main/kotlin/org/valkyrienskies/mod/common/command/commands/DeleteCommand.kt"
path = root / rel
text = path.read_text(encoding="utf-8")


def replace_count(old: str, new: str, expected: int = 1) -> None:
    global text
    count = text.count(old)
    if count != expected:
        raise SystemExit(f"expected {expected} matches in {rel}: {old!r}; found {count}")
    text = text.replace(old, new)


# Pinned baseline f39132148e... and current 1.21.1/main are byte-identical at
# blob 0d4696201608cacd336824f1e2c711a3d770feb7. deleteShipCommandPerms is
# constrained to 0..4 and defaults to 2. Preserve that threshold through the
# Minecraft 26.2 permission API without changing delete/message semantics.
replace_count(
    "import net.minecraft.network.chat.Component\n",
    "import net.minecraft.network.chat.Component\nimport net.minecraft.server.permissions.Permission\nimport net.minecraft.server.permissions.PermissionLevel\n",
)
replace_count(
    ".requires{ it.hasPermission(VSGameConfig.SERVER.Commands.deleteShipCommandPerms)}",
    ".requires{ it.permissions().hasPermission(Permission.HasCommandLevel(PermissionLevel.byId(VSGameConfig.SERVER.Commands.deleteShipCommandPerms)))}",
)

path.write_text(text, encoding="utf-8")
print("P1_DELETE_PERMISSION_26_2_OVERLAY_APPLIED")
