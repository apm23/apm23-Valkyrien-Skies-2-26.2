#!/usr/bin/env python3
"""Adapt only pinned VS2 OptiFine-compat section bounds to Minecraft 26.2.

Pinned 1.21.1 Level#getMaxSection() is an exclusive upper bound. Minecraft 26.2
Level#getMaxSectionY() is the inclusive maximum section Y. Preserve the exact upstream
F3+A ship-chunk refresh coverage while changing only the section-height vocabulary:

    y = getMinSection(); y < getMaxSection()
becomes
    y = getMinSectionY(); y <= getMaxSectionY()

The separate removed ViewArea#setDirty authority remains intentionally untouched here so
it can be adapted/proven as its own root hypothesis after this vocabulary unit.
"""
from pathlib import Path
import subprocess, sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/optifine_vanilla/MixinLevelRenderer.java"
if not path.is_file():
    raise SystemExit(f"fail-closed: pinned OptiFine compat renderer source missing: {path}")

text = path.read_text(encoding="utf-8")
old_loop = "for (int y = level.getMinSection(); y < level.getMaxSection(); y++) {"
new_loop = "for (int y = level.getMinSectionY(); y <= level.getMaxSectionY(); y++) {"

# Preserve the exact upstream optional-compat behavior around the accessor-only edit.
anchors = {
    "@Mixin(LevelRenderer.class)": 1,
    '@Inject(\n        method = "allChanged",': 1,
    "if (!(this.level.getChunkSource() instanceof final ClientChunkCacheDuck chunks)) return;": 1,
    "chunks.vs$getShipChunks().forEach((pos, chunk) -> {": 1,
    "viewArea.setDirty(ChunkPos.getX(pos), y, ChunkPos.getZ(pos), false);": 1,
}
for anchor, expected in anchors.items():
    count = text.count(anchor)
    if count != expected:
        raise SystemExit(
            f"fail-closed: OptiFine refresh semantic anchor changed: {anchor!r} count={count} expected={expected}"
        )

if text.count(old_loop) != 1:
    raise SystemExit(f"fail-closed: expected one legacy OptiFine section loop, found {text.count(old_loop)}")
if text.count("level.getMinSection()") != 1 or text.count("level.getMaxSection()") != 1:
    raise SystemExit("fail-closed: OptiFine legacy section accessor count changed outside the proven loop")
if "level.getMinSectionY()" in text or "level.getMaxSectionY()" in text:
    raise SystemExit("fail-closed: OptiFine section-range adaptation already partially present")

new_text = text.replace(old_loop, new_loop, 1)

if old_loop in new_text or "level.getMinSection()" in new_text or "level.getMaxSection()" in new_text:
    raise SystemExit("fail-closed: legacy OptiFine section range remains after adaptation")
if new_text.count("level.getMinSectionY()") != 1 or new_text.count("level.getMaxSectionY()") != 1:
    raise SystemExit("fail-closed: OptiFine 26.2 section accessors did not converge exactly once")
if new_text.count(new_loop) != 1:
    raise SystemExit("fail-closed: OptiFine inclusive section loop did not converge exactly once")
for anchor, expected in anchors.items():
    count = new_text.count(anchor)
    if count != expected:
        raise SystemExit(
            f"fail-closed: OptiFine refresh semantic anchor changed after section adaptation: {anchor!r} count={count} expected={expected}"
        )

path.write_text(new_text, encoding="utf-8")
print("P1_OPTIFINE_LEVELRENDERER_SECTION_RANGE_26_2_OVERLAY_APPLIED loop=exclusive-to-inclusive min_sites=1 max_sites=1 dirty_authority=untouched")

# Dirty authority is a separate compile unit. Run it only after the section-range transform
# so each hypothesis remains independently fail-closed and the already-proven range stays frozen.
dirty_helper = Path(__file__).with_name("apply_p1_optifine_levelrenderer_dirty_authority_26_2.py")
if not dirty_helper.is_file():
    raise SystemExit(f"fail-closed: required OptiFine dirty-authority helper missing: {dirty_helper}")
subprocess.run([sys.executable, str(dirty_helper), str(root)], check=True)
print("P1_OPTIFINE_LEVELRENDERER_DIRTY_AUTHORITY_26_2_CHAINED")
