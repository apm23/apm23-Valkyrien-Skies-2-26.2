#!/usr/bin/env python3
"""Apply the isolated Minecraft 26.2 VSGameEvents RenderType package adaptation.

Pinned upstream VS2 uses net.minecraft.client.renderer.RenderType as the typed
payload for ShipStartRenderEvent and ShipRenderEvent. Minecraft 26.2 retains
RenderType but moves it to net.minecraft.client.renderer.rendertype.RenderType.
This overlay changes only that import; the event payload type, emitter flow, and
VS2 rendering architecture remain otherwise unchanged.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
rel = "common/src/main/kotlin/org/valkyrienskies/mod/common/hooks/VSGameEvents.kt"
path = root / rel
text = path.read_text(encoding="utf-8")

old = "import net.minecraft.client.renderer.RenderType\n"
new = "import net.minecraft.client.renderer.rendertype.RenderType\n"
count = text.count(old)
if count != 1:
    raise SystemExit(f"expected exactly 1 legacy RenderType import in {rel}; found {count}")

# Fail closed if the pinned event shape has drifted. These two fields are the
# complete RenderType surface in VSGameEvents and remain passive event payloads.
field_count = text.count("val renderType: RenderType")
if field_count != 2:
    raise SystemExit(f"expected exactly 2 RenderType event payload fields in {rel}; found {field_count}")

text = text.replace(old, new, 1)

if old in text:
    raise SystemExit(f"legacy RenderType import still present in {rel}")
if text.count(new) != 1:
    raise SystemExit(f"expected exactly 1 Minecraft 26.2 RenderType import in {rel}")
if text.count("val renderType: RenderType") != 2:
    raise SystemExit(f"RenderType event payload fields changed unexpectedly in {rel}")

path.write_text(text, encoding="utf-8")
print("P1_VSGAMEEVENTS_RENDERTYPE_26_2_OVERLAY_APPLIED")
