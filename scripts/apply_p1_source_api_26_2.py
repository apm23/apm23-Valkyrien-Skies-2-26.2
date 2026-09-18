#!/usr/bin/env python3
"""Apply narrowly-scoped Minecraft 26.2 source API adaptations to exact upstream VS2.

This overlay is intentionally separate from the build/tooling baseline. Every edit is an
explicit, fail-closed adaptation from the pinned upstream source to Mojang's unobfuscated
26.x API names. It must not replace or emulate VS2 ship-space, physics, collision,
entity-dragging, player/camera, networking, or rendering architecture.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")


def replace_count(rel: str, old: str, new: str, expected: int) -> None:
    path = root / rel
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != expected:
        raise SystemExit(f"expected {expected} matches in {rel}: {old!r}; found {count}")
    path.write_text(text.replace(old, new), encoding="utf-8")


# Minecraft 1.21.11+/26.x renamed ResourceLocation to Identifier. These two data-provider
# files are the first compile-error cluster from exact P1 run 35316976816. They do not
# construct identifiers, so this is a direct type/import rename with no semantic rewrite.
replace_count(
    "common/src/main/kotlin/org/valkyrienskies/mod/api/datagen/VSBlockInfoDataProvider.kt",
    "ResourceLocation",
    "Identifier",
    5,
)
replace_count(
    "common/src/main/kotlin/org/valkyrienskies/mod/api/datagen/VSShipyardEntityDataProvider.kt",
    "ResourceLocation",
    "Identifier",
    3,
)

# ResourceKey#location() was renamed to ResourceKey#identifier() on the same 26.x API
# surface. Restrict the edit to the exact registry-holder callsites proven by the compiler.
replace_count(
    "common/src/main/kotlin/org/valkyrienskies/mod/api/datagen/VSBlockInfoDataProvider.kt",
    "builtInRegistryHolder().key().location()",
    "builtInRegistryHolder().key().identifier()",
    1,
)
replace_count(
    "common/src/main/kotlin/org/valkyrienskies/mod/api/datagen/VSShipyardEntityDataProvider.kt",
    "builtInRegistryHolder().key().location()",
    "builtInRegistryHolder().key().identifier()",
    1,
)

print("P1_SOURCE_API_26_2_OVERLAY_APPLIED")
