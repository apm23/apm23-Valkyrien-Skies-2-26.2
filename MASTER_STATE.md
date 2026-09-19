# MASTER_STATE — REAL VS2 26.2 PORT

GitHub code is the implementation source of truth. This file is the durable continuity ledger; chat memory is not authoritative.

## Project identity

- Repository: `apm23/apm23-Valkyrien-Skies-2-26.2`
- Mission: port the **actual original Valkyrien Skies 2 source** to Minecraft Java/Fabric 26.2, then integrate Create Fly / Steam 'n' Rails / Copycats only after standalone real VS2 is proven.
- Hard contract: **VS2 ASLI. BUKAN SYSTEM MIRIP VS2.**
- Architecture contract: `PORT_CONTRACT.md`.
- Exact dependency/environment lock: `BASELINE_LOCK.json`.
- Upstream provenance: `UPSTREAM_PROVENANCE.md`.

## Authoritative upstream baseline

- repository: `ValkyrienSkies/Valkyrien-Skies-2`
- branch used to select baseline: `1.21.1/main`
- exact commit: `f39132148e717d325933b4ce6e9e9fb13d929390`
- exact root tree: `91116399605d3ecd1c93b0011560e09281ee1fa4`
- upstream mod version: `2.4.12`
- imported as git submodule/gitlink `upstream-vs2/`

The upstream baseline remains pinned. Minecraft 26.2 changes are applied by explicit fail-closed overlays so every adaptation remains traceable to upstream VS2 source.

## Current reconciliation — entity local-authority/interpolation boundary proven and frozen

### Source semantic unit

Pinned upstream files inspected together:
- `common/src/main/kotlin/org/valkyrienskies/mod/common/networking/VSGamePackets.kt`
- `common/src/main/kotlin/org/valkyrienskies/mod/common/util/EntityDragger.kt`

Exact previous standalone Kotlin residue from corrected optional-Create probe `35454908850` was only:
- `VSGamePackets.kt:78`: removed `Entity.isControlledByLocalInstance`;
- `VSGamePackets.kt:132`: removed `Entity.lerpTo`;
- `VSGamePackets.kt:142`: removed `Entity.isControlledByLocalInstance`;
- `EntityDragger.kt:148`: removed `Entity.isControlledByLocalInstance`.

Pinned VS2 semantics at these sites are authority-sensitive and remain binding:
- incoming entity ship-motion / mob-rotation corrections must not override a locally authoritative entity;
- the existing real VS2 ship-relative -> world transforms remain unchanged;
- `IEntityDraggingInformationProvider` / `draggingInformation` remains the VS2 dragging/interpolation state authority;
- `entity.draggingInformation.lerpSteps = 3` remains unchanged;
- `EntityDragger` retains the upstream split between remote non-player interpolation and the existing local/player drag behavior;
- existing upstream `setPos`, `setDeltaMovement`, `push`, teleport-related code, and bounding-box writes are not replaced or augmented by this bridge.

Exact Minecraft 26.2 API/source inspection established the minimal vanilla boundary:
- public current local-instance authority predicate: `Entity.isLocalInstanceAuthoritative()`;
- `isLocalClientAuthoritative()` exists but is protected and is not used as an external VS2 helper call;
- current public entity movement/interpolation entry: `moveOrInterpolateTo(Vec3 position, float yRot, float xRot)`;
- this keeps interpolation behavior inside current vanilla entity/interpolation handling rather than inventing a VS2-side teleport chase or synthetic carry system.

### Proven implementation

- Fail-closed source overlay: `b7e583af13598b6ddcc583380872f578b8a40bb8` (`P1: add entity authority interpolation overlay`).
- Exact proof harness HEAD: `9f2719be070e79b91b7f47ceddaec61d7f5cff40` (`ci: probe entity authority interpolation bridge`).
- Exact-head P0: run `35455551709`, job `105930062007`, completed `success`; exact pinned upstream identity remained unchanged.
- Authority probe: run `35455551701`, job `105930062029`, completed `failure` only after Kotlin became compiler-clean and `:common:compileJava` exposed the next independent Java API/mixin drift.
- Diagnostic artifact: `p1-entity-authority-probe-9f2719be070e79b91b7f47ceddaec61d7f5cff40`, artifact ID `10588037512`, size `21648` bytes, ZIP SHA-256 `c6d6557bababe5543957c846ffcd85623897bec849bae4291d93bb50284992a8`.
- Exact artifact log timeline: `:common:compileKotlin` runs successfully; `:common:compileJava` is then reached and fails with javac diagnostics.
- Exact artifact log contains **zero** occurrences of `isControlledByLocalInstance` and zero unresolved `lerpTo` diagnostics.

