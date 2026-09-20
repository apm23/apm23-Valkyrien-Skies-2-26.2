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

## Current reconciliation — 2026-09-20 P1 Java API frontier

Current proven source implementation boundary:

- canonical implementation/proof HEAD: `b7104b6e1796fa498f1e7782ebfcc899e771b3fe` — `ci: chain LevelChunk serialized parse factory overlay`.
- semantic helper commit: `22c6668c8a02d98fcabaa334220a85b586a9d1bd` — `fix: port LevelChunk serialized parse factory to 26.2`.
- helper guard-only correction: `02dd62e7705e42b320ab673b808d697fc741a6cb` — `ci: align LevelChunk parse helper guard with canonical source`; this was harness-only and did not change the semantic adaptation.
- exact-head P0 provenance run `35516856165`: **success**.
- exact-head standalone P1 compile run `35516856204`: **compile-frontier failure only** after the canonical overlay chain reached javac.
- canonical compile artifact: `p1-compile-log-b7104b6e1796fa498f1e7782ebfcc899e771b3fe`, ID `10607530237`, digest `sha256:6a9035938d523d9ec6aae0a6976101836ab26aa8ad091ae30227d5ec111f5176`.
- extracted `p1-compile.log`: **235530 bytes**, SHA-256 `b6b2d5b542919de810ac8e2241a8d540d4c07df8f2a99d73aa80ebd25e99a538`.
- authoritative first primary javac pass: **52 errors across 8 Java source files**. Later Gradle repeats are not frontier authority.

Current ownership-boundary evidence after that compile:

- documentation freeze commit `67e1cf5fde706e8f673a7758969d2e5725378fe8`; exact-head P0 run `35517338549`: **success**.
- ownership-probe HEAD `df2722ced726e73d5fe70b2290225d664860cfd8` — `ci: inspect LevelChunk blending data ownership`.
- exact-head P0 provenance run `35517373180`: **success**.
- exact mapped ownership probe run `35517373126`: **success**.
- ownership artifact `p1-levelchunk-blendingdata-ownership-probe-df2722ced726e73d5fe70b2290225d664860cfd8`, ID `10607406974`, digest `sha256:4bca5d6470869e95b1d9963d2977c6eb13734c549e8d4d524540234c3151cc8b`.
- extracted classpath log: **30709 bytes**, SHA-256 `80fa2200aeaa7d52d9e0460388eee69a1a026d49cf5009017745401138612ffb`.
- extracted ownership probe log: **428831 bytes**, SHA-256 `f8e0ad29d2ee5cd6ee63a99c4932ad7a04cbf006ac4188ff2d01a8c955fba72b`.
- project state: `P1_SOURCE_API_ADAPTATION_IN_PROGRESS`.
- active blocker classification: `MINECRAFT_26_2_LEVELCHUNK_BLENDING_OWNERSHIP_BOUNDARY`.
- This is not P1 boot proof, not P2/M1 ship proof, and not runtime rendering proof.

### Artifact metadata correction for the preceding 59-error boundary

The 59-error count at implementation head `8653eb7b9c4d0db62e04614c744aac1810255d75` remains valid, but an earlier ledger copied incorrect artifact metadata. GitHub live artifact metadata and the downloaded archive establish the corrected values:

- run `35512025153`, artifact ID `10605932626`.
- artifact digest: `sha256:259db4d42ab3e5e85f1d9847f3ea22ae17a60c1ffdbddfe4607190095b283be2`.
- extracted `p1-compile.log`: **246264 bytes**, SHA-256 `5135b5b93e1a565fc4eb88bea8cd84013a1c50d5d20d3821977a2625faf3d3d7`.
- authoritative first primary javac pass: **59 errors / 8 files**.

Do not restore the superseded incorrect digest/size/hash from the earlier ledger revision.

### Proven frontier progression

