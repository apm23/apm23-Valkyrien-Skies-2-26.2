#!/usr/bin/env python3
"""Adapt pinned VS2 ViewArea dirty ownership to Minecraft 26.2.

Pinned VS2 intercepted ViewArea#setDirty so shipyard RenderSections could keep dirty state
on each RenderSection, and it explicitly marked custom sections dirty after lookup/creation.
Minecraft 26.2 removed both ViewArea#setDirty and RenderSection dirty state. Exact mapped
bytecode proof shows dirty events now enter LevelExtractor, preserving the player/important
bit, then flow through SectionUpdateTracker. Frozen P1 unit #17 already supplies the minimal
LevelExtractorInvoker for the exact private four-argument authority.

Therefore the obsolete ViewArea#setDirty interception is removed rather than recreated, and
the pinned forced-dirty call for custom ship sections is forwarded to that same 26.2
authority. No local dirty set, duplicate renderer authority, or gameplay behavior is added.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/vanilla_renderer/MixinViewAreaVanilla.java"
if not path.is_file():
    raise SystemExit(f"fail-closed: expected transformed VS2 ViewArea source missing: {path}")

text = path.read_text(encoding="utf-8")

# Require the previously frozen ViewArea vocabulary/lifecycle adaptations first.
required = {
    "level.getMinSectionY()": 3,
    "ChunkPos.pack(": 5,
    "level.getMinY()": 1,
    "SectionPos.asLong(chunkX, sectionY, chunkZ)": 1,
    ".reset();": 2,
    "vs$getShipRenderSection": 1,
    "vs$getOrCreateShipRenderSection": 1,
    "arr[yIndex].setDirty(true);": 1,
    '@Inject(method = "setDirty", at = @At("HEAD"), cancellable = true)': 1,
    "renderChunksArray[yIndex].setDirty(important);": 1,
}
for anchor, expected in required.items():
    count = text.count(anchor)
    if count != expected:
        raise SystemExit(
            f"fail-closed: ViewArea dirty/lifecycle anchor changed before authority adaptation: {anchor!r} count={count} expected={expected}"
        )
if "level.getMinSection()" in text or "ChunkPos.asLong(" in text or ".releaseBuffers();" in text:
    raise SystemExit("fail-closed: a frozen ViewArea adaptation regressed before dirty-authority bridge")
if "LevelExtractorInvoker" in text or "vs$invokeSetSectionDirty" in text:
    raise SystemExit("fail-closed: ViewArea LevelExtractor dirty bridge already partially present")

# 26.2 has no ViewArea#setDirty. Remove only the pinned interception block; ordinary dirty
# intent is already owned earlier by LevelExtractor/SectionUpdateTracker.
start_marker = "    /**\n     * This mixin creates render chunks for ship chunks.\n     */\n    @Inject(method = \"setDirty\", at = @At(\"HEAD\"), cancellable = true)\n"
end_marker = "    /**\n     * This mixin allows {@link ViewArea} to return the render chunks for ships.\n     */\n"
if text.count(start_marker) != 1 or text.count(end_marker) != 1:
    raise SystemExit("fail-closed: exact pinned ViewArea setDirty interception boundaries changed")
start = text.index(start_marker)
end = text.index(end_marker, start)
old_block = text[start:end]
if old_block.count("private void preScheduleRebuild") != 1 or old_block.count("callbackInfo.cancel();") != 1:
    raise SystemExit("fail-closed: pinned ViewArea setDirty interception body changed")
text = text[:start] + text[end:]

# Reuse the already-frozen LevelExtractor private-boolean invoker. Do not create a second
# accessor or a second dirty-state authority.
level_renderer_import = "import net.minecraft.client.renderer.LevelRenderer;\n"
minecraft_import = "import net.minecraft.client.Minecraft;\n"
vs_import = "import org.valkyrienskies.mod.mixinducks.client.render.IVSViewAreaMethods;\n"
invoker_import = "import org.valkyrienskies.mod.mixin.accessors.client.render.LevelExtractorInvoker;\n"
if text.count(level_renderer_import) != 1 or text.count(vs_import) != 1:
    raise SystemExit("fail-closed: ViewArea import anchors changed")
if minecraft_import in text or invoker_import in text:
    raise SystemExit("fail-closed: dirty-authority imports already present")
text = text.replace(level_renderer_import, minecraft_import + level_renderer_import, 1)
text = text.replace(vs_import, invoker_import + vs_import, 1)

old_force = "        arr[yIndex].setDirty(true);"
new_force = (
    "        ((LevelExtractorInvoker) Minecraft.getInstance().levelExtractor)\n"
    "            .vs$invokeSetSectionDirty(chunkX, sectionY, chunkZ, true);"
)
if text.count(old_force) != 1:
    raise SystemExit(f"fail-closed: expected one custom-section forced dirty call, found {text.count(old_force)}")
text = text.replace(old_force, new_force, 1)

# Post-transform checks: obsolete authority is gone, forced dirty uses 26.2 authority once,
# and every independently frozen ViewArea lifecycle/vocabulary boundary remains intact.
for forbidden in (
    '@Inject(method = "setDirty"',
    "preScheduleRebuild",
    "renderChunksArray[yIndex].setDirty(important);",
    "arr[yIndex].setDirty(true);",
):
    if forbidden in text:
        raise SystemExit(f"fail-closed: obsolete ViewArea dirty authority remains: {forbidden}")
if text.count("vs$invokeSetSectionDirty(chunkX, sectionY, chunkZ, true);") != 1:
    raise SystemExit("fail-closed: custom-section dirty authority did not converge exactly once")
if text.count(minecraft_import) != 1 or text.count(invoker_import) != 1:
    raise SystemExit("fail-closed: dirty-authority imports did not converge exactly once")
for anchor, expected in (
    ("level.getMinSectionY()", 2),
    ("ChunkPos.pack(", 4),
    ("level.getMinY()", 1),
    ("SectionPos.asLong(chunkX, sectionY, chunkZ)", 1),
    (".reset();", 2),
    ("vs$getShipRenderSection", 1),
    ("vs$getOrCreateShipRenderSection", 1),
):
    count = text.count(anchor)
    if count != expected:
        raise SystemExit(
            f"fail-closed: frozen ViewArea boundary changed after dirty-authority bridge: {anchor!r} count={count} expected={expected}"
        )
if "level.getMinSection()" in text or "ChunkPos.asLong(" in text or ".releaseBuffers();" in text:
    raise SystemExit("fail-closed: frozen ViewArea adaptation regressed after dirty-authority bridge")

path.write_text(text, encoding="utf-8")
print("P1_VIEWAREA_VANILLA_DIRTY_AUTHORITY_26_2_OVERLAY_APPLIED obsolete_setdirty=removed forced_dirty=LevelExtractor:true")
