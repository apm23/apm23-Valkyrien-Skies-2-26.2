#!/usr/bin/env python3
"""Fail-closed Minecraft 26.2 compatibility overlay for TestHingeBlock.onPaste NBT ship-id reads.

Pinned upstream VS2 uses CompoundTag.getLong(...) directly as Long map keys. Minecraft 26.2
returns Optional<Long>. Unwrap only the four onPaste shipId0/shipId1 reads with legacy
primitive-getter default-zero semantics. No transform, copy/paste, joint, physics, or block-entity
behavior is changed here.
"""

from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit("usage: apply_p1_testhinge_onpaste_getlong_26_2.py <upstream-vs2-root>")

root = Path(sys.argv[1])
target = root / "common/src/main/kotlin/org/valkyrienskies/mod/common/block/TestHingeBlock.kt"
text = target.read_text(encoding="utf-8")

old0 = 'tag.getLong("shipId0")'
old1 = 'tag.getLong("shipId1")'
new0 = 'tag.getLong("shipId0").orElse(0L)'
new1 = 'tag.getLong("shipId1").orElse(0L)'

count0 = text.count(old0)
count1 = text.count(old1)
if count0 != 2 or count1 != 2:
    raise SystemExit(
        f"fail-closed: expected exactly 2 shipId0 and 2 shipId1 getLong reads in pinned TestHingeBlock.kt; found {count0} and {count1}"
    )

text = text.replace(old0, new0).replace(old1, new1)

if text.count(new0) != 2 or text.count(new1) != 2:
    raise SystemExit("fail-closed: TestHinge onPaste Optional<Long> replacement count mismatch")

target.write_text(text, encoding="utf-8")
print("P1_TESTHINGE_ONPASTE_GETLONG_26_2_OVERLAY_APPLIED")
