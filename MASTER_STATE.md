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

## Current reconciliation — 2026-09-21 P1 Java/API frontier

### Canonical implementation proof

- canonical implementation/proof HEAD: `867cbb01a66c0842e22e831d1be02d42479b92e6` — `ci: prove OptiFine dirty-authority frontier`.
- exact-head P0 provenance run `35529562987`: **success**.
- exact-head canonical P1 compile run `35529562974`: reached primary `:common:compileJava`; compile-frontier failure only.
- compile artifact `p1-compile-log-867cbb01a66c0842e22e831d1be02d42479b92e6`, ID `10611096790`, digest `sha256:ef5dffcae65d0e759bf9fcb0d3aafbdf12fbd5fb120185701413249cb20f55f7`.
- authoritative first primary javac pass: **28 errors across exactly 2 Java source files**.
- `MixinViewAreaVanilla.java`, FTB Chunks compat, and OptiFine compat are absent from the primary error pass.
- project state: `P1_SOURCE_API_ADAPTATION_IN_PROGRESS`.
- active blocker classification: `MAPPINGS_API / IMMERSIVE_PORTALS_COMPAT`.
- This is not P1 boot proof, not P2/M1 ship proof, and not runtime rendering proof.

### Current primary Java frontier at `867cbb01...`

1. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/immersive_portals/MixinMyBuiltChunkStorage.java` — **25 errors**.
2. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/immersive_portals/MixinImmPtlChunkTracking.java` — **3 errors**.

Exact `MixinImmPtlChunkTracking` diagnostics:
- line 31: dependency/mapping access failure through `instance.getCenter().dimension`: `class file for net.minecraft.class_5321 not found`;
- line 43: removed `ServerLevel.getMinBuildHeight()`;
- line 46: removed `ServerLevel.getMaxBuildHeight()`.

The two build-height diagnostics are mechanically independent from the remaining dependency/mapping diagnostic and use an already-frozen 26.2 mapping: lower bound `getMinY()`, exclusive upper bound `getMinY() + getHeight()`.

## Proven frontier progression — frozen at P1 compile/API scope

