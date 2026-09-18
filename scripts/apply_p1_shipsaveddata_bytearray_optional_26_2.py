#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/kotlin/org/valkyrienskies/mod/common/ShipSavedData.kt"
text = path.read_text(encoding="utf-8")

replacements = [
    (
        "            val queryableShipDataAsBytes = compoundTag.getByteArray(QUERYABLE_SHIP_DATA_NBT_KEY)",
        "            val queryableShipDataAsBytes = compoundTag.getByteArray(QUERYABLE_SHIP_DATA_NBT_KEY).orElse(byteArrayOf())",
    ),
    (
        "            val chunkAllocatorAsBytes = compoundTag.getByteArray(CHUNK_ALLOCATOR_NBT_KEY)",
        "            val chunkAllocatorAsBytes = compoundTag.getByteArray(CHUNK_ALLOCATOR_NBT_KEY).orElse(byteArrayOf())",
    ),
    (
        "            val pipelineAsBytes = compoundTag.getByteArray(PIPELINE_NBT_KEY)",
        "            val pipelineAsBytes = compoundTag.getByteArray(PIPELINE_NBT_KEY).orElse(byteArrayOf())",
    ),
]

for old, new in replacements:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"expected exactly one occurrence of {old!r} in {path}, found {count}")
    text = text.replace(old, new)

path.write_text(text, encoding="utf-8")
print("P1_SHIPSAVEDDATA_BYTEARRAY_OPTIONAL_26_2_OVERLAY_APPLIED")