1. `MixinServerLevel` chunk-key/build-height vocabulary: **86 -> 82**. Exact four-site adaptation only; TicketStorage predicates, SHIP_CHUNK lifecycle, load/unload ordering, terrain updates, wing scan, and shipyard keep-loaded authority preserved.
2. optional legacy Sodium chunk-tracker bridge isolation: **82 -> 80**. Standalone P1 does not include Sodium; only obsolete optional callbacks/imports were isolated. Vanilla VS2 rendering remains authority.
3. `MixinEntity.entityInside` 26.2 effect collector adaptation: **80 -> 79**. Real upstream VS2 ship-space scan feeds vanilla inside-block effect collection; no duplicate authority.
4. `MixinLivingEntity` local-instance authority vocabulary: **79 -> 78**. Dragged-entity ship lookup/interpolation authority unchanged.
5. `MixinLocalPlayer` movement-packet constructors: **78 -> 74**. Current packet variants forward vanilla horizontal-collision state while retaining VS2 ship-motion packet/transform paths.
6. `MixinClientChunkCache` packed keys plus packet-heightmap API: **74 -> 66**. Vocabulary/parameter adaptation only; packet decode, relight, terrain connectivity, ship lifecycle, renderer selection, and `onChunkLoaded` ordering unchanged.
7. `MixinClientChunkCache` section-height range: **66 -> 64**. Preserved pinned upstream exclusive range as current inclusive min/max-Y vocabulary. Earlier loop-count failure was harness-only; corrected at `8dea5dfb0e2df52fbf7440abfa6e69b88c94846b`.
8. `MixinMinecraftServer` shutdown SHIP_CHUNK ticket removal: **64 -> 63**. `fc887ec127899ba1437433ebf77ee6fc968c82ab` extends the proven radius-ticket mapping to the missed shutdown callsite only; proof `35510099480`.
9. `MixinClientLevel` creative barrier two-hand API: **63 -> 62**. `getHandSlots()` became explicit main/off-hand reads; ship transforms and particle/reference-space behavior unchanged. Proof `35510781654` at `486dbdaec5302f983d76bd871dea4e59eac67479`.
10. `MixinClientLevel` canonical standing-width API: **62 -> 61**. Uses the proven base standing dimensions boundary via `getDefaultDimensions(Pose.STANDING)`, not scale-aware `getDimensions`. Exact compile `35511223209` removes `MixinClientLevel` from the primary error set.
11. `MixinClientPacketListener` packet-created mounting-entity creation API: **61 -> 60**. Exact 26.2 packet-spawn creation uses `EntitySpawnReason.LOAD`; real VS2 mounting-entity authority and packet ordering preserved. Proof head `d0bf1efc8ae705ba0aa1f88e7c64be79db3e365b`.
12. `MixinClientPacketListener` packet-position initialization vocabulary: **60 -> 59**. The old three-double `moveTo` call maps to current `snapTo` at the same packet-position stage; explicit codec sync, rotation, id/UUID, addEntity, teleport handling, spawn reason, cancellation, and real VS2 mounting authority remain unchanged. Exact compile `35512025153` removes `MixinClientPacketListener` entirely.
13. `MixinLevelChunk` dirty-save marking: **59 -> 57**. Minecraft 26.2 makes `ChunkAccess.unsaved` private and exposes public `markUnsaved()`, whose state transition is `unsaved = true`. The fail-closed overlay replaces exactly the two pinned VS2 post-operation direct assignments after `clearChunk()` and `copyChunkFromOtherDimension()` with `this.markUnsaved()`. Block-entity clearing, tick-container unregister/register ordering, sections/heightmaps, light state, deserialization/copy flow, structure data, blending data, and ship lifecycle are unchanged. Exact compile `35514352664` removes exactly the two private-field diagnostics; `MixinLevelChunk` drops **8 -> 6** with no new primary diagnostic.
14. `MixinLevelChunk` empty-section construction: **57 -> 53**. Pinned VS2's two biome-registry contexts and two `LevelChunkSection(Registry<Biome>)` constructors map to Minecraft 26.2's `level.palettedContainerFactory()` and `LevelChunkSection(PalettedContainerFactory)`. The helper changes exactly the two null-fill sites in `clearChunk()` and `copyChunkFromOtherDimension()` and removes only the now-unused Registry/Biome imports. Section count, null checks, copy ordering, tick-container lifecycle, heightmaps, light state, dirty marking, `SerializableChunkData.parse(...)`, `blendingData`, and all ship lifecycle/reference-space authority remain unchanged. Exact compile `35515573624` removes exactly four diagnostics; `MixinLevelChunk` drops **6 -> 2** with no new primary diagnostic.
15. `MixinLevelChunk` serialized parse factory context: **53 -> 52**. Minecraft 26.2 `SerializableChunkData.parse(...)` requires a `PalettedContainerFactory` as its second argument; the fail-closed helper changes only `level.registryAccess()` to `level.palettedContainerFactory()` at the pinned VS2 copy/deserialization site. Serialized tag, `.read(...)` parameters, copy ordering, sections, tick containers, heightmaps, light state, dirty marking, final blending-data ownership, and all real VS2 ship lifecycle/reference-space authority remain unchanged. Exact compile `35516856204` removes exactly the parse-context diagnostic; `MixinLevelChunk` drops **2 -> 1** with no new primary diagnostic. The first helper guard mismatch was harness-only and was corrected by `02dd62e7705e42b320ab673b808d697fc741a6cb` before canonical chaining.

