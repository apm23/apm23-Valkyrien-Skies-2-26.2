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

- upstream repository: `ValkyrienSkies/Valkyrien-Skies-2`
- selection branch: `1.21.1/main`
- exact commit: `f39132148e717d325933b4ce6e9e9fb13d929390`
- exact root tree: `91116399605d3ecd1c93b0011560e09281ee1fa4`
- upstream mod version: `2.4.12`
- imported as gitlink/submodule `upstream-vs2/`

Minecraft 26.2 changes are applied by explicit fail-closed overlays. Every core subsystem must remain traceable to upstream VS2 or to a documented minimal 26.2 adaptation feeding the existing VS2 architecture.

## Current reconciliation — 2026-09-20 P1 Java API frontier

Current proven implementation boundary before this documentation-only reconciliation commit:

- canonical implementation HEAD: `62475d87c27412edcadfe67aa13640f99602c866` — `ci: retrigger corrected ChunkMap packed-key proof`.
- exact-head P0 provenance run `35504056641`: **success**.
- exact-head ship-debug/canonical-chain proof run `35504056674`: **success**. Replay, isolated apply, semantic validation, unrelated-failure compile preservation, and existing ship-debug compiler-clean proof all succeeded.
- exact-head standalone P1 compile run `35504056711`: **compile-frontier failure only**. All 87 canonical overlay/apply steps, port-delta validation, Gradle runtime, and diagnostic upload succeeded.
- canonical compile artifact: `p1-compile-log-62475d87c27412edcadfe67aa13640f99602c866`, ID `10602658986`, artifact digest `sha256:7ef66587b81a6087fecfa8290849f628c13bf9cfc10143c061b5af42143d7916`.
- extracted `p1-compile.log`: **285058 bytes**, SHA-256 `1ad7a2c767bc6bff5cafbb853db7c3b6c3942be6217ec940b691870bdff16764`.
- authoritative primary javac pass: **86 errors across 16 Java source files**. Gradle repeats the same diagnostics later; use the first `86 errors` javac summary as frontier authority.
- project state: `P1_SOURCE_API_ADAPTATION_IN_PROGRESS`.
- active blocker classification: `MINECRAFT_26_2_JAVA_API_FRONTIER`.
- This is not P1 boot proof, not P2/M1 ship proof, and not runtime rendering proof.

### Current primary Java frontier at `62475d87...`

1. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/immersive_portals/MixinMyBuiltChunkStorage.java` — 25
2. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/vanilla_renderer/MixinViewAreaVanilla.java` — 14
3. `common/src/main/java/org/valkyrienskies/mod/mixin/client/world/MixinClientChunkCache.java` — 11
4. `common/src/main/java/org/valkyrienskies/mod/mixin/world/chunk/MixinLevelChunk.java` — 8
5. `common/src/main/java/org/valkyrienskies/mod/mixin/feature/entity_movement_packets/MixinLocalPlayer.java` — 4
6. `common/src/main/java/org/valkyrienskies/mod/mixin/server/world/MixinServerLevel.java` — 4
7. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/vanilla_renderer/MixinLevelRendererVanilla.java` — 3
8. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/immersive_portals/MixinImmPtlChunkTracking.java` — 3
9. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/optifine_vanilla/MixinLevelRenderer.java` — 3
10. `common/src/main/java/org/valkyrienskies/mod/compat/SodiumCompat.java` — 2
11. `common/src/main/java/org/valkyrienskies/mod/mixin/client/world/MixinClientLevel.java` — 2
12. `common/src/main/java/org/valkyrienskies/mod/mixin/client/multiplayer/MixinClientPacketListener.java` — 2
13. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/ftb_chunks/MixinClaimedChunkManagerImpl.java` — 2
14. `common/src/main/java/org/valkyrienskies/mod/mixin/entity/MixinEntity.java` — 1
15. `common/src/main/java/org/valkyrienskies/mod/mixin/feature/entity_collision/MixinLivingEntity.java` — 1
16. `common/src/main/java/org/valkyrienskies/mod/mixin/server/MixinMinecraftServer.java` — 1

`MixinChunkMap.java`, reconnect `MixinServerPlayer.java`, `MixinNoiseBasedChunkGenerator.java`, and `MixinRenderChunk.java` are no longer in the primary javac frontier.

