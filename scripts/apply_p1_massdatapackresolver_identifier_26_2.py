#!/usr/bin/env python3
"""Apply the isolated Minecraft 26.2 ResourceLocation -> Identifier adaptation.

The pinned VS2 MassDatapackResolver uses ResourceLocation only as Minecraft
resource-identifier vocabulary. Minecraft 26.2 uses Identifier. This overlay
replaces exactly the eight pinned vocabulary occurrences and deliberately leaves
the independent reload-listener/apply shape, registry tag lookup, datapack
parsing/priority behavior, collision generation, and dummy-world semantics
unchanged.

Run this after apply_p1_massdatapackresolver_miny_26_2.py so the previously
proven dummy-BlockGetter lower-bound adaptation remains composed first.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
rel = "common/src/main/kotlin/org/valkyrienskies/mod/common/config/MassDatapackResolver.kt"
path = root / rel
text = path.read_text(encoding="utf-8")

old = "ResourceLocation"
new = "Identifier"
count = text.count(old)
if count != 8:
    raise SystemExit(f"expected exactly eight pinned ResourceLocation occurrences in {rel}, found {count}")
if text.count(new) != 0:
    raise SystemExit(f"expected Identifier to be absent before overlay in {rel}")

text = text.replace(old, new)

if text.count(old) != 0:
    raise SystemExit(f"ResourceLocation remained after replacement in {rel}")
if text.count(new) != 8:
    raise SystemExit(f"expected exactly eight Identifier occurrences after overlay in {rel}, found {text.count(new)}")

path.write_text(text, encoding="utf-8")
print("P1_MASSDATAPACKRESOLVER_IDENTIFIER_26_2_OVERLAY_APPLIED")
