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

## Current reconciliation — 2026-09-20 P1 Java API frontier

Current proven implementation boundary before this documentation-only reconciliation commit:

- canonical implementation HEAD: `cc56a4ca3a8b851d283f051d090f434628de1ec6` — `ci: retrigger Camera accessor after exact guard repair`.
- exact-head P0 provenance run `35501765675`: **success**.
- exact-head ship-debug/dispatcher proof run `35501765686`: **success**, including replay, isolated dispatcher apply, semantic validation, unrelated-failure compile preservation, and ship-debug compiler-clean proof.
- exact-head standalone P1 compile run `35501765677`: **compile-frontier failure only**. All canonical overlays/apply steps, port-delta validation, and Gradle runtime steps succeeded; diagnostic upload succeeded.
- canonical compile artifact: `p1-compile-log-cc56a4ca3a8b851d283f051d090f434628de1ec6`, ID `10602268395`, artifact digest `sha256:4bc1959854df54971730967fafb041cef57c13166e6ab5be3184b4a1ed9234c9`.
- extracted `p1-compile.log`: **297300 bytes**, SHA-256 `8d9d9f8e4fe10b09f1b0d7f9fa8dad5b3b1c93f21e9eb9b049898c079bade8b7`.
- current primary javac pass: **94 errors across 20 Java source files**. Gradle repeats the same diagnostics later in the log; the primary count is authoritative for frontier size.
- project state: `P1_SOURCE_API_ADAPTATION_IN_PROGRESS`.
- active blocker classification: `MINECRAFT_26_2_JAVA_API_FRONTIER`.
- This is not P1 boot proof, not M1 proof, and not runtime rendering proof.

### Current primary Java frontier at `cc56a4ca...`

Primary javac errors by normalized source file:

1. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/immersive_portals/MixinMyBuiltChunkStorage.java` — 25
2. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/vanilla_renderer/MixinViewAreaVanilla.java` — 14
3. `common/src/main/java/org/valkyrienskies/mod/mixin/client/world/MixinClientChunkCache.java` — 11
4. `common/src/main/java/org/valkyrienskies/mod/mixin/world/chunk/MixinLevelChunk.java` — 8
5. `common/src/main/java/org/valkyrienskies/mod/mixin/feature/entity_movement_packets/MixinLocalPlayer.java` — 4
6. `common/src/main/java/org/valkyrienskies/mod/mixin/feature/fix_render_chunk_sorting/MixinRenderChunk.java` — 4
7. `common/src/main/java/org/valkyrienskies/mod/mixin/server/world/MixinServerLevel.java` — 4
8. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/vanilla_renderer/MixinLevelRendererVanilla.java` — 3
9. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/immersive_portals/MixinImmPtlChunkTracking.java` — 3
10. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/optifine_vanilla/MixinLevelRenderer.java` — 3
11. `common/src/main/java/org/valkyrienskies/mod/compat/SodiumCompat.java` — 2
12. `common/src/main/java/org/valkyrienskies/mod/mixin/client/world/MixinClientLevel.java` — 2
13. `common/src/main/java/org/valkyrienskies/mod/mixin/client/multiplayer/MixinClientPacketListener.java` — 2
14. `common/src/main/java/org/valkyrienskies/mod/mixin/server/world/MixinChunkMap.java` — 2
15. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/ftb_chunks/MixinClaimedChunkManagerImpl.java` — 2
16. `common/src/main/java/org/valkyrienskies/mod/mixin/entity/MixinEntity.java` — 1
17. `common/src/main/java/org/valkyrienskies/mod/mixin/feature/teleport_reconnected_player_to_ship/MixinServerPlayer.java` — 1
18. `common/src/main/java/org/valkyrienskies/mod/mixin/feature/entity_collision/MixinLivingEntity.java` — 1
19. `common/src/main/java/org/valkyrienskies/mod/mixin/world/level/levelgen/MixinNoiseBasedChunkGenerator.java` — 1
20. `common/src/main/java/org/valkyrienskies/mod/mixin/server/MixinMinecraftServer.java` — 1

Do not treat this list as permission for a bulk rewrite. Continue one bounded evidence-backed 26.2 API unit at a time.

## Newly converged mechanical units — current cycle

### Legacy Sable compile-only isolation — completed

- The prior Sable-only frontier is no longer the active blocker.
- Canonical dispatcher now removes only the two exact optional legacy Sable mixin sources plus their common mixin registration for standalone P1 compilation.
- This is compile-only isolation. It does not bundle, emulate, or claim Sable runtime compatibility on 26.2.

### ChunkPos record accessor family — completed for the proven set

