#!/usr/bin/env python3
"""Apply the isolated Minecraft 26.2 RenameCommand permission adaptation.

Exact P1 run 35359836381 proved DryCommand clean and reports exactly one
compile error in RenameCommand.kt: the removed CommandSourceStack.hasPermission(Int)
API. This fail-closed overlay changes only that permission predicate and imports;
VS2 ship selection and vsCore.renameShip behavior remain unchanged.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
rel = "common/src/main/kotlin/org/valkyrienskies/mod/common/command/commands/RenameCommand.kt"
path = root / rel
text = path.read_text(encoding="utf-8")


def replace_count(old: str, new: str, expected: int = 1) -> None:
    global text
    count = text.count(old)
    if count != expected:
        raise SystemExit(f"expected {expected} matches in {rel}: {old!r}; found {count}")
    text = text.replace(old, new)


# Pinned baseline f39132148e... and current 1.21.1/main are byte-identical at
# blob 004232736c5ff628794156d826d39bdd0cb53bc7. renameShipCommandPerms is
# explicitly constrained to 0..4 and defaults to 2. Preserve that threshold via
# Minecraft 26.2 Permission.HasCommandLevel without changing rename semantics.
replace_count(
    "import net.minecraft.commands.Commands.literal\n",
    "import net.minecraft.commands.Commands.literal\nimport net.minecraft.server.permissions.Permission\nimport net.minecraft.server.permissions.PermissionLevel\n",
)
replace_count(
    ".requires{ it.hasPermission(VSGameConfig.SERVER.Commands.renameShipCommandPerms)}",
    ".requires{ it.permissions().hasPermission(Permission.HasCommandLevel(PermissionLevel.byId(VSGameConfig.SERVER.Commands.renameShipCommandPerms)))}",
)

path.write_text(text, encoding="utf-8")
print("P1_RENAME_PERMISSION_26_2_OVERLAY_APPLIED")
