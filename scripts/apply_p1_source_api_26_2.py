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

# Run 35322680307 proved the same ResourceLocation -> Identifier API rename is still the
# direct compile blocker in BlockStateInfoProvider. The four occurrences are only the import
# and Identifier arguments passed to ResourceKey/Registry; VS2 registry and block-state
# semantics remain untouched.
replace_count(
    "common/src/main/kotlin/org/valkyrienskies/mod/common/BlockStateInfoProvider.kt",
    "ResourceLocation",
    "Identifier",
    4,
)

# Run 35324164902 proved BlockStateInfoProvider is now clean and exposed the same direct
# ResourceLocation -> Identifier rename in SimpleSoundInstanceOnShip. There are exactly two
# occurrences: the import and constructor parameter type. Ship-space sound positioning,
# transform use, velocity computation, and constructor flow are left unchanged.
replace_count(
    "common/src/main/kotlin/org/valkyrienskies/mod/client/audio/SimpleSoundInstanceOnShip.kt",
    "ResourceLocation",
    "Identifier",
    2,
)

# Run 35324792402 proved SimpleSoundInstanceOnShip is now clean. VSEntityManager's direct
# errors are the same 26.x type rename plus cascaded generic/overload inference from that
# missing type. Exactly seven occurrences cover only the import, map key/value declarations,
# two registration IDs, and public handler-name parameter types; handler selection, Create
# compat routing, caches, networking, and entity-reference semantics remain unchanged.
replace_count(
    "common/src/main/kotlin/org/valkyrienskies/mod/common/entity/handling/VSEntityManager.kt",
    "ResourceLocation",
    "Identifier",
    7,
)

# Run 35325476529 proved VSEntityManager is now clean. Minecraft 26.2's entity-data API
# constrains EntityDataSerializer/EntityDataAccessor values to non-null T : Any. Preserve the
# exact upstream delegate/get/set behavior and add only the compiler-required Kotlin bounds.
replace_count(
    "common/src/main/kotlin/org/valkyrienskies/mod/util/EntityData.kt",
    "inline fun <reified T : Entity, R> defineSynced(serializer: EntityDataSerializer<R>) =",
    "inline fun <reified T : Entity, R : Any> defineSynced(serializer: EntityDataSerializer<R>) =",
    1,
)
replace_count(
    "common/src/main/kotlin/org/valkyrienskies/mod/util/EntityData.kt",
    "class EntityDataDelegate<T>(val data: EntityDataAccessor<T>) {",
    "class EntityDataDelegate<T : Any>(val data: EntityDataAccessor<T>) {",
    1,
)

# Run 35327172496 proved EntityData is now clean. Minecraft 26.2 changed CompoundTag#getDouble
# from primitive Double to Optional<Double>. NbtUtil already checks contains(...) for each key
# before every read, so explicitly falling back to 0.0 preserves the old primitive/default
# behavior without changing VS2 vector/quaternion serialization semantics.
replace_count(
    "common/src/main/kotlin/org/valkyrienskies/mod/util/NbtUtil.kt",
    "getDouble(prefix + \"x\")",
    "getDouble(prefix + \"x\").orElse(0.0)",
    2,
)
replace_count(
    "common/src/main/kotlin/org/valkyrienskies/mod/util/NbtUtil.kt",
    "getDouble(prefix + \"y\")",
    "getDouble(prefix + \"y\").orElse(0.0)",
    2,
)
replace_count(
    "common/src/main/kotlin/org/valkyrienskies/mod/util/NbtUtil.kt",
    "getDouble(prefix + \"z\")",
    "getDouble(prefix + \"z\").orElse(0.0)",
    2,
)
replace_count(
    "common/src/main/kotlin/org/valkyrienskies/mod/util/NbtUtil.kt",
    "getDouble(prefix + \"w\")",
    "getDouble(prefix + \"w\").orElse(0.0)",
    1,
)

# Run 35327644535 proved NbtUtil is now clean. Minecraft 26.x keeps Direction's unit
# block-vector semantics behind the public getUnitVec3i() accessor while the normal backing
# field is private. Adapt only the single VectorConversionsMC callsite; transform overload
# structure and JOML math stay unchanged.
replace_count(
    "common/src/main/kotlin/org/valkyrienskies/mod/util/VectorConversionsMC.kt",
    "transformDirection(dir.normal, dest)",
    "transformDirection(dir.getUnitVec3i(), dest)",
    1,
)

# Run 35329592695 proved VectorConversionsMC is now clean. ValkyrienSkies.kt contains the
# same upstream transformDirection(Direction, ...) overload and the same private Direction
# backing-field access. Adapt only that one compiler-proven callsite to the public 26.x
# accessor; API surface, overload structure, and JOML transform behavior remain unchanged.
replace_count(
    "common/src/main/kotlin/org/valkyrienskies/mod/api/ValkyrienSkies.kt",
    "transformDirection(dir.normal, dest)",
    "transformDirection(dir.getUnitVec3i(), dest)",
    1,
)

print("P1_SOURCE_API_26_2_OVERLAY_APPLIED")
