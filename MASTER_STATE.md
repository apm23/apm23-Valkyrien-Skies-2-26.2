# MASTER_STATE — REAL VS2 26.2 PORT

GitHub code is the implementation source of truth. This file is the durable continuity ledger; chat memory is not authoritative.

## Project identity

- Repository: `apm23/apm23-Valkyrien-Skies-2-26.2`
- Mission: port the **actual original Valkyrien Skies 2 source** to Minecraft Java/Fabric 26.2, then integrate Create Fly / Steam 'n' Rails / Copycats only after standalone real VS2 is proven.
- Hard contract: **VS2 ASLI. BUKAN SYSTEM MIRIP VS2.**
- Architecture contract: `PORT_CONTRACT.md`.
- Exact dependency/environment lock: `BASELINE_LOCK.json`.
- Upstream provenance: `UPSTREAM_PROVENANCE.md`.

## Authoritative upstream baseline

- repository: `ValkyrienSkies/Valkyrien-Skies-2`
- branch used to select baseline: `1.21.1/main`
- exact commit: `f39132148e717d325933b4ce6e9e9fb13d929390`
- exact root tree: `91116399605d3ecd1c93b0011560e09281ee1fa4`
- upstream mod version: `2.4.12`
- imported as git submodule/gitlink `upstream-vs2/`

The upstream baseline remains pinned. Minecraft 26.2 changes are applied by explicit fail-closed overlays so every adaptation remains traceable to upstream VS2 source.

## Current reconciliation — canonical P1 chain through LavaFluid ServerLevel boundary

Current proven canonical source boundary before this ledger-only reconciliation commit:
- canonical implementation HEAD: `19b0e356b34dae20c3aa8d9409d90fc0b96838b2`.
- canonical P1 chain contains the prior frozen overlays plus the canonical LavaFluid ServerLevel overlay.
- exact-head P0 provenance run `35479600636`: `success`.
- exact-head LavaFluid randomTick ServerLevel proof run `35479600673`: `success`.
- exact-head canonical standalone compile run `35479600694`: compiler-frontier failure only; canonical overlay/apply steps completed and the remaining Java frontier failed as expected.
- compile artifact: `p1-compile-log-19b0e356b34dae20c3aa8d9409d90fc0b96838b2`, ID `10595491627`, size `21334` bytes, artifact digest `sha256:31054e1f3996d1b39a68c524c1b0392a772bed5dfb628670452e89f583f847d3`.
- compiler log contains **300 `error:` diagnostics across 34 normalized source files**.
- compared with prior canonical artifact `10595505232` at `5d0fd81810a824b2da989b834dd6d2f92475dc33`, `feature/fire_between_ship_and_world/LavaFluidMixin.java` is removed from the frontier and the only newly visible normalized source file is `feature/explosions/MixinExplosion.java`.

### LavaFluid randomTick ServerLevel boundary — frozen

Pinned upstream target:
`common/src/main/java/org/valkyrienskies/mod/mixin/feature/fire_between_ship_and_world/LavaFluidMixin.java`.

Minimal 26.2 bridge:
- injected callback/local level type is narrowed from `Level` to `ServerLevel` only so the existing vanilla `LavaFluid.randomTick(...)` invocation matches Minecraft 26.2.
- exact resolved Minecraft 26.2 jar `javap` proves `LavaFluid.randomTick(ServerLevel, BlockPos, FluidState, RandomSource)`.
- no cast, synthetic server lookup, replacement random source, or alternate tick authority was introduced.
- existing real VS2 fire-between-ship-and-world ship lookup/transform path, block-position conversion, recursion/branch behavior, fire behavior, random source, and vanilla `LavaFluid.randomTick` authority remain unchanged.

