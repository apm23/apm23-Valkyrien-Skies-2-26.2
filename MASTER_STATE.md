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

- canonical implementation HEAD: `fc887ec127899ba1437433ebf77ee6fc968c82ab` — `fix: port shutdown ship ticket removal to 26.2 radius API`.
- exact-head standalone P1 compile run `35510099480`: **compile-frontier failure only** after the full canonical overlay chain reached javac.
- canonical compile artifact: `p1-compile-log-fc887ec127899ba1437433ebf77ee6fc968c82ab`, ID `10603954992`, artifact digest `sha256:483474ac247515fd0f749c39c1d7f2f91f125b596309d28a377f1a784459ae35`.
- extracted `p1-compile.log`: **253560 bytes**, SHA-256 `1608c7491fe9dd1cd7f7bae99a9676da6fe67dd3d53d05eb28f1b5015f280907`.
- authoritative primary javac pass: **63 errors across 10 Java source files**. Gradle repeats diagnostics later; use the first `63 errors` summary as frontier authority.
- project state: `P1_SOURCE_API_ADAPTATION_IN_PROGRESS`.
- active blocker classification: `MINECRAFT_26_2_JAVA_API_FRONTIER`.
- This is not P1 boot proof, not P2/M1 ship proof, and not runtime rendering proof.

### Proven frontier progression since the old 86-error ledger

1. `MixinServerLevel` chunk-key/build-height vocabulary: **86 -> 82**. Exact four-site adaptation only; TicketStorage predicates, SHIP_CHUNK lifecycle, load/unload ordering, terrain updates, wing scan, and shipyard keep-loaded authority preserved.
2. optional legacy Sodium chunk-tracker bridge isolation: **82 -> 80**. P1 standalone does not include Sodium; only the two obsolete optional callbacks/imports were isolated. Vanilla VS2 rendering remains authority.
3. `MixinEntity.entityInside` 26.2 effect collector adaptation: **80 -> 79**. Real upstream VS2 ship-space scan now feeds Entity's own vanilla `InsideBlockEffectApplier.StepBasedCollector`; no NOOP suppression or duplicate block-effect authority.
4. `MixinLivingEntity` local-instance authority vocabulary: **79 -> 78**. Old `isControlledByLocalInstance()` semantics were matched to the 26.2 local-instance authority split; dragged-entity ship lookup/interpolation authority unchanged.
5. `MixinLocalPlayer` movement-packet constructors: **78 -> 74**. All four 26.2 `ServerboundMovePlayerPacket` variants forward the incoming vanilla `horizontalCollision()` flag unchanged while retaining VS2's existing `isOnGround` adaptation and real ship-motion packet/transform paths.
6. `MixinClientChunkCache` packed chunk keys plus packet-heightmap API: **74 -> 66**. Six exact `ChunkPos.asLong(...)` uses were adapted to canonical 26.2 packed-key vocabulary, and the two packet decode paths now forward `Map<Heightmap.Types, long[]>`; chunk storage, packet decode, relight, terrain connectivity, ship lifecycle, renderer selection, and `onChunkLoaded` ordering remain unchanged.
7. `MixinClientChunkCache` section-height range: **66 -> 64**. The 1.21.1 exclusive `getMinSection() .. < getMaxSection()` loop is preserved on 26.2 as inclusive `getMinSectionY() .. <= getMaxSectionY()`. A transport guard initially expected one `dx/dz` loop although pinned upstream legitimately contains two; commit `8dea5dfb0e2df52fbf7440abfa6e69b88c94846b` corrected only that fail-closed harness count, and exact-head compile then proved the semantic unit.
8. `MixinMinecraftServer` shutdown SHIP_CHUNK ticket removal: **64 -> 63**. Pinned upstream removes each active ship chunk's radius-0 `SHIP_CHUNK` ticket before shutdown drain and then clears any legacy FORCED ticket. The already-frozen 26.2 lifecycle overlay maps the same old `removeRegionTicket(type, pos, radius, value)` boundary to `removeTicketWithRadius(type, pos, radius)` elsewhere. Commit `fc887ec127899ba1437433ebf77ee6fc968c82ab` extends only that proven mapping to the missed Java shutdown callsite; iteration, radius 0, shutdown ordering, ticket type, and `updateChunkForced(cp, false)` cleanup are unchanged. Exact compile `35510099480` removes `MixinMinecraftServer` from the primary error set.

Freeze all eight units above at P1 compile/API scope. Runtime semantics remain to be proven later by the normal P1/P2 gates.

### Current primary Java frontier at `fc887ec1...`

1. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/immersive_portals/MixinMyBuiltChunkStorage.java` — 25
2. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/vanilla_renderer/MixinViewAreaVanilla.java` — 14
3. `common/src/main/java/org/valkyrienskies/mod/mixin/world/chunk/MixinLevelChunk.java` — 8
4. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/vanilla_renderer/MixinLevelRendererVanilla.java` — 3
5. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/immersive_portals/MixinImmPtlChunkTracking.java` — 3
6. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/optifine_vanilla/MixinLevelRenderer.java` — 3
7. `common/src/main/java/org/valkyrienskies/mod/mixin/client/world/MixinClientLevel.java` — 2
8. `common/src/main/java/org/valkyrienskies/mod/mixin/client/multiplayer/MixinClientPacketListener.java` — 2
9. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/ftb_chunks/MixinClaimedChunkManagerImpl.java` — 2
10. `common/src/main/java/org/valkyrienskies/mod/mixin/client/world/MixinClientChunkCache.java` — 1

`MixinServerLevel`, `SodiumCompat`, `MixinEntity`, `MixinLivingEntity`, `MixinLocalPlayer`, and `MixinMinecraftServer` are zero-error in the primary javac pass. `MixinClientChunkCache` has been reduced from 11 errors to one without redesigning its lifecycle/packet/ship-render authority.

Do not bulk-rewrite this list. Continue one bounded, evidence-backed 26.2 API unit at a time.

## Frozen architecture-sensitive boundaries

Do not reopen absent direct contradictory evidence:

- real VS2 ship chunk-ticket lifecycle — original boundary `65a42e782de192f27d5bf720691d6e08f395a719`, proof `35450402031`; matching missed shutdown removal callsite adapted at `fc887ec127899ba1437433ebf77ee6fc968c82ab`, compile proof `35510099480`. Radius/lifetime/type/order remain frozen.
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
- ClientChunkCache section-range guard at `4f7a8461508a55d1c204eaf08343f6af01e32d14` expected one `dx/dz` loop but pinned upstream legitimately has two (render invalidation plus relight). `8dea5dfb0e2df52fbf7440abfa6e69b88c94846b` corrected the harness only; the exact section-range adaptation then compiled down by two errors. Never infer semantic failure from the earlier guard failure.
- Do not replace the remaining `RenderSection.setDirty(true)` mechanically with a vanilla dirty call. In pinned VS2 that call dirties a section obtained through `IVSViewAreaMethods.vs$getShipRenderSection(...)`; Minecraft 26.2 removed RenderSection dirty mutators and moved vanilla dirty propagation toward LevelExtractor. The exact ship-render-section invalidation ownership/access path must be proven before mutation.
- Actions self-push workflow edits without `workflows` permission remain failed transport hypothesis.
- retired `apm23/VS2-Create_Interactive` implementation is forbidden.

## Target runtime baseline

Exact `BASELINE_LOCK.json` remains authoritative. Current locked stack includes:

- Minecraft `26.2`
- Java `25`
- Fabric Loader observed `0.19.3`
- Fabric API `0.160.0+26.2`, SHA-256 `5f3dff88e1666e222213302b25ace6c36dc3683804cbd4b5acf93138ea05e`
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
3. Treat artifact `10603954992` as the canonical **63-error / 10-source-file** Java frontier until a later exact canonical compile changes it.
4. Freeze the proven `MixinClientChunkCache` packed-key, packet-heightmap, and exclusive-to-inclusive section-range units plus the `MixinMinecraftServer` shutdown radius-ticket API adaptation. Do not replay them.
5. `MixinClientChunkCache.java` still has exactly one primary error: upstream `renderSection.setDirty(true)` on a ship render section returned by `IVSViewAreaMethods.vs$getShipRenderSection(...)`. Exact ship-specific 26.2 invalidation ownership has not been proven. Leave this error in place rather than substituting vanilla dirty authority.
6. Move to the smallest non-optional core frontier with stronger evidence. `MixinClientLevel.java` has two independent API errors: removed `LocalPlayer.getHandSlots()` in creative barrier detection and protected `Player.STANDING_DIMENSIONS` in scale calculation. Split them. First inspect the exact 26.2 public two-hand access API and adapt only barrier-item detection if a one-to-one replacement is proven; do not touch the standing-dimensions/scale unit in the same hypothesis.
7. `MixinClientPacketListener.java` also has two errors around client creation/placement of the real `SHIP_MOUNTING_ENTITY_TYPE`. Treat entity spawn/placement as a separate lifecycle-sensitive unit; do not guess a spawn reason or placement API merely to compile.
8. `MixinLevelChunk.java` remains lifecycle/storage sensitive and must be split by error class before mutation. Optional compat (`Immersive Portals`, FTB Chunks, OptiFine) is not the first target merely because it has many errors.
9. After any bounded mutation, run exact canonical standalone P1 compile, classify the first primary javac pass from the uploaded artifact, and update this ledger at the next meaningful proven boundary.
10. Remain P1. No ordinary compile/debug video.
