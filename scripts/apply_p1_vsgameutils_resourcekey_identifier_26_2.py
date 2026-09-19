#!/usr/bin/env python3
"""Apply the isolated Minecraft 26.2 VSGameUtils ResourceKey/Identifier boundary adaptation.

Pinned upstream VS2 f39132148e... encodes a DimensionId as
"<registry namespace>:<registry path>:<dimension namespace>:<dimension path>" and reconstructs
its ResourceKey through ResourceKeyAccessor. Minecraft 26.2 renamed ResourceLocation to
Identifier and ResourceKey.location() to ResourceKey.identifier(), while retaining the private
ResourceKey.create(Identifier, Identifier) shape and private registryName field used by the
existing mixin accessor/invoker.

This overlay preserves that exact upstream DimensionId encoding/cache/accessor architecture.
It intentionally does not touch y-range, chunk packing/tickets, ship lifecycle, transforms,
physics, collision, entity dragging, camera, networking, or authority behavior.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")


def patch(rel: str, replacements: list[tuple[str, str, int]]) -> None:
    path = root / rel
    text = path.read_text(encoding="utf-8")
    for old, new, expected in replacements:
        count = text.count(old)
        if count != expected:
            raise SystemExit(
                f"expected {expected} matches in {rel}: {old!r}; found {count}"
            )
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")


patch(
    "common/src/main/kotlin/org/valkyrienskies/mod/common/VSGameUtils.kt",
    [
        (
            "import net.minecraft.resources.ResourceLocation",
            "import net.minecraft.resources.Identifier",
            1,
        ),
        (
            "ResourceLocation.fromNamespaceAndPath(registryNamespace, registryName), ResourceLocation.fromNamespaceAndPath(namespace, name)",
            "Identifier.fromNamespaceAndPath(registryNamespace, registryName), Identifier.fromNamespaceAndPath(namespace, name)",
            1,
        ),
    ],
)

patch(
    "common/src/main/java/org/valkyrienskies/mod/mixin/accessors/resource/ResourceKeyAccessor.java",
    [
        (
            "import net.minecraft.resources.ResourceLocation;",
            "import net.minecraft.resources.Identifier;",
            1,
        ),
        (
            "ResourceLocation getRegistryName();",
            "Identifier getRegistryName();",
            1,
        ),
        (
            "static <T> ResourceKey<T> callCreate(final ResourceLocation parent, final ResourceLocation location)",
            "static <T> ResourceKey<T> callCreate(final Identifier parent, final Identifier identifier)",
            1,
        ),
    ],
)

patch(
    "common/src/main/java/org/valkyrienskies/mod/mixin/world/level/MixinLevel.java",
    [
        (
            "((ResourceKeyAccessor) dim).getRegistryName().toString() + \":\" + dim.location();",
            "((ResourceKeyAccessor) dim).getRegistryName().toString() + \":\" + dim.identifier();",
            1,
        ),
    ],
)

print("P1_VSGAMEUTILS_RESOURCEKEY_IDENTIFIER_26_2_OVERLAY_APPLIED")