Do not treat this list as permission for a bulk rewrite. Continue one bounded, evidence-backed Minecraft 26.2 API unit at a time.

## Newly converged bounded units

### ChunkMap spawning-distance ChunkPos vocabulary — frozen P1 compile-clean

Pinned upstream target:
`common/src/main/java/org/valkyrienskies/mod/mixin/server/world/MixinChunkMap.java`, blob `4ddfc6a20cc1ca00adb5a5c848623c37132c73d3`.

Upstream behavior preserved:
- `anyPlayerCloseEnoughForSpawning` still transforms the chunk middle block position through `VSGameUtilsKt.toWorldCoordinates(level, ...)` and calls the original `DistanceManager.hasPlayersNearby` wrapper with the resulting packed chunk key;
- `playerIsCloseEnoughForSpawning` still transforms the chunk middle block position through the same VS2 world-space authority and calls the original Euclidean-distance wrapper;
- player watching, ship lookup, save filtering, and all unrelated ChunkMap behavior remain unchanged.

Exact adaptation:
- `new ChunkPos(BlockPos.containing(VSGameUtilsKt.toWorldCoordinates(...arg...))).toLong()` -> `ChunkPos.containing(BlockPos.containing(VSGameUtilsKt.toWorldCoordinates(...arg...))).pack()`;
- `new ChunkPos(BlockPos.containing(VSGameUtilsKt.toWorldCoordinates(...d0...)))` -> `ChunkPos.containing(BlockPos.containing(VSGameUtilsKt.toWorldCoordinates(...d0...)))`.

Evidence/history:
- initial bounded helper created at `b170d13aa295e9693f78c0d2e33e55e264f4019e`.
- first canonical chain `41d697a8fb3c23bbc02140cba529399cc4670898`: P0 `35503664475` success, proof `35503664699` success, P1 `35503664472` unrelated-frontier failure; artifact `10603306555`, digest `sha256:9a4a54de29b804cca30012341154dea2c7c48b6854a02e8a1ec75764b05e0df8`, extracted log SHA-256 `cd07c050f144fed1137cc9d1d7fa2bafa3f2bb63f2267399bd992c48a4f28717`. This reduced the global frontier **88 -> 87** but left one exact `ChunkPos.containing(...).toLong()` error in `MixinChunkMap`.
- `0a724f22cee622dd212b7526439426cd4289e64b` / canonical retrigger `6ce41dfbef36b8c8021f48f52f0020e7b1131d5f` incorrectly targeted a nonexistent `getById(arg.toLong())` expression. P0 `35503933601` succeeded, but proof `35503933610` and P1 `35503933627` failed before javac at the helper guard. **Locked assertion-only/wrong-target negative evidence; no compile signal. Do not replay.**
- exact artifact inspection corrected the target to the spawning wrapper's `new ChunkPos(...).toLong()` expression.
- corrected helper `96739ba02bd5620d4225232d70c86a56c25b4be5`; helper-only P0 `35504023890` success.
- final canonical proof boundary `62475d87c27412edcadfe67aa13640f99602c866`: P0 `35504056641` success, proof `35504056674` success, P1 `35504056711` unrelated-frontier failure.
- artifact `10602658986`, digest `sha256:7ef66587b81a6087fecfa8290849f628c13bf9cfc10143c061b5af42143d7916`, proves `MixinChunkMap.java` has **zero primary javac errors** and reduces global frontier **87 -> 86** and **17 -> 16 files**, with no new source frontier.

Freeze this exact three-vocabulary-site unit at P1 compile/API scope. It changes no spawning-distance, ship-transform, ticket, or player-watching authority.

### Reconnected-player mixin superclass constructor — frozen P1 compile-clean

