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

old = "registerTickContainerInLevel((ServerLevel) level);\n        this.unsaved = true;"
new = "registerTickContainerInLevel((ServerLevel) level);\n        this.markUnsaved();"

if text.count(old) != 2:
    raise SystemExit(f"fail-closed: expected two LevelChunk post-register unsaved marks, found {text.count(old)}")
if text.count("this.markUnsaved();") != 0:
    raise SystemExit("fail-closed: LevelChunk markUnsaved adaptation already present")
if "setUnsaved(" in text:
    raise SystemExit("fail-closed: forbidden obsolete setUnsaved hypothesis present")

anchors = {
    "public void clearChunk() {": 1,
    "public void copyChunkFromOtherDimension(@NotNull final VSLevelChunk srcChunkVS) {": 1,
    "unregisterTickContainerFromLevel((ServerLevel) level);": 2,
    "this.setLightCorrect(false);": 2,
    "registerTickContainerInLevel((ServerLevel) level);": 2,
}
for anchor, expected in anchors.items():
    actual = text.count(anchor)
    if actual != expected:
        raise SystemExit(f"fail-closed: preserved LevelChunk lifecycle anchor {anchor!r} count={actual} expected={expected}")

text = text.replace(old, new)

if "this.unsaved = true;" in text:
    raise SystemExit("fail-closed: direct private ChunkAccess.unsaved assignment remains")
if text.count("this.markUnsaved();") != 2:
    raise SystemExit(f"fail-closed: expected two markUnsaved calls after adaptation, found {text.count('this.markUnsaved();')}")
if "setUnsaved(" in text:
    raise SystemExit("fail-closed: forbidden obsolete setUnsaved hypothesis introduced")
for anchor, expected in anchors.items():
    actual = text.count(anchor)
    if actual != expected:
        raise SystemExit(f"fail-closed: LevelChunk lifecycle anchor changed after dirty-mark adaptation: {anchor!r} count={actual} expected={expected}")

path.write_text(text, encoding="utf-8")
print("P1_LEVELCHUNK_MARK_UNSAVED_26_2_OVERLAY_APPLIED")