1. `MixinServerLevel` chunk-key/build-height vocabulary: **86 -> 82**.
2. optional legacy Sodium callbacks isolation: **82 -> 80**; standalone P1 vanilla renderer remains authority.
3. `MixinEntity.entityInside` 26.2 effect collector adaptation: **80 -> 79**.
4. `MixinLivingEntity` local-instance authority vocabulary: **79 -> 78**; dragging/interpolation authority unchanged.
5. `MixinLocalPlayer` movement packet constructors: **78 -> 74**.
6. `MixinClientChunkCache` packed keys + packet-heightmap API: **74 -> 66**.
7. `MixinClientChunkCache` section-height range: **66 -> 64**; exclusive old max became inclusive 26.2 max without changing covered sections.
8. `MixinMinecraftServer` shutdown SHIP_CHUNK ticket removal: **64 -> 63**, commit `fc887ec127899ba1437433ebf77ee6fc968c82ab`, proof `35510099480`.
9. `MixinClientLevel` two-hand creative-barrier API: **63 -> 62**, proof head `486dbdaec5302f983d76bd871dea4e59eac67479`.
10. `MixinClientLevel` base standing dimensions API: **62 -> 61**, proof `35511223209`; retain `getDefaultDimensions(Pose.STANDING)`.
11. `MixinClientPacketListener` packet-created entity creation API: **61 -> 60**, proof head `d0bf1efc8ae705ba0aa1f88e7c64be79db3e365b`.
12. `MixinClientPacketListener` packet-position `moveTo -> snapTo`: **60 -> 59**, proof `35512025153`; VS2 mounting/network ordering preserved.
13. `MixinLevelChunk` dirty-save marking: **59 -> 57**; direct `unsaved=true` became public `markUnsaved()` only. Proof `35514352664`.
14. `MixinLevelChunk` empty-section construction: **57 -> 53**; registry context became `palettedContainerFactory()`. Proof `35515573624`.
15. `MixinLevelChunk` serialized parse factory: **53 -> 52**; `SerializableChunkData.parse` context became `level.palettedContainerFactory()`. Proof `35516856204` at `b7104b6e1796fa498f1e7782ebfcc899e771b3fe`.
16. `MixinLevelChunk` final `BlendingData` ownership: **52 -> 51** and file compile-clean. Exact proof `1860dc3863c2151320eb18f7ab9b161f5ae7f551`, P0 `35519773694`, P1 `35519773646`, artifact `10607928437`.
17. `MixinClientChunkCache` vanilla renderer dirty scheduling: **51 -> 50**, **7 -> 6 files**. `RenderSection.setDirty(true)` is bridged into exact MC26.2 `Minecraft.levelExtractor -> LevelExtractor.setSectionDirty(..., boolean) -> SectionUpdateTracker` via one Mixin invoker, preserving boolean `true` and original VS2 ordering. Proof HEAD `b2e308ff693ef88c091228002f8077b61f01d6d6`; P0 `35522623140`; P1 `35522623113`; artifact `10608463644`.
18. `MixinLevelRendererVanilla` ship-visible section bounds: **50 -> 47**, **6 -> 5 files**. `getMinSection()` / exclusive `getMaxSection()` became `getMinSectionY()` / inclusive `getMaxSectionY()` with `<=`. Proof HEAD `dcf4a14e09c9c67ca7bf51ba3552027b2a7e80cf`; P0 `35523910648`; P1 `35523910705`; artifact `10609192424`.
19. `MixinViewAreaVanilla` ship-section array index origin: **47 -> 44**, file **14 -> 11**. Three `getMinSection()` calls became `getMinSectionY()`. Proof HEAD `9405f49a9bd5c348a12098fb9e983b62712f16fe`; P0 `35524343843`; P1 `35524343861`; artifact `10609430640`.
20. `MixinViewAreaVanilla` packed ship-chunk keys: **44 -> 39**, file **11 -> 6**. Five `ChunkPos.asLong(x,z)` became `ChunkPos.pack(x,z)`. Proof HEAD `cc747f3b550054bab8b638a8772d001fe8e546d8`; P0 `35524734167`; P1 `35524734103`; artifact `10609600687`.
21. `MixinViewAreaVanilla` minimum block-height vocabulary: **39 -> 38**, file **6 -> 5**. One `level.getMinBuildHeight()` became exact MC26.2 `level.getMinY()`. Proof HEAD `810dc19a7a80d7cfcdbcc9ed141292ee976240e7`; P0 `35525024857`; P1 `35525024849`; artifact `10609334285`.
22. `MixinViewAreaVanilla` custom RenderSection construction: **38 -> 37**, file **5 -> 4**. Exact 26.2 constructor `(int,long)` receives `SectionPos.asLong(chunkX, sectionY, chunkZ)`. Corrected proof HEAD `40a1e1c01bd3ab9bd95e88ccb13b24a20b161652`; P0 `35525809602`; P1 `35525809605`; artifact `10609846738`. First harness-only attempt `cac6bfbc31de769b2567b5f2f7aff73076f8ca5e` remains negative evidence.
23. `MixinViewAreaVanilla` custom RenderSection disposal: **37 -> 35**, file **4 -> 2**. Two removed `releaseBuffers()` calls became exact MC26.2 `RenderSection.reset()`. Proof HEAD `46cba3394c19097a936b86682e3cff2fdaf9898d`; P0 `35526099440`; P1 `35526099434`; artifact `10609587540`.
24. `MixinViewAreaVanilla` dirty-authority migration: **35 -> 33**, total files **5 -> 4**, and `MixinViewAreaVanilla` compile-clean. Obsolete pinned `ViewArea#setDirty` interception is removed because 26.2 dirty ownership moved earlier; forced dirtying of newly created custom ship sections reuses the frozen `LevelExtractorInvoker` with boolean `true`. Exact proof HEAD `792b4c95cbbbff30acbc1d0f73eace7685a5f44f`; P1 `35527545210`; artifact `10610560981`, digest `sha256:ef018f4387786af54587ba303198374e9b4ed61452f428b5e112aa7754a57aae`.
25. FTB Chunks build-height vocabulary: **33 -> 31**, total files **4 -> 3**, FTB file compile-clean. Lower bound became `getMinY()` and old exclusive upper bound became `getMinY() + getHeight()`; claim policy, ship lookup, real VS2 transform, and return ordering remain unchanged. Exact proof HEAD `7e40db44586a26c9048b1474e732fdce381ea039`; P0 `35528043018`; P1 `35528042981`; artifact `10609734883`, digest `sha256:7c5b4e27b8b31d56099b606861d89c34cad85a15c9adae3260aa9d3c266ee0ad`.
26. OptiFine compat section range: **31 -> 29**. Old `getMinSection()` / exclusive `getMaxSection()` became `getMinSectionY()` / inclusive `getMaxSectionY()` with `<=`; F3+A refresh semantics and dirty call remained untouched in this unit. Exact proof HEAD `e6fcc37b11382523e4e8136098e5544660032931`; P0 `35528400870`; P1 `35528400868`; artifact `10609953228`, digest `sha256:fd96c7b7d2cd80215b3dafb8c936b34e8c37a91c4a09eaa68901c2cbd4d0a459`.
27. OptiFine compat dirty authority: **29 -> 28**, total files **3 -> 2**, OptiFine file compile-clean. Removed `ViewArea.setDirty(..., false)` is bridged through the already-frozen `LevelExtractorInvoker`, preserving boolean `false`, ship-chunk iteration, section coverage, and `allChanged` injection. Exact proof HEAD `867cbb01a66c0842e22e831d1be02d42479b92e6`; P0 `35529562987`; P1 `35529562974`; artifact `10611096790`, digest `sha256:ef5dffcae65d0e759bf9fcb0d3aafbdf12fbd5fb120185701413249cb20f55f7`.

