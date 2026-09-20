#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/feature/ship_debug_overlay/MixinDebugScreenOverlay.java"
text = path.read_text(encoding="utf-8")

old = "VSGameUtilsKt.toWorldCoordinates(ship, blockPos.getCenter())"
new = "VSGameUtilsKt.toWorldCoordinates(ship, Vec3.atCenterOf(blockPos))"

if text.count(old) != 1:
    raise SystemExit(f"expected exactly one pinned ship-debug-overlay center expression in {path}, found {text.count(old)}")
if new in text:
    raise SystemExit(f"ship-debug-overlay center expression is already adapted in {path}")

anchors = [
    "VSGameUtilsKt.getShipManagingPos(l, blockPos)",
    "VSGameUtilsKt.getLoadedShipManagingPos((ServerLevel) l, blockPos)",
    "ship.getTransform().getShipToWorldScaling()",
    "ship.getVelocity()",
    "ship.getOmega()",
]
for anchor in anchors:
    if text.count(anchor) != 1:
        raise SystemExit(f"expected exactly one authority anchor {anchor!r} in {path}, found {text.count(anchor)}")

text = text.replace(old, new, 1)

if text.count(new) != 1 or old in text:
    raise SystemExit("fail-closed: ship-debug-overlay center replacement did not converge exactly once")
for anchor in anchors:
    if text.count(anchor) != 1:
        raise SystemExit(f"fail-closed: authority anchor changed unexpectedly: {anchor!r}")

path.write_text(text, encoding="utf-8")
print("P1_SHIP_DEBUG_OVERLAY_BLOCKPOS_CENTER_26_2_OVERLAY_APPLIED")

# Transport-only chaining for the separately proven pathfinding debug lifecycle adaptation.
helper = Path(__file__).with_name("apply_p1_pathfinding_debug_lifecycle_26_2.py")
if not helper.is_file():
    raise SystemExit(f"fail-closed: required pathfinding debug overlay helper missing: {helper}")
subprocess.run([sys.executable, str(helper), str(root)], check=True)

# Transport-only chaining for the LevelRenderer/GameRenderer/LevelExtractor 26.2 split.
level_helper = Path(__file__).with_name("apply_p1_levelrenderer_split_26_2.py")
if not level_helper.is_file():
    raise SystemExit(f"fail-closed: required LevelRenderer split overlay helper missing: {level_helper}")
subprocess.run([sys.executable, str(level_helper), str(root)], check=True)

# Transport-only chaining for the ship debug bounding-box gizmo adaptation.
bb_helper = Path(__file__).with_name("apply_p1_ship_debug_bb_gizmo_26_2.py")
if not bb_helper.is_file():
    raise SystemExit(f"fail-closed: required ship debug BB gizmo overlay helper missing: {bb_helper}")
subprocess.run([sys.executable, str(bb_helper), str(root)], check=True)

# Transport-only chaining for the Minecraft 26.2 vanilla terrain-renderer bridge.
renderer_helper = Path(__file__).with_name("apply_p1_vanilla_renderer_26_2.py")
if not renderer_helper.is_file():
    raise SystemExit(f"fail-closed: required vanilla renderer overlay helper missing: {renderer_helper}")
subprocess.run([sys.executable, str(renderer_helper), str(root)], check=True)

# Transport-only isolation for the two exact legacy Sable compatibility mixins.
sable_helper = Path(__file__).with_name("apply_p1_legacy_sable_compileonly_isolation_26_2.py")
if not sable_helper.is_file():
    raise SystemExit(f"fail-closed: required legacy Sable isolation helper missing: {sable_helper}")
subprocess.run([sys.executable, str(sable_helper), str(root)], check=True)
print("P1_LEGACY_SABLE_COMPILEONLY_ISOLATION_CHAINED_HITBOX_GATE_V2")

# Mechanical record-accessor adaptation for the exact 54 active ChunkPos.x/z call sites.
chunkpos_helper = Path(__file__).with_name("apply_p1_chunkpos_record_accessors_26_2.py")
if not chunkpos_helper.is_file():
    raise SystemExit(f"fail-closed: required ChunkPos accessor overlay helper missing: {chunkpos_helper}")
