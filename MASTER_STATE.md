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

## Current reconciliation — canonical P1 chain through pathfinding debug lifecycle bridge

Current proven implementation boundary before this documentation-only reconciliation commit:

- canonical implementation HEAD: `f56fa6d76d31661e561de85b7223b6de64e39de9` — `ci: wire proven pathfinding debug lifecycle overlay`.
- exact-head P0 provenance run `35494307209`: **success**.
- exact-head standalone P1 compile run `35494307188` (#125): **frontier-only failure**. Every overlay/apply step, port-delta validation, Gradle runtime setup, and diagnostic upload succeeded; only the remaining javac frontier failed.
- compile artifact: `p1-compile-log-f56fa6d76d31661e561de85b7223b6de64e39de9`, ID `10599943032`, artifact digest `sha256:21f39b7b1cbab7d071070df51e724f7b11038329c4d8aac206fc87135bb6a8b4`.
- extracted `p1-compile.log`: 189020 bytes, SHA-256 `6cfabb025ca4056e0da29d33dc02f5c6e6c3f80e9ccaf9bef85f6b40620db1e2`.
- exact compile log contains **51 `: error:` diagnostics across 5 normalized source files**.
- `common/src/main/java/org/valkyrienskies/mod/mixin/feature/render_pathfinding/MixinDebugRenderer.java` has **zero mentions** in the exact compile log.
- immediately prior canonical implementation `480ca1e32024db619574b28488ad8a1c88045d52` had artifact `10600285721` with **57 diagnostics across 6 files**. Therefore the pathfinding lifecycle bridge removed exactly that source unit from the observed frontier without reopening any previously frozen compile unit.
- frozen ship-debug-overlay proof reran at this exact implementation HEAD as run `35494307216`: **success**, including isolated semantic validation and exact-file compiler-clean proof. The transport chaining used to invoke the pathfinding helper therefore did not reopen the frozen ship-debug-overlay source boundary.

## Pathfinding debug lifecycle bridge — frozen green

Pinned upstream target:
`common/src/main/java/org/valkyrienskies/mod/mixin/feature/render_pathfinding/MixinDebugRenderer.java`.

### Upstream behavior and 26.2 migration

Pinned upstream 1.21.1 behavior:

- targets `DebugRenderer`;
- shadows a dedicated `PathfindingRenderer pathfindingRenderer` field;
- injects at old `DebugRenderer.render(...)` HEAD;
- while `VSGameConfig.COMMON.ADVANCED.getRenderPathfinding()` is true, directly invokes the old `PathfindingRenderer.render(PoseStack, BufferSource, camX, camY, camZ)` path.

Exact Minecraft 26.2 API inspection proved that this is not a type rename:

- `DebugRenderer.pathfindingRenderer` no longer exists;
- `DebugRenderer.render(...)` no longer exists;
- current owner has `List<DebugRenderer.SimpleDebugRenderer> renderers` backed by a mutable `ArrayList`;
- current entry point is `emitGizmos(Frustum,double,double,double,float)`;
- `emitGizmos(...)` obtains `DebugValueAccess`, conditionally refreshes the renderer list, then performs one list iteration and dispatches `SimpleDebugRenderer.emitGizmos(...)`;
- `PathfindingRenderer` has a public constructor, implements public `DebugRenderer.SimpleDebugRenderer`, consumes `DebugValueAccess` / `DebugSubscriptions.ENTITY_PATHS`, and emits current gizmos rather than using old `PoseStack` / `MultiBufferSource` rendering;
- vanilla `refreshRendererList()` adds its own `PathfindingRenderer` only under `SharedConstants.DEBUG_PATHFINDING`.

Initial architecture probe `60d2669345667436f4be4986bff0f6d8d2271b63`, P0 `35493559167`, run `35493559177`, artifact `10600326144`, digest `sha256:5ebc5d2985270d212967f906fd771e7a54e37e8526b091056ec1209a6ef40710`, established the list/gizmo migration and intentionally failed a stale-field assertion. It authorized inspection only, not a patch.

Lifecycle proof commit `63c6c314719d3f75456d50332268f67ca243f9b1`:

- P0 run `35494083783`: **success**;
- exact lifecycle/scratch probe run `35494083822`: **success**;
- artifact `p1-pathfinding-debug-api-probe-63c6c314719d3f75456d50332268f67ca243f9b1`, ID `10600376722`, digest `sha256:dc8aada751ed3f75050029951cd0f2bf0f3551ebcbcf4af485219777456032ab`;
- marker: `PATHFINDING_DEBUG_26_2_LIFECYCLE_PROVEN list_owner=true mutable_arraylist=true simple_interface_public=true path_ctor_public=true refresh_before_iterator=true iterator_unique=true vanilla_dispatch=true membership_only_candidate=true`;
- marker: `PATHFINDING_DEBUG_26_2_SCRATCH_MIXIN_COMPILES`;
- the probe checked all four vanilla-pathfinding-present / VS-config-on combinations and proved the candidate membership rule never creates more than one pathfinding renderer and never removes a vanilla-owned renderer.

One earlier lifecycle probe `b3927e625acf40edbf517970ebc952a104a20c97` / run `35493933563` failed only because the probe expected the textual `javap` phrase `public abstract interface`; exact output used `public interface`. This was a probe-parser error, not renderer negative evidence; commit `63c6c...` changed only that assertion before the successful proof above.

### Minimal bridge installed

- helper overlay creation: `a2364658f33da328a4d019d8b260ce2e51c23bab` — `scripts/apply_p1_pathfinding_debug_lifecycle_26_2.py`;
- canonical wiring/proof implementation: `f56fa6d76d31661e561de85b7223b6de64e39de9`;
- the helper is fail-closed against the exact pinned upstream pathfinding mixin;
- it shadows the current vanilla `renderers` list and keeps at most one VS-owned `PathfindingRenderer` instance;
- injection occurs immediately before the unique `List.iterator()` invocation in `DebugRenderer.emitGizmos`, which exact bytecode proves occurs after any vanilla refresh;
- VS config ON: if vanilla already supplied any `PathfindingRenderer`, nothing is added; otherwise the one VS-owned renderer is lazily added;
- VS config OFF: only the VS-owned renderer is removed; vanilla-owned debug renderer membership is never removed;
- the mixin never directly calls `PathfindingRenderer.emitGizmos`, never creates `DebugValueAccess`, and never renders gizmos itself. Vanilla 26.2 owns current debug-data access, Frustum flow, dispatch, and gizmo output;
- no ship lifecycle, transform, movement, collision, entity dragging, player, camera, networking, physics, or reference-space authority is introduced.

Transport note: canonical P1 currently invokes the dedicated helper after the already-frozen ship-debug-overlay center script. That chaining is transport-only; exact run `35494307216` proves the frozen ship-debug-overlay semantic source remains compiler-clean. Do not alter either helper casually; any future transport cleanup must preserve both source outputs exactly.

Do not reopen this pathfinding boundary absent direct contradictory compile/runtime evidence.

## Recent mechanical Java convergence — preserved

Already-landed API/mapping bridges that must not be repeated blindly include:

- `28ee0eabe77778dd2f9bbd84e528d9c3a6718531`: client sound `ResourceLocation` -> `Identifier`.
- `4aa395c810476d78c2f8cfb1bee423d2f5248616`: `BlockUtil` package relocation.
- `880df3aa1ecbdaf2a5b9974d65dd68a266fbc764`: `DimensionDataStorage` -> `SavedDataStorage` in `MixinChunkMap`.
- `82887915b04b1546129ab0dba610d4ba0ed7e075`: `applyCarvers` signature adaptation.
- `9b229bbadfc3bab5ed918556144ad566ca37e448`: LevelChunk `ChunkSerializer` -> `SerializableChunkData` vocabulary bridge.
- `6faec034d400458d4471e8aa608c77ecb01119e9`: ChunkMap shutdown-work dispatcher bridge.
- `480ca1e32024db619574b28488ad8a1c88045d52`: alpha-HUD `Gui`/`GuiGraphics` -> `Hud`/`GuiGraphicsExtractor` lifecycle bridge; exact API probe `39d20e58f40fec26bb4face0823255789f560747`, run `35492969240`, artifact `10599492174`.
- `f56fa6d76d31661e561de85b7223b6de64e39de9`: pathfinding debug membership/gizmo lifecycle bridge described above.

These are API/mapping adaptations only and authorize no replacement VS2 architecture.

## Frozen architecture-sensitive boundaries

All prior frozen-green proof records in Git history remain binding. Key locks include:

- **Real VS2 ship chunk-ticket lifecycle** — implementation `65a42e782de192f27d5bf720691d6e08f395a719`; proof `35450402031`. Load-only radius-zero explicit ticket add/remove lifecycle, flush/order, ship-alive removal guard, and deletion cleanup remain authority.
- **DistanceManager / TicketStorage read bridge** — implementation `8a338f95103227ed6a5acb35804d573bbae0d96c`; proof HEAD `ca07a2fff0fd922cbbd578a0531d3377313827de`; P0 `35463018487`; proof `35463018541`. Read-only compatibility only; never expand into replacement ticket lifecycle.
- **ShipSavedData persistence** — implementation `f2b3ec68e0d2146bb8b443da76a62a4766e01fce`; proof `35451366140`. Vanilla saved-data storage remains authority.
- **Entity local authority / interpolation** — implementation `b7e583af13598b6ddcc583380872f578b8a40bb8`; proof HEAD `9f2719be070e79b91b7f47ceddaec61d7f5cff40`; proof `35455551701`. Real dragging information, ship transforms, and interpolation authority remain intact; no synthetic carry system.
- **Entity renderer submit lifecycle** — implementation `a87512437f40a3bfa1325d78f8e2588587ec7cc8`; proof HEAD `58d8554ba623896d486b91f18771df9bdcd6f2b3`; proof `35458380245`. Real VS2 render authorities remain authoritative.
- **Shipyard teleport API mapping** — P0 `35467615792`; proof `35467615790`. Real VS2 ship-to-world transform remains authority; no manual packet/setPos/teleport chase.
- NaturalSpawner, particle collision, EntitySectionStorage, WaterFluid, POIManager, AirAndWaterRandomPos, tick-ship-chunks, ship-debug overlay, world-weather, clip-replace, LavaFluid, Explosion, StructureTemplate, LevelChunk, ChunkMapClose, alpha-HUD, and pathfinding-debug lifecycle boundaries remain frozen green.
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

Exact-head artifact `10599943032` at implementation HEAD `f56fa6d76d31661e561de85b7223b6de64e39de9` contains **51 `: error:` diagnostics across 5 normalized source files**:

1. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/vanilla_renderer/MixinLevelRendererVanilla.java` — 24 diagnostics.
2. `common/src/main/java/org/valkyrienskies/mod/mixin/feature/render_ship_debug_bb/MixinDebugRenderer.java` — 9 diagnostics.
3. `common/src/main/java/org/valkyrienskies/mod/mixin/client/renderer/MixinLevelRenderer.java` — 6 diagnostics.
4. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/sable/MixinSubLevelHoldingChunkMap.java` — 6 diagnostics.
5. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/sable/MixinActiveSableCompanion.java` — 6 diagnostics.

Observed direct missing-symbol surfaces from the exact artifact:

- ship-debug bounding-box renderer: `MultiBufferSource`, `RenderType`, and `MultiBufferSource.BufferSource` no longer resolve;
- client `MixinLevelRenderer`: `net.minecraft.client.renderer.LightTexture` no longer resolves, including its render callback parameter; callback signature is renderer-sensitive;
- vanilla renderer compat: `Uniform`, `VertexBuffer`, `LightTexture`, `RenderType`, `ShaderInstance`, plus related signatures no longer resolve;
- Sable: absent optional companion classes/packages.

Classification:

- all three non-Sable units are rendering/debug/camera-adjacent and must not be blind-patched;
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
- active_blocker: `MINECRAFT_26_2_RENDERER_API_MIXIN_DRIFT`
- active_proof_head: `f56fa6d76d31661e561de85b7223b6de64e39de9; canonical P1 chain through frozen pathfinding debug lifecycle bridge`
- active_proof_run: `P0 35494307209 success; P1 compile 35494307188 frontier-only failure; artifact 10599943032; 51 diagnostics / 5 normalized source files; pathfinding mixin absent; frozen ship-debug proof 35494307216 success`
- active_hypothesis: `next work must inspect one smallest remaining renderer boundary against the exact resolved Minecraft 26.2 API before mutation; do not guess replacement names and do not batch renderer families`
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
- Frozen pathfinding debug bridge may only control membership in vanilla's current debug-render list; it must not take ownership of `DebugValueAccess`, gizmo dispatch, or direct rendering.
- `FINAL_READY` is forbidden from CI alone.
- Video is closure-only and must not be used for ordinary compile/debug hypothesis testing.

## next_safe_action

1. This ledger reconciliation commit is documentation-only. Require exact-head P0 provenance success before another source/workflow mutation.
2. Preserve every frozen boundary and all negative evidence in Git history. Do not repeat landed patches.
3. Use compile artifact `10599943032` as the canonical **51-diagnostic / 5-source-file** frontier until implementation/compiler state changes.
4. Do **not** reopen `feature/render_pathfinding/MixinDebugRenderer.java`; it is frozen green at implementation `f56fa6d76d31661e561de85b7223b6de64e39de9`.
5. Preferred next inspection unit: pinned upstream `common/src/main/java/org/valkyrienskies/mod/mixin/client/renderer/MixinLevelRenderer.java`, because its current observed direct compile drift is only the removed `net.minecraft.client.renderer.LightTexture` type/import repeated across compile tasks.
6. Before any mutation, inspect the exact Minecraft 26.2 `LevelRenderer` callback/method targeted by that mixin and identify the exact current type/lifecycle replacing the old `LightTexture` parameter. Treat this as renderer-sensitive: do not infer a rename from mappings or neighboring classes.
7. If exact resolved 26.2 bytecode/signatures prove one bounded callback/type bridge with unchanged upstream VS2 behavior, create one fail-closed overlay and exact-file compile proof. Otherwise HOLD that unit and do not broaden the action.
8. Do not combine this unit with `render_ship_debug_bb`, vanilla renderer compat, Sable, Create/SNR/Copycats, movement, collision, entity dragging, or camera authority.
9. Remain standalone P1. No ordinary compile/debug video.

## Video and milestone gate

- `M1_COMPLETE` is forbidden until full P2 real-VS2 runtime proof exists: real ship lifecycle, translation+rotation, ship-space, collision, standing/walking, jump-airborne-natural landing, floor/walls/ceiling, stable free camera/look, entity dragging/reference space, rendering, and client/server sync.
- `FINAL_BUILD`, `FINAL_VERIFY`, and `FINAL_READY` are not applicable during P1.
- Video is closure-only. Visible failure overrides telemetry green. `FINAL_READY` still requires exact-final-JAR real-user runtime acceptance.