Freeze all fifteen units above at P1 compile/API scope. Runtime semantics remain to be proven later by normal P1/P2 gates.

### Current primary Java frontier at `b7104b6e...`

1. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/immersive_portals/MixinMyBuiltChunkStorage.java` — 25
2. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/vanilla_renderer/MixinViewAreaVanilla.java` — 14
3. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/vanilla_renderer/MixinLevelRendererVanilla.java` — 3
4. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/immersive_portals/MixinImmPtlChunkTracking.java` — 3
5. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/optifine_vanilla/MixinLevelRenderer.java` — 3
6. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/ftb_chunks/MixinClaimedChunkManagerImpl.java` — 2
7. `common/src/main/java/org/valkyrienskies/mod/mixin/client/world/MixinClientChunkCache.java` — 1
8. `common/src/main/java/org/valkyrienskies/mod/mixin/world/chunk/MixinLevelChunk.java` — 1

`MixinServerLevel`, `SodiumCompat`, `MixinEntity`, `MixinLivingEntity`, `MixinLocalPlayer`, `MixinMinecraftServer`, `MixinClientLevel`, and `MixinClientPacketListener` are zero-error in the primary javac pass. `MixinClientChunkCache` remains intentionally at one unresolved ship-render dirty-invalidation error.

### LevelChunk final blending-data ownership boundary

The only remaining `MixinLevelChunk` diagnostic is:

- `this.blendingData = protoChunk.getBlendingData()`: `ChunkAccess.blendingData` is final in Minecraft 26.2.

Exact mapped 26.2 bytecode from the canonical P1 compile classpath proves:

- `ChunkAccess` declares `protected final BlendingData blendingData`.
- `ChunkAccess`'s constructor receives `BlendingData` and performs the field write there.
- `LevelChunk(Level, ChunkPos, UpgradeData, LevelChunkTicks, LevelChunkTicks, long, LevelChunkSection[], PostLoadProcessor, BlendingData)` forwards the supplied value into `ChunkAccess` construction.
- vanilla `LevelChunk(ServerLevel, ProtoChunk, PostLoadProcessor)` calls `ProtoChunk.getBlendingData()` and forwards that value into the constructor above.
- `ProtoChunk` likewise receives blending data at construction.
- no mapped `setBlendingData` method exists in the inspected `ChunkAccess` / `LevelChunk` / `ProtoChunk` boundary.
- `SerializableChunkData.read(...)` unpacks persisted blending data before constructing either `LevelChunk` or `ProtoChunk`; vanilla ownership is therefore construction-time, not post-construction reassignment.

Pinned VS2's real dimension-transfer path is materially different from vanilla construction ownership:

- `MixinMinecraftServer.moveTerrainAcrossDimensions(...)` obtains an already-live destination `LevelChunk` via `destLevel.getChunk(x, z)` and then calls `VSLevelChunk.copyChunkFromOtherDimension(...)` on that existing object.
- immediately before that, `VSServerLevel.removeChunk(x, z)` is called with an upstream comment explicitly calling the sequence a hack intended to fix destination-level state.
- pinned `MixinServerLevel.removeChunk(...)` only removes the chunk position from VS's private `vs$knownChunks` tracking map; it does **not** evict or replace the vanilla `LevelChunk` object in `ServerChunkCache` / `ChunkHolder`.
- therefore vanilla's legitimate constructor path cannot be substituted locally inside `MixinLevelChunk.copyChunkFromOtherDimension(...)`: replacing the live chunk requires an independently proven server chunk-holder/cache lifecycle boundary.

This evidence rejects a mechanical final-field workaround. Do not use `@Mutable`, reflection, accessor writes, duplicate blending storage, unsafe/final-field mutation, silently drop the assignment, or preserve stale destination blending data without semantic proof.

## Frozen architecture-sensitive boundaries

Do not reopen absent direct contradictory evidence:

- real VS2 ship chunk-ticket lifecycle — original boundary `65a42e782de192f27d5bf720691d6e08f395a719`, proof `35450402031`; matching shutdown removal `fc887ec127899ba1437433ebf77ee6fc968c82ab`, compile proof `35510099480`. Radius/lifetime/type/order remain frozen.
- DistanceManager / TicketStorage read bridge — `8a338f95103227ed6a5acb35804d573bbae0d96c`, proof head `ca07a2fff0fd922cbbd578a0531d3377313827de`, P0 `35463018487`, proof `35463018541`; **READ ONLY**.
- ShipSavedData persistence — `f2b3ec68e0d2146bb8b443da76a62a4766e01fce`, proof `35451366140`.
- entity local authority / interpolation — `b7e583af13598b6ddcc583380872f578b8a40bb8`, proof `35455551701`; no synthetic carry.
- entity renderer submit lifecycle — `a87512437f40a3bfa1325d78f8e2588587ec7cc8`, proof `35458380245`.
- shipyard teleport API mapping — proof `35467615790`; real VS2 transform authority, no per-tick teleport chase.
- vanilla renderer bridge — canonical `290e2bb6c1f6248437e4d189dfb4a01e82a31e33`; real VS2 ship-aware distance, loaded-ship iteration, transformed ship AABB, and `VSClientGameUtils.transformRenderWithShip` remain authority.
- LevelRenderer / LevelExtractor split — `660d5320902a3ecba4f3219969aa77b0316cfa52`; existing `IVSCamera` is observation only.
- optional Create deployer helper is P1 compile isolation only, never P3 Create integration.
- `MixinClientLevel` two-hand barrier read and base-standing-width adaptations are frozen at proof heads `486dbdaec5302f983d76bd871dea4e59eac67479` and `4e880e6271c9fa79001df9d3077086c4dda6530f`; do not broaden to inventory scanning, scale-aware dimensions, or particle/reference-space redesign.
- `MixinClientPacketListener` creation + snap units are frozen through `8653eb7b9c4d0db62e04614c744aac1810255d75`; do not substitute `setPos`, `setPosRaw`, whole `recreateFromPacket`, another spawn reason, or alter the explicit packet ordering.
- `MixinLevelChunk` dirty-save unit is frozen through `e6a4ed6b6310d2780e0196881393f10e70a0f5eb`; use the public `markUnsaved()` state transition only. Do not revive `setUnsaved(false)` or direct-field access.
- `MixinLevelChunk` empty-section factory unit is frozen through `f4333069216e177654ff3a41ec3ecafe034904cb` (semantic helper `a019168466fe13f0e6d9375575cad5123da9d0dd`, proof `35515573624`). Do not restore biome-registry construction or broaden this unit into parse/blending ownership.
- `MixinLevelChunk` serialized parse factory unit is frozen through `b7104b6e1796fa498f1e7782ebfcc899e771b3fe` (semantic helper `22c6668c8a02d98fcabaa334220a85b586a9d1bd`, guard correction `02dd62e7705e42b320ab673b808d697fc741a6cb`, compile proof `35516856204`). Do not restore `RegistryAccess` as the parse context or broaden this unit into final blending-data ownership.

Forbidden final architecture remains: custom VS2-like reference frames, synthetic carry/inertia, fake gravity or wall/floor clamps, per-tick setPos chase, camera counter-rotation/forcing, duplicate authority, floor-only fake success, or reuse of retired `apm23/VS2-Create_Interactive` implementation code.

## Locked negative evidence

