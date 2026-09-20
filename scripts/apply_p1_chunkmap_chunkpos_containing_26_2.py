#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/server/world/MixinChunkMap.java"
text = path.read_text(encoding="utf-8")

old_a = "new ChunkPos(BlockPos.containing(VSGameUtilsKt.toWorldCoordinates(level, arg.getMiddleBlockPosition(63))))"
new_a = "ChunkPos.containing(BlockPos.containing(VSGameUtilsKt.toWorldCoordinates(level, arg.getMiddleBlockPosition(63))))"
old_b = "new ChunkPos(BlockPos.containing(VSGameUtilsKt.toWorldCoordinates(level, d0.getMiddleBlockPosition(63))))"
new_b = "ChunkPos.containing(BlockPos.containing(VSGameUtilsKt.toWorldCoordinates(level, d0.getMiddleBlockPosition(63))))"

for old, new, label in [(old_a, new_a, "nearby"), (old_b, new_b, "distance")]:
    if text.count(old) != 1:
        raise SystemExit(f"fail-closed: expected exactly one legacy {label} ChunkPos(BlockPos) conversion in {path}, found {text.count(old)}")
    if new in text:
        raise SystemExit(f"fail-closed: {label} ChunkPos conversion already adapted before this helper")

# Preserve the upstream VS2 world-space conversion and wrapped vanilla call semantics exactly.
anchors = [
    ('@WrapOperation(method = "anyPlayerCloseEnoughForSpawning"', 1),
    ('@WrapOperation(method = "playerIsCloseEnoughForSpawning"', 1),
    ("VSGameUtilsKt.toWorldCoordinates(level, arg.getMiddleBlockPosition(63))", 1),
    ("VSGameUtilsKt.toWorldCoordinates(level, d0.getMiddleBlockPosition(63))", 1),
    ("return original.call(instance,", 1),
    ("return original.call(", 2),
    ("VSGameUtilsKt.getShipObjectWorld(level)", 1),
]
for token, expected in anchors:
    actual = text.count(token)
    if actual != expected:
        raise SystemExit(f"fail-closed: expected {expected} authority anchor(s) {token!r} in {path}, found {actual}")

text = text.replace(old_a, new_a, 1).replace(old_b, new_b, 1)

for old in (old_a, old_b):
    if old in text:
        raise SystemExit("fail-closed: legacy ChunkPos(BlockPos) conversion remains")
for new in (new_a, new_b):
    if text.count(new) != 1:
        raise SystemExit("fail-closed: ChunkPos.containing(BlockPos) conversion did not converge exactly once")
for token, expected in anchors:
    if text.count(token) != expected:
        raise SystemExit(f"fail-closed: authority anchor changed unexpectedly: {token!r}")

path.write_text(text, encoding="utf-8")
print("P1_CHUNKMAP_CHUNKPOS_CONTAINING_26_2_OVERLAY_APPLIED count=2")