The bridge is exactly:
- `entity.isControlledByLocalInstance` -> `entity.isLocalInstanceAuthoritative()` at the two packet sites and one dragging site;
- the old non-living packet call `entity.lerpTo(worldPosition..., yaw, pitch, 3)` -> current vanilla `entity.moveOrInterpolateTo(Vec3(worldPosition...), yaw, pitch)`;
- the existing VS2 `draggingInformation.lerpSteps = 3` remains intact.

The overlay is fail-closed on exact call counts and semantic anchors. It also verifies that counts of the existing authority-sensitive operations `setPos(`, `setDeltaMovement(`, `.push(`, `teleport`, and `boundingBox =` are unchanged by this adaptation.

### Authority proof boundary

This proof is **only** the current vanilla local-authority/interpolation API bridge into existing VS2 packet/entity-dragging architecture. It does not authorize:
- per-tick teleport or `setPos` chase;
- synthetic carry velocity/inertia;
- fake gravity;
- manual floor/wall/ceiling clamps;
- camera forcing/counter-rotation;
- duplicate movement authority;
- replacing real VS2 entity-dragging/reference-space semantics.

No video was recorded because this is compile/API proof, not closure-ready runtime evidence.

## Newly exposed Java compile frontier

With the Kotlin authority blocker removed, exact probe `35455551701` reaches `:common:compileJava` for the first time in this chain and javac stops after its 100-error diagnostic cap. This is a new evidence frontier; absence of diagnostics beyond the cap is not proof of compatibility.

The first exact Java diagnostics reveal multiple **independent** semantic clusters. They must not be patched together:

1. **Entity/render dispatcher lifecycle and renderer-state API**
   - `MixinEntityRenderDispatcher.java`: `EntityRenderer<T>` now requires two type arguments and old `MultiBufferSource` references are unresolved;
   - `MixinEntityRenderer.java`: old `MultiBufferSource`-based render hook surface is unresolved;
   - `MixinBlockEntityRenderDispatcher.java`: `BlockEntityRenderer<E>` now requires two type arguments;
   - other debug/pathfinding render mixins also contain old `MultiBufferSource` surfaces.
   The earlier frozen Kotlin renderer-handler proof does **not** prove these Java mixin injection lifecycles.

2. **Ticket / distance-manager API drift**
   - `DistanceManagerAccessor.java`: `Ticket<?>` is invalid because current `Ticket` is non-generic.
   This is separate from the already-frozen ship-ticket lifecycle overlay; do not edit the frozen ticket add/remove semantics merely because this accessor type drift exists.

3. **Shipyard-entity teleport API drift**
   - `MixinEntity.java`, `MixinServerPlayer.java`, and `MixinServerGamePacketListenerImpl.java` reference removed/relocated `RelativeMovement` and old teleport signatures.
   This is authority-sensitive and must be inspected as a semantic unit before any edit.

4. **AI/entity package and nested-goal drift**
   - bee goal/entity mixins cannot resolve old `net.minecraft.world.entity.animal.Bee` / nested goal locations;
   - villager behavior mixins also expose changed symbols.

5. **Client/render/HUD/shader vocabulary and lifecycle drift**
   - examples in the first 100 diagnostics include old `ResourceLocation`, `GuiGraphics`, `LightTexture`, `MultiBufferSource`, and shader `Uniform` surfaces.
   These are not permission for blind package-name replacement; exact current lifecycle/signature evidence is required.

6. **Chunk/worldgen/server storage/API drift**
   - examples include `ChunkSerializer`, `GenerationStep.Carving`, `ChunkTaskPriorityQueueSorter`, `DimensionDataStorage`, and `BlockUtil` changes.

7. **Optional compatibility/dependency residue**
   - old Create 1.20.1 compile-only classfiles and ETF compile-only classfiles produce intermediary-class attachment failures in javac;
   - Sable Java mixins still reference runtime Sable classes not supplied by the already-frozen lightweight Companion compile boundary.
   These must not be used to pull Create/Sable runtime architecture into standalone P1.

