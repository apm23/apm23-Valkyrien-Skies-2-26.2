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

- upstream repository: `ValkyrienSkies/Valkyrien-Skies-2`
- selection branch: `1.21.1/main`
- exact commit: `f39132148e717d325933b4ce6e9e9fb13d929390`
- exact root tree: `91116399605d3ecd1c93b0011560e09281ee1fa4`
- upstream mod version: `2.4.12`
- imported as gitlink/submodule `upstream-vs2/`

Minecraft 26.2 changes are applied by explicit fail-closed overlays. Every core subsystem remains traceable to upstream VS2 or to a documented minimal 26.2 adaptation feeding existing VS2 architecture.

## Current reconciliation — 2026-09-20 P1 Java/API frontier

### Canonical implementation proof

- canonical implementation/proof HEAD: `1860dc3863c2151320eb18f7ab9b161f5ae7f551` — `ci: chain LevelChunk blending data invariant overlay`.
- semantic invariant helper: `1554f25f13258fd33e18fa8847f3bfb4bc6d6967` — `fix: guard LevelChunk blending data invariant on 26.2`.
- exact-head P0 provenance run `35519773694`: **success**.
- exact-head canonical P1 compile run `35519773646`: reached primary javac; compile-frontier failure only.
- compile artifact `p1-compile-log-1860dc3863c2151320eb18f7ab9b161f5ae7f551`, ID `10607928437`, digest `sha256:404279544d035f211e688642b41e2a44b46b381592c3924e7801b49f374615ad`.
- extracted `p1-compile.log`: **238067 bytes**, SHA-256 `3eac3e8b71d4ccd013e2e9f56d6b4b6953027bf253155f10e026116313fa6c24`.
- authoritative first primary `:common:compileJava` pass: **51 errors across 7 Java source files**.
- `MixinLevelChunk.java` is absent from that entire first primary error pass.
- project state: `P1_SOURCE_API_ADAPTATION_IN_PROGRESS`.
- active blocker classification: `MINECRAFT_26_2_RENDERER_DIRTY_INVALIDATION_AUTHORITY`.
- This is not P1 boot proof, not P2/M1 ship proof, and not runtime rendering proof.

### Current primary Java frontier at `1860dc3863...`

1. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/immersive_portals/MixinMyBuiltChunkStorage.java` — 25
2. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/vanilla_renderer/MixinViewAreaVanilla.java` — 14
3. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/vanilla_renderer/MixinLevelRendererVanilla.java` — 3
4. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/immersive_portals/MixinImmPtlChunkTracking.java` — 3
5. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/optifine_vanilla/MixinLevelRenderer.java` — 3
6. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/ftb_chunks/MixinClaimedChunkManagerImpl.java` — 2
7. `common/src/main/java/org/valkyrienskies/mod/mixin/client/world/MixinClientChunkCache.java` — 1

The first primary diagnostic is mandatory/core `MixinClientChunkCache.java:166`: the pinned VS2 ship-render section invalidation call `renderSection.setDirty(true)` no longer exists on Minecraft 26.2 `SectionRenderDispatcher.RenderSection`.

Optional compat is **not** the first target merely because it owns most remaining errors. Resolve the core `MixinClientChunkCache` renderer-authority boundary first.

## Proven frontier progression — frozen at P1 compile/API scope