- Canonical helper adapts **54 active** `ChunkPos.x/z` field accesses to Minecraft 26.2 record accessors `x()/z()` across 10 files.
- Historical/commented-out occurrences are not blindly rewritten.
- The original 40-error batch was removed; a later javac pass exposed 14 additional active sites in `MixinServerLevel` and `MixinChunkMapShipyard`, which were added under the same bounded mechanical hypothesis.

### Level client-side accessor family — completed for the proven set

- Canonical helper adapts **7 exact** `Level.isClientSide` field uses to the public `isClientSide()` method across 2 files.

### CompoundTag Optional primitive family — completed for the proven set

- Canonical helper adapts **7 exact** primitive reads to the 26.2 Optional-returning API with the old primitive default semantics preserved.

### World-weather ServerLevel vocabulary — frozen P1 compile-clean at target

- helper: `scripts/apply_p1_world_weather_serverlevel_26_2.py`
- helper creation: `531abf3b307b8198698d8452d62cf761154f5cf1` — `fix: adapt server weather API to 26.2`.
- canonical wiring: `1fc653b2641ae1b95f2de264cdd10d45a0fa8dcb` — `fix: chain server weather 26.2 overlay`.
- exact pinned target blob: `82442838833e64b8d854091be5b93f7ded8793c3`.
- exact adaptation: 1× `getMinBuildHeight()` -> `getMinY()` and 3× `BlockPos.getCenter()` -> `Vec3.atCenterOf(...)`.
- upstream VS2 weather/ship-space authority anchors remain unchanged.
- exact-head `1fc653...` P0 run `35501378926`: **success**; dispatcher proof `35501378851`: **success**; P1 compile `35501378883`: unrelated-frontier failure only.
- compile artifact `10602646175`, digest `sha256:ff9ada938ff73aaf1ede5e19a69d4ae0a0d2c9502ba30a30e2162a8bfaad0466`.
- independent artifact inspection: `world_weather/MixinServerLevel.java` has **zero compiler error markers**.
- Freeze this four-call-site unit at P1 compile/API scope; no runtime-weather claim yet.

### Camera `position()` accessor family — frozen P1 compile-clean at the three proven sites

- exact MC26.2 mapped `Camera` evidence from artifact `10601632052` proves `public net.minecraft.world.phys.Vec3 position()`.
- helper created at `86c02dd04d951f10c7ecd042d0db0e5767054d28`.
- first canonical wiring `414091705188ec6ee9a672e5f6b9bab9867684c1` failed only because the helper incorrectly expected the **raw** block-entity mixin blob after an earlier canonical source-API overlay had already widened `BlockEntityRenderer<E>` to `BlockEntityRenderer<E, ?>`. This is locked assertion/integration negative evidence, not an API failure.
- guard repair `4640a16c0af2bc383cf8afd061629b4ec54519c1` anchors the exact post-source-api blob `25eec1917bf21d640a8f9ddd96611b25a700f1df` while preserving authority anchors.
- canonical retrigger/implementation boundary `cc56a4ca3a8b851d283f051d090f434628de1ec6`.
- exact adaptation only:
  - `MixinBlockEntityRenderDispatcher`: `this.camera.getPosition()` -> `this.camera.position()`;
  - `MixinGameRenderer`: `camera.getPosition()` -> `camera.position()`;
  - `MixinGameRenderer`: `this.mainCamera.getPosition()` -> `this.mainCamera.position()`.
- no camera acquisition, camera transform, orientation, reference-space, or forcing logic was added or changed.
- exact-head P0 `35501765675`: **success**; dispatcher proof `35501765686`: **success**; canonical compile `35501765677`: unrelated-frontier failure only.
- artifact `10602268395`, digest `sha256:4bc1959854df54971730967fafb041cef57c13166e6ab5be3184b4a1ed9234c9`.
- independent artifact inspection: both `MixinBlockEntityRenderDispatcher.java` and `client/renderer/MixinGameRenderer.java` have **zero compiler error markers**.
- Freeze only these three accessor sites at P1 compile/API scope.

## Vanilla renderer 26.2 bridge — frozen P1 compile/API boundary

Pinned upstream target:
`common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/vanilla_renderer/MixinLevelRendererVanilla.java`, exact upstream blob `824e1ac56a99bc6480cc80c32c085d18c2425b09`.

Canonical bridge boundary `290e2bb6c1f6248437e4d189dfb4a01e82a31e33` remains architecture-frozen:

- ship-aware compile distance still uses `VSGameUtilsKt.squaredDistanceBetweenInclShips`;
- loaded `ClientShip` iteration, `ShipRenderer.VANILLA`, active-chunk/air-section checks and transformed ship render-AABB frustum semantics remain upstream VS2 behavior;
- terrain/block-entity transform authority remains upstream `VSClientGameUtils.transformRenderWithShip`;
- Minecraft 26.2 retains terrain GPU/draw ownership through `prepareChunkRenders`, `ChunkSectionsToRender`, and `DynamicUniforms.ChunkSectionInfo`;
- no physics, collision, movement, entity-dragging, camera forcing, ship lifecycle, or replacement reference-space authority is introduced.

