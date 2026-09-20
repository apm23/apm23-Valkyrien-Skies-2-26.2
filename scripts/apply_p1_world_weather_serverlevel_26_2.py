#!/usr/bin/env python3
from pathlib import Path
import hashlib
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/feature/world_weather/MixinServerLevel.java"
text = path.read_text(encoding="utf-8")

# Exact pinned upstream source at f39132148e717d325933b4ce6e9e9fb13d929390.
expected_sha1 = "82442838833e64b8d854091be5b93f7ded8793c3"
# Git blob SHA is checked by reproducing Git's blob identity, not a plain file SHA-1.
raw = text.encode("utf-8")
blob_sha1 = hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()
if blob_sha1 != expected_sha1:
    raise SystemExit(
        f"fail-closed: unexpected pinned world-weather ServerLevel blob {blob_sha1}; expected {expected_sha1}"
    )

import_anchor = "import net.minecraft.world.level.levelgen.Heightmap.Types;\n"
vec3_import = "import net.minecraft.world.phys.Vec3;\n"
if text.count(import_anchor) != 1 or vec3_import in text:
    raise SystemExit("fail-closed: unexpected Vec3 import state in pinned world-weather ServerLevel mixin")

old_min_y = "BlockPos failure = BlockPos.ZERO.above(level.getMinBuildHeight() - 1);"
new_min_y = "BlockPos failure = BlockPos.ZERO.above(level.getMinY() - 1);"
old_result_center = "CompatUtil.INSTANCE.toSameSpaceAs(level, result.getCenter(), (Ship)null, ship)"
new_result_center = "CompatUtil.INSTANCE.toSameSpaceAs(level, Vec3.atCenterOf(result), (Ship)null, ship)"
old_pos_center = "CompatUtil.INSTANCE.toSameSpaceAs(level, pos.getCenter(), (Ship)null, shipRef.get())"
new_pos_center = "CompatUtil.INSTANCE.toSameSpaceAs(level, Vec3.atCenterOf(pos), (Ship)null, shipRef.get())"

expected = [
    (old_min_y, 1),
    (old_result_center, 1),
    (old_pos_center, 2),
]
for token, count in expected:
    actual = text.count(token)
    if actual != count:
        raise SystemExit(f"fail-closed: expected {count} occurrences of {token!r}, found {actual}")

# Preserve the original VS2 authority/behavior anchors.
anchors = [
    ("VSGameUtilsKt.getShipManagingPos(level, chunk.getPos())", 1),
    ("CompatUtil.INSTANCE.toSameSpaceAs(", 3),
    ("shipRef.set(ship);", 1),
    ("original.call(level, types, pos)", 1),
    ("original.call(level, types, worldPos)", 1),
]
for token, count in anchors:
    actual = text.count(token)
    if actual != count:
        raise SystemExit(f"fail-closed: authority anchor {token!r} count {actual}, expected {count}")

text = text.replace(import_anchor, import_anchor + vec3_import, 1)
text = text.replace(old_min_y, new_min_y, 1)
text = text.replace(old_result_center, new_result_center, 1)
text = text.replace(old_pos_center, new_pos_center, 2)

if text.count(new_min_y) != 1 or text.count(new_result_center) != 1 or text.count(new_pos_center) != 2:
    raise SystemExit("fail-closed: world-weather ServerLevel 26.2 adaptation did not converge exactly")
if any(token in text for token, _ in expected):
    raise SystemExit("fail-closed: obsolete world-weather ServerLevel vocabulary remains")
for token, count in anchors:
    if text.count(token) != count:
        raise SystemExit(f"fail-closed: authority anchor changed unexpectedly: {token!r}")

path.write_text(text, encoding="utf-8")
print("P1_WORLD_WEATHER_SERVERLEVEL_26_2_OVERLAY_APPLIED count=4")
