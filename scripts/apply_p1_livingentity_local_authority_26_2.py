#!/usr/bin/env python3
"""Adapt one real-VS2 local-control query to Minecraft 26.2 authority vocabulary.

Pinned Minecraft-era Entity.isControlledByLocalInstance() semantics were:
- controlling Player -> Player.isLocalPlayer();
- otherwise -> server-side effective AI.

Minecraft 26.2 expresses the same ownership split with the public final
Entity.isLocalInstanceAuthoritative(): on the client it delegates to local-client
authority, while on the server it is the inverse of client authority. Player remains
client-authoritative and locally authoritative only for the local player.

Change only that query in VS2's existing dragged-entity lerp guard. Do not alter ship
lookup, dragging state, lerp execution, player fallback, tick timing, or camera/player
authority beyond the Minecraft vocabulary replacement.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/feature/entity_collision/MixinLivingEntity.java"
if not path.is_file():
    raise SystemExit(f"fail-closed: expected pinned VS2 MixinLivingEntity source missing: {path}")

text = path.read_text(encoding="utf-8")
old = "this.isControlledByLocalInstance()"
new = "this.isLocalInstanceAuthoritative()"

anchors = (
    "if (this.level() != null && this.level().isClientSide() && !firstTick)",
    "(((Entity) this instanceof Player player) && player.isLocalPlayer())",
    "((IEntityDraggingInformationProvider) this).getDraggingInformation()",
    "dragInfo.getLastShipStoodOn()",
    "VSGameUtilsKt.getShipObjectWorld(level()).getAllShips().getById(dragInfo.getLastShipStoodOn())",
    "EntityLerper.INSTANCE.lerpStep(dragInfo, ship, (LivingEntity) (Object) this);",
    "EntityLerper.INSTANCE.lerpHeadStep(dragInfo, ship, (LivingEntity) (Object) this);",
)

if text.count(old) != 1:
    raise SystemExit(f"fail-closed: expected exactly one legacy local-control query, found {text.count(old)}")
if new in text:
    raise SystemExit("fail-closed: Minecraft 26.2 local-instance authority query already present")
for anchor in anchors:
    if text.count(anchor) != 1:
        raise SystemExit(f"fail-closed: preserved dragged-entity authority anchor changed: {anchor!r} count={text.count(anchor)}")

text = text.replace(old, new, 1)

if old in text or text.count(new) != 1:
    raise SystemExit("fail-closed: local-authority vocabulary replacement did not converge exactly once")
for anchor in anchors:
    if text.count(anchor) != 1:
        raise SystemExit(f"fail-closed: dragged-entity authority anchor changed after replacement: {anchor!r}")

path.write_text(text, encoding="utf-8")
print("P1_LIVINGENTITY_LOCAL_AUTHORITY_26_2_OVERLAY_APPLIED count=1")
