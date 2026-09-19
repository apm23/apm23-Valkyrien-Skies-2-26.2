#!/usr/bin/env python3
"""Apply the isolated Minecraft 26.2 ResourceLocation -> Identifier adaptation.

The pinned VS2 VSEntityHandlerDataLoader uses ResourceLocation only as Minecraft
resource-identifier vocabulary at exactly three sites: the import, the reload
map key, and the handler-id parser. Minecraft 26.2 uses Identifier at these
boundaries. This overlay deliberately leaves the independent typed reload-
listener generic/constructor/apply shape, registry lookup, JSON extraction,
handler pairing, logging, and all surrounding VS2 behavior unchanged.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
rel = "common/src/main/kotlin/org/valkyrienskies/mod/common/config/VSEntityHandlerDataLoader.kt"
path = root / rel
text = path.read_text(encoding="utf-8")

old = "ResourceLocation"
new = "Identifier"
count = text.count(old)
if count != 3:
    raise SystemExit(f"expected exactly three pinned ResourceLocation occurrences in {rel}, found {count}")
if text.count(new) != 0:
    raise SystemExit(f"expected Identifier to be absent before overlay in {rel}")

text = text.replace(old, new)

if text.count(old) != 0:
    raise SystemExit(f"ResourceLocation remained after replacement in {rel}")
if text.count(new) != 3:
    raise SystemExit(f"expected exactly three Identifier occurrences after overlay in {rel}, found {text.count(new)}")

path.write_text(text, encoding="utf-8")
print("P1_VSENTITYHANDLERDATALOADER_IDENTIFIER_26_2_OVERLAY_APPLIED")