Evidence:
- targeted proof artifact `p1-lavafluid-randomtick-serverlevel-proof-19b0e356b34dae20c3aa8d9409d90fc0b96838b2`, ID `10594948261`, digest `sha256:3fe31b7e7cf3b2c184045d75cecb9c07bd054a62c1e02c311c9fd10069218c64`.
- exact proof run `35479600673`: success; resolved-jar `javap` records `randomTick(net.minecraft.server.level.ServerLevel, ...)` and exhaustive compile reports no `LavaFluidMixin.java` diagnostic.
- canonical commit `19b0e356b34dae20c3aa8d9409d90fc0b96838b2` installs `scripts/apply_p1_lavafluid_randomtick_serverlevel_26_2.py` into canonical `p1-compile.yml`.
- exact canonical P0 `35479600636`: success.
- exact canonical compile `35479600694`: frontier-only failure; artifact `10595491627`; 300 diagnostics / 34 normalized source files; LavaFluid target absent.
- comparison against artifact `10595505232`: LavaFluid left the normalized source frontier; only `feature/explosions/MixinExplosion.java` became newly visible under the compiler cap.

### Clip-replace Direction descriptor boundary — frozen

Pinned upstream target:
`common/src/main/java/org/valkyrienskies/mod/mixin/feature/clip_replace/MixinBlockGetter.java`.

Minimal 26.2 bridge:
- `Direction.getNearest(vec3.x, vec3.y, vec3.z)` -> `Direction.getApproximateNearest(vec3.x, vec3.y, vec3.z)` only.
- exact Minecraft 26.2 resolved client jar proved `getApproximateNearest(double,double,double)` exists while the old triple-double `getNearest` overload does not.
- the current method preserves nearest-direction selection from the three vector components; this is method-vocabulary drift only.
- existing real VS2 authorities remain unchanged: ship-managing lookup, existing ship/world clip path, `clipIncludeShipsImpl(...)`, vector `from - to`, face-selection intent, miss/hit construction, collision/raycast semantics, and reference-space transforms.
- no collision authority, raycast policy, movement authority, camera authority, ship transform authority, or custom reference frame was introduced.

Evidence:
- exact API probe proved Minecraft 26.2 `Direction.getApproximateNearest(double,double,double)` against the resolved Loom client jar before mutation.
- isolated candidate overlay changed exactly one call expression; semantic guards preserved all surrounding clip/reference-space authority.
- targeted exact-file proof run `35478456716`: success.
- targeted exact-head P0 run `35478456712`: success.
- canonical commit `5d0fd81810a824b2da989b834dd6d2f92475dc33` installs `scripts/apply_p1_clip_replace_direction_26_2.py` into canonical `p1-compile.yml`.
- exact canonical P0 `35478903000`: success.
- exact canonical clip-replace proof `35478902949`: success.
- exact canonical compile `35478902906`: frontier-only failure; artifact `10595505232`; 300 diagnostics / 34 normalized source files; target absent.
- comparison against artifact `10595080252`: only `feature/clip_replace/MixinBlockGetter.java` left the normalized source frontier; no new normalized source file appeared.

## Frozen recent canonical P1 boundaries

The following boundaries remain frozen green and may not be reopened without direct contradictory evidence:

- **World-weather BlockPos center** — target `feature/world_weather/MixinLevelRenderer.java`; `vanillaHeight.getCenter()` -> `Vec3.atCenterOf(vanillaHeight)` plus required import only. Canonical `2bafed0bb9001a49249d36f4b5b51a6fcdbcbebc`; P0 `35476486062`; proof `35476486047`; artifact `10595080252`; target absent.
- **Ship debug overlay BlockPos center** — target `feature/ship_debug_overlay/MixinDebugScreenOverlay.java`; block-center vocabulary bridge only. Canonical `7728fb1bb9f44b417039e1d3510b761c659564b7`; P0 `35475480606`; proof `35475480642`; target absent.
- **Tick-ship-chunks ChunkPos accessors** — exactly three `.x/.z` reads -> `.x()/.z()`; real VS2 distance/shipyard/spawn authorities unchanged. Canonical `20789867ea96d411cfc9e20402e074b235ea5877`; P0 `35474675327`; proof `35474675349`; target absent.
- **AirAndWaterRandomPos max-build** — old max-build getter -> `getMinY() + getHeight()` only as existing exclusive upper bound. Canonical `960582c42b407e9c4dbc1943f1d2cc3d8c3dbfe6`; P0 `35472794096`; proof `35472793999`; target absent.
- **POIManager ChunkPos construction** — `new ChunkPos(blockPos)` -> `ChunkPos.containing(blockPos)` only. Canonical `73197278b8ee26ced0dc267d84ea9eb825d02e98`; P0 `35471264991`; proof `35471264941`.
- **WaterFluid Level client accessor** — `level.isClientSide` -> `level.isClientSide()` only; canonical `224fb040c4e1f3ae9015d712fcac9d26447024bf`; P0 `35470783272`; proof `35470783283`.
- **EntitySectionStorage Level client accessor** — `level.isClientSide` -> `level.isClientSide()` only; canonical `f90a3c1979dd957a34d5a0ebebfe00ab5c6fc133`; P0 `35470148414`; proof `35470148397`.
- **NaturalSpawner ChunkPos accessors** — `chunk.getPos().x/z` -> `x()/z()` only; proof `35467860056`; P0 `35467860082`.
- **Particle-collision Level client accessor** — `level.isClientSide` -> `level.isClientSide()` only; no collision/reference-space authority change.
- **Shipyard teleport API adaptation** — old `RelativeMovement` vocabulary -> current `Relative`/`PositionMoveRotation` authority; real VS2 `ServerShip.getShipToWorld().transformPosition` stays authoritative; no manual packet/setPos chase. P0 `35467615792`; proof `35467615790`.
- **Canonical proof-overlay chain repair** — commit `8e40e5dc0885768727f16b96d5968080a7bd0ffb` canonicalized six previously proven overlays without changing their frozen semantics.