The list above is classification of the first capped javac output, not an exhaustive inventory of all remaining Java work.

## Immediately preceding frozen proof — optional Create deployer helper isolated from standalone P1

- Corrected implementation: `cd2434e69caf28e12560bf4444fc220a3023e40b`.
- P0: `35454908696` / job `105928361982`, success.
- Corrected probe: `35454908850` / job `105928362519`.
- Artifact `10588156201`, SHA-256 `6d1516425d4c28755bffea02de77d8a5622f576fbf449b2573bfcc7aabfa45e6`.
- Exactly one unreferenced helper is excluded under `sourceSets.main.java`: `org/valkyrienskies/mod/compat/create/DeployerScrollOptionSlot.kt`.
- The upstream file remains present and must be revisited legitimately in P3.
- This does not prove Create runtime compatibility or authorize P3.

Failed hypothesis locked as negative evidence:
- probe HEAD `3bcbf90c75dc4d02448cfdb4590cc9c9674e0ed6`, run `35454717409`, artifact `10588041201`, SHA-256 `86f2e0472c36dee58c7c3434b8e0dbd0f18fa5cdcddc9c99c080aabf6b2c8ece`;
- putting the exact helper exclusion in `sourceSets.main.kotlin` does not filter a `.kt` file physically owned by `src/main/java`; do not replay absent direct new source-layout evidence.

## Earlier frozen proof — optional Sable Companion compile boundary

- Overlay `58bd44154c20f141969b758b8e35372d982ac358`.
- Proof HEAD `c0c1efb790c31f90c8916121f7c4a06864a58b7f`.
- P0 `35454031928` / job `105926053661`, success.
- Probe `35454031987` / job `105926053824`.
- Artifact `10587876899`, SHA-256 `b672943267368cd4adb06cc686808a2c2c6c79680dae69febe1447721c494f09`.
- Proven compile-only boundary: `dev.ryanhcode.sable-companion:sable-companion-common-1.21.1:1.6.0`.
- No claim exists that a Minecraft-1.21.1 Sable/Companion runtime works on 26.2; no fake local companion/stub is allowed.

## Earlier frozen proof — renderer handler render-state boundary

- Overlay `6a13ff6d1f730678d9dd793f575887c08792b161`.
- Proof HEAD `6aa93ba02e830fa432f0b6e00185ea533227e967`.
- P0 `35452733152` / job `105922599182`, success.
- Probe `35452733162` / job `105922599245`; artifact `10587053238`, SHA-256 `ae32e69c0556e903e813e317b6cca848acc0a4554ca0014ef1231fe51b7accd2`.
- Frozen bridge: upstream real VS2 handler contract uses `EntityRenderer<T,S>`, `S : EntityRenderState`, and `getRenderOffset(renderState)` while preserving VS2 render-transform math and authority.
- It explicitly did not prove Java dispatcher/mixin lifecycle. Exact Java diagnostics are now finally available from run `35455551701`.

## Earlier frozen proof — ShipSavedData persistence boundary

- Implementation `f2b3ec68e0d2146bb8b443da76a62a4766e01fce`.
- P0 `35451366274` / job `105918982071`, success.
- P1 `35451366140` / job `105918981784`; artifact `10586956459`, SHA-256 `7921227c49729f5b23f8d54d19204ee5b1965c38506b59ad6da9ba3e8b4b234f`.
- Overworld `SavedDataStorage` remains the single persistence authority; current `SavedDataType + Codec` replaces only obsolete API boundaries.
- Legacy 1.21.1 root-path `vs_ship_data.dat` automatic migration is not proven and must not be guessed.

## Earlier frozen proof — real VS2 ship chunk-ticket lifecycle

- Implementation `65a42e782de192f27d5bf720691d6e08f395a719`.
- P0 `35450402081` / job `105916444806`, success.
- P1 `35450402031` / job `105916444686`; artifact `10585479315`, SHA-256 `4443fd49b99f2fed5b44ee21529b543c503b4ff8494d6ca45b06572aaf9ceede`.
- Frozen semantics: load-only radius-zero explicit ticket add/remove lifecycle, distance-manager flush/order, ship-alive removal guard, and `tryMarkSaved()` deletion cleanup.

## Frozen proof ancestry / negative evidence

