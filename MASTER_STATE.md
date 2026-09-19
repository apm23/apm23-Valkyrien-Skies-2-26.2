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

## Current reconciliation — renderer handler render-state boundary compiler-proven and frozen

- Source overlay implementation: `6a13ff6d1f730678d9dd793f575887c08792b161` (`P1: adapt entity handlers to renderer state API`).
- Exact proof harness HEAD before this ledger-only freeze: `6aa93ba02e830fa432f0b6e00185ea533227e967` (`ci: probe entity handler render state boundary`).
- The proof harness replays all 63 canonical frozen P1 overlays in canonical order, then applies only `scripts/apply_p1_entityhandler_renderstate_26_2.py` and audits the three targeted upstream handler files before compile.
- Exact-head P0 provenance for `6aa93ba02e830fa432f0b6e00185ea533227e967`: run `35452733152`, job `105922599182`, completed `success`; exact upstream identity remained pinned to `f39132148e717d325933b4ce6e9e9fb13d929390`.
- Exact renderer-state probe: run `35452733162`, job `105922599245`, completed `failure` only because independent Kotlin P1 clusters remain. Replay of the canonical frozen chain, the isolated renderer overlay, delta validation, Gradle runtime setup, and diagnostic upload all completed successfully.
- Diagnostic artifact: `p1-renderstate-probe-6aa93ba02e830fa432f0b6e00185ea533227e967`, artifact ID `10587053238`, size `4438` bytes, ZIP SHA-256 `ae32e69c0556e903e813e317b6cca848acc0a4554ca0014ef1231fe51b7accd2`.
- Exact probe run `35452733162` contains **no compiler diagnostic** for `VSEntityHandler.kt`, `AbstractShipyardEntityHandler.kt`, `WorldEntityHandler.kt`, `MultiBufferSource`, the former one-parameter `EntityRenderer<T>` handler signatures, or the former `getRenderOffset(entity, partialTicks)` calls.

### Proven renderer-handler root cause and minimal 26.2 adaptation

Pinned upstream VS2 carries the real ship rendering integration through `VSEntityHandler.applyRenderTransform`, implemented by `AbstractShipyardEntityHandler` and `WorldEntityHandler`. The upstream contract receives the real VS2 `ClientShip`, entity, vanilla renderer, camera-relative coordinates, partial tick, and `PoseStack`; ship-space/world-space transform math remains in these real VS2 handlers.

Minecraft 26.2 changed the vanilla renderer boundary:
- `EntityRenderer<T>` became `EntityRenderer<T, S>` where `S : EntityRenderState`;
- `getRenderOffset(entity, partialTicks)` became `getRenderOffset(renderState)`;
- the old `MultiBufferSource` render-boundary argument is no longer part of this handler-facing submit path.

The proven overlay therefore changes only the three handler contracts:
- imports `EntityRenderState` instead of the removed handler-side `MultiBufferSource` dependency;
- changes `applyRenderTransform` to `<T : Entity, S : EntityRenderState>` and `EntityRenderer<T, S>`;
- passes `renderState: S` through the existing handler contract;
- changes only the vanilla offset lookup to `entityRenderer.getRenderOffset(renderState)`;
- preserves the upstream real VS2 ship render transform, position transform, rotation, scaling, camera-relative translation, mounted-entity transform, movement logic, projectile logic, entity dragging behavior, and all gameplay authority.

No custom renderer, fake reference frame, duplicate transform authority, camera forcing, synthetic carry, teleport chase, or retired-project code was introduced.

### Renderer proof boundary — dispatcher lifecycle is NOT yet claimed

This freeze is intentionally narrower than the whole rendering subsystem.