## Other frozen architecture-sensitive proofs

- **DistanceManager / TicketStorage read boundary** — implementation `8a338f95103227ed6a5acb35804d573bbae0d96c`; proof HEAD `ca07a2fff0fd922cbbd578a0531d3377313827de`; P0 `35463018487`; proof `35463018541`. Read-only compatibility only; it does not replace or modify real ship-ticket lifecycle.
- **Real VS2 ship chunk-ticket lifecycle** — implementation `65a42e782de192f27d5bf720691d6e08f395a719`; proof `35450402031`. Load-only radius-zero explicit ticket add/remove lifecycle, flush/order, ship-alive removal guard, and deletion cleanup remain authority.
- **ShipSavedData persistence** — implementation `f2b3ec68e0d2146bb8b443da76a62a4766e01fce`; proof `35451366140`. Overworld `SavedDataStorage` remains authority; `SavedDataType + Codec` is API bridge only.
- **Entity renderer submit lifecycle** — implementation `a87512437f40a3bfa1325d78f8e2588587ec7cc8`; proof HEAD `58d8554ba623896d486b91f18771df9bdcd6f2b3`; proof `35458380245`. Real VS2 render authorities remain authoritative.
- **Entity local-authority / interpolation** — implementation `b7e583af13598b6ddcc583380872f578b8a40bb8`; proof HEAD `9f2719be070e79b91b7f47ceddaec61d7f5cff40`; proof `35455551701`. Existing dragging information, ship transforms and interpolation authority remain intact.
- **Optional Create deployer helper isolation** — implementation `cd2434e69caf28e12560bf4444fc220a3023e40b`; proof `35454908850`. P1 compile isolation only, not Create integration.
- **Optional Sable Companion compile boundary** — overlay `58bd44154c20f141969b758b8e35372d982ac358`; proof HEAD `c0c1efb790c31f90c8916121f7c4a06864a58b7f`; proof `35454031987`. Compile-only; no 1.21.1 Sable runtime compatibility claim.
- **Renderer handler render-state boundary** — overlay `6a13ff6d1f730678d9dd793f575887c08792b161`; proof HEAD `6aa93ba02e830fa432f0b6e00185ea533227e967`; proof `35452733162`. Upstream VS2 transform math remains intact.

## Frozen implementation ancestry

All frozen-green and negative-evidence records in Git history remain binding. Ledger compaction does not unfreeze or supersede them. Key implementation ancestry includes:

