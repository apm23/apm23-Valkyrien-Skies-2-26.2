#!/usr/bin/env python3
"""Apply the isolated Minecraft 26.2 CreativeModeTab.Output access adaptation.

Minecraft 26.2 makes CreativeModeTab.Output protected, while Fabric API's
creative-tab module explicitly marks the same nested type transitive-accessible.
The P1 no-remap common compile currently sees Fabric API as plain compileOnly,
so that dependency class-tweaker is not reflected in the common Minecraft jar.
Mirror only that access contract into VS2's existing common access widener.
Do not alter ValkyrienSkiesMod.createCreativeTab(), item order, or tab behavior.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
rel = "common/src/main/resources/valkyrienskies-common.accesswidener"
path = root / rel
text = path.read_text(encoding="utf-8")

header = "accessWidener\tv2\tofficial\n"
if not text.startswith(header):
    raise SystemExit(f"expected Minecraft 26.2 official access-widener header in {rel}")

access_line = "accessible\tclass\tnet/minecraft/world/item/CreativeModeTab$Output"
if access_line in text:
    raise SystemExit(f"CreativeModeTab.Output access line already present in {rel}")

anchor = "# Only put classes in here. For everything else use Accessor mixins\n\n"
if text.count(anchor) != 1:
    raise SystemExit(f"expected exactly one class-only anchor in {rel}, found {text.count(anchor)}")

replacement = (
    anchor
    + "# Minecraft 26.2 creative-tab Output access; mirrors Fabric API's transitive class-tweaker contract\n"
    + access_line
    + "\n\n"
)
text = text.replace(anchor, replacement, 1)

if text.count(access_line) != 1:
    raise SystemExit(f"expected exactly one CreativeModeTab.Output access line after overlay in {rel}")

path.write_text(text, encoding="utf-8")
print("P1_CREATIVETAB_OUTPUT_ACCESS_26_2_OVERLAY_APPLIED")