- target `feature/teleport_reconnected_player_to_ship/MixinServerPlayer.java`, upstream blob `71d145feac17c628a6d0807edbcd74d311abdce4`.
- exact adaptation only: unreachable mixin constructor `super(level, blockPos, f, gameProfile)` -> Minecraft 26.2 `super(level, gameProfile)`.
- save/load injections, ship lookup, ship-to-world restore transform, and world-to-ship save transform remain unchanged.
- first proof `e9499c10396afbc341a915a585926773fbfc5e7b` / `35503354785` failed only an authority-anchor count assertion; no compile signal. Guard corrected at `1759012799662ad9c86c8656e92b0256e3fcb73c`.
- canonical `e84097bd8aa6a588f3b16d47db4f8894df42ae83`: P0 `35503419553` success, proof `35503419721` success, P1 `35503419633` unrelated-frontier failure; artifact `10603565748`, digest `sha256:011b57bfe89f51ffa7cc93165e955ddd066af5401af614b0afee527edd109332`. Target 0 errors; frontier 89 -> 88 and 18 -> 17 files.

### NoiseBasedChunkGenerator height vocabulary — frozen P1 compile-clean

- canonical `c66a45c7c34e89690c4b1ea74d15259a108f5aed`.
- exact adaptation: one `LevelHeightAccessor.getMinBuildHeight()` -> `getMinY()` in existing shipyard noise-generation guard; `VS2ChunkAllocator` authority unchanged.
- P0 `35502363441`, proof `35502363442`; artifact `10602184412`, digest `sha256:f38811d8ab70fc0ca1c431b44d6af4a62c7b7846e5a03ed674a87ece2973f0ae`; target 0, frontier 90 -> 89 and 19 -> 18 files.

### Render-chunk sorting Camera vocabulary — frozen P1 compile-clean

- canonical `c3521c0ee92bb7566d182f6a6c34999c303a7b50`.
- exact adaptation: `GameRenderer.getMainCamera()` -> `mainCamera()` and 3x `Camera.getPosition()` -> `position()`.
- upstream VS2 ship-to-world render transform and distance calculation remain unchanged; no camera forcing/reference-space authority introduced.
- P0 `35502115969`, proof `35502115961`; artifact `10602721957`; target 0, frontier 94 -> 90.

### Earlier current-cycle mechanical families — frozen at proven scope

- optional legacy Sable compatibility: compile-only isolation; no 26.2 Sable runtime compatibility claim.
- ChunkPos record accessors: 54 active `x/z` field sites -> `x()/z()` across 10 exact files; no blind comment/history sweep.
- Level client-side accessors: seven exact `Level.isClientSide` -> `isClientSide()` sites.
- CompoundTag Optional primitives: seven exact reads with legacy numeric fallback semantics.
- world-weather ServerLevel vocabulary: canonical `1fc653b2641ae1b95f2de264cdd10d45a0fa8dcb`; one `getMinBuildHeight()` -> `getMinY()` and three `BlockPos.getCenter()` -> `Vec3.atCenterOf(...)`; target compile-clean in artifact `10602646175`.
- Camera position accessor family: canonical `cc56a4ca3a8b851d283f051d090f434628de1ec6`; exactly three already-owned Camera `getPosition()` -> `position()` sites; no camera acquisition/transform/orientation change; artifact `10602268395`.

## Renderer/debug boundaries — frozen at proven scope

- **Vanilla renderer bridge** — canonical `290e2bb6c1f6248437e4d189dfb4a01e82a31e33`. Real upstream VS2 ship-aware distance, loaded-ship iteration, `ShipRenderer.VANILLA`, transformed ship AABB, and `VSClientGameUtils.transformRenderWithShip` remain authority. Minecraft 26.2 retains terrain draw/GPU authority through `prepareChunkRenders` / `DynamicUniforms.ChunkSectionInfo`. Frozen at P1 compile/API design scope only; later compiler progress exposed three new API errors, but do not redesign transform authority.
- renderer terrain/frustum probe `35497544023`, artifact `10601551867`; camera/global-uniform artifact `10601632052`; corrected scratch proof `35498189907`, artifact `10600767769`.
- **Ship debug BB gizmo** — `a17dd669717354bfdfcb6c05146836aacc62be8f`, proof `35495680174`, artifact `10600194493`.
- **LevelRenderer / LevelExtractor split** — `660d5320902a3ecba4f3219969aa77b0316cfa52`, lifecycle proof `35494987861`, block-damage proof `35495140731`. Existing `IVSCamera` is observation only; no replacement camera authority.
- **Pathfinding debug lifecycle** — `f56fa6d76d31661e561de85b7223b6de64e39de9`, proof `35494083822`, artifact `10600376722`.

