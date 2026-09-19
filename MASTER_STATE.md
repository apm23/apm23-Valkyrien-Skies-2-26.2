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

## Current reconciliation — entity renderer submit lifecycle proven and frozen

### Exact source/API inspection

The previous authority/interpolation proof exposed the Java renderer frontier. The bounded renderer lifecycle was then inspected against the exact Minecraft 26.2 compile classpath rather than guessed from names.

- Inspection-only commit: `372088cd2a5b043b81b4b4bbaca0bf2f1ce103b0` (`ci: inspect Minecraft 26.2 renderer dispatcher API`).
- Exact renderer API inspection run: `35457489250`, completed `success`.
- Inspection artifact: `p1-render-dispatcher-api-probe-372088cd2a5b043b81b4b4bbaca0bf2f1ce103b0`, ID `10588459495`, size `37519` bytes, SHA-256 `2d0b54947fc3fda5b0e89fed33e12b96dd2fdfdf2f4c90d47befbb7f43e02636`.
- The exact 26.2 dispatcher lifecycle is split across entity-state extraction and submission. The old pinned `EntityRenderDispatcher.render(Entity, ...)` / `MultiBufferSource` hook cannot be preserved by blind descriptor replacement.

### Frozen implementation

- Implementation commit: `a87512437f40a3bfa1325d78f8e2588587ec7cc8` (`p1: adapt entity renderer dispatcher submit lifecycle`).
- Fail-closed overlay: `scripts/apply_p1_entity_renderer_submit_26_2.py`.
- The overlay adapts only the renderer semantic unit around the pinned upstream shipyard-entity rendering path:
  - `MixinEntityRenderDispatcher.java`;
  - `MixinEntityRenderer.java`;
  - `MixinEntityRenderState.java`;
  - `VSEntityRenderStateContext.java`;
  - `EntityRendererCullingInvoker.java`;
  - matching registrations in `valkyrienskies-common.mixins.json`.
- It preserves the real upstream VS2 render authorities: `ClientShip`, `ShipMountedToData`, `VSEntityManager`, and the existing ship render transforms.
- The existing VS2 entity + partial-tick context is carried through current `EntityRenderState` only so the same upstream ship-space rendering semantics can be applied at the new 26.2 submit boundary.
- It does **not** add or change movement authority, carry velocity, physics, collision, entity dragging, teleport behavior, camera forcing, or any replacement reference-frame system.

### Exhaustive proof

- Probe validation quoting fix: `43097c8cc7e334a178f97fb289d65065f95e04a0`.
- Exact exhaustive proof HEAD: `58d8554ba623896d486b91f18771df9bdcd6f2b3` (`ci: make renderer submit proof exhaustive`).
- Exact-head P0: run `35458380219`, job `105937635998`, completed `success`; pinned upstream identity remained unchanged.
- Renderer submit proof: run `35458380245`, job `105937636148`, completed `success`.
- Artifact: `p1-entity-renderer-submit-probe-58d8554ba623896d486b91f18771df9bdcd6f2b3`, ID `10589560814`, size `40827` bytes, SHA-256 `24adfcc02c965648f547820f02b80095eb20025f6048833e7117b4f25c64bb22`.
- The proof raises javac's diagnostic ceiling to 10000 and rejects a capped diagnostic stream.
- Exact artifact review found `882` unrelated `error:` diagnostics and **no javac cap marker**.
- Exact target-file compiler-error count is zero for all five bounded renderer source files:
  - `MixinEntityRenderDispatcher.java` — 0;
  - `MixinEntityRenderer.java` — 0;
  - `MixinEntityRenderState.java` — 0;
  - `EntityRendererCullingInvoker.java` — 0;
  - `VSEntityRenderStateContext.java` — 0.
- Therefore the renderer submit semantic unit is compiler-clean under exhaustive diagnostics while the full standalone compile remains red on independent Java API/mixin clusters.

### Renderer proof boundary

