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

Minecraft 26.2 changes are applied by explicit fail-closed overlays. Every core subsystem remains traceable to upstream VS2 or is documented as a minimal 26.2 bridge.

## Current reconciliation — vanilla renderer 26.2 bridge

Current proven implementation boundary before this documentation-only reconciliation commit:

- canonical implementation HEAD: `290e2bb6c1f6248437e4d189dfb4a01e82a31e33` — `fix: wire 26.2 vanilla renderer bridge`.
- exact-head P0 provenance run `35498340524`: **success**.
- exact-head standalone P1 compile run `35498340530`: **frontier-only failure**. Every canonical overlay/apply step and port-delta validation succeeded; only the remaining optional Sable javac frontier failed, and diagnostic upload succeeded.
- canonical compile artifact: `p1-compile-log-290e2bb6c1f6248437e4d189dfb4a01e82a31e33`, ID `10601028900`, artifact digest `sha256:143585f347569c7b6122db538056953e14cf06f77ad067630825a166f4f6f57b`.
- extracted `p1-compile.log`: **172288 bytes**, SHA-256 `9f3cd25741ba06f10e2746fc958ddf73bee520e5caf5a184ee43246e261eea63`.
- durable marker metric: **12 `: error:` markers across 2 normalized source files**; primary javac pass reports **4 actual errors**. All are the two optional Sable mixins. `MixinLevelRendererVanilla.java` has zero error markers.
- previous canonical `a17dd669717354bfdfcb6c05146836aacc62be8f` had 36 markers / 3 files / 12 primary errors. Therefore the bounded renderer bridge removed exactly the old **24-marker / one-source-file / 8-primary-error** renderer unit without opening a new compile unit.

## Vanilla renderer 26.2 bridge — frozen P1 compile/API green

Pinned upstream target:
`common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/vanilla_renderer/MixinLevelRendererVanilla.java`, exact upstream blob `824e1ac56a99bc6480cc80c32c085d18c2425b09`.

Pinned upstream semantics retained:

- ship-aware compile distance uses `VSGameUtilsKt.squaredDistanceBetweenInclShips`;
- loaded `ClientShip` iteration, `ShipRenderer.VANILLA` filter, active-chunk/air-section checks and transformed ship render-AABB frustum semantics remain upstream VS2 behavior;
- terrain transform remains the upstream `VSClientGameUtils.transformRenderWithShip` authority;
- block-entity transform remains ship-aware using the same upstream transform helper;
- no physics, collision, movement, entity dragging, player movement, camera movement/rotation, ship lifecycle, or reference-space authority is introduced.

Exact Minecraft 26.2 evidence:

- old direct `renderLevel` / `setupRender` / `renderSectionLayer` plus `ShaderInstance`, `Uniform`, `VertexBuffer`, and `LightTexture` terrain route is obsolete;
- current terrain preparation authority is `LevelRenderer.prepareChunkRenders(...)`, `ChunkSectionsToRender`, and `DynamicUniforms.ChunkSectionInfo` while current vanilla retains GPU/draw ownership;
- current block-entity submission still provides the relocatable `PoseStack.translate(blockPos-cameraPos)` semantic in `submitBlockEntities(...)`;
- current frustum state flows through `Camera.extractRenderState` / `CameraRenderState.cullFrustum` and vanilla `LevelExtractor.applyFrustum` / `SectionOcclusionGraph.addSectionsInFrustum`;
- exact shader + CPU uniform evidence proves terrain section coordinates are camera-relative before model-view application, allowing the existing VS2 transform helper to be connected without creating a second render/reference-space authority.

Probe / proof history:

