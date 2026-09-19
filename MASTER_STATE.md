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

## Current reconciliation — optional Create deployer helper isolated from standalone P1

### Exact classification

Pinned upstream file:
`common/src/main/java/org/valkyrienskies/mod/compat/create/DeployerScrollOptionSlot.kt`

The exact pinned source tree proves this is a narrowly isolated optional Create compatibility helper for `DirectionalExtenderScrollOptionSlot`:
- exact common Kotlin source contains no caller/reference to `DeployerScrollOptionSlot` outside the helper itself;
- exact common Java source contains no caller/reference to that symbol outside the helper itself;
- exact `valkyrienskies-common.mixins.json` contains no direct `mod_compat.create.*` registration and no `DeployerScrollOptionSlot` registration;
- the helper is physically located under `common/src/main/java` even though its language is Kotlin;
- standalone real-VS2 P1 has no proven dependency on this helper, while full Create integration is contractually deferred to P3 after standalone P2 is frozen green.

Therefore the safe P1 action is to omit only this unreferenced helper from standalone compilation, not to port Create internals or begin the Create bridge early. The upstream source file remains present in the pinned submodule and must be revisited legitimately in P3.

### Failed first exclusion hypothesis — locked negative evidence

- Initial overlay commit: `3e5bb792230abba0eeff4e7a0277ba3529341ade`.
- First probe HEAD: `3bcbf90c75dc4d02448cfdb4590cc9c9674e0ed6`.
- Exact-head P0: run `35454717378`, job `105927859141`, success.
- Probe run: `35454717409`, job `105927859438`, completed `failure`.
- Artifact: `p1-deployer-exclusion-probe-3bcbf90c75dc4d02448cfdb4590cc9c9674e0ed6`, ID `10588041201`, size `4402` bytes, ZIP SHA-256 `86f2e0472c36dee58c7c3434b8e0dbd0f18fa5cdcddc9c99c080aabf6b2c8ece`.
- Failed hypothesis: adding the exact helper exclusion under `sourceSets.main.kotlin` would filter the `.kt` file.
- Exact result: all `DeployerScrollOptionSlot.kt` diagnostics remained unchanged because the file is physically owned by the `src/main/java` source root.

**Lock:** do not replay the `kotlin { exclude "org/valkyrienskies/mod/compat/create/DeployerScrollOptionSlot.kt" }` hypothesis absent direct new source-layout evidence.

### Proven corrected P1 exclusion

- Corrected implementation HEAD: `cd2434e69caf28e12560bf4444fc220a3023e40b` (`P1: exclude deployer helper from actual source root`).
- Exact-head P0: run `35454908696`, job `105928361982`, completed `success`; exact upstream identity remained pinned.
- Corrected probe: run `35454908850`, job `105928362519`, completed `failure` only because the independent authority-sensitive Kotlin cluster remains.
- Artifact: `p1-deployer-exclusion-probe-cd2434e69caf28e12560bf4444fc220a3023e40b`, artifact ID `10588156201`, size `3978` bytes, ZIP SHA-256 `6d1516425d4c28755bffea02de77d8a5622f576fbf449b2573bfcc7aabfa45e6`.
- Proven adaptation: exactly one source-set line is added under `sourceSets.main.java`:
  `exclude "org/valkyrienskies/mod/compat/create/DeployerScrollOptionSlot.kt"`.
- The fail-closed overlay verifies the helper still matches the pinned role, scans common Java/Kotlin for any caller before exclusion, rejects any matching direct runtime/mixin registration, and refuses broad `compat/create/**` exclusion.
- Exact run `35454908850` contains **zero compiler diagnostic** for `DeployerScrollOptionSlot.kt`, its Create intermediary `class_*` signatures, `DirectionalExtenderScrollOptionSlot`, or the former Direction-normal error.
- Exact remaining Kotlin diagnostics are only:
  - `VSGamePackets.kt:78`: `isControlledByLocalInstance` unresolved;
  - `VSGamePackets.kt:132`: `lerpTo` unresolved;
  - `VSGamePackets.kt:142`: `isControlledByLocalInstance` unresolved;
  - `EntityDragger.kt:148`: `isControlledByLocalInstance` unresolved.

### Proof boundary

This proof authorizes only the exact one-file standalone-P1 compile exclusion. It does **not** claim Create runtime compatibility, does not begin P3, does not remove or rewrite upstream Create compatibility source, and does not alter ship-space, physics, collision, networking, rendering, entity dragging, player/camera, or gameplay authority. No Create/SNR/Copycats dependency is allowed to mask standalone VS2 failures.

No video was recorded because this is compile/source-classification proof, not closure-ready runtime evidence.

## Immediately preceding frozen proof — optional Sable Companion compile boundary

