# MASTER_STATE — REAL VS2 26.2 PORT

GitHub code is the implementation source of truth. This file is the durable continuity ledger; chat memory is not authoritative. Git history remains binding for frozen-green and negative-evidence records even when this ledger is compacted.

## Project identity

- Repository: `apm23/apm23-Valkyrien-Skies-2-26.2`
- Mission: port the **actual original Valkyrien Skies 2 source** to Minecraft Java/Fabric 26.2, then integrate Create Fly / Steam 'n' Rails / Copycats only after standalone real VS2 is proven.
- Hard contract: **VS2 ASLI. BUKAN SYSTEM MIRIP VS2.**
- Architecture contract: `PORT_CONTRACT.md`.
- Dependency/environment lock: `BASELINE_LOCK.json`.
- Upstream provenance: `UPSTREAM_PROVENANCE.md`.

## Authoritative upstream baseline

- repository: `ValkyrienSkies/Valkyrien-Skies-2`
- selection branch: `1.21.1/main`
- exact commit: `f39132148e717d325933b4ce6e9e9fb13d929390`
- exact root tree: `91116399605d3ecd1c93b0011560e09281ee1fa4`
- upstream mod version: `2.4.12`
- imported as gitlink/submodule `upstream-vs2/`

Minecraft 26.2 changes are applied by explicit fail-closed overlays. Every core ported subsystem must remain traceable to upstream VS2 or be documented as a minimal 26.2 compatibility bridge.

## Current reconciliation — canonical P1 chain through ChunkMap shutdown-work boundary

Current proven implementation boundary before this documentation-only reconciliation commit:

