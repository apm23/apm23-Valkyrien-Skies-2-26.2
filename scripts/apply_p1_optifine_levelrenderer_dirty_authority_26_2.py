#!/usr/bin/env python3
"""Bridge pinned VS2 OptiFine-compat refresh dirtying into Minecraft 26.2 authority.

Pinned VS2's OptiFine compatibility mixin refreshes every loaded ship-chunk section on
LevelRenderer.allChanged() by calling ViewArea.setDirty(sectionX, sectionY, sectionZ, false).
Minecraft 26.2 removed ViewArea#setDirty and moved section dirty state to
Minecraft.levelExtractor -> LevelExtractor.setSectionDirty(..., boolean) -> SectionUpdateTracker.

The earlier frozen P1 renderer bridge already introduced and registered LevelExtractorInvoker
for this exact private 4-arg authority. Reuse it here and preserve the pinned boolean false,
ship-chunk iteration, section coverage, and allChanged injection. No renderer state or authority
is duplicated by this overlay.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
source = root / "common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/optifine_vanilla/MixinLevelRenderer.java"
invoker = root / "common/src/main/java/org/valkyrienskies/mod/mixin/accessors/client/render/LevelExtractorInvoker.java"
mixins = root / "common/src/main/resources/valkyrienskies-common.mixins.json"

for path in (source, invoker, mixins):
    if not path.is_file():
        raise SystemExit(f"fail-closed: required transformed VS2 file missing: {path}")

text = source.read_text(encoding="utf-8")
invoker_text = invoker.read_text(encoding="utf-8")
mixin_text = mixins.read_text(encoding="utf-8")

old_import = "import net.minecraft.client.multiplayer.ClientLevel;\n"
new_import = (
    "import net.minecraft.client.Minecraft;\n"
    "import net.minecraft.client.multiplayer.ClientLevel;\n"
)
accessor_import = "import org.valkyrienskies.mod.mixin.accessors.client.render.LevelExtractorInvoker;\n"
old_call = "                viewArea.setDirty(ChunkPos.getX(pos), y, ChunkPos.getZ(pos), false);"
new_call = (
    "                ((LevelExtractorInvoker) Minecraft.getInstance().levelExtractor)\n"
    "                    .vs$invokeSetSectionDirty(ChunkPos.getX(pos), y, ChunkPos.getZ(pos), false);"
)

# Require the exact prior section-range unit plus the original optional-compat refresh semantics.
anchors = {
    "@Mixin(LevelRenderer.class)": 1,
    '@Inject(\n        method = "allChanged",': 1,
    "if (!(this.level.getChunkSource() instanceof final ClientChunkCacheDuck chunks)) return;": 1,
    "chunks.vs$getShipChunks().forEach((pos, chunk) -> {": 1,
    "for (int y = level.getMinSectionY(); y <= level.getMaxSectionY(); y++) {": 1,
    old_call.strip(): 1,
}
for anchor, expected in anchors.items():
    count = text.count(anchor)
    if count != expected:
        raise SystemExit(
            f"fail-closed: OptiFine refresh boundary changed before dirty bridge: {anchor!r} count={count} expected={expected}"
        )
if "level.getMinSection()" in text or "level.getMaxSection()" in text:
    raise SystemExit("fail-closed: frozen OptiFine section-range adaptation regressed")
if "LevelExtractorInvoker" in text or "vs$invokeSetSectionDirty" in text:
    raise SystemExit("fail-closed: OptiFine dirty-authority bridge already partially present")
if text.count(old_import) != 1:
    raise SystemExit(f"fail-closed: expected one ClientLevel import anchor, found {text.count(old_import)}")

# Reuse the exact already-frozen invoker rather than introducing another dirty authority.
for anchor in (
    "package org.valkyrienskies.mod.mixin.accessors.client.render;",
    "@Mixin(LevelExtractor.class)",
    '@Invoker("setSectionDirty")',
    "void vs$invokeSetSectionDirty(int sectionX, int sectionY, int sectionZ, boolean playerChanged);",
):
    if invoker_text.count(anchor) != 1:
        raise SystemExit(f"fail-closed: frozen LevelExtractorInvoker anchor changed: {anchor!r}")
if mixin_text.count('"accessors.client.render.LevelExtractorInvoker"') != 1:
    raise SystemExit("fail-closed: frozen LevelExtractorInvoker mixin registration missing or duplicated")

new_text = text.replace(old_import, new_import, 1)
# Keep imports grouped with the existing VS2 mixin-duck import without broad source reformatting.
duck_import = "import org.valkyrienskies.mod.mixinducks.client.world.ClientChunkCacheDuck;\n"
if new_text.count(duck_import) != 1:
    raise SystemExit("fail-closed: expected one ClientChunkCacheDuck import anchor")
new_text = new_text.replace(duck_import, accessor_import + duck_import, 1)
new_text = new_text.replace(old_call, new_call, 1)

if old_call in new_text:
    raise SystemExit("fail-closed: removed ViewArea#setDirty call remains after OptiFine bridge")
if new_text.count("import net.minecraft.client.Minecraft;") != 1:
    raise SystemExit("fail-closed: Minecraft import did not converge exactly once")
if new_text.count("import org.valkyrienskies.mod.mixin.accessors.client.render.LevelExtractorInvoker;") != 1:
    raise SystemExit("fail-closed: LevelExtractorInvoker import did not converge exactly once")
if new_text.count("vs$invokeSetSectionDirty(ChunkPos.getX(pos), y, ChunkPos.getZ(pos), false);") != 1:
    raise SystemExit("fail-closed: OptiFine false dirty invalidation did not converge exactly once")
for anchor, expected in anchors.items():
    if anchor == old_call.strip():
        continue
    count = new_text.count(anchor)
    if count != expected:
        raise SystemExit(
            f"fail-closed: OptiFine refresh boundary changed after dirty bridge: {anchor!r} count={count} expected={expected}"
        )

source.write_text(new_text, encoding="utf-8")
print("P1_OPTIFINE_LEVELRENDERER_DIRTY_AUTHORITY_26_2_OVERLAY_APPLIED authority=LevelExtractor boolean=false sites=1")