Pinned upstream `MixinEntityRenderDispatcher` still targets the pre-26.2 `EntityRenderDispatcher.render(...)` lifecycle and old renderer signatures. Exact Minecraft 26.2 API inspection shows a split pipeline:
- `extractEntity(entity, partialTicks)` creates `EntityRenderState`;
- `submit(renderState, camera, x, y, z, PoseStack, SubmitNodeCollector)` performs the render submission;
- `getRenderOffset` consumes the render state;
- the old `distanceToSqr(DDD)` overload used by one upstream injection is absent from the inspected current dispatcher source.

The current exact probe never reached `:common:compileJava` because unrelated Kotlin blockers stop `:common:compileKotlin` first. Therefore **no compile-clean claim is made for `MixinEntityRenderDispatcher` yet**. Do not patch it from guesses and do not treat the three-handler proof as renderer-runtime closure. Its 26.2 lifecycle adaptation must resume from direct API semantics plus the first exact Java diagnostics once the Kotlin stage is unblocked, or from an equally exact isolated Java proof harness.

No video was recorded because this is compile/API proof, not closure-ready runtime evidence.

## Immediately preceding frozen proof — real VS2 ShipSavedData persistence boundary

- Proven implementation HEAD: `f2b3ec68e0d2146bb8b443da76a62a4766e01fce`.
- Source overlay ancestry: `7b51117fc1f0286ba7a7aea1017deed09d410d09` plus canonical P1 wiring `f2b3ec68e0d2146bb8b443da76a62a4766e01fce`.
- Exact P0: run `35451366274`, job `105918982071`, success.
- Exact P1: run `35451366140`, job `105918981784`; failure only from independent clusters, with ShipSavedData/MixinMinecraftServer persistence diagnostics absent.
- Artifact `p1-compile-log-f2b3ec68e0d2146bb8b443da76a62a4766e01fce`, ID `10586956459`, SHA-256 `7921227c49729f5b23f8d54d19204ee5b1965c38506b59ad6da9ba3e8b4b234f`.
- Frozen semantics: overworld `SavedDataStorage` remains the single authority; current `SavedDataType<ShipSavedData>` + `CompoundTag.CODEC.xmap(::load, ShipSavedData::saveToTag)` replaces only the obsolete Factory/save boundary; existing VS pipeline payload keys and fallback semantics remain unchanged.
- Legacy 1.21.1 root-path `vs_ship_data.dat` automatic file-location migration is **not** proven and must not be guessed.

## Frozen proof ancestry / negative evidence

All frozen-green and negative-evidence records already present in Git history remain binding. Ledger compaction does not unfreeze or supersede them. Do not replay failed probes or edit a frozen site merely because a later compiler error looks similar.

