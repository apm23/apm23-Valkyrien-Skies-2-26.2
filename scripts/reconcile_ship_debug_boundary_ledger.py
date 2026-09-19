# -*- coding: utf-8 -*-
from pathlib import Path

path = Path("MASTER_STATE.md")
text = path.read_text(encoding="utf-8")


def replace_section(body: str, start: str, end: str, replacement: str) -> str:
    if body.count(start) != 1 or body.count(end) != 1:
        raise SystemExit(
            f"fail-closed section markers: {start!r}={body.count(start)} {end!r}={body.count(end)}"
        )
    a = body.index(start)
    b = body.index(end, a)
    return body[:a] + replacement.rstrip() + "\n\n" + body[b:]


current = """## Current reconciliation — canonical P1 chain through ship debug overlay BlockPos center boundary

Current proven canonical source boundary before this ledger-only reconciliation commit:
- canonical implementation HEAD: `7728fb1bb9f44b417039e1d3510b761c659564b7`.
- canonical P1 chain contains **82 ordered fail-closed overlays**.
- exact-head P0 provenance run `35475480606`: `success`.
- exact-head ship-debug-overlay proof run `35475480642`: `success`.
- exact-head canonical standalone compile run `35475480661`: compiler-frontier failure only; all 82 overlay/apply steps, port-delta validation, and Gradle-runtime validation were green before compilation.
- compile artifact: `p1-compile-log-7728fb1bb9f44b417039e1d3510b761c659564b7`, ID `10593368657`, size `21774` bytes, artifact SHA-256 `ab97633c5c7f71bf4d813c3d41695d5ff1517d356361687995d5248135710027`; contained `p1-compile.log` SHA-256 `debfaf1ffd7d79ba1ecb08f94b72bce43a64c19e9d49f9e1b783c75b954fb658`.
- compiler log contains **300 `error:` diagnostics across 36 normalized source files** with no javac cap marker observed.
- `feature/ship_debug_overlay/MixinDebugScreenOverlay.java` is absent from that frontier. Compared with tick-ship-chunks artifact `10593542676`, it disappeared and **no new normalized source file appeared**.

### Ship debug overlay BlockPos center boundary — frozen

Pinned upstream target:
`common/src/main/java/org/valkyrienskies/mod/mixin/feature/ship_debug_overlay/MixinDebugScreenOverlay.java`.

Minimal 26.2 bridge:
- `VSGameUtilsKt.toWorldCoordinates(ship, blockPos.getCenter())` -> `VSGameUtilsKt.toWorldCoordinates(ship, Vec3.atCenterOf(blockPos))`.
- This reuses the frozen CompatUtil center mapping and preserves the exact block-center geometry.
- Existing real VS2/debug authorities remain unchanged: ship lookup, loaded-server-ship lookup, ship slug/static/mass/scale/velocity/omega reporting, and `VSGameUtilsKt.toWorldCoordinates(ship, ...)`.
- No camera, movement, collision, entity-dragging, ship-transform, or custom reference-frame authority was introduced.

Evidence:
- fail-closed overlay script commit `3024896a2445955491e31786ed61115121879e40`.
- exact-file proof workflow commit `677c884ba4a89d5e1ee60da169cab230fad04a71`.
- canonical commit `7728fb1bb9f44b417039e1d3510b761c659564b7`.
- exact canonical P0 `35475480606`: success.
- exact canonical ship-debug-overlay proof `35475480642`: success, including isolated replay/apply/semantic validation, exhaustive compile, and exact target-file compiler-clean classifier.
- exact canonical compile `35475480661`: frontier-only failure; artifact `10593368657`; 300 diagnostics / 36 normalized source files; target absent.
"""
text = replace_section(
    text,
    "## Current reconciliation — canonical P1 chain through tick-ship-chunks ChunkPos accessor boundary",
    "### Tick-ship-chunks ChunkPos accessor boundary — frozen",
    current,
)

