#!/usr/bin/env python3
"""Adapt only Fabric VSDataComponents generic bound required by Minecraft 26.2 DataComponentType.

Exact-head P1 compile at dfaf4a78f... proved the prior Identifier migration and left exactly
two diagnostics in VSDataComponents.kt. Both report that register<T> does not satisfy the
current DataComponentType<T : Any> bound. Preserve registration, codec, registry key, and
builder semantics; add only the non-null Kotlin upper bound required by the mapped API.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "fabric/src/main/kotlin/org/valkyrienskies/mod/fabric/common/VSDataComponents.kt"
if not path.is_file():
    raise SystemExit(f"fail-closed: pinned Fabric VSDataComponents source missing: {path}")

text = path.read_text(encoding="utf-8")
old_decl = "private fun <T> register(name: String, builder: () -> DataComponentType<T>): DataComponentType<T> {"
new_decl = "private fun <T : Any> register(name: String, builder: () -> DataComponentType<T>): DataComponentType<T> {"

anchors = {
    "object VSDataComponents {": 1,
    "import net.minecraft.resources.Identifier": 1,
    "Identifier.fromNamespaceAndPath(ValkyrienSkiesMod.MOD_ID, name)": 1,
    "BuiltInRegistries.DATA_COMPONENT_TYPE": 1,
    "builder(),": 1,
    "DataComponentType.builder<BlockPos>().persistent(BlockPos.CODEC).build()": 1,
}
for anchor, expected in anchors.items():
    actual = text.count(anchor)
    if actual != expected:
        raise SystemExit(
            f"fail-closed: VSDataComponents generic-bound semantic anchor changed: {anchor!r} count={actual} expected={expected}"
        )

if text.count(old_decl) != 1:
    raise SystemExit(f"fail-closed: expected one unbounded VSDataComponents register declaration, found {text.count(old_decl)}")
if new_decl in text:
    raise SystemExit("fail-closed: VSDataComponents generic-bound adaptation already present")

new_text = text.replace(old_decl, new_decl, 1)
if old_decl in new_text or new_text.count(new_decl) != 1:
    raise SystemExit("fail-closed: VSDataComponents generic-bound postcondition failed")
for anchor, expected in anchors.items():
    actual = new_text.count(anchor)
    if actual != expected:
        raise SystemExit(
            f"fail-closed: VSDataComponents semantic anchor changed after generic-bound adaptation: {anchor!r} count={actual} expected={expected}"
        )

path.write_text(new_text, encoding="utf-8")
print("P1_VSDATACOMPONENTS_GENERIC_BOUND_26_2_OVERLAY_APPLIED bound=T:Any sites=1")
