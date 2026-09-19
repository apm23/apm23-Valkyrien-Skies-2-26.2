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

## Current reconciliation — optional Sable Companion compile boundary proven and frozen

- Fail-closed probe overlay implementation: `58bd44154c20f141969b758b8e35372d982ac358` (`P1: add Sable Companion compile-only probe overlay`).
- Exact proof harness HEAD before this ledger-only freeze: `c0c1efb790c31f90c8916121f7c4a06864a58b7f` (`ci: probe Sable Companion compile boundary`).
- Exact-head P0 provenance for `c0c1efb790c31f90c8916121f7c4a06864a58b7f`: run `35454031928`, job `105926053661`, completed `success`; pinned upstream identity remained unchanged.
- Exact Sable probe: run `35454031987`, job `105926053824`, completed `failure` only because two independent Kotlin clusters remain: Create compatibility and authority-sensitive networking/entity dragging.
- Diagnostic artifact: `p1-sable-probe-c0c1efb790c31f90c8916121f7c4a06864a58b7f`, artifact ID `10587876899`, size `4376` bytes, ZIP SHA-256 `b672943267368cd4adb06cc686808a2c2c6c79680dae69febe1447721c494f09`.
- Exact probe run `35454031987` contains **no compiler diagnostic** for `SableCompat.kt`, `dev.ryanhcode`, `SableCompanion`, `projectOutOfSubLevel`, or `isInPlotGrid`.

### Proven Sable root cause and minimal P1 adaptation

Pinned upstream VS2 actually imports `dev.ryanhcode.sable.companion.SableCompanion` in `SableCompat.kt`, and `VSGameUtils.kt` conditionally uses that adapter from `isChunkInShipyard` / `isBlockInShipyard` behind `LoadedMods.sable`. `LoadedMods.sable` itself detects the same `dev.ryanhcode.sable.companion.SableCompanion` class.

The existing P1 build baseline had removed the old upstream coordinate `dev.ryanhcode.sable:sable-common-${minecraft_version}:${sable_version}` while incorrectly documenting that the Sable API was not imported by VS2 source. That removal left real pinned `SableCompat.kt` uncompilable.

Current official Sable Companion evidence shows:
- the compatibility API is maintained as the separate `ryanhcode/sable-companion` project;
- current source version is `1.6.0`;
- its documented/current source line still targets Minecraft `1.21.1`;
- it exposes the exact API shapes used by pinned VS2 (`projectOutOfSubLevel` and `isInPlotGrid`);
- it is designed as an optional lightweight compatibility API with a safe default implementation.

Because no Minecraft-26.2 Sable Companion runtime release/branch was found, the proven P1 bridge is deliberately **compile-only**:
`dev.ryanhcode.sable-companion:sable-companion-common-1.21.1:1.6.0`.

The probe proves only that this published API artifact resolves and supplies the upstream VS2 source symbols during the 26.2 compile. It is **not** bundled, is not `implementation` or `api`, and makes no claim that a 1.21.1 Sable/Companion runtime is compatible with Minecraft 26.2. When the companion class is absent from the target runtime, upstream `LoadedMods.sable` remains false and the optional Sable path stays short-circuited.

No `SableCompat.kt`, `VSGameUtils.kt`, `LoadedMods.kt`, shipyard transform, physics, collision, rendering, networking, entity dragging, player/camera, or gameplay-authority code was changed. No fake `SableCompanion` package/class was invented.

### Sable proof boundary

- Compile/API boundary only; no runtime Sable compatibility closure is claimed.
- Do not promote the 1.21.1 Companion artifact to runtime/JiJ for the 26.2 final stack without a separate exact 26.2 runtime dependency proof.
- Do not replace Sable Companion with a home-grown stub merely to satisfy source compilation.
- The final required runtime stack does not currently include Sable, so this optional compatibility surface must not block standalone VS2 P1 when the class is absent.
- No video was recorded because this is compile/dependency proof, not closure-ready runtime evidence.

## Immediately preceding frozen proof — renderer handler render-state boundary

