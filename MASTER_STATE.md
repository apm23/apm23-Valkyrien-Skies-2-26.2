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

## Current reconciliation — ship debug bounding-box gizmo bridge

Current proven implementation boundary before this documentation-only reconciliation commit:

- canonical implementation HEAD: `a17dd669717354bfdfcb6c05146836aacc62be8f` — `fix: port ship debug bounds to 26.2 gizmos`.
- exact-head P0 provenance run `35496345836`: **success**.
- exact-head standalone P1 compile run `35496345873`: **frontier-only failure**. Every canonical overlay/apply step, port-delta validation, Gradle runtime setup, and diagnostic upload succeeded; only the remaining javac frontier failed.
- compile artifact: `p1-compile-log-a17dd669717354bfdfcb6c05146836aacc62be8f`, ID `10600870487`, artifact digest `sha256:8ec8d8279533684cbbafd82293509f84091759c8e16084373eae9089786fa0d2`.
- extracted `p1-compile.log`: 183024 bytes, SHA-256 `353a17f6315e4bf1bfa1a31110f943c03ea3dbcfefea48fbda79303b4ee0e919`.
- using the same durable ledger metric as prior states, the exact compile log contains **36 `: error:` markers across 3 normalized source files**; the primary javac pass itself reports **12 errors**. The factor-of-three marker repetition comes from Gradle exception/report replay and must not be confused with 36 distinct javac errors.
- `common/src/main/java/org/valkyrienskies/mod/mixin/feature/render_ship_debug_bb/MixinDebugRenderer.java` has **zero `: error:` mentions** in the exact compile log.
- immediately prior canonical implementation `660d5320902a3ecba4f3219969aa77b0316cfa52` had artifact `10600448490` with **45 `: error:` markers across 4 normalized source files**. Therefore this bounded ship-debug bridge removed exactly the old 9-marker / one-source-file unit without creating a new compile unit.
- frozen client `MixinLevelRenderer` / `MixinLevelExtractor`, pathfinding debug, and ship-debug-overlay boundaries remain closed; this implementation did not reopen their source authority.

## Ship debug bounding-box 26.2 gizmo bridge — frozen P1 compile/API green

Pinned upstream target:
`common/src/main/java/org/valkyrienskies/mod/mixin/feature/render_ship_debug_bb/MixinDebugRenderer.java`.

Pinned upstream behavior:

- render only when vanilla entity hitboxes are enabled;
- draw ship center-of-mass bounds in world space;
- draw the ship voxel AABB through the ship render transform, preserving ship rotation;
- draw the ship render AABB in world space;
- do not own physics, movement, collision, camera, ship lifecycle, or reference-space authority.

Exact 26.2 inspection history:

- `73a8a8d0568042c80c008cc0e0e355e8a9f42a39` — initial ship-debug gizmo API inspection;
- `5aa12dd065861180e54533e04f4ab47a65caba39` — exact gizmo package follow-up;
- exact probe run `35495680174`: **success**;
- probe artifact `p1-ship-debug-bb-api-probe-5aa12dd065861180e54533e04f4ab47a65caba39`, ID `10600194493`, digest `sha256:5f82165eeb7c20c71c8abe27c32ad5a26eca2a66e9c26bad57737f725cfa5757`;
- exact evidence proved Minecraft 26.2 uses `DebugRenderer.emitGizmos(...)` plus `Gizmos`/`GizmoStyle`; vanilla debug renderers already emit through that lifecycle;
- current API provides `Gizmos.cuboid(AABB, GizmoStyle)`, `Gizmos.line(Vec3, Vec3, int, float)`, and `GizmoStyle.stroke(int)` while the old direct `MultiBufferSource` / `RenderType.lines()` path is obsolete for this unit.

Minimal bridge installed at `a17dd669717354bfdfcb6c05146836aacc62be8f`:

