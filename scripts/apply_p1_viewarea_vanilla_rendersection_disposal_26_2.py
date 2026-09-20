#!/usr/bin/env python3
"""Adapt only pinned VS2 custom RenderSection disposal to Minecraft 26.2.

Exact mapped 26.2 ViewArea#releaseAllBuffers delegates RenderSection teardown to reset().
RenderSection#reset cancels compile work and releases/closes the section mesh and backing
uber-buffer allocations. Preserve custom ship-section ownership, dirty scheduling, and
all creation/lookup ordering.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/vanilla_renderer/MixinViewAreaVanilla.java"
if not path.is_file():
    raise SystemExit(f"fail-closed: expected transformed VS2 ViewArea source missing: {path}")

text = path.read_text(encoding="utf-8")
old = ".releaseBuffers();"
new = ".reset();"
ctor = "vs$sectionRenderDispatcher.new RenderSection(0, SectionPos.asLong(chunkX, sectionY, chunkZ))"

# Require the independently proven constructor unit and all prior ViewArea vocabulary units.
if text.count("import net.minecraft.core.SectionPos;") != 1 or text.count(ctor) != 1:
    raise SystemExit("fail-closed: frozen ViewArea RenderSection constructor unit missing before disposal adaptation")
if text.count("level.getMinSectionY()") != 3 or "level.getMinSection()" in text:
    raise SystemExit("fail-closed: frozen ViewArea section-index unit changed before disposal adaptation")
if text.count("ChunkPos.pack(") != 5 or "ChunkPos.asLong(" in text:
    raise SystemExit("fail-closed: frozen ViewArea packed-key unit changed before disposal adaptation")
if text.count("level.getMinY()") != 1 or "level.getMinBuildHeight()" in text:
    raise SystemExit("fail-closed: frozen ViewArea minY unit changed before disposal adaptation")

# Dirty authority is a separate later unit and must remain exactly untouched here.
anchors = {
    "renderChunksArray[yIndex].setDirty(important);": 1,
    "arr[yIndex].setDirty(true);": 1,
    "@Inject(method = \"releaseAllBuffers\", at = @At(\"HEAD\"))": 1,
    "vs$shipRenderChunks.clear();": 1,
    "vs$getShipRenderSection": 1,
    "vs$getOrCreateShipRenderSection": 1,
}
for anchor, expected in anchors.items():
    count = text.count(anchor)
    if count != expected:
        raise SystemExit(
            f"fail-closed: preserved ViewArea authority/lifecycle anchor changed: {anchor!r} count={count} expected={expected}"
        )

if text.count(old) != 2:
    raise SystemExit(f"fail-closed: expected exactly two legacy RenderSection disposal calls, found {text.count(old)}")
if new in text:
    raise SystemExit("fail-closed: ViewArea RenderSection disposal adaptation already partially present")

new_text = text.replace(old, new)

if old in new_text or new_text.count(new) != 2:
    raise SystemExit("fail-closed: ViewArea RenderSection disposal adaptation did not converge exactly twice")
if new_text.count(ctor) != 1:
    raise SystemExit("fail-closed: frozen ViewArea RenderSection constructor changed during disposal adaptation")
for anchor, expected in anchors.items():
    count = new_text.count(anchor)
    if count != expected:
        raise SystemExit(
            f"fail-closed: ViewArea authority/lifecycle anchor changed after disposal adaptation: {anchor!r} count={count} expected={expected}"
        )

path.write_text(new_text, encoding="utf-8")
print("P1_VIEWAREA_VANILLA_RENDERSECTION_DISPOSAL_26_2_OVERLAY_APPLIED sites=2 method=reset")