- Source overlay implementation: `6a13ff6d1f730678d9dd793f575887c08792b161` (`P1: adapt entity handlers to renderer state API`).
- Exact proof harness HEAD: `6aa93ba02e830fa432f0b6e00185ea533227e967`.
- Exact P0: run `35452733152`, job `105922599182`, success.
- Exact renderer-state probe: run `35452733162`, job `105922599245`; failure only because independent Kotlin P1 clusters remained.
- Artifact `p1-renderstate-probe-6aa93ba02e830fa432f0b6e00185ea533227e967`, ID `10587053238`, size `4438`, SHA-256 `ae32e69c0556e903e813e317b6cca848acc0a4554ca0014ef1231fe51b7accd2`.
- Proven handler bridge: `EntityRenderer<T>` -> `EntityRenderer<T,S>`, `EntityRenderState` passed through the existing real VS2 handler contract, and `getRenderOffset(entity, partialTicks)` -> `getRenderOffset(renderState)`.
- Upstream real VS2 ship render transform math, position transform, rotation, scaling, camera-relative translation, mounted-entity transform, movement/projectile/entity-dragging behavior and gameplay authority remain unchanged.

### Renderer proof boundary — dispatcher lifecycle is NOT yet claimed

Pinned upstream `MixinEntityRenderDispatcher` still targets the pre-26.2 dispatcher lifecycle. Exact Minecraft 26.2 API inspection shows `extractEntity(entity, partialTicks)` -> `EntityRenderState` and separate `submit(renderState, camera, x, y, z, PoseStack, SubmitNodeCollector)`. The old `distanceToSqr(DDD)` overload used by one upstream injection is absent from inspected current source.

Normal `:common:compileJava` is still unreachable because Kotlin blockers stop first, so **no compile-clean claim exists for `MixinEntityRenderDispatcher`**. Do not guess its injection lifecycle from method names. Resume only from exact Java diagnostics once Kotlin is unblocked, or from an equivalent isolated Java compile proof.

## Earlier frozen proof — real VS2 ShipSavedData persistence boundary

- Proven implementation HEAD: `f2b3ec68e0d2146bb8b443da76a62a4766e01fce`.
- Exact P0: run `35451366274`, job `105918982071`, success.
- Exact P1: run `35451366140`, job `105918981784`; failure only from independent clusters.
- Artifact `p1-compile-log-f2b3ec68e0d2146bb8b443da76a62a4766e01fce`, ID `10586956459`, SHA-256 `7921227c49729f5b23f8d54d19204ee5b1965c38506b59ad6da9ba3e8b4b234f`.
- Frozen semantics: overworld `SavedDataStorage` remains the single authority; current `SavedDataType<ShipSavedData>` + `CompoundTag.CODEC.xmap(::load, ShipSavedData::saveToTag)` replaces only the obsolete Factory/save boundary; existing VS pipeline payload keys and fallback semantics remain unchanged.
- Legacy 1.21.1 root-path `vs_ship_data.dat` automatic file-location migration is **not** proven and must not be guessed.

## Frozen proof ancestry / negative evidence

All frozen-green and negative-evidence records already present in Git history remain binding. Ledger compaction does not unfreeze or supersede them. Do not replay failed probes or edit a frozen site merely because a later compiler error looks similar.