- exact terrain semantics probe `20a99be85e597385b01dd9892b4028ab9020d5fa`, run `35497544023`: **success**; artifact `10601551867`, digest `sha256:963c973bba1b9003e280395327e984d44e482fc0883fdd461aaf94e7870368bc`.
- camera/global-uniform probe `3d6ca4d5bdc5805de1b7c5a3d5ae27cc3a5ea4fe`, run `35497721437`, failed only an over-strict textual assertion; artifact `10601632052`, digest `sha256:117146b78f813612288fcbeb0d13fe6d2bb7cdd47a546f2039cecb60aaf8e59d` contains the bytecode evidence. This is parser/assertion negative evidence, not API failure.
- helper created at `fe9f051c01e7aba3ac4d41997b29f4c59fd77b5b`; fail-closed upstream identity remains exact.
- `bc6e3c7744a0dedc5d77108e8ed31cafec67ac77` / run `35497975815`: helper guard used bare substring `Uniform` and falsely matched valid 26.2 `DynamicUniforms`; no compile evidence. Do not replay broad substring guard.
- `02b783b24692f7224f89558e54502e3e9708f4cb` / run `35498155312`: scratch-proof guard repeated the same bare `Uniform` false positive; no compile evidence. Do not replay.
- corrected scratch proof HEAD `3be7a411b73bc48aa9f34fdb55b84332bae2d00c`, run `35498189907`: **success**; artifact `10600767769`, digest `sha256:96fa794b526d7c175a95d9ea609f2e72ba272e6942b239a0ca70fd25fd1d3e09`; renderer source zero errors and only the two known Sable files remained.
- canonical transport is wired at `290e2bb6c1f6248437e4d189dfb4a01e82a31e33` through the established fail-closed dispatcher; exact canonical compile reproduces the same Sable-only frontier.

This boundary is frozen at **P1 compile/API level only**. Runtime rendering proof belongs to later standalone P1 boot/runtime validation. Do not reopen absent direct contradictory compile/runtime evidence.

## Other frozen renderer/debug boundaries

- **Ship debug bounding-box gizmo** — canonical `a17dd669717354bfdfcb6c05146836aacc62be8f`; probe run `35495680174`, artifact `10600194493`, digest `sha256:5f82165eeb7c20c71c8abe27c32ad5a26eca2a66e9c26bad57737f725cfa5757`. Uses 26.2 `DebugRenderer.emitGizmos`, `Gizmos`, `GizmoStyle`; preserves VS2 transforms and hitbox gate. Frozen P1 compile/API green.
- **LevelRenderer / LevelExtractor split** — canonical `660d5320902a3ecba4f3219969aa77b0316cfa52`; successful lifecycle probe `ea4fe41eea15ff879ddcebe005f401bf01c0ce23` run `35494987861`, artifact `10600567053`; block-damage proof `8c19b74c5b69f1ab28a241b55672840af2824bd0` run `35495140731`, artifact `10599724029`. Existing `IVSCamera` observation only; no replacement camera authority.
- **Pathfinding debug lifecycle** — canonical `f56fa6d76d31661e561de85b7223b6de64e39de9`; proof `63c6c314719d3f75456d50332268f67ca243f9b1`, run `35494083822`, artifact `10600376722`, digest `sha256:dc8aada751ed3f75050029951cd0f2bf0f3551ebcbcf4af485219777456032ab`. Membership-only bridge; vanilla DebugValueAccess/gizmo lifecycle remains authority.

Do not reopen these frozen boundaries absent direct contradictory evidence.

## Recent mechanical convergence — preserved

Already-landed compatibility bridges that must not be repeated blindly include:

- `28ee0eabe77778dd2f9bbd84e528d9c3a6718531`: client sound `ResourceLocation` -> `Identifier`.
- `4aa395c810476d78c2f8cfb1bee423d2f5248616`: `BlockUtil` package relocation.
- `880df3aa1ecbdaf2a5b9974d65dd68a266fbc764`: `DimensionDataStorage` -> `SavedDataStorage`.
- `82887915b04b1546129ab0dba610d4ba0ed7e075`: `applyCarvers` signature.
- `9b229bbadfc3bab5ed918556144ad566ca37e448`: LevelChunk serializer vocabulary.
- `6faec034d400458d4471e8aa608c77ecb01119e9`: ChunkMap shutdown-work dispatcher.
- `480ca1e32024db619574b28488ad8a1c88045d52`: alpha-HUD lifecycle bridge.
- `f56fa6d76d31661e561de85b7223b6de64e39de9`: pathfinding debug lifecycle.
- `660d5320902a3ecba4f3219969aa77b0316cfa52`: client LevelRenderer / LevelExtractor split.
- `a17dd669717354bfdfcb6c05146836aacc62be8f`: ship-debug bounding-box gizmo.
- `290e2bb6c1f6248437e4d189dfb4a01e82a31e33`: vanilla renderer 26.2 bridge.

