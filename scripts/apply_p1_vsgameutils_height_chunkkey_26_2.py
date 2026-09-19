#!/usr/bin/env python3
"""Apply the isolated Minecraft 26.2 VSGameUtils height/chunk-key adaptation.

Pinned upstream VS2 still uses the legacy Level minBuildHeight/maxBuildHeight
properties and ChunkPos.asLong(x, z). Minecraft 26.2 exposes the equivalent
semantics as getMinY(), getHeight(), and ChunkPos.pack(x, z). This overlay
changes only those exact expressions. It does not touch the separately frozen
ResourceKey/Identifier dimension-identity bridge or any VS2 ship semantics.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
rel = "common/src/main/kotlin/org/valkyrienskies/mod/common/VSGameUtils.kt"
path = root / rel
text = path.read_text(encoding="utf-8")

replacements = [
    (
        "val Level.yRange get() = LevelYRange(minBuildHeight, maxBuildHeight - 1)",
        "val Level.yRange get() = LevelYRange(getMinY(), getMinY() + getHeight() - 1)",
    ),
    (
        "ChunkPos.asLong(chunkX, chunkZ)",
        "ChunkPos.pack(chunkX, chunkZ)",
    ),
]

for old, new in replacements:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"expected exactly one pinned VSGameUtils expression {old!r} in {rel}, found {count}")
    text = text.replace(old, new, 1)

path.write_text(text, encoding="utf-8")
print("P1_VSGAMEUTILS_HEIGHT_CHUNKKEY_26_2_OVERLAY_APPLIED")
