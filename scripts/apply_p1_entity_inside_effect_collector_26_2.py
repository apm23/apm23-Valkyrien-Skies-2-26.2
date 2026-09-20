#!/usr/bin/env python3
"""Adapt the real VS2 ship-space Entity inside-block scan to Minecraft 26.2's effect collector API.

Minecraft 26.2 routes BlockState.entityInside effects through Entity's own
InsideBlockEffectApplier.StepBasedCollector and applies that collector immediately after the
vanilla inside-block scan. Preserve the upstream VS2 ship-space scan and feed its block effects
into that same vanilla collector; do not introduce a second effect authority or suppress effects.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/entity/MixinEntity.java"
if not path.is_file():
    raise SystemExit(f"fail-closed: expected pinned VS2 MixinEntity source missing: {path}")

text = path.read_text(encoding="utf-8")

import_anchor = (
    "import net.minecraft.world.entity.Entity;\n"
    "import net.minecraft.world.entity.EntityType;\n"
)
import_replacement = (
    "import net.minecraft.world.entity.Entity;\n"
    "import net.minecraft.world.entity.EntityType;\n"
    "import net.minecraft.world.entity.InsideBlockEffectApplier;\n"
)
mutable_anchor = "        final BlockPos.MutableBlockPos mutableBlockPos = new BlockPos.MutableBlockPos();\n"
mutable_replacement = (
    "        final BlockPos.MutableBlockPos mutableBlockPos = new BlockPos.MutableBlockPos();\n"
    "        int effectStep = Integer.MIN_VALUE;\n"
)
old_call = "                            blockState.entityInside(this.level, mutableBlockPos, self);\n"
new_call = (
    "                            this.insideEffectCollector.advanceStep(effectStep++);\n"
    "                            blockState.entityInside(this.level, mutableBlockPos, self, this.insideEffectCollector, true);\n"
)
shadow_anchor = (
    "    @Shadow\n"
    "    public Level level;\n"
)
shadow_replacement = (
    "    @Shadow\n"
    "    public Level level;\n\n"
    "    @Shadow\n"
    "    @Final\n"
    "    private InsideBlockEffectApplier.StepBasedCollector insideEffectCollector;\n"
)

for needle, expected, label in (
    (import_anchor, 1, "Entity/EntityType import anchor"),
    (mutable_anchor, 1, "ship-space mutable BlockPos anchor"),
    (old_call, 1, "legacy three-argument entityInside call"),
    (shadow_anchor, 1, "Entity level shadow anchor"),
    ("originalCheckInside(inShipBB);", 1, "real VS2 ship-space inside-block handoff"),
    ("ship.getShipTransform().getWorldToShipMatrix()", 1, "real VS2 world-to-ship transform authority"),
    ("this.onInsideBlock(blockState);", 1, "upstream inside-block callback"),
):
    actual = text.count(needle)
    if actual != expected:
        raise SystemExit(f"fail-closed: {label}: expected {expected}, found {actual}")

for already in (
    "import net.minecraft.world.entity.InsideBlockEffectApplier;",
    "private InsideBlockEffectApplier.StepBasedCollector insideEffectCollector;",
    "this.insideEffectCollector.advanceStep(effectStep++);",
):
    if already in text:
        raise SystemExit(f"fail-closed: Entity inside-effect collector adaptation already present: {already}")

text = text.replace(import_anchor, import_replacement, 1)
text = text.replace(mutable_anchor, mutable_replacement, 1)
text = text.replace(old_call, new_call, 1)
text = text.replace(shadow_anchor, shadow_replacement, 1)

# The 26.2 call must use Entity's vanilla collector and keep the old VS2 scan/callback authority intact.
for needle, expected, label in (
    ("import net.minecraft.world.entity.InsideBlockEffectApplier;", 1, "collector import"),
    ("private InsideBlockEffectApplier.StepBasedCollector insideEffectCollector;", 1, "vanilla Entity collector shadow"),
    ("int effectStep = Integer.MIN_VALUE;", 1, "ship-space effect step seed"),
    ("this.insideEffectCollector.advanceStep(effectStep++);", 1, "effect step advance"),
    ("blockState.entityInside(this.level, mutableBlockPos, self, this.insideEffectCollector, true);", 1, "26.2 entityInside call"),
    ("originalCheckInside(inShipBB);", 1, "real VS2 ship-space inside-block handoff"),
    ("ship.getShipTransform().getWorldToShipMatrix()", 1, "real VS2 world-to-ship transform authority"),
    ("this.onInsideBlock(blockState);", 1, "upstream inside-block callback"),
):
    actual = text.count(needle)
    if actual != expected:
        raise SystemExit(f"fail-closed: {label}: expected {expected}, found {actual}")

if old_call in text:
    raise SystemExit("fail-closed: legacy three-argument entityInside call remains")
if "InsideBlockEffectApplier.NOOP" in text:
    raise SystemExit("fail-closed: refusing to suppress real inside-block effects with a NOOP applier")

path.write_text(text, encoding="utf-8")
print("P1_ENTITY_INSIDE_EFFECT_COLLECTOR_26_2_OVERLAY_APPLIED count=1")
