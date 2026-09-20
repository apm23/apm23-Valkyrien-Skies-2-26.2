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

- canonical implementation/proof HEAD: `46cba3394c19097a936b86682e3cff2fdaf9898d` — `ci: prove ViewArea RenderSection disposal frontier`.
- exact-head P0 provenance run `35526099440`: **success**.
- exact-head canonical P1 compile run `35526099434`: reached primary javac; compile-frontier failure only. All canonical overlays and delta validation completed successfully before javac.
- compile artifact `p1-compile-log-46cba3394c19097a936b86682e3cff2fdaf9898d`, ID `10609587540`, digest `sha256:d5042099d3dc77f8d34c79cedaf7af4caee2814dfb4372789d6d4b7176a43e66`.
- extracted `p1-compile.log`: **216857 bytes**, SHA-256 `6cf0220fb64476c73f1320b18aaadd24246b01c588c721d19757d426f50989f9`.
- authoritative first primary `:common:compileJava` pass: **35 errors across 5 Java source files**.
- `MixinViewAreaVanilla.java` is down to **2 errors**, both removed `RenderSection.setDirty(boolean)` authority sites.
- `MixinClientChunkCache.java`, `MixinLevelRendererVanilla.java`, `MixinLevelChunk.java`, and `LevelExtractorInvoker` remain absent from the first primary error pass.
- project state: `P1_SOURCE_API_ADAPTATION_IN_PROGRESS`.
- active blocker classification: `MINECRAFT_26_2_VIEWAREA_DIRTY_AUTHORITY_MIGRATION`.
- This is not P1 boot proof, not P2/M1 ship proof, and not runtime rendering proof.

### Current primary Java frontier at `46cba339...`

1. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/immersive_portals/MixinMyBuiltChunkStorage.java` — 25
2. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/immersive_portals/MixinImmPtlChunkTracking.java` — 3
3. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/optifine_vanilla/MixinLevelRenderer.java` — 3
4. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/ftb_chunks/MixinClaimedChunkManagerImpl.java` — 2
5. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/vanilla_renderer/MixinViewAreaVanilla.java` — 2

Optional compat is not the next target merely because it appears first in javac ordering. Standalone P1 vanilla ship rendering remains mandatory; finish the two dirty-authority diagnostics first.

### Exact remaining `MixinViewAreaVanilla` blocker

Both remaining diagnostics are `RenderSection.setDirty(boolean)` calls from pinned upstream:

1. old `ViewArea.setDirty(...)` injection mirrors vanilla dirty scheduling into the custom ship section;
2. `vs$getOrCreateShipRenderSection(...)` marks a newly created custom section dirty with `true`.

Exact MC26.2 `RenderSection` has no dirty field/method, and exact MC26.2 `ViewArea` has no `setDirty(...)`. Dirty state is owned by `SectionUpdateTracker`, reached through `Minecraft.levelExtractor -> LevelExtractor.setSectionDirty(x,y,z,boolean)`. Do not recreate dirty state inside RenderSection.

## Proven frontier progression — frozen at P1 compile/API scope

1. `MixinServerLevel` chunk-key/build-height vocabulary: **86 -> 82**.
2. optional legacy Sodium callbacks isolation: **82 -> 80**; standalone P1 vanilla renderer remains authority.
3. `MixinEntity.entityInside` 26.2 effect collector adaptation: **80 -> 79**.
4. `MixinLivingEntity` local-instance authority vocabulary: **79 -> 78**; dragging/interpolation authority unchanged.
5. `MixinLocalPlayer` movement packet constructors: **78 -> 74**.
6. `MixinClientChunkCache` packed keys + packet-heightmap API: **74 -> 66**.
7. `MixinClientChunkCache` section-height range: **66 -> 64**; exclusive 1.21 max became inclusive 26.2 max without changing covered sections.
8. `MixinMinecraftServer` shutdown SHIP_CHUNK ticket removal: **64 -> 63**, commit `fc887ec127899ba1437433ebf77ee6fc968c82ab`, proof `35510099480`.
9. `MixinClientLevel` two-hand creative-barrier API: **63 -> 62**, proof head `486dbdaec5302f983d76bd871dea4e59eac67479`.
10. `MixinClientLevel` base standing dimensions API: **62 -> 61**, proof `35511223209`; do not use scale-aware dimensions here.
11. `MixinClientPacketListener` packet-created entity creation API: **61 -> 60**, proof head `d0bf1efc8ae705ba0aa1f88e7c64be79db3e365b`.
12. `MixinClientPacketListener` packet-position `moveTo -> snapTo`: **60 -> 59**, proof `35512025153`; explicit VS2 mounting/network ordering preserved.
13. `MixinLevelChunk` dirty-save marking: **59 -> 57**; direct `unsaved=true` became public `markUnsaved()` only. Proof `35514352664`.
14. `MixinLevelChunk` empty-section construction: **57 -> 53**; registry context became `palettedContainerFactory()`. Proof `35515573624`.
15. `MixinLevelChunk` serialized parse factory: **53 -> 52**; `SerializableChunkData.parse` context became `level.palettedContainerFactory()`. Proof `35516856204` at `b7104b6e1796fa498f1e7782ebfcc899e771b3fe`.
16. `MixinLevelChunk` final `BlendingData` ownership: **52 -> 51** and `MixinLevelChunk` compile-clean. Exact proof `1860dc3863c2151320eb18f7ab9b161f5ae7f551`, P0 `35519773694`, P1 `35519773646`, artifact `10607928437`.
17. `MixinClientChunkCache` vanilla renderer dirty scheduling: **51 -> 50**, **7 -> 6 files**. Pinned `RenderSection.setDirty(true)` is bridged into exact MC26.2 `Minecraft.levelExtractor -> LevelExtractor.setSectionDirty(x,y,z,boolean) -> SectionUpdateTracker` via one Mixin invoker, preserving boolean `true`, custom ship-section coordinates, renderer selection, relight, and `onChunkLoaded` ordering. Canonical proof HEAD `b2e308ff693ef88c091228002f8077b61f01d6d6`; P0 `35522623140`; P1 `35522623113`; artifact `10608463644`.
18. `MixinLevelRendererVanilla` ship-visible section bounds: **50 -> 47**, **6 -> 5 files**. `getMinSection()` / exclusive `getMaxSection()` became `getMinSectionY()` / inclusive `getMaxSectionY()` with `<=`. Proof HEAD `dcf4a14e09c9c67ca7bf51ba3552027b2a7e80cf`; P0 `35523910648`; P1 `35523910705`; artifact `10609192424`.
19. `MixinViewAreaVanilla` ship-section array index origin: **47 -> 44**, file **14 -> 11**. Three `getMinSection()` calls became `getMinSectionY()`. Proof HEAD `9405f49a9bd5c348a12098fb9e983b62712f16fe`; P0 `35524343843`; P1 `35524343861`; artifact `10609430640`.
20. `MixinViewAreaVanilla` packed ship-chunk keys: **44 -> 39**, file **11 -> 6**. Five `ChunkPos.asLong(x,z)` became `ChunkPos.pack(x,z)`. Proof HEAD `cc747f3b550054bab8b638a8772d001fe8e546d8`; P0 `35524734167`; P1 `35524734103`; artifact `10609600687`.
21. `MixinViewAreaVanilla` minimum block-height vocabulary: **39 -> 38**, file **6 -> 5**. One `level.getMinBuildHeight()` became exact MC26.2 `level.getMinY()`. Proof HEAD `810dc19a7a80d7cfcdbcc9ed141292ee976240e7`; P0 `35525024857`; P1 `35525024849`; artifact `10609334285`.
22. `MixinViewAreaVanilla` custom RenderSection construction: **38 -> 37**, file **5 -> 4**. Exact 26.2 constructor `(int,long)` receives `SectionPos.asLong(chunkX, sectionY, chunkZ)` and the helper adds exactly one `SectionPos` import; block-coordinate shifts are not retained. Initial helper/chain `7fa958568e9584a30179c9876fb46bda0796228d` / `ad7cc0d601f83c66c44747dfedee27c1e4454bd5`. First proof HEAD `cac6bfbc31de769b2567b5f2f7aff73076f8ca5e` / P1 `35525664958` failed harness-only because the helper wrongly required a pre-existing SectionPos import. Corrected helper `e13f87d93d950edaa604acef76bede3f2d477709`; exact proof HEAD `40a1e1c01bd3ab9bd95e88ccb13b24a20b161652`; P0 `35525809602`; P1 `35525809605`; artifact `10609846738`, digest `sha256:c14bdfe20b9d31f809092123aef8de5b2fe49d1bbb6438795aa018e998ccea4d`.
23. `MixinViewAreaVanilla` custom RenderSection disposal: **37 -> 35**, file **4 -> 2**, total files unchanged at 5. Exactly two removed `releaseBuffers()` calls become exact MC26.2 `RenderSection.reset()`; custom map removal/clear and dirty authority remain untouched. Helper `7b0a48c33c87baf9a6268fa5cbb1ad5b0a537010`; canonical chain `54d22184eeb475c3b9e106846ec765905691b2f7`; exact proof HEAD `46cba3394c19097a936b86682e3cff2fdaf9898d`; P0 `35526099440`; P1 `35526099434`; artifact `10609587540`.

Freeze all twenty-three units above. Runtime semantics remain to be proven later by normal P1/P2 gates.

## Renderer authority evidence and locked boundaries

- Initial dirty probe HEAD `8db9a7cbf8c909609b3078010d6866d6ef70ecd1`, run `35520170375`, artifact `10608013620`: exact 26.2 `RenderSection` has no dirty-related field/method. `setDirty(true) -> setDirty()` is a locked failed hypothesis.
- Exact authority probe `35520379454` established dirty/update ownership moved into `LevelExtractor` / `SectionUpdateTracker`.
- Corrected owner/signature probe HEAD `f35ef5b437f3f5accb31226390eb9518339b805c`, run `35522306388`, artifact `10609236384`, digest `sha256:0a1fe77a594684feccb041f19ae9dc26c1bb0899cff17af42b37c91850b4d0cb`: `Minecraft.levelExtractor` is the owner; private 4-arg dirty entrypoint preserves upstream boolean; extraction consumes dirty state through `visibleSections`; `LevelRenderer` performs the 26.2 `ViewArea.getRenderSection(long)` lookup.
- Exact 26.2 `RenderSection` constructor `(int,long)` stores a packed section node. Vanilla `ViewArea` constructs sections with `SectionPos.asLong(sectionX,sectionY,sectionZ)`. Unit #22 is the compile-proven bounded adaptation.
- Exact 26.2 vanilla `ViewArea.releaseAllBuffers()` calls `RenderSection.reset()`. `reset()` cancels compile work, releases/closes section mesh and backing uber-buffer allocations, and clears render-section task/upload state. Unit #23 is the compile-proven bounded custom-section teardown adaptation.
- Exact 26.2 `ViewArea` has no `setDirty(...)`. Dirty state is keyed by section node in `SectionUpdateTracker`; `LevelExtractor.extractUsedSectionRenderStates(...)` consumes it and `LevelRenderer` resolves the section through `ViewArea.getRenderSection(long)`. Do not invent per-section dirty state.
- Vanilla renderer bridge remains original VS2 authority: loaded ships, transformed ship AABB, `VSClientGameUtils.transformRenderWithShip`, custom ship ViewArea sections, and vanilla visibleSections. No custom renderer authority is permitted.

## LevelChunk blending-data boundary — resolved invariant

Exact mapped 26.2 evidence established `ChunkAccess.blendingData` is final and constructor-owned, with no setter. Live `LevelChunk` hot replacement is not a safe local substitute: `GenerationChunkHolder.replaceProtoChunk` is promotion-only and normal unload is asynchronous.

Evidence: ownership `df2722ced726e73d5fe70b2290225d664860cfd8` / `35517373126`; live replacement `cd1b1c8988089adcece9a379a6aeec31df74a796` / `35517757678`; promotion `0ed859be21b7efe367051855b91950b1e9d8f2cb` / `35518028364`; unload/reload `5e976d7bac63a5c840f7fb3b668ad21ca32d6e43` / `35518330932`.

The frozen helper removes only the now-illegal null-to-null assignment and throws if source or destination ever carries non-null blending data. Do not reopen with `@Mutable`, reflection, unsafe/accessor final writes, private future/map mutation, duplicate storage, silent metadata loss, or forced synchronous unload/reload.

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
- all frozen ClientLevel, ClientPacketListener, ClientChunkCache, LevelChunk, vanilla LevelRenderer, and ViewArea units listed above retain original VS2 authority/order.

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
- constructor first proof HEAD `cac6bfbc31de769b2567b5f2f7aff73076f8ca5e` / P1 `35525664958` is locked as helper/import-guard-only failure; it incorrectly assumed SectionPos was already imported. Corrected unit #22 is authoritative.
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
2. Preserve all twenty-three frozen P1 units and all locked negative evidence.
3. Treat `46cba3394c19097a936b86682e3cff2fdaf9898d` / P0 `35526099440` / canonical compile `35526099434` / artifact `10609587540` as the authoritative **35-error / 5-source-file** implementation proof until a later exact canonical compile changes it.
4. Continue mandatory standalone vanilla renderer before optional FTB/OptiFine/Immersive-Portals work.
5. Investigate the exact 26.2 dirty route before source mutation. Prove how ordinary block/section dirty events enter `LevelExtractor.setSectionDirty(..., boolean)`, then flow through `SectionUpdateTracker` and `ViewArea.getRenderSection(long)`, including whether the pinned upstream `ViewArea.setDirty` injection is now redundant because its authority moved earlier into LevelExtractor.
6. Reconcile the two remaining upstream semantics separately: (a) mirroring ordinary dirty events for shipyard sections with the upstream `important` boolean; (b) forcing a newly created custom ship section dirty with `true`. Prefer the smallest bridge into the already-proven LevelExtractor authority; do not recreate RenderSection dirty state or manually compile sections.
7. Only after ownership/target semantics are proven, implement the smallest fail-closed dirty-authority overlay and run exact-head P0 + canonical P1 compile. Expected compile-clean ViewArea outcome is **35 -> 33** and `MixinViewAreaVanilla` **2 -> 0**, but do not assume it before artifact proof.
8. Remain P1. No optional compat first, no Create/SNR/Copycats integration, and no ordinary compile/debug video.
