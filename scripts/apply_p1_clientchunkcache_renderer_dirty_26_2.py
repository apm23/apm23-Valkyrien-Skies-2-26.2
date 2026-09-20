#!/usr/bin/env python3
"""Bridge pinned VS2 ship RenderSection dirty invalidation into Minecraft 26.2 authority.

Pinned VS2 directly marked the existing custom ship RenderSection dirty with boolean true.
Minecraft 26.2 moved dirty state out of RenderSection into LevelExtractor -> SectionUpdateTracker.
The public 3-int LevelExtractor entrypoint hardcodes false, so preserving the pinned boolean
requires a minimal Mixin @Invoker to the exact private 4-arg method.

This overlay does NOT create new renderer authority. It keeps the upstream VS2 custom ship
ViewArea lookup/null guard, exact dx/dz/sy coordinates, renderer selection, relight and
onChunkLoaded ordering; it only forwards that existing invalidation into the 26.2 tracker.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
source = root / "common/src/main/java/org/valkyrienskies/mod/mixin/client/world/MixinClientChunkCache.java"
invoker = root / "common/src/main/java/org/valkyrienskies/mod/mixin/accessors/client/render/LevelExtractorInvoker.java"
mixins = root / "common/src/main/resources/valkyrienskies-common.mixins.json"

for path in (source, mixins):
    if not path.is_file():
        raise SystemExit(f"fail-closed: required pinned VS2 file missing: {path}")
if invoker.exists():
    raise SystemExit(f"fail-closed: LevelExtractor invoker already exists before overlay: {invoker}")

text = source.read_text(encoding="utf-8")
mixin_text = mixins.read_text(encoding="utf-8")

old_import = "import org.valkyrienskies.mod.mixin.accessors.client.render.LevelRendererAccessor;\n"
new_import = old_import + "import org.valkyrienskies.mod.mixin.accessors.client.render.LevelExtractorInvoker;\n"
old_call = "                                    renderSection.setDirty(true);"
new_call = (
    "                                    ((LevelExtractorInvoker) Minecraft.getInstance().levelExtractor)\n"
    "                                        .vs$invokeSetSectionDirty(x + dx, sy, z + dz, true);"
)
config_anchor = '    "accessors.client.render.LevelRendererAccessor",\n'
config_entry = '    "accessors.client.render.LevelExtractorInvoker",\n'

# Require all earlier frozen ClientChunkCache adaptations and the exact pinned renderer boundary.
required_source = {
    "import net.minecraft.client.Minecraft;": 1,
    old_import.strip(): 1,
    "for (int sy = level.getMinSectionY(); sy <= level.getMaxSectionY(); sy++) {": 1,
    "final SectionRenderDispatcher.RenderSection renderSection =": 1,
    "viewArea.vs$getShipRenderSection(x + dx, sy, z + dz);": 1,
    "if (renderSection != null) {": 1,
    old_call.strip(): 1,
    "relightChunk(worldChunk);": 1,
    "this.level.onChunkLoaded(pos);": 1,
    "ValkyrienCommonMixinConfigPlugin.getVSRenderer() != VSRenderer.SODIUM": 3,
    "ValkyrienCommonMixinConfigPlugin.getVSRenderer() == VSRenderer.SODIUM": 1,
}
for anchor, expected in required_source.items():
    count = text.count(anchor)
    if count != expected:
        raise SystemExit(
            f"fail-closed: ClientChunkCache preserved renderer/lifecycle anchor changed: {anchor!r} count={count} expected={expected}"
        )
if "LevelExtractorInvoker" in text or "vs$invokeSetSectionDirty" in text:
    raise SystemExit("fail-closed: renderer dirty bridge already partially present in ClientChunkCache")
if text.count("ChunkPos.pack(") != 6 or "ChunkPos.asLong(" in text:
    raise SystemExit("fail-closed: frozen ClientChunkCache packed-key adaptation missing before dirty bridge")
if text.count("final Map<Heightmap.Types, long[]> heightmaps,") != 1:
    raise SystemExit("fail-closed: frozen ClientChunkCache packet-heightmap adaptation missing before dirty bridge")

if mixin_text.count(config_anchor) != 1:
    raise SystemExit(f"fail-closed: expected one LevelRendererAccessor client config anchor, found {mixin_text.count(config_anchor)}")
if "accessors.client.render.LevelExtractorInvoker" in mixin_text:
    raise SystemExit("fail-closed: LevelExtractor invoker already registered before overlay")

# Compute every output before writing any file.
new_source = text.replace(old_import, new_import, 1).replace(old_call, new_call, 1)
new_mixin_text = mixin_text.replace(config_anchor, config_anchor + config_entry, 1)
invoker_text = """package org.valkyrienskies.mod.mixin.accessors.client.render;

import net.minecraft.client.renderer.extract.LevelExtractor;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.gen.Invoker;

@Mixin(LevelExtractor.class)
public interface LevelExtractorInvoker {

    @Invoker(\"setSectionDirty\")
    void vs$invokeSetSectionDirty(int sectionX, int sectionY, int sectionZ, boolean playerChanged);
}
"""

# Post-transform fail-closed validation.
if old_call in new_source or new_source.count("vs$invokeSetSectionDirty(x + dx, sy, z + dz, true);") != 1:
    raise SystemExit("fail-closed: renderer dirty call did not converge exactly once")
if new_source.count("import org.valkyrienskies.mod.mixin.accessors.client.render.LevelExtractorInvoker;") != 1:
    raise SystemExit("fail-closed: LevelExtractorInvoker import did not converge exactly once")
for anchor, expected in required_source.items():
    if anchor == old_call.strip():
        continue
    count = new_source.count(anchor)
    if count != expected:
        raise SystemExit(
            f"fail-closed: ClientChunkCache renderer/lifecycle anchor changed after dirty bridge: {anchor!r} count={count} expected={expected}"
        )
if new_mixin_text.count("accessors.client.render.LevelExtractorInvoker") != 1:
    raise SystemExit("fail-closed: LevelExtractor invoker config entry did not converge exactly once")
if invoker_text.count('@Invoker("setSectionDirty")') != 1 or invoker_text.count("boolean playerChanged") != 1:
    raise SystemExit("fail-closed: LevelExtractor private-boolean invoker declaration malformed")

source.write_text(new_source, encoding="utf-8")
mixins.write_text(new_mixin_text, encoding="utf-8")
invoker.parent.mkdir(parents=True, exist_ok=True)
invoker.write_text(invoker_text, encoding="utf-8")

print("P1_CLIENTCHUNKCACHE_RENDERER_DIRTY_26_2_OVERLAY_APPLIED authority=LevelExtractor boolean=true sites=1")
