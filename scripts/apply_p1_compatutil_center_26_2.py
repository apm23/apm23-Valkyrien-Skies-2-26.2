#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/kotlin/org/valkyrienskies/mod/common/CompatUtil.kt"
text = path.read_text(encoding="utf-8")

replacements = [
    (
        "level.getHeightmapPos(types, pos).center",
        "Vec3.atCenterOf(level.getHeightmapPos(types, pos))",
    ),
    (
        "val end = worldHeight.center",
        "val end = Vec3.atCenterOf(worldHeight)",
    ),
    (
        "ship.shipToWorld.transformPosition(pos.center)",
        "ship.shipToWorld.transformPosition(Vec3.atCenterOf(pos))",
    ),
]

for old, new in replacements:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"expected exactly one pinned CompatUtil expression {old!r} in {path}, found {count}")
    text = text.replace(old, new, 1)

path.write_text(text, encoding="utf-8")
print("P1_COMPATUTIL_CENTER_26_2_OVERLAY_APPLIED")
