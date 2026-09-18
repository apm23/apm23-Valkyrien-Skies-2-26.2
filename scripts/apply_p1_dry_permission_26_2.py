#!/usr/bin/env python3
"""Apply the isolated Minecraft 26.2 DryCommand permission adaptation.

Exact P1 run 35357765377 proved GetGravityCommand clean and reports exactly one
compile error in DryCommand.kt: the removed CommandSourceStack.hasPermission(Int)
API. This fail-closed overlay changes only that permission predicate and imports;
VS2 ship iteration, liquid handling, messages, and runtime architecture stay intact.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
rel = "common/src/main/kotlin/org/valkyrienskies/mod/common/command/commands/DryCommand.kt"
path = root / rel
text = path.read_text(encoding="utf-8")


def replace_count(old: str, new: str, expected: int = 1) -> None:
    global text
    count = text.count(old)
    if count != expected:
        raise SystemExit(f"expected {expected} matches in {rel}: {old!r}; found {count}")
    text = text.replace(old, new)


# Pinned baseline f39132148e... and current 1.21.1/main are byte-identical at
# blob 89439156f2eb6a1f20e017c4d46722bf46d40c2f. dryShipCommandPerms is explicitly
# constrained to 0..4 and defaults to 2. Preserve that threshold via Minecraft
# 26.2 Permission.HasCommandLevel without changing dryShip behavior.
replace_count(
    "import net.minecraft.network.chat.Component\n",
    "import net.minecraft.network.chat.Component\nimport net.minecraft.server.permissions.Permission\nimport net.minecraft.server.permissions.PermissionLevel\n",
)
replace_count(
    ".requires{ it.hasPermission(VSGameConfig.SERVER.Commands.dryShipCommandPerms)}",
    ".requires{ it.permissions().hasPermission(Permission.HasCommandLevel(PermissionLevel.byId(VSGameConfig.SERVER.Commands.dryShipCommandPerms)))}",
)

path.write_text(text, encoding="utf-8")
print("P1_DRY_PERMISSION_26_2_OVERLAY_APPLIED")