- fail-closed helper: `scripts/apply_p1_ship_debug_bb_gizmo_26_2.py`;
- helper is pinned to the exact upstream source blob and rejects missing upstream semantic anchors;
- callback moves from obsolete `DebugRenderer.render(...)` to exact current `DebugRenderer.emitGizmos(...)` TAIL;
- center-of-mass and render AABBs delegate to vanilla `Gizmos.cuboid`;
- ship voxel AABB remains orientation-preserving: its eight ship-space corners are transformed by the original `ShipTransform.getShipToWorld().transformPosition(...)`, then its twelve world-space edges are emitted with vanilla `Gizmos.line`;
- original loaded-ship iteration and vanilla hitbox gate are preserved;
- obsolete direct-buffer authority (`MultiBufferSource`, `RenderType`, `LevelRenderer.renderLineBox`, direct batch end) is forbidden by the helper after rewrite;
- canonical transport only chains this helper after the already-frozen pathfinding and LevelRenderer-split helpers.

P1 proof at `a17dd669...`: P0 `35496345836` success and P1 compile artifact `10600870487` removes the entire ship-debug compile unit. This freezes the bridge at **P1 compile/API level only**; runtime rendering still belongs to later P1/P2 boot/runtime proof and must not be inferred from compile success.

Do not reopen this boundary absent direct contradictory compile/runtime evidence.

## LevelRenderer / LevelExtractor 26.2 split bridge — frozen green

Pinned upstream semantic unit:
`common/src/main/java/org/valkyrienskies/mod/mixin/client/renderer/MixinLevelRenderer.java`.

- canonical implementation: `660d5320902a3ecba4f3219969aa77b0316cfa52`;
- initial exact API inspection `3e824228a912d9af4e8af5e4bdab29cf2ed11944`, P0 `35494738858`, probe `35494738882`; that probe failed only its deliberately obsolete-owner assertion after proving the current split and remains negative probe-parser evidence, not renderer evidence;
- successful split-lifecycle probe `ea4fe41eea15ff879ddcebe005f401bf01c0ce23`, P0 `35494987862`, probe `35494987861`, artifact `10600567053`, digest `sha256:34174f63d123166c1ec0fef37eae606f3d08dbdf2fa0ad0c369421f087582b1d`;
- exact relocated block-damage proof `8c19b74c5b69f1ab28a241b55672840af2824bd0`, P0 `35495140714`, probe `35495140731`, artifact `10599724029`, digest `sha256:4a33fb1f6caba9c01460e9eae24758fad4e8c70735758fa5307d6bee9681f2fd`;
- upstream camera behavior remains observation-only: use the existing `IVSCamera` transform and invalidate vanilla `SectionOcclusionGraph` when required; no replacement camera authority is introduced;
- old block-damage distance hook is relocated to exact current `LevelExtractor.extractBlockDestroyAnimation(...)` authority with the same upstream `Double.MAX_VALUE` behavior;
- exact current compile remains free of the frozen client `MixinLevelRenderer` and `MixinLevelExtractor` units.

Do not reopen this boundary absent direct contradictory evidence.

## Pathfinding debug lifecycle bridge — frozen green

Pinned upstream target:
`common/src/main/java/org/valkyrienskies/mod/mixin/feature/render_pathfinding/MixinDebugRenderer.java`.

- canonical implementation: `f56fa6d76d31661e561de85b7223b6de64e39de9`;
- exact lifecycle/scratch probe `63c6c314719d3f75456d50332268f67ca243f9b1`, P0 `35494083783`, probe `35494083822`, artifact `10600376722`, digest `sha256:dc8aada751ed3f75050029951cd0f2bf0f3551ebcbcf4af485219777456032ab`;
- exact 26.2 migrated from direct pathfinding render calls to vanilla `SimpleDebugRenderer` / `DebugValueAccess` / gizmo dispatch;
- bridge controls only renderer-list membership, keeps at most one VS-owned pathfinding renderer, never removes vanilla-owned membership, and never owns `DebugValueAccess`, Frustum, or gizmo rendering;
- exact current compile remains free of this unit.

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
- `660d5320902a3ecba4f3219969aa77b0316cfa52`: LevelRenderer / LevelExtractor split bridge.
- `a17dd669717354bfdfcb6c05146836aacc62be8f`: ship-debug bounding-box gizmo bridge.

These are compatibility adaptations only and authorize no replacement VS2 architecture.

## Frozen architecture-sensitive boundaries

All prior frozen-green proof records in Git history remain binding. Key locks include:

- **Real VS2 ship chunk-ticket lifecycle** — implementation `65a42e782de192f27d5bf720691d6e08f395a719`; proof `35450402031`. Explicit load-only radius-zero ticket add/remove lifecycle, flush/order, ship-alive removal guard, and deletion cleanup remain authority.
- **DistanceManager / TicketStorage read bridge** — implementation `8a338f95103227ed6a5acb35804d573bbae0d96c`; proof HEAD `ca07a2fff0fd922cbbd578a0531d3377313827de`; P0 `35463018487`; proof `35463018541`. Read-only compatibility only; never expand into replacement ticket lifecycle.
- **ShipSavedData persistence** — implementation `f2b3ec68e0d2146bb8b443da76a62a4766e01fce`; proof `35451366140`. Vanilla saved-data storage remains authority.
- **Entity local authority / interpolation** — implementation `b7e583af13598b6ddcc583380872f578b8a40bb8`; proof HEAD `9f2719be070e79b91b7f47ceddaec61d7f5cff40`; proof `35455551701`. Real dragging information and ship transforms remain intact; no synthetic carry system.
- **Entity renderer submit lifecycle** — implementation `a87512437f40a3bfa1325d78f8e2588587ec7cc8`; proof HEAD `58d8554ba623896d486b91f18771df9bdcd6f2b3`; proof `35458380245`.
- **Shipyard teleport API mapping** — P0 `35467615792`; proof `35467615790`. Real VS2 ship-to-world transform remains authority; no manual packet/setPos/teleport chase.
- NaturalSpawner, particle collision, EntitySectionStorage, WaterFluid, POIManager, AirAndWaterRandomPos, tick-ship-chunks, ship-debug overlay, world-weather, clip-replace, LavaFluid, Explosion, StructureTemplate, LevelChunk, ChunkMapClose, alpha-HUD, pathfinding-debug, client LevelRenderer/LevelExtractor, and ship-debug bounding-box boundaries remain frozen at their proven scope.
- **Clip-replace Direction vocabulary** — canonical `5d0fd81810a824b2da989b834dd6d2f92475dc33`; P0 `35478903000`; proof `35478902949`.
- **LavaFluid randomTick ServerLevel** — canonical `19b0e356b34dae20c3aa8d9409d90fc0b96838b2`; P0 `35479600636`; proof `35479600673`.
- **Explosion Level client accessor** — canonical `322dcf22e2baf25192682d4b9ee942f4a35dc86b`; P0 `35480514635`; proof `35480514714`.
- **Optional Sable Companion boundary** — compile-only. It does not authorize bundling or claiming a 1.21.1 Sable runtime on 26.2.
- **Optional Create deployer helper isolation** — P1 compile isolation only, never a substitute for P3 Create integration.

## Locked negative evidence

- `3bcbf90c75dc4d02448cfdb4590cc9c9674e0ed6` / run `35454717409`: wrong Kotlin-source-set exclusion for `DeployerScrollOptionSlot.kt`; do not replay.
- `a72aaef8eca34a352ef949eeb57e6bbcda81171f`: `setUnsaved(false)` is invalid current API; do not replay absent direct new evidence.
- VSKeyBindings failed probes `e108526cbd728454c175c76bffc610d4e074da49`, `fcc65187d79c4b546883875da3597345db1e01cd`, `e9a3efd58acb2af9539628eb2875e6cb829c3cec`, `fb3c7e65a4c2089f6fa695114734d14836bde1d3` remain negative evidence.
- pathfinding lifecycle probe `b3927e625acf40edbf517970ebc952a104a20c97` / run `35493933563` failed only because of a too-strict textual `javap` assertion; do not replay that parser assumption.
- initial LevelRenderer probe `3e824228...` / run `35494738882` failed its obsolete-owner assertion after producing useful exact evidence; do not treat that conclusion as an API failure.
- Actions self-push of workflow changes without `workflows` permission is a locked failed transport hypothesis.
- retired `apm23/VS2-Create_Interactive` workarounds remain historical warning evidence only and are forbidden as implementation source.

## Current remaining Java compile frontier

Exact artifact `10600870487` at implementation HEAD `a17dd669717354bfdfcb6c05146836aacc62be8f` contains **36 `: error:` markers across 3 normalized source files**; the primary javac pass reports **12 actual errors**:

1. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/vanilla_renderer/MixinLevelRendererVanilla.java` — 24 repeated markers / 8 primary javac errors.
2. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/sable/MixinSubLevelHoldingChunkMap.java` — 6 repeated markers / 2 primary javac errors.
3. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/sable/MixinActiveSableCompanion.java` — 6 repeated markers / 2 primary javac errors.

Observed direct missing-symbol surfaces:

- vanilla renderer compat: obsolete/unresolved `Uniform`, `VertexBuffer`, `LightTexture`, `RenderType`, `ShaderInstance`, plus related method signatures;
- Sable: absent optional companion classes/packages (`SubLevelHoldingChunkMap`, `ActiveSableCompanion`).

Classification:

- `MixinLevelRendererVanilla.java` is now the only remaining non-Sable Java compile unit and is renderer-sensitive; it must not be blind-patched by package-name guessing;
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
- active_blocker: `MINECRAFT_26_2_VANILLA_RENDERER_COMPAT_API_DRIFT`
- active_proof_head: `a17dd669717354bfdfcb6c05146836aacc62be8f; canonical P1 chain through frozen ship-debug bounding-box gizmo bridge`
- active_proof_run: `P0 35496345836 success; P1 compile 35496345873 frontier-only failure; artifact 10600870487; 36 repeated error markers / 3 normalized source files / 12 primary javac errors; ship-debug bounding-box source absent from compile frontier`
- active_hypothesis: `next work must inspect pinned upstream MixinLevelRendererVanilla behavior against exact resolved Minecraft 26.2 renderer/shader/buffer APIs before mutation; no package-name guessing, no renderer architecture replacement, and no batching with Sable or integrations`
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
- Frozen client LevelRenderer bridge observes the already-existing `IVSCamera` state and invalidates vanilla occlusion graph only; it must not become camera movement/rotation authority.
- Frozen ship-debug bounding-box bridge may only adapt upstream debug visualization to vanilla 26.2 gizmo output; it must not become transform, camera, or gameplay authority.
- `FINAL_READY` is forbidden from CI alone.
- Video is closure-only and must not be used for ordinary compile/debug hypothesis testing.

## next_safe_action

1. This ledger reconciliation commit is documentation-only. Require exact-head P0 provenance success before another source/workflow mutation.
2. Preserve every frozen boundary and all negative evidence in Git history. Do not repeat landed patches.
3. Use compile artifact `10600870487` as the canonical **36-marker / 3-source-file / 12-primary-error** frontier until implementation/compiler state changes.
4. Do **not** reopen ship-debug bounding-box, pathfinding debug, or the client LevelRenderer/LevelExtractor split absent direct contradictory evidence.
5. Preferred next inspection unit: pinned upstream `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/vanilla_renderer/MixinLevelRendererVanilla.java`, the only remaining non-Sable compile unit (24 repeated markers / 8 primary javac errors).
6. Before any source mutation, inspect the exact pinned upstream semantics and exact resolved Minecraft 26.2 replacements/owners for `Uniform`, `VertexBuffer`, `LightTexture`, `RenderType`, `ShaderInstance`, and every affected render callback/signature. Treat this as renderer-sensitive; do not infer replacements from names and do not copy the already-frozen client LevelRenderer bridge unless exact current authority proves the same lifecycle.
7. If exact bytecode/signatures prove one bounded vanilla-renderer compatibility adaptation that preserves original VS2 render transforms/visibility semantics while delegating current rendering authority to vanilla 26.2, create exactly one fail-closed overlay and exact compile/API proof. Otherwise HOLD the unit.
8. Do not combine this action with Sable, Create/SNR/Copycats, movement, collision, entity dragging, player/camera authority, networking, ship lifecycle, or physics.
9. Remain standalone P1. No ordinary compile/debug video.

## Video and milestone gate

- `M1_COMPLETE` is forbidden until full P2 real-VS2 runtime proof exists: real ship lifecycle, translation+rotation, ship-space, collision, standing/walking, jump-airborne-natural landing, floor/walls/ceiling, stable free camera/look, entity dragging/reference space, rendering, and client/server sync.
- `FINAL_BUILD`, `FINAL_VERIFY`, and `FINAL_READY` are not applicable during P1.
- Video is closure-only. Visible failure overrides telemetry green. `FINAL_READY` still requires exact-final-JAR real-user runtime acceptance.
