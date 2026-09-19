#!/usr/bin/env python3
"""Fail-closed Minecraft 26.2 shipyard teleport API bridge.

This adapts only the pinned upstream VS2 teleport API/mixin boundary from
RelativeMovement + the pre-26.2 teleport signatures to Minecraft 26.2's
Relative + PositionMoveRotation API. The existing VS2 ship transform remains
the only shipyard-to-world authority. Vanilla 26.2 retains teleport state,
player position application, relative rotation/delta semantics, and packet I/O.
"""

from pathlib import Path
import sys

MIXIN_ENTITY = Path("common/src/main/java/org/valkyrienskies/mod/mixin/feature/shipyard_entities/MixinEntity.java")
MIXIN_SERVER_PLAYER = Path("common/src/main/java/org/valkyrienskies/mod/mixin/server/command/level/MixinServerPlayer.java")
MIXIN_PACKET_LISTENER = Path("common/src/main/java/org/valkyrienskies/mod/mixin/server/network/MixinServerGamePacketListenerImpl.java")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"fail-closed: expected exactly one {label}, found {count}")
    return text.replace(old, new, 1)


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {sys.argv[0]} <upstream-vs2-root>")

    root = Path(sys.argv[1])
    entity_path = root / MIXIN_ENTITY
    player_path = root / MIXIN_SERVER_PLAYER
    listener_path = root / MIXIN_PACKET_LISTENER
    for path in (entity_path, player_path, listener_path):
        if not path.is_file():
            raise SystemExit(f"fail-closed: pinned teleport source missing: {path}")

    entity = entity_path.read_text(encoding="utf-8")
    player = player_path.read_text(encoding="utf-8")
    listener = listener_path.read_text(encoding="utf-8")

    entity_anchors = (
        "private boolean isModifyingTeleport = false;",
        "VSEntityManager.INSTANCE.getHandler(Entity.class.cast(this))",
        ".getTeleportPos(Entity.class.cast(this), new Vector3d(d, e, f));",
    )
    player_anchors = (
        "VSGameUtilsKt.getShipManagingPos(level, x, y, z)",
        "ship.getTransform().getShipToWorld().transformDirection(lookVector)",
        "((IEntityDraggingInformationProvider)this).vs$dragImmediately(ship);",
    )
    listener_anchors = (
        "// Bed Bug",
        "VSGameConfig.SERVER.getTransformTeleports()",
        "VSGameUtilsKt.getShipManagingPos((ServerLevel) player.level(), blockPos)",
        "ship.getShipToWorld().transformPosition(pos);",
    )
    for label, text, anchors in (
        ("MixinEntity", entity, entity_anchors),
        ("MixinServerPlayer", player, player_anchors),
        ("MixinServerGamePacketListenerImpl", listener, listener_anchors),
    ):
        for anchor in anchors:
            if anchor not in text:
                raise SystemExit(f"fail-closed: {label} teleport anchor changed: {anchor}")

    entity = replace_once(
        entity,
        "import net.minecraft.world.entity.RelativeMovement;",
        "import net.minecraft.world.entity.Relative;",
        "MixinEntity RelativeMovement import",
    )
    entity = replace_once(
        entity,
        "public abstract boolean teleportTo(ServerLevel serverLevel, double d, double e, double f, Set<RelativeMovement> set, float g, float h);",
        "public abstract boolean teleportTo(ServerLevel serverLevel, double d, double e, double f, Set<Relative> set, float g, float h, boolean resetCamera);",
        "MixinEntity teleport shadow",
    )
    entity = replace_once(
        entity,
        'method = "teleportTo(Lnet/minecraft/server/level/ServerLevel;DDDLjava/util/Set;FF)Z",',
        'method = "teleportTo(Lnet/minecraft/server/level/ServerLevel;DDDLjava/util/Set;FFZ)Z",',
        "MixinEntity teleport descriptor",
    )
    entity = replace_once(
        entity,
        "private void beforeTeleportTo(ServerLevel serverLevel, double d, double e, double f, Set<RelativeMovement> set, float g, float h, final CallbackInfoReturnable<Boolean> ci) {",
        "private void beforeTeleportTo(ServerLevel serverLevel, double d, double e, double f, Set<Relative> set, float g, float h, boolean resetCamera, final CallbackInfoReturnable<Boolean> ci) {",
        "MixinEntity teleport handler signature",
    )
    entity = replace_once(
        entity,
        "teleportTo(serverLevel, pos.x, pos.y, pos.z, set, g, h);",
        "teleportTo(serverLevel, pos.x, pos.y, pos.z, set, g, h, resetCamera);",
        "MixinEntity transformed teleport recursion",
    )

    player = replace_once(
        player,
        "import net.minecraft.world.entity.RelativeMovement;",
        "import net.minecraft.world.entity.Relative;",
        "MixinServerPlayer RelativeMovement import",
    )
    player = replace_once(
        player,
        "public abstract boolean teleportTo(ServerLevel serverLevel, double d, double e, double f, Set<RelativeMovement> set, float g, float h);",
        "public abstract boolean teleportTo(ServerLevel serverLevel, double d, double e, double f, Set<Relative> set, float g, float h, boolean resetCamera);",
        "MixinServerPlayer teleport shadow",
    )
    player = replace_once(
        player,
        "this.teleportTo(level, inWorldNext.x, inWorldNext.y, inWorldNext.z, Set.of(), this.getYRot(), this.getXRot());",
        "this.teleportTo(level, inWorldNext.x, inWorldNext.y, inWorldNext.z, Set.of(), this.getYRot(), this.getXRot(), false);",
        "MixinServerPlayer dismount teleport call",
    )

    listener = replace_once(
        listener,
        "import com.llamalad7.mixinextras.injector.ModifyExpressionValue;\n",
        "import com.llamalad7.mixinextras.injector.ModifyExpressionValue;\nimport com.llamalad7.mixinextras.injector.wrapmethod.WrapMethod;\n",
        "packet-listener WrapMethod import",
    )
    listener = replace_once(
        listener,
        "import java.util.Collections;\nimport java.util.Set;",
        "import java.util.EnumSet;\nimport java.util.Set;",
        "packet-listener collection imports",
    )
    listener = replace_once(
        listener,
        "import net.minecraft.network.protocol.game.ClientboundPlayerPositionPacket;\n",
        "",
        "packet-listener obsolete player-position packet import",
    )
    listener = replace_once(
        listener,
        "import net.minecraft.world.entity.RelativeMovement;\n",
        "import net.minecraft.world.entity.PositionMoveRotation;\nimport net.minecraft.world.entity.Relative;\n",
        "packet-listener teleport type imports",
    )

    old_shadows = '''    @Shadow\n    private int awaitingTeleport;\n\n    @Shadow\n    private int tickCount;\n\n    @Shadow\n    private Vec3 awaitingPositionFromClient;\n\n    @Shadow\n    private int awaitingTeleportTime;\n\n'''
    listener = replace_once(listener, old_shadows, "", "obsolete manual teleport bookkeeping shadows")

    old_method = '''    @Inject(\n        method = "teleport(DDDFFLjava/util/Set;)V",\n        at = @At(value = "HEAD"),\n        cancellable = true\n    )\n    private void transformTeleport(final double x, final double y, final double z, final float yaw, final float pitch,\n        final Set<RelativeMovement> relativeSet, final CallbackInfo ci) {\n\n        if (!VSGameConfig.SERVER.getTransformTeleports()) {\n            return;\n        }\n\n        final BlockPos blockPos = BlockPos.containing(x, y, z);\n        final ServerShip ship = VSGameUtilsKt.getShipManagingPos((ServerLevel) player.level(), blockPos);\n\n        // TODO add flag to disable this https://github.com/ValkyrienSkies/Valkyrien-Skies-2/issues/30\n        if (ship != null) {\n            final Vector3d pos = new Vector3d(x, y, z);\n            ship.getShipToWorld().transformPosition(pos);\n\n            this.awaitingPositionFromClient = VectorConversionsMCKt.toMinecraft(pos);\n            if (++this.awaitingTeleport == Integer.MAX_VALUE) {\n                this.awaitingTeleport = 0;\n            }\n            this.awaitingTeleportTime = this.tickCount;\n            this.player.absMoveTo(pos.x, pos.y, pos.z, yaw, pitch);\n\n            this.send(\n                new ClientboundPlayerPositionPacket(pos.x, pos.y, pos.z, yaw, pitch, Collections.emptySet(),\n                    awaitingTeleport));\n            ci.cancel();\n        }\n    }\n'''
    new_method = '''    @WrapMethod(\n        method = "teleport(Lnet/minecraft/world/entity/PositionMoveRotation;Ljava/util/Set;)V"\n    )\n    private void transformTeleport(final PositionMoveRotation change, final Set<Relative> relativeSet,\n        final Operation<Void> original) {\n\n        if (!VSGameConfig.SERVER.getTransformTeleports()) {\n            original.call(change, relativeSet);\n            return;\n        }\n\n        final PositionMoveRotation absolute = PositionMoveRotation.calculateAbsolute(\n            PositionMoveRotation.of(player), change, relativeSet);\n        final Vec3 absolutePos = absolute.position();\n        final BlockPos blockPos = BlockPos.containing(absolutePos.x, absolutePos.y, absolutePos.z);\n        final ServerShip ship = VSGameUtilsKt.getShipManagingPos((ServerLevel) player.level(), blockPos);\n\n        // TODO add flag to disable this https://github.com/ValkyrienSkies/Valkyrien-Skies-2/issues/30\n        if (ship == null) {\n            original.call(change, relativeSet);\n            return;\n        }\n\n        final Vector3d pos = new Vector3d(absolutePos.x, absolutePos.y, absolutePos.z);\n        ship.getShipToWorld().transformPosition(pos);\n\n        final Set<Relative> transformedRelatives = EnumSet.noneOf(Relative.class);\n        transformedRelatives.addAll(relativeSet);\n        transformedRelatives.remove(Relative.X);\n        transformedRelatives.remove(Relative.Y);\n        transformedRelatives.remove(Relative.Z);\n\n        final PositionMoveRotation transformedChange = new PositionMoveRotation(\n            VectorConversionsMCKt.toMinecraft(pos), change.deltaMovement(), change.yRot(), change.xRot());\n        original.call(transformedChange, transformedRelatives);\n    }\n'''
    listener = replace_once(listener, old_method, new_method, "packet-listener upstream teleport transform method")

    checks = (
        (entity, "RelativeMovement", 0, "MixinEntity obsolete RelativeMovement"),
        (player, "RelativeMovement", 0, "MixinServerPlayer obsolete RelativeMovement"),
        (listener, "RelativeMovement", 0, "packet-listener obsolete RelativeMovement"),
        (listener, "awaitingTeleport", 0, "packet-listener manual awaitingTeleport authority"),
        (listener, "awaitingPositionFromClient", 0, "packet-listener manual awaiting-position authority"),
        (listener, "ClientboundPlayerPositionPacket", 0, "packet-listener manual position packet"),
        (listener, "player.absMoveTo", 0, "packet-listener manual player movement"),
        (listener, "original.call(transformedChange, transformedRelatives);", 1, "packet-listener vanilla delegation"),
    )
    for text, token, expected, label in checks:
        count = text.count(token)
        if count != expected:
            raise SystemExit(f"fail-closed: {label} count {count}, expected {expected}")

    entity_path.write_text(entity, encoding="utf-8")
    player_path.write_text(player, encoding="utf-8")
    listener_path.write_text(listener, encoding="utf-8")
    print("P1_SHIPYARD_TELEPORT_API_26_2_OVERLAY_APPLIED")


if __name__ == "__main__":
    main()