Explicit recent frozen implementation proofs include:
- `58bd44154c20f141969b758b8e35372d982ac358` + probe HEAD `c0c1efb790c31f90c8916121f7c4a06864a58b7f`: Sable Companion compile-only API boundary; P0 `35454031928` / job `105926053661`; probe `35454031987` / job `105926053824`; artifact `10587876899`; SHA-256 `b672943267368cd4adb06cc686808a2c2c6c79680dae69febe1447721c494f09`. Runtime Sable compatibility explicitly excluded from this proof.
- `6a13ff6d1f730678d9dd793f575887c08792b161` + probe HEAD `6aa93ba02e830fa432f0b6e00185ea533227e967`: renderer-handler `EntityRenderer<T,S>` / `EntityRenderState` contract; P0 `35452733152` / job `105922599182`; probe `35452733162` / job `105922599245`; artifact `10587053238`; SHA-256 `ae32e69c0556e903e813e317b6cca848acc0a4554ca0014ef1231fe51b7accd2`. Dispatcher lifecycle explicitly excluded from this proof.
- `f2b3ec68e0d2146bb8b443da76a62a4766e01fce`: ShipSavedData persistence boundary; P0 `35451366274` / job `105918982071`; P1 `35451366140` / job `105918981784`; artifact `10586956459`.
- `65a42e782de192f27d5bf720691d6e08f395a719`: real VS2 ship chunk-ticket lifecycle; P0 `35450402081` / job `105916444806`; P1 `35450402031` / job `105916444686`; artifact `10585479315`.
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
- `ea2084954eb4edd2bd9922aa1f59342b76709809`: MassDatapackResolver registry tag.
- `27e181c70184b2aac38eeb1a646905d93ba45023`: MassDatapackResolver typed reload listener.
- `ac739bbf0c1598087a6ae9b158117c4764ce3079`: DimensionParametersResolver typed reload listener.
- `2af9d9ba1d48f8a0baf825398d3d441b1219f19d`: VSEntityHandlerDataLoader typed reload listener.
- `9d82234aa769a6a0eece07f52e7d5ace2d334aab`: VSGamePackets Identifier vocabulary.
- `4a657f4625f69b26b9ccef9f7235cee271325d98`, `19d15fccf7345fc80f91800356a105d3595db87c`, `a40316e93a61594018fd6f8f9d4b913d7fb2eb80`, `563cbcba7bb1c92ca27820ef785d11bb88872524`, `75a434c728f1ca020b550882967085ccc53d5c3b`: earlier identifier/reload/minY/chunk-key proofs.

Locked negative evidence includes:
- `a72aaef8eca34a352ef949eeb57e6bbcda81171f`: `setUnsaved(false)` is invalid current API; do not replay absent direct new evidence.
- VSKeyBindings failed probes `e108526cbd728454c175c76bffc610d4e074da49`, `fcc65187d79c4b546883875da3597345db1e01cd`, `e9a3efd58acb2af9539628eb2875e6cb829c3cec`, `fb3c7e65a4c2089f6fa695114734d14836bde1d3` remain negative evidence.
- Do not interpret the Sable compile-only proof as permission to bundle/run the 1.21.1 Companion artifact on 26.2; that runtime hypothesis has not been tested.
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
- active_proof_head: `c0c1efb790c31f90c8916121f7c4a06864a58b7f; optional Sable Companion compile-only API boundary proven; runtime Sable compatibility explicitly unclaimed`
- active_proof_run: `P0 35454031928 / job 105926053661 success; Sable probe 35454031987 / job 105926053824 failure only on independent Create-compat and authority-sensitive Kotlin clusters; Sable diagnostics absent`
- active_hypothesis: `none selected after Sable compile-boundary freeze; after this ledger-only HEAD passes exact-head P0, choose exactly one of the two remaining Kotlin semantic clusters`
- final_ready: `false`
- user_runtime_validation: `NOT_APPLICABLE_YET`
- video_status: `NOT_APPLICABLE_YET`

## Proven P1 progress

Build/toolchain and all frozen source/API overlays remain green at their exact boundaries. Supplemental isolated probes now prove both the renderer-handler state boundary and the optional Sable compile API boundary without changing real VS2 gameplay authority or importing Create/SNR/Copycats architecture into P1.

## Remaining compiler areas from exact Sable probe run `35454031987`

The Kotlin compiler residue is now only:

1. **Create compatibility intermediary/classpath/API drift** in `common/src/main/java/org/valkyrienskies/mod/compat/create/DeployerScrollOptionSlot.kt`:
   - `BiPredicate<BlockState, Direction>` vs intermediary Create-side classes;
   - `getLocalOffset` override/signature mismatch;
   - inaccessible intermediary Vec3/LevelAccessor/BlockPos/BlockState types;
   - current Direction normal accessor drift.
   This is optional Create compatibility residue during standalone P1; it is **not** permission to begin P3 or make Create authoritative for VS2.

2. **Authority-sensitive networking/entity dragging**:
   - `VSGamePackets.kt`: removed/changed `Entity.isControlledByLocalInstance` and `lerpTo`;
   - `EntityDragger.kt`: removed/changed `isControlledByLocalInstance`.
   Never replace these with per-tick teleport/setPos chase, synthetic carry velocity/inertia, manual floor/wall/ceiling clamps, fake gravity, or camera forcing.

