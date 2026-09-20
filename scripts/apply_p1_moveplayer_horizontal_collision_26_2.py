#!/usr/bin/env python3
"""Adapt the four pinned VS2 player-movement packet reconstructions to Minecraft 26.2.

Minecraft 26.2 added a horizontalCollision boolean to every ServerboundMovePlayerPacket
variant. VS2's existing wrapper intentionally changes only onGround while preserving the
rest of the vanilla packet. Forward the incoming packet's horizontalCollision() value
unchanged; do not create a new movement authority or alter ship-space motion packets.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/feature/entity_movement_packets/MixinLocalPlayer.java"
if not path.is_file():
    raise SystemExit(f"fail-closed: expected pinned VS2 MixinLocalPlayer source missing: {path}")

text = path.read_text(encoding="utf-8")

replacements = (
    (
        "new ServerboundMovePlayerPacket.PosRot(movePacket.getX(0.0), movePacket.getY(0.0), movePacket.getZ(0.0), movePacket.getYRot(0.0f), movePacket.getXRot(0.0f), isOnGround)",
        "new ServerboundMovePlayerPacket.PosRot(movePacket.getX(0.0), movePacket.getY(0.0), movePacket.getZ(0.0), movePacket.getYRot(0.0f), movePacket.getXRot(0.0f), isOnGround, movePacket.horizontalCollision())",
    ),
    (
        "new ServerboundMovePlayerPacket.Pos(movePacket.getX(0.0), movePacket.getY(0.0), movePacket.getZ(0.0), isOnGround)",
        "new ServerboundMovePlayerPacket.Pos(movePacket.getX(0.0), movePacket.getY(0.0), movePacket.getZ(0.0), isOnGround, movePacket.horizontalCollision())",
    ),
    (
        "new ServerboundMovePlayerPacket.Rot(movePacket.getYRot(0.0f), movePacket.getXRot(0.0f), isOnGround)",
        "new ServerboundMovePlayerPacket.Rot(movePacket.getYRot(0.0f), movePacket.getXRot(0.0f), isOnGround, movePacket.horizontalCollision())",
    ),
    (
        "new ServerboundMovePlayerPacket.StatusOnly(isOnGround)",
        "new ServerboundMovePlayerPacket.StatusOnly(isOnGround, movePacket.horizontalCollision())",
    ),
)

anchors = (
    "final boolean isOnGround = movePacket.isOnGround() || getDraggingInformation().isEntityBeingDraggedByAShip();",
    "PacketPlayerShipMotion packet = new PacketPlayerShipMotion(",
    "ship.getWorldToShip().transformPosition(",
    "ValkyrienSkiesMod.getVsCore().getSimplePacketNetworking().sendToServer(packet);",
    "original.call(instance, realArg);",
    "PacketEntityShipMotion packet = new PacketEntityShipMotion(",
    "original.call(instance, arg);",
)

for old, new in replacements:
    if text.count(old) != 1:
        raise SystemExit(f"fail-closed: expected exactly one legacy move-player constructor site, found {text.count(old)}: {old}")
    if new in text:
        raise SystemExit(f"fail-closed: 26.2 move-player constructor already adapted: {new}")
for anchor in anchors:
    if text.count(anchor) != 1:
        raise SystemExit(f"fail-closed: preserved VS2 movement authority anchor changed: {anchor!r} count={text.count(anchor)}")

for old, new in replacements:
    text = text.replace(old, new, 1)

for old, new in replacements:
    if old in text or text.count(new) != 1:
        raise SystemExit(f"fail-closed: move-player constructor replacement did not converge exactly once: {new}")
if text.count("movePacket.horizontalCollision()") != 4:
    raise SystemExit(f"fail-closed: expected four forwarded horizontalCollision flags, found {text.count('movePacket.horizontalCollision()')}")
for anchor in anchors:
    if text.count(anchor) != 1:
        raise SystemExit(f"fail-closed: VS2 movement authority anchor changed after adaptation: {anchor!r}")

path.write_text(text, encoding="utf-8")
print("P1_MOVEPLAYER_HORIZONTAL_COLLISION_26_2_OVERLAY_APPLIED count=4")
