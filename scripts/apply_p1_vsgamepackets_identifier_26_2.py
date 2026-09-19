#!/usr/bin/env python3
"""Apply the isolated Minecraft 26.2 ResourceLocation -> Identifier adaptation.

The pinned VS2 VSGamePackets uses ResourceLocation only at exactly two vocabulary
sites: the import and the handler-id tryParse call in PacketSyncVSEntityTypes.
Minecraft 26.2 uses Identifier at these boundaries. This overlay deliberately
leaves registry lookup/pairing, packet registration, entity dragging/reference-
space state, local-control checks, lerp/setPos behavior, client/server authority,
and all other networking/gameplay semantics unchanged.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
rel = "common/src/main/kotlin/org/valkyrienskies/mod/common/networking/VSGamePackets.kt"
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
print("P1_VSGAMEPACKETS_IDENTIFIER_26_2_OVERLAY_APPLIED")
