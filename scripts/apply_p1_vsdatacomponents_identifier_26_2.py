#!/usr/bin/env python3
"""Adapt only Fabric VSDataComponents ResourceLocation vocabulary to Minecraft 26.2 Identifier.

Pinned upstream VS2 registers the same DATA_COMPONENT_TYPE key with
ResourceLocation.fromNamespaceAndPath(...). Exact-head P1 compile at 6b0693fe... reaches
:fabric:compileKotlin and reports only the ResourceLocation import/factory as unresolved in
this semantic unit, alongside a separate generic-bound diagnostic intentionally left untouched.
Minecraft 26.2 uses Identifier for this already-frozen resource-key vocabulary.
"""
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "fabric/src/main/kotlin/org/valkyrienskies/mod/fabric/common/VSDataComponents.kt"
if not path.is_file():
    raise SystemExit(f"fail-closed: pinned Fabric VSDataComponents source missing: {path}")

text = path.read_text(encoding="utf-8")
old_import = "import net.minecraft.resources.ResourceLocation"
new_import = "import net.minecraft.resources.Identifier"
old_factory = "ResourceLocation.fromNamespaceAndPath(ValkyrienSkiesMod.MOD_ID, name)"
new_factory = "Identifier.fromNamespaceAndPath(ValkyrienSkiesMod.MOD_ID, name)"

# Preserve registry/data-component semantics and deliberately leave the independent
# Kotlin generic-bound migration for its separately chained proof unit.
anchors = {
    "object VSDataComponents {": 1,
    "private fun <T> register(name: String, builder: () -> DataComponentType<T>): DataComponentType<T> {": 1,
    "BuiltInRegistries.DATA_COMPONENT_TYPE": 1,
    "builder(),": 1,
    "DataComponentType.builder<BlockPos>().persistent(BlockPos.CODEC).build()": 1,
}
for anchor, expected in anchors.items():
    actual = text.count(anchor)
    if actual != expected:
        raise SystemExit(
            f"fail-closed: VSDataComponents semantic anchor changed: {anchor!r} count={actual} expected={expected}"
        )

if text.count(old_import) != 1:
    raise SystemExit(f"fail-closed: expected one ResourceLocation import in {path}, found {text.count(old_import)}")
if text.count(old_factory) != 1:
    raise SystemExit(f"fail-closed: expected one ResourceLocation factory in {path}, found {text.count(old_factory)}")
if new_import in text or new_factory in text:
    raise SystemExit("fail-closed: VSDataComponents Identifier adaptation already partially present")

new_text = text.replace(old_import, new_import, 1).replace(old_factory, new_factory, 1)

if "ResourceLocation" in new_text:
    raise SystemExit("fail-closed: stale ResourceLocation vocabulary remains in VSDataComponents")
if new_text.count(new_import) != 1 or new_text.count(new_factory) != 1:
    raise SystemExit("fail-closed: VSDataComponents Identifier postcondition failed")
for anchor, expected in anchors.items():
    actual = new_text.count(anchor)
    if actual != expected:
        raise SystemExit(
            f"fail-closed: VSDataComponents semantic anchor changed after Identifier adaptation: {anchor!r} count={actual} expected={expected}"
        )

path.write_text(new_text, encoding="utf-8")
print("P1_VSDATACOMPONENTS_IDENTIFIER_26_2_OVERLAY_APPLIED generic_bound=deferred")

# The exact-head Identifier proof left only the independent Kotlin T : Any bound in this file.
# Chain that one-site API adaptation only after Identifier semantics have been preserved.
generic_bound_helper = Path(__file__).with_name("apply_p1_vsdatacomponents_generic_bound_26_2.py")
if not generic_bound_helper.is_file():
    raise SystemExit(f"fail-closed: required VSDataComponents generic-bound helper missing: {generic_bound_helper}")
subprocess.run([sys.executable, str(generic_bound_helper), str(root)], check=True)
print("P1_VSDATACOMPONENTS_GENERIC_BOUND_26_2_CHAINED")
