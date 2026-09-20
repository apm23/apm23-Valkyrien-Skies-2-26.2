#!/usr/bin/env python3
from pathlib import Path
import subprocess
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

# Transport-only chaining for the separately proven pathfinding debug lifecycle adaptation.
# This does not alter or reopen the frozen ship-debug source patch above. The helper itself
# is fail-closed against the exact pinned upstream pathfinding mixin and delegates rendering
# to Minecraft 26.2's vanilla SimpleDebugRenderer/DebugValueAccess/gizmo lifecycle.
helper = Path(__file__).with_name("apply_p1_pathfinding_debug_lifecycle_26_2.py")
if not helper.is_file():
    raise SystemExit(f"fail-closed: required pathfinding debug overlay helper missing: {helper}")
subprocess.run([sys.executable, str(helper), str(root)], check=True)

# Transport-only chaining for the separately proven LevelRenderer/GameRenderer/LevelExtractor
# 26.2 split. The helper preserves the upstream VS camera-transform observation and block-damage
# distance behavior at their exact current vanilla owners; it adds no camera or render authority.
level_helper = Path(__file__).with_name("apply_p1_levelrenderer_split_26_2.py")
if not level_helper.is_file():
    raise SystemExit(f"fail-closed: required LevelRenderer split overlay helper missing: {level_helper}")
subprocess.run([sys.executable, str(level_helper), str(root)], check=True)

# Transport-only chaining for the separately proven ship debug bounding-box gizmo adaptation.
# The helper preserves the original VS2 ship render transform and hitbox gate, while delegating
# debug primitive emission to Minecraft 26.2's vanilla Gizmos API inside DebugRenderer.emitGizmos.
bb_helper = Path(__file__).with_name("apply_p1_ship_debug_bb_gizmo_26_2.py")
if not bb_helper.is_file():
    raise SystemExit(f"fail-closed: required ship debug BB gizmo overlay helper missing: {bb_helper}")
subprocess.run([sys.executable, str(bb_helper), str(root)], check=True)