This freezes only the entity renderer submit/state bridge described above. It does **not** prove all client rendering or runtime rendering green. In particular, `MixinBlockEntityRenderDispatcher`, debug/pathfinding render mixins, HUD/shader vocabulary, and other independent renderer diagnostics are not silently included in this proof.

No video was recorded because this is compile/API closure, not a closure-ready user-visible runtime blocker. Do not revisit this frozen renderer submit unit absent direct regression evidence or new exact Minecraft API evidence.

## Immediately preceding frozen proof — entity local-authority/interpolation boundary

Pinned source semantic unit:
- `common/src/main/kotlin/org/valkyrienskies/mod/common/networking/VSGamePackets.kt`;
- `common/src/main/kotlin/org/valkyrienskies/mod/common/util/EntityDragger.kt`.

Frozen semantics remain binding:
- incoming ship-motion / mob-rotation corrections must not override a locally authoritative entity;
- existing VS2 ship-relative -> world transforms remain unchanged;
- `IEntityDraggingInformationProvider` / `draggingInformation` remains the VS2 dragging/interpolation authority;
- `entity.draggingInformation.lerpSteps = 3` remains intact;
- no existing upstream `setPos`, `setDeltaMovement`, `push`, teleport-related code, or bounding-box write was augmented into a chase/carry substitute.

Proven bridge:
- `entity.isControlledByLocalInstance` -> `entity.isLocalInstanceAuthoritative()` at the two packet sites and one dragging site;
- old non-living `lerpTo(..., 3)` call -> current vanilla `moveOrInterpolateTo(Vec3(...), yaw, pitch)`;
- implementation `b7e583af13598b6ddcc583380872f578b8a40bb8`;
- proof HEAD `9f2719be070e79b91b7f47ceddaec61d7f5cff40`;
- P0 `35455551709` / job `105930062007`, success;
- authority probe `35455551701` / job `105930062029` reached `:common:compileJava` after Kotlin became compiler-clean;
- artifact `10588037512`, size `21648`, SHA-256 `c6d6557bababe5543957c846ffcd85623897bec849bae4291d93bb50284992a8`;
- old `isControlledByLocalInstance` and unresolved `lerpTo` diagnostics are absent.

This proof does not authorize synthetic carry/inertia, fake gravity, clamps, camera forcing, duplicate movement authority, or per-tick teleport/setPos chase.

## Remaining Java compile frontier

The exhaustive renderer proof confirms that the standalone build still has many independent Java API/mixin adaptation clusters. They must remain separated.

1. **Ticket / distance-manager API drift**
   - `DistanceManagerAccessor.java`: old `Ticket<?>` generic usage conflicts with current non-generic `Ticket`.
   - This is separate from the already-frozen ship-ticket lifecycle semantics.

2. **Shipyard-entity teleport API drift**
   - `MixinEntity.java`, `MixinServerPlayer.java`, and `MixinServerGamePacketListenerImpl.java` contain removed/relocated `RelativeMovement` and old teleport signatures.
   - This is authority-sensitive and must be handled as one inspected semantic unit only when selected.

3. **AI/entity package and nested-goal drift**
   - bee/entity goals and villager behavior mixins expose changed symbols/packages.

4. **Other client/render/HUD/shader drift**
   - includes block-entity/debug/pathfinding renderer lifecycles plus old `ResourceLocation`, `GuiGraphics`, `LightTexture`, `MultiBufferSource`, shader `Uniform`, and related vocabulary.
   - The frozen entity renderer submit proof does not cover these independent sites.

5. **Chunk/worldgen/server storage/API drift**
   - includes `ChunkSerializer`, `GenerationStep.Carving`, `ChunkTaskPriorityQueueSorter`, `DimensionDataStorage`, `BlockUtil`, and related changes.

6. **Optional compatibility/dependency residue**
   - old Create 1.20.1 compile-only and ETF classfiles can produce intermediary attachment failures;
   - Sable Java mixins still expose runtime Sable references beyond the already-frozen lightweight Companion compile boundary.
   - These are not permission to pull Create/Sable runtime architecture into standalone P1.

