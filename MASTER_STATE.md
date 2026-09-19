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

## Current reconciliation — canonical P1 chain through POIManager ChunkPos construction

Current proven canonical source boundary before this ledger-only reconciliation commit:
- canonical implementation HEAD: `73197278b8ee26ced0dc267d84ea9eb825d02e98`
- canonical P1 chain contains **79 ordered fail-closed overlays**.
- exact-head P0 provenance run `35471264991`: `success`.
- exact-head POIManager proof run `35471264941`: `success`.
- exact-head canonical standalone compile run `35471264985`: compiler-frontier failure only; every overlay/apply/delta-validation step before compilation was green.
- compile artifact: `p1-compile-log-73197278b8ee26ced0dc267d84ea9eb825d02e98`, ID `10592549176`, size `22090` bytes, SHA-256 `1d9ab6e6c707cccace39a6a01ff9c5f527001170be222f03a84ff3cc67fdc9b1`.
- exhaustive uncapped compiler frontier: **300 `error:` diagnostics across 37 source files**; no javac cap marker.
- `MixinPOIManager.java` is absent from that frontier.

### POIManager ChunkPos construction boundary — frozen

Pinned upstream target:
`common/src/main/java/org/valkyrienskies/mod/mixin/feature/poi/MixinPOIManager.java`.

Minimal 26.2 bridge:
- `ChunkPos.rangeClosed(new ChunkPos(blockPos), j)` -> `ChunkPos.rangeClosed(ChunkPos.containing(blockPos), j)`.
- This reuses the already-frozen ShipAssembler BlockPos→ChunkPos mapping precedent from `02e356638690d0413a105d409aaae4bcfd6e160c`.
- Existing POI authorities/semantics remain unchanged: `Math.floorDiv(i, 16) + 1` radius, AABB range, loaded-ship intersection, `POIChunkSearcher.shipChunkBounds(ship.getActiveChunksSet())`, `getInChunk(...)`, and world-coordinate conversion.
- No POI policy, AI behavior, ship transform, ticket lifecycle, movement/collision/camera authority, or custom reference frame was introduced.

Evidence:
- fail-closed overlay commit `49e25966f7195a2689417b65d47ec14f96b2acb8`.
- isolated proof workflow HEAD `2cfae46b189661f5bbaece68283bc927d61f4b2a`.
- isolated P0 `35471091468`: success.
- isolated POI proof `35471091469`: success.
- canonicalizer staging HEAD `c57429b56409c9b3fa5eecb8d135970632620d0a`.
- canonicalizer run `35471245342`: transformation, `git diff --check`, and local validated commit creation succeeded; only Actions transport failed because the GitHub App cannot update workflow files without `workflows` permission.
- validated canonical commit `73197278b8ee26ced0dc267d84ea9eb825d02e98` was fast-forwarded through the GitHub connector.
- exact canonical P0 `35471264991`: success.
- exact canonical POI proof `35471264941`: success.
- exact canonical compile `35471264985`: frontier-only failure; artifact `10592549176`; 300 diagnostics / 37 files.

The Actions self-push workflow-permission failure is a **locked transport negative**. Do not retry Actions self-push as the actual transport mechanism for workflow-file changes; a locally validated exact commit may be fast-forwarded through the connector after diff verification.

## Recently frozen canonical P1 boundaries

### WaterFluid Level client accessor — frozen

Target: `common/src/main/java/org/valkyrienskies/mod/mixin/feature/submarines/MixinWaterFluid.java`.

- only bridge: `level.isClientSide` -> `level.isClientSide()` inside existing `ValkyrienSkies.isConnectivityEnabled(...)`.
- VS2 authorities preserved: `isBlockInShipyard`, `getShipsIntersecting`, `ship.getWorldToShip().transformPosition`, `isPositionMaybeSealed`, and original `ci.cancel()`.
- script commit `377eddea6c20c828762aa7ed40e2c8f273f0a17c`.
- isolated proof HEAD `e28b1695a2f374b0fb62debdd5171e42c0d94a15`; P0 `35470549956`; proof `35470549962`: success.
- canonical commit `224fb040c4e1f3ae9015d712fcac9d26447024bf`; P0 `35470783272`; exact proof `35470783283`: success.
- canonical compile `35470783276`; artifact `10592822987`, SHA-256 `4c85123a2c56c0beafa0ae0d42a5ec1877a7a2adb73aa540db4ebdf30e6d391f`; frontier 300 / 38 files.