All frozen-green and negative-evidence records already present in Git history remain binding. Ledger compaction does not unfreeze or supersede them. Do not replay failed probes or edit a frozen site merely because a later compiler error looks similar.

Key frozen implementation ancestry includes:
- `30b9f70d3c6c71dfd30ca76339e19cfcb56461e4`: ShipAssembler block-entity ValueInput.
- `45de97f06a3ab25c1e19b0dc09790ebde2d8e851`: ShipAssembler Clearable.
- `e923ba7658197ff04af605e85507618c09dd390b`: RelocationUtil block-entity ValueInput.
- `52a05bdae75fd2a469287234c680bf191fd5b105`: RelocationUtil pending loot-table clear.
- `7a7e2f320605b27bb65e9f0bb6cb88d8aa41a4e7`: RelocationUtil neighbor-update.
- `ce6ff8bb8f06eeb8e98544f6bf9ca1e503936fdb`: RelocationUtil direct chunk-write zero flags.
- `2da9ca25e3ce6fd2f601cc2f6b626b0e3998a677`: ShipAssembler StructureProcessor.
- `aa26d707fac479c63a6a5e097ca65818dd145262`: ShipAssembler fast-path direct chunk-write.
- `12f182325f9f3e10c502afae7da567e4b1b95c28`: AssemblyUtil neighbor dispatch.
- `644d108b111bed17d0f3259dc840803f7c9a3192`: AssemblyUtil block-entity Value I/O.
- `820ef37e8ca012fe484d9960242cbfc0eefbacc8`: AssemblyUtil ScheduledTick non-null.
- `a803150d066fdc7e0a0bfdd5bd1661b85c627417`: AssemblyUtil direct chunk-write.
- `02e356638690d0413a105d409aaae4bcfd6e160c`: ShipAssembler BlockPos -> containing ChunkPos.
- `39e2abc40af3d785d4d6ca5f14ac7b28ef03334f`: ShipMountingEntity `kill(ServerLevel)`.
- `36549552477a1dd9b24cc12c6e21c6849b2e8b54`: ShipMountingEntity `hurtServer`.
- `0a23528d781baf280bb553a8f9fa94c21f447af2`: ShipMountingEntity Value I/O.
- `d258e69e46ce2f85c1ccb953dc97db7abd669841`: entity-handler projectile packages.
- `3d8d7255d36f26da902e0d43e1c830fa5015594e`: VSGameEvents RenderType package.
- `24802fb75610a3ceb1614fda1a78cab1fab7cfe5`: VSGameUtils build-height / packed chunk-key.
- `a5e219c7036937ce0ef4b5dfe5032bd82c764ee9`: VSGameUtils ResourceKey / Identifier.
- `ee7e9c56be55fd95114d0f7e194be69185db4385`: nullable translation arguments.
- `169e0007dcbeb2263701e6b41e40757de6d62ff2`: TestChair entity creation / positioning.
- `2c763500338955135d0700b273594a87dab9d982`: VSKeyBindings Category.
- `5c8a80eca1b996c4b89d5a394d7cfb9115d3f070`: CreativeModeTab.Output access.
- `4641ae31765f0d067923cc1ef54b9a26abe99a19`: TestHingeBlockEntity Value I/O.
- `ea2084954eb4edd2bd9922aa1f59342b76709809`: MassDatapackResolver registry-tag.
- `27e181c70184b2aac38eeb1a646905d93ba45023`: MassDatapackResolver typed reload listener.
- `ac739bbf0c1598087a6ae9b158117c4764ce3079`: DimensionParametersResolver typed reload listener.
- `2af9d9ba1d48f8a0baf825398d3d441b1219f19d`: VSEntityHandlerDataLoader typed reload listener.
- `9d82234aa769a6a0eece07f52e7d5ace2d334aab`: VSGamePackets Identifier vocabulary.