Explicit recent frozen implementation proofs include:
- `6a13ff6d1f730678d9dd793f575887c08792b161` + probe HEAD `6aa93ba02e830fa432f0b6e00185ea533227e967`: renderer-handler `EntityRenderer<T,S>` / `EntityRenderState` contract; P0 `35452733152` / job `105922599182`; probe `35452733162` / job `105922599245`; artifact `10587053238`; SHA-256 `ae32e69c0556e903e813e317b6cca848acc0a4554ca0014ef1231fe51b7accd2`. Dispatcher lifecycle explicitly excluded from this proof.
- `f2b3ec68e0d2146bb8b443da76a62a4766e01fce`: ShipSavedData `SavedDataType + Codec + MixinMinecraftServer` persistence boundary; P0 `35451366274` / job `105918982071`; P1 `35451366140` / job `105918981784`; artifact `10586956459`.
- `65a42e782de192f27d5bf720691d6e08f395a719`: real VS2 ship chunk-ticket lifecycle bridge; P0 `35450402081` / job `105916444806`; P1 `35450402031` / job `105916444686`; artifact `10585479315`.
- `30b9f70d3c6c71dfd30ca76339e19cfcb56461e4`: ShipAssembler block-entity ValueInput bridge.
- `45de97f06a3ab25c1e19b0dc09790ebde2d8e851`: ShipAssembler Clearable bridge.
- `e923ba7658197ff04af605e85507618c09dd390b`: RelocationUtil block-entity ValueInput bridge.
- `52a05bdae75fd2a469287234c680bf191fd5b105`: RelocationUtil pending loot-table clear proof.
- `7a7e2f320605b27bb65e9f0bb6cb88d8aa41a4e7`: RelocationUtil neighbor-update proof.
- `ce6ff8bb8f06eeb8e98544f6bf9ca1e503936fdb`: RelocationUtil direct chunk-write zero-flag proof.
- `2da9ca25e3ce6fd2f601cc2f6b626b0e3998a677`: ShipAssembler StructureProcessor proof.
- `aa26d707fac479c63a6a5e097ca65818dd145262`: ShipAssembler fast-path direct chunk-write proof.
- `12f182325f9f3e10c502afae7da567e4b1b95c28`: AssemblyUtil neighbor-dispatch proof.
- `644d108b111bed17d0f3259dc840803f7c9a3192`: AssemblyUtil block-entity Value I/O proof.
- `820ef37e8ca012fe484d9960242cbfc0eefbacc8`: AssemblyUtil ScheduledTick non-null proof.
- `a803150d066fdc7e0a0bfdd5bd1661b85c627417`: AssemblyUtil direct chunk-write proof.
- `02e356638690d0413a105d409aaae4bcfd6e160c`: ShipAssembler BlockPos -> containing ChunkPos proof.
- `39e2abc40af3d785d4d6ca5f14ac7b28ef03334f`: ShipMountingEntity `kill(ServerLevel)` proof.
- `36549552477a1dd9b24cc12c6e21c6849b2e8b54`: ShipMountingEntity `hurtServer` proof.
- `0a23528d781baf280bb553a8f9fa94c21f447af2`: ShipMountingEntity Value I/O proof.
- `d258e69e46ce2f85c1ccb953dc97db7abd669841`: entity-handler projectile package proof.
- `3d8d7255d36f26da902e0d43e1c830fa5015594e`: VSGameEvents RenderType package proof.
- `24802fb75610a3ceb1614fda1a78cab1fab7cfe5`: VSGameUtils build-height / packed chunk-key proof.
- `a5e219c7036937ce0ef4b5dfe5032bd82c764ee9`: VSGameUtils ResourceKey / Identifier proof.
- `ee7e9c56be55fd95114d0f7e194be69185db4385`: nullable translation-argument proof.
- `169e0007dcbeb2263701e6b41e40757de6d62ff2`: TestChair entity creation / positioning proof.
- `2c763500338955135d0700b273594a87dab9d982`: VSKeyBindings Category proof.
- `5c8a80eca1b996c4b89d5a394d7cfb9115d3f070`: CreativeModeTab.Output access proof.
- `4641ae31765f0d067923cc1ef54b9a26abe99a19`: TestHingeBlockEntity Value I/O proof.
- `ea2084954eb4edd2bd9922aa1f59342b76709809`: MassDatapackResolver registry-tag proof.
- `27e181c70184b2aac38eeb1a646905d93ba45023`: MassDatapackResolver typed reload-listener proof.
- `ac739bbf0c1598087a6ae9b158117c4764ce3079`: DimensionParametersResolver typed reload-listener proof.
- `2af9d9ba1d48f8a0baf825398d3d441b1219f19d`: VSEntityHandlerDataLoader typed reload-listener proof.
- `9d82234aa769a6a0eece07f52e7d5ace2d334aab`: VSGamePackets Identifier vocabulary proof.
- `4a657f4625f69b26b9ccef9f7235cee271325d98`, `19d15fccf7345fc80f91800356a105d3595db87c`, `a40316e93a61594018fd6f8f9d4b913d7fb2eb80`, `563cbcba7bb1c92ca27820ef785d11bb88872524`, `75a434c728f1ca020b550882967085ccc53d5c3b`: earlier identifier/reload/minY/chunk-key proofs.

