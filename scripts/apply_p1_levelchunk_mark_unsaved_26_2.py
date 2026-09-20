#!/usr/bin/env python3
"""Adapt only MixinLevelChunk's dirty-save marking to Minecraft 26.2.

Pinned upstream VS2 marks the target LevelChunk dirty after clearChunk() and after
copyChunkFromOtherDimension() by assigning ChunkAccess.unsaved = true. Minecraft 26.2 makes
that field private and exposes ChunkAccess.markUnsaved(), whose implementation performs the
same state transition.

This fail-closed overlay changes only those two post-operation dirty marks. It preserves block
entity clearing, tick-container unregister/register ordering, section/heightmap work, light
state, copy/deserialization flow, structure data, blending data, and ship chunk lifecycle.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/world/chunk/MixinLevelChunk.java"
if not path.is_file():
    raise SystemExit(f"fail-closed: expected pinned VS2 MixinLevelChunk source missing: {path}")

text = path.read_text(encoding="utf-8")
old = "this.unsaved = true;"
new = "this.markUnsaved();"

if text.count(old) != 2:
    raise SystemExit(f"fail-closed: expected exactly two LevelChunk unsaved assignments, found {text.count(old)}")
if text.count(new) != 0:
    raise SystemExit("fail-closed: LevelChunk markUnsaved adaptation already present")
if "setUnsaved(" in text:
    raise SystemExit("fail-closed: forbidden obsolete setUnsaved hypothesis present")

anchors = {
    "public void clearChunk() {": 1,
    "public void copyChunkFromOtherDimension(@NotNull final VSLevelChunk srcChunkVS) {": 1,
    "unregisterTickContainerFromLevel((ServerLevel) level);": 2,
    "this.setLightCorrect(false);": 2,
    "registerTickContainerInLevel((ServerLevel) level);": 2,
    "registerTickContainerInLevel((ServerLevel) level);\n        this.unsaved = true;": 1,
    "registerTickContainerInLevel((ServerLevel) level);\n\n        this.unsaved = true;": 1,
}
for anchor, expected in anchors.items():
    actual = text.count(anchor)
    if actual != expected:
        raise SystemExit(f"fail-closed: preserved LevelChunk dirty/lifecycle anchor {anchor!r} count={actual} expected={expected}")

text = text.replace(old, new)

if old in text:
    raise SystemExit("fail-closed: direct private ChunkAccess.unsaved assignment remains")
if text.count(new) != 2:
    raise SystemExit(f"fail-closed: expected two markUnsaved calls after adaptation, found {text.count(new)}")
if "setUnsaved(" in text:
    raise SystemExit("fail-closed: forbidden obsolete setUnsaved hypothesis introduced")

post_anchors = {
    "public void clearChunk() {": 1,
    "public void copyChunkFromOtherDimension(@NotNull final VSLevelChunk srcChunkVS) {": 1,
    "unregisterTickContainerFromLevel((ServerLevel) level);": 2,
    "this.setLightCorrect(false);": 2,
    "registerTickContainerInLevel((ServerLevel) level);": 2,
    "registerTickContainerInLevel((ServerLevel) level);\n        this.markUnsaved();": 1,
    "registerTickContainerInLevel((ServerLevel) level);\n\n        this.markUnsaved();": 1,
}
for anchor, expected in post_anchors.items():
    actual = text.count(anchor)
    if actual != expected:
        raise SystemExit(f"fail-closed: LevelChunk dirty/lifecycle anchor changed after adaptation: {anchor!r} count={actual} expected={expected}")

path.write_text(text, encoding="utf-8")
print("P1_LEVELCHUNK_MARK_UNSAVED_26_2_OVERLAY_APPLIED")
