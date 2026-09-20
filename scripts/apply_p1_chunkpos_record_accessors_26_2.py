#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")

# Minecraft 26.2 exposes ChunkPos as a record. Canonical javac first exposed
# 40 active direct x/z field accesses at 22fe6fe80f87e22a6aa384072bb56c00081ac51a;
# after those became clean, a2c59dd670badf96ffbdb176a061e870c2956efb
# revealed 14 more active accesses behind javac's 100-error frontier. Adapt
# only these exact pinned VS2 call sites to x()/z(); do not sweep unrelated
# .x/.z members or the historical commented-out MixinChunkMap block.
PATCHES = {
    "common/src/main/java/org/valkyrienskies/mod/mixin/client/world/MixinClientChunkCache.java": [
        ("pos.x", "pos.x()", 2, 2),
        ("pos.z", "pos.z()", 2, 2),
        ("chunkPos.x", "chunkPos.x()", 1, 1),
        ("chunkPos.z", "chunkPos.z()", 1, 1),
        ("cp.x", "cp.x()", 2, 2),
        ("cp.z", "cp.z()", 2, 2),
    ],
    "common/src/main/java/org/valkyrienskies/mod/mixin/world/chunk/MixinLevelChunk.java": [
        ("this.chunkPos.x", "this.chunkPos.x()", 1, 1),
        ("this.chunkPos.z", "this.chunkPos.z()", 1, 1),
    ],
    "common/src/main/java/org/valkyrienskies/mod/mixin/world/level/levelgen/MixinNoiseBasedChunkGenerator.java": [
        ("chunkPos.x", "chunkPos.x()", 4, 4),
        ("chunkPos.z", "chunkPos.z()", 4, 4),
    ],
    "common/src/main/java/org/valkyrienskies/mod/mixin/world/level/levelgen/MixinChunkStatus.java": [
        ("chunkPos.x", "chunkPos.x()", 3, 3),
        ("chunkPos.z", "chunkPos.z()", 3, 3),
    ],
    "common/src/main/java/org/valkyrienskies/mod/mixin/world/level/levelgen/MixinFlatLevelSource.java": [
        ("chunkPos.x", "chunkPos.x()", 1, 1),
        ("chunkPos.z", "chunkPos.z()", 1, 1),
    ],
    "common/src/main/java/org/valkyrienskies/mod/mixin/server/world/MixinGenerationChunkHolder.java": [
        ("pos.x", "pos.x()", 1, 1),
        ("pos.z", "pos.z()", 1, 1),
    ],
    "common/src/main/java/org/valkyrienskies/mod/mixin/server/world/MixinChunkHolder.java": [
        ("pos.x", "pos.x()", 3, 3),
        ("pos.z", "pos.z()", 3, 3),
    ],
    "common/src/main/java/org/valkyrienskies/mod/mixin/server/world/MixinChunkMap.java": [
        (
            "getIPlayersWatchingShipChunk(chunkPos.x, chunkPos.z, VSGameUtilsKt.getDimensionId(level))",
            "getIPlayersWatchingShipChunk(chunkPos.x(), chunkPos.z(), VSGameUtilsKt.getDimensionId(level))",
            1,
            2,
        ),
        ("pos.x", "pos.x()", 1, 1),
        ("pos.z", "pos.z()", 1, 1),
    ],
    "common/src/main/java/org/valkyrienskies/mod/mixin/server/world/MixinServerLevel.java": [
        ("worldChunk.getPos().x", "worldChunk.getPos().x()", 2, 2),
        ("worldChunk.getPos().z", "worldChunk.getPos().z()", 2, 2),
        ("pos.x", "pos.x()", 2, 2),
        ("pos.z", "pos.z()", 2, 2),
        ("cp.x", "cp.x()", 2, 2),
        ("cp.z", "cp.z()", 2, 2),
    ],
    "common/src/main/java/org/valkyrienskies/mod/mixin/server/world/MixinChunkMapShipyard.java": [
        ("center.x", "center.x()", 1, 1),
        ("center.z", "center.z()", 1, 1),
    ],
}

changed = 0
for rel, replacements in PATCHES.items():
    path = root / rel
    if not path.is_file():
        raise SystemExit(f"fail-closed: expected pinned VS2 source missing: {path}")
    text = path.read_text(encoding="utf-8")
    for old, new, expected, adapted_fields in replacements:
        actual = text.count(old)
        if actual != expected:
            raise SystemExit(
                f"fail-closed: expected {expected} occurrences of {old!r} in {rel}, found {actual}"
            )
        text = text.replace(old, new)
        changed += adapted_fields
    path.write_text(text, encoding="utf-8")

if changed != 54:
    raise SystemExit(f"fail-closed: expected exactly 54 active ChunkPos field adaptations, got {changed}")

print("P1_CHUNKPOS_RECORD_ACCESSORS_26_2_OVERLAY_APPLIED count=54 files=10")