These are compatibility adaptations only and authorize no replacement VS2 architecture.

## Frozen architecture-sensitive boundaries

All prior frozen-green proof records in Git history remain binding. Key locks:

- **Real VS2 ship chunk-ticket lifecycle** — `65a42e782de192f27d5bf720691d6e08f395a719`; proof `35450402031`. Load-only radius-zero ticket add/remove lifecycle, flush/order, alive removal guard and deletion cleanup remain authority.
- **DistanceManager / TicketStorage read bridge** — `8a338f95103227ed6a5acb35804d573bbae0d96c`; proof head `ca07a2fff0fd922cbbd578a0531d3377313827de`, P0 `35463018487`, proof `35463018541`. READ ONLY.
- **ShipSavedData persistence** — `f2b3ec68e0d2146bb8b443da76a62a4766e01fce`; proof `35451366140`.
- **Entity local authority / interpolation** — `b7e583af13598b6ddcc583380872f578b8a40bb8`; proof head `9f2719be070e79b91b7f47ceddaec61d7f5cff40`, proof `35455551701`. No synthetic carry.
- **Entity renderer submit lifecycle** — `a87512437f40a3bfa1325d78f8e2588587ec7cc8`; proof head `58d8554ba623896d486b91f18771df9bdcd6f2b3`, proof `35458380245`.
- **Shipyard teleport API mapping** — P0 `35467615792`, proof `35467615790`; real VS2 transform authority, no manual teleport chase.
- NaturalSpawner, particle collision, EntitySectionStorage, WaterFluid, POIManager, AirAndWaterRandomPos, tick-ship-chunks, ship-debug overlay, weather, clip-replace, LavaFluid, Explosion, StructureTemplate, LevelChunk, ChunkMapClose, alpha HUD, pathfinding, client LevelRenderer/Extractor, ship-debug BB, and vanilla renderer boundaries remain frozen at proven scope.
- **Clip Direction** canonical `5d0fd81810a824b2da989b834dd6d2f92475dc33`; proof `35478902949`.
- **LavaFluid** canonical `19b0e356b34dae20c3aa8d9409d90fc0b96838b2`; proof `35479600673`.
- **Explosion accessor** canonical `322dcf22e2baf25192682d4b9ee942f4a35dc86b`; proof `35480514714`.
- **Optional Sable boundary** is compile-only. Never bundle or claim 1.21.1 Sable runtime compatibility on 26.2 without separate evidence.
- **Create deployer helper isolation** is P1 compile isolation only, never P3 integration.

## Locked negative evidence

- `3bcbf90c75dc4d02448cfdb4590cc9c9674e0ed6` / run `35454717409`: wrong Kotlin source-set exclusion for `DeployerScrollOptionSlot`; do not replay.
- `a72aaef8eca34a352ef949eeb57e6bbcda81171f`: `setUnsaved(false)` invalid current API.
- VSKeyBindings failed probes `e108526cbd728454c175c76bffc610d4e074da49`, `fcc65187d79c4b546883875da3597345db1e01cd`, `e9a3efd58acb2af9539628eb2875e6cb829c3cec`, `fb3c7e65a4c2089f6fa695114734d14836bde1d3` remain negative evidence.
- pathfinding probe `b3927e625acf40edbf517970ebc952a104a20c97` / `35493933563`: too-strict textual javap assertion only.
- initial LevelRenderer probe `3e824228...` / `35494738882`: obsolete-owner assertion only.
- renderer camera probe `3d6ca4d5...` / `35497721437`: textual uniform-name assertion only; bytecode evidence remains valid.
- renderer helper/proof runs `35497975815` and `35498155312`: bare `Uniform` guard falsely matched `DynamicUniforms`; never replay broad substring guard.
- Actions self-push workflow changes without `workflows` permission remains failed transport hypothesis.
- retired `apm23/VS2-Create_Interactive` workarounds are forbidden implementation source.

## Current remaining Java compile frontier

Canonical implementation `290e2bb6c1f6248437e4d189dfb4a01e82a31e33`, artifact `10601028900`:

