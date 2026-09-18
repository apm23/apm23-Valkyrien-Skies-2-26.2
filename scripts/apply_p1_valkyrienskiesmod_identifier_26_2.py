#!/usr/bin/env python3
"""Apply the isolated Minecraft 26.2 ValkyrienSkiesMod Identifier adaptation.

Exact P1 run 35384633761 leaves two independent ValkyrienSkiesMod.kt API areas:
ResourceLocation no longer resolves at the import and the two existing resource
factory calls, while CreativeModeTab.Output access is a separate compiler
failure. This fail-closed overlay changes only resource identifier vocabulary
and leaves creative-tab population/output semantics untouched.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
rel = "common/src/main/kotlin/org/valkyrienskies/mod/common/ValkyrienSkiesMod.kt"
path = root / rel
text = path.read_text(encoding="utf-8")


def replace_count(old: str, new: str, expected: int = 1) -> None:
    global text
    count = text.count(old)
    if count != expected:
        raise SystemExit(f"expected {expected} matches in {rel}: {old!r}; found {count}")
    text = text.replace(old, new)


# Pinned baseline f39132148e... and current 1.21.1/main are byte-identical
# at blob 6d9b4671b0f95c722f39938d5b74097acd780036. Minecraft 26.2 uses
# Identifier where this upstream source used ResourceLocation. Preserve
# ResourceKey/TagKey construction and all independent CreativeModeTab behavior.
replace_count(
    "import net.minecraft.resources.ResourceLocation",
    "import net.minecraft.resources.Identifier",
)
replace_count(
    'ResourceLocation.parse("valkyrienskies")',
    'Identifier.parse("valkyrienskies")',
)
replace_count(
    'ResourceLocation.fromNamespaceAndPath(MOD_ID, "assemble_blacklist")',
    'Identifier.fromNamespaceAndPath(MOD_ID, "assemble_blacklist")',
)

path.write_text(text, encoding="utf-8")
print("P1_VALKYRIENSKIESMOD_IDENTIFIER_26_2_OVERLAY_APPLIED")