frontier = """## Remaining Java compile frontier

Canonical artifact `10593368657` at `7728fb1bb9f44b417039e1d3510b761c659564b7` contains **300 `error:` diagnostics across 36 normalized source files** with no javac cap marker observed. This is evidence only and never permission to batch-fix categories.

Compared with prior tick-ship-chunks artifact `10593542676`:
- removed from frontier: `feature/ship_debug_overlay/MixinDebugScreenOverlay.java`;
- newly visible normalized source files: none.

Current broad categories remain:
1. AI/entity nested-goal and mapping/API drift.
2. client/render/HUD/debug-render lifecycle drift.
3. entity/player/teleport-reconnect and collision API drift outside already-frozen authority-sensitive units.
4. chunk/worldgen/server storage/API drift.
5. optional compatibility/dependency residue, including old mapped Create/Copycat and Sable surfaces that are not standalone-P1 runtime authority.

Current smallest observed mechanical units include:
- `feature/world_weather/MixinLevelRenderer.java`: one removed `BlockPos.getCenter()` call at the existing weather-height coordinate conversion.
- `MixinBlockGetter.java`: `Direction.getNearest(double,double,double)` descriptor drift.
- `LavaFluidMixin.java`: `randomTick` now expects `ServerLevel`.
- `feature/fix_render_chunk_sorting/MixinRenderChunk.java`: removed `GameRenderer.getMainCamera()` and `Camera.getPosition()`; no frozen 26.2 camera-acquisition precedent exists yet.
- `MixinLivingEntity.java`: removed local-authority method; authority-sensitive and not preferred for a blind mechanical patch.
- `StructureTemplateMixin.java`: block-entity save ValueOutput API drift.
- `world/chunk/MixinLevelChunk.java`: `ChunkSerializer` mapping/API drift.
- `compat/create/AirFlowClipContext.java`: old mapped Create/Copycat dependency residue; not preferred for standalone P1.

### Next candidate — world-weather BlockPos center, proof first

Pinned target:
`common/src/main/java/org/valkyrienskies/mod/mixin/feature/world_weather/MixinLevelRenderer.java`.

Fresh canonical compile shows the bounded center-vocabulary diagnostic at:
`CompatUtil.INSTANCE.toSameSpaceAs(level, vanillaHeight.getCenter(), (Ship) null, null)`.

There are now two frozen local precedents for this exact geometry adaptation: the CompatUtil center bridge and the just-frozen ship-debug-overlay bridge. Inspect/prove only:
- `vanillaHeight.getCenter()` -> `Vec3.atCenterOf(vanillaHeight)`;
- add only the required `net.minecraft.world.phys.Vec3` import if the pinned file does not already import it.

Preserve all existing weather/ship behavior exactly: vanilla `getHeightmapPos` result, `CompatUtil.INSTANCE.toSameSpaceAs(...)`, `BlockPos.containing(...)`, ship heightmap hit, shared lookup position, block/fluid/collision surface lookup, and rain/snow render occlusion. This is a coordinate-vocabulary bridge only; it must not become camera, weather-policy, movement, collision-authority, or ship-transform authority.
"""
text = replace_section(text, "## Remaining Java compile frontier", "## Target runtime baseline", frontier)

state = """## Project state

- project_state: `P1_SOURCE_API_ADAPTATION_IN_PROGRESS`
- active_blocker: `MINECRAFT_26_2_JAVA_API_MIXIN_DRIFT`
- active_proof_head: `7728fb1bb9f44b417039e1d3510b761c659564b7; canonical P1 chain through ship debug overlay BlockPos center boundary`
- active_proof_run: `P0 35475480606 success; ship-debug-overlay exact proof 35475480642 success; canonical compile 35475480661 frontier-only failure; artifact 10593368657; 300 diagnostics / 36 normalized source files; target absent`
- active_hypothesis: `next smallest direct-precedent unit is feature/world_weather/MixinLevelRenderer vanillaHeight.getCenter(); prove only Vec3.atCenterOf(vanillaHeight) using frozen center precedents after this ledger HEAD passes P0`
- final_ready: `false`
- user_runtime_validation: `NOT_APPLICABLE_YET`
- video_status: `NOT_APPLICABLE_YET`
"""
text = replace_section(text, "## Project state", "## Engineering locks", state)

next_action = """## next_safe_action

1. This ledger reconciliation commit is documentation-only, not source proof. Require exact-head P0 provenance success before another source/workflow mutation.
2. Preserve every frozen boundary above and all frozen/negative evidence in Git history.
3. Use artifact `10593368657` as the current canonical 300-diagnostic / 36-normalized-file frontier unless HEAD/compiler state changes.
4. Inspect/prove only pinned `feature/world_weather/MixinLevelRenderer.java` BlockPos center vocabulary.
5. If still bounded and unambiguous, create one fail-closed overlay changing only `vanillaHeight.getCenter()` to `Vec3.atCenterOf(vanillaHeight)` plus the required Vec3 import, and an exact-file exhaustive compiler proof.
6. Preserve the existing weather heightmap, `CompatUtil.INSTANCE.toSameSpaceAs`, ship-heightmap-hit, shared surface lookup, block/fluid/collision lookup, and rain/snow occlusion semantics exactly.
7. Do not combine this with `MixinRenderChunk` camera API drift, `MixinBlockGetter`, LavaFluid, collision authority, StructureTemplate, world/chunk serializer drift, Create/Copycat, Sable, or any other cluster.
8. Remain standalone P1. Do not use Create/SNR/Copycats to hide real VS2 failures. Do not record ordinary compile/debug video.
"""
text = replace_section(text, "## next_safe_action", "## Video and milestone gate", next_action)

path.write_text(text, encoding="utf-8")
print("MASTER_STATE_SHIP_DEBUG_BOUNDARY_RECONCILED")
