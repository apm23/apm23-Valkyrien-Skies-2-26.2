#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/kotlin/org/valkyrienskies/mod/common/CompatUtil.kt"
text = path.read_text(encoding="utf-8")

import_anchor = "import net.minecraft.world.phys.Vec3\n"
new_import = "import net.minecraft.world.phys.shapes.CollisionContext\n"

anchor_count = text.count(import_anchor)
if anchor_count != 1:
    raise SystemExit(f"expected exactly one CompatUtil Vec3 import anchor in {path}, found {anchor_count}")
if text.count(new_import) != 0:
    raise SystemExit(f"expected CollisionContext import to be absent before overlay in {path}")
text = text.replace(import_anchor, import_anchor + new_import, 1)

old = "null as net.minecraft.world.entity.Entity?"
new = "CollisionContext.empty()"
count = text.count(old)
if count != 2:
    raise SystemExit(f"expected exactly two pinned CompatUtil null Entity ClipContext arguments in {path}, found {count}")
text = text.replace(old, new)

path.write_text(text, encoding="utf-8")
print("P1_COMPATUTIL_COLLISION_CONTEXT_26_2_OVERLAY_APPLIED")