- Probe overlay: `58bd44154c20f141969b758b8e35372d982ac358`.
- Exact proof HEAD: `c0c1efb790c31f90c8916121f7c4a06864a58b7f`.
- P0: run `35454031928`, job `105926053661`, success.
- Sable probe: run `35454031987`, job `105926053824`; failure only on then-independent Create and authority clusters.
- Artifact `p1-sable-probe-c0c1efb790c31f90c8916121f7c4a06864a58b7f`, ID `10587876899`, size `4376`, SHA-256 `b672943267368cd4adb06cc686808a2c2c6c79680dae69febe1447721c494f09`.
- `SableCompat.kt`, `dev.ryanhcode`, `SableCompanion`, `projectOutOfSubLevel`, and `isInPlotGrid` are absent from probe diagnostics.
- Proven compile boundary uses only `compileOnly("dev.ryanhcode.sable-companion:sable-companion-common-1.21.1:1.6.0")`.
- This is compile/API proof only. It is not permission to bundle or run a Minecraft-1.21.1 Sable/Companion runtime on 26.2, and no fake local companion/stub is allowed.

## Earlier frozen proof — renderer handler render-state boundary

- Source overlay: `6a13ff6d1f730678d9dd793f575887c08792b161`.
- Exact proof HEAD: `6aa93ba02e830fa432f0b6e00185ea533227e967`.
- P0: `35452733152` / job `105922599182`, success.
- Renderer-state probe: `35452733162` / job `105922599245`; artifact `10587053238`, SHA-256 `ae32e69c0556e903e813e317b6cca848acc0a4554ca0014ef1231fe51b7accd2`.
- Proven bridge: upstream real VS2 handler contract now uses `EntityRenderer<T,S>`, `S : EntityRenderState`, and `getRenderOffset(renderState)` while preserving upstream VS2 render-transform math and authority.
- `MixinEntityRenderDispatcher` is explicitly **not** proven. The normal Java compile stage has not yet been reached because Kotlin blockers still stop first. Resume dispatcher work only from exact Java diagnostics or an equivalent isolated exact Java proof.

## Earlier frozen proof — ShipSavedData persistence boundary

- Proven implementation: `f2b3ec68e0d2146bb8b443da76a62a4766e01fce`.
- P0 `35451366274` / job `105918982071`, success.
- P1 `35451366140` / job `105918981784`; artifact `10586956459`, SHA-256 `7921227c49729f5b23f8d54d19204ee5b1965c38506b59ad6da9ba3e8b4b234f`.
- Frozen semantics: overworld `SavedDataStorage` remains the single persistence authority; current `SavedDataType<ShipSavedData>` + `CompoundTag.CODEC.xmap(::load, ShipSavedData::saveToTag)` replaces only obsolete SavedData API boundaries.
- Legacy 1.21.1 root-path `vs_ship_data.dat` automatic file-location migration is not proven and must not be guessed.

## Earlier frozen proof — real VS2 ship chunk-ticket lifecycle

- Proven implementation: `65a42e782de192f27d5bf720691d6e08f395a719`.
- P0 `35450402081` / job `105916444806`, success.
- P1 `35450402031` / job `105916444686`; artifact `10585479315`, SHA-256 `4443fd49b99f2fed5b44ee21529b543c503b4ff8494d6ca45b06572aaf9ceede`.
- Frozen semantics: load-only `TicketType(0L, TicketType.FLAG_LOADING)`, radius-zero explicit add/remove lifecycle, distance-manager flush/order preserved, ship-alive removal guard preserved, and existing deletion clean-marker adapted to `tryMarkSaved()`.

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
- `4a657f4625f69b26b9ccef9f7235cee271325d98`, `19d15fccf7345fc80f91800356a105d3595db87c`, `a40316e93a61594018fd6f8f9d4b913d7fb2eb80`, `563cbcba7bb1c92ca27820ef785d11bb88872524`, `75a434c728f1ca020b550882967085ccc53d5c3b`: earlier identifier/reload/minY/chunk-key proofs.

Locked negative evidence includes:
- `3bcbf90c75dc4d02448cfdb4590cc9c9674e0ed6` / run `35454717409`: putting the exact `DeployerScrollOptionSlot.kt` exclusion in the Kotlin source-set block does not filter the file under `src/main/java`; do not replay.
- `a72aaef8eca34a352ef949eeb57e6bbcda81171f`: `setUnsaved(false)` is invalid current API; do not replay absent direct new evidence.
- VSKeyBindings failed probes `e108526cbd728454c175c76bffc610d4e074da49`, `fcc65187d79c4b546883875da3597345db1e01cd`, `e9a3efd58acb2af9539628eb2875e6cb829c3cec`, `fb3c7e65a4c2089f6fa695114734d14836bde1d3` remain negative evidence.
- Do not interpret the Sable compile-only proof as permission to bundle/run its 1.21.1 runtime artifact on 26.2.
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
- active_proof_head: `cd2434e69caf28e12560bf4444fc220a3023e40b; exact one-file DeployerScrollOptionSlot standalone-P1 exclusion compiler-proven; Create integration remains deferred to P3`
- active_proof_run: `P0 35454908696 / job 105928361982 success; corrected exclusion probe 35454908850 / job 105928362519 failure only on authority-sensitive VSGamePackets/EntityDragger Kotlin residue; Deployer/Create diagnostics absent`
- active_hypothesis: `none selected; after this ledger-only HEAD passes exact-head P0, inspect VSGamePackets + EntityDragger together as one authority semantic unit against exact Minecraft 26.2 ownership/control/interpolation semantics`
- final_ready: `false`
- user_runtime_validation: `NOT_APPLICABLE_YET`
- video_status: `NOT_APPLICABLE_YET`