Locked negative evidence includes:
- `a72aaef8eca34a352ef949eeb57e6bbcda81171f`: `setUnsaved(false)` is invalid current API; do not replay absent direct new evidence.
- VSKeyBindings failed probes `e108526cbd728454c175c76bffc610d4e074da49`, `fcc65187d79c4b546883875da3597345db1e01cd`, `e9a3efd58acb2af9539628eb2875e6cb829c3cec`, `fb3c7e65a4c2089f6fa695114734d14836bde1d3` remain negative evidence.
- Any retired `apm23/VS2-Create_Interactive` workaround is historical warning evidence only and is forbidden as implementation source.

## Target runtime baseline

- Minecraft `26.2`
- Java `25`
- Fabric Loader `0.19.3`
- Fabric API `0.160.0+26.2`, SHA-256 `5f3dff88e1661166e222213302b25ace6c36dc3683804cbd4b5acf93138ea05e`
- Create Fly `6.0.9-1`, SHA-256 `d9c6cb6116d5caa1174a289ecd7d3cdd463ccef6e8db1249ab0bcfcd8c935870`
- Steam 'n' Rails embedded `SNR.FLY-STABLE-1.2.2+fabric-mc26.2`, SHA-256 `33c87d5a7da0d468d3b6c0e99f726b835c63b693e7447fdaeca5e1f204caab84`
- Copycats embedded `3.0.7-createfly+mc.26.2-v1.14`, SHA-256 `1922db10a49dfab42c4c272fbaee41cdc149287cd08ca84148b497e598029858`
- Exact bytes and metadata rules are locked by `BASELINE_LOCK.json`; filenames are not authoritative when embedded metadata/hash disagree.

## Project state

- project_state: `P1_SOURCE_API_ADAPTATION_IN_PROGRESS`
- active_blocker: `MINECRAFT_26_2_SOURCE_API_DRIFT`
- active_proof_head: `6aa93ba02e830fa432f0b6e00185ea533227e967; renderer handler EntityRenderer<T,S>/EntityRenderState boundary compiler-proven in isolated exact-head probe; full dispatcher lifecycle remains unproven`
- active_proof_run: `P0 35452733152 / job 105922599182 success; renderer probe 35452733162 / job 105922599245 failure only on independent Create/authority/Sable Kotlin clusters, with all three targeted handler diagnostics absent`
- active_hypothesis: `none selected after renderer-handler sub-boundary freeze; current Kotlin blockers must be reduced one semantic cluster at a time before normal common:compileJava can expose exact dispatcher diagnostics`
- final_ready: `false`
- user_runtime_validation: `NOT_APPLICABLE_YET`
- video_status: `NOT_APPLICABLE_YET`

## Proven P1 progress

Build/toolchain and all frozen source/API overlays remain green at their exact boundaries. The renderer-handler probe replayed the complete canonical frozen overlay chain and proved the handler-facing renderer-state adaptation compiler-clean. No Create/SNR/Copycats bridge work has been used to mask standalone real-VS2 failures.

## Remaining compiler areas from exact renderer probe run `35452733162`

The Kotlin compiler residue is now only:

- Create compatibility intermediary/classpath/API drift in `DeployerScrollOptionSlot.kt`: `BiPredicate` intermediary mismatch, `getLocalOffset` override/signature mismatch, inaccessible intermediary Vec3/LevelAccessor/BlockPos/BlockState classes, and current Direction normal accessor drift. This is P1 compile residue only; it is **not** permission to begin P3 or let Create define VS2 architecture.
- Authority-sensitive `VSGamePackets.kt` / `EntityDragger.kt`: removed/changed `isControlledByLocalInstance` and `lerpTo`. Never replace these with teleport chase, synthetic carry velocity, manual clamps, fake inertia, or camera forcing.
- Sable dependency boundary in `SableCompat.kt`: unresolved `ryanhcode` / `SableCompanion`. Sable must be satisfied by a real dependency or an upstream-compatible documented boundary, never by a fake companion/package.

