#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")

# Minecraft 26.2 exposes ChunkPos as a record. The exact-head canonical javac
# frontier at 22fe6fe80f87e22a6aa384072bb56c00081ac51a reports these 40
# direct x/z field accesses as private. Adapt only the reported pinned VS2
# call sites to the record accessors; do not sweep unrelated .x/.z members.
PATCHES = {
    "common/src/main/java/org/valkyrienskies/mod/mixin/client/world/MixinClientChunkCache.java": [
        ("pos.x", "pos.x()", 2),
        ("pos.z", "pos.z()", 2),
        ("chunkPos.x", "chunkPos.x()", 1),
        ("chunkPos.z", "chunkPos.z()", 1),
        ("cp.x", "cp.x()", 2),
        ("cp.z", "cp.z()", 2),
    ],
    "common/src/main/java/org/valkyrienskies/mod/mixin/world/chunk/MixinLevelChunk.java": [
        ("this.chunkPos.x", "this.chunkPos.x()", 1),
        ("this.chunkPos.z", "this.chunkPos.z()", 1),
    ],
    "common/src/main/java/org/valkyrienskies/mod/mixin/world/level/levelgen/MixinNoiseBasedChunkGenerator.java": [
        ("chunkPos.x", "chunkPos.x()", 4),
        ("chunkPos.z", "chunkPos.z()", 4),
    ],
    "common/src/main/java/org/valkyrienskies/mod/mixin/world/level/levelgen/MixinChunkStatus.java": [
        ("chunkPos.x", "chunkPos.x()", 3),
        ("chunkPos.z", "chunkPos.z()", 3),
    ],
    "common/src/main/java/org/valkyrienskies/mod/mixin/world/level/levelgen/MixinFlatLevelSource.java": [
        ("chunkPos.x", "chunkPos.x()", 1),
        ("chunkPos.z", "chunkPos.z()", 1),
    ],
    "common/src/main/java/org/valkyrienskies/mod/mixin/server/world/MixinGenerationChunkHolder.java": [
        ("pos.x", "pos.x()", 1),
        ("pos.z", "pos.z()", 1),
    ],
    "common/src/main/java/org/valkyrienskies/mod/mixin/server/world/MixinChunkHolder.java": [
        ("pos.x", "pos.x()", 3),
        ("pos.z", "pos.z()", 3),
    ],
    "common/src/main/java/org/valkyrienskies/mod/mixin/server/world/MixinChunkMap.java": [
        ("chunkPos.x", "chunkPos.x()", 1),
        ("chunkPos.z", "chunkPos.z()", 1),
        ("pos.x", "pos.x()", 1),
        ("pos.z", "pos.z()", 1),
    ],
}

changed = 0
for rel, replacements in PATCHES.items():
    path = root / rel
    if not path.is_file():
        raise SystemExit(f"fail-closed: expected pinned VS2 source missing: {path}")
    text = path.read_text(encoding="utf-8")
    for old, new, expected in replacements:
        actual = text.count(old)
        if actual != expected:
            raise SystemExit(
                f"fail-closed: expected {expected} occurrences of {old!r} in {rel}, found {actual}"
            )
        text = text.replace(old, new)
        changed += expected
    path.write_text(text, encoding="utf-8")

if changed != 40:
    raise SystemExit(f"fail-closed: expected exactly 40 ChunkPos field adaptations, got {changed}")

print("P1_CHUNKPOS_RECORD_ACCESSORS_26_2_OVERLAY_APPLIED count=40 files=8")