## Remaining compiler area from exact corrected probe `35454908850`

The Kotlin compiler residue is now one authority-sensitive semantic cluster only:
- `VSGamePackets.kt`: removed/changed `Entity.isControlledByLocalInstance` at two sites and removed/changed `lerpTo` at one site;
- `EntityDragger.kt`: removed/changed `isControlledByLocalInstance` at one site.

This cluster controls client/server entity ownership and interpolation and is therefore authority-sensitive. Never replace the missing APIs with guessed local-player ownership, `setPos`, per-tick teleport/chase, synthetic carry velocity/inertia, fake gravity, manual floor/wall/ceiling clamps, or camera forcing.

Separately, `MixinEntityRenderDispatcher` remains an unresolved Java renderer-lifecycle continuation because normal `:common:compileJava` has still not been reached. Its absence from diagnostics is not proof of compatibility.

## Engineering locks

- First-failure classification must stay factual: upstream/provenance, build, mappings/API, loader, mixin, VSCore/native, networking/serialization, storage, transforms, rendering, collision, entity/player/camera, Create bridge, SNR/Copycats, CI/harness, or final packaging.
- Make one evidence-backed root change at a time.
- Standalone real VS2 P1 must initialize before any Create bridge work.
- P2/M1 requires real VS2 ship lifecycle, translation+rotation, ship-space, collision, standing/walking, jump-airborne-natural landing, floor/walls/ceiling, free camera, entity dragging/reference-space, rendering, and client/server sync. No floor-only or fake-carry success counts.
- Frozen optional Create proof authorizes only the exact one-file standalone-P1 compile exclusion. It does not authorize broad Create exclusion, Create runtime adaptation, or P3 architecture.
- Frozen Sable proof authorizes only compile-time use of the official Companion API artifact. It does not authorize runtime bundling of a 1.21.1 artifact on 26.2 or a fake local replacement.
- Frozen renderer-handler proof authorizes only the exact `EntityRenderer<T,S>` / `EntityRenderState` contract bridge and render-offset lookup. It does not authorize a guessed dispatcher lifecycle, custom renderer/reference frame, or camera workaround.
- Frozen ticket proof authorizes only the exact load-only radius-zero add/remove lifecycle and `tryMarkSaved()` cleanup. It does not authorize force-loading redesign.
- Frozen ShipSavedData proof authorizes only the `SavedDataType + Codec` API bridge and matching server acquisition change. It does not authorize alternate storage authority, world-file migration guesses, payload redesign, or manual save management.
- Authority-sensitive networking/entity dragging requires direct current API semantics before edits.
- Do not use Create/SNR/Copycats as a P1 crutch.
- Do not record ordinary compile/debug/hypothesis-test video.
- `FINAL_READY` is forbidden from CI alone and requires exact-final-JAR real-user runtime acceptance.

## next_safe_action

1. Preserve corrected optional-Create implementation `cd2434e69caf28e12560bf4444fc220a3023e40b`, its exact proof run/artifact, and the failed Kotlin-sourceSet hypothesis as locked negative evidence. Preserve all earlier frozen-green/negative evidence.
2. This ledger-only freeze commit is **not** source proof. Require exact-head P0 provenance success for the resulting ledger HEAD before any further source mutation.
3. After that gate, inspect pinned upstream `VSGamePackets.kt` and `EntityDragger.kt` together as **one authority semantic unit**, plus the exact Minecraft 26.2 entity ownership/client-control/interpolation APIs that replace the old `isControlledByLocalInstance` and `lerpTo` semantics.
4. Before editing, map each old call to its upstream role: who owns movement authority, when a locally controlled entity should be excluded/included, and whether packet correction is interpolation or direct authoritative relocation. Do not infer semantics from method names alone.
5. Any adaptation must connect changed 26.2 APIs into the existing upstream VS2 networking/entity-dragging architecture. Do **not** introduce `setPos`/teleport chase, guessed local-player checks, synthetic carry velocity/inertia, fake gravity, manual collision clamps, camera forcing, or duplicate authority.
6. If this authority cluster becomes Kotlin-clean, use the newly reachable compiler stage to expose exact common-Java diagnostics. Only then resume `MixinEntityRenderDispatcher` from direct Java evidence unless another earlier standalone-P1 blocker appears first.
7. Remain in standalone P1. Do not begin Create bridge/P3, do not use SNR/Copycats to hide failures, and do not record ordinary compile/debug video.

## Video and final gate

- Video is closure-only, never a debugging tool.
- `M1_COMPLETE` is forbidden until the complete P2 real-VS2 runtime matrix is proven.
- `FINAL_BUILD` / `FINAL_VERIFY` / `FINAL_READY` are not applicable during P1.
- `FINAL_READY` still requires exact-final-JAR real-user runtime acceptance.
