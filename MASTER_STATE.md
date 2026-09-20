# MASTER_STATE — REAL VS2 26.2 PORT

GitHub code is the implementation source of truth. This file is the durable continuity ledger; chat memory is not authoritative. Git history remains binding for every frozen-green and negative-evidence record even when this ledger is compacted.

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

## Current reconciliation — canonical P1 chain through LevelRenderer / LevelExtractor split bridge

Current proven implementation boundary before this documentation-only reconciliation commit:

- canonical implementation HEAD: `660d5320902a3ecba4f3219969aa77b0316cfa52` — `ci: wire proven LevelRenderer split overlay`.
- exact-head P0 provenance run `35495275084`: **success**.
- exact-head standalone P1 compile run `35495275097` (#126): **frontier-only failure**. Every canonical overlay/apply step, port-delta validation, Gradle runtime setup, and diagnostic upload succeeded; only the remaining javac frontier failed.
- compile artifact: `p1-compile-log-660d5320902a3ecba4f3219969aa77b0316cfa52`, ID `10600448490`, artifact digest `sha256:a10100d02d295cdfc0466c5761ec41f82cedfcf00d1efd857f27ce379b8a4986`.
- extracted `p1-compile.log`: 186698 bytes, SHA-256 `4b22fee82f3cfe2d87f2c87eb6581d1e7317565d5b22e68a22a5d4bb55504996`.
- exact compile log contains **45 `: error:` diagnostics across 4 normalized source files**.
- both `common/src/main/java/org/valkyrienskies/mod/mixin/client/renderer/MixinLevelRenderer.java` and the new `MixinLevelExtractor.java` have **zero mentions** in the exact compile log.
- frozen `feature/render_pathfinding/MixinDebugRenderer.java` and frozen ship-debug-overlay `MixinDebugScreenOverlay.java` also have **zero mentions**.
- immediately prior canonical implementation `f56fa6d76d31661e561de85b7223b6de64e39de9` had artifact `10599943032` with **51 diagnostics across 5 files**. Therefore this bounded renderer-split bridge removed exactly the old client `MixinLevelRenderer.java` compile unit without creating a new compile unit.
- frozen ship-debug-overlay proof reran at this exact implementation HEAD as run `35495275080`: **success**, including isolated semantic validation and exact-file compiler-clean proof. Transport chaining did not reopen that frozen source boundary.

## LevelRenderer / LevelExtractor 26.2 split bridge — frozen green

Pinned upstream semantic unit:
`common/src/main/java/org/valkyrienskies/mod/mixin/client/renderer/MixinLevelRenderer.java`.

Pinned upstream active behavior had two independent pieces:

1. at old `LevelRenderer.renderLevel(...)` HEAD, read the existing VS-mounted transform from the already-existing vanilla `Camera` via `IVSCamera`, compare it with the previous transform, and call vanilla `SectionOcclusionGraph.invalidate()` when the ship-mounted camera rotation changes by more than one degree;
2. replace the vanilla `1024.0` block-damage render distance constant with `Double.MAX_VALUE`, making block damage visible independent of that vanilla cap.

No new camera transform, carry system, camera forcing, movement, collision, or ship-space authority is part of this unit.

### Exact 26.2 API evidence

Initial inspection-only commit `3e824228a912d9af4e8af5e4bdab29cf2ed11944`:

- P0 run `35494738858`: **success**;
- API probe run `35494738882`: fail-closed **failure after successful exact classpath/javap inspection** because the probe deliberately expected the obsolete owner shape;
- artifact `p1-levelrenderer-api-probe-3e824228a912d9af4e8af5e4bdab29cf2ed11944`, ID `10600437709`, digest `sha256:405f650030249271cd8b5c2d3675399e4d814aa7e3f7df982379876237406505`;
- exact evidence proved `LevelRenderer.renderLevel(...)` is gone, obsolete `LightTexture` is absent, and `renderLevel(DeltaTracker)` now belongs to `GameRenderer`.

Successful split-lifecycle probe commit `ea4fe41eea15ff879ddcebe005f401bf01c0ce23`:

- P0 run `35494987862`: **success**;
- probe run `35494987861`: **success**;
- artifact `p1-levelrenderer-api-probe-ea4fe41eea15ff879ddcebe005f401bf01c0ce23`, ID `10600567053`, digest `sha256:34174f63d123166c1ec0fef37eae606f3d08dbdf2fa0ad0c369421f087582b1d`;
- marker: `LEVELRENDERER_26_2_SPLIT_PROVEN old_renderlevel_owner_absent=true current_render_owner=true game_main_camera=true section_graph_invalidate=true old_lighttexture_absent=true`;
- marker: `LEVELRENDERER_26_2_SCRATCH_MIXIN_COMPILES`;
- exact current `LevelRenderer.render(...)` descriptor is `(GraphicsResourceAllocator, DeltaTracker, boolean, CameraRenderState, Matrix4fc, GpuBufferSlice, Vector4f, boolean)`;
- exact `LevelRenderer` still owns final `GameRenderer gameRenderer` and final `SectionOcclusionGraph sectionOcclusionGraph`;
- exact `GameRenderer.mainCamera()` exists and returns the same vanilla `Camera` instance; no replacement camera is created;
- exact `SectionOcclusionGraph.invalidate()` remains public/current.

The same exact inspection proved the block-damage distance behavior moved out of `LevelRenderer`: current `LevelRenderer` consumes `LevelRenderState.blockBreakingRenderStates`, while the distance filter is built earlier in `LevelExtractor`.

Relocated block-damage proof commit `8c19b74c5b69f1ab28a241b55672840af2824bd0`:

- P0 run `35495140714`: **success**;
- exact LevelExtractor probe run `35495140731`: **success**;
- artifact `p1-level-extractor-blockdamage-probe-8c19b74c5b69f1ab28a241b55672840af2824bd0`, ID `10599724029`, digest `sha256:4a33fb1f6caba9c01460e9eae24758fad4e8c70735758fa5307d6bee9681f2fd`;
- exact current owner is private `LevelExtractor.extractBlockDestroyAnimation(Camera, LevelRenderState)`;
- exact bytecode gets `Camera.position()`, iterates `ClientLevel.destructionProgress()`, computes `BlockPos.distToCenterSqr(...)`, compares against exactly one `double 1024.0d`, and then emits `BlockBreakingRenderState` into `LevelRenderState.blockBreakingRenderStates`;
- scratch `@Mixin(LevelExtractor.class)` + MixinExtras `@ModifyExpressionValue` on that exact 1024 constant compiled against the resolved 26.2 classpath.

### Minimal bridge installed

- helper creation: `66f09e12fb612cc9cbd680982fd5202a97e58157` — `scripts/apply_p1_levelrenderer_split_26_2.py`;
- canonical wiring/proof implementation: `660d5320902a3ecba4f3219969aa77b0316cfa52`;
- old client `MixinLevelRenderer` remains targeted at `LevelRenderer`, but its active callback moves from removed `renderLevel(...)` to exact current `render(...)`;
- it reads `gameRenderer.mainCamera()` and then uses the existing upstream `((IVSCamera) camera).getShipMountedRenderTransform()` path unchanged; it does not create, reposition, rotate, force, or counter-rotate a camera;
- upstream transform comparison threshold and vanilla `sectionOcclusionGraph.invalidate()` authority remain unchanged;
- the stale block-damage constant hook is removed only from its obsolete owner and recreated as `MixinLevelExtractor`, targeting the exact relocated `1024.0d` filter with the same `Double.MAX_VALUE` behavior;
- `valkyrienskies-common.mixins.json` registers exactly one new `client.renderer.MixinLevelExtractor` entry;
- no gameplay, ship lifecycle, physics, movement, collision, entity dragging, networking, or reference-space authority is added or replaced.

This is compile/API proof for this semantic unit, not a claim that every other renderer/camera mixin is runtime-valid. In particular, future P1 runtime/mixin application may expose separate drift in other upstream renderer mixins; do not broaden this frozen bridge to hide such failures.

Transport note: canonical P1 invokes this dedicated helper from the already-used ship-debug-overlay transport dispatcher after the frozen pathfinding helper. Repo diff from probe-head `8c19b74...` to implementation `660d532...` contains only the new helper and eight transport lines. Exact ship-debug proof `35495275080` stayed green. Any future transport cleanup must preserve all semantic outputs exactly.

Do not reopen this LevelRenderer/LevelExtractor boundary absent direct contradictory compile/runtime evidence.

## Pathfinding debug lifecycle bridge — frozen green

Pinned upstream target: `common/src/main/java/org/valkyrienskies/mod/mixin/feature/render_pathfinding/MixinDebugRenderer.java`.

- canonical implementation: `f56fa6d76d31661e561de85b7223b6de64e39de9`;
- exact lifecycle/scratch probe commit `63c6c314719d3f75456d50332268f67ca243f9b1`, P0 `35494083783`, probe `35494083822`, artifact `10600376722`, digest `sha256:dc8aada751ed3f75050029951cd0f2bf0f3551ebcbcf4af485219777456032ab`;
- exact 26.2 migrated from direct `PathfindingRenderer.render(PoseStack, BufferSource, ...)` to vanilla `SimpleDebugRenderer` / `DebugValueAccess` / gizmo dispatch;
- bridge controls only renderer-list membership, keeps at most one VS-owned pathfinding renderer, never removes vanilla-owned membership, and never directly owns `DebugValueAccess`, Frustum, or gizmo rendering;
- canonical compile reduced the frontier 57/6 -> 51/5 and exact pathfinding source remains absent at current implementation `660d532...`.

Do not reopen this boundary absent direct contradictory evidence.

## Recent mechanical Java convergence — preserved

Already-landed API/mapping bridges that must not be repeated blindly include:

- `28ee0eabe77778dd2f9bbd84e528d9c3a6718531`: client sound `ResourceLocation` -> `Identifier`.
- `4aa395c810476d78c2f8cfb1bee423d2f5248616`: `BlockUtil` package relocation.
- `880df3aa1ecbdaf2a5b9974d65dd68a266fbc764`: `DimensionDataStorage` -> `SavedDataStorage` in `MixinChunkMap`.
- `82887915b04b1546129ab0dba610d4ba0ed7e075`: `applyCarvers` signature adaptation.
- `9b229bbadfc3bab5ed918556144ad566ca37e448`: LevelChunk `ChunkSerializer` -> `SerializableChunkData` vocabulary bridge.
- `6faec034d400458d4471e8aa608c77ecb01119e9`: ChunkMap shutdown-work dispatcher bridge.
- `480ca1e32024db619574b28488ad8a1c88045d52`: alpha-HUD `Gui`/`GuiGraphics` -> `Hud`/`GuiGraphicsExtractor` lifecycle bridge; exact API probe `39d20e58f40fec26bb4face0823255789f560747`, run `35492969240`, artifact `10599492174`.
- `f56fa6d76d31661e561de85b7223b6de64e39de9`: pathfinding debug membership/gizmo lifecycle bridge.
- `660d5320902a3ecba4f3219969aa77b0316cfa52`: LevelRenderer / LevelExtractor split bridge described above.

These are compatibility adaptations only and authorize no replacement VS2 architecture.

## Frozen architecture-sensitive boundaries

All prior frozen-green proof records in Git history remain binding. Key locks include:

- **Real VS2 ship chunk-ticket lifecycle** — implementation `65a42e782de192f27d5bf720691d6e08f395a719`; proof `35450402031`. Explicit load-only radius-zero ticket add/remove lifecycle, flush/order, ship-alive removal guard, and deletion cleanup remain authority.
- **DistanceManager / TicketStorage read bridge** — implementation `8a338f95103227ed6a5acb35804d573bbae0d96c`; proof HEAD `ca07a2fff0fd922cbbd578a0531d3377313827de`; P0 `35463018487`; proof `35463018541`. Read-only compatibility only; never expand into replacement ticket lifecycle.
- **ShipSavedData persistence** — implementation `f2b3ec68e0d2146bb8b443da76a62a4766e01fce`; proof `35451366140`. Vanilla saved-data storage remains authority.
- **Entity local authority / interpolation** — implementation `b7e583af13598b6ddcc583380872f578b8a40bb8`; proof HEAD `9f2719be070e79b91b7f47ceddaec61d7f5cff40`; proof `35455551701`. Real dragging information and ship transforms remain intact; no synthetic carry system.
- **Entity renderer submit lifecycle** — implementation `a87512437f40a3bfa1325d78f8e2588587ec7cc8`; proof HEAD `58d8554ba623896d486b91f18771df9bdcd6f2b3`; proof `35458380245`.
- **Shipyard teleport API mapping** — P0 `35467615792`; proof `35467615790`. Real VS2 ship-to-world transform remains authority; no manual packet/setPos/teleport chase.
- NaturalSpawner, particle collision, EntitySectionStorage, WaterFluid, POIManager, AirAndWaterRandomPos, tick-ship-chunks, ship-debug overlay, world-weather, clip-replace, LavaFluid, Explosion, StructureTemplate, LevelChunk, ChunkMapClose, alpha-HUD, pathfinding-debug, and LevelRenderer/LevelExtractor boundaries remain frozen green.
- **Clip-replace Direction vocabulary** — canonical `5d0fd81810a824b2da989b834dd6d2f92475dc33`; P0 `35478903000`; proof `35478902949`.
- **LavaFluid randomTick ServerLevel** — canonical `19b0e356b34dae20c3aa8d9409d90fc0b96838b2`; P0 `35479600636`; proof `35479600673`.
- **Explosion Level client accessor** — canonical `322dcf22e2baf25192682d4b9ee942f4a35dc86b`; P0 `35480514635`; proof `35480514714`.
- **Optional Sable Companion boundary** — compile-only. It does not authorize bundling or claiming a 1.21.1 Sable runtime on 26.2.
- **Optional Create deployer helper isolation** — P1 compile isolation only, never a substitute for P3 Create integration.

## Locked negative evidence

- `3bcbf90c75dc4d02448cfdb4590cc9c9674e0ed6` / run `35454717409`: wrong Kotlin-source-set exclusion for `DeployerScrollOptionSlot.kt`; do not replay.
- `a72aaef8eca34a352ef949eeb57e6bbcda81171f`: `setUnsaved(false)` is invalid current API; do not replay absent direct new evidence.
- VSKeyBindings failed probes `e108526cbd728454c175c76bffc610d4e074da49`, `fcc65187d79c4b546883875da3597345db1e01cd`, `e9a3efd58acb2af9539628eb2875e6cb829c3cec`, `fb3c7e65a4c2089f6fa695114734d14836bde1d3` remain negative evidence.
- pathfinding lifecycle probe `b3927e625acf40edbf517970ebc952a104a20c97` / run `35493933563` failed only because of a too-strict textual `javap` assertion; this is probe-parser negative evidence, not renderer evidence.
- initial LevelRenderer probe `3e824228...` / run `35494738882` failed its obsolete-owner assertion after producing useful exact evidence; do not treat that conclusion as an API failure.
- Actions self-push of workflow changes without `workflows` permission is a locked failed transport hypothesis.
- retired `apm23/VS2-Create_Interactive` workarounds remain historical warning evidence only and are forbidden as implementation source.

## Current remaining Java compile frontier

Exact artifact `10600448490` at implementation HEAD `660d5320902a3ecba4f3219969aa77b0316cfa52` contains **45 `: error:` diagnostics across 4 normalized source files**:

1. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/vanilla_renderer/MixinLevelRendererVanilla.java` — 24 diagnostics.
2. `common/src/main/java/org/valkyrienskies/mod/mixin/feature/render_ship_debug_bb/MixinDebugRenderer.java` — 9 diagnostics.
3. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/sable/MixinSubLevelHoldingChunkMap.java` — 6 diagnostics.
4. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/sable/MixinActiveSableCompanion.java` — 6 diagnostics.

Observed direct missing-symbol surfaces:

- ship-debug bounding-box renderer: `MultiBufferSource`, `RenderType`, and `MultiBufferSource.BufferSource` no longer resolve;
- vanilla renderer compat: `Uniform`, `VertexBuffer`, `LightTexture`, `RenderType`, `ShaderInstance`, plus related signatures no longer resolve;
- Sable: absent optional companion classes/packages.

Classification:

- the two remaining non-Sable units are renderer/debug-sensitive and must not be blind-patched;
- both Sable units are optional compatibility residue and remain compile-only isolation territory, not standalone-P1 runtime authority;
- there is no remaining non-render core Java unit in the observed javac frontier.

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
- active_blocker: `MINECRAFT_26_2_RENDERER_API_MIXIN_DRIFT`
- active_proof_head: `660d5320902a3ecba4f3219969aa77b0316cfa52; canonical P1 chain through frozen LevelRenderer / LevelExtractor split bridge`
- active_proof_run: `P0 35495275084 success; P1 compile 35495275097 frontier-only failure; artifact 10600448490; 45 diagnostics / 4 normalized source files; client LevelRenderer and LevelExtractor absent; frozen ship-debug proof 35495275080 success`
- active_hypothesis: `next work must inspect the smallest remaining real renderer/debug unit against exact resolved Minecraft 26.2 rendering APIs before mutation; no package-name guessing and no batching with vanilla renderer compat or Sable`
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
- Frozen pathfinding bridge may only control membership in vanilla debug-render list; it must not own `DebugValueAccess` or gizmo dispatch.
- Frozen LevelRenderer bridge observes the already-existing `IVSCamera` state and invalidates vanilla occlusion graph only; it must not become camera movement/rotation authority.
- `FINAL_READY` is forbidden from CI alone.
- Video is closure-only and must not be used for ordinary compile/debug hypothesis testing.

## next_safe_action

1. This ledger reconciliation commit is documentation-only. Require exact-head P0 provenance success before another source/workflow mutation.
2. Preserve every frozen boundary and all negative evidence in Git history. Do not repeat landed patches.
3. Use compile artifact `10600448490` as the canonical **45-diagnostic / 4-source-file** frontier until implementation/compiler state changes.
4. Do **not** reopen pathfinding debug or the client LevelRenderer/LevelExtractor split absent direct contradictory evidence.
5. Preferred next inspection unit: pinned upstream `common/src/main/java/org/valkyrienskies/mod/mixin/feature/render_ship_debug_bb/MixinDebugRenderer.java`, the smallest remaining non-Sable renderer unit at 9 diagnostics.
6. Before any source mutation, inspect its exact pinned upstream behavior and the exact Minecraft 26.2 `DebugRenderer` / current debug-render output APIs replacing `MultiBufferSource`, `RenderType`, and `MultiBufferSource.BufferSource`. Treat this as renderer-sensitive; do not infer replacements from names or from the already-frozen pathfinding bridge.
7. If exact resolved bytecode/signatures prove one bounded ship-debug bounding-box adaptation that preserves upstream VS2 ship transform/bounds behavior while delegating current output authority to vanilla 26.2, create one fail-closed overlay and exact proof. Otherwise HOLD that unit.
8. Do not combine this action with `MixinLevelRendererVanilla`, Sable, Create/SNR/Copycats, movement, collision, entity dragging, camera, or physics authority.
9. Remain standalone P1. No ordinary compile/debug video.

## Video and milestone gate

- `M1_COMPLETE` is forbidden until full P2 real-VS2 runtime proof exists: real ship lifecycle, translation+rotation, ship-space, collision, standing/walking, jump-airborne-natural landing, floor/walls/ceiling, stable free camera/look, entity dragging/reference space, rendering, and client/server sync.
- `FINAL_BUILD`, `FINAL_VERIFY`, and `FINAL_READY` are not applicable during P1.
- Video is closure-only. Visible failure overrides telemetry green. `FINAL_READY` still requires exact-final-JAR real-user runtime acceptance.
