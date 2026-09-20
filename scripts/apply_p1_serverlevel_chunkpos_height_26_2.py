#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/server/world/MixinServerLevel.java"
if not path.is_file():
    raise SystemExit(f"fail-closed: expected pinned VS2 source missing: {path}")

text = path.read_text(encoding="utf-8")

replacements = [
    (
        "vs$chunksToUnload.remove(worldChunk.getPos().toLong());",
        "vs$chunksToUnload.remove(worldChunk.getPos().pack());",
        "loaded-chunk unload-delay key",
    ),
    (
        "worldChunk.getMinBuildHeight()",
        "worldChunk.getMinY()",
        "wing-scan minimum Y",
    ),
    (
        "final long chunkPos = knownChunkPosEntry.getKey().toLong();",
        "final long chunkPos = knownChunkPosEntry.getKey().pack();",
        "known-chunk packed key",
    ),
    (
        "vs$pendingForcedChunks.add(ChunkPos.asLong(chunkX, chunkZ));",
        "vs$pendingForcedChunks.add(ChunkPos.pack(chunkX, chunkZ));",
        "pending forced-chunk packed key",
    ),
]

for old, new, label in replacements:
    actual = text.count(old)
    if actual != 1:
        raise SystemExit(
            f"fail-closed: expected exactly one legacy {label} expression {old!r} in {path}, found {actual}"
        )
    if new in text:
        raise SystemExit(f"fail-closed: {label} expression already adapted before this helper")

# Require the post-canonical state that already contains the separately proven
# ChunkPos record-accessor and TicketStorage bridges. These are authority guards,
# not mutations performed by this helper.
anchors = [
    (
        "!distanceManagerAccessor.getTicketStorage().getTickets(chunkHolder.getPos().pack()).isEmpty()",
        1,
        "ticket-storage load membership",
    ),
    (
        "distanceManagerAccessor.getTicketStorage().getTickets(chunkPos).isEmpty()",
        1,
        "ticket-storage unload membership",
    ),
    ("levelChunk.registerTickContainerInLevel(self);", 1, "shipyard tick-container registration"),
    ("self.startTickingChunk(levelChunk);", 1, "shipyard ticking start"),
    ('@Inject(method = "unload", at = @At("HEAD"), cancellable = true)', 1, "shipyard keep-loaded hook"),
    ("VSGameUtilsKt.getShipManagingPos(self, pos.x(), pos.z()) != null", 1, "live-ship keep-loaded predicate"),
    ("shipObjectWorld.addTerrainUpdates(", 1, "terrain update handoff"),
    ("blockState.getBlock() instanceof WingBlock", 1, "wing scan"),
    ("DragInfoReporter.INSTANCE.tick((ServerLevel) (Object) this);", 1, "drag-info tick"),
]
for token, expected, label in anchors:
    actual = text.count(token)
    if actual != expected:
        raise SystemExit(
            f"fail-closed: expected {expected} {label} authority anchor(s) {token!r}, found {actual}"
        )

if "distanceManagerAccessor.getTickets().containsKey" in text:
    raise SystemExit("fail-closed: obsolete pre-26.2 DistanceManager ticket-map predicate reappeared")

ticket_mutation_tokens = ("addTicket", "removeTicket", "addRegionTicket", "removeRegionTicket")
ticket_mutation_before = {token: text.count(token) for token in ticket_mutation_tokens}

for old, new, _ in replacements:
    text = text.replace(old, new, 1)

for old, new, label in replacements:
    if old in text:
        raise SystemExit(f"fail-closed: legacy {label} expression remains")
    if text.count(new) != 1:
        raise SystemExit(f"fail-closed: {label} adaptation did not converge exactly once")

for token, expected, label in anchors:
    if text.count(token) != expected:
        raise SystemExit(f"fail-closed: {label} authority anchor changed unexpectedly: {token!r}")

ticket_mutation_after = {token: text.count(token) for token in ticket_mutation_tokens}
if ticket_mutation_before != ticket_mutation_after:
    raise SystemExit(
        "fail-closed: ticket mutation token counts changed in MixinServerLevel: "
        f"before={ticket_mutation_before} after={ticket_mutation_after}"
    )

path.write_text(text, encoding="utf-8")
print("P1_SERVERLEVEL_CHUNKPOS_HEIGHT_26_2_OVERLAY_APPLIED count=4")