- `30b9f70d3c6c71dfd30ca76339e19cfcb56461e4`: ShipAssembler block-entity ValueInput.
- `45de97f06a3ab25c1e19b0dc09790ebde2d8e851`: ShipAssembler Clearable.
- `e923ba7658197ff04af605e85507618c09dd390b`: RelocationUtil block-entity ValueInput.
- `52a05bdae75fd2a469287234c680bf191fd5b105`: RelocationUtil pending loot-table clear.
- `7a7e2f320605b27bb65e9f0bb6cb88d8aa41a4e7`: RelocationUtil neighbor-update.
- `ce6ff8bb8f06eeb8e98544f6bf9ca1e503936fdb`: RelocationUtil direct chunk-write zero flags.
- `2da9ca25e3ce6fd2f601cc2f6b626b0e3998a677`: ShipAssembler StructureProcessor.
- `aa26d707fac479c63a6a5e097ca65818dd145262`: ShipAssembler fast-path direct chunk-write.
- `12f182325f9f3e10c502afae7da567e4b1b95c28`: AssemblyUtil neighbor dispatch.
- `644d108b111bed17d0f3259dc840803f7c9a3192`: AssemblyUtil block-entity Value I/O.
- `820ef37e8ca012fe484d9960242cbfc0eefbacc8`: AssemblyUtil ScheduledTick non-null.
- `a803150d066fdc7e0a0bfdd5bd1661b85c627417`: AssemblyUtil direct chunk-write.
- `02e356638690d0413a105d409aaae4bcfd6e160c`: ShipAssembler `BlockPos` -> containing `ChunkPos`.
- `39e2abc40af3d785d4d6ca5f14ac7b28ef03334f`: ShipMountingEntity `kill(ServerLevel)`.
- `36549552477a1dd9b24cc12c6e21c6849b2e8b54`: ShipMountingEntity `hurtServer`.
- `0a23528d781baf280bb553a8f9fa94c21f447af2`: ShipMountingEntity Value I/O.
- `d258e69e46ce2f85c1ccb953dc97db7abd669841`: entity-handler projectile packages.
- `3d8d7255d36f26da902e0d43e1c830fa5015594e`: VSGameEvents RenderType package.
- `24802fb75610a3ceb1614fda1a78cab1fab7cfe5`: VSGameUtils build-height / packed chunk-key.
- `a5e219c7036937ce0ef4b5dfe5032bd82c764ee9`: VSGameUtils ResourceKey / Identifier.
- `ee7e9c56be55fd95114d0f7e194be69185db4385`: nullable translation arguments.
- `169e0007dcbeb2263701e6b41e40757de6d62ff2`: TestChair entity creation / positioning.
- `2c763500338955135d0700b273594a87dab9d982`: VSKeyBindings Category.
- `5c8a80eca1b996c4b89d5a394d7cfb9115d3f070`: CreativeModeTab.Output access.
- `4641ae31765f0d067923cc1ef54b9a26abe99a19`: TestHingeBlockEntity Value I/O.
- `ea2084954eb4edd2bd9922aa1f59342b76709809`: MassDatapackResolver registry-tag.
- `27e181c70184b2aac38eeb1a646905d93ba45023`: MassDatapackResolver typed reload listener.
- `ac739bbf0c1598087a6ae9b158117c4764ce3079`: DimensionParametersResolver typed reload listener.
- `2af9d9ba1d48f8a0baf825398d3d441b1219f19d`: VSEntityHandlerDataLoader typed reload listener.
- `9d82234aa769a6a0eece07f52e7d5ace2d334aab`: VSGamePackets Identifier vocabulary.

## Locked negative evidence

- `3bcbf90c75dc4d02448cfdb4590cc9c9674e0ed6` / run `35454717409`: wrong Kotlin-source-set exclusion for `DeployerScrollOptionSlot.kt`.
- `a72aaef8eca34a352ef949eeb57e6bbcda81171f`: `setUnsaved(false)` is invalid current API; do not replay absent direct new evidence.
- VSKeyBindings failed probes `e108526cbd728454c175c76bffc610d4e074da49`, `fcc65187d79c4b546883875da3597345db1e01cd`, `e9a3efd58acb2af9539628eb2875e6cb829c3cec`, `fb3c7e65a4c2089f6fa695114734d14836bde1d3` remain negative evidence.
- Actions self-push of workflow changes without `workflows` permission is a locked failed transport hypothesis; do not use it as the actual transport step. A validated exact commit/blob may be fast-forwarded through the GitHub connector after diff verification.
- retired `apm23/VS2-Create_Interactive` workarounds remain historical warning evidence only and are forbidden as implementation source.