- canonical implementation HEAD: `6faec034d400458d4471e8aa608c77ecb01119e9` — `ci: adapt ChunkMap shutdown work dispatchers for 26.2`.
- exact-head P0 provenance run `35492025315`: **success**.
- exact-head standalone P1 compile run `35492025305` (#123): **frontier-only failure**. All overlay/apply steps, port-delta validation, and Gradle runtime setup succeeded; only the remaining javac frontier failed.
- compile artifact: `p1-compile-log-6faec034d400458d4471e8aa608c77ecb01119e9`, ID `10599810712`, artifact digest `sha256:7766dbb259f545e85471624b6a8d8aa5d490454327efbcfe647f7f88d0abda23`.
- extracted `p1-compile.log`: 193588 bytes, SHA-256 `60903897cd141b4d1d17dcac4f0806f4ced029492891e59443ef9e98435464f0`.
- exact compile log contains **63 `: error:` diagnostics across 7 normalized source files**.
- `MixinChunkMapClose.java`, `ChunkTaskPriorityQueueSorter`, `ChunkTaskDispatcher`, `worldgenTaskDispatcher`, and `lightTaskDispatcher` have **zero mentions** in the exact-head compile log.
- immediately prior implementation HEAD `9b229bbadfc3bab5ed918556144ad566ca37e448` had artifact `10598698213` with **69 diagnostics across 8 normalized source files**. Therefore the bounded ChunkMap shutdown-work bridge removed exactly `MixinChunkMapClose.java` from the observed frontier without reopening previously frozen units.

## ChunkMap shutdown-work API bridge — frozen green

Pinned upstream target:
`common/src/main/java/org/valkyrienskies/mod/mixin/server/world/MixinChunkMapClose.java`.

Upstream VS2 intent preserved:

- primary shutdown fix remains `MixinMinecraftServer.preStopServer()`, which removes real VS2 `SHIP_CHUNK` tickets;
- `MixinChunkMapClose` remains defense-in-depth only;
- when `updatingChunkMap` contains only shipyard chunks, it evaluates vanilla non-ticket work and intentionally omits only `distanceManager.hasTickets()` because stale shipyard ticket entries may linger;
- no ticket lifecycle, chunk authority, ship lifecycle, transform, movement, collision, entity dragging, camera, rendering, or reference-space authority was replaced or introduced.

### Exact Minecraft 26.2 API proof

Probe-only commit: `080c8720ffd389b5f67e5218fd101c6c10e13c50`.

- P0 provenance run `35491869222`: **success**.
- exact API probe run `35491869220`: **success**.
- probe artifact: `p1-chunkmap-haswork-api-probe-080c8720ffd389b5f67e5218fd101c6c10e13c50`, ID `10599332974`, digest `sha256:c75ef5ec5287807fda907ce206b67918badce88b9dfaa94dd728044a2080de89`.
- extracted probe log SHA-256: `cbecc43ac4b1303cf5b2ae66ff6c22b65a80ff72dc63d57a0f833155d23a7095`.
- exact resolved 26.2 mapped jar proves old `ChunkTaskPriorityQueueSorter` is absent.
- exact `ChunkMap` contains `worldgenTaskDispatcher` and `lightTaskDispatcher`, both current task-dispatch boundaries.
- exact `ChunkMap.hasWork()` checks, in vanilla work semantics: light engine; pending unloads; updating map; POI work; `toDrop`; unload queue; `worldgenTaskDispatcher.hasWork()`; `lightTaskDispatcher.hasWork()`; then `distanceManager.hasTickets()`.
- exact `ChunkTaskDispatcher.hasWork()` exists and reports dispatcher/priority-queue work.
- probe marker: `CHUNKMAP_26_2_API_PROVEN old_sorter_absent=true current_dispatchers=true hasWork_signatures=true`.

### Minimal bridge installed by `6faec034d400458d4471e8aa608c77ecb01119e9`

Only the proven API structure changed:

- `ChunkTaskPriorityQueueSorter` import -> `ChunkTaskDispatcher`;
- one old `queueSorter` shadow -> two current shadows, `worldgenTaskDispatcher` and `lightTaskDispatcher`;
- `queueSorter.hasWork()` -> `worldgenTaskDispatcher.hasWork() || lightTaskDispatcher.hasWork()`.

The intentional omission of `distanceManager.hasTickets()` is unchanged. Do not reopen this boundary absent direct contradictory compile/runtime evidence.

## Recent mechanical Java convergence — preserved

The following already-landed changes must not be repeated blindly:

- `28ee0eabe77778dd2f9bbd84e528d9c3a6718531`: client sound `ResourceLocation` -> `Identifier`.
- `4aa395c810476d78c2f8cfb1bee423d2f5248616`: `BlockUtil` package relocation.
- `880df3aa1ecbdaf2a5b9974d65dd68a266fbc764`: `DimensionDataStorage` -> `SavedDataStorage` in `MixinChunkMap`.
- `82887915b04b1546129ab0dba610d4ba0ed7e075`: `applyCarvers` signature adaptation; obsolete `GenerationStep.Carving` removed only where unused.
- `9b229bbadfc3bab5ed918556144ad566ca37e448`: LevelChunk `ChunkSerializer` -> `SerializableChunkData` serialization-vocabulary bridge; exact artifact `10598698213` proves target absence.
- `6faec034d400458d4471e8aa608c77ecb01119e9`: ChunkMap shutdown-work dispatcher bridge described above.

These are API/mapping adaptations only and authorize no replacement VS2 architecture.

## Frozen architecture-sensitive boundaries

All prior frozen-green proof records in Git history remain binding. Key locks include:

- **Real VS2 ship chunk-ticket lifecycle** — implementation `65a42e782de192f27d5bf720691d6e08f395a719`; proof `35450402031`. Load-only radius-zero explicit ticket add/remove lifecycle, flush/order, ship-alive removal guard, and deletion cleanup remain authority.
- **DistanceManager / TicketStorage read bridge** — implementation `8a338f95103227ed6a5acb35804d573bbae0d96c`; proof HEAD `ca07a2fff0fd922cbbd578a0531d3377313827de`; P0 `35463018487`; proof `35463018541`. Read-only compatibility only; never expand into replacement ticket lifecycle.
- **ShipSavedData persistence** — implementation `f2b3ec68e0d2146bb8b443da76a62a4766e01fce`; proof `35451366140`. Vanilla saved-data storage remains authority; codec/type changes are API bridges only.
- **Entity local authority / interpolation** — implementation `b7e583af13598b6ddcc583380872f578b8a40bb8`; proof HEAD `9f2719be070e79b91b7f47ceddaec61d7f5cff40`; proof `35455551701`. Real dragging information, ship transforms, and interpolation authority remain intact; no synthetic carry system.
- **Entity renderer submit lifecycle** — implementation `a87512437f40a3bfa1325d78f8e2588587ec7cc8`; proof HEAD `58d8554ba623896d486b91f18771df9bdcd6f2b3`; proof `35458380245`. Real VS2 render authorities remain authoritative.
- **Shipyard teleport API mapping** — P0 `35467615792`; proof `35467615790`. Real VS2 ship-to-world transform remains authority; no manual packet/setPos/teleport chase.
- NaturalSpawner, particle collision, EntitySectionStorage, WaterFluid, POIManager, AirAndWaterRandomPos, tick-ship-chunks, ship-debug overlay, world-weather, clip-replace, LavaFluid, Explosion, StructureTemplate, LevelChunk, and ChunkMapClose canonical proof boundaries remain frozen green.
- **Clip-replace Direction vocabulary** — canonical `5d0fd81810a824b2da989b834dd6d2f92475dc33`; P0 `35478903000`; proof `35478902949`.
- **LavaFluid randomTick ServerLevel** — canonical `19b0e356b34dae20c3aa8d9409d90fc0b96838b2`; P0 `35479600636`; proof `35479600673`.
- **Explosion Level client accessor** — canonical `322dcf22e2baf25192682d4b9ee942f4a35dc86b`; P0 `35480514635`; proof `35480514714`.
- **Optional Sable Companion boundary** — compile-only. It does not authorize bundling or claiming a 1.21.1 Sable runtime on 26.2.
- **Optional Create deployer helper isolation** — P1 compile isolation only, never a substitute for P3 Create integration.

## Locked negative evidence

- `3bcbf90c75dc4d02448cfdb4590cc9c9674e0ed6` / run `35454717409`: wrong Kotlin-source-set exclusion for `DeployerScrollOptionSlot.kt`; do not replay.
- `a72aaef8eca34a352ef949eeb57e6bbcda81171f`: `setUnsaved(false)` is invalid current API; do not replay absent direct new evidence.
- VSKeyBindings failed probes `e108526cbd728454c175c76bffc610d4e074da49`, `fcc65187d79c4b546883875da3597345db1e01cd`, `e9a3efd58acb2af9539628eb2875e6cb829c3cec`, `fb3c7e65a4c2089f6fa695114734d14836bde1d3` remain negative evidence.
- Actions self-push of workflow changes without `workflows` permission is a locked failed transport hypothesis.
- retired `apm23/VS2-Create_Interactive` workarounds remain historical warning evidence only and are forbidden as implementation source.

## Current remaining Java compile frontier

Exact-head artifact `10599810712` at implementation HEAD `6faec034d400458d4471e8aa608c77ecb01119e9` contains **63 `: error:` diagnostics across 7 normalized source files**:

1. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/vanilla_renderer/MixinLevelRendererVanilla.java` — 24 diagnostics.
2. `common/src/main/java/org/valkyrienskies/mod/mixin/feature/render_ship_debug_bb/MixinDebugRenderer.java` — 9 diagnostics.
3. `common/src/main/java/org/valkyrienskies/mod/mixin/client/renderer/MixinLevelRenderer.java` — 6 diagnostics.
4. `common/src/main/java/org/valkyrienskies/mod/mixin/feature/render_pathfinding/MixinDebugRenderer.java` — 6 diagnostics.
5. `common/src/main/java/org/valkyrienskies/mod/mixin/feature/vs2_alpha_hud/MixinGui.java` — 6 diagnostics.
6. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/sable/MixinActiveSableCompanion.java` — 6 diagnostics.
7. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/sable/MixinSubLevelHoldingChunkMap.java` — 6 diagnostics.

Observed direct missing-symbol surfaces:

- ship-debug renderer: `MultiBufferSource`, `RenderType`, and `MultiBufferSource.BufferSource` vocabulary;
- pathfinding renderer: `MultiBufferSource.BufferSource` vocabulary;
- alpha HUD: `GuiGraphics` vocabulary / injected render callback type;
- client level renderer: `LightTexture` vocabulary / render signature;
- vanilla renderer compat: `Uniform`, `VertexBuffer`, `LightTexture`, `RenderType`, `ShaderInstance` plus related signatures;
- Sable: absent optional companion classes/packages.

Classification:

- all five non-Sable units are rendering/HUD/camera-adjacent and must not be blind-patched;
- both Sable units are optional compatibility residue and remain compile-only isolation territory, not standalone-P1 runtime authority;
- there is currently no remaining non-render core Java unit in the observed frontier.

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
- active_blocker: `MINECRAFT_26_2_RENDER_HUD_API_MIXIN_DRIFT`
- active_proof_head: `6faec034d400458d4471e8aa608c77ecb01119e9; canonical P1 chain through frozen ChunkMap shutdown-work dispatcher boundary`
- active_proof_run: `P0 35492025315 success; P1 compile 35492025305 frontier-only failure; artifact 10599810712; 63 diagnostics / 7 normalized source files; MixinChunkMapClose absent`
- active_hypothesis: `next work must inspect one smallest renderer/HUD boundary against exact resolved Minecraft 26.2 APIs before any mutation; do not batch renderer families and do not use Sable residue to hide standalone VS2 failures`
- final_ready: `false`
- user_runtime_validation: `NOT_APPLICABLE_YET`
- video_status: `NOT_APPLICABLE_YET`

## Engineering locks

- First-failure classification stays factual: provenance, build/mappings/API/loader/mixin/VSCore-native/networking/storage/transforms/rendering/collision/entity-player-camera/Create/SNR-Copycats/CI/final packaging.
- Make one evidence-backed root/semantic change at a time.
- Standalone real VS2 P1 must initialize before Create integration.
- Never replace ship-space/physics/collision/entity-dragging/player-camera systems with a new custom implementation.
- Never use synthetic carry/inertia, fake gravity, manual floor/wall/ceiling clamps, per-tick teleport/setPos chase, camera counter-rotation/forcing, duplicate authority, or floor-only success as final architecture.
- Frozen TicketStorage read bridge is read-only compatibility; frozen real ship-ticket lifecycle remains add/remove/load authority.
- Frozen renderer submit/state bridges may not be expanded into movement/camera/collision/gameplay authority.
- Frozen entity authority/interpolation bridge may not be expanded into a custom movement/carry system.
- Frozen Sable proof is compile-only and does not authorize bundling a 1.21.1 Sable runtime on 26.2.
- Frozen Create helper exclusion is P1 compile isolation only, not P3.
- Frozen shipyard teleport mapping may not be replaced by manual packet/setPos/teleport-chase authority.
- `FINAL_READY` is forbidden from CI alone.
- Video is closure-only and must not be used for ordinary compile/debug hypothesis testing.

## next_safe_action

1. This ledger reconciliation commit is documentation-only. Require exact-head P0 provenance success before another source/workflow mutation.
2. Preserve every frozen boundary and all negative evidence in Git history. Do not repeat landed patches.
3. Use exact-head compile artifact `10599810712` as the canonical **63-diagnostic / 7-source-file** frontier until HEAD/compiler state changes.
4. Do **not** batch-patch renderer/HUD classes by package-name guesswork and do not widen the frozen renderer authority bridges.
5. Preferred next inspection unit: pinned upstream `feature/vs2_alpha_hud/MixinGui.java`, because it has only two unique direct compiler failures (`GuiGraphics` import and corresponding callback parameter) repeated across compile tasks. Inspect the exact Minecraft 26.2 `Gui` render/status-effect overlay method and current graphics/context type before any source mutation.
6. If exact resolved 26.2 signatures prove one bounded HUD vocabulary/signature bridge with unchanged VS2 alpha-HUD behavior, create one fail-closed overlay and exact-file proof. Otherwise HOLD and inspect no broader renderer family.
7. Do not combine that unit with `MixinLevelRenderer`, vanilla renderer compat, debug renderers, Sable, Create/SNR/Copycats, movement, collision, entity dragging, or camera authority.
8. Remain standalone P1. No ordinary compile/debug video.

## Video and milestone gate

- `M1_COMPLETE` is forbidden until full P2 real-VS2 runtime proof exists: real ship lifecycle, translation+rotation, ship-space, collision, standing/walking, jump-airborne-natural landing, floor/walls/ceiling, stable free camera/look, entity dragging/reference space, rendering, and client/server sync.
- `FINAL_BUILD`, `FINAL_VERIFY`, and `FINAL_READY` are not applicable during P1.
- Video is closure-only. Visible failure overrides telemetry green. `FINAL_READY` still requires exact-final-JAR real-user runtime acceptance.
