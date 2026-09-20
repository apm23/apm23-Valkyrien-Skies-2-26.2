#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/feature/teleport_reconnected_player_to_ship/MixinServerPlayer.java"
text = path.read_text(encoding="utf-8")

old = "super(level, blockPos, f, gameProfile);"
new = "super(level, gameProfile);"

if text.count(old) != 1:
    raise SystemExit(f"expected exactly one pinned legacy Player constructor call in {path}, found {text.count(old)}")
if new in text:
    raise SystemExit(f"Player constructor call is already adapted in {path}")

# This mixin constructor is deliberately unreachable; preserve the injected VS2 reconnect
# ship save/restore authority exactly and adapt only the Minecraft 26.2 superclass vocabulary.
anchors = [
    ("public MixinServerPlayer(final Level level, final BlockPos blockPos, final float f,", 1),
    ("final GameProfile gameProfile) {", 1),
    ('throw new IllegalStateException("Unreachable");', 1),
    ('@Inject(method = "readAdditionalSaveData", at = @At("RETURN"))', 1),
    ('@Inject(method = "addAdditionalSaveData", at = @At("RETURN"))', 1),
    ("VSGameUtilsKt.getShipObjectWorld(serverLevel()).getAllShips().getById(lastShipId)", 2),
    ("ship.getShipToWorld().transformPosition(playerShipPosition)", 1),
    ("ship.getWorldToShip().transformPosition(playerWorldPosition)", 1),
]
for anchor, expected in anchors:
    actual = text.count(anchor)
    if actual != expected:
        raise SystemExit(f"expected {expected} reconnect-player authority anchor(s) {anchor!r} in {path}, found {actual}")

text = text.replace(old, new, 1)

if text.count(new) != 1 or old in text:
    raise SystemExit("fail-closed: reconnect-player constructor replacement did not converge exactly once")
for anchor, expected in anchors:
    if text.count(anchor) != expected:
        raise SystemExit(f"fail-closed: reconnect-player authority anchor changed unexpectedly: {anchor!r}")

path.write_text(text, encoding="utf-8")
print("P1_RECONNECTED_PLAYER_CONSTRUCTOR_26_2_OVERLAY_APPLIED")
