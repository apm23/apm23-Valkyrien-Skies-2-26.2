#!/usr/bin/env python3
"""Adapt pinned upstream VS2 NaturalSpawnerMixin to Minecraft 26.2 ChunkPos accessors.

Minecraft 26.2 exposes ChunkPos coordinates through record-style x()/z()
accessors instead of public x/z fields. This preserves the upstream VS2
shipyard spawn-policy check exactly and changes only the API boundary.
"""

from pathlib import Path
import sys

TARGET = Path(
    "common/src/main/java/org/valkyrienskies/mod/mixin/feature/mob_spawning/NaturalSpawnerMixin.java"
)


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {sys.argv[0]} <upstream-vs2-root>")

    path = Path(sys.argv[1]) / TARGET
    if not path.is_file():
        raise SystemExit(f"fail-closed: pinned NaturalSpawner mixin missing: {path}")

    text = path.read_text(encoding="utf-8")
    old = "VSGameUtilsKt.isChunkInShipyard(level, chunk.getPos().x, chunk.getPos().z)"
    new = "VSGameUtilsKt.isChunkInShipyard(level, chunk.getPos().x(), chunk.getPos().z())"

    count = text.count(old)
    if count != 1:
        raise SystemExit(
            f"fail-closed: expected exactly one pinned ChunkPos field-access anchor, found {count}"
        )
    if text.count("chunk.getPos().x()") or text.count("chunk.getPos().z()"):
        raise SystemExit("fail-closed: 26.2 ChunkPos accessor adaptation already present")

    text = text.replace(old, new, 1)

    if text.count(new) != 1:
        raise SystemExit("fail-closed: NaturalSpawner ChunkPos accessor replacement count mismatch")

    path.write_text(text, encoding="utf-8")
    print("P1_NATURALSPAWNER_CHUNKPOS_ACCESSORS_26_2_OVERLAY_APPLIED")


if __name__ == "__main__":
    main()
