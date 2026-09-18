#!/usr/bin/env python3
"""Apply the isolated Minecraft 26.2 TestHinge getShape signature adaptation.

Exact P1 run 35388500277 reports TestHingeBlock.kt getShape overrides
nothing and supplies the exact Minecraft 26.2 candidate signature with
non-null BlockGetter, BlockPos, and CollisionContext parameters. This
fail-closed overlay removes only those three nullable markers and preserves
the method body plus all independent TestHinge APIs unchanged.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
rel = "common/src/main/kotlin/org/valkyrienskies/mod/common/block/TestHingeBlock.kt"
path = root / rel
text = path.read_text(encoding="utf-8")

old = "        state: BlockState, level: BlockGetter?, pos: BlockPos?, context: CollisionContext?\n"
new = "        state: BlockState, level: BlockGetter, pos: BlockPos, context: CollisionContext\n"
count = text.count(old)
if count != 1:
    raise SystemExit(f"expected 1 getShape signature match in {rel}; found {count}")

text = text.replace(old, new)
path.write_text(text, encoding="utf-8")
print("P1_TESTHINGE_GETSHAPE_SIGNATURE_26_2_OVERLAY_APPLIED")
