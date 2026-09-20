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

- canonical implementation/proof HEAD: `9405f49a9bd5c348a12098fb9e983b62712f16fe` — `ci: rerun ViewArea section index proof after guard fix`.
- exact-head P0 provenance run `35524343843`: **success**.
- exact-head canonical P1 compile run `35524343861`: reached primary javac; compile-frontier failure only. All canonical overlays and delta validation completed successfully before javac.
- compile artifact `p1-compile-log-9405f49a9bd5c348a12098fb9e983b62712f16fe`, ID `10609430640`, digest `sha256:1a9aea1bd002b6b6f8141e06c60d328a0503af98b8aa859c2111c044a95a78f0`.
- extracted `p1-compile.log`: **225399 bytes**, SHA-256 `05e49fcd4c799dc5e9861efd967f9a342335be7e1237612a2b513b0f111fc85a`.
- authoritative first primary `:common:compileJava` pass: **44 errors across 5 Java source files**.
- `MixinClientChunkCache.java`, `MixinLevelRendererVanilla.java`, `MixinLevelChunk.java`, and `LevelExtractorInvoker` remain absent from the first primary error pass.
- project state: `P1_SOURCE_API_ADAPTATION_IN_PROGRESS`.
- active blocker classification: `MINECRAFT_26_2_VIEWAREA_SHIP_RENDER_SECTION_LIFECYCLE`.
- This is not P1 boot proof, not P2/M1 ship proof, and not runtime rendering proof.

### Current primary Java frontier at `9405f49a...`

1. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/immersive_portals/MixinMyBuiltChunkStorage.java` — 25
2. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/vanilla_renderer/MixinViewAreaVanilla.java` — 11
3. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/immersive_portals/MixinImmPtlChunkTracking.java` — 3
4. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/optifine_vanilla/MixinLevelRenderer.java` — 3
5. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/ftb_chunks/MixinClaimedChunkManagerImpl.java` — 2

Optional compat is not the next target merely because it appears first in javac ordering. Standalone P1 vanilla ship rendering remains mandatory; resolve `MixinViewAreaVanilla` in bounded units first.

### Exact `MixinViewAreaVanilla` remaining-error decomposition

The 11 current diagnostics are five distinct API/lifecycle classes and must not be flattened into one speculative patch:

- 5 × `ChunkPos.asLong(int,int)` missing — packed chunk-key vocabulary.
- 1 × `Level.getMinBuildHeight()` missing — minimum build-height vocabulary.
- 2 × `RenderSection.setDirty(boolean)` missing — dirty scheduling authority moved out of `RenderSection`.
- 1 × `RenderSection(int,int,int,int)` constructor missing — 26.2 constructor is `(int,long)` and packed section-node semantics must be preserved.
- 2 × `RenderSection.releaseBuffers()` missing — disposal/resource ownership changed and requires exact lifecycle evidence before replacement.

The three prior `Level.getMinSection()` diagnostics are compile-proven resolved only as `getMinSectionY()` index-origin vocabulary. Do not combine constructor, dirty scheduling, or disposal into a guessed renderer rewrite.

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
17. `MixinClientChunkCache` vanilla renderer dirty scheduling: **51 -> 50**, **7 -> 6 files**. Pinned `RenderSection.setDirty(true)` is bridged into exact MC26.2 `Minecraft.levelExtractor -> LevelExtractor.setSectionDirty(x,y,z,boolean) -> SectionUpdateTracker` via one Mixin invoker, preserving boolean `true`, custom ship-section coordinates, renderer selection, relight, and `onChunkLoaded` ordering. Canonical proof HEAD `b2e308ff693ef88c091228002f8077b61f01d6d6`; P0 `35522623140`; P1 `35522623113`; artifact `10608463644`, digest `sha256:4add3cc94a2d63ae3de0904dea949ea7c5cb946a794e32a2ce3eb3a56de24a24`; extracted log 232091 bytes SHA-256 `acdebc9c70e3f887ffc80420b09e69f4a053c8808760c7628050403a60b06d35`.
18. `MixinLevelRendererVanilla` ship-visible section bounds: **50 -> 47**, **6 -> 5 files**. Pinned `getMinSection()` / exclusive `getMaxSection()` loop becomes `getMinSectionY()` / inclusive `getMaxSectionY()` with `<=`, preserving identical section coverage and relative array index. Semantic helper commit `8546527f1da53344c630245084e5d18aca0cebd8`; canonical chain `f482f643b96ddbbfed611312b35cf3d5cef2211f`; exact proof HEAD `dcf4a14e09c9c67ca7bf51ba3552027b2a7e80cf`; P0 `35523910648`; P1 `35523910705`; artifact `10609192424`.
19. `MixinViewAreaVanilla` ship-section array index origin: **47 -> 44** with the file **14 -> 11** and total files unchanged at 5. Exactly three removed `Level.getMinSection()` calls become `Level.getMinSectionY()`; there is no max-bound loop and no renderer lifecycle/authority change. Semantic helper commit `e84c9ecd588d1c42b14cab03730fcb82ea17223d`; canonical chain `304fb05763f2ab28e5bff4effd585d7c3efe7b82`; first proof attempt `425565338ad68d325cbde4e3cd15438501904fcc` / P1 `35524246045` failed harness-only because `vs$getShipRenderSection` was guarded as two occurrences instead of the pinned one. Guard-only correction `0f5c5eb78207199faf32c10b0148d952df69668c`; exact proof HEAD `9405f49a9bd5c348a12098fb9e983b62712f16fe`; P0 `35524343843`; P1 `35524343861`; artifact `10609430640`.

Freeze all nineteen units above. Runtime semantics remain to be proven later by normal P1/P2 gates.

## Renderer authority evidence and locked boundaries

- Initial dirty probe HEAD `8db9a7cbf8c909609b3078010d6866d6ef70ecd1`, run `35520170375`, artifact `10608013620`: exact 26.2 `RenderSection` has no dirty-related field/method. Therefore `setDirty(true) -> setDirty()` is a locked failed hypothesis.
- Exact authority probe `35520379454` established dirty/update ownership moved into `LevelExtractor` / `SectionUpdateTracker`.
- Corrected owner/signature probe HEAD `f35ef5b437f3f5accb31226390eb9518339b805c`, run `35522306388`, artifact `10609236384`, digest `sha256:0a1fe77a594684feccb041f19ae9dc26c1bb0899cff17af42b37c91850b4d0cb`: `Minecraft.levelExtractor` is the owner; private 4-arg dirty entrypoint preserves the upstream boolean; extraction consumes dirty state through `visibleSections`; `LevelRenderer` performs the 26.2 `ViewArea.getRenderSection(long)` lookup.
- First renderer-dirty helper run failed only because its fail-closed guard expected two `!= VSRenderer.SODIUM` sites while pinned source legitimately has three; corrected count is frozen. No semantic workaround resulted from that harness failure.
- Vanilla renderer bridge remains original VS2 authority: loaded ships, transformed ship AABB, `VSClientGameUtils.transformRenderWithShip`, custom ship `ViewArea` sections, and vanilla `visibleSections`. No custom renderer authority is permitted.

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
- all frozen ClientLevel, ClientPacketListener, ClientChunkCache, LevelChunk, vanilla LevelRenderer, and ViewArea section-index units listed above retain original VS2 authority/order.

Forbidden final architecture remains: custom VS2-like reference frames, synthetic carry/inertia, fake gravity, manual wall/floor/ceiling clamps, per-tick teleport/setPos chase, camera counter-rotation/forcing, duplicate authority, floor-only fake success, or implementation reuse from retired `apm23/VS2-Create_Interactive`.

## Locked negative evidence

- wrong Kotlin source-set exclusion for `DeployerScrollOptionSlot`: `3bcbf90c75dc4d02448cfdb4590cc9c9674e0ed6` / `35454717409`.
- `setUnsaved(false)` is invalid current API: `a72aaef8eca34a352ef949eeb57e6bbcda81171f`.
- VSKeyBindings failed probes: `e108526cbd728454c175c76bffc610d4e074da49`, `fcc65187d79c4b546883875da3597345db1e01cd`, `e9a3efd58acb2af9539628eb2875e6cb829c3cec`, `fb3c7e65a4c2089f6fa695114734d14836bde1d3`.
- pathfinding `b3927e625acf40edbf517970ebc952a104a20c97` / `35493933563`: parser/assertion-only failure.
- renderer proof `35497975815` / `35498155312`: broad substring `Uniform` falsely matched valid `DynamicUniforms`; never replay.
- ChunkMap retrigger `6ce41dfbef36b8c8021f48f52f0020e7b1131d5f`: wrongly targeted nonexistent `getById(arg.toLong())`; never replay.
- LivingEntity and move-player first helpers had overly narrow occurrence guards; harness-only, later corrected.
- ClientChunkCache section-range first guard `4f7a8461508a55d1c204eaf08343f6af01e32d14` expected one loop while source legitimately has two; corrected at `8dea5dfb0e2df52fbf7440abfa6e69b88c94846b`.
- ClientLevel hand transport `587c6b41d2a95815d26440ee753abc0f70faecb6` / `35510733124` invoked helper twice; later corrected without semantic change.
- `player.getDimensions(Pose.STANDING)` is a locked failed standing-width hypothesis; retain `getDefaultDimensions(Pose.STANDING)`.
- LevelChunk dirty-mark/parse first failures were helper-guard-only; later corrected frozen units are authoritative.
- direct final-field mutation and synchronous LevelChunk replacement/unload are locked failed hypotheses.
- `RenderSection.setDirty(true) -> setDirty()` is locked failed; 26.2 `RenderSection` has no dirty member.
- renderer-dirty helper two-site `!= VSRenderer.SODIUM` guard is locked failed; pinned source has three sites.
- ViewArea section-index helper two-site `vs$getShipRenderSection` guard is locked failed; pinned source has one occurrence. This was harness-only and did not authorize semantic changes.
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
2. Preserve all nineteen frozen P1 units and all locked negative evidence.
3. Treat `9405f49a9bd5c348a12098fb9e983b62712f16fe` / P0 `35524343843` / canonical compile `35524343861` / artifact `10609430640` as the authoritative **44-error / 5-source-file** implementation proof until a later exact canonical compile changes it.
4. Continue the mandatory standalone vanilla renderer before optional FTB/OptiFine/Immersive-Portals work.
5. In pinned `MixinViewAreaVanilla`, address only the five removed packed-key calls `ChunkPos.asLong(x,z)` -> exact MC26.2 `ChunkPos.pack(x,z)`. This is vocabulary already compile-proven in frozen ClientChunkCache/ChunkMap units; preserve every argument, custom ship map lookup/removal, section-array ownership, dirty scheduling, constructor, and disposal site.
6. Do not touch `getMinBuildHeight`, either `setDirty` site, the `RenderSection` constructor, or either `releaseBuffers` site in the same patch.
7. Chain the one packed-key helper canonically, run exact-head P0 + canonical P1 compile, and classify the uploaded first-primary artifact. Expected clean outcome is **44 -> 39** with `MixinViewAreaVanilla` **11 -> 6**; do not assume that result before artifact proof.
8. After that proof, `getMinBuildHeight -> getMinY` is the next already-evidenced vocabulary-only unit. Constructor/disposal still require exact 26.2 ownership/lifecycle evidence before source mutation. Dirty scheduling must continue using proven `LevelExtractor` authority rather than inventing `RenderSection` state.
9. Remain P1. No Create/SNR/Copycats integration and no ordinary compile/debug video.