Freeze all twenty-seven units above. Runtime semantics remain to be proven later by normal P1/P2 gates. Do not reopen them absent direct contradictory evidence.

## Renderer authority evidence and locked boundaries

- Exact MC26.2 `RenderSection` has no dirty field/method. `setDirty(true) -> setDirty()` is a locked failed hypothesis.
- Exact authority probe `35520379454` and corrected owner/signature probe `f35ef5b437f3f5accb31226390eb9518339b805c` / `35522306388` / artifact `10609236384` established dirty ownership in `Minecraft.levelExtractor -> LevelExtractor.setSectionDirty(x,y,z,boolean) -> SectionUpdateTracker`.
- The public 3-int route does not preserve the pinned boolean; the single registered `LevelExtractorInvoker` exposes the exact private 4-arg authority. Reuse this invoker; do not create a second dirty state/authority.
- Exact 26.2 `RenderSection` constructor `(int,long)` stores a packed section node; use `SectionPos.asLong(sectionX, sectionY, sectionZ)` where this upstream renderer architecture requires a new custom section.
- Exact 26.2 `ViewArea.releaseAllBuffers()` uses `RenderSection.reset()`; unit #23 is the bounded ship-section teardown adaptation.
- Vanilla renderer bridge remains original VS2 authority: loaded ships, transformed ship AABB, `VSClientGameUtils.transformRenderWithShip`, custom ship ViewArea sections, and vanilla `visibleSections`. No custom renderer authority is permitted.

## LevelChunk blending-data invariant

Exact mapped 26.2 evidence established `ChunkAccess.blendingData` is final and constructor-owned, with no setter. Live `LevelChunk` hot replacement is not a safe local substitute. Evidence: ownership `df2722ced726e73d5fe70b2290225d664860cfd8` / `35517373126`; live replacement `cd1b1c8988089adcece9a379a6aeec31df74a796` / `35517757678`; promotion `0ed859be21b7efe367051855b91950b1e9d8f2cb` / `35518028364`; unload/reload `5e976d7bac63a5c840f7fb3b668ad21ca32d6e43` / `35518330932`.

The frozen helper removes only the now-illegal null-to-null assignment and throws if source or destination ever carries non-null blending data. Do not reopen with `@Mutable`, reflection, unsafe/final writes, private future/map mutation, duplicate storage, silent metadata loss, or forced synchronous unload/reload.

## Frozen architecture-sensitive boundaries

Do not reopen absent direct contradictory evidence:

- real VS2 ship chunk-ticket lifecycle — `65a42e782de192f27d5bf720691d6e08f395a719`, proof `35450402031`; shutdown removal `fc887ec127899ba1437433ebf77ee6fc968c82ab`, proof `35510099480`.
- DistanceManager / TicketStorage bridge — `8a338f95103227ed6a5acb35804d573bbae0d96c`, proof head `ca07a2fff0fd922cbbd578a0531d3377313827de`, proof `35463018541`; **READ ONLY**.
- ShipSavedData persistence — `f2b3ec68e0d2146bb8b443da76a62a4766e01fce`, proof `35451366140`.
- entity local authority / interpolation — `b7e583af13598b6ddcc583380872f578b8a40bb8`, proof `35455551701`; no synthetic carry.
- entity renderer submit lifecycle — `a87512437f40a3bfa1325d78f8e2588587ec7cc8`, proof `35458380245`.
- shipyard teleport mapping — proof `35467615790`; real VS2 transforms remain authority, no per-tick chase.
- LevelRenderer / LevelExtractor split — `660d5320902a3ecba4f3219969aa77b0316cfa52`; `IVSCamera` observation only.
- optional Create deployer helper is P1 compile isolation only, never P3 integration.
- all frozen ClientLevel, ClientPacketListener, ClientChunkCache, LevelChunk, vanilla renderer, ViewArea, FTB and OptiFine units listed above retain original VS2 authority/order.

