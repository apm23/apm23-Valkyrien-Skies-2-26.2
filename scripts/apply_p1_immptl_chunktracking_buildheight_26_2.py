#!/usr/bin/env python3
"""Adapt only pinned VS2 Immersive Portals chunk-tracking build-height accessors to MC 26.2.

Pinned VS2 builds an AABB around the Immersive Portals ChunkLoader and expands it over the
full server-level build height before asking real VS2 for intersecting ships. Minecraft 26.2
removed getMinBuildHeight()/getMaxBuildHeight(). Preserve that exact box coverage by mapping
the lower bound to getMinY() and the old exclusive upper bound to getMinY() + getHeight().

This overlay intentionally does not touch ChunkLoader center/dimension access. The existing
`net.minecraft.class_5321` dependency/mapping diagnostic remains a separate root hypothesis.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/immersive_portals/MixinImmPtlChunkTracking.java"
if not path.is_file():
    raise SystemExit(f"fail-closed: pinned Immersive Portals chunk-tracking source missing: {path}")

text = path.read_text(encoding="utf-8")
old_min = "world.getMinBuildHeight()"
old_max = "world.getMaxBuildHeight()"
new_min = "world.getMinY()"
new_max = "world.getMinY() + world.getHeight()"

# Preserve the exact upstream ChunkLoader + VS2 ship-injection semantics around this accessor-only edit.
anchors = {
    "@Mixin(ImmPtlChunkTracking.class)": 1,
    'method = "updateForPlayer"': 1,
    "final ChunkLoader instance, final ChunkPosConsumer func, @Local final ServerLevel world": 1,
    "for (int dx = -instance.radius(); dx <= instance.radius(); dx++) {": 1,
    "for (int dz = -instance.radius(); dz <= instance.radius(); dz++) {": 1,
    "instance.getCenter().dimension": 2,
    "VSGameUtilsKt.getShipsIntersecting(world, box)": 1,
    "ship.getActiveChunksSet().forEach((x, z) -> {": 1,
    "Math.max(Math.abs(dx), Math.abs(dz))": 1,
    "1 // todo: change this?": 1,
}
for anchor, expected in anchors.items():
    count = text.count(anchor)
    if count != expected:
        raise SystemExit(
            f"fail-closed: Immersive Portals chunk-tracking semantic anchor changed: {anchor!r} count={count} expected={expected}"
        )

if text.count(old_min) != 1 or text.count(old_max) != 1:
    raise SystemExit(
        f"fail-closed: expected one pinned ImmPtl build-height pair; min={text.count(old_min)} max={text.count(old_max)}"
    )
if new_max in text or "world.getHeight()" in text:
    raise SystemExit("fail-closed: ImmPtl build-height adaptation already partially present")

new_text = text.replace(old_min, new_min, 1).replace(old_max, new_max, 1)

if old_min in new_text or old_max in new_text:
    raise SystemExit("fail-closed: legacy ImmPtl build-height accessor remains")
# The exclusive max expression contains a second getMinY().
if new_text.count("world.getMinY()") != 2 or new_text.count("world.getHeight()") != 1:
    raise SystemExit("fail-closed: ImmPtl 26.2 build-height vocabulary count mismatch")
for anchor, expected in anchors.items():
    count = new_text.count(anchor)
    if count != expected:
        raise SystemExit(
            f"fail-closed: Immersive Portals chunk-tracking semantic anchor changed after adaptation: {anchor!r} count={count} expected={expected}"
        )

path.write_text(new_text, encoding="utf-8")
print("P1_IMMPTL_CHUNKTRACKING_BUILDHEIGHT_26_2_OVERLAY_APPLIED min=getMinY maxExclusive=getMinY+getHeight class_5321=untouched")
