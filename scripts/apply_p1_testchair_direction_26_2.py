#!/usr/bin/env python3
"""Apply the isolated Minecraft 26.2 TestChairBlock Direction accessor adaptation.

Exact P1 run 35381321453 leaves three independent TestChairBlock.kt API areas:
changed entity creation at line 54, removed moveTo at line 57, and private
Direction.normal at line 58. This fail-closed overlay changes only the chair-facing
unit-vector accessor and leaves mounting/riding semantics and the other errors untouched.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
rel = "common/src/main/kotlin/org/valkyrienskies/mod/common/block/TestChairBlock.kt"
path = root / rel
text = path.read_text(encoding="utf-8")


def replace_count(old: str, new: str, expected: int = 1) -> None:
    global text
    count = text.count(old)
    if count != expected:
        raise SystemExit(f"expected {expected} matches in {rel}: {old!r}; found {count}")
    text = text.replace(old, new)


# Pinned baseline f39132148e... and current 1.21.1/main are byte-identical
# at blob e830d6c3afd12b3c330ee13335a71e1d2c8021d8. The expression only obtains
# the chair-facing unit vector before the existing toDoubles(), position offset,
# and lookAt call. Use Minecraft 26.2's public accessor without changing entity
# creation, positioning, controller state, spawn, riding, or lookAt semantics.
replace_count(
    "state.getValue(FACING).normal.toDoubles()",
    "state.getValue(FACING).getUnitVec3i().toDoubles()",
)

path.write_text(text, encoding="utf-8")
print("P1_TESTCHAIR_DIRECTION_26_2_OVERLAY_APPLIED")
