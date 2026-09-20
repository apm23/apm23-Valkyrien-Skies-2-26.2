#!/usr/bin/env python3
"""Adapt only pinned VS2 ViewArea custom RenderSection construction to Minecraft 26.2.

Exact mapped 26.2 evidence shows RenderSection now takes (index, packedSectionNode), and
vanilla ViewArea packs section coordinates with SectionPos.asLong(sectionX, sectionY,
sectionZ). Preserve all VS2 custom ViewArea ownership, dirty scheduling and disposal.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/vanilla_renderer/MixinViewAreaVanilla.java"
if not path.is_file():
    raise SystemExit(f"fail-closed: expected transformed VS2 ViewArea source missing: {path}")

text = path.read_text(encoding="utf-8")
old = "vs$sectionRenderDispatcher.new RenderSection(0, chunkX << 4, sectionY << 4, chunkZ << 4)"
new = "vs$sectionRenderDispatcher.new RenderSection(0, SectionPos.asLong(chunkX, sectionY, chunkZ))"

# Require all independently frozen ViewArea vocabulary units first.
if text.count("level.getMinSectionY()") != 3 or "level.getMinSection()" in text:
    raise SystemExit("fail-closed: frozen ViewArea section-index unit missing before constructor adaptation")
if text.count("ChunkPos.pack(") != 5 or "ChunkPos.asLong(" in text:
    raise SystemExit("fail-closed: frozen ViewArea packed-key unit missing before constructor adaptation")
if text.count("level.getMinY()") != 1 or "level.getMinBuildHeight()" in text:
    raise SystemExit("fail-closed: frozen ViewArea minY unit missing before constructor adaptation")

# SectionPos is part of pinned upstream source and is the exact 26.2 section-node packer.
if text.count("import net.minecraft.core.SectionPos;") != 1:
    raise SystemExit("fail-closed: expected pinned SectionPos import missing or duplicated")

anchors = {
    "private final Long2ObjectMap<SectionRenderDispatcher.RenderSection[]> vs$shipRenderChunks": 1,
    "renderChunksArray[yIndex].setDirty(important);": 1,
    "arr[yIndex].setDirty(true);": 1,
    ".releaseBuffers();": 2,
    "vs$getShipRenderSection": 1,
    "vs$getOrCreateShipRenderSection": 1,
}
for anchor, expected in anchors.items():
    count = text.count(anchor)
    if count != expected:
        raise SystemExit(
            f"fail-closed: preserved ViewArea lifecycle anchor changed: {anchor!r} count={count} expected={expected}"
        )

if text.count(old) != 1:
    raise SystemExit(f"fail-closed: expected exactly one legacy ViewArea RenderSection constructor, found {text.count(old)}")
if new in text:
    raise SystemExit("fail-closed: ViewArea RenderSection constructor adaptation already partially present")

new_text = text.replace(old, new, 1)

if old in new_text or new_text.count(new) != 1:
    raise SystemExit("fail-closed: ViewArea RenderSection constructor adaptation did not converge exactly once")
for anchor, expected in anchors.items():
    count = new_text.count(anchor)
    if count != expected:
        raise SystemExit(
            f"fail-closed: ViewArea lifecycle anchor changed after constructor adaptation: {anchor!r} count={count} expected={expected}"
        )

path.write_text(new_text, encoding="utf-8")
print("P1_VIEWAREA_VANILLA_RENDERSECTION_CTOR_26_2_OVERLAY_APPLIED sites=1")
