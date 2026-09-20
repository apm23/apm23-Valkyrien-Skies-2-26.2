#!/usr/bin/env python3
"""Adapt only MixinClientPacketListener's packet-spawn position call to Minecraft 26.2.

Pinned VS2 intercepts ClientboundAddEntityPacket for the real SHIP_MOUNTING_ENTITY_TYPE,
creates the same entity, syncs its packet-position codec, calls Entity.moveTo(x,y,z), then
applies the packet rotations/id/UUID and adds it to the ClientLevel.

The 1.21.1 Mojang moveTo(double,double,double) method is intermediary method_24203. In the
current 26.2 API that same intermediary method is named snapTo(double,double,double). Vanilla
26.2 Entity.recreateFromPacket also uses snapTo for packet position initialization after syncing
the packet-position codec. Therefore this is a vocabulary-only adaptation of that exact old
position operation, not a new teleport/carry authority.

This overlay intentionally does not call recreateFromPacket(), setPos(), or setPosRaw(), and it
preserves creation reason, packet cancellation, codec sync, explicit packet rotations, id/UUID,
level.addEntity(), and the existing VS2 teleport interpolation wrapper unchanged.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/client/multiplayer/MixinClientPacketListener.java"
if not path.is_file():
    raise SystemExit(f"fail-closed: expected pinned VS2 MixinClientPacketListener source missing: {path}")

text = path.read_text(encoding="utf-8")

old = "entity.moveTo(d, e, f);"
new = "entity.snapTo(d, e, f);"

if text.count(old) != 1:
    raise SystemExit(f"fail-closed: expected one legacy packet-position moveTo site, found {text.count(old)}")
if new in text:
    raise SystemExit("fail-closed: packet-position snapTo adaptation already present")

anchors = {
    "import net.minecraft.world.entity.EntitySpawnReason;": 1,
    "if (packet.getType().equals(ValkyrienSkiesMod.SHIP_MOUNTING_ENTITY_TYPE)) {": 1,
    "ci.cancel();": 1,
    "final double d = packet.getX();": 1,
    "final double e = packet.getY();": 1,
    "final double f = packet.getZ();": 1,
    "final Entity entity = ValkyrienSkiesMod.SHIP_MOUNTING_ENTITY_TYPE.create(level, EntitySpawnReason.LOAD);": 1,
    "final int i = packet.getId();": 1,
    "entity.syncPacketPositionCodec(d, e, f);": 1,
    "entity.setXRot((float) (packet.getXRot() * 360) / 256.0f);": 1,
    "entity.setYRot((float) (packet.getYRot() * 360) / 256.0f);": 1,
    "entity.setId(i);": 1,
    "entity.setUUID(packet.getUUID());": 1,
    "this.level.addEntity(entity);": 1,
    "private void teleportingWithNoStep(final Entity instance,": 1,
    "instance.setPos(x, y, z);": 1,
    "lerpTo.call(instance, x, y, z, yRot, xRot, 1);": 1,
}
for anchor, expected in anchors.items():
    actual = text.count(anchor)
    if actual != expected:
        raise SystemExit(f"fail-closed: preserved ClientPacketListener anchor {anchor!r} count={actual} expected={expected}")

# Do not replace the manual VS2 branch with the broader vanilla recreation lifecycle.
for forbidden in (
    "entity.recreateFromPacket(packet);",
    "entity.setPos(d, e, f);",
    "entity.setPosRaw(d, e, f);",
):
    if forbidden in text:
        raise SystemExit(f"fail-closed: forbidden broader packet-position substitution already present: {forbidden}")

text = text.replace(old, new, 1)

if old in text:
    raise SystemExit("fail-closed: legacy packet-position moveTo call remains")
if text.count(new) != 1:
    raise SystemExit(f"fail-closed: expected one packet-position snapTo call after adaptation, found {text.count(new)}")
for forbidden in (
    "entity.recreateFromPacket(packet);",
    "entity.setPos(d, e, f);",
    "entity.setPosRaw(d, e, f);",
):
    if forbidden in text:
        raise SystemExit(f"fail-closed: forbidden broader packet-position substitution introduced: {forbidden}")

for anchor, expected in anchors.items():
    actual = text.count(anchor)
    if actual != expected:
        raise SystemExit(f"fail-closed: ClientPacketListener lifecycle anchor changed after snap adaptation: {anchor!r} count={actual} expected={expected}")

path.write_text(text, encoding="utf-8")
print("P1_CLIENTPACKETLISTENER_ENTITY_SNAP_26_2_OVERLAY_APPLIED")