### Shipyard teleport API adaptation — frozen

The authority-sensitive teleport unit was inspected against Minecraft 26.2 before adaptation. Frozen mapping:
- old `RelativeMovement` vocabulary -> current `Relative` vocabulary where required.
- current `PositionMoveRotation`/vanilla teleport authority is used; no manual packet/awaiting-teleport/`absMoveTo` replacement was introduced.
- real VS2 `ServerShip.getShipToWorld().transformPosition` remains the ship-to-world transform authority.
- transformed X/Y/Z are absolute, so only relative X/Y/Z flags are removed; delta movement, yaw, and pitch semantics are preserved.
- ServerPlayer teleport boolean semantics are preserved; dismount teleport remains `false`.

Exact target files proven compiler-clean:
- `org/valkyrienskies/mod/mixin/feature/shipyard_entities/MixinEntity.java`
- `org/valkyrienskies/mod/mixin/server/command/level/MixinServerPlayer.java`
- `org/valkyrienskies/mod/mixin/server/network/MixinServerGamePacketListenerImpl.java`

Canonical exact-head proof `35467615790`: success. P0 `35467615792`: success.

### Canonical proof-overlay chain repair — frozen

Commit `8e40e5dc0885768727f16b96d5968080a7bd0ffb` canonicalized six already-proven overlays that had previously existed only in targeted proof replay:
- entity-handler render state
- Sable compile boundary
- optional Create deployer exclusion
- entity local-authority/interpolation
- entity renderer submit
- DistanceManager/TicketStorage

Canonical compile `35467615786` produced artifact `10591658320` and established the then-current exhaustive frontier at 300 diagnostics / 42 files.

### NaturalSpawner ChunkPos accessor — frozen

- `chunk.getPos().x/z` -> `chunk.getPos().x()/z()` only.
- shipyard spawn policy and `VSGameConfig.SERVER.getAllowMobSpawns()` unchanged.
- isolated proof `35467860056`: success; P0 `35467860082`: success.

### Particle-collision Level client accessor — frozen

- target `feature/particle_collision/MixinEntity.java`.
- `level.isClientSide` -> `level.isClientSide()` only.
- no VS2 particle/collision/reference-space authority change.

### EntitySectionStorage Level client accessor — frozen

- target `feature/shipyard_entities/MixinEntitySectionStorage.java`.
- `level.isClientSide` -> `level.isClientSide()` only at existing client ship-load listener branch.
- canonical commit `f90a3c1979dd957a34d5a0ebebfe00ab5c6fc133`.
- P0 `35470148414`: success; exact proof `35470148397`: success.
- canonical compile `35470148413`; artifact `10592178068`, SHA-256 `9264730d7997684cf9152e17b82943053a69e86b31c3e8dd7fd0e0e686578a15`; frontier 300 / 39 files.

## Frozen DistanceManager / TicketStorage read boundary

- implementation `8a338f95103227ed6a5acb35804d573bbae0d96c`.
- bounded proof/classifier HEAD `ca07a2fff0fd922cbbd578a0531d3377313827de`.
- P0 `35463018487`: success; proof `35463018541`: success.
- artifact `10590562117`, SHA-256 `269700efd41b44176ebce58c282a22a8a6af64b69fe39c532607548663ced2ee`.
- `DistanceManagerAccessor` exposes current `TicketStorage`; membership reads use `TicketStorage.getTickets(long).isEmpty()` and current packed chunk-key vocabulary.
- read-only compatibility only; it does not replace or modify the frozen real ship-ticket lifecycle.

## Other frozen proofs

### Frozen entity renderer submit lifecycle
- implementation `a87512437f40a3bfa1325d78f8e2588587ec7cc8`; proof HEAD `58d8554ba623896d486b91f18771df9bdcd6f2b3`; proof `35458380245`: success.
- real VS2 render authorities (`ClientShip`, `ShipMountedToData`, `VSEntityManager`, ship transforms) remain authoritative.