- `3bcbf90c75dc4d02448cfdb4590cc9c9674e0ed6` / `35454717409`: wrong Kotlin source-set exclusion for `DeployerScrollOptionSlot`.
- `a72aaef8eca34a352ef949eeb57e6bbcda81171f`: `setUnsaved(false)` invalid current API.
- VSKeyBindings failed probes `e108526cbd728454c175c76bffc610d4e074da49`, `fcc65187d79c4b546883875da3597345db1e01cd`, `e9a3efd58acb2af9539628eb2875e6cb829c3cec`, `fb3c7e65a4c2089f6fa695114734d14836bde1d3`.
- pathfinding `b3927e625acf40edbf517970ebc952a104a20c97` / `35493933563`: parser/assertion-only failure.
- renderer helper/proof `35497975815` and `35498155312`: broad substring `Uniform` falsely matched valid `DynamicUniforms`; never replay broad guard.
- ChunkMap retrigger `6ce41dfbef36b8c8021f48f52f0020e7b1131d5f`: helper wrongly targeted nonexistent `getById(arg.toLong())`; never replay.
- LivingEntity first authority helper expected one `getLastShipStoodOn()` but source legitimately had two; harness-only failure, later compile-green.
- move-player first helper guard expected one transform/networking anchor but source legitimately had player + vehicle paths; harness-only failure, later compile-green.
- ClientChunkCache section-range guard at `4f7a8461508a55d1c204eaf08343f6af01e32d14` expected one `dx/dz` loop but source has two; corrected at `8dea5dfb0e2df52fbf7440abfa6e69b88c94846b` and later compile-green.
- Do not replace remaining `RenderSection.setDirty(true)` mechanically with a vanilla dirty call. It targets a section obtained through `IVSViewAreaMethods.vs$getShipRenderSection(...)`; exact ship-render invalidation ownership/access must be proven before mutation.
- ClientLevel hand-overlay transport `587c6b41d2a95815d26440ee753abc0f70faecb6` / `35510733124` invoked the hand helper twice and failed its idempotence guard before javac; `486dbdaec5302f983d76bd871dea4e59eac67479` removed only the duplicate call.
- `player.getDimensions(Pose.STANDING)` is a locked failed/forbidden standing-width hypothesis for this site; use the proven base-standing `getDefaultDimensions(Pose.STANDING)` mapping only.
- LevelChunk dirty-mark first chain at `bc2825456b124096b7845bbc4654082e5379902e`, StructureTemplate proof `35514218070`, failed before javac because its helper wrongly expected both direct `unsaved` assignments to be immediately adjacent to `registerTickContainerInLevel(...)`. Pinned upstream has one such site separated by a blank line. `37514ff84a4b7233b6f347fbac1d30105430fcd9` corrected only the fail-closed guard; `e6a4ed6b6310d2780e0196881393f10e70a0f5eb` retriggered the watched chain and proved **57 errors / 8 files**. Never treat `35514218070` as semantic failure.
- LevelChunk parse-factory first helper guard expected a line break between `parse(...)` and `.read(...)`, while the canonical overlay source had the call on one line. This was harness-only; `02dd62e7705e42b320ab673b808d697fc741a6cb` corrected the guard before the helper entered the canonical chain. Never treat it as semantic failure.
- LevelChunk `blendingData` is a locked non-mechanical boundary: the exact mapped field is final and construction-owned. Do not replay direct assignment with `@Mutable`, accessors, reflection/unsafe, duplicate storage, assignment removal, or stale destination-state retention merely to make javac pass.
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
2. Preserve all frozen boundaries and negative evidence above.
3. Treat artifact `10607530237` as the canonical **52-error / 8-source-file** Java compile frontier until a later exact canonical compile changes it.
4. Treat ownership probe `35517373126` / artifact `10607406974` as authoritative evidence that 26.2 `blendingData` is constructor-owned and final; do not attempt another one-line `MixinLevelChunk` field patch.
5. Keep `MixinClientChunkCache`'s one ship-specific dirty-invalidation error untouched unless its custom ship-render ownership path is independently proven.
6. Enter a bounded `ROOT_REDESIGN` investigation of the **existing upstream VS2 dimension-transfer/chunk-copy boundary**, not a replacement architecture. Inspect exact Minecraft 26.2 `ServerChunkCache`, `ChunkHolder`, `ChunkMap`, and related full-chunk promotion/replacement APIs from the canonical P1 classpath, together with pinned `MixinMinecraftServer.moveTerrainAcrossDimensions`, `VSServerLevel.removeChunk`, and `MixinLevelChunk.copyChunkFromOtherDimension`.
7. Determine whether a legitimate 26.2 path can construct the destination `LevelChunk` from the deserialized `ProtoChunk` (thereby transferring `BlendingData` through vanilla construction) and install it through vanilla chunk lifecycle while preserving VS2 ticketing, tick-container registration, block entities, heightmaps, lighting, terrain updates, save state, and object visibility. Do not mutate source until that lifecycle path is proven.
8. If vanilla exposes no safe live-chunk replacement boundary, inspect the upstream VS2 transfer design for the smallest traceable adaptation; do not invent custom chunk authority and do not silently discard source blending semantics.
9. Optional compat (`Immersive Portals`, FTB Chunks, OptiFine) is not first target merely because it has many errors.
10. After any bounded source mutation, run exact canonical standalone P1 compile, classify the first primary javac pass from the uploaded artifact, and update this ledger at the next meaningful proven boundary.
11. Remain P1. No ordinary compile/debug video.
