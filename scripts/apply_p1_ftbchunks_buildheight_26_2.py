#!/usr/bin/env python3
"""Adapt only FTB Chunks compat build-height accessors to Minecraft 26.2.

Pinned VS2 checks the ship-to-world transformed claim position against Level's old
getMinBuildHeight()/getMaxBuildHeight() accessors before deciding whether an out-of-build-height
ship position should remain protected by the original chunk claim. Minecraft 26.2 removed
those accessor names. Frozen P1 build-height evidence maps the lower bound to getMinY() and the
exclusive upper bound to getMinY() + getHeight(). This overlay changes only that vocabulary;
FTB claim policy, ship lookup, transform authority, and return ordering remain upstream VS2.
"""
from pathlib import Path
import subprocess, sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/ftb_chunks/MixinClaimedChunkManagerImpl.java"
if not path.is_file():
    raise SystemExit(f"fail-closed: pinned FTB Chunks compat source missing: {path}")

text = path.read_text(encoding="utf-8")
old_max = "level.getMaxBuildHeight()"
old_min = "level.getMinBuildHeight()"
new_max = "level.getMinY() + level.getHeight()"
new_min = "level.getMinY()"

if text.count(old_max) != 1 or text.count(old_min) != 1:
    raise SystemExit(
        f"fail-closed: expected exactly one pinned FTB build-height pair; max={text.count(old_max)} min={text.count(old_min)}"
    )
if new_max in text:
    raise SystemExit("fail-closed: FTB exclusive max build-height adaptation already present")

# Preserve the exact upstream claim/ship semantics around the accessor-only edit.
for anchor in (
    '@Mixin(targets = "dev.ftb.mods.ftbchunks.data.ClaimedChunkManagerImpl")',
    'method = "shouldPreventInteraction"',
    "VSGameConfig.SERVER.getFTBChunks().getShipsProtectedByClaims()",
    "VSGameUtilsKt.getShipManagingPos(level, pos)",
    "ship.getShipToWorld().transformPosition",
    "BlockPos.containing(VectorConversionsMCKt.toMinecraft(vec))",
    "VSGameConfig.SERVER.getFTBChunks().getShipsProtectionOutOfBuildHeight()",
    "return newPos;",
):
    if text.count(anchor) < 1:
        raise SystemExit(f"fail-closed: required upstream FTB semantic anchor missing: {anchor!r}")

text = text.replace(old_max, new_max, 1)
text = text.replace(old_min, new_min, 1)

if old_max in text or old_min in text:
    raise SystemExit("fail-closed: legacy FTB build-height accessor remains")
if text.count(new_max) != 1:
    raise SystemExit("fail-closed: FTB exclusive max build-height expression did not converge exactly once")
# new_max contains one getMinY(), plus the explicit lower-bound getMinY().
if text.count("level.getMinY()") != 2 or text.count("level.getHeight()") != 1:
    raise SystemExit("fail-closed: FTB 26.2 build-height vocabulary count mismatch")

path.write_text(text, encoding="utf-8")
print("P1_FTBCHUNKS_BUILDHEIGHT_26_2_OVERLAY_APPLIED min=getMinY maxExclusive=getMinY+getHeight")

# OptiFine renderer section bounds are a separate optional-compat compile unit. Chain only
# after the now compile-proven FTB accessor transform; the remaining OptiFine dirty-authority
# call is intentionally left untouched for its own later proof.
optifine_range_helper = Path(__file__).with_name("apply_p1_optifine_levelrenderer_section_range_26_2.py")
if not optifine_range_helper.is_file():
    raise SystemExit(f"fail-closed: required OptiFine section-range helper missing: {optifine_range_helper}")
subprocess.run([sys.executable, str(optifine_range_helper), str(root)], check=True)
print("P1_OPTIFINE_LEVELRENDERER_SECTION_RANGE_26_2_CHAINED")
