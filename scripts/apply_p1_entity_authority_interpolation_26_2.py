#!/usr/bin/env python3
"""Fail-closed Minecraft 26.2 entity authority/interpolation API bridge.

This adapts only the removed vanilla Entity authority/interpolation API calls used
by pinned upstream VS2. It preserves the existing VS2 packet/entity-dragging
architecture and does not add movement, carry, collision, camera, or teleport
logic.
"""

from pathlib import Path
import sys

VS_GAME_PACKETS = Path("common/src/main/kotlin/org/valkyrienskies/mod/common/networking/VSGamePackets.kt")
ENTITY_DRAGGER = Path("common/src/main/kotlin/org/valkyrienskies/mod/common/util/EntityDragger.kt")

OLD_AUTH = "entity.isControlledByLocalInstance"
NEW_AUTH = "entity.isLocalInstanceAuthoritative()"
OLD_LERP = (
    "entity.lerpTo(worldPosition.x, worldPosition.y, worldPosition.z, "
    "Math.toDegrees(setMotion.yRot).toFloat(), Math.toDegrees(setMotion.xRot).toFloat(), 3)"
)
NEW_LERP = (
    "entity.moveOrInterpolateTo(Vec3(worldPosition.x, worldPosition.y, worldPosition.z), "
    "Math.toDegrees(setMotion.yRot).toFloat(), Math.toDegrees(setMotion.xRot).toFloat())"
)

# These existing upstream operations are authority-sensitive. This overlay may
# not add/remove any of them while replacing the obsolete vanilla API boundary.
PRESERVE_COUNTS = (
    "setPos(",
    "setDeltaMovement(",
    ".push(",
    "teleport",
    "boundingBox =",
)


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {sys.argv[0]} <upstream-vs2-root>")

    root = Path(sys.argv[1])
    packets_path = root / VS_GAME_PACKETS
    dragger_path = root / ENTITY_DRAGGER
    if not packets_path.is_file() or not dragger_path.is_file():
        raise SystemExit("fail-closed: pinned authority semantic-unit source files are missing")

    packets = packets_path.read_text(encoding="utf-8")
    dragger = dragger_path.read_text(encoding="utf-8")

    if packets.count(OLD_AUTH) != 2:
        raise SystemExit(
            f"fail-closed: expected exactly two VSGamePackets old authority calls, found {packets.count(OLD_AUTH)}"
        )
    if dragger.count(OLD_AUTH) != 1:
        raise SystemExit(
            f"fail-closed: expected exactly one EntityDragger old authority call, found {dragger.count(OLD_AUTH)}"
        )
    if packets.count(OLD_LERP) != 1:
        raise SystemExit(
            f"fail-closed: expected exactly one pinned VSGamePackets lerpTo call, found {packets.count(OLD_LERP)}"
        )

    # Anchor the semantic roles rather than replacing same-named methods blindly.
    required_packet_context = (
        "PacketEntityShipMotion::class.registerClientHandler",
        "PacketMobShipRotation::class.registerClientHandler",
        "if(entity !is LivingEntity)",
        "entity.draggingInformation.lerpSteps = 3",
    )
    for anchor in required_packet_context:
        if anchor not in packets:
            raise SystemExit(f"fail-closed: VSGamePackets authority/interpolation anchor changed: {anchor}")

    required_dragger_context = (
        "fun dragEntitiesWithShips",
        "if (!entity.isControlledByLocalInstance && entity !is Player)",
        "entityDraggingInformation.addedYawRotLastTick = addedYRot",
    )
    for anchor in required_dragger_context:
        if anchor not in dragger:
            raise SystemExit(f"fail-closed: EntityDragger authority anchor changed: {anchor}")

    before_counts = {
        (path, token): text.count(token)
        for path, text in ((VS_GAME_PACKETS, packets), (ENTITY_DRAGGER, dragger))
        for token in PRESERVE_COUNTS
    }

    packets_new = packets.replace(OLD_AUTH, NEW_AUTH)
    packets_new = packets_new.replace(OLD_LERP, NEW_LERP, 1)
    dragger_new = dragger.replace(OLD_AUTH, NEW_AUTH)

    if OLD_AUTH in packets_new or OLD_AUTH in dragger_new:
        raise SystemExit("fail-closed: obsolete isControlledByLocalInstance call remains")
    if OLD_LERP in packets_new:
        raise SystemExit("fail-closed: obsolete lerpTo call remains")
    if packets_new.count(NEW_AUTH) != 2 or dragger_new.count(NEW_AUTH) != 1:
        raise SystemExit("fail-closed: current authority predicate replacement count mismatch")
    if packets_new.count(NEW_LERP) != 1:
        raise SystemExit("fail-closed: current moveOrInterpolateTo replacement count mismatch")

    after_counts = {
        (path, token): text.count(token)
        for path, text in ((VS_GAME_PACKETS, packets_new), (ENTITY_DRAGGER, dragger_new))
        for token in PRESERVE_COUNTS
    }
    if before_counts != after_counts:
        changes = [
            f"{path}:{token} {before_counts[(path, token)]}->{after_counts[(path, token)]}"
            for path, token in before_counts
            if before_counts[(path, token)] != after_counts[(path, token)]
        ]
        raise SystemExit("fail-closed: overlay changed existing movement-authority operations: " + ", ".join(changes))

    packets_path.write_text(packets_new, encoding="utf-8")
    dragger_path.write_text(dragger_new, encoding="utf-8")
    print("P1_ENTITY_AUTHORITY_INTERPOLATION_26_2_OVERLAY_APPLIED")


if __name__ == "__main__":
    main()
