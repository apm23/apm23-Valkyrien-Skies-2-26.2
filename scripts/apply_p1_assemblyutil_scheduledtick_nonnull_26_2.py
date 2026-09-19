#!/usr/bin/env python3
"""Adapt only AssemblyUtil's ScheduledTick generic bound to Minecraft 26.2 non-null T.

Pinned upstream VS2 transfers a pending block tick in copyBlock() by scheduling
ScheduledTick<Block?>(state.block, to, 0, 0). Minecraft 26.2 keeps the same four-argument
ScheduledTick(type, pos, triggerTick, subTickOrder) constructor and LevelTicks.schedule flow,
but Kotlin now sees ScheduledTick's type parameter as non-null. The upstream value state.block
is already a non-null Block, so this overlay changes only the explicit generic argument from
Block? to Block. It deliberately preserves the hasScheduledTick guard, destination, trigger tick,
sub-tick order, default constructor priority, block-entity transfer, neighbor updates, assembly,
relocation, transforms, physics, networking, and authority.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
path = root / "common/src/main/kotlin/org/valkyrienskies/mod/common/assembly/AssemblyUtil.kt"
text = path.read_text(encoding="utf-8")

old = (
    "        // Transfer pending schedule-ticks\n"
    "        if (level.blockTicks.hasScheduledTick(from, state.block)) {\n"
    "            level.blockTicks.schedule(ScheduledTick<Block?>(state.block, to, 0, 0))\n"
    "        }\n"
)
new = (
    "        // Transfer pending schedule-ticks\n"
    "        if (level.blockTicks.hasScheduledTick(from, state.block)) {\n"
    "            level.blockTicks.schedule(ScheduledTick<Block>(state.block, to, 0, 0))\n"
    "        }\n"
)

count = text.count(old)
if count != 1:
    raise SystemExit(
        f"expected exactly one pinned upstream AssemblyUtil scheduled-tick transfer context in {path}, found {count}"
    )

text = text.replace(old, new)

expected = "level.blockTicks.schedule(ScheduledTick<Block>(state.block, to, 0, 0))"
legacy = "level.blockTicks.schedule(ScheduledTick<Block?>(state.block, to, 0, 0))"
if text.count(expected) != 1:
    raise SystemExit(f"expected exactly one Minecraft 26.2 non-null ScheduledTick<Block> call in {path}")
if legacy in text:
    raise SystemExit(f"legacy nullable ScheduledTick<Block?> call remains in {path}")

path.write_text(text, encoding="utf-8")
print("P1_ASSEMBLYUTIL_SCHEDULEDTICK_NONNULL_26_2_OVERLAY_APPLIED")
