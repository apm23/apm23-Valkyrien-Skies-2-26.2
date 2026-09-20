#!/usr/bin/env python3
"""Adapt only MixinClientLevel's canonical standing-width lookup to Minecraft 26.2.

Pinned VS2 computes particle-range scale as current player bounding-box width divided by
Player.STANDING_DIMENSIONS.width(). Minecraft 26.2 moved STANDING_DIMENSIONS to Avatar as
protected state, while Avatar.getDefaultDimensions(Pose) is public and returns
POSES.getOrDefault(pose, STANDING_DIMENSIONS). Therefore getDefaultDimensions(Pose.STANDING)
exposes the same unscaled standing EntityDimensions without switching to the scale-aware
LivingEntity.getDimensions(Pose) path.

This overlay changes only the denominator access vocabulary. It preserves the current
getBbWidth() numerator, creative barrier behavior, ship intersection, world-to-ship
transforms, particle probabilities/ranges, and all VS2 renderer/physics authority.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/client/world/MixinClientLevel.java"
if not path.is_file():
    raise SystemExit(f"fail-closed: expected pinned VS2 MixinClientLevel source missing: {path}")

text = path.read_text(encoding="utf-8")

import_anchor = "import net.minecraft.util.RandomSource;\n"
pose_import = "import net.minecraft.world.entity.Pose;\n"
old = "final double playerScale = player.getBbWidth() / Player.STANDING_DIMENSIONS.width();"
new = "final double playerScale = player.getBbWidth() / player.getDefaultDimensions(Pose.STANDING).width();"

if text.count(import_anchor) != 1:
    raise SystemExit(f"fail-closed: expected one RandomSource import anchor, found {text.count(import_anchor)}")
if pose_import in text:
    raise SystemExit("fail-closed: Pose import already present before standing-width adaptation")
if text.count(old) != 1:
    raise SystemExit(f"fail-closed: expected one pinned standing-width formula, found {text.count(old)}")
if "player.getDefaultDimensions(Pose.STANDING).width()" in text:
    raise SystemExit("fail-closed: standing-width adaptation already partially present")

# The separately proven hand adaptation must already be present in the canonical chain.
hand_anchors = {
    "this.minecraft.player.getMainHandItem().getItem() == Blocks.BARRIER.asItem()": 1,
    "this.minecraft.player.getOffhandItem().getItem() == Blocks.BARRIER.asItem()": 1,
}
for anchor, expected in hand_anchors.items():
    actual = text.count(anchor)
    if actual != expected:
        raise SystemExit(f"fail-closed: frozen hand adaptation anchor {anchor!r} count={actual} expected={expected}")
if "getHandSlots()" in text:
    raise SystemExit("fail-closed: legacy getHandSlots reappeared before standing-width adaptation")

# Guard the surrounding real-VS2 particle/reference-space algorithm.
anchors = {
    "final double playerScale = player.getBbWidth() / Player.STANDING_DIMENSIONS.width();": 1,
    "final AABBdc shipIntersectBB = AABBdUtilKt.expand(new AABBd(playerCenterBB), 32.0);": 1,
    "final double biggerBBProbability = 668.0 / (32.0 * 32.0 * 32.0);": 1,
    "final double smallerBBProbability = 668.0 / (16.0 * 16.0 * 16.0);": 1,
    "for (final Ship ship : VSGameUtilsKt.getShipsIntersecting(ClientLevel.class.cast(this), shipIntersectBB)) {": 1,
    "final AABBdc biggerBB = AABBdUtilKt.expand(temp6.set(playerCenterBB), 32.0 * playerScale);": 1,
    "final AABBdc smallerBB = AABBdUtilKt.expand(temp7.set(playerCenterBB), 16.0 * playerScale);": 1,
    "biggerBB.transform(ship.getWorldToShip(), temp0)": 1,
    "smallerBB.transform(ship.getWorldToShip(), temp2)": 1,
    "if (holdingBarrierItem && blockState.is(Blocks.BARRIER)) {": 1,
}
for anchor, expected in anchors.items():
    actual = text.count(anchor)
    if actual != expected:
        raise SystemExit(f"fail-closed: preserved MixinClientLevel scale/particle anchor {anchor!r} count={actual} expected={expected}")

text = text.replace(import_anchor, import_anchor + pose_import, 1)
text = text.replace(old, new, 1)

if "Player.STANDING_DIMENSIONS" in text:
    raise SystemExit("fail-closed: protected standing-dimensions access remains")
if text.count(pose_import) != 1:
    raise SystemExit(f"fail-closed: expected one Pose import after adaptation, found {text.count(pose_import)}")
if text.count(new) != 1:
    raise SystemExit(f"fail-closed: expected one public default-standing formula after adaptation, found {text.count(new)}")
# Explicitly forbid accidentally switching to the current/scale-aware dimensions getter.
if "player.getDimensions(Pose.STANDING)" in text:
    raise SystemExit("fail-closed: scale-aware getDimensions(Pose.STANDING) substitution is forbidden")

for anchor, expected in hand_anchors.items():
    actual = text.count(anchor)
    if actual != expected:
        raise SystemExit(f"fail-closed: frozen hand adaptation changed: {anchor!r} count={actual} expected={expected}")
for anchor, expected in anchors.items():
    if anchor == old:
        continue
    actual = text.count(anchor)
    if actual != expected:
        raise SystemExit(f"fail-closed: MixinClientLevel particle/reference-space anchor changed after adaptation: {anchor!r} count={actual} expected={expected}")

path.write_text(text, encoding="utf-8")
print("P1_CLIENTLEVEL_STANDING_DIMENSIONS_26_2_OVERLAY_APPLIED")