Locked negative evidence includes:
- `3bcbf90c75dc4d02448cfdb4590cc9c9674e0ed6` / run `35454717409`: wrong Kotlin-source-set exclusion for `DeployerScrollOptionSlot.kt`; do not replay.
- `a72aaef8eca34a352ef949eeb57e6bbcda81171f`: `setUnsaved(false)` is invalid current API; do not replay absent direct new evidence.
- VSKeyBindings failed probes `e108526cbd728454c175c76bffc610d4e074da49`, `fcc65187d79c4b546883875da3597345db1e01cd`, `e9a3efd58acb2af9539628eb2875e6cb829c3cec`, `fb3c7e65a4c2089f6fa695114734d14836bde1d3` remain negative evidence.
- retired `apm23/VS2-Create_Interactive` workarounds remain historical warning evidence only and are forbidden as implementation source.

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
- active_blocker: `MINECRAFT_26_2_JAVA_API_MIXIN_DRIFT`
- active_proof_head: `9f2719be070e79b91b7f47ceddaec61d7f5cff40; entity local-authority/interpolation API boundary compiler-clean; common Java frontier now reached`
- active_proof_run: `P0 35455551709 / job 105930062007 success; authority probe 35455551701 / job 105930062029 reaches common compileJava; artifact 10588037512; old authority diagnostics absent`
- active_hypothesis: `none selected after authority/interpolation freeze; after this ledger-only HEAD passes exact-head P0, choose exactly one newly exposed Java semantic cluster`
- final_ready: `false`
- user_runtime_validation: `NOT_APPLICABLE_YET`
- video_status: `NOT_APPLICABLE_YET`

## Engineering locks

- First-failure classification stays factual: provenance, build/mappings/API/loader/mixin/VSCore-native/networking/storage/transforms/rendering/collision/entity-player-camera/Create/SNR-Copycats/CI/final packaging.
- Make one evidence-backed root/semantic change at a time.
- Standalone real VS2 P1 must initialize before Create integration.
- Frozen authority bridge may not be expanded into a custom movement/carry system.
- Frozen renderer-handler proof does not authorize guessed Java dispatcher injection targets.
- Frozen Sable proof is compile-only and does not authorize bundling a 1.21.1 Sable runtime on 26.2.
- Frozen Create helper exclusion is P1 compile isolation only, not P3.
- Frozen ticket proof authorizes only its exact ticket lifecycle; `DistanceManagerAccessor` generic drift is a separate API issue.
- Frozen ShipSavedData proof authorizes only its `SavedDataType + Codec` bridge and matching server acquisition change.
- `FINAL_READY` is forbidden from CI alone.
- Video is closure-only and must not be used for ordinary compile/debug hypothesis testing.

## next_safe_action

1. Preserve authority implementation `b7e583af13598b6ddcc583380872f578b8a40bb8`, proof HEAD `9f2719be070e79b91b7f47ceddaec61d7f5cff40`, and every prior frozen-green / negative-evidence boundary.
2. This ledger-only freeze commit is **not** source proof. Require exact-head P0 provenance success for the resulting ledger HEAD before any further source mutation.
3. After that gate, inspect exact artifact/log from authority probe `35455551701` and exact Minecraft 26.2 source/API for **one** newly exposed Java semantic cluster only. Do not patch multiple javac categories together merely because javac reported 100 errors.
4. Preferred next bounded cluster: the Java entity-render dispatcher lifecycle centered on `MixinEntityRenderDispatcher.java` (and only files proven to be part of the same dispatcher/render-state semantic unit). Exact evidence now exists that `EntityRenderer` type parameters and the old `MultiBufferSource`/dispatcher lifecycle changed. Inspect current `EntityRenderDispatcher` extraction/submission lifecycle and exact mixin target descriptors before any edit. Do not guess package renames or preserve obsolete render callbacks by force.
5. If exact inspection shows `MixinEntityRenderer.java` is inseparable from the same renderer-state lifecycle, handle it in the same explicitly bounded semantic unit; otherwise leave it for a later hypothesis.
6. Do not combine renderer work with `DistanceManagerAccessor`, `RelativeMovement`/teleport, AI packages, chunk/worldgen, Sable, Create/ETF dependency cleanup, or other Java diagnostics.
7. Remain standalone P1. Do not use Create/SNR/Copycats to hide real VS2 failures. Do not record ordinary compile/debug video.

## Video and milestone gate

- `M1_COMPLETE` is forbidden until full P2 real-VS2 runtime proof exists: real ship lifecycle, translation+rotation, ship-space, collision, standing/walking, jump-airborne-natural landing, floor/walls/ceiling, free stable camera/look, entity dragging/reference space, rendering, and client/server sync.
- `FINAL_BUILD`, `FINAL_VERIFY`, and `FINAL_READY` are not applicable during P1.
- `FINAL_READY` still requires exact-final-JAR real-user runtime acceptance.