## Remaining Java compile frontier

Canonical artifact `10595491627` at `19b0e356b34dae20c3aa8d9409d90fc0b96838b2` contains **300 `error:` diagnostics across 34 normalized source files**. This is evidence only and never permission to batch-fix categories.

Compared with prior artifact `10595505232`:
- removed from frontier: `feature/fire_between_ship_and_world/LavaFluidMixin.java`;
- newly visible normalized source file: `feature/explosions/MixinExplosion.java`.

Current broad categories remain:
1. AI/entity nested-goal and mapping/API drift.
2. client/render/HUD/debug-render lifecycle drift.
3. entity/player/teleport-reconnect and collision API drift outside already-frozen authority-sensitive units.
4. chunk/worldgen/server storage/API drift.
5. optional compatibility/dependency residue, including old mapped Create/Copycat and Sable surfaces that are not standalone-P1 runtime authority.

Current smallest observed mechanical units include:
- `feature/explosions/MixinExplosion.java`: one source diagnostic repeated across compile tasks; direct `Level.isClientSide` field access is private in 26.2. This is newly visible after LavaFluid left the capped frontier and has frozen same-vocabulary precedents.
- `feature/structure_template/StructureTemplateMixin.java`: block-entity save ValueOutput API drift.
- `world/chunk/MixinLevelChunk.java`: `ChunkSerializer` mapping/API drift.
- `feature/fix_render_chunk_sorting/MixinRenderChunk.java`: removed camera acquisition vocabulary; authority-sensitive and no frozen camera precedent exists yet.
- `feature/entity_collision/MixinLivingEntity.java`: local-authority method drift; authority-sensitive and not preferred for blind mechanical patch.
- `compat/create/AirFlowClipContext.java`: old mapped Create/Copycat residue; not preferred for standalone P1.

### Next candidate — Explosion Level client accessor, inspect/prove first

Pinned target:
`common/src/main/java/org/valkyrienskies/mod/mixin/feature/explosions/MixinExplosion.java`.

Fresh canonical compile reports only:
`isClientSide has private access in Level`
at the existing `if (this.level.isClientSide)` early-return in `doExplodeForce()`.

Pinned upstream inspection confirms that this check only gates the existing server-side explosion-force path before the real VS2 ship lookup, ship/world clipping, transforms, splitting hook, and `GameToPhysicsAdapter` force application. Frozen WaterFluid / EntitySectionStorage / particle-collision precedents already establish the 26.2 vocabulary change from direct `Level.isClientSide` field access to `Level.isClientSide()`.

Do **not** broaden or redesign explosion semantics. Before mutation, require this ledger HEAD to pass P0 and establish an exact-file fail-closed proof that the only source change is `this.level.isClientSide` -> `this.level.isClientSide()`. Preserve all existing real VS2 explosion force, ship lookup/transform, clipping, splitting, force application, recursive explosion, and getSeenPercent/noRayTrace behavior exactly.

## Target runtime baseline

- Minecraft `26.2`
- Java `25`
- Fabric Loader `0.19.3`
- Fabric API `0.160.0+26.2`, SHA-256 `5f3dff88e1661166e222213302b25ace6c36dc3683804cbd4b5acf93138ea05e`
- Create Fly `6.0.9-1`, SHA-256 `d9c6cb6116d5caa1174a289ecd7d3cdd463ccef6e8db1249ab0bcfcd8c935870`
- Steam 'n' Rails embedded `SNR.FLY-STABLE-1.2.2+fabric-mc26.2`, SHA-256 `33c87d5a7da0d468d3b6c0e99f726b835c63b693e7447fdaeca5e1f204caab84`
- Copycats embedded `3.0.7-createfly+mc.26.2-v1.14`, SHA-256 `1922db10a49dfab42c4c272fbaee41cdc149287cd08ca84148b497e598029858`
- `BASELINE_LOCK.json` is authoritative over filenames when metadata/hash disagree.

## Project state

