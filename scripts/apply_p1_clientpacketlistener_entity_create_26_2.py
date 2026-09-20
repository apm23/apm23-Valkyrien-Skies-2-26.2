#!/usr/bin/env python3
"""Adapt only MixinClientPacketListener's client entity creation call to Minecraft 26.2.

Pinned VS2 intercepts ClientboundAddEntityPacket for the real SHIP_MOUNTING_ENTITY_TYPE,
cancels vanilla handling, and creates that same entity type on the ClientLevel before applying
packet position/rotation/id/UUID and adding it to the level. Minecraft 26.2 vanilla
ClientPacketListener.createEntityFromPacket() creates non-player packet entities with
EntityType.create(level, EntitySpawnReason.LOAD).

This overlay changes only that create() API boundary. It intentionally leaves the separate
removed Entity.moveTo(...) call untouched for its own evidence/proof unit, and preserves packet
cancellation, SHIP_MOUNTING_ENTITY_TYPE authority, packet position codec sync, rotation, id/UUID,
level.addEntity(), and the existing VS2 ship teleport interpolation behavior.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/client/multiplayer/MixinClientPacketListener.java"
if not path.is_file():
    raise SystemExit(f"fail-closed: expected pinned VS2 MixinClientPacketListener source missing: {path}")

text = path.read_text(encoding="utf-8")

import_anchor = "import net.minecraft.world.entity.Entity;\n"
spawn_import = "import net.minecraft.world.entity.EntitySpawnReason;\n"
old = "final Entity entity = ValkyrienSkiesMod.SHIP_MOUNTING_ENTITY_TYPE.create(level);"
new = "final Entity entity = ValkyrienSkiesMod.SHIP_MOUNTING_ENTITY_TYPE.create(level, EntitySpawnReason.LOAD);"

if text.count(import_anchor) != 1:
    raise SystemExit(f"fail-closed: expected one Entity import anchor, found {text.count(import_anchor)}")
if spawn_import in text:
    raise SystemExit("fail-closed: EntitySpawnReason import already present before creation adaptation")
if text.count(old) != 1:
    raise SystemExit(f"fail-closed: expected one legacy SHIP_MOUNTING_ENTITY_TYPE.create(level) site, found {text.count(old)}")
if "SHIP_MOUNTING_ENTITY_TYPE.create(level," in text:
    raise SystemExit("fail-closed: client mounting-entity creation adaptation already partially present")

# Guard the exact real-VS2 client spawn lifecycle and independent move/teleport units.
anchors = {
    "if (packet.getType().equals(ValkyrienSkiesMod.SHIP_MOUNTING_ENTITY_TYPE)) {": 1,
    "ci.cancel();": 1,
    "final double d = packet.getX();": 1,
    "final double e = packet.getY();": 1,
    "final double f = packet.getZ();": 1,
    "final int i = packet.getId();": 1,
    "entity.syncPacketPositionCodec(d, e, f);": 1,
    "entity.moveTo(d, e, f);": 1,
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

text = text.replace(import_anchor, import_anchor + spawn_import, 1)
text = text.replace(old, new, 1)

if text.count(spawn_import) != 1:
    raise SystemExit(f"fail-closed: expected one EntitySpawnReason import, found {text.count(spawn_import)}")
if text.count(new) != 1:
    raise SystemExit(f"fail-closed: expected one LOAD creation call after adaptation, found {text.count(new)}")
if "SHIP_MOUNTING_ENTITY_TYPE.create(level);" in text:
    raise SystemExit("fail-closed: legacy create(level) remains")
# Do not consume the second compile frontier in this unit.
if text.count("entity.moveTo(d, e, f);") != 1:
    raise SystemExit("fail-closed: independent moveTo frontier changed unexpectedly")

for anchor, expected in anchors.items():
    actual = text.count(anchor)
    if actual != expected:
        raise SystemExit(f"fail-closed: ClientPacketListener lifecycle anchor changed after adaptation: {anchor!r} count={actual} expected={expected}")

path.write_text(text, encoding="utf-8")
print("P1_CLIENTPACKETLISTENER_ENTITY_CREATE_26_2_OVERLAY_APPLIED")