subprocess.run([sys.executable, str(chunkpos_helper), str(root)], check=True)
print("P1_CHUNKPOS_RECORD_ACCESSORS_26_2_CHAINED_V3")

# Mechanical accessor adaptation for seven exact Level.isClientSide field uses that
# Minecraft 26.2 now exposes through the public isClientSide() method.
clientside_helper = Path(__file__).with_name("apply_p1_level_clientside_accessor_26_2.py")
if not clientside_helper.is_file():
    raise SystemExit(f"fail-closed: required Level client-side accessor overlay helper missing: {clientside_helper}")
subprocess.run([sys.executable, str(clientside_helper), str(root)], check=True)
print("P1_LEVEL_CLIENTSIDE_ACCESSOR_26_2_CHAINED")

# Mechanical Optional-unwrapping adaptation for seven exact CompoundTag primitive reads.
# Use the legacy numeric fallback value so old VS2 save semantics are preserved.
nbt_helper = Path(__file__).with_name("apply_p1_compoundtag_optional_primitives_26_2.py")
if not nbt_helper.is_file():
    raise SystemExit(f"fail-closed: required CompoundTag Optional primitive overlay helper missing: {nbt_helper}")
subprocess.run([sys.executable, str(nbt_helper), str(root)], check=True)
print("P1_COMPOUNDTAG_OPTIONAL_PRIMITIVES_26_2_CHAINED")

# Mechanical ServerLevel weather vocabulary adaptation: getMinY() and Vec3.atCenterOf.
# Preserve the upstream VS2 occlusion/biome/precipitation transform authority unchanged.
weather_server_helper = Path(__file__).with_name("apply_p1_world_weather_serverlevel_26_2.py")
if not weather_server_helper.is_file():
    raise SystemExit(f"fail-closed: required world-weather ServerLevel overlay helper missing: {weather_server_helper}")
subprocess.run([sys.executable, str(weather_server_helper), str(root)], check=True)
print("P1_WORLD_WEATHER_SERVERLEVEL_26_2_CHAINED")

# Mechanical Camera accessor adaptation proven from the exact MC26.2 Camera javap artifact.
# Changes only getPosition() -> position() on already-owned Camera instances; no camera acquisition,
# transform, orientation, or authority logic changes.
camera_position_helper = Path(__file__).with_name("apply_p1_camera_position_accessor_26_2.py")
if not camera_position_helper.is_file():
    raise SystemExit(f"fail-closed: required Camera position accessor overlay helper missing: {camera_position_helper}")
subprocess.run([sys.executable, str(camera_position_helper), str(root)], check=True)
print("P1_CAMERA_POSITION_ACCESSOR_26_2_CHAINED_V2")

# Exact 26.2 GameRenderer/Camera vocabulary for the upstream render-chunk sorting fix.
# Keeps VS2 ship-to-world transform and distance calculation unchanged.
render_chunk_camera_helper = Path(__file__).with_name("apply_p1_render_chunk_sorting_camera_26_2.py")
if not render_chunk_camera_helper.is_file():
    raise SystemExit(f"fail-closed: required render-chunk sorting Camera overlay helper missing: {render_chunk_camera_helper}")
subprocess.run([sys.executable, str(render_chunk_camera_helper), str(root)], check=True)
print("P1_RENDER_CHUNK_SORTING_CAMERA_26_2_CHAINED")

# Mechanical LevelHeightAccessor vocabulary adaptation in the shipyard noise-generation guard.
# Preserve VS2ChunkAllocator shipyard authority and all generation cancellation semantics.
noise_height_helper = Path(__file__).with_name("apply_p1_noisebased_height_accessor_26_2.py")
if not noise_height_helper.is_file():
    raise SystemExit(f"fail-closed: required NoiseBasedChunkGenerator height overlay helper missing: {noise_height_helper}")
subprocess.run([sys.executable, str(noise_height_helper), str(root)], check=True)
print("P1_NOISEBASED_HEIGHT_ACCESSOR_26_2_CHAINED_RECONNECT_CTOR_V2")