`SableCompat.kt` and all three renderer-handler Kotlin files are no longer remaining compiler areas in the exact latest probe.

Separately, `MixinEntityRenderDispatcher` remains an unresolved Java renderer lifecycle continuation because normal `:common:compileJava` has still not been reached. Its absence from diagnostics is not proof of compatibility.

## Engineering locks

- First-failure classification must stay factual: build/mappings/API/loader/mixin/VSCore-native/networking/storage/transforms/rendering/collision/entity-player-camera/Create bridge/SNR-Copycats/CI/final packaging.
- Make one evidence-backed root change at a time.
- Standalone real VS2 P1 must initialize before any Create bridge work.
- P2/M1 requires real VS2 ship lifecycle, translation+rotation, ship-space, collision, standing/walking, jump-airborne-natural landing, floor/walls/ceiling, free camera, entity dragging/reference-space, rendering, and client/server sync. No floor-only or fake-carry success counts.
- Frozen Sable proof authorizes only compile-time use of the official Companion API artifact for the optional upstream compatibility source. It does not authorize runtime bundling of a 1.21.1 artifact on 26.2 or a fake local replacement.
- Frozen renderer-handler proof authorizes only the exact `EntityRenderer<T,S>` / `EntityRenderState` contract bridge and current render-offset lookup. It does not authorize a guessed dispatcher lifecycle, custom renderer, custom reference frame, or camera workaround.
- Frozen ticket proof authorizes only its exact load-only radius-zero add/remove lifecycle and `tryMarkSaved()` deletion cleanup. It does not authorize force-loading redesign.
- Frozen ShipSavedData proof authorizes only the `SavedDataType + Codec` API bridge and matching server acquisition change. It does not authorize alternate storage authority, world-file migration guesses, payload redesign, or manual save management.
- Authority-sensitive networking/entity dragging requires direct current API semantics before edits.
- Do not use Create/SNR/Copycats as a P1 crutch.
- Do not record ordinary compile/debug/hypothesis-test video.
- `FINAL_READY` is forbidden from CI alone and requires exact-final-JAR real-user runtime acceptance.

## next_safe_action

1. Preserve Sable probe implementation `58bd44154c20f141969b758b8e35372d982ac358`, exact proof HEAD `c0c1efb790c31f90c8916121f7c4a06864a58b7f`, renderer handler `6a13ff6d1f730678d9dd793f575887c08792b161`, ShipSavedData `f2b3ec68e0d2146bb8b443da76a62a4766e01fce`, ticket lifecycle `65a42e782de192f27d5bf720691d6e08f395a719`, and all earlier frozen-green / negative evidence.
2. This ledger-only freeze commit is **not** source proof. Require exact-head P0 provenance success for the resulting ledger HEAD before any further source mutation.
3. After that gate, select **one** of the two remaining Kotlin semantic clusters only. Do not patch Create compatibility and authority-sensitive entity/networking in the same hypothesis.
4. For the Create residue, first prove whether `DeployerScrollOptionSlot.kt` is an optional upstream Create-compat source that should simply be excluded from standalone P1 together with every matching runtime/mixin registration, rather than porting Create internals before P3. Exclusion is allowed only if the standalone real-VS2 path has no dependency on it. Do not begin Create bridge architecture.
5. If selecting authority-sensitive networking/entity dragging instead, inspect exact Minecraft 26.2 entity control/interpolation semantics before any edit. No guessed `setPos`, teleport, synthetic velocity, manual carry, or camera workaround is allowed.
6. Keep `MixinEntityRenderDispatcher` parked until normal `:common:compileJava` becomes reachable and yields exact diagnostics or an isolated Java proof harness supplies equivalent exact evidence.
7. Remain in standalone P1. Do not use Create/SNR/Copycats to hide real VS2 failures. Do not record ordinary compile/debug video.

## Video and final gate

- Video is closure-only, never a debugging tool.
- `M1_COMPLETE` is forbidden until the complete P2 real-VS2 runtime matrix is proven.
- `FINAL_BUILD` / `FINAL_VERIFY` / `FINAL_READY` are not applicable during P1.
- `FINAL_READY` still requires exact-final-JAR real-user runtime acceptance.