Evidence:

- terrain/frustum probe `20a99be85e597385b01dd9892b4028ab9020d5fa`, run `35497544023`: success; artifact `10601551867`, digest `sha256:963c973bba1b9003e280395327e984d44e482fc0883fdd461aaf94e7870368bc`.
- camera/global-uniform artifact `10601632052`, digest `sha256:117146b78f813612288fcbeb0d13fe6d2bb7cdd47a546f2039cecb60aaf8e59d`; run `35497721437` failed only over-strict textual assertion. Bytecode evidence remains valid.
- corrected scratch proof `3be7a411b73bc48aa9f34fdb55b84332bae2d00c`, run `35498189907`: success; artifact `10600767769`, digest `sha256:96fa794b526d7c175a95d9ea609f2e72ba272e6942b239a0ca70fd25fd1d3e09`.

The current 94-error frontier again contains `MixinLevelRendererVanilla` errors exposed after later compiler progress. Do **not** reopen the frozen transform/authority design. Any follow-up there must be a separately evidenced 26.2 API/lifecycle adaptation.

## Other frozen renderer/debug boundaries

- **Ship debug bounding-box gizmo** — `a17dd669717354bfdfcb6c05146836aacc62be8f`; probe `35495680174`, artifact `10600194493`, digest `sha256:5f82165eeb7c20c71c8abe27c32ad5a26eca2a66e9c26bad57737f725cfa5757`.
- **LevelRenderer / LevelExtractor split** — `660d5320902a3ecba4f3219969aa77b0316cfa52`; lifecycle probe `35494987861`, artifact `10600567053`; block-damage proof `35495140731`, artifact `10599724029`. Existing `IVSCamera` observation only; no replacement camera authority.
- **Pathfinding debug lifecycle** — `f56fa6d76d31661e561de85b7223b6de64e39de9`; proof `35494083822`, artifact `10600376722`, digest `sha256:dc8aada751ed3f75050029951cd0f2bf0f3551ebcbcf4af485219777456032ab`.

Do not reopen these boundaries absent direct contradictory evidence.

## Frozen architecture-sensitive boundaries

- **Real VS2 ship chunk-ticket lifecycle** — `65a42e782de192f27d5bf720691d6e08f395a719`; proof `35450402031`.
- **DistanceManager / TicketStorage read bridge** — `8a338f95103227ed6a5acb35804d573bbae0d96c`; proof head `ca07a2fff0fd922cbbd578a0531d3377313827de`, P0 `35463018487`, proof `35463018541`. READ ONLY.
- **ShipSavedData persistence** — `f2b3ec68e0d2146bb8b443da76a62a4766e01fce`; proof `35451366140`.
- **Entity local authority / interpolation** — `b7e583af13598b6ddcc583380872f578b8a40bb8`; proof head `9f2719be070e79b91b7f47ceddaec61d7f5cff40`, proof `35455551701`. No synthetic carry.
- **Entity renderer submit lifecycle** — `a87512437f40a3bfa1325d78f8e2588587ec7cc8`; proof head `58d8554ba623896d486b91f18771df9bdcd6f2b3`, proof `35458380245`.
- **Shipyard teleport API mapping** — P0 `35467615792`, proof `35467615790`; real VS2 transform authority, no manual teleport chase.
- **Clip Direction** — `5d0fd81810a824b2da989b834dd6d2f92475dc33`; proof `35478902949`.
- **LavaFluid** — `19b0e356b34dae20c3aa8d9409d90fc0b96838b2`; proof `35479600673`.
- **Explosion accessor** — `322dcf22e2baf25192682d4b9ee942f4a35dc86b`; proof `35480514714`.
- Optional Sable remains compile-only isolation; never claim 26.2 Sable runtime compatibility without separate evidence.
- Create deployer helper isolation remains P1 compile isolation only, never P3 integration.

## Recent mechanical convergence — preserved

Do not repeat blindly. Important landed families include:

- client sound `ResourceLocation` -> `Identifier`;
- `BlockUtil` relocation;
- `DimensionDataStorage` -> `SavedDataStorage`;
- `applyCarvers` signature;
- LevelChunk serializer vocabulary;
- ChunkMap shutdown-work dispatcher;
- alpha-HUD lifecycle;
- pathfinding lifecycle;
- LevelRenderer/LevelExtractor split;
- ship-debug BB gizmo;
- vanilla renderer bridge;
- Sable compile-only isolation;
- 54 active ChunkPos record accessors;
- 7 Level client-side accessors;
- 7 CompoundTag Optional primitive reads;
- world-weather ServerLevel 4-call-site adaptation;
- three proven Camera `position()` accessors.

