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

# Run 35331485313 proved ValkyrienSkies.kt is now clean and reported a direct private
# Direction.normal access in TestFlapBlock#getWing. Pinned baseline and current 1.21.1/main
# are byte-identical at this callsite. Replace only that unit-vector accessor; Wing
# construction, coefficients, and toJOMLD conversion remain unchanged.
replace_count(
    "common/src/main/kotlin/org/valkyrienskies/mod/common/block/TestFlapBlock.kt",
    "blockState.getValue(FACING).normal.toJOMLD()",
    "blockState.getValue(FACING).getUnitVec3i().toJOMLD()",
    1,
)

# Run 35333733932 proved TestFlapBlock.kt is now clean and reports the same single private
# Direction.normal access in TestWingBlock#getWing. Pinned baseline and current 1.21.1/main
# are byte-identical at blob 0728a94852bd0adbe5fe9d3bcbd7ee719d54bb6b. Replace only
# that unit-vector accessor; Wing construction, coefficients, camber bias, and toJOMLD stay unchanged.
replace_count(
    "common/src/main/kotlin/org/valkyrienskies/mod/common/block/TestWingBlock.kt",
    "blockState.getValue(FACING).normal.toJOMLD()",
    "blockState.getValue(FACING).getUnitVec3i().toJOMLD()",
    1,
)

# Run 35334206051 proved TestWingBlock.kt clean and reports exactly one private
# Direction.normal access in TestThrusterBlockEntity#physTick. Pinned baseline and current
# 1.21.1/main are byte-identical at blob e1491b05b5b8f91cb8a6ffd1de2fdd3df7554e53.
# Replace only the direction unit-vector accessor; applyModelForce, force magnitude,
# application point, activity/null guards, and physics-listener semantics stay unchanged.
replace_count(
    "common/src/main/kotlin/org/valkyrienskies/mod/common/blockentity/TestThrusterBlockEntity.kt",
    "facing.normal.toJOMLD()",
    "facing.getUnitVec3i().toJOMLD()",
    1,
)

# Run 35336506362 proved TestThrusterBlockEntity.kt clean and exposed one direct standalone
# Minecraft 26.2 override drift in TestThrusterBlock#neighborChanged. Pinned baseline and
# current 1.21.1/main are byte-identical at blob d8bd39c9d3c92de942968cfb95bd807f1cfd3f19.
# Minecraft 26.2 replaces the old neighbor BlockPos parameter with nullable Orientation.
# The old final BlockPos/Boolean parameters are unused by VS2 here, so change only the import
# and override signature; redstone state transitions and block-entity activation remain unchanged.
replace_count(
    "common/src/main/kotlin/org/valkyrienskies/mod/common/block/TestThrusterBlock.kt",
    "import net.minecraft.world.level.block.state.properties.BlockStateProperties\n",
    "import net.minecraft.world.level.block.state.properties.BlockStateProperties\nimport net.minecraft.world.level.redstone.Orientation\n",
    1,
)
replace_count(
    "common/src/main/kotlin/org/valkyrienskies/mod/common/block/TestThrusterBlock.kt",
    "blockState: BlockState, level: Level, blockPos: BlockPos, block: Block, blockPos2: BlockPos, bl: Boolean",
    "blockState: BlockState, level: Level, blockPos: BlockPos, block: Block, orientation: Orientation?, movedByPiston: Boolean",
    1,
)

# Run 35337116568 proved TestThrusterBlock.kt clean and exposed exactly two direct
# Minecraft 26.2 compile errors in RaycastUtils.kt. Pinned baseline and current 1.21.1/main
# are byte-identical at blob 97fa4f9fcc776cd1b6445d130087306f7c8fe800.
# 26.2 renamed the floating-point vector-direction lookup to getApproximateNearest(); use
# that exact replacement without altering miss-position or ship/world clip selection.
replace_count(
    "common/src/main/kotlin/org/valkyrienskies/mod/common/world/RaycastUtils.kt",
    "Direction.getNearest(line.x, line.y, line.z)",
    "Direction.getApproximateNearest(line.x, line.y, line.z)",
    1,
)