1. `MixinServerLevel` chunk-key/build-height vocabulary: **86 -> 82**.
2. optional legacy Sodium chunk-tracker bridge isolation: **82 -> 80**; standalone P1 vanilla renderer remains authority.
3. `MixinEntity.entityInside` 26.2 effect collector adaptation: **80 -> 79**; upstream VS2 ship-space scan still feeds vanilla effect collection.
4. `MixinLivingEntity` local-instance authority vocabulary: **79 -> 78**; dragging/interpolation authority unchanged.
5. `MixinLocalPlayer` movement packet constructors: **78 -> 74**; VS2 packet/transform path retained.
6. `MixinClientChunkCache` packed keys + packet-heightmap API: **74 -> 66**.
7. `MixinClientChunkCache` section-height range: **66 -> 64**; corrected guard at `8dea5dfb0e2df52fbf7440abfa6e69b88c94846b`.
8. `MixinMinecraftServer` shutdown SHIP_CHUNK ticket removal: **64 -> 63**, commit `fc887ec127899ba1437433ebf77ee6fc968c82ab`, proof `35510099480`.
9. `MixinClientLevel` two-hand creative-barrier API: **63 -> 62**, proof head `486dbdaec5302f983d76bd871dea4e59eac67479`.
10. `MixinClientLevel` base standing dimensions API: **62 -> 61**, proof `35511223209`; do not use scale-aware dimensions here.
11. `MixinClientPacketListener` packet-created entity creation API: **61 -> 60**, proof head `d0bf1efc8ae705ba0aa1f88e7c64be79db3e365b`.
12. `MixinClientPacketListener` packet-position `moveTo -> snapTo`: **60 -> 59**, proof `35512025153`; explicit VS2 mounting/network ordering preserved.
13. `MixinLevelChunk` dirty-save marking: **59 -> 57**; direct `unsaved=true` became public `markUnsaved()` only. Proof `35514352664`.
14. `MixinLevelChunk` empty-section construction: **57 -> 53**; registry context became `palettedContainerFactory()`. Proof `35515573624`.
15. `MixinLevelChunk` serialized parse factory: **53 -> 52**; `SerializableChunkData.parse` second argument became `level.palettedContainerFactory()`. Proof `35516856204` at `b7104b6e1796fa498f1e7782ebfcc899e771b3fe`.
16. `MixinLevelChunk` final `BlendingData` ownership: **52 -> 51** and `MixinLevelChunk` becomes compile-clean. Pinned VS2's illegal post-construction assignment is replaced only by a fail-closed invariant requiring both source deserialized and live destination shipyard `BlendingData` to be null. All other original VS2 live-copy state and authority remain unchanged. Exact proof: `1860dc3863c2151320eb18f7ab9b161f5ae7f551`, P0 `35519773694`, P1 `35519773646`, artifact `10607928437`.

Freeze all sixteen units above. Runtime semantics remain to be proven later by normal P1/P2 gates.

## LevelChunk blending-data boundary — resolved invariant and locked negative evidence

Exact mapped 26.2 evidence established:

- `ChunkAccess.blendingData` is `final` and constructor-owned.
- `LevelChunk`/`ProtoChunk` receive `BlendingData` during construction; no mapped setter exists.
- vanilla `LevelChunk(ServerLevel, ProtoChunk, ...)` forwards `ProtoChunk.getBlendingData()` at construction.
- pinned VS2 `moveTerrainAcrossDimensions(...)` instead live-copies into an already-existing destination `LevelChunk`.

The bounded lifecycle investigation established that hot replacement is not a legitimate local one-line substitute:

- ownership probe HEAD `df2722ced726e73d5fe70b2290225d664860cfd8`, P0 `35517373180`, probe `35517373126`, artifact `10607406974`.
- live-replacement probe HEAD `cd1b1c8988089adcece9a379a6aeec31df74a796`, run `35517757678`, artifact `10607197727`: no public safe live `LevelChunk` hot-swap path; `GenerationChunkHolder.replaceProtoChunk(...)` is promotion-only.
- promotion probe HEAD `0ed859be21b7efe367051855b91950b1e9d8f2cb`, P0 `35518028363`, probe `35518028364`, artifact `10607157900`: `ChunkStatusTasks.full(...)` constructs the `LevelChunk` during ProtoChunk -> FULL promotion, then performs load/registration lifecycle.
- unload/reload probe HEAD `5e976d7bac63a5c840f7fb3b668ad21ca32d6e43`, P0 `35518330927`, run `35518330932`, artifact `10607372557`, digest `sha256:2772a01e9d92ecb9cc58452ff7b696de90986ea0485987cb7ef66901a79ba2a9`: ticket drop moves holder to pending unload; actual save/unload occurs asynchronously only after `getSaveSyncFuture()` completion.
- therefore synchronous `remove + immediate getChunk()` is not a valid vanilla reconstruction path.

Why the final invariant is legitimate and smaller than a lifecycle rewrite:

- normal VS2 shipyard chunks are created through empty ProtoChunk construction with `BlendingData=null`.
- pinned upstream VS2 bypasses/cancels the relevant shipyard worldgen stages.
- in 26.2 the field is final, so a normal live shipyard chunk cannot later acquire a different blending-data object.
- helper `apply_p1_levelchunk_blendingdata_invariant_26_2.py` removes only the now-illegal null-to-null field assignment and throws if either source or destination ever carries non-null blending data. It does **not** silently drop non-null metadata.
- this preserves pinned upstream's current live-copy design introduced by upstream portal work rather than reviving the older storage-write/unload design.

Do not reopen with `@Mutable`, reflection, unsafe/accessor final writes, private-future mutation, duplicate storage, silent assignment deletion, stale destination metadata, or synchronous forced unload/reload.

## Current renderer dirty-invalidation investigation

