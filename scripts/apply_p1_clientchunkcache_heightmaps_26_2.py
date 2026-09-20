#!/usr/bin/env python3
"""Adapt the pinned VS2 ClientChunkCache packet heightmap argument to Minecraft 26.2.

Minecraft 26.2 changed ClientChunkCache.replaceWithPacketData and LevelChunk.replaceWithPacketData
from CompoundTag heightmaps to Map<Heightmap.Types, long[]>. This helper changes only the
injected method parameter, its two forwarding calls, and required imports. Ship-chunk storage,
terrain connectivity, relighting, renderer invalidation, unload ordering, and onChunkLoaded
ordering remain unchanged.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/client/world/MixinClientChunkCache.java"
if not path.is_file():
    raise SystemExit(f"fail-closed: expected pinned VS2 MixinClientChunkCache source missing: {path}")

text = path.read_text(encoding="utf-8")

old_param = "final CompoundTag tag,"
new_param = "final Map<Heightmap.Types, long[]> heightmaps,"
old_call = "replaceWithPacketData(buf, tag, consumer);"
new_call = "replaceWithPacketData(buf, heightmaps, consumer);"

if text.count("import java.util.Map;") != 0:
    raise SystemExit("fail-closed: java.util.Map import already present before heightmap adaptation")
if text.count("import net.minecraft.nbt.CompoundTag;") != 1:
    raise SystemExit(f"fail-closed: expected one legacy CompoundTag import, found {text.count('import net.minecraft.nbt.CompoundTag;')}")
if text.count("import net.minecraft.world.level.levelgen.Heightmap;") != 0:
    raise SystemExit("fail-closed: Heightmap import already present before adaptation")
if text.count(old_param) != 1:
    raise SystemExit(f"fail-closed: expected one legacy packet heightmap parameter, found {text.count(old_param)}")
if text.count(old_call) != 2:
    raise SystemExit(f"fail-closed: expected two legacy packet heightmap forwarding calls, found {text.count(old_call)}")
if new_param in text or new_call in text:
    raise SystemExit("fail-closed: packet heightmap adaptation is already partially present")

# This helper is intentionally chained after the separately proven packed-key unit.
if text.count("ChunkPos.pack(") != 6 or "ChunkPos.asLong(" in text:
    raise SystemExit("fail-closed: expected frozen six-site ClientChunkCache packed-key adaptation before heightmap unit")

anchors = {
    '@Inject(method = "replaceWithPacketData", at = @At("HEAD"), cancellable = true)': 1,
    "ClientChunkCacheStorageAccessor.class.cast(storage);": 2,
    "if (!clientChunkMapAccessor.callInRange(x, z)) {": 1,
    "if (VSGameUtilsKt.isChunkInShipyard(level, x, z)) {": 1,
    "clientChunkMapAccessor.setChunkCount(clientChunkMapAccessor.getChunkCount() + 1);": 1,
    "clientShipWorld.forceUpdateConnectivityChunk(": 1,
    "clientShipWorld.addTerrainUpdates(dimensionId, voxelShapeUpdates);": 1,
    "relightChunk(worldChunk);": 1,
    "this.level.onChunkLoaded(pos);": 1,
    "level.unload(chunk);": 1,
}
for anchor, expected in anchors.items():
    count = text.count(anchor)
    if count != expected:
        raise SystemExit(f"fail-closed: preserved ClientChunkCache authority/lifecycle anchor changed: {anchor!r} count={count} expected={expected}")

text = text.replace("import java.util.ArrayList;\n", "import java.util.ArrayList;\nimport java.util.Map;\n", 1)
text = text.replace("import net.minecraft.nbt.CompoundTag;\n", "", 1)
text = text.replace(
    "import net.minecraft.world.level.lighting.LevelLightEngine;\n",
    "import net.minecraft.world.level.levelgen.Heightmap;\nimport net.minecraft.world.level.lighting.LevelLightEngine;\n",
    1,
)
text = text.replace(old_param, new_param, 1)
text = text.replace(old_call, new_call)

if text.count("import java.util.Map;") != 1:
    raise SystemExit("fail-closed: java.util.Map import did not converge exactly once")
if "CompoundTag" in text:
    raise SystemExit("fail-closed: legacy CompoundTag remains in MixinClientChunkCache after heightmap adaptation")
if text.count("import net.minecraft.world.level.levelgen.Heightmap;") != 1:
    raise SystemExit("fail-closed: Heightmap import did not converge exactly once")
if text.count(new_param) != 1 or old_param in text:
    raise SystemExit("fail-closed: packet heightmap parameter did not converge exactly once")
if text.count(new_call) != 2 or old_call in text:
    raise SystemExit("fail-closed: packet heightmap forwarding calls did not converge exactly twice")
if text.count("ChunkPos.pack(") != 6 or "ChunkPos.asLong(" in text:
    raise SystemExit("fail-closed: frozen ClientChunkCache packed-key adaptation changed unexpectedly")
for anchor, expected in anchors.items():
    count = text.count(anchor)
    if count != expected:
        raise SystemExit(f"fail-closed: ClientChunkCache authority/lifecycle anchor changed after adaptation: {anchor!r} count={count} expected={expected}")

path.write_text(text, encoding="utf-8")
print("P1_CLIENTCHUNKCACHE_HEIGHTMAPS_26_2_OVERLAY_APPLIED calls=2")
