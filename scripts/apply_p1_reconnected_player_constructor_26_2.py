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
    "public MixinServerPlayer(final Level level, final BlockPos blockPos, final float f,",
    "final GameProfile gameProfile) {",
    'throw new IllegalStateException("Unreachable");',
    '@Inject(method = "readAdditionalSaveData", at = @At("RETURN"))',
    '@Inject(method = "addAdditionalSaveData", at = @At("RETURN"))',
    "VSGameUtilsKt.getShipObjectWorld(serverLevel()).getAllShips().getById(lastShipId)",
    "ship.getShipToWorld().transformPosition(playerShipPosition)",
    "ship.getWorldToShip().transformPosition(playerWorldPosition)",
]
for anchor in anchors:
    if text.count(anchor) != 1:
        raise SystemExit(f"expected exactly one reconnect-player authority anchor {anchor!r} in {path}, found {text.count(anchor)}")

text = text.replace(old, new, 1)

if text.count(new) != 1 or old in text:
    raise SystemExit("fail-closed: reconnect-player constructor replacement did not converge exactly once")
for anchor in anchors:
    if text.count(anchor) != 1:
        raise SystemExit(f"fail-closed: reconnect-player authority anchor changed unexpectedly: {anchor!r}")

path.write_text(text, encoding="utf-8")
print("P1_RECONNECTED_PLAYER_CONSTRUCTOR_26_2_OVERLAY_APPLIED")
