#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/feature/clip_replace/MixinBlockGetter.java"
text = path.read_text(encoding="utf-8")

old_expr = "Direction.getNearest(vec3.x, vec3.y, vec3.z)"
new_expr = "Direction.getApproximateNearest(vec3.x, vec3.y, vec3.z)"

if text.count(old_expr) != 1:
    raise SystemExit(f"expected exactly one pinned clip-replace Direction triple-double expression in {path}, found {text.count(old_expr)}")
if new_expr in text:
    raise SystemExit(f"refusing already-adapted/non-baseline Direction expression in {path}")

# Freeze the surrounding real VS2 clip/reference-space authorities before touching vocabulary.
if text.count("VSGameUtilsKt.getShipManagingPos(") != 2:
    raise SystemExit("fail-closed: existing ship-managing-position authority count changed")
if text.count("RaycastUtilsKt.clipIncludeShipsImpl(") != 1:
    raise SystemExit("fail-closed: existing VS2 include-ships raycast authority changed")
if text.count("clipContext.getFrom().subtract(clipContext.getTo())") != 1:
    raise SystemExit("fail-closed: existing miss-direction vector construction changed")
if text.count("BlockHitResult.miss(") != 1:
    raise SystemExit("fail-closed: existing miss-result construction changed")
if text.count("BlockPos.containing(clipContext.getTo())") != 1:
    raise SystemExit("fail-closed: existing miss BlockPos construction changed")

text = text.replace(old_expr, new_expr, 1)

if old_expr in text:
    raise SystemExit("fail-closed: old Direction triple-double vocabulary remains")
if text.count(new_expr) != 1:
    raise SystemExit("fail-closed: adapted Direction expression count mismatch")
if text.count("VSGameUtilsKt.getShipManagingPos(") != 2:
    raise SystemExit("fail-closed: ship-managing-position authority changed after adaptation")
if text.count("RaycastUtilsKt.clipIncludeShipsImpl(") != 1:
    raise SystemExit("fail-closed: VS2 include-ships raycast authority changed after adaptation")

path.write_text(text, encoding="utf-8")
print("P1_CLIP_REPLACE_DIRECTION_26_2_OVERLAY_APPLIED")