- project_state: `P1_SOURCE_API_ADAPTATION_IN_PROGRESS`
- active_blocker: `MINECRAFT_26_2_JAVA_API_MIXIN_DRIFT`
- active_proof_head: `19b0e356b34dae20c3aa8d9409d90fc0b96838b2; canonical P1 chain through frozen LavaFluid ServerLevel boundary`
- active_proof_run: `P0 35479600636 success; LavaFluid exact proof 35479600673 success; canonical compile 35479600694 frontier-only failure; artifact 10595491627; 300 diagnostics / 34 normalized source files; LavaFluid target absent; MixinExplosion newly visible`
- active_hypothesis: `next smallest evidence-backed unit is feature/explosions/MixinExplosion direct Level.isClientSide field access; exact pinned source plus frozen 26.2 precedents indicate a one-token accessor-vocabulary bridge, but source mutation waits for this ledger HEAD P0 and exact-file fail-closed proof`
- final_ready: `false`
- user_runtime_validation: `NOT_APPLICABLE_YET`
- video_status: `NOT_APPLICABLE_YET`

## Engineering locks

- First-failure classification stays factual: provenance, build/mappings/API/loader/mixin/VSCore-native/networking/storage/transforms/rendering/collision/entity-player-camera/Create/SNR-Copycats/CI/final packaging.
- Make one evidence-backed root/semantic change at a time.
- Standalone real VS2 P1 must initialize before Create integration.
- Frozen TicketStorage read bridge is read-only compatibility; it may not be expanded into a replacement ticket lifecycle.
- Frozen real ship-ticket lifecycle remains the add/remove/load authority.
- Frozen renderer submit/state bridge may not be expanded into movement/camera/collision/gameplay authority.
- Frozen authority/interpolation bridge may not be expanded into a custom movement/carry system.
- Frozen Sable proof is compile-only and does not authorize bundling a 1.21.1 Sable runtime on 26.2.
- Frozen Create helper exclusion is P1 compile isolation only, not P3.
- Frozen ShipSavedData proof authorizes only its `SavedDataType + Codec` bridge and matching server acquisition change.
- Frozen shipyard teleport mapping may not be replaced by manual packet/setPos/teleport-chase authority.
- Frozen clip-replace boundary may not be expanded into collision/raycast/reference-space authority.
- Frozen LavaFluid boundary may not be expanded into custom fire/randomTick or server-selection authority.
- `FINAL_READY` is forbidden from CI alone.
- Video is closure-only and must not be used for ordinary compile/debug hypothesis testing.

## next_safe_action

1. This ledger reconciliation commit is documentation-only, not source proof. Require exact-head P0 provenance success before another source/workflow mutation.
2. Preserve every frozen boundary above and all frozen/negative evidence in Git history.
3. Use artifact `10595491627` as the current canonical 300-diagnostic / 34-normalized-file frontier unless HEAD/compiler state changes.
4. Inspect/prove only pinned `feature/explosions/MixinExplosion.java` and the exact Minecraft 26.2 `Level.isClientSide()` accessor boundary. Do not touch the surrounding explosion/reference-space logic.
5. If exact inspection/proof confirms the one bounded vocabulary bridge, create one fail-closed overlay changing exactly `this.level.isClientSide` -> `this.level.isClientSide()` and an exact-file exhaustive compiler proof; otherwise HOLD rather than widening scope.
6. Preserve existing VS2 explosion ship lookup/transform, ship/world clip, splitting hook, `GameToPhysicsAdapter` force application, recursive explosion, `getSeenPercent`, and `noRayTrace` behavior exactly.
7. Do not combine this with render-camera, entity collision/local authority, StructureTemplate ValueOutput, world/chunk serializer, movement packets, Create/Copycat, Sable, or any other cluster.
8. Remain standalone P1. Do not use Create/SNR/Copycats to hide real VS2 failures. Do not record ordinary compile/debug video.

## Video and milestone gate

- `M1_COMPLETE` is forbidden until full P2 real-VS2 runtime proof exists: real ship lifecycle, translation+rotation, ship-space, collision, standing/walking, jump-airborne-natural landing, floor/walls/ceiling, free stable camera/look, entity dragging/reference space, rendering, and client/server sync.
- `FINAL_BUILD`, `FINAL_VERIFY`, and `FINAL_READY` are not applicable during P1.