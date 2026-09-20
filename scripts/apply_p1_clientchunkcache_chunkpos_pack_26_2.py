#!/usr/bin/env python3
"""Adapt the six pinned MixinClientChunkCache packed ChunkPos key calls to Minecraft 26.2.

This is vocabulary-only: ChunkPos.asLong(int,int) became ChunkPos.pack(int,int).
Do not change ship-chunk storage authority, packet decode, connectivity, relight,
renderer invalidation, unload ordering, or Sodium/vanilla renderer selection.
"""
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/client/world/MixinClientChunkCache.java"
if not path.is_file():
    raise SystemExit(f"fail-closed: expected pinned VS2 MixinClientChunkCache source missing: {path}")

text = path.read_text(encoding="utf-8")
old = "ChunkPos.asLong("
new = "ChunkPos.pack("

if text.count(old) != 6:
    raise SystemExit(f"fail-closed: expected six legacy packed-key calls, found {text.count(old)}")
if new in text:
    raise SystemExit("fail-closed: ClientChunkCache packed-key vocabulary already adapted")

anchors = {
    "private final Long2ObjectMap<LevelChunk> vs$shipChunks = new Long2ObjectOpenHashMap<>();": 1,
    "private final Long2ObjectMap<LevelChunk> emptyShipChunks = new Long2ObjectOpenHashMap<>();": 1,
    "VSGameUtilsKt.isChunkInShipyard(level, x, z)": 1,
    "VSGameUtilsKt.isChunkInShipyard(level, chunkX, chunkZ)": 2,
    "clientChunkMapAccessor.setChunkCount(clientChunkMapAccessor.getChunkCount() + 1);": 1,
    "clientChunkMapAccessor.setChunkCount(clientChunkMapAccessor.getChunkCount() - 1);": 1,
    "level.unload(chunk);": 1,
    "relightChunk(worldChunk);": 1,
    "this.level.onChunkLoaded(pos);": 1,
    "ValkyrienCommonMixinConfigPlugin.getVSRenderer() == VSRenderer.SODIUM": 1,
}
for anchor, expected in anchors.items():
    count = text.count(anchor)
    if count != expected:
        raise SystemExit(f"fail-closed: preserved ClientChunkCache lifecycle anchor changed: {anchor!r} count={count} expected={expected}")

text = text.replace(old, new)

if old in text or text.count(new) != 6:
    raise SystemExit(f"fail-closed: expected six ChunkPos.pack calls after adaptation, found {text.count(new)}")
for anchor, expected in anchors.items():
    count = text.count(anchor)
    if count != expected:
        raise SystemExit(f"fail-closed: ClientChunkCache lifecycle anchor changed after adaptation: {anchor!r} count={count} expected={expected}")

path.write_text(text, encoding="utf-8")
print("P1_CLIENTCHUNKCACHE_CHUNKPOS_PACK_26_2_OVERLAY_APPLIED count=6")

# Transport-only chaining for the separately evidenced Minecraft 26.2 packet-heightmap type.
# This changes only the injector parameter/imports and its two LevelChunk forwarding calls.
heightmap_helper = Path(__file__).with_name("apply_p1_clientchunkcache_heightmaps_26_2.py")
if not heightmap_helper.is_file():
    raise SystemExit(f"fail-closed: required ClientChunkCache heightmap overlay helper missing: {heightmap_helper}")
subprocess.run([sys.executable, str(heightmap_helper), str(root)], check=True)
print("P1_CLIENTCHUNKCACHE_HEIGHTMAPS_26_2_CHAINED")

# Transport-only chaining for the separately evidenced Minecraft 26.2 LevelHeightAccessor vocabulary.
# Change only the two section-bound calls; renderer-dirty semantics remain untouched.
section_range_helper = Path(__file__).with_name("apply_p1_clientchunkcache_section_range_26_2.py")
if not section_range_helper.is_file():
    raise SystemExit(f"fail-closed: required ClientChunkCache section-range overlay helper missing: {section_range_helper}")
subprocess.run([sys.executable, str(section_range_helper), str(root)], check=True)
print("P1_CLIENTCHUNKCACHE_SECTION_RANGE_26_2_CHAINED")

# Transport-only chaining for the independently evidenced MixinClientLevel hand API split.
# Preserve creative gating and barrier semantics; do not touch the separate player-scale frontier.
clientlevel_hand_helper = Path(__file__).with_name("apply_p1_clientlevel_hand_items_26_2.py")
if not clientlevel_hand_helper.is_file():
    raise SystemExit(f"fail-closed: required ClientLevel hand-items overlay helper missing: {clientlevel_hand_helper}")
subprocess.run([sys.executable, str(clientlevel_hand_helper), str(root)], check=True)
print("P1_CLIENTLEVEL_HAND_ITEMS_26_2_CHAINED")
