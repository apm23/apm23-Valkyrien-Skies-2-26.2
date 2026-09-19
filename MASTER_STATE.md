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

## Current reconciliation — DistanceManager / TicketStorage read boundary proven and frozen

### Exact source/API boundary

The pinned VS2 server-level mixin only needs to answer whether a chunk currently has any active ticket at two existing read sites. Minecraft 26.2 moved ticket storage out of the old `DistanceManager.tickets` map into `TicketStorage`.

Frozen adaptation:
- `DistanceManagerAccessor` now exposes `@Accessor("ticketStorage") TicketStorage getTicketStorage()` instead of the obsolete ticket-map accessor.
- Existing ticket-presence checks use `TicketStorage.getTickets(long).isEmpty()` and preserve the original positive/negative membership meaning.
- The load-side chunk key uses current Minecraft 26.2 `ChunkPos.pack()` rather than removed `ChunkPos.toLong()`.
- This packed-key rename is independently consistent with the already-frozen `ChunkPos` 26.2 adaptation used by `SeamlessChunksManager`.
- No ticket type, radius, add/remove lifecycle, distance-manager flush/order, unload timing, ship lifecycle, movement, physics, collision, entity dragging, camera, or authority semantics were changed.

Implementation/proof ancestry:
- initial ticket-storage bridge and import repair culminated in `e79d2ca8f0a8d159f8df051cdadb4ba0a1fb21e3`.
- exact source/probe correction for the 26.2 packed chunk key: `8a338f95103227ed6a5acb35804d573bbae0d96c` (`p1: use 26.2 packed chunk key for ticket lookup`).
- bounded proof-classifier HEAD: `ca07a2fff0fd922cbbd578a0531d3377313827de`. The classifier was narrowed to the accessor and exact two ticket-read sites because `MixinServerLevel.java` also contains independent API drift; this did not change VS2 source semantics.

### Exact-head exhaustive proof

- P0 provenance run `35463018487`, job `105950149680`, completed `success`; exact upstream pin/tree remained unchanged.
- Ticket-storage proof run `35463018541`, job `105950149775`, completed `success`.
- Artifact: `p1-distance-manager-ticket-storage-probe-ca07a2fff0fd922cbbd578a0531d3377313827de`, ID `10590562117`, size `40466` bytes, SHA-256 `269700efd41b44176ebce58c282a22a8a6af64b69fe39c532607548663ced2ee`.
- Full Gradle standalone status remains `1`; the exhaustive artifact contains `876` unrelated `error:` diagnostics and **no javac cap marker**.
- The bounded ticket-storage semantic unit is compiler-clean. The remaining compile failures are independent clusters and must not be folded into this frozen boundary.

Negative/repair evidence preserved:
- run `35460435968` exposed a real target error in `MixinServerLevel`: removed `ChunkPos.toLong()` at the ticket-read site; this was not merely a classifier false negative.
- after `8a338f95103227ed6a5acb35804d573bbae0d96c`, source target diagnostics were gone but the proof still went red because the classifier treated every unrelated `MixinServerLevel.java` diagnostic as ticket-storage failure.
- `ca07a2fff0fd922cbbd578a0531d3377313827de` repaired only that proof granularity and the exact-head proof passed.

No video was recorded because this is compile/API closure, not a closure-ready user-visible runtime blocker.

## Frozen entity renderer submit lifecycle

