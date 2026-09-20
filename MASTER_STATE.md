# MASTER_STATE — REAL VS2 26.2 PORT

GitHub code is the implementation source of truth. This file is the durable continuity ledger; chat memory is not authoritative. Git history remains binding for all frozen-green and negative-evidence records even when this ledger is compacted.

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

## Current reconciliation — canonical P1 chain through alpha-HUD API boundary

Current proven implementation boundary before this documentation-only reconciliation commit:

- canonical implementation HEAD: `480ca1e32024db619574b28488ad8a1c88045d52` — `ci: adapt VS2 alpha HUD API for 26.2`.
- exact-head P0 provenance run `35493204506`: **success**.
- exact-head standalone P1 compile run `35493204485` (#124): **frontier-only failure**. All overlay/apply steps, port-delta validation, Gradle runtime setup, and diagnostic upload succeeded; only the remaining javac frontier failed.
- compile artifact: `p1-compile-log-480ca1e32024db619574b28488ad8a1c88045d52`, ID `10600285721`, artifact digest `sha256:94b983084696b37599b153bc9fb957998e5a8909b6b2d1427d6e268736a06056`.
- extracted `p1-compile.log`: 191240 bytes, SHA-256 `671d6aca6279258cf5f19026941662f33e924f520cb10f96a2e9302e2804b8c3`.
- exact compile log contains **57 `: error:` diagnostics across 6 normalized source files**.
- `MixinGui.java`, `GuiGraphics`, `GuiGraphicsExtractor`, `renderEffects`, and `extractEffects` have **zero mentions** in the exact-head compile log.
- immediately prior implementation HEAD `6faec034d400458d4471e8aa608c77ecb01119e9` had artifact `10599810712` with **63 diagnostics across 7 normalized source files**. Therefore the bounded alpha-HUD bridge removed exactly `feature/vs2_alpha_hud/MixinGui.java` from the observed frontier without reopening previously frozen units.

## Alpha HUD API bridge — frozen green

Pinned upstream target:
`common/src/main/java/org/valkyrienskies/mod/mixin/feature/vs2_alpha_hud/MixinGui.java`.

Upstream VS2 behavior preserved:

- the existing optional VS2 alpha/debug HUD remains the only behavior of this mixin;
- debug-toggle/config reads, physics/voxel/UDP text, text order, positions, background rectangles, and colors remain unchanged;
- the mixin introduces no ship lifecycle, transform, movement, collision, entity dragging, camera, networking, physics, or reference-space authority.

### Exact Minecraft 26.2 API proof

Probe-only commit: `39d20e58f40fec26bb4face0823255789f560747` — `ci: inspect Minecraft 26.2 HUD extraction API`.

- P0 provenance run `35492969228`: **success**.
- exact API probe run `35492969240`: **success**.
- probe artifact: `p1-gui-hud-api-probe-39d20e58f40fec26bb4face0823255789f560747`, ID `10599492174`, digest `sha256:e0bd8d6c812e96256e8876e9ee8d3ce40168f93f6b021e0bb5e184fd1f0ed1b5`.
- exact mapped 26.2 compile classpath proves obsolete `net.minecraft.client.gui.GuiGraphics` is absent.
- exact `Gui` has neither old `renderEffects` nor current `extractEffects` ownership.
- exact `Hud` contains the `Minecraft minecraft` field used by upstream VS2.
- exact `Hud` contains `extractEffects(GuiGraphicsExtractor, DeltaTracker)` with descriptor `(Lnet/minecraft/client/gui/GuiGraphicsExtractor;Lnet/minecraft/client/DeltaTracker;)V`.
- exact `GuiGraphicsExtractor` exposes `fill(int,int,int,int,int)`.
- exact `GuiGraphicsExtractor` exposes `text(Font,String,int,int,int)`; bytecode delegates to the boolean overload with `shadow=true`, preserving the old five-argument `drawString` presentation behavior.
- probe marker: `GUI_HUD_26_2_API_PROVEN old_gui_graphics_absent=true gui_renderEffects_absent=true hud_extractEffects=true hud_minecraft=true extractor_fill=true`.

### Minimal bridge installed by `480ca1e32024db619574b28488ad8a1c88045d52`

Only the exact proven HUD API surface changed:

- `Gui` import/target -> `Hud`;
- `GuiGraphics` -> `GuiGraphicsExtractor`;
- injection method `renderEffects` -> `extractEffects`;
- handler graphics parameter -> `GuiGraphicsExtractor`;
- five-argument `drawString(...)` -> five-argument `text(...)`.

The exact-head compile artifact proves this source unit absent from the frontier. Do not reopen this boundary absent direct contradictory compile/runtime evidence.

## Recent mechanical Java convergence — preserved

Already-landed API/mapping bridges that must not be repeated blindly include:

- `28ee0eabe77778dd2f9bbd84e528d9c3a6718531`: client sound `ResourceLocation` -> `Identifier`.
- `4aa395c810476d78c2f8cfb1bee423d2f5248616`: `BlockUtil` package relocation.
- `880df3aa1ecbdaf2a5b9974d65dd68a266fbc764`: `DimensionDataStorage` -> `SavedDataStorage` in `MixinChunkMap`.
- `82887915b04b1546129ab0dba610d4ba0ed7e075`: `applyCarvers` signature adaptation.
- `9b229bbadfc3bab5ed918556144ad566ca37e448`: LevelChunk `ChunkSerializer` -> `SerializableChunkData` vocabulary bridge.
- `6faec034d400458d4471e8aa608c77ecb01119e9`: ChunkMap shutdown-work dispatcher bridge.
- `480ca1e32024db619574b28488ad8a1c88045d52`: alpha-HUD owner/graphics/text API bridge described above.

These are API/mapping adaptations only and authorize no replacement VS2 architecture.

## Frozen architecture-sensitive boundaries

All prior frozen-green proof records in Git history remain binding. Key locks include:

- **Real VS2 ship chunk-ticket lifecycle** — implementation `65a42e782de192f27d5bf720691d6e08f395a719`; proof `35450402031`. Load-only radius-zero explicit ticket add/remove lifecycle, flush/order, ship-alive removal guard, and deletion cleanup remain authority.
- **DistanceManager / TicketStorage read bridge** — implementation `8a338f95103227ed6a5acb35804d573bbae0d96c`; proof HEAD `ca07a2fff0fd922cbbd578a0531d3377313827de`; P0 `35463018487`; proof `35463018541`. Read-only compatibility only; never expand into replacement ticket lifecycle.
- **ShipSavedData persistence** — implementation `f2b3ec68e0d2146bb8b443da76a62a4766e01fce`; proof `35451366140`. Vanilla saved-data storage remains authority; codec/type changes are API bridges only.
- **Entity local authority / interpolation** — implementation `b7e583af13598b6ddcc583380872f578b8a40bb8`; proof HEAD `9f2719be070e79b91b7f47ceddaec61d7f5cff40`; proof `35455551701`. Real dragging information, ship transforms, and interpolation authority remain intact; no synthetic carry system.
- **Entity renderer submit lifecycle** — implementation `a87512437f40a3bfa1325d78f8e2588587ec7cc8`; proof HEAD `58d8554ba623896d486b91f18771df9bdcd6f2b3`; proof `35458380245`. Real VS2 render authorities remain authoritative.
- **Shipyard teleport API mapping** — P0 `35467615792`; proof `35467615790`. Real VS2 ship-to-world transform remains authority; no manual packet/setPos/teleport chase.
- NaturalSpawner, particle collision, EntitySectionStorage, WaterFluid, POIManager, AirAndWaterRandomPos, tick-ship-chunks, ship-debug overlay, world-weather, clip-replace, LavaFluid, Explosion, StructureTemplate, LevelChunk, ChunkMapClose, and alpha-HUD canonical proof boundaries remain frozen green.
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

Exact-head artifact `10600285721` at implementation HEAD `480ca1e32024db619574b28488ad8a1c88045d52` contains **57 `: error:` diagnostics across 6 normalized source files**:

1. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/vanilla_renderer/MixinLevelRendererVanilla.java` — 24 diagnostics.
2. `common/src/main/java/org/valkyrienskies/mod/mixin/feature/render_ship_debug_bb/MixinDebugRenderer.java` — 9 diagnostics.
3. `common/src/main/java/org/valkyrienskies/mod/mixin/feature/render_pathfinding/MixinDebugRenderer.java` — 6 diagnostics.
4. `common/src/main/java/org/valkyrienskies/mod/mixin/client/renderer/MixinLevelRenderer.java` — 6 diagnostics.
5. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/sable/MixinSubLevelHoldingChunkMap.java` — 6 diagnostics.
6. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/sable/MixinActiveSableCompanion.java` — 6 diagnostics.

Observed direct missing-symbol surfaces:

- pathfinding debug renderer: `net.minecraft.client.renderer.MultiBufferSource.BufferSource` no longer resolves;
- ship-debug renderer: `MultiBufferSource`, `RenderType`, and `MultiBufferSource.BufferSource` no longer resolve;
- client level renderer: `LightTexture` no longer resolves and its render callback signature is renderer-sensitive;
- vanilla renderer compat: `Uniform`, `VertexBuffer`, `LightTexture`, `RenderType`, `ShaderInstance`, plus related signatures no longer resolve;
- Sable: absent optional companion classes/packages.

Classification:

- all four non-Sable units are rendering/debug/camera-adjacent and must not be blind-patched;
- both Sable units are optional compatibility residue and remain compile-only isolation territory, not standalone-P1 runtime authority;
- there is currently no remaining non-render core Java unit in the observed frontier.

## Pathfinding debug exact API inspection — HOLD

Pinned upstream unit inspected:
`common/src/main/java/org/valkyrienskies/mod/mixin/feature/render_pathfinding/MixinDebugRenderer.java`.

Upstream 1.21.1 behavior at pin `f39132148e717d325933b4ce6e9e9fb13d929390`:

- targets `DebugRenderer`;
- shadows a dedicated `PathfindingRenderer pathfindingRenderer` field;
- injects at `DebugRenderer.render(...)` HEAD;
- when `VSGameConfig.COMMON.ADVANCED.getRenderPathfinding()` is true, directly calls `pathfindingRenderer.render(PoseStack, BufferSource, camX, camY, camZ)`.

Probe history:

- probe-only commit `e1f0472b4a3765b5df3c039123ec8276efe5842f` added only `.github/workflows/p1-pathfinding-debug-api-probe.yml`.
- exact-head P0 run `35493504094`: **success**.
- first probe run `35493504112`: **infrastructure-only failure** before `javap`; canonical overlays replayed successfully, then Gradle could not resolve `architectury-plugin:3.5.170`. This run is not renderer-API evidence.
- one probe-only retry commit `60d2669345667436f4be4986bff0f6d8d2271b63` changed only the inspection workflow and documented the retry.
- retry exact-head P0 run `35493559167`: **success**.
- retry probe run `35493559177`: classpath resolution **success**; exact mapped Minecraft 26.2 jar was inspected. The job conclusion is failure only because its deliberate fail-closed assertion expected the obsolete `DebugRenderer.pathfindingRenderer` field, which exact 26.2 proves no longer exists.
- retry artifact: `p1-pathfinding-debug-api-probe-60d2669345667436f4be4986bff0f6d8d2271b63`, ID `10600326144`, digest `sha256:5ebc5d2985270d212967f906fd771e7a54e37e8526b091056ec1209a6ef40710`.

Exact Minecraft 26.2 evidence from the mapped jar:

- `DebugRenderer` no longer has a dedicated `pathfindingRenderer` field. It owns `List<DebugRenderer.SimpleDebugRenderer> renderers` plus a debug-entry version field.
- `DebugRenderer.render(...)` is gone. Current boundary is `emitGizmos(Frustum,double,double,double,float)` with descriptor `(Lnet/minecraft/client/renderer/culling/Frustum;DDDF)V`.
- `DebugRenderer.emitGizmos(...)` creates `DebugValueAccess` through the current client connection, refreshes the renderer list when debug-entry state changes, then iterates `SimpleDebugRenderer` instances and calls `emitGizmos(double,double,double,DebugValueAccess,Frustum,float)`.
- `refreshRendererList()` creates/adds a `PathfindingRenderer` only under vanilla `SharedConstants.DEBUG_PATHFINDING`; there is no old always-addressable pathfinding-renderer field.
- `PathfindingRenderer` now implements `DebugRenderer.SimpleDebugRenderer`.
- current `PathfindingRenderer.emitGizmos(...)` descriptor is `(DDDLnet/minecraft/util/debug/DebugValueAccess;Lnet/minecraft/client/renderer/culling/Frustum;F)V`.
- current pathfinding debug data comes through `DebugSubscriptions.ENTITY_PATHS` / `DebugValueAccess` and output is emitted through the gizmo system (`Gizmos`, `GizmoStyle`, `TextGizmo`), not `PoseStack` + `MultiBufferSource.BufferSource`.
- exact class inventory contains current gizmo/submit infrastructure such as `LevelRenderer$FinalizedGizmos`, `SubmitNodeCollector`, `SubmitNodeStorage`, and gizmo feature/render classes.
- exact probe markers: `DebugRenderer render=false emitGizmos=true MultiBufferSource=false PoseStack=false DebugValueAccess=true`; `PathfindingRenderer render=false emitGizmos=true MultiBufferSource=false PoseStack=false DebugValueAccess=true`.

Decision for this unit:

- this is **not** a direct `BufferSource` rename or bounded callback-signature drift;
- Minecraft changed the ownership/lifecycle/data-input/render-output model for debug pathfinding;
- blindly changing the old injection to `emitGizmos`, manually creating `DebugValueAccess`, or inventing a second pathfinding renderer could duplicate or bypass vanilla 26.2 debug-render authority;
- therefore no source overlay was applied in this cycle and the canonical compiler frontier remains 57 diagnostics / 6 files.

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
- active_proof_head: `480ca1e32024db619574b28488ad8a1c88045d52; canonical P1 compile implementation remains unchanged through frozen alpha-HUD API boundary`
- active_proof_run: `P0 35493204506 success; P1 compile 35493204485 frontier-only failure; artifact 10600285721; 57 diagnostics / 6 normalized source files; pathfinding exact API probe 35493559177 proves gizmo/list architecture migration but authorizes no source patch`
- active_hypothesis: `pathfinding debug requires a lifecycle-preserving integration into the 26.2 SimpleDebugRenderer/gizmo pipeline, not a vocabulary rename; no mutation is authorized until exact list membership, nested interface accessibility, refresh ordering, duplicate-render avoidance, and per-frame VS config semantics are proven`
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
3. Use compile artifact `10600285721` as the canonical **57-diagnostic / 6-source-file** frontier until implementation/compiler state changes. Probe-only workflow commits do not change that frontier.
4. Keep `feature/render_pathfinding/MixinDebugRenderer.java` on **HOLD** for source mutation: exact 26.2 proves a renderer lifecycle/data-path migration, not a direct vocabulary/signature bridge.
5. If this same unit is inspected further, stay inspection-only and prove the exact `DebugRenderer.SimpleDebugRenderer` accessibility/contract, renderer-list refresh timing, and a way to preserve the upstream per-render VS config toggle without creating duplicate `PathfindingRenderer` instances or bypassing vanilla `DebugValueAccess`/gizmo authority. Do not invent that bridge from inference.
6. If those invariants cannot all be established exactly, keep this unit HOLD. Do not patch around it merely to reduce javac diagnostics.
7. Do not broaden the same action into ship-debug renderer, `MixinLevelRenderer`, vanilla renderer compat, Sable, Create/SNR/Copycats, movement, collision, entity dragging, or camera authority.
8. Remain standalone P1. No ordinary compile/debug video.

## Video and milestone gate

- `M1_COMPLETE` is forbidden until full P2 real-VS2 runtime proof exists: real ship lifecycle, translation+rotation, ship-space, collision, standing/walking, jump-airborne-natural landing, floor/walls/ceiling, stable free camera/look, entity dragging/reference space, rendering, and client/server sync.
- `FINAL_BUILD`, `FINAL_VERIFY`, and `FINAL_READY` are not applicable during P1.
- Video is closure-only. Visible failure overrides telemetry green. `FINAL_READY` still requires exact-final-JAR real-user runtime acceptance.