### Frozen entity local-authority / interpolation
- implementation `b7e583af13598b6ddcc583380872f578b8a40bb8`; proof HEAD `9f2719be070e79b91b7f47ceddaec61d7f5cff40`; proof `35455551701`.
- `isControlledByLocalInstance` -> `isLocalInstanceAuthoritative()` at exact existing sites; old non-living `lerpTo(..., 3)` -> vanilla `moveOrInterpolateTo(...)`.
- existing dragging information, ship transforms, and interpolation authority remain intact.

### Optional Create deployer helper isolation
- implementation `cd2434e69caf28e12560bf4444fc220a3023e40b`; proof `35454908850`: success.
- exactly one unreferenced helper excluded for standalone P1; this is not Create integration.

### Optional Sable Companion compile boundary
- overlay `58bd44154c20f141969b758b8e35372d982ac358`; proof HEAD `c0c1efb790c31f90c8916121f7c4a06864a58b7f`; proof `35454031987`.
- compile-only; no 1.21.1 Sable runtime compatibility claim.

### Renderer handler render-state boundary
- overlay `6a13ff6d1f730678d9dd793f575887c08792b161`; proof HEAD `6aa93ba02e830fa432f0b6e00185ea533227e967`; proof `35452733162`.
- upstream VS2 transform math remains intact.

### ShipSavedData persistence boundary
- implementation `f2b3ec68e0d2146bb8b443da76a62a4766e01fce`; proof `35451366140`: success.
- overworld `SavedDataStorage` remains authority; `SavedDataType + Codec` is an API bridge only.

### Real VS2 ship chunk-ticket lifecycle
- implementation `65a42e782de192f27d5bf720691d6e08f395a719`; proof `35450402031`: success.
- load-only radius-zero explicit ticket add/remove lifecycle, distance-manager flush/order, ship-alive removal guard, and `tryMarkSaved()` deletion cleanup remain frozen.

## Frozen proof ancestry / negative evidence

All frozen-green and negative-evidence records in Git history remain binding. Ledger compaction does not unfreeze or supersede them.

Key frozen implementation ancestry:
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

Locked negative evidence:
- `3bcbf90c75dc4d02448cfdb4590cc9c9674e0ed6` / run `35454717409`: wrong Kotlin-source-set exclusion for `DeployerScrollOptionSlot.kt`.
- `a72aaef8eca34a352ef949eeb57e6bbcda81171f`: `setUnsaved(false)` is invalid current API; do not replay absent direct new evidence.
- VSKeyBindings failed probes `e108526cbd728454c175c76bffc610d4e074da49`, `fcc65187d79c4b546883875da3597345db1e01cd`, `e9a3efd58acb2af9539628eb2875e6cb829c3cec`, `fb3c7e65a4c2089f6fa695114734d14836bde1d3` remain negative evidence.
- Actions self-push of workflow changes without `workflows` permission is a locked failed transport hypothesis; do not use it as the actual transport step.
- retired `apm23/VS2-Create_Interactive` workarounds remain historical warning evidence only and are forbidden as implementation source.

## Remaining Java compile frontier

Canonical artifact `10592549176` at `73197278b8ee26ced0dc267d84ea9eb825d02e98` contains **300 uncapped diagnostics across 37 source files**. This is evidence only and never permission to batch-fix categories.

Current broad categories include:
1. AI/entity nested-goal and mapping/API drift.
2. client/render/HUD/debug-render lifecycle drift.
3. entity/player/teleport-reconnect and collision API drift outside already-frozen authority-sensitive units.
4. chunk/worldgen/server storage/API drift.
5. optional compatibility/dependency residue, including old mapped Create/Copycat and Sable surfaces that are not standalone-P1 runtime authority.

Current three-diagnostic units include:
- `MixinAirAndWaterRandomPos.java`: removed `Level.getMaxBuildHeight()`.
- `MixinBlockGetter.java`: `Direction.getNearest(double,double,double)` descriptor drift.
- `LavaFluidMixin.java`: `randomTick` now expects `ServerLevel`.
- `MixinLivingEntity.java`: removed local-authority method; authority-sensitive, not preferred for a blind mechanical patch.
- `MixinDebugScreenOverlay.java`: removed `BlockPos.getCenter()`.
- `StructureTemplateMixin.java`: block-entity save ValueOutput API drift.
- `feature/world_weather/MixinLevelRenderer.java`: removed `BlockPos.getCenter()`.
- `world/chunk/MixinLevelChunk.java`: `ChunkSerializer` mapping/API drift.
- `compat/create/AirFlowClipContext.java`: old mapped Create/Copycat dependency residue; not preferred for standalone P1.

