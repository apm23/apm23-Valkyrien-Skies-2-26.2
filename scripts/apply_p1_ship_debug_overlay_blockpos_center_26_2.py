#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/feature/ship_debug_overlay/MixinDebugScreenOverlay.java"
text = path.read_text(encoding="utf-8")

old = "VSGameUtilsKt.toWorldCoordinates(ship, blockPos.getCenter())"
new = "VSGameUtilsKt.toWorldCoordinates(ship, Vec3.atCenterOf(blockPos))"

if text.count(old) != 1:
    raise SystemExit(f"expected exactly one pinned ship-debug-overlay center expression in {path}, found {text.count(old)}")
if new in text:
    raise SystemExit(f"ship-debug-overlay center expression is already adapted in {path}")

anchors = [
    "VSGameUtilsKt.getShipManagingPos(l, blockPos)",
    "VSGameUtilsKt.getLoadedShipManagingPos((ServerLevel) l, blockPos)",
    "ship.getTransform().getShipToWorldScaling()",
    "ship.getVelocity()",
    "ship.getOmega()",
]
for anchor in anchors:
    if text.count(anchor) != 1:
        raise SystemExit(f"expected exactly one authority anchor {anchor!r} in {path}, found {text.count(anchor)}")

text = text.replace(old, new, 1)

if text.count(new) != 1 or old in text:
    raise SystemExit("fail-closed: ship-debug-overlay center replacement did not converge exactly once")
for anchor in anchors:
    if text.count(anchor) != 1:
        raise SystemExit(f"fail-closed: authority anchor changed unexpectedly: {anchor!r}")

path.write_text(text, encoding="utf-8")
print("P1_SHIP_DEBUG_OVERLAY_BLOCKPOS_CENTER_26_2_OVERLAY_APPLIED")
