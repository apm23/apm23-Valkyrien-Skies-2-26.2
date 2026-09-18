#!/usr/bin/env python3
"""Apply the isolated Minecraft 26.2 TestHinge getTicker generic-bound adaptation.

Exact P1 run 35392499337 reports that TestHingeBlock.kt getTicker overrides
nothing and supplies the Minecraft 26.2 candidate with a non-null
`T : BlockEntity` bound. The pinned upstream source differs at that bound only:
`T : BlockEntity?`. This fail-closed overlay changes exactly that generic bound
and preserves parameters, return expression, ticker body and all other hinge APIs.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
rel = "common/src/main/kotlin/org/valkyrienskies/mod/common/block/TestHingeBlock.kt"
path = root / rel
text = path.read_text(encoding="utf-8")

old = "    override fun <T : BlockEntity?> getTicker(\n"
new = "    override fun <T : BlockEntity> getTicker(\n"
count = text.count(old)
if count != 1:
    raise SystemExit(f"expected 1 getTicker generic-bound match in {rel}; found {count}")

text = text.replace(old, new)
path.write_text(text, encoding="utf-8")
print("P1_TESTHINGE_GETTICKER_BOUND_26_2_OVERLAY_APPLIED")
