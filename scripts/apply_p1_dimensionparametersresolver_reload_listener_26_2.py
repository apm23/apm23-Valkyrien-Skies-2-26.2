#!/usr/bin/env python3
"""Apply the isolated Minecraft 26.2 typed JSON reload-listener adaptation.

The pinned VS2 DimensionParametersResolver intentionally consumes raw
JsonElement values from the `vs_dimension_parameters` JSON directory, then
performs its own object/array parsing, validation, priority selection, logging,
and dimensionMap replacement. Minecraft 26.2 changed
SimpleJsonResourceReloadListener from the legacy (Gson, directory) constructor
to a typed (Codec<T>, FileToIdConverter) boundary.

This fail-closed overlay preserves the upstream raw-JSON/apply semantics by using
SimpleJsonResourceReloadListener<JsonElement>, ExtraCodecs.JSON, and
FileToIdConverter.json("vs_dimension_parameters"). It deliberately preserves
the existing nullable map guards, parse routine, priority behavior, logging, and
dimensionMap semantics. It does not touch ship lifecycle, physics, collision,
entity dragging/reference-space behavior, networking, player, or camera code.

Run this only after apply_p1_dimensionparametersresolver_identifier_26_2.py.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
rel = "common/src/main/kotlin/org/valkyrienskies/mod/common/config/DimensionParametersResolver.kt"
path = root / rel
text = path.read_text(encoding="utf-8")

old_gson_import = "import com.google.gson.Gson\n"
identifier_import = "import net.minecraft.resources.Identifier\n"
listener_import = "import net.minecraft.server.packs.resources.SimpleJsonResourceReloadListener\n"
new_converter_import = "import net.minecraft.resources.FileToIdConverter\n"
new_codec_import = "import net.minecraft.util.ExtraCodecs\n"
old_decl = 'object DimensionParametersResolver: SimpleJsonResourceReloadListener(Gson(), "vs_dimension_parameters") {'
new_decl = 'object DimensionParametersResolver: SimpleJsonResourceReloadListener<JsonElement>(ExtraCodecs.JSON, FileToIdConverter.json("vs_dimension_parameters")) {'

# Pin the already-proven Identifier overlay and the upstream apply/parser shape so
# this listener migration cannot silently absorb unrelated semantic changes.
expected_apply = """    override fun apply(\n        objects: Map<Identifier?, JsonElement?>,\n        resourceManager: ResourceManager,\n        profiler: ProfilerFiller\n    ) {\n"""
expected_parse = '    private fun parse(element: JsonElement, map: MutableMap<String, Parameters>) {'
expected_null_guard = '            if (key == null || value == null) {return@forEach}'
expected_priority = '            if (it.priority < priority) {'

if text.count(old_gson_import) != 1:
    raise SystemExit(f"expected exactly one legacy Gson import in {rel}")
if text.count(old_decl) != 1:
    raise SystemExit(f"expected exactly one legacy reload-listener declaration in {rel}")
if text.count(identifier_import) != 1:
    raise SystemExit(f"expected prior Identifier overlay to be present exactly once in {rel}")
if text.count(listener_import) != 1:
    raise SystemExit(f"expected exactly one SimpleJsonResourceReloadListener import in {rel}")
if expected_apply not in text:
    raise SystemExit(f"expected pinned nullable apply shape in {rel}")
if text.count(expected_parse) != 1:
    raise SystemExit(f"expected pinned parse routine in {rel}")
if text.count(expected_null_guard) != 1:
    raise SystemExit(f"expected pinned null guard in {rel}")
if text.count(expected_priority) != 1:
    raise SystemExit(f"expected pinned priority-selection behavior in {rel}")
if new_converter_import in text or new_codec_import in text or new_decl in text:
    raise SystemExit(f"typed reload-listener adaptation already present in {rel}")

text = text.replace(old_gson_import, "", 1)
text = text.replace(identifier_import, identifier_import + new_converter_import, 1)
text = text.replace(listener_import, listener_import + new_codec_import, 1)
text = text.replace(old_decl, new_decl, 1)

if "Gson()" in text or old_decl in text:
    raise SystemExit(f"legacy reload-listener constructor remained in {rel}")
if text.count(new_decl) != 1:
    raise SystemExit(f"expected exactly one typed reload-listener declaration after overlay in {rel}")
if text.count('FileToIdConverter.json("vs_dimension_parameters")') != 1:
    raise SystemExit(f"expected exactly one vs_dimension_parameters FileToIdConverter after overlay in {rel}")
if text.count("ExtraCodecs.JSON") != 1:
    raise SystemExit(f"expected exactly one raw JSON codec after overlay in {rel}")
if expected_apply not in text or text.count(expected_parse) != 1 or text.count(expected_null_guard) != 1 or text.count(expected_priority) != 1:
    raise SystemExit(f"upstream apply/parser semantics changed unexpectedly in {rel}")

path.write_text(text, encoding="utf-8")
print("P1_DIMENSIONPARAMETERSRESOLVER_RELOAD_LISTENER_26_2_OVERLAY_APPLIED")
