#!/usr/bin/env python3
"""Apply the isolated Minecraft 26.2 EntityDragger Direction accessor adaptation.

Exact P1 run 35379217305 leaves two independent EntityDragger.kt errors:
removed/private Direction.normal access at line 342 and the unrelated removed
isControlledByLocalInstance API at line 148. This fail-closed overlay changes
only the hit-face Direction unit-vector accessor and leaves dragging semantics
and the independent local-control site untouched.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
rel = "common/src/main/kotlin/org/valkyrienskies/mod/common/util/EntityDragger.kt"
path = root / rel
text = path.read_text(encoding="utf-8")


def replace_count(old: str, new: str, expected: int = 1) -> None:
    global text
    count = text.count(old)
    if count != expected:
        raise SystemExit(f"expected {expected} matches in {rel}: {old!r}; found {count}")
    text = text.replace(old, new)


# Pinned baseline f39132148e... and current 1.21.1/main are byte-identical
# at blob 4048b116af9c5dc37223490ffdc49e97be1fb3be. This expression only
# obtains the hit-face unit vector before the existing ship-to-world transform
# and up-vector dot-product test. Use Minecraft 26.2's public accessor without
# changing any collision, movement, yaw, transform, raycast, or dragging logic.
replace_count(
    "val hitSide = result.direction.normal.toJOMLD()",
    "val hitSide = result.direction.getUnitVec3i().toJOMLD()",
)

path.write_text(text, encoding="utf-8")
print("P1_ENTITYDRAGGER_DIRECTION_26_2_OVERLAY_APPLIED")
