#!/usr/bin/env python3
"""Apply the isolated Minecraft 26.2 registry-tag lookup adaptation.

The pinned upstream VS2 MassDatapackResolver defers tag-backed mass entries until
VSGameEvents.tagsAreLoaded, then looks up each TagKey in BuiltInRegistries.BLOCK.
Minecraft 26.2 exposes HolderLookup/Registry tag lookup as get(TagKey), returning
Optional<HolderSet.Named<T>>, instead of the legacy getTag(TagKey) call.

This fail-closed overlay changes exactly that method vocabulary. It deliberately
preserves the upstream tagsAreLoaded timing, nullable Optional wrapper, missing-tag
warning/skip behavior, holder iteration, priority/application path, block-key lookup,
and all block-state/physics registration semantics.

Run this only after apply_p1_massdatapackresolver_reload_listener_26_2.py.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
rel = "common/src/main/kotlin/org/valkyrienskies/mod/common/config/MassDatapackResolver.kt"
path = root / rel
text = path.read_text(encoding="utf-8")

old_lookup = "                        BuiltInRegistries.BLOCK.getTag(TagKey.create(Registries.BLOCK, tagInfo.id))"
new_lookup = "                        BuiltInRegistries.BLOCK.get(TagKey.create(Registries.BLOCK, tagInfo.id))"

# Pin the surrounding real upstream deferred-tag semantics so this overlay cannot
# silently absorb parsing, timing, priority, registration, or missing-tag changes.
expected_event = "            VSGameEvents.tagsAreLoaded.on { _, _ ->"
expected_optional_type = "                    val tag: Optional<HolderSet.Named<Block>>? ="
expected_presence = "                        if (!tag.isPresent) {"
expected_warning = "                            logger.warn(\"No specified tag '${tagInfo.id}' doesn't exist!\")"
expected_skip = "                            return@forEach"
expected_iteration = "                        tag.get().forEach {"
expected_registry_key = "                                    BuiltInRegistries.BLOCK.getKey(it.value()), tagInfo.priority, tagInfo.mass, tagInfo.friction,"
expected_deferred_add = "        private fun addToBeAddedTags(tag: VSBlockStateInfo) {"

if text.count(old_lookup) != 1:
    raise SystemExit(f"expected exactly one legacy registry getTag lookup in {rel}, found {text.count(old_lookup)}")
if new_lookup in text:
    raise SystemExit(f"Minecraft 26.2 registry get(TagKey) lookup already present in {rel}")

for needle, label in [
    (expected_event, "tagsAreLoaded event"),
    (expected_optional_type, "nullable Optional declaration"),
    (expected_presence, "missing-tag presence check"),
    (expected_warning, "missing-tag warning"),
    (expected_skip, "missing-tag skip"),
    (expected_iteration, "tag holder iteration"),
    (expected_registry_key, "block key/priority application"),
    (expected_deferred_add, "deferred tag collection"),
]:
    if text.count(needle) != 1:
        raise SystemExit(f"expected pinned {label} exactly once in {rel}")

text = text.replace(old_lookup, new_lookup, 1)

if old_lookup in text:
    raise SystemExit(f"legacy getTag lookup remained in {rel}")
if text.count(new_lookup) != 1:
    raise SystemExit(f"expected exactly one Minecraft 26.2 get(TagKey) lookup after overlay in {rel}")

for needle, label in [
    (expected_event, "tagsAreLoaded event"),
    (expected_optional_type, "nullable Optional declaration"),
    (expected_presence, "missing-tag presence check"),
    (expected_warning, "missing-tag warning"),
    (expected_skip, "missing-tag skip"),
    (expected_iteration, "tag holder iteration"),
    (expected_registry_key, "block key/priority application"),
    (expected_deferred_add, "deferred tag collection"),
]:
    if text.count(needle) != 1:
        raise SystemExit(f"pinned {label} changed unexpectedly in {rel}")

path.write_text(text, encoding="utf-8")
print("P1_MASSDATAPACKRESOLVER_REGISTRY_TAG_26_2_OVERLAY_APPLIED")
