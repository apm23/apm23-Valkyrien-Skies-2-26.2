#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/feature/world_weather/MixinLevelRenderer.java"
text = path.read_text(encoding="utf-8")

old_import_anchor = "import net.minecraft.world.phys.BlockHitResult;\n"
new_import_block = "import net.minecraft.world.phys.BlockHitResult;\nimport net.minecraft.world.phys.Vec3;\n"
old_expr = "CompatUtil.INSTANCE.toSameSpaceAs(level, vanillaHeight.getCenter(), (Ship) null, null)"
new_expr = "CompatUtil.INSTANCE.toSameSpaceAs(level, Vec3.atCenterOf(vanillaHeight), (Ship) null, null)"

if text.count(old_import_anchor) != 1:
    raise SystemExit(f"expected exactly one pinned BlockHitResult import anchor in {path}, found {text.count(old_import_anchor)}")
if "import net.minecraft.world.phys.Vec3;" in text:
    raise SystemExit(f"refusing already-adapted/non-baseline Vec3 import in {path}")
if text.count(old_expr) != 1:
    raise SystemExit(f"expected exactly one pinned world-weather center expression in {path}, found {text.count(old_expr)}")
if new_expr in text:
    raise SystemExit(f"refusing already-adapted world-weather center expression in {path}")

text = text.replace(old_import_anchor, new_import_block, 1)
text = text.replace(old_expr, new_expr, 1)

if text.count("import net.minecraft.world.phys.Vec3;") != 1:
    raise SystemExit("fail-closed: Vec3 import adaptation count mismatch")
if text.count(new_expr) != 1:
    raise SystemExit("fail-closed: world-weather center adaptation count mismatch")
if text.count("CompatUtil.INSTANCE.toSameSpaceAs(") != 1:
    raise SystemExit("fail-closed: existing CompatUtil.toSameSpaceAs authority changed")
if text.count("CompatUtil.INSTANCE.getShipHeightmapHitAboveWorldHeight(") != 1:
    raise SystemExit("fail-closed: existing ship heightmap authority changed")
if text.count("weatherSurfaceLookupPos.set(") != 2:
    raise SystemExit("fail-closed: shared weather lookup behavior changed")

path.write_text(text, encoding="utf-8")
print("P1_WORLD_WEATHER_BLOCKPOS_CENTER_26_2_OVERLAY_APPLIED")
