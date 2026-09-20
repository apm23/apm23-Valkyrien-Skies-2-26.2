#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/feature/fire_between_ship_and_world/LavaFluidMixin.java"
text = path.read_text(encoding="utf-8")

old_import = "import net.minecraft.world.level.Level;"
new_import = "import net.minecraft.server.level.ServerLevel;"
old_param = "public void fireTickMixin(final Level level, final BlockPos pos, final FluidState state, final RandomSource random,"
new_param = "public void fireTickMixin(final ServerLevel level, final BlockPos pos, final FluidState state, final RandomSource random,"

if text.count(old_import) != 1:
    raise SystemExit(f"expected exactly one pinned Level import in {path}, found {text.count(old_import)}")
if new_import in text:
    raise SystemExit(f"refusing already-adapted/non-baseline ServerLevel import in {path}")
if text.count(old_param) != 1:
    raise SystemExit(f"expected exactly one pinned LavaFluid randomTick callback Level parameter in {path}, found {text.count(old_param)}")
if new_param in text:
    raise SystemExit(f"refusing already-adapted/non-baseline LavaFluid callback in {path}")

# Freeze the existing real VS2 fire-between-ship-and-world behavior before changing only type vocabulary.
if text.count('@Inject(method = "randomTick", at = @At("TAIL"))') != 1:
    raise SystemExit("fail-closed: randomTick TAIL injection authority changed")
if text.count("private boolean isModifyingFireTick = false;") != 1:
    raise SystemExit("fail-closed: recursion guard field changed")
if text.count("if (isModifyingFireTick)") != 1:
    raise SystemExit("fail-closed: recursion early-return guard changed")
if text.count("isModifyingFireTick = true;") != 1 or text.count("isModifyingFireTick = false;") != 2:
    raise SystemExit("fail-closed: recursion guard mutation shape changed")
if text.count("VSGameUtilsKt.transformToNearbyShipsAndWorld(level, origX, origY, origZ, 3, (x, y, z) -> {") != 1:
    raise SystemExit("fail-closed: VS2 nearby-ship/world transform authority changed")
if text.count("randomTick(level, BlockPos.containing(x, y, z), state, random);") != 1:
    raise SystemExit("fail-closed: vanilla LavaFluid randomTick delegation changed")
if "(ServerLevel)" in text:
    raise SystemExit("fail-closed: baseline unexpectedly contains a ServerLevel cast")

text = text.replace(old_import, new_import, 1)
text = text.replace(old_param, new_param, 1)

if old_import in text or old_param in text:
    raise SystemExit("fail-closed: old Level callback vocabulary remains")
if text.count(new_import) != 1 or text.count(new_param) != 1:
    raise SystemExit("fail-closed: ServerLevel adaptation count mismatch")
if "(ServerLevel)" in text:
    raise SystemExit("fail-closed: adaptation must narrow the injected callback type, not cast at use sites")
if text.count('@Inject(method = "randomTick", at = @At("TAIL"))') != 1:
    raise SystemExit("fail-closed: randomTick injection changed after adaptation")
if text.count("VSGameUtilsKt.transformToNearbyShipsAndWorld(level, origX, origY, origZ, 3, (x, y, z) -> {") != 1:
    raise SystemExit("fail-closed: VS2 transform authority changed after adaptation")
if text.count("randomTick(level, BlockPos.containing(x, y, z), state, random);") != 1:
    raise SystemExit("fail-closed: vanilla randomTick delegation changed after adaptation")

path.write_text(text, encoding="utf-8")
print("P1_LAVAFLUID_RANDOMTICK_SERVERLEVEL_26_2_OVERLAY_APPLIED")