## Frozen architecture-sensitive boundaries

Do not reopen absent direct contradictory evidence:

- real VS2 ship chunk-ticket lifecycle — `65a42e782de192f27d5bf720691d6e08f395a719`, proof `35450402031`.
- DistanceManager / TicketStorage read bridge — `8a338f95103227ed6a5acb35804d573bbae0d96c`, proof head `ca07a2fff0fd922cbbd578a0531d3377313827de`, P0 `35463018487`, proof `35463018541`; **READ ONLY**.
- ShipSavedData persistence — `f2b3ec68e0d2146bb8b443da76a62a4766e01fce`, proof `35451366140`.
- entity local authority / interpolation — `b7e583af13598b6ddcc583380872f578b8a40bb8`, proof `35455551701`; no synthetic carry.
- entity renderer submit lifecycle — `a87512437f40a3bfa1325d78f8e2588587ec7cc8`, proof `35458380245`.
- shipyard teleport API mapping — proof `35467615790`; real VS2 transform authority, no per-tick teleport chase.
- clip Direction — `5d0fd81810a824b2da989b834dd6d2f92475dc33`, proof `35478902949`.
- LavaFluid — `19b0e356b34dae20c3aa8d9409d90fc0b96838b2`, proof `35479600673`.
- Explosion accessor — `322dcf22e2baf25192682d4b9ee942f4a35dc86b`, proof `35480514714`.
- optional Create deployer helper is P1 compile isolation only, never P3 Create integration.

Forbidden final architecture remains: custom VS2-like reference frames, synthetic carry/inertia, fake gravity or wall/floor clamps, per-tick setPos chase, camera counter-rotation/forcing, duplicate authority, floor-only fake success, or reuse of retired `apm23/VS2-Create_Interactive` implementation code.

## Locked negative evidence

- `3bcbf90c75dc4d02448cfdb4590cc9c9674e0ed6` / `35454717409`: wrong Kotlin source-set exclusion for `DeployerScrollOptionSlot`.
- `a72aaef8eca34a352ef949eeb57e6bbcda81171f`: `setUnsaved(false)` invalid current API.
- VSKeyBindings failed probes `e108526cbd728454c175c76bffc610d4e074da49`, `fcc65187d79c4b546883875da3597345db1e01cd`, `e9a3efd58acb2af9539628eb2875e6cb829c3cec`, `fb3c7e65a4c2089f6fa695114734d14836bde1d3`.
- pathfinding `b3927e625acf40edbf517970ebc952a104a20c97` / `35493933563`: parser/assertion-only failure.
- initial LevelRenderer probe `3e824228...` / `35494738882`: obsolete-owner assertion-only failure.
- renderer camera probe `3d6ca4d5...` / `35497721437`: textual shader/uniform assertion-only failure; artifact bytecode evidence remains valid.
- renderer helper/proof `35497975815` and `35498155312`: broad substring `Uniform` falsely matched valid `DynamicUniforms`; never replay broad guard.
- Camera accessor first canonical attempt `414091705188ec6ee9a672e5f6b9bab9867684c1`: raw-upstream guard invalid after earlier generic widening; assertion-only.
- reconnect constructor proof `35503354785` at `e9499c10396afbc341a915a585926773fbfc5e7b`: authority-anchor count assertion-only failure.
- ChunkMap retrigger `6ce41dfbef36b8c8021f48f52f0020e7b1131d5f`, proof `35503933610`, P1 `35503933627`: helper wrongly targeted nonexistent `getById(arg.toLong())`; fail-closed assertion before javac. Exact artifact showed the real remaining call was `ChunkPos.containing(...).toLong()` in the spawning wrapper. Never replay the wrong target.
- Actions self-push workflow edits without `workflows` permission remain failed transport hypothesis.
- retired `apm23/VS2-Create_Interactive` implementation is forbidden.

## Target runtime baseline

Exact `BASELINE_LOCK.json` remains authoritative. Current locked stack includes:

