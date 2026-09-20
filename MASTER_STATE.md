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

- canonical implementation HEAD: `419ff924c17869ed0b49068f238dafd203d94860` — `ci: retrigger corrected move-player collision proof`.
- exact-head P0 provenance run `35506833892`: **success**.
- exact-head ship-debug/canonical-chain proof run `35506833895`: **success**.
- exact-head standalone P1 compile run `35506833883`: **compile-frontier failure only** after the full canonical overlay chain reached javac.
- canonical compile artifact: `p1-compile-log-419ff924c17869ed0b49068f238dafd203d94860`, ID `10604386289`, artifact digest `sha256:b8c93733d83a64d57a0438678ed0554387558856a7423cbeaa698daa979b0b26`.
- extracted `p1-compile.log`: **267133 bytes**, SHA-256 `d00916db65dbc95a0b59a27766ef5c3f71074a347530a8f28aa7abbdf6ab608a`.
- authoritative primary javac pass: **74 errors across 11 Java source files**. Gradle repeats the same diagnostics later; use the first `74 errors` summary as frontier authority.
- project state: `P1_SOURCE_API_ADAPTATION_IN_PROGRESS`.
- active blocker classification: `MINECRAFT_26_2_JAVA_API_FRONTIER`.
- This is not P1 boot proof, not P2/M1 ship proof, and not runtime rendering proof.

### Proven frontier progression since the old 86-error ledger

1. `MixinServerLevel` chunk-key/build-height vocabulary: **86 -> 82**. Exact four-site adaptation only; TicketStorage predicates, SHIP_CHUNK lifecycle, load/unload ordering, terrain updates, wing scan, and shipyard keep-loaded authority preserved.
2. optional legacy Sodium chunk-tracker bridge isolation: **82 -> 80**. P1 standalone does not include Sodium; only the two obsolete optional callbacks/imports were isolated. Vanilla VS2 rendering remains authority.
3. `MixinEntity.entityInside` 26.2 effect collector adaptation: **80 -> 79**. Real upstream VS2 ship-space scan now feeds Entity's own vanilla `InsideBlockEffectApplier.StepBasedCollector`; no NOOP suppression or duplicate block-effect authority.
4. `MixinLivingEntity` local-instance authority vocabulary: **79 -> 78**. Old `isControlledByLocalInstance()` semantics were matched to the 26.2 local-instance authority split; dragged-entity ship lookup/interpolation authority unchanged.
5. `MixinLocalPlayer` movement-packet constructors: **78 -> 74**. All four 26.2 `ServerboundMovePlayerPacket` variants forward the incoming vanilla `horizontalCollision()` flag unchanged while retaining VS2's existing `isOnGround` adaptation and real ship-motion packet/transform paths.

Freeze all five units above at P1 compile/API scope. Runtime semantics remain to be proven later by the normal P1/P2 gates.

### Current primary Java frontier at `419ff924...`

1. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/immersive_portals/MixinMyBuiltChunkStorage.java` — 25
2. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/vanilla_renderer/MixinViewAreaVanilla.java` — 14
3. `common/src/main/java/org/valkyrienskies/mod/mixin/client/world/MixinClientChunkCache.java` — 11
4. `common/src/main/java/org/valkyrienskies/mod/mixin/world/chunk/MixinLevelChunk.java` — 8
5. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/vanilla_renderer/MixinLevelRendererVanilla.java` — 3
6. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/immersive_portals/MixinImmPtlChunkTracking.java` — 3
7. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/optifine_vanilla/MixinLevelRenderer.java` — 3
8. `common/src/main/java/org/valkyrienskies/mod/mixin/client/world/MixinClientLevel.java` — 2
9. `common/src/main/java/org/valkyrienskies/mod/mixin/client/multiplayer/MixinClientPacketListener.java` — 2
10. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/ftb_chunks/MixinClaimedChunkManagerImpl.java` — 2
11. `common/src/main/java/org/valkyrienskies/mod/mixin/server/MixinMinecraftServer.java` — 1

`MixinServerLevel`, `SodiumCompat`, `MixinEntity`, `MixinLivingEntity`, and `MixinLocalPlayer` are now zero-error in the primary javac pass.

Do not bulk-rewrite this list. Continue one bounded, evidence-backed 26.2 API unit at a time.

## Frozen architecture-sensitive boundaries

Do not reopen absent direct contradictory evidence:

- real VS2 ship chunk-ticket lifecycle — `65a42e782de192f27d5bf720691d6e08f395a719`, proof `35450402031`.
- DistanceManager / TicketStorage read bridge — `8a338f95103227ed6a5acb35804d573bbae0d96c`, proof head `ca07a2fff0fd922cbbd578a0531d3377313827de`, P0 `35463018487`, proof `35463018541`; **READ ONLY**.
- ShipSavedData persistence — `f2b3ec68e0d2146bb8b443da76a62a4766e01fce`, proof `35451366140`.
- entity local authority / interpolation — `b7e583af13598b6ddcc583380872f578b8a40bb8`, proof `35455551701`; no synthetic carry.
- entity renderer submit lifecycle — `a87512437f40a3bfa1325d78f8e2588587ec7cc8`, proof `35458380245`.
- shipyard teleport API mapping — proof `35467615790`; real VS2 transform authority, no per-tick teleport chase.
- vanilla renderer bridge — canonical `290e2bb6c1f6248437e4d189dfb4a01e82a31e33`; real VS2 ship-aware distance, loaded-ship iteration, transformed ship AABB, and `VSClientGameUtils.transformRenderWithShip` remain authority. Later 26.2 renderer errors do not authorize redesigning transform authority.
- LevelRenderer / LevelExtractor split — `660d5320902a3ecba4f3219969aa77b0316cfa52`; existing `IVSCamera` is observation only.
- optional Create deployer helper is P1 compile isolation only, never P3 Create integration.

Forbidden final architecture remains: custom VS2-like reference frames, synthetic carry/inertia, fake gravity or wall/floor clamps, per-tick setPos chase, camera counter-rotation/forcing, duplicate authority, floor-only fake success, or reuse of retired `apm23/VS2-Create_Interactive` implementation code.

## Locked negative evidence

- `3bcbf90c75dc4d02448cfdb4590cc9c9674e0ed6` / `35454717409`: wrong Kotlin source-set exclusion for `DeployerScrollOptionSlot`.
- `a72aaef8eca34a352ef949eeb57e6bbcda81171f`: `setUnsaved(false)` invalid current API.
- VSKeyBindings failed probes `e108526cbd728454c175c76bffc610d4e074da49`, `fcc65187d79c4b546883875da3597345db1e01cd`, `e9a3efd58acb2af9539628eb2875e6cb829c3cec`, `fb3c7e65a4c2089f6fa695114734d14836bde1d3`.
- pathfinding `b3927e625acf40edbf517970ebc952a104a20c97` / `35493933563`: parser/assertion-only failure.
- renderer helper/proof `35497975815` and `35498155312`: broad substring `Uniform` falsely matched valid `DynamicUniforms`; never replay broad guard.
- ChunkMap retrigger `6ce41dfbef36b8c8021f48f52f0020e7b1131d5f`: helper wrongly targeted nonexistent `getById(arg.toLong())`; never replay.
- LivingEntity first authority helper guard expected one `getLastShipStoodOn()` but source legitimately had two. Corrected harness-only; authority hypothesis later compile-green.
- move-player first helper guard expected one `ship.getWorldToShip().transformPosition(` / networking anchor but source legitimately had two (player + vehicle paths). Corrected harness-only; packet hypothesis later compile-green.
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
3. Treat artifact `10604386289` as the canonical **74-error / 11-source-file** Java frontier until a later exact canonical compile changes it.
4. First non-optional frontier is `MixinClientChunkCache.java`. Split its 11 errors into semantic units; do not file-wide rewrite it.
5. Already-proven exact 26.2 evidence for the first mechanical units:
   - `LevelChunk.replaceWithPacketData` / `ClientChunkCache.replaceWithPacketData` now take `Map<Heightmap.Types, long[]>` instead of old `CompoundTag` heightmaps. Adapt only the packet-heightmap type/call sites after checking exact upstream method signature/anchors.
   - `ChunkPos` packed-key/accessor vocabulary may be adapted mechanically only where already-proven canonical vocabulary applies.
   - old `SectionRenderDispatcher.RenderSection.setDirty(boolean)` is gone in 26.2. Do **not** guess a direct replacement. Current vanilla 26.2 dirty propagation goes through `ClientLevel.setSectionDirtyWithNeighbors(...)` / `LevelExtractor`; inspect the exact VS2 intent and section-coordinate semantics before any render-dirty adaptation.
6. Keep packet decode, relight, terrain connectivity updates, ship chunk lifecycle, renderer selection, and `onChunkLoaded` ordering unchanged while adapting any bounded `MixinClientChunkCache` unit.
7. Optional compat (`Immersive Portals`, FTB Chunks, OptiFine) is not the first target merely because it has many errors. Establish target-runtime optionality/dependency evidence before isolation or port work.
8. `MixinLevelChunk`, `MixinClientLevel`, `MixinClientPacketListener`, and `MixinMinecraftServer` each contain lifecycle/authority-sensitive changes. Split them into separately evidenced units.
9. After any bounded mutation, run exact canonical standalone P1 compile, classify the first primary javac pass from the uploaded artifact, and update this ledger at the next meaningful proven boundary.
10. Remain P1. No ordinary compile/debug video.
