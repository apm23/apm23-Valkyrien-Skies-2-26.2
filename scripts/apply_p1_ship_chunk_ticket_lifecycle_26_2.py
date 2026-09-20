#!/usr/bin/env python3
"""Adapt only the real VS2 ship-chunk ticket lifecycle to Minecraft 26.2.

Pinned upstream VS2 uses the pre-26.x generic TicketType<T> factory plus
ServerChunkCache.addRegionTicket/removeRegionTicket(type, pos, radius, value).
Minecraft 26.2 uses non-generic TicketType and the radius APIs no longer carry a
per-ticket value.  A permanent load-only TicketType plus radius 0 preserves the
existing VS2 intent: keep exactly the requested shipyard chunk at FULL status,
without turning it into a simulation/entity-ticking or disk-persisted ticket.

This fail-closed overlay changes only the ticket API boundary shared by
VSTicketType, ChunkManagement, ShipAssembler, and the existing MinecraftServer
shutdown cleanup. At the existing ship-delete cleanup site, the removed writable
isUnsaved property is bridged to current ChunkAccess.tryMarkSaved(), which clears
the dirty marker if present. It does not change ticket radius/lifetime intent,
ship deletion checks, assembly/shutdown ordering, ship lifecycle, transforms,
physics, collision, entity dragging, rendering, networking/gameplay authority,
or camera behavior.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
ship_path = root / "common/src/main/kotlin/org/valkyrienskies/mod/common/assembly/ShipAssembler.kt"
chunk_path = root / "common/src/main/kotlin/org/valkyrienskies/mod/common/world/ChunkManagement.kt"
ticket_path = root / "common/src/main/kotlin/org/valkyrienskies/mod/common/world/VSTicketType.kt"
server_path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/server/MixinMinecraftServer.java"

ship = ship_path.read_text(encoding="utf-8")
chunk = chunk_path.read_text(encoding="utf-8")
ticket = ticket_path.read_text(encoding="utf-8")
server = server_path.read_text(encoding="utf-8")

# ShipAssembler: exactly one batch-preload radius-0 ticket. Preserve the
# explicit distance-manager flush and subsequent synchronous FULL chunk waits.
ship_old = """chunkSource.addRegionTicket(\n                org.valkyrienskies.mod.common.world.VSTicketType.SHIP_CHUNK, cp, 0, cp\n            )"""
ship_new = """chunkSource.addTicketWithRadius(\n                org.valkyrienskies.mod.common.world.VSTicketType.SHIP_CHUNK, cp, 0\n            )"""
if ship.count(ship_old) != 1:
    raise SystemExit(f"expected exactly one ShipAssembler addRegionTicket site, found {ship.count(ship_old)}")
for guard in (
    ".callRunDistanceManagerUpdates()",
    "level.getChunk(cp.x, cp.z)",
):
    if ship.count(guard) != 1:
        raise SystemExit(f"unexpected ShipAssembler preload lifecycle shape: {guard}")
ship = ship.replace(ship_old, ship_new)

# ChunkManagement: preserve add-on-watch, remove-only-on-actual-ship-delete,
# radius 0, and the existing non-shipyard updateChunkForced path.
chunk_add_old = "level.chunkSource.addRegionTicket(VSTicketType.SHIP_CHUNK, chunkPos, 0, chunkPos)"
chunk_add_new = "level.chunkSource.addTicketWithRadius(VSTicketType.SHIP_CHUNK, chunkPos, 0)"
chunk_remove_old = "level.chunkSource.removeRegionTicket(VSTicketType.SHIP_CHUNK, chunkPos, 0, chunkPos)"
chunk_remove_new = "level.chunkSource.removeTicketWithRadius(VSTicketType.SHIP_CHUNK, chunkPos, 0)"
chunk_dirty_old = "chunk?.isUnsaved = false"
chunk_dirty_new = "chunk?.tryMarkSaved()"
for old, expected, label in (
    (chunk_add_old, 1, "ChunkManagement addRegionTicket"),
    (chunk_remove_old, 1, "ChunkManagement removeRegionTicket"),
    (chunk_dirty_old, 1, "ChunkManagement ship-delete clean mark"),
):
    if chunk.count(old) != expected:
        raise SystemExit(f"expected exactly {expected} {label} site, found {chunk.count(old)}")
for guard in (
    "val shipStillAlive = shipWorld.allShips.getById(taskShip.id) != null",
    "if (!shipStillAlive)",
    "level.chunkSource.updateChunkForced(chunkPos, true)",
    "level.chunkSource.updateChunkForced(chunkPos, false)",
):
    if chunk.count(guard) != 1:
        raise SystemExit(f"unexpected ChunkManagement lifecycle guard shape: {guard}")
chunk = chunk.replace(chunk_add_old, chunk_add_new)
chunk = chunk.replace(chunk_remove_old, chunk_remove_new)
chunk = chunk.replace(chunk_dirty_old, chunk_dirty_new)

# MixinMinecraftServer: shutdown already removes every active ship's radius-0
# SHIP_CHUNK ticket before Minecraft drains ChunkHolders. Minecraft 26.2 exposes
# the same radius removal boundary as removeTicketWithRadius and no longer carries
# the old per-ticket ChunkPos value. Preserve iteration, ordering, legacy FORCED
# cleanup, and radius exactly; adapt only the removed API call.
server_remove_old = """level.getChunkSource().removeRegionTicket(
                            org.valkyrienskies.mod.common.world.VSTicketType.SHIP_CHUNK, cp, 0, cp);"""
server_remove_new = """level.getChunkSource().removeTicketWithRadius(
                            org.valkyrienskies.mod.common.world.VSTicketType.SHIP_CHUNK, cp, 0);"""
if server.count(server_remove_old) != 1:
    raise SystemExit(
        f"expected exactly one MixinMinecraftServer shutdown removeRegionTicket site, found {server.count(server_remove_old)}"
    )
for guard in (
    "ship.getActiveChunksSet().forEach((final int x, final int z) -> {",
    "level.getChunkSource().updateChunkForced(cp, false);",
):
    if server.count(guard) != 1:
        raise SystemExit(f"unexpected MixinMinecraftServer shutdown lifecycle shape: {guard}")
server = server.replace(server_remove_old, server_remove_new)

# VSTicketType: old comparator/value identity is gone in current Minecraft.
# A zero-expiration, load-only type is the direct semantic replacement for the
# VS2 shipyard ticket: permanent until explicit removal and not simulation-ticking.
chunkpos_import = "import net.minecraft.world.level.ChunkPos\n"
comparator_import = "import java.util.Comparator\n"
ticket_old = """val SHIP_CHUNK: TicketType<ChunkPos> = TicketType.create(
        \"vs_ship_chunk\", Comparator.comparingLong(ChunkPos::toLong)
    )"""
ticket_new = "val SHIP_CHUNK: TicketType = TicketType(0L, TicketType.FLAG_LOADING)"
if ticket.count(chunkpos_import) != 1 or ticket.count(comparator_import) != 1:
    raise SystemExit("unexpected VSTicketType legacy imports; refusing broader rewrite")
if ticket.count(ticket_old) != 1:
    raise SystemExit(f"expected exactly one legacy VSTicketType declaration, found {ticket.count(ticket_old)}")
ticket = ticket.replace(chunkpos_import, "")
ticket = ticket.replace(comparator_import, "")
ticket = ticket.replace(ticket_old, ticket_new)

# Fail closed on both legacy API residue and accidental semantic broadening.
for text, needle, label in (
    (ship, "addRegionTicket(", "ShipAssembler legacy addRegionTicket"),
    (chunk, "addRegionTicket(", "ChunkManagement legacy addRegionTicket"),
    (chunk, "removeRegionTicket(", "ChunkManagement legacy removeRegionTicket"),
    (server, "removeRegionTicket(", "MixinMinecraftServer legacy removeRegionTicket"),
    (ticket, "TicketType.create(", "legacy TicketType factory"),
    (ticket, "TicketType<", "legacy generic TicketType"),
):
    if needle in text:
        raise SystemExit(f"{label} remains after adaptation")

if ship.count("addTicketWithRadius(") != 1:
    raise SystemExit("ShipAssembler current radius-ticket add was not installed exactly once")
if chunk.count("addTicketWithRadius(") != 1 or chunk.count("removeTicketWithRadius(") != 1:
    raise SystemExit("ChunkManagement current add/remove radius-ticket pair was not installed exactly once")
if server.count("removeTicketWithRadius(") != 1:
    raise SystemExit("MixinMinecraftServer current shutdown radius-ticket removal was not installed exactly once")
if chunk.count("tryMarkSaved()") != 1:
    raise SystemExit("ChunkManagement current clean mark was not installed exactly once")
if ticket.count("TicketType(0L, TicketType.FLAG_LOADING)") != 1:
    raise SystemExit("VSTicketType permanent load-only declaration was not installed exactly once")
if "FLAG_SIMULATION" in ticket:
    raise SystemExit("SHIP_CHUNK must remain load-only; refusing simulation-ticket broadening")

ship_path.write_text(ship, encoding="utf-8")
chunk_path.write_text(chunk, encoding="utf-8")
ticket_path.write_text(ticket, encoding="utf-8")
server_path.write_text(server, encoding="utf-8")
print("P1_SHIP_CHUNK_TICKET_LIFECYCLE_26_2_OVERLAY_APPLIED")