- **12 `: error:` markers / 2 normalized source files / 4 primary javac errors**.
- `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/sable/MixinSubLevelHoldingChunkMap.java` — 6 repeated markers / 2 primary errors: missing `dev.ryanhcode.sable.sublevel.storage.holding.SubLevelHoldingChunkMap` and its `@Mixin` class reference.
- `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/sable/MixinActiveSableCompanion.java` — 6 repeated markers / 2 primary errors: missing `dev.ryanhcode.sable.ActiveSableCompanion` and its `@Mixin` class reference.
- No non-Sable Java compile unit remains in the observed javac frontier.

Classification: **OPTIONAL_SABLE_COMPILE_ISOLATION**. This is compile-only optional-mod residue and is not authority for standalone VS2 runtime behavior.

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
- active_blocker: `OPTIONAL_SABLE_COMPILE_ISOLATION`
- active_proof_head: `290e2bb6c1f6248437e4d189dfb4a01e82a31e33; canonical P1 chain through frozen vanilla renderer 26.2 bridge`
- active_proof_run: `P0 35498340524 success; P1 compile 35498340530 frontier-only failure; artifact 10601028900; 12 repeated error markers / 2 normalized source files / 4 primary javac errors; all Sable-only`
- active_hypothesis: `inspect the exact existing Sable compile-only overlay, pinned upstream Sable mixins/mixin configuration and resolved dependency availability; only isolate the two optional Sable Java sources if exact evidence proves they are optional and absent from the locked standalone 26.2 environment`
- final_ready: `false`
- user_runtime_validation: `NOT_APPLICABLE_YET`
- video_status: `NOT_APPLICABLE_YET`

## Engineering locks

- First-failure classification stays factual.
- Make one evidence-backed root/semantic change at a time.
- Standalone real VS2 P1 must initialize before Create integration.
- Never replace ship-space/physics/collision/entity-dragging/player-camera systems with a new custom implementation.
- Never use synthetic carry/inertia, fake gravity, manual floor/wall/ceiling clamps, per-tick teleport/setPos chase, camera forcing, duplicate authority, or floor-only success as final architecture.
- Frozen renderer bridges must not expand into movement/camera/collision/gameplay authority.
- Frozen TicketStorage bridge remains read-only; frozen real ticket lifecycle remains load authority.
- Sable work is compile-only optional-mod isolation and may not imply runtime compatibility.
- `FINAL_READY` is forbidden from CI alone; video is closure-only.

## next_safe_action

1. This ledger reconciliation commit is documentation-only. Require exact-head P0 provenance success before another source/workflow mutation.
2. Preserve all frozen boundaries and negative evidence. Do not repeat landed renderer/debug patches.
3. Use artifact `10601028900` as canonical **12-marker / 2-source-file / 4-primary-error** frontier until compiler state changes.
4. Do not reopen vanilla renderer, ship-debug BB, pathfinding, client LevelRenderer/Extractor, physics, collision, dragging, player/camera, networking, ship lifecycle, Create, SNR or Copycats.
5. Inspect `scripts/apply_p1_sable_companion_compileonly_26_2.py`, the two pinned upstream Sable mixins, their mixin configuration entries, and build/dependency declarations. Determine whether Sable is explicitly optional and absent from the resolved locked standalone 26.2 classpath.
6. If exact evidence proves these are optional compatibility sources with no locked 26.2 Sable runtime, create exactly one bounded fail-closed compile-only isolation covering only the two Sable source files/config entries required for standalone P1 compilation. Do not bundle stubs and do not claim Sable runtime compatibility. Otherwise HOLD.
7. Prove the isolation with exact canonical standalone P1 compile. If compilation advances, classify the next first failure before any further mutation.
8. Remain standalone P1. No ordinary compile/debug video.

## Video and milestone gate

- `M1_COMPLETE` is forbidden until full P2 real-VS2 runtime proof exists: real ship lifecycle, translation+rotation, ship-space, collision, standing/walking, jump-airborne-natural landing, floor/walls/ceiling, stable free camera/look, entity dragging/reference space, rendering, and client/server sync.
- `FINAL_BUILD`, `FINAL_VERIFY`, and `FINAL_READY` are not applicable during P1.
- Video is closure-only. Visible failure overrides telemetry green. `FINAL_READY` still requires exact-final-JAR real-user runtime acceptance.
