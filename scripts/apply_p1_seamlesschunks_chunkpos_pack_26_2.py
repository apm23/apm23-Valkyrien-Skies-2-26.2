#!/usr/bin/env python3
"""Apply the isolated Minecraft 26.2 ChunkPos packed-key API adaptation.

The pinned VS2 SeamlessChunksManager uses the legacy instance toLong() and
static asLong(x, z) names. Minecraft 26.2 exposes the equivalent packed chunk
key operations as instance pack() and static pack(x, z). This overlay changes
only those three exact call sites and preserves all queue/packet semantics.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
rel = "common/src/main/kotlin/org/valkyrienskies/mod/common/assembly/SeamlessChunksManager.kt"
path = root / rel
text = path.read_text(encoding="utf-8")

replacements = [
    ("it.toMinecraft().toLong()", "it.toMinecraft().pack()"),
    ("pos.toLong()", "pos.pack()"),
    ("ChunkPos.asLong(chunkX, chunkZ)", "ChunkPos.pack(chunkX, chunkZ)"),
]

for old, new in replacements:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"expected exactly one pinned SeamlessChunksManager expression {old!r} in {rel}, found {count}")
    text = text.replace(old, new, 1)

path.write_text(text, encoding="utf-8")
print("P1_SEAMLESSCHUNKS_CHUNKPOS_PACK_26_2_OVERLAY_APPLIED")