- exact compile `35519773646` proves the first current error is `MixinClientChunkCache.java:166`, `RenderSection.setDirty(boolean)` missing.
- initial exact-classpath probe HEAD `8db9a7cbf8c909609b3078010d6866d6ef70ecd1`, run `35520170375`, artifact `10608013620`, digest `sha256:7926c30c1acddad20b778b962c13cdf41f30945cb29f088f35974f282a13c95a`.
- extracted first probe log: **36839 bytes**, SHA-256 `c0fe535e85e32b17bbdcfc72643469a00bc05d430ef35d91d068f55f3f9cdc2c`.
- that probe deliberately failed after exact `javap` proved Minecraft 26.2 `SectionRenderDispatcher.RenderSection` has **no dirty-related field or method at all**. It still has section mesh, reset, compileAsync/compileSync, transparency and section-position lifecycle; dirty scheduling authority has moved elsewhere.
- therefore `setDirty(true) -> setDirty()` is a locked failed/mechanical hypothesis and must not be attempted.
- follow-up exact-classpath renderer-authority probe HEAD `ce63c58aacacf18ebc6138e6c11a708a46d552ec`, run `35520379454` is active as of this ledger reconciliation. It inspects exact mapped `ViewArea`, `LevelRenderer`, `LevelExtractor`, `SectionUpdateTracker`, and `RenderSection` candidates for the moved dirty/update authority.
- exact-head P0 for that probe commit: run `35520379433` (check live conclusion before source mutation).

## Frozen architecture-sensitive boundaries

Do not reopen absent direct contradictory evidence:

- real VS2 ship chunk-ticket lifecycle — original boundary `65a42e782de192f27d5bf720691d6e08f395a719`, proof `35450402031`; matching shutdown removal `fc887ec127899ba1437433ebf77ee6fc968c82ab`, proof `35510099480`. Radius/lifetime/type/order frozen.
- DistanceManager / TicketStorage read bridge — `8a338f95103227ed6a5acb35804d573bbae0d96c`, proof head `ca07a2fff0fd922cbbd578a0531d3377313827de`, P0 `35463018487`, proof `35463018541`; **READ ONLY**.
- ShipSavedData persistence — `f2b3ec68e0d2146bb8b443da76a62a4766e01fce`, proof `35451366140`.
- entity local authority / interpolation — `b7e583af13598b6ddcc583380872f578b8a40bb8`, proof `35455551701`; no synthetic carry.
- entity renderer submit lifecycle — `a87512437f40a3bfa1325d78f8e2588587ec7cc8`, proof `35458380245`.
- shipyard teleport API mapping — proof `35467615790`; real VS2 transforms remain authority, no per-tick chase.
- vanilla renderer bridge — canonical `290e2bb6c1f6248437e4d189dfb4a01e82a31e33`; ship-aware distance, loaded-ship iteration, transformed ship AABB and `VSClientGameUtils.transformRenderWithShip` remain authority.
- LevelRenderer / LevelExtractor split — `660d5320902a3ecba4f3219969aa77b0316cfa52`; existing `IVSCamera` is observation only.
- optional Create deployer helper is P1 compile isolation only, never P3 integration.
- `MixinClientLevel` hand + standing units frozen; no inventory scanning or scale-aware replacement.
- `MixinClientPacketListener` creation/snap units frozen; no `setPos` chase, no alternate spawn reason, no packet-order redesign.
- all `MixinLevelChunk` units listed above are frozen; retain live-copy/tick-container/block-entity/heightmap/light/save ordering.

Forbidden final architecture remains: custom VS2-like reference frames, synthetic carry/inertia, fake gravity, manual wall/floor/ceiling clamps, per-tick teleport/setPos chase, camera counter-rotation/forcing, duplicate authority, floor-only fake success, or implementation reuse from retired `apm23/VS2-Create_Interactive`.

## Locked negative evidence