Forbidden final architecture remains: custom VS2-like reference frames, synthetic carry/inertia, fake gravity, manual wall/floor/ceiling clamps, per-tick teleport/setPos chase, camera counter-rotation/forcing, duplicate authority, floor-only fake success, or implementation reuse from retired `apm23/VS2-Create_Interactive`.

## Locked negative evidence

- wrong Kotlin source-set exclusion for `DeployerScrollOptionSlot`: `3bcbf90c75dc4d02448cfdb4590cc9c9674e0ed6` / `35454717409`.
- `setUnsaved(false)` invalid current API: `a72aaef8eca34a352ef949eeb57e6bbcda81171f`.
- VSKeyBindings failed probes: `e108526cbd728454c175c76bffc610d4e074da49`, `fcc65187d79c4b546883875da3597345db1e01cd`, `e9a3efd58acb2af9539628eb2875e6cb829c3cec`, `fb3c7e65a4c2089f6fa695114734d14836bde1d3`.
- pathfinding `b3927e625acf40edbf517970ebc952a104a20c97` / `35493933563`: parser/assertion-only failure.
- renderer proof `35497975815` / `35498155312`: broad substring `Uniform` falsely matched valid `DynamicUniforms`; never replay.
- ChunkMap retrigger `6ce41dfbef36b8c8021f48f52f0020e7b1131d5f`: wrongly targeted nonexistent `getById(arg.toLong())`; never replay.
- `player.getDimensions(Pose.STANDING)` is locked failed; retain `getDefaultDimensions(Pose.STANDING)`.
- direct final-field mutation and synchronous LevelChunk replacement/unload are locked failed hypotheses.
- `RenderSection.setDirty(true) -> setDirty()` is locked failed; 26.2 RenderSection has no dirty member.
- renderer-dirty helper two-site `!= VSRenderer.SODIUM` guard is locked failed; pinned source has three sites.
- ViewArea section-index helper two-site `vs$getShipRenderSection` guard is locked failed; pinned source has one occurrence. Harness-only.
- ViewArea constructor first proof HEAD `cac6bfbc31de769b2567b5f2f7aff73076f8ca5e` / P1 `35525664958` is locked as helper/import-guard-only failure; corrected unit #22 is authoritative.
- Actions self-push workflow edits without `workflows` permission remain failed transport.
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
2. Preserve all twenty-seven frozen P1 units and all locked negative evidence.
3. Treat `867cbb01a66c0842e22e831d1be02d42479b92e6` / P0 `35529562987` / canonical P1 `35529562974` / artifact `10611096790` as the authoritative **28-error / 2-source-file** implementation proof until a later exact canonical compile changes it.
4. Remain P1 standalone. The active compile frontier is now only upstream Immersive Portals compatibility source; no Create/SNR/Copycats integration and no gameplay redesign.
5. Apply the smallest mechanical unit to `MixinImmPtlChunkTracking`: map exactly one old lower build-height accessor to `world.getMinY()` and exactly one old exclusive upper accessor to `world.getMinY() + world.getHeight()`. Preserve `ChunkLoader` loops, `ChunkPosConsumer`, `VSGameUtilsKt.getShipsIntersecting`, active ship chunk iteration, dimensions, and distance argument.
6. Run exact-head P0 + canonical P1. Expected result for this accessor-only unit is **28 -> 26**, with `MixinImmPtlChunkTracking` **3 -> 1** and only the existing `net.minecraft.class_5321` dependency/mapping access diagnostic remaining in that file. Do not assume success before artifact proof.
7. After that proof, investigate the exact current Immersive Portals compile dependency/mapping identity behind `ChunkLoader.getCenter().dimension` / missing `net.minecraft.class_5321` before mutating that access. Do not guess a field/method replacement from a different Immersive Portals version.
8. Keep `MixinMyBuiltChunkStorage` as a separate later frontier. Its 25 errors span constructor/method/field API changes and renderer authority; port it in bounded units using already-frozen vanilla ViewArea/RenderSection evidence, not a new renderer implementation.
9. No ordinary compile/debug video.