The `882` exhaustive javac diagnostics are evidence of remaining work, not permission to batch-fix categories.

## Other frozen proofs

### Optional Create deployer helper isolated from standalone P1
- Corrected implementation `cd2434e69caf28e12560bf4444fc220a3023e40b`.
- P0 `35454908696` / job `105928361982`, success.
- Probe `35454908850` / job `105928362519`.
- Artifact `10588156201`, SHA-256 `6d1516425d4c28755bffea02de77d8a5622f576fbf449b2573bfcc7aabfa45e6`.
- Exactly one unreferenced helper is excluded under `sourceSets.main.java`: `org/valkyrienskies/mod/compat/create/DeployerScrollOptionSlot.kt`.
- Upstream source remains pinned and must be revisited legitimately in P3.
- Failed hypothesis `3bcbf90c75dc4d02448cfdb4590cc9c9674e0ed6` / run `35454717409`: placing this exclusion under `sourceSets.main.kotlin` does not filter the file physically owned by `src/main/java`; do not replay without new source-layout evidence.

### Optional Sable Companion compile boundary
- Overlay `58bd44154c20f141969b758b8e35372d982ac358`.
- Proof HEAD `c0c1efb790c31f90c8916121f7c4a06864a58b7f`.
- P0 `35454031928` / job `105926053661`, success.
- Probe `35454031987` / job `105926053824`.
- Artifact `10587876899`, SHA-256 `b672943267368cd4adb06cc686808a2c2c6c79680dae69febe1447721c494f09`.
- Proven compile-only boundary: `dev.ryanhcode.sable-companion:sable-companion-common-1.21.1:1.6.0`.
- No claim exists that a Minecraft-1.21.1 Sable runtime works on 26.2; no fake local companion/stub is allowed.

### Renderer handler render-state boundary
- Overlay `6a13ff6d1f730678d9dd793f575887c08792b161`.
- Proof HEAD `6aa93ba02e830fa432f0b6e00185ea533227e967`.
- P0 `35452733152` / job `105922599182`, success.
- Probe `35452733162` / job `105922599245`.
- Artifact `10587053238`, SHA-256 `ae32e69c0556e903e813e317b6cca848acc0a4554ca0014ef1231fe51b7accd2`.
- Frozen handler contract uses `EntityRenderer<T,S>`, `S : EntityRenderState`, and `getRenderOffset(renderState)` while preserving VS2 render-transform math and authority.

### ShipSavedData persistence boundary
- Implementation `f2b3ec68e0d2146bb8b443da76a62a4766e01fce`.
- P0 `35451366274` / job `105918982071`, success.
- Probe `35451366140` / job `105918981784`; artifact `10586956459`, SHA-256 `7921227c49729f5b23f8d54d19204ee5b1965c38506b59ad6da9ba3e8b4b234f`.
- Overworld `SavedDataStorage` remains the single persistence authority; current `SavedDataType + Codec` replaces obsolete API boundaries only.
- Legacy 1.21.1 root-path `vs_ship_data.dat` automatic migration is not proven and must not be guessed.

### Real VS2 ship chunk-ticket lifecycle
- Implementation `65a42e782de192f27d5bf720691d6e08f395a719`.
- P0 `35450402081` / job `105916444806`, success.
- Probe `35450402031` / job `105916444686`; artifact `10585479315`, SHA-256 `4443fd49b99f2fed5b44ee21529b543c503b4ff8494d6ca45b06572aaf9ceede`.
- Frozen semantics: load-only radius-zero explicit ticket add/remove lifecycle, distance-manager flush/order, ship-alive removal guard, and `tryMarkSaved()` deletion cleanup.

## Frozen proof ancestry / negative evidence

