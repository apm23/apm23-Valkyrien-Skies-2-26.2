#!/usr/bin/env python3
"""Adapt pinned upstream VS2 tick-ship-chunks ChunkPos coordinate reads to Minecraft 26.2.

Minecraft 26.2 exposes ChunkPos coordinates through x()/z() accessors instead of
public x/z fields. This changes only the API vocabulary at the existing VS2
random-tick/spawning hooks and preserves all ship-aware distance and lookup logic.
"""

from pathlib import Path
import sys

TARGET = Path(
    "common/src/main/java/org/valkyrienskies/mod/mixin/feature/tick_ship_chunks/MixinChunkMap.java"
)


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {sys.argv[0]} <upstream-vs2-root>")

    path = Path(sys.argv[1]) / TARGET
    if not path.is_file():
        raise SystemExit(f"fail-closed: pinned tick-ship-chunks mixin missing: {path}")

    text = path.read_text(encoding="utf-8")

    if text.count("chunkPos.x") != 3 or text.count("chunkPos.z") != 3:
        raise SystemExit(
            "fail-closed: expected exactly three pinned chunkPos.x and three chunkPos.z reads "
            f"in {path}, found x={text.count('chunkPos.x')} z={text.count('chunkPos.z')}"
        )
    if "chunkPos.x()" in text or "chunkPos.z()" in text:
        raise SystemExit("fail-closed: 26.2 ChunkPos accessor adaptation already present")

    required = {
        "VSGameUtilsKt.squaredDistanceBetweenInclShips(": 1,
        "VSGameUtilsKt.isChunkInShipyard(level, chunkPos.x, chunkPos.z)": 1,
        ".getByChunkPos(chunkPos.x, chunkPos.z, VSGameUtilsKt.getDimensionId(level))": 1,
        "cir.setReturnValue(retValue);": 1,
        "cir.setReturnValue(true);": 1,
    }
    for anchor, expected in required.items():
        count = text.count(anchor)
        if count != expected:
            raise SystemExit(
                f"fail-closed: pinned semantic anchor {anchor!r} expected {expected}, found {count}"
            )

    text = text.replace("chunkPos.x", "chunkPos.x()")
    text = text.replace("chunkPos.z", "chunkPos.z()")

    if text.count("chunkPos.x()") != 3 or text.count("chunkPos.z()") != 3:
        raise SystemExit("fail-closed: ChunkPos accessor replacement count mismatch")
    if "chunkPos.x *" in text or "chunkPos.z *" in text:
        raise SystemExit("fail-closed: old direct ChunkPos field access remains")

    path.write_text(text, encoding="utf-8")
    print("P1_TICK_SHIP_CHUNKS_CHUNKPOS_ACCESSORS_26_2_OVERLAY_APPLIED")


if __name__ == "__main__":
    main()