- Inspection-only commit `372088cd2a5b043b81b4b4bbaca0bf2f1ce103b0`; renderer API inspection run `35457489250`, success.
- Inspection artifact `10588459495`, size `37519`, SHA-256 `2d0b54947fc3fda5b0e89fed33e12b96dd2fdfdf2f4c90d47befbb7f43e02636`.
- Implementation `a87512437f40a3bfa1325d78f8e2588587ec7cc8`; fail-closed overlay `scripts/apply_p1_entity_renderer_submit_26_2.py`.
- Proof HEAD `58d8554ba623896d486b91f18771df9bdcd6f2b3`; P0 `35458380219` / job `105937635998`, success; proof `35458380245` / job `105937636148`, success.
- Artifact `10589560814`, size `40827`, SHA-256 `24adfcc02c965648f547820f02b80095eb20025f6048833e7117b4f25c64bb22`.
- Target files `MixinEntityRenderDispatcher.java`, `MixinEntityRenderer.java`, `MixinEntityRenderState.java`, `EntityRendererCullingInvoker.java`, and `VSEntityRenderStateContext.java` had zero diagnostics under exhaustive javac; 882 unrelated errors remained at that proof point.
- Existing real VS2 render authorities (`ClientShip`, `ShipMountedToData`, `VSEntityManager`, ship transforms) remain authoritative. No movement/camera/collision/gameplay authority was introduced.

## Frozen entity local-authority / interpolation boundary

- Pinned semantic unit: `VSGamePackets.kt` + `EntityDragger.kt`.
- Implementation `b7e583af13598b6ddcc583380872f578b8a40bb8`; proof HEAD `9f2719be070e79b91b7f47ceddaec61d7f5cff40`.
- P0 `35455551709` / job `105930062007`, success; authority probe `35455551701` / job `105930062029`.
- Artifact `10588037512`, size `21648`, SHA-256 `c6d6557bababe5543957c846ffcd85623897bec849bae4291d93bb50284992a8`.
- Frozen bridge: `isControlledByLocalInstance` -> `isLocalInstanceAuthoritative()` at the exact existing sites; old non-living `lerpTo(..., 3)` -> current vanilla `moveOrInterpolateTo(Vec3(...), yaw, pitch)`.
- `IEntityDraggingInformationProvider`, `draggingInformation`, existing ship-relative/world transforms, and `lerpSteps = 3` remain authority. No synthetic carry/inertia, fake gravity, clamps, camera forcing, duplicate movement authority, or per-tick teleport/setPos chase is authorized.

## Other frozen proofs

### Optional Create deployer helper isolated from standalone P1
- implementation `cd2434e69caf28e12560bf4444fc220a3023e40b`.
- P0 `35454908696` / job `105928361982`, success; probe `35454908850` / job `105928362519`.
- artifact `10588156201`, SHA-256 `6d1516425d4c28755bffea02de77d8a5622f576fbf449b2573bfcc7aabfa45e6`.
- exactly one unreferenced helper is excluded under `sourceSets.main.java`: `org/valkyrienskies/mod/compat/create/DeployerScrollOptionSlot.kt`.
- failed hypothesis `3bcbf90c75dc4d02448cfdb4590cc9c9674e0ed6` / run `35454717409`: Kotlin source-set exclusion does not filter the file physically under `src/main/java`; do not replay without new evidence.

### Optional Sable Companion compile boundary
- overlay `58bd44154c20f141969b758b8e35372d982ac358`; proof HEAD `c0c1efb790c31f90c8916121f7c4a06864a58b7f`.
- P0 `35454031928` / job `105926053661`, success; probe `35454031987` / job `105926053824`.
- artifact `10587876899`, SHA-256 `b672943267368cd4adb06cc686808a2c2c6c79680dae69febe1447721c494f09`.
- proven compile-only boundary: `dev.ryanhcode.sable-companion:sable-companion-common-1.21.1:1.6.0`. No 1.21.1 Sable runtime compatibility claim exists.

### Renderer handler render-state boundary
- overlay `6a13ff6d1f730678d9dd793f575887c08792b161`; proof HEAD `6aa93ba02e830fa432f0b6e00185ea533227e967`.
- P0 `35452733152` / job `105922599182`, success; probe `35452733162` / job `105922599245`.
- artifact `10587053238`, SHA-256 `ae32e69c0556e903e813e317b6cca848acc0a4554ca0014ef1231fe51b7accd2`.
- frozen handler contract uses `EntityRenderer<T,S>`, `S : EntityRenderState`, and `getRenderOffset(renderState)` while preserving upstream VS2 transform math.

