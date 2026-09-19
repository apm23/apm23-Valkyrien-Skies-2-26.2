#!/usr/bin/env python3
"""Apply the isolated Minecraft 26.2 BlockGetter lower-bound API adaptation.

The pinned VS2 MassDatapackResolver dummy BlockGetter overrides the legacy
getMinBuildHeight() method. Minecraft 26.2 requires getMinY(). This overlay
renames only that exact override and preserves the dummy world's return value
and all surrounding datapack/collision-map semantics.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
rel = "common/src/main/kotlin/org/valkyrienskies/mod/common/config/MassDatapackResolver.kt"
path = root / rel
text = path.read_text(encoding="utf-8")

old = "override fun getMinBuildHeight(): Int = 0"
new = "override fun getMinY(): Int = 0"
count = text.count(old)
if count != 1:
    raise SystemExit(f"expected exactly one pinned MassDatapackResolver getMinBuildHeight override in {rel}, found {count}")
if text.count(new) != 0:
    raise SystemExit(f"expected MassDatapackResolver getMinY override to be absent before overlay in {rel}")

text = text.replace(old, new, 1)
path.write_text(text, encoding="utf-8")
print("P1_MASSDATAPACKRESOLVER_MINY_26_2_OVERLAY_APPLIED")