All frozen-green and negative-evidence records in Git history remain binding. Ledger compaction does not unfreeze or supersede them.

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
- `3bcbf90c75dc4d02448cfdb4590cc9c9674e0ed6` / run `35454717409`: wrong Kotlin-source-set exclusion for `DeployerScrollOptionSlot.kt`.
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
- active_proof_head: `58d8554ba623896d486b91f18771df9bdcd6f2b3; entity renderer submit/state semantic unit compiler-clean under exhaustive javac diagnostics`
- active_proof_run: `P0 35458380219 / job 105937635998 success; renderer submit proof 35458380245 / job 105937636148 success; artifact 10589560814; 882 unrelated javac errors remain and target renderer files have zero errors`
- active_hypothesis: `none selected after renderer-submit freeze; next candidate is the isolated DistanceManagerAccessor Ticket generic API drift after this ledger HEAD passes exact-head P0`
- final_ready: `false`
- user_runtime_validation: `NOT_APPLICABLE_YET`
- video_status: `NOT_APPLICABLE_YET`

## Engineering locks

- First-failure classification stays factual: provenance, build/mappings/API/loader/mixin/VSCore-native/networking/storage/transforms/rendering/collision/entity-player-camera/Create/SNR-Copycats/CI/final packaging.
- Make one evidence-backed root/semantic change at a time.
- Standalone real VS2 P1 must initialize before Create integration.
- Frozen renderer submit/state bridge may not be expanded into movement/camera/collision/gameplay authority.
- Frozen authority/interpolation bridge may not be expanded into a custom movement/carry system.
- Frozen Sable proof is compile-only and does not authorize bundling a 1.21.1 Sable runtime on 26.2.
- Frozen Create helper exclusion is P1 compile isolation only, not P3.
- Frozen ticket lifecycle proof authorizes only its exact add/remove/load semantics; `DistanceManagerAccessor` generic drift is a separate API issue.
- Frozen ShipSavedData proof authorizes only its `SavedDataType + Codec` bridge and matching server acquisition change.
- `FINAL_READY` is forbidden from CI alone.
- Video is closure-only and must not be used for ordinary compile/debug hypothesis testing.

## next_safe_action

1. Preserve renderer implementation `a87512437f40a3bfa1325d78f8e2588587ec7cc8`, exhaustive proof HEAD `58d8554ba623896d486b91f18771df9bdcd6f2b3`, authority implementation `b7e583af13598b6ddcc583380872f578b8a40bb8`, and every prior frozen-green / negative-evidence boundary.
2. This ledger-only freeze commit is not source proof. Require exact-head P0 provenance success for the resulting ledger HEAD before any further source mutation.
3. After that gate, choose exactly one remaining Java semantic cluster from the exhaustive renderer artifact. Do not batch the `882` diagnostics.
4. Preferred next bounded cluster: `DistanceManagerAccessor.java` only, starting with exact pinned upstream semantics and exact Minecraft 26.2 `Ticket` / distance-manager API inspection. The known first drift is old `Ticket<?>` versus current non-generic `Ticket`.
5. Do not modify the already-frozen ship ticket add/remove lifecycle while resolving the accessor type surface unless direct exact evidence proves a semantic dependency.
6. Do not combine this accessor work with teleport/`RelativeMovement`, AI packages, renderer/HUD/shader sites, chunk/worldgen, Sable, Create/ETF cleanup, or any other diagnostic category.
7. Remain standalone P1. Do not use Create/SNR/Copycats to hide real VS2 failures. Do not record ordinary compile/debug video.

## Video and milestone gate

- `M1_COMPLETE` is forbidden until full P2 real-VS2 runtime proof exists: real ship lifecycle, translation+rotation, ship-space, collision, standing/walking, jump-airborne-natural landing, floor/walls/ceiling, free stable camera/look, entity dragging/reference space, rendering, and client/server sync.
- `FINAL_BUILD`, `FINAL_VERIFY`, and `FINAL_READY` are not applicable during P1.
- `FINAL_READY` still requires exact-final-JAR real-user runtime acceptance.