### ShipSavedData persistence boundary
- implementation `f2b3ec68e0d2146bb8b443da76a62a4766e01fce`.
- P0 `35451366274` / job `105918982071`, success; probe `35451366140` / job `105918981784`.
- artifact `10586956459`, SHA-256 `7921227c49729f5b23f8d54d19204ee5b1965c38506b59ad6da9ba3e8b4b234f`.
- overworld `SavedDataStorage` remains persistence authority; `SavedDataType + Codec` replaces obsolete API boundary only. Legacy root-path migration is not proven.

### Real VS2 ship chunk-ticket lifecycle
- implementation `65a42e782de192f27d5bf720691d6e08f395a719`.
- P0 `35450402081` / job `105916444806`, success; probe `35450402031` / job `105916444686`.
- artifact `10585479315`, SHA-256 `4443fd49b99f2fed5b44ee21529b543c503b4ff8494d6ca45b06572aaf9ceede`.
- frozen semantics: load-only radius-zero explicit ticket add/remove lifecycle, distance-manager flush/order, ship-alive removal guard, and `tryMarkSaved()` deletion cleanup.
- The newly frozen TicketStorage read boundary does not modify or supersede this lifecycle proof.

## Frozen proof ancestry / negative evidence

All frozen-green and negative-evidence records in Git history remain binding. Ledger compaction does not unfreeze or supersede them.

Key frozen implementation ancestry:
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

Locked negative evidence:
- `3bcbf90c75dc4d02448cfdb4590cc9c9674e0ed6` / run `35454717409`: wrong Kotlin-source-set exclusion for `DeployerScrollOptionSlot.kt`.
- `a72aaef8eca34a352ef949eeb57e6bbcda81171f`: `setUnsaved(false)` is invalid current API; do not replay absent direct new evidence.
- VSKeyBindings failed probes `e108526cbd728454c175c76bffc610d4e074da49`, `fcc65187d79c4b546883875da3597345db1e01cd`, `e9a3efd58acb2af9539628eb2875e6cb829c3cec`, `fb3c7e65a4c2089f6fa695114734d14836bde1d3` remain negative evidence.
- retired `apm23/VS2-Create_Interactive` workarounds remain historical warning evidence only and are forbidden as implementation source.

## Remaining Java compile frontier

The exact `ca07a2...` ticket-storage artifact leaves `876` exhaustive javac diagnostics. These are evidence only; they are not permission to batch-fix categories.

1. **Shipyard-entity teleport API drift — next candidate, inspection first**
   - `MixinEntity.java`, `MixinServerPlayer.java`, and `MixinServerGamePacketListenerImpl.java` contain removed/relocated `RelativeMovement` and old teleport signatures.
   - This is authority-sensitive. Inspect exact Minecraft 26.2 classes/descriptors before any source adaptation.
2. **AI/entity package and nested-goal drift**
   - bee/entity goals and villager behavior mixins expose changed symbols/packages.
3. **Other client/render/HUD/shader drift**
   - block-entity/debug/pathfinding renderer lifecycles plus old `ResourceLocation`, `GuiGraphics`, `LightTexture`, `MultiBufferSource`, shader `Uniform`, and related vocabulary.
4. **Chunk/worldgen/server storage/API drift**
   - `ChunkSerializer`, `GenerationStep.Carving`, `ChunkTaskPriorityQueueSorter`, `DimensionDataStorage`, `BlockUtil`, and related changes.
5. **Optional compatibility/dependency residue**
   - old Create 1.20.1 compile-only and ETF classfiles can produce intermediary attachment failures;
   - Sable Java mixins still expose runtime Sable references beyond the frozen lightweight Companion compile boundary.

