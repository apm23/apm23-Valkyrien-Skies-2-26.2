#!/usr/bin/env python3
"""Apply the isolated Minecraft 26.2 typed JSON reload-listener adaptation.

The pinned VS2 VSEntityHandlerDataLoader intentionally consumes raw JsonElement
values from the `vs_entities` JSON directory and performs its own handler lookup,
pairing, exception handling, and logging. Minecraft 26.2 changed
SimpleJsonResourceReloadListener from the legacy (Gson, directory) constructor
to a typed (Codec<T>, FileToIdConverter) boundary.

This fail-closed overlay preserves the upstream raw-JSON/apply semantics by using
SimpleJsonResourceReloadListener<JsonElement>, ExtraCodecs.JSON, and
FileToIdConverter.json("vs_entities"). It deliberately does not change registry
lookup, JSON extraction, entity-handler pairing, error handling, networking,
entity dragging, or any VS2 authority/reference-space behavior.

Run this only after apply_p1_vsentityhandlerdataloader_identifier_26_2.py.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
rel = "common/src/main/kotlin/org/valkyrienskies/mod/common/config/VSEntityHandlerDataLoader.kt"
path = root / rel
text = path.read_text(encoding="utf-8")

old_gson_import = "import com.google.gson.Gson\n"
new_converter_import = "import net.minecraft.resources.FileToIdConverter\n"
new_codec_import = "import net.minecraft.util.ExtraCodecs\n"
old_decl = 'object VSEntityHandlerDataLoader : SimpleJsonResourceReloadListener(Gson(), "vs_entities") {'
new_decl = 'object VSEntityHandlerDataLoader : SimpleJsonResourceReloadListener<JsonElement>(ExtraCodecs.JSON, FileToIdConverter.json("vs_entities")) {'

if text.count(old_gson_import) != 1:
    raise SystemExit(f"expected exactly one legacy Gson import in {rel}")
if text.count(old_decl) != 1:
    raise SystemExit(f"expected exactly one legacy reload-listener declaration in {rel}")
if "import net.minecraft.resources.Identifier\n" not in text:
    raise SystemExit(f"expected prior Identifier overlay to be present in {rel}")
if new_converter_import in text or new_codec_import in text or new_decl in text:
    raise SystemExit(f"typed reload-listener adaptation already present in {rel}")

text = text.replace(old_gson_import, "", 1)
text = text.replace(
    "import net.minecraft.resources.Identifier\n",
    "import net.minecraft.resources.Identifier\n" + new_converter_import,
    1,
)
text = text.replace(
    "import net.minecraft.server.packs.resources.SimpleJsonResourceReloadListener\n",
    "import net.minecraft.server.packs.resources.SimpleJsonResourceReloadListener\n" + new_codec_import,
    1,
)
text = text.replace(old_decl, new_decl, 1)

if "Gson()" in text or old_decl in text:
    raise SystemExit(f"legacy reload-listener constructor remained in {rel}")
if text.count(new_decl) != 1:
    raise SystemExit(f"expected exactly one typed reload-listener declaration after overlay in {rel}")
if text.count('FileToIdConverter.json("vs_entities")') != 1:
    raise SystemExit(f"expected exactly one vs_entities FileToIdConverter after overlay in {rel}")
if text.count("ExtraCodecs.JSON") != 1:
    raise SystemExit(f"expected exactly one raw JSON codec after overlay in {rel}")

path.write_text(text, encoding="utf-8")
print("P1_VSENTITYHANDLERDATALOADER_RELOAD_LISTENER_26_2_OVERLAY_APPLIED")