The three renderer-handler Kotlin files are **not** remaining compiler areas after run `35452733162`.

Separately, `MixinEntityRenderDispatcher` remains an unresolved renderer lifecycle continuation because the Java stage has not yet been reached. Its absence from diagnostics is not proof of compatibility.

## Engineering locks

- First-failure classification must stay factual: build/mappings/API/loader/mixin/VSCore-native/networking/storage/transforms/rendering/collision/entity-player-camera/Create bridge/SNR-Copycats/CI/final packaging.
- Make one evidence-backed root change at a time.
- Standalone real VS2 P1 must initialize before any Create bridge work.
- P2/M1 requires real VS2 ship lifecycle, translation+rotation, ship-space, collision, standing/walking, jump-airborne-natural landing, floor/walls/ceiling, free camera, entity dragging/reference-space, rendering, and client/server sync. No floor-only or fake-carry success counts.
- Frozen renderer-handler proof authorizes only the exact `EntityRenderer<T,S>` / `EntityRenderState` contract bridge and current render-offset lookup. It does not authorize a guessed dispatcher lifecycle, custom renderer, custom reference frame, or camera workaround.
- Frozen ticket proof authorizes only its exact load-only radius-zero add/remove lifecycle and `tryMarkSaved()` deletion cleanup. It does not authorize force-loading redesign.
- Frozen ShipSavedData proof authorizes only the `SavedDataType + Codec` API bridge and matching server acquisition change. It does not authorize alternate storage authority, world-file migration guesses, payload redesign, or manual save management.
- Authority-sensitive networking/entity dragging requires direct current API semantics before edits.
- Do not use Create/SNR/Copycats as a P1 crutch.
- Do not record ordinary compile/debug/hypothesis-test video.
- `FINAL_READY` is forbidden from CI alone and requires exact-final-JAR real-user runtime acceptance.

## next_safe_action

1. Preserve renderer-handler implementation `6a13ff6d1f730678d9dd793f575887c08792b161`, exact probe HEAD `6aa93ba02e830fa432f0b6e00185ea533227e967`, ShipSavedData `f2b3ec68e0d2146bb8b443da76a62a4766e01fce`, ticket lifecycle `65a42e782de192f27d5bf720691d6e08f395a719`, and all earlier frozen-green / negative evidence.
2. This ledger-only freeze commit is **not** source proof. Require exact-head P0 provenance success for the resulting ledger HEAD before any further source mutation.
3. After that gate, inspect exact probe run `35452733162` plus direct current API/dependency evidence for **one** of the three remaining Kotlin semantic clusters only. Do not patch multiple independent clusters.
4. Prefer a well-bounded dependency/API cluster that can remove a real Kotlin blocker without touching VS2 gameplay authority. Sable requires evidence for the real upstream dependency/boundary before any edit. Authority-sensitive networking/entity dragging remains locked until exact 26.2 control/lerp semantics are identified. Create compatibility may be repaired only as compile/API compatibility and may not become P3 architecture.
5. Keep `MixinEntityRenderDispatcher` parked until either normal `:common:compileJava` becomes reachable and yields exact diagnostics or an isolated Java proof harness provides equivalent exact compile evidence. Do not guess its new injection lifecycle merely from method names.
6. Remain in standalone P1. Do not use Create/SNR/Copycats to hide standalone VS2 failures. Do not record ordinary compile/debug video.

## Video and final gate

- Video is closure-only, never a debugging tool.
- `M1_COMPLETE` is forbidden until the complete P2 real-VS2 runtime matrix is proven.
- `FINAL_BUILD` / `FINAL_VERIFY` / `FINAL_READY` are not applicable during P1.
- `FINAL_READY` still requires exact-final-JAR real-user runtime acceptance.
