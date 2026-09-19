#!/usr/bin/env python3
"""Apply the isolated Minecraft 26.2 ResourceLocation -> Identifier adaptation.

The pinned VS2 DimensionParametersResolver uses ResourceLocation only as
Minecraft resource-identifier vocabulary: one import and one reload-map key.
Minecraft 26.2 uses Identifier for those keys. This overlay replaces exactly
those two pinned vocabulary occurrences and deliberately leaves the independent
SimpleJsonResourceReloadListener generic/constructor migration, apply shape and
nullability, JSON parsing, priority selection, and dimensionMap semantics
unchanged.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
rel = "common/src/main/kotlin/org/valkyrienskies/mod/common/config/DimensionParametersResolver.kt"
path = root / rel
text = path.read_text(encoding="utf-8")

old = "ResourceLocation"
new = "Identifier"
count = text.count(old)
if count != 2:
    raise SystemExit(f"expected exactly two pinned ResourceLocation occurrences in {rel}, found {count}")
if text.count(new) != 0:
    raise SystemExit(f"expected Identifier to be absent before overlay in {rel}")

text = text.replace(old, new)

if text.count(old) != 0:
    raise SystemExit(f"ResourceLocation remained after replacement in {rel}")
if text.count(new) != 2:
    raise SystemExit(f"expected exactly two Identifier occurrences after overlay in {rel}, found {text.count(new)}")

path.write_text(text, encoding="utf-8")
print("P1_DIMENSIONPARAMETERSRESOLVER_IDENTIFIER_26_2_OVERLAY_APPLIED")