The TicketStorage / DistanceManager read boundary is frozen and is no longer part of the active frontier.

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
- active_proof_head: `ca07a2fff0fd922cbbd578a0531d3377313827de; DistanceManager/TicketStorage active-ticket read boundary compiler-clean under exhaustive javac diagnostics`
- active_proof_run: `P0 35463018487 / job 105950149680 success; ticket-storage proof 35463018541 / job 105950149775 success; artifact 10590562117; 876 unrelated javac errors remain; no cap marker`
- active_hypothesis: `none selected after ticket-storage freeze; next candidate is authority-sensitive shipyard teleport API drift, after this ledger HEAD passes exact-head P0`
- final_ready: `false`
- user_runtime_validation: `NOT_APPLICABLE_YET`
- video_status: `NOT_APPLICABLE_YET`

## Engineering locks

- First-failure classification stays factual: provenance, build/mappings/API/loader/mixin/VSCore-native/networking/storage/transforms/rendering/collision/entity-player-camera/Create/SNR-Copycats/CI/final packaging.
- Make one evidence-backed root/semantic change at a time.
- Standalone real VS2 P1 must initialize before Create integration.
- Frozen TicketStorage read bridge is read-only compatibility; it may not be expanded into a replacement ticket lifecycle.
- Frozen real ship-ticket lifecycle remains the add/remove/load authority.
- Frozen renderer submit/state bridge may not be expanded into movement/camera/collision/gameplay authority.
- Frozen authority/interpolation bridge may not be expanded into a custom movement/carry system.
- Frozen Sable proof is compile-only and does not authorize bundling a 1.21.1 Sable runtime on 26.2.
- Frozen Create helper exclusion is P1 compile isolation only, not P3.
- Frozen ShipSavedData proof authorizes only its `SavedDataType + Codec` bridge and matching server acquisition change.
- Teleport/`RelativeMovement` drift is authority-sensitive: inspect exact 26.2 API before adapting; do not infer a movement substitute from compile errors.
- `FINAL_READY` is forbidden from CI alone.
- Video is closure-only and must not be used for ordinary compile/debug hypothesis testing.

## next_safe_action

1. Preserve ticket-storage implementation `8a338f95103227ed6a5acb35804d573bbae0d96c`, proof/classifier HEAD `ca07a2fff0fd922cbbd578a0531d3377313827de`, frozen ship-ticket lifecycle `65a42e782de192f27d5bf720691d6e08f395a719`, renderer/authority proofs, and every prior frozen-green / negative-evidence boundary.
2. This ledger-only freeze commit is not source proof. Require exact-head P0 provenance success for the resulting ledger HEAD before any further source/workflow mutation.
3. After that gate, choose exactly one remaining Java semantic cluster. Do not batch the `876` diagnostics.
4. Preferred next action: **inspection-only** probe of the shipyard teleport API drift in `MixinEntity.java`, `MixinServerPlayer.java`, and `MixinServerGamePacketListenerImpl.java`.
5. Inspect the exact Minecraft 26.2 location/type of `RelativeMovement` (or its replacement) and exact teleport-related method descriptors used by those three pinned upstream mixins. Fail closed on ambiguous class discovery.
6. Do not patch movement/teleport source until that exact inspection provides a bounded compatibility mapping. Do not alter VS2 dragging/reference-space authority, setPos behavior, carry velocity, camera, collision, or ship transforms.
7. Do not combine teleport inspection with AI, renderer/HUD/shader, chunk/worldgen, Sable, Create/ETF, or any other category.
8. Remain standalone P1. Do not use Create/SNR/Copycats to hide real VS2 failures. Do not record ordinary compile/debug video.

## Video and milestone gate

- `M1_COMPLETE` is forbidden until full P2 real-VS2 runtime proof exists: real ship lifecycle, translation+rotation, ship-space, collision, standing/walking, jump-airborne-natural landing, floor/walls/ceiling, free stable camera/look, entity dragging/reference space, rendering, and client/server sync.
- `FINAL_BUILD`, `FINAL_VERIFY`, and `FINAL_READY` are not applicable during P1.
