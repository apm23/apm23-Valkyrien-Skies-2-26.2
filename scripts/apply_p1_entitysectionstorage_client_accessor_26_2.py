#!/usr/bin/env python3
"""Adapt pinned upstream VS2 EntitySectionStorage client-side check to Minecraft 26.2.

Minecraft 26.2 exposes Level client-side state through isClientSide() rather than
permitting direct field access. Preserve the upstream VS2 ship-section lifecycle,
ShipLoadEventClient subscription, delayed section bookkeeping, and ship lookup.
"""

from pathlib import Path
import sys

TARGET = Path(
    "common/src/main/java/org/valkyrienskies/mod/mixin/feature/shipyard_entities/MixinEntitySectionStorage.java"
)


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {sys.argv[0]} <upstream-vs2-root>")

    path = Path(sys.argv[1]) / TARGET
    if not path.is_file():
        raise SystemExit(f"fail-closed: pinned EntitySectionStorage mixin missing: {path}")

    text = path.read_text(encoding="utf-8")
    old = "if(level.isClientSide) ShipLoadEventClient.Companion.on(this::handleShipLoad);"
    new = "if(level.isClientSide()) ShipLoadEventClient.Companion.on(this::handleShipLoad);"

    count = text.count(old)
    if count != 1:
        raise SystemExit(
            f"fail-closed: expected exactly one pinned Level.isClientSide field-access anchor, found {count}"
        )
    if text.count("level.isClientSide()"):
        raise SystemExit("fail-closed: 26.2 Level client accessor adaptation already present")

    text = text.replace(old, new, 1)

    required = (
        "ShipLoadEventClient.Companion.on(this::handleShipLoad)",
        "VSGameUtilsKt.getShipManagingPos",
        "VSGameUtilsKt.isChunkInShipyard",
        "this.forEachAccessibleNonEmptySection",
    )
    for anchor in required:
        if anchor not in text:
            raise SystemExit(f"fail-closed: upstream VS2 EntitySectionStorage authority anchor changed: {anchor}")

    if text.count(new) != 1:
        raise SystemExit("fail-closed: EntitySectionStorage Level client accessor replacement count mismatch")

    path.write_text(text, encoding="utf-8")
    print("P1_ENTITYSECTIONSTORAGE_CLIENT_ACCESSOR_26_2_OVERLAY_APPLIED")


if __name__ == "__main__":
    main()
