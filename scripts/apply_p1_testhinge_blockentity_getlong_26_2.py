#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/kotlin/org/valkyrienskies/mod/common/blockentity/TestHingeBlockEntity.kt"
text = path.read_text(encoding="utf-8")

replacements = [
    (
        '            tag.getLong("shipId0"), VSJointPose(',
        '            tag.getLong("shipId0").orElse(0L), VSJointPose(',
    ),
    (
        '            tag.getLong("shipId1"), VSJointPose(',
        '            tag.getLong("shipId1").orElse(0L), VSJointPose(',
    ),
]

for old, new in replacements:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"expected exactly one occurrence of {old!r} in {path}, found {count}")
    text = text.replace(old, new)

path.write_text(text, encoding="utf-8")
print("P1_TESTHINGE_BLOCKENTITY_GETLONG_26_2_OVERLAY_APPLIED")
