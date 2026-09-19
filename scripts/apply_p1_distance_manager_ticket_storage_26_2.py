#!/usr/bin/env python3
"""Fail-closed Minecraft 26.2 DistanceManager ticket-storage adaptation.

Pinned VS2 only needs to answer whether a chunk currently has any active ticket at
this boundary. Minecraft 26.2 moved the ticket map out of DistanceManager into
TicketStorage. Exact 26.2 bytecode proves TicketStorage.getTickets(long) returns
List.of() when no active ticket exists and removes the map key when the final
ticket is removed.

This overlay therefore changes only the accessor boundary and the two existing
membership checks. It does not change VS2 ticket types, add/remove lifecycle,
radius, loading/simulation semantics, or chunk-unload timing.
"""

from pathlib import Path
import sys

ACCESSOR = Path(
    "common/src/main/java/org/valkyrienskies/mod/mixin/accessors/server/level/DistanceManagerAccessor.java"
)
SERVER_LEVEL = Path(
    "common/src/main/java/org/valkyrienskies/mod/mixin/server/world/MixinServerLevel.java"
)


def fail(message: str) -> None:
    raise SystemExit(f"fail-closed: {message}")


def require_count(text: str, needle: str, expected: int, label: str) -> None:
    actual = text.count(needle)
    if actual != expected:
        fail(f"{label}: expected {expected} occurrence(s) of {needle!r}, found {actual}")


def apply(root: Path) -> None:
    accessor_path = root / ACCESSOR
    server_level_path = root / SERVER_LEVEL

    if not accessor_path.is_file():
        fail(f"missing pinned accessor source: {ACCESSOR}")
    if not server_level_path.is_file():
        fail(f"missing pinned server-level source: {SERVER_LEVEL}")

    accessor = accessor_path.read_text(encoding="utf-8")
    server_level = server_level_path.read_text(encoding="utf-8")

    old_import_block = (
        "import it.unimi.dsi.fastutil.longs.Long2ObjectOpenHashMap;\n"
        "import net.minecraft.server.level.DistanceManager;\n"
        "import net.minecraft.server.level.Ticket;\n"
        "import net.minecraft.util.SortedArraySet;\n"
    )
    new_import_block = (
        "import net.minecraft.server.level.DistanceManager;\n"
        "import net.minecraft.world.level.TicketStorage;\n"
    )
    require_count(accessor, old_import_block, 1, "DistanceManagerAccessor pinned import block")

    old_accessor = (
        '    @Accessor("tickets")\n'
        "    Long2ObjectOpenHashMap<SortedArraySet<Ticket<?>>> getTickets();"
    )
    require_count(accessor, old_accessor, 1, "DistanceManagerAccessor pinned field accessor")
    require_count(accessor, "@Accessor(", 1, "DistanceManagerAccessor accessor count")

    old_load_membership = (
        "distanceManagerAccessor.getTickets().containsKey(chunkHolder.getPos().toLong())"
    )
    old_unload_membership = "!distanceManagerAccessor.getTickets().containsKey(chunkPos)"
    require_count(server_level, old_load_membership, 1, "MixinServerLevel load membership")
    require_count(server_level, old_unload_membership, 1, "MixinServerLevel unload membership")
    require_count(
        server_level,
        "distanceManagerAccessor.getTickets().containsKey",
        2,
        "MixinServerLevel total old ticket-map membership",
    )

    # Frozen ticket lifecycle is elsewhere. Record relevant token counts here so this
    # accessor-only bridge cannot silently introduce ticket mutation into MixinServerLevel.
    lifecycle_tokens = ("addTicket", "removeTicket", "addRegionTicket", "removeRegionTicket")
    lifecycle_counts_before = {token: server_level.count(token) for token in lifecycle_tokens}

    accessor = accessor.replace(old_import_block, new_import_block, 1)
    accessor = accessor.replace(
        old_accessor,
        '    @Accessor("ticketStorage")\n    TicketStorage getTicketStorage();',
        1,
    )

    server_level = server_level.replace(
        old_load_membership,
        "!distanceManagerAccessor.getTicketStorage().getTickets(chunkHolder.getPos().pack()).isEmpty()",
        1,
    )
    server_level = server_level.replace(
        old_unload_membership,
        "distanceManagerAccessor.getTicketStorage().getTickets(chunkPos).isEmpty()",
        1,
    )

    require_count(accessor, "import net.minecraft.server.level.DistanceManager;", 1, "DistanceManager import")
    require_count(accessor, "import net.minecraft.world.level.TicketStorage;", 1, "TicketStorage import")
    for obsolete_import in (
        "import it.unimi.dsi.fastutil.longs.Long2ObjectOpenHashMap;",
        "import net.minecraft.server.level.Ticket;",
        "import net.minecraft.util.SortedArraySet;",
    ):
        if obsolete_import in accessor:
            fail(f"obsolete accessor import remains: {obsolete_import}")
    require_count(accessor, '@Accessor("ticketStorage")', 1, "ticketStorage accessor annotation")
    require_count(accessor, "TicketStorage getTicketStorage();", 1, "ticketStorage accessor method")
    if '@Accessor("tickets")' in accessor or "getTickets();" in accessor:
        fail("obsolete DistanceManager tickets accessor remains")

    require_count(
        server_level,
        "!distanceManagerAccessor.getTicketStorage().getTickets(chunkHolder.getPos().pack()).isEmpty()",
        1,
        "new load active-ticket membership",
    )
    require_count(
        server_level,
        "distanceManagerAccessor.getTicketStorage().getTickets(chunkPos).isEmpty()",
        1,
        "new unload no-active-ticket membership",
    )
    if "distanceManagerAccessor.getTickets().containsKey" in server_level:
        fail("obsolete DistanceManager ticket-map membership remains")

    lifecycle_counts_after = {token: server_level.count(token) for token in lifecycle_tokens}
    if lifecycle_counts_before != lifecycle_counts_after:
        fail(
            "ticket mutation token counts changed in MixinServerLevel: "
            f"before={lifecycle_counts_before} after={lifecycle_counts_after}"
        )

    accessor_path.write_text(accessor, encoding="utf-8")
    server_level_path.write_text(server_level, encoding="utf-8")
    print("P1_DISTANCE_MANAGER_TICKET_STORAGE_26_2_OVERLAY_APPLIED")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} <upstream-vs2-root>")
    apply(Path(sys.argv[1]))


if __name__ == "__main__":
    main()