- `3bcbf90c75dc4d02448cfdb4590cc9c9674e0ed6` / `35454717409`: wrong Kotlin source-set exclusion for `DeployerScrollOptionSlot`.
- `a72aaef8eca34a352ef949eeb57e6bbcda81171f`: `setUnsaved(false)` invalid current API.
- VSKeyBindings failed probes: `e108526cbd728454c175c76bffc610d4e074da49`, `fcc65187d79c4b546883875da3597345db1e01cd`, `e9a3efd58acb2af9539628eb2875e6cb829c3cec`, `fb3c7e65a4c2089f6fa695114734d14836bde1d3`.
- pathfinding `b3927e625acf40edbf517970ebc952a104a20c97` / `35493933563`: parser/assertion-only failure.
- renderer proof `35497975815` / `35498155312`: broad substring `Uniform` falsely matched valid `DynamicUniforms`; never replay that guard.
- ChunkMap retrigger `6ce41dfbef36b8c8021f48f52f0020e7b1131d5f`: wrongly targeted nonexistent `getById(arg.toLong())`; never replay.
- LivingEntity authority and move-player first helpers had overly narrow occurrence guards; harness-only failures, later compile-green.
- ClientChunkCache section-range first guard at `4f7a8461508a55d1c204eaf08343f6af01e32d14` expected one loop but source legitimately has two; corrected at `8dea5dfb0e2df52fbf7440abfa6e69b88c94846b`.
- ClientLevel hand transport `587c6b41d2a95815d26440ee753abc0f70faecb6` / `35510733124` invoked helper twice; later corrected without semantic change.
- `player.getDimensions(Pose.STANDING)` is a locked failed standing-width hypothesis; retain proven `getDefaultDimensions(Pose.STANDING)` mapping.
- LevelChunk dirty-mark and parse-factory first failures were helper-guard-only, not semantic failures; preserve their later corrected frozen units.
- LevelChunk direct final-field mutation and synchronous hot replacement/unload are locked failed hypotheses as documented above.
- renderer `RenderSection.setDirty(true) -> setDirty()` is locked failed: exact 26.2 RenderSection has no dirty member.
- Actions self-push workflow edits without `workflows` permission remain a failed transport hypothesis.
- retired `apm23/VS2-Create_Interactive` implementation is forbidden.

## Target runtime baseline

Exact `BASELINE_LOCK.json` remains authoritative:

- Minecraft `26.2`
- Java `25`
- Fabric Loader observed `0.19.3`
- Fabric API `0.160.0+26.2`, SHA-256 `5f3dff88e1661166e222213302b25ace6c36dc3683804cbd4b5acf93138ea05e`
- Create Fly `6.0.9-1`, SHA-256 `d9c6cb6116d5caa1174a289ecd7d3cdd463ccef6e8db1249ab0bcfcd8c935870`
- SNR embedded `SNR.FLY-STABLE-1.2.2+fabric-mc26.2`, SHA-256 `33c87d5a7da0d468d3b6c0e99f726b835c63b693e7447fdaeca5e1f204caab84`
- Copycats embedded `3.0.7-createfly+mc.26.2-v1.14`, SHA-256 `1922db10a49dfab42c4c272fbaee41cdc149287cd08ca84148b497e598029858`

Create/SNR/Copycats are not authority for current standalone P1 work and must not enter the active frontier prematurely.

## Phase gates

- P0 provenance/import: maintained by exact-head provenance workflow.
- P1 standalone real VS2 source/API/boot: **in progress**. Java compile frontier remains.
- P2/M1 standalone real VS2 ship: not entered; `M1_COMPLETE` forbidden.
- P3 Create Fly bridge: not entered.
- P4 SNR + Copycats: not entered.
- P5/final: not entered.
- `FINAL_READY` requires exact-final-JAR real-user runtime acceptance; CI alone can never authorize it.
- video is closure-only and never ordinary compile/debug instrumentation.

## next_safe_action

1. Reconcile actual GitHub HEAD and read this file completely before acting.
2. Preserve all sixteen frozen P1 units and all locked negative evidence.
3. Treat `1860dc3863c2151320eb18f7ab9b161f5ae7f551` / P0 `35519773694` / canonical compile `35519773646` / artifact `10607928437` as the authoritative **51-error / 7-source-file** implementation proof until a later exact canonical compile changes it.
4. Reconcile the active renderer-authority probe `35520379454` at HEAD `ce63c58aacacf18ebc6138e6c11a708a46d552ec` plus exact-head P0 `35520379433`. If still active, HOLD; do not stack source patches.
5. If the probe completes, inspect its actual artifact/bytecode and identify the exact Minecraft 26.2 owner/method that replaces old per-`RenderSection` dirty scheduling. Preserve the pinned VS2 intent: invalidate the custom ship render sections around the newly loaded ship chunk after relight and before `level.onChunkLoaded(pos)`.
6. Do **not** mechanically call `RenderSection.reset`, `compileAsync`, `compileSync`, or a guessed dirty method. Do not move renderer authority into a custom system. Use the current vanilla 26.2 invalidation owner only if exact ownership/access and section-coordinate semantics are proven.
7. If a smallest legitimate mapping for the one mandatory `MixinClientChunkCache` site is proven, implement it as one fail-closed overlay, chain it canonically, then run exact-head P0 + canonical standalone P1 compile. Expected clean outcome is removal of that one core diagnostic; classify the new first primary error from the uploaded artifact instead of guessing.
8. Optional compat (`Immersive Portals`, FTB Chunks, OptiFine) remains secondary while the mandatory core site is unresolved.
9. Remain P1. No Create/SNR/Copycats integration and no ordinary compile/debug video.
