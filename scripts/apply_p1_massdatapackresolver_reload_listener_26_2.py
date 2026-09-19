#!/usr/bin/env python3
"""Apply the isolated Minecraft 26.2 typed JSON reload-listener adaptation.

The pinned VS2 MassDatapackResolver intentionally consumes raw JsonElement values
from the `vs_mass` JSON directory, clears/rebuilds its direct block map, and
collects tag-backed entries for the later tagsAreLoaded callback. Minecraft 26.2
changed SimpleJsonResourceReloadListener from the legacy (Gson, directory)
constructor to a typed (Codec<T>, FileToIdConverter) boundary whose apply map has
non-null Identifier/T type arguments.

This fail-closed overlay changes only that reload-listener boundary. It preserves
the upstream raw JSON payload, `vs_mass` directory, map/tags clearing, object/array
parsing, priority behavior, deferred tag list, later registry-tag lookup, logging,
and all block-state/physics registration semantics. In particular, the separate
Minecraft 26.2 registry `getTag` drift is pinned but deliberately NOT changed here.

Run this only after apply_p1_massdatapackresolver_identifier_26_2.py.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
rel = "common/src/main/kotlin/org/valkyrienskies/mod/common/config/MassDatapackResolver.kt"
path = root / rel
text = path.read_text(encoding="utf-8")

old_gson_import = "import com.google.gson.Gson\n"
identifier_import = "import net.minecraft.resources.Identifier\n"
listener_import = "import net.minecraft.server.packs.resources.SimpleJsonResourceReloadListener\n"
new_converter_import = "import net.minecraft.resources.FileToIdConverter\n"
new_codec_import = "import net.minecraft.util.ExtraCodecs\n"
old_decl = '    class VSMassDataLoader : SimpleJsonResourceReloadListener(Gson(), "vs_mass") {'
new_decl = '    class VSMassDataLoader : SimpleJsonResourceReloadListener<JsonElement>(ExtraCodecs.JSON, FileToIdConverter.json("vs_mass")) {'
old_apply = """        override fun apply(\n            objects: MutableMap<Identifier, JsonElement>?,\n            resourceManager: ResourceManager?,\n            profiler: ProfilerFiller?\n        ) {\n"""
new_apply = """        override fun apply(\n            objects: MutableMap<Identifier, JsonElement>,\n            resourceManager: ResourceManager?,\n            profiler: ProfilerFiller?\n        ) {\n"""

# Pin unrelated semantics so this overlay cannot silently absorb the separate
# registry-tag/API migration or change datapack parsing behavior.
expected_map_clear = "            map.clear()"
expected_tags_clear = "            tags.clear()"
expected_iteration = "            objects?.forEach { (location, element) ->"
expected_tag_lookup = "                        BuiltInRegistries.BLOCK.getTag(TagKey.create(Registries.BLOCK, tagInfo.id))"
expected_tag_presence = "                        if (!tag.isPresent) {"
expected_parse = "        private fun parse(element: JsonElement, origin: Identifier) {"
expected_priority = "                if (map[info.id]!!.priority < info.priority) {"

if text.count(old_gson_import) != 1:
    raise SystemExit(f"expected exactly one legacy Gson import in {rel}")
if text.count(identifier_import) != 1:
    raise SystemExit(f"expected prior Identifier overlay exactly once in {rel}")
if text.count(listener_import) != 1:
    raise SystemExit(f"expected exactly one SimpleJsonResourceReloadListener import in {rel}")
if text.count(old_decl) != 1:
    raise SystemExit(f"expected exactly one legacy VSMassDataLoader declaration in {rel}")
if old_apply not in text:
    raise SystemExit(f"expected pinned nullable reload-listener apply map shape in {rel}")
for needle, label in [
    (expected_map_clear, "map clear"),
    (expected_tags_clear, "tag clear"),
    (expected_iteration, "raw JSON iteration"),
    (expected_tag_lookup, "legacy registry-tag lookup"),
    (expected_tag_presence, "tag presence handling"),
    (expected_parse, "parse routine"),
    (expected_priority, "priority replacement"),
]:
    if text.count(needle) != 1:
        raise SystemExit(f"expected pinned {label} exactly once in {rel}")
if new_converter_import in text or new_codec_import in text or new_decl in text or new_apply in text:
    raise SystemExit(f"typed reload-listener adaptation already present in {rel}")

text = text.replace(old_gson_import, "", 1)
text = text.replace(identifier_import, identifier_import + new_converter_import, 1)
text = text.replace(listener_import, listener_import + new_codec_import, 1)
text = text.replace(old_decl, new_decl, 1)
text = text.replace(old_apply, new_apply, 1)

if "Gson()" in text or old_decl in text or old_apply in text:
    raise SystemExit(f"legacy reload-listener boundary remained in {rel}")
if text.count(new_decl) != 1 or text.count(new_apply) != 1:
    raise SystemExit(f"expected exactly one typed reload-listener boundary after overlay in {rel}")
if text.count('FileToIdConverter.json("vs_mass")') != 1:
    raise SystemExit(f"expected exactly one vs_mass FileToIdConverter after overlay in {rel}")
if text.count("ExtraCodecs.JSON") != 1:
    raise SystemExit(f"expected exactly one raw JSON codec after overlay in {rel}")
# The separate tag API drift must still be present after this isolated proof.
if text.count(expected_tag_lookup) != 1 or text.count(expected_tag_presence) != 1:
    raise SystemExit(f"registry-tag behavior changed unexpectedly in {rel}")
if text.count(expected_map_clear) != 1 or text.count(expected_tags_clear) != 1 or text.count(expected_iteration) != 1:
    raise SystemExit(f"reload apply-body semantics changed unexpectedly in {rel}")
if text.count(expected_parse) != 1 or text.count(expected_priority) != 1:
    raise SystemExit(f"parser/priority semantics changed unexpectedly in {rel}")

path.write_text(text, encoding="utf-8")
print("P1_MASSDATAPACKRESOLVER_RELOAD_LISTENER_26_2_OVERLAY_APPLIED")