# The same run reports Kotlin nullable location at EntityHitResult construction, whose 26.2
# constructor requires a non-null Vec3. Upstream assigns location in every branch that assigns
# resultEntity, and construction already occurs only when resultEntity != null. Assert that
# existing paired invariant only; do not introduce a fallback hit position or raycast behavior.
replace_count(
    "common/src/main/kotlin/org/valkyrienskies/mod/common/world/RaycastUtils.kt",
    "EntityHitResult(resultEntity, location)",
    "EntityHitResult(resultEntity, location!!)",
    1,
)

# Run 35338858979 proved RaycastUtils.kt clean and reports exactly two removed legacy
# integer permission-level calls in MinecraftPlayer.kt. Pinned baseline and current
# 1.21.1/main are byte-identical at blob c11d83b71dc7be4144fb9473ac76636f458898a5.
# Minecraft 26.2 maps the old command level 4 to PermissionLevel.OWNERS and exposes that
# threshold as Permissions.COMMANDS_OWNER. Adapt only the permission predicate; keep the
# physical-client shortcut and every VsiPlayer wrapper/reference-state behavior unchanged.
replace_count(
    "common/src/main/kotlin/org/valkyrienskies/mod/common/util/MinecraftPlayer.kt",
    "import net.minecraft.world.entity.player.Player\n",
    "import net.minecraft.server.permissions.Permissions\nimport net.minecraft.world.entity.player.Player\n",
    1,
)
replace_count(
    "common/src/main/kotlin/org/valkyrienskies/mod/common/util/MinecraftPlayer.kt",
    "player.hasPermissions(4)",
    "player.permissions().hasPermission(Permissions.COMMANDS_OWNER)",
    2,
)

# Run 35340545586 proved MinecraftPlayer.kt clean and reports one direct removed legacy
# CommandSourceStack.hasPermission(Int) call in BackendCommand.kt. Pinned baseline and current
# 1.21.1/main are byte-identical at blob 46778377f9235c4f3492ea3c7b1bb2ef4c4fb8cf.
# The configured threshold is explicitly constrained to 0..4. Minecraft 26.2 represents the
# same command-level predicate as Permission.HasCommandLevel(PermissionLevel.byId(level)).
# Adapt only this predicate; backend/lod execution, config mutation, and messages stay unchanged.
replace_count(
    "common/src/main/kotlin/org/valkyrienskies/mod/common/command/commands/BackendCommand.kt",
    "import net.minecraft.network.chat.Component\n",
    "import net.minecraft.network.chat.Component\nimport net.minecraft.server.permissions.Permission\nimport net.minecraft.server.permissions.PermissionLevel\n",
    1,
)
replace_count(
    "common/src/main/kotlin/org/valkyrienskies/mod/common/command/commands/BackendCommand.kt",
    ".requires{ it.hasPermission(VSGameConfig.SERVER.Commands.changeBackendCommandPerms)}",
    ".requires{ it.permissions().hasPermission(Permission.HasCommandLevel(PermissionLevel.byId(VSGameConfig.SERVER.Commands.changeBackendCommandPerms)))}",
    1,
)

# Run 35342297011 proved BackendCommand.kt clean and reports exactly one removed legacy
# CommandSourceStack.hasPermission(Int) call in GetAirCommand.kt. Pinned baseline and current
# 1.21.1/main are byte-identical at blob c7048590927798690821a4135745c7fd020c218a.
# getAirValuesPerms is explicitly constrained to 0..4 and defaults to 0. Preserve that exact
# command-level threshold with Minecraft 26.2's Permission.HasCommandLevel representation.
# Adapt only the permission imports and predicate; aerodynamic lookups, dimension handling,
# messages, return values, and command structure stay unchanged.
replace_count(
    "common/src/main/kotlin/org/valkyrienskies/mod/common/command/commands/GetAirCommand.kt",
    "import net.minecraft.network.chat.Component.translatable\n",
    "import net.minecraft.network.chat.Component.translatable\nimport net.minecraft.server.permissions.Permission\nimport net.minecraft.server.permissions.PermissionLevel\n",
    1,
)
replace_count(
    "common/src/main/kotlin/org/valkyrienskies/mod/common/command/commands/GetAirCommand.kt",
    "literal(\"get-air\").requires { it.hasPermission(VSGameConfig.SERVER.Commands.getAirValuesPerms)}",
    "literal(\"get-air\").requires { it.permissions().hasPermission(Permission.HasCommandLevel(PermissionLevel.byId(VSGameConfig.SERVER.Commands.getAirValuesPerms)))}",
    1,
)

print("P1_SOURCE_API_26_2_OVERLAY_APPLIED")