These are compatibility adaptations only and authorize no replacement VS2 architecture.

## Locked negative evidence

- `3bcbf90c75dc4d02448cfdb4590cc9c9674e0ed6` / `35454717409`: wrong Kotlin source-set exclusion for DeployerScrollOptionSlot.
- `a72aaef8eca34a352ef949eeb57e6bbcda81171f`: `setUnsaved(false)` invalid.
- VSKeyBindings failed probes `e108526cbd728454c175c76bffc610d4e074da49`, `fcc65187d79c4b546883875da3597345db1e01cd`, `e9a3efd58acb2af9539628eb2875e6cb829c3cec`, `fb3c7e65a4c2089f6fa695114734d14836bde1d3`.
- pathfinding `b3927e625acf40edbf517970ebc952a104a20c97` / `35493933563`: too-strict textual javap assertion only.
- initial LevelRenderer probe `3e824228...` / `35494738882`: obsolete-owner assertion only.
- renderer camera probe `3d6ca4d5...` / `35497721437`: textual uniform-name assertion only; bytecode evidence valid.
- renderer proof failures `35497975815` and `35498155312`: bare `Uniform` guard falsely matched `DynamicUniforms`; never replay broad substring guard.
- `414091705188ec6ee9a672e5f6b9bab9867684c1` / proof `35501644581` / canonical `35501644590`: Camera accessor helper expected raw BlockEntityRenderDispatcher blob after `apply_p1_source_api_26_2.py` had already changed its renderer generic. Guard failure only; corrected at `4640a16...` and proven at `cc56a4ca...`.
- Actions self-push workflow changes without `workflows` permission remain failed transport hypothesis.
- retired `apm23/VS2-Create_Interactive` workarounds are forbidden implementation source.

## Target runtime baseline

- Minecraft `26.2`
- Java `25`
- Fabric Loader observed `0.19.3`
- Fabric API `0.160.0+26.2`, SHA-256 `5f3dff88e1661166e222213302b25ace6c36dc3683804cbd4b5acf93138ea05e`
- Create Fly `6.0.9-1`, SHA-256 `d9c6cb6116d5caa1174a289ecd7d3cdd463ccef6e8db1249ab0bcfcd8c935870`
- embedded SNR `SNR.FLY-STABLE-1.2.2+fabric-mc26.2`, SHA-256 `33c87d5a7da0d468d3b6c0e99f726b835c63b693e7447fdaeca5e1f204caab84`
- embedded Copycats `3.0.7-createfly+mc.26.2-v1.14`, SHA-256 `1922db10a49dfab42c4c272fbaee41cdc149287cd08ca84148b497e598029858`
- exact final lock remains `BASELINE_LOCK.json`.

## Milestone state

- P0 provenance/import: established and continuously gated.
- P1 standalone VS2: **source/API adaptation in progress**.
- P1 standalone boot/runtime: not yet proven.
- P2/M1 real standalone ship: not started as a completed milestone.
- P3 Create Fly bridge: not authorized yet.
- P4 SNR + Copycats: not authorized yet.
- P5/final: not authorized yet.
- `M1_COMPLETE`, `FINAL_BUILD`, `FINAL_VERIFY`, and `FINAL_READY` are forbidden at the current state.

## next_safe_action

Do **not** reopen completed Sable, ChunkPos, client-side accessor, CompoundTag, world-weather ServerLevel, or the three proven Camera-position units.

Next action is one bounded P1 Java API unit from the current `cc56a4ca...` artifact. Preferred candidate is `feature/fix_render_chunk_sorting/MixinRenderChunk.java` because its four primary errors are a small coherent camera-API family, but **first obtain exact Minecraft 26.2 evidence for the current GameRenderer camera acquisition owner/method**. `Camera.position()` itself is already exact-proven; the old `GameRenderer.getMainCamera()` replacement is not yet authorized by this ledger. If exact API evidence supports a direct minimal owner/method mapping, patch only that file and preserve its existing VS2 ship/world distance semantics. Otherwise select another small compiler-proven unit with exact API evidence.

For optional compat frontiers (Immersive Portals, FTB, OptiFine, Sodium), do not invent stubs or replacement integrations. Isolate or adapt only when dependency status and runtime intent are explicitly evidenced.

After each source change: require exact-head P0 green, consume only the relevant latest P1 run, independently inspect the compile artifact, update this ledger when the frontier meaningfully moves, and never infer runtime success from compile success.