### Next candidate — AirAndWaterRandomPos max-build boundary, proof first

Pinned target:
`common/src/main/java/org/valkyrienskies/mod/mixin/feature/ai/path_retargeting/MixinAirAndWaterRandomPos.java`.

Current compiler diagnostic is one source site repeated by the three compile tasks/log passes:
`pathfinderMob.level().getMaxBuildHeight()` no longer exists in Minecraft 26.2 inside the existing `RandomPos.moveUpOutOfSolid(...)` call.

Existing frozen precedent `scripts/apply_p1_compatutil_buildheight_26_2.py` already maps the old exclusive max-build boundary to `level.getMinY() + level.getHeight()` in real VS2 CompatUtil. The pinned AirAndWaterRandomPos source uses the value only as the same upper build-height argument; the surrounding VS2 logic is separate and must remain unchanged:
- null return guard and `blockPos2` guard;
- loaded-ship intersection;
- `ship.getWorldToShip().transformPosition(...)`;
- `BlockPos.containing(...)`;
- `GoalUtils.isRestricted(...)` and `GoalUtils.hasMalus(...)`;
- `RandomPos.moveUpOutOfSolid(...)` callback;
- `cir.setReturnValue(blockPosInShip)` and break behavior.

No patch has been applied to this target yet. Inspect/prove exactly one accessor-vocabulary replacement before canonicalization. Do not alter AI policy, pathfinding, ship transforms, movement/collision/camera authority, or any other file.

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
- active_proof_head: `73197278b8ee26ced0dc267d84ea9eb825d02e98; canonical P1 chain through POIManager ChunkPos containing`
- active_proof_run: `P0 35471264991 success; POI exact proof 35471264941 success; canonical compile 35471264985 frontier-only failure; artifact 10592549176; 300 diagnostics / 37 files; no javac cap marker`
- active_hypothesis: `next smallest evidence-backed unit is MixinAirAndWaterRandomPos max-build accessor; reuse frozen exclusive-max boundary level.getMinY()+level.getHeight() only after this ledger HEAD passes P0`
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
- `FINAL_READY` is forbidden from CI alone.
- Video is closure-only and must not be used for ordinary compile/debug hypothesis testing.

## next_safe_action

1. This ledger commit is documentation-only, not source proof. Require exact-head P0 provenance success before another source/workflow mutation.
2. Preserve every frozen boundary above and all frozen/negative evidence in Git history.
3. Use artifact `10592549176` as the current canonical 300-diagnostic / 37-file frontier unless HEAD/compiler state changes.
4. Inspect/prove only the pinned `MixinAirAndWaterRandomPos.java` max-build accessor site.
5. If still bounded and unambiguous, create one fail-closed overlay changing only `pathfinderMob.level().getMaxBuildHeight()` to the already-frozen 26.2 exclusive-max expression `pathfinderMob.level().getMinY() + pathfinderMob.level().getHeight()` and an exact-file exhaustive compiler proof.
6. Preserve loaded-ship intersection, world-to-ship transform, restriction/malus checks, `moveUpOutOfSolid` callback, return/break behavior, and all AI/pathfinding semantics.
7. Do not combine this with `MixinBlockGetter`, LavaFluid, collision authority, render/HUD, StructureTemplate, Create/Copycat, Sable, or any other cluster.
8. Remain standalone P1. Do not use Create/SNR/Copycats to hide real VS2 failures. Do not record ordinary compile/debug video.

## Video and milestone gate

- `M1_COMPLETE` is forbidden until full P2 real-VS2 runtime proof exists: real ship lifecycle, translation+rotation, ship-space, collision, standing/walking, jump-airborne-natural landing, floor/walls/ceiling, free stable camera/look, entity dragging/reference space, rendering, and client/server sync.
- `FINAL_BUILD`, `FINAL_VERIFY`, and `FINAL_READY` are not applicable during P1.
