#!/usr/bin/env python3
"""Isolate the obsolete optional Sodium ChunkTrackerHolder bridge for standalone P1.

Pinned VS2 2.4.12 targets Sodium mc1.21.1-0.6.9 and its SodiumCompat helper directly
calls ChunkTrackerHolder. Under Minecraft 26.2's unobfuscated loom-no-remap compile path,
that old optional jar exposes an intermediary ClientLevel descriptor (class_638), while
current Sodium 0.9.x no longer provides this legacy ChunkTrackerHolder API at all.

Sodium is not part of the locked P1 standalone runtime stack, and the pinned Fabric
Sodium renderer mixin is already excluded from its source set. Keep the two upstream
SodiumCompat call-surface methods so MixinClientChunkCache remains source-traceable, but
make only those optional callbacks inert for P1. Vanilla VS2 chunk ownership, terrain
updates, connectivity, lighting, rendering, ship-space, physics, collision, entity/player
handling, networking, and camera authority are untouched.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/compat/SodiumCompat.java"

if not path.is_file():
    raise SystemExit(f"fail-closed: expected pinned VS2 SodiumCompat source missing: {path}")

text = path.read_text(encoding="utf-8")

imports = (
    "import net.caffeinemc.mods.sodium.client.render.chunk.map.ChunkStatus;\n"
    "import net.caffeinemc.mods.sodium.client.render.chunk.map.ChunkTrackerHolder;\n"
)
plugin_import = "import org.valkyrienskies.mod.mixin.ValkyrienCommonMixinConfigPlugin;\n"
added_old = (
    "        if (ValkyrienCommonMixinConfigPlugin.getVSRenderer() == VSRenderer.SODIUM) {\n"
    "            ChunkTrackerHolder.get(level).onChunkStatusAdded(x, z, ChunkStatus.FLAG_HAS_BLOCK_DATA);\n"
    "        }"
)
removed_old = (
    "        if (ValkyrienCommonMixinConfigPlugin.getVSRenderer() == VSRenderer.SODIUM) {\n"
    "            ChunkTrackerHolder.get(level).onChunkStatusRemoved(x, z, ChunkStatus.FLAG_HAS_BLOCK_DATA);\n"
    "        }"
)

for needle, expected, label in (
    (imports, 1, "legacy Sodium imports"),
    (plugin_import, 1, "legacy Sodium renderer-plugin import"),
    (added_old, 1, "legacy chunk-added callback"),
    (removed_old, 1, "legacy chunk-removed callback"),
    ("public static void onChunkAdded(final ClientLevel level, final int x, final int z)", 1, "onChunkAdded signature"),
    ("public static void onChunkRemoved(final ClientLevel level, final int x, final int z)", 1, "onChunkRemoved signature"),
):
    actual = text.count(needle)
    if actual != expected:
        raise SystemExit(f"fail-closed: {label}: expected {expected}, found {actual}")

# Refuse to silently erase a broader/newer Sodium integration if the pinned source shape changed.
for unexpected in ("renderShips(", "SodiumWorldRenderer", "RenderSectionManager", "ChunkRenderMatrices"):
    if unexpected in text:
        raise SystemExit(f"fail-closed: unexpected broader Sodium integration present: {unexpected}")

added_new = (
    "        // P1 standalone intentionally has no Sodium runtime. Sodium 26.2 removed the\n"
    "        // legacy ChunkTrackerHolder API used by this pinned optional compatibility path."
)
removed_new = added_new

text = text.replace(imports, "", 1)
text = text.replace(plugin_import, "", 1)
text = text.replace(added_old, added_new, 1)
text = text.replace(removed_old, removed_new, 1)

for obsolete in (
    "net.caffeinemc.mods.sodium",
    "ChunkTrackerHolder",
    "ChunkStatus.FLAG_HAS_BLOCK_DATA",
    "ValkyrienCommonMixinConfigPlugin",
):
    if obsolete in text:
        raise SystemExit(f"fail-closed: obsolete Sodium 1.21.1 bridge token remains: {obsolete}")

if text.count("public static void onChunkAdded(final ClientLevel level, final int x, final int z)") != 1:
    raise SystemExit("fail-closed: onChunkAdded call surface changed")
if text.count("public static void onChunkRemoved(final ClientLevel level, final int x, final int z)") != 1:
    raise SystemExit("fail-closed: onChunkRemoved call surface changed")
if text.count("import net.minecraft.client.multiplayer.ClientLevel;") != 1:
    raise SystemExit("fail-closed: ClientLevel call-surface import changed")

path.write_text(text, encoding="utf-8")
print("P1_SODIUM_CHUNK_TRACKER_ISOLATION_26_2_OVERLAY_APPLIED callbacks=2")