- Minecraft `26.2`
- Java `25`
- Fabric Loader observed `0.19.3`
- Fabric API `0.160.0+26.2`, SHA-256 `5f3dff88e1661166e222213302b25ace6c36dc3683804cbd4b5acf93138ea05e`
- Create Fly `6.0.9-1`, SHA-256 `d9c6cb6116d5caa1174a289ecd7d3cdd463ccef6e8db1249ab0bcfcd8c935870`
- SNR embedded `SNR.FLY-STABLE-1.2.2+fabric-mc26.2`, SHA-256 `33c87d5a7da0d468d3b6c0e99f726b835c63b693e7447fdaeca5e1f204caab84`
- Copycats embedded `3.0.7-createfly+mc.26.2-v1.14`, SHA-256 `1922db10a49dfab42c4c272fbaee41cdc149287cd08ca84148b497e598029858`

Create/SNR/Copycats are not authority for current standalone P1 source adaptation and must not be pulled into the active frontier prematurely.

## Phase gates

- P0 provenance/import: maintained by exact-head provenance workflow.
- P1 standalone VS2 source/API/boot: **in progress**. Java compile frontier remains.
- P2/M1 real standalone VS2 ship: not entered; `M1_COMPLETE` forbidden.
- P3 Create Fly bridge: not entered.
- P4 SNR + Copycats: not entered.
- P5/final: not entered.
- `FINAL_READY` requires exact-final-JAR real-user runtime acceptance; CI alone can never authorize it.
- Video is closure-only, never compile/debug instrumentation.

## next_safe_action

1. This ledger commit is documentation-only. Require exact-head P0 provenance success before the next source mutation.
2. Preserve all frozen boundaries and negative evidence above. Do not reopen renderer architecture, physics, collision authority, dragging, player/camera authority, networking, ship lifecycle, Create, SNR, or Copycats merely because compiler errors remain nearby.
3. Treat artifact `10602658986` as the canonical **86-error / 16-source-file** Java frontier until a later exact canonical compile changes it.
4. The smallest evidence-backed non-optional mechanical family now visible is the four-error `MixinServerLevel.java` vocabulary set:
   - `worldChunk.getPos().toLong()` -> `worldChunk.getPos().pack()`;
   - `worldChunk.getMinBuildHeight()` -> `worldChunk.getMinY()`;
   - `knownChunkPosEntry.getKey().toLong()` -> `knownChunkPosEntry.getKey().pack()`;
   - `ChunkPos.asLong(chunkX, chunkZ)` -> `ChunkPos.pack(chunkX, chunkZ)`.
   Exact 26.2 replacements are already independently proven by canonical `ChunkPos.pack()` and `getMinY()` overlays. Before mutation, inspect the **post-canonical** `MixinServerLevel` state because frozen DistanceManager/TicketStorage and ship-chunk lifecycle overlays also touch this file. If exact anchors prove these four expressions remain purely vocabulary-level, apply only these four replacements fail-closed and assert that all ticket-storage membership, SHIP_CHUNK add/remove lifecycle, load/unload ordering, terrain update, wing scan, and shipyard keep-loaded semantics are unchanged. Do not alter any ticket predicate while making this mechanical patch.
5. Do **not** patch the one-error `MixinEntity.entityInside`, `MixinLivingEntity.isControlledByLocalInstance`, or `MixinMinecraftServer.removeRegionTicket` units without separate exact lifecycle/authority evidence; they touch collision/effects, local-control authority, or frozen ticket lifecycle.
6. `MixinLocalPlayer` packet constructors now require an additional boolean in all four packet variants; do not guess that boolean. Probe exact 26.2 packet semantics/field meaning before adaptation because this is entity movement/network authority.
7. Do not bulk-port optional compat (`Immersive Portals`, FTB Chunks, OptiFine/Sodium) merely to reduce error count. Establish target-runtime optionality/dependency evidence before isolation or compatibility work.
8. `MixinClientChunkCache`, `MixinLevelChunk`, `MixinClientLevel`, and `MixinClientPacketListener` contain mixed API/lifecycle changes; split them into separately evidenced semantic units rather than file-wide rewrites.
9. After any bounded mutation, run exact canonical standalone P1 compile, classify the new primary frontier from the uploaded artifact, then update this ledger only at a meaningful proven boundary.
10. Remain P1. No ordinary compile/debug video.
