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

## Current reconciliation — real VS2 ShipSavedData persistence boundary proven and frozen

- Current proven implementation HEAD: `f2b3ec68e0d2146bb8b443da76a62a4766e01fce` (`P1: wire ShipSavedData persistence proof`).
- Implementation ancestry for this proof: fail-closed source overlay `7b51117fc1f0286ba7a7aea1017deed09d410d09` plus canonical P1 workflow wiring `f2b3ec68e0d2146bb8b443da76a62a4766e01fce`.
- Immediately preceding ledger-only HEAD `beed6cae81b526910aedcbd3c960957258937ba2` had exact-head P0 provenance success in run `35450793995`, job `105917469329`, before this source mutation.
- Exact-head P0 provenance for implementation HEAD `f2b3ec68e0d2146bb8b443da76a62a4766e01fce`: run `35451366274`, job `105918982071`, completed `success`; exact upstream identity remained pinned to `f39132148e717d325933b4ce6e9e9fb13d929390`.
- Exact-head P1 standalone compile: run `35451366140`, job `105918981784`, completed `failure` only because independent P1 compiler clusters remain. The new ShipSavedData persistence overlay, port-delta validation, Gradle runtime setup, and compile-log upload completed successfully.
- Diagnostic artifact: `p1-compile-log-f2b3ec68e0d2146bb8b443da76a62a4766e01fce`, artifact ID `10586956459`, size `4588` bytes, ZIP SHA-256 `7921227c49729f5b23f8d54d19204ee5b1965c38506b59ad6da9ba3e8b4b234f`.
- Exact P1 run `35451366140` contains **no compiler diagnostic** for `ShipSavedData`, `MixinMinecraftServer`, `SavedDataType`, `SavedData.Factory`, its `computeIfAbsent` registration, or the former `save overrides nothing` failure.

### Proven root cause and minimal 26.2 adaptation

Pinned upstream VS2 uses one persistence authority: overworld `SavedData` storage. `ShipSavedData` owns the VS pipeline payload and `MixinMinecraftServer` acquires it during server level creation through the old `SavedData.Factory + computeIfAbsent(factory, string-id)` API. The old `ShipSavedData.save(CompoundTag, HolderLookup.Provider)` override writes the pipeline bytes.

Exact Minecraft 26.2 source/API inspection proves this boundary changed as one semantic unit:
- `SavedDataStorage.computeIfAbsent` now accepts one `SavedDataType<T>`;
- `SavedDataType<T>` owns an `Identifier`, constructor, `Codec<T>`, and data-fix type;
- `SavedDataStorage` decodes/encodes through that codec and wraps the payload under its own root `data` tag;
- `CompoundTag.CODEC` exists and can carry the existing VS2 NBT payload without a second serializer or persistence authority;
- `Identifier.resolveAgainst(dataFolder)` makes the namespace part of the current on-disk path.

The proven overlay therefore:
- preserves **overworld `getDataStorage()` as the only ShipSavedData authority**; it does not move VS2 persistence to server-global storage or create a second store;
- replaces the old Factory registration with exactly one `ShipSavedData.TYPE: SavedDataType<ShipSavedData>` and `computeIfAbsent(ShipSavedData.TYPE)`;
- uses `CompoundTag.CODEC.xmap(::load, ShipSavedData::saveToTag)` so decode still delegates to the real upstream VS2 `load` implementation and encode writes the same pipeline-byte payload;
- preserves `DataFixTypes.LEVEL`, matching the upstream Factory;
- preserves the existing payload keys exactly: `queryable_ship_data`, `chunk_allocator`, `vs_pipeline`;
- preserves the already-frozen Minecraft-26.2 Optional adaptation for all three `getByteArray` calls;
- preserves pipeline-first loading, the legacy queryable/chunk-allocator fallback, `loadingException`, the fatal server-init rethrow, and the same handoff into `vsPipeline` / real VS2 ship world;
- preserves always-dirty behavior because real VS2 physics transforms change continuously;
- removes only the obsolete `SavedData.save(...)` override and old Factory boundary.

Current type identity is `Identifier.fromNamespaceAndPath(ValkyrienSkiesMod.MOD_ID, SAVED_DATA_ID)` with `MOD_ID=valkyrienskies` and `SAVED_DATA_ID=vs_ship_data`. Exact 26.2 storage semantics therefore place current-format data under the identifier namespace/path rather than the old pre-26.x root `data/vs_ship_data.dat` location.

**Important proof boundary:** this compile/API proof does **not** claim or implement automatic migration of an existing 1.21.1 root-path `vs_ship_data.dat` file into the current identifier-resolved path. No speculative manual file-copy/move path was introduced because that would require its own exact world-path/runtime evidence. Fresh/current 26.2 persistence registration is proven compiler-clean; legacy-world file-location migration remains a later compatibility/runtime concern if required by a world-upgrade gate. Payload compatibility itself remains preserved inside `ShipSavedData.load`.

This proof does not alter ship creation/allocation, transforms, physics, collision, entity dragging, rendering, networking/gameplay authority, camera behavior, chunk ticketing, Create integration, SNR, or Copycats. No code from retired `apm23/VS2-Create_Interactive` was imported or reused. No video was recorded because this was an isolated compile/API persistence proof, not a closure-ready user-visible runtime blocker.

## Frozen proof ancestry / negative evidence

All frozen-green and negative-evidence records that existed in Git history through ledger HEAD `beed6cae81b526910aedcbd3c960957258937ba2` remain binding. Ledger compaction does not unfreeze or supersede them. Do not replay failed probes or edit a frozen site merely because a later compiler error looks similar.

Explicit recent frozen implementation proofs include:
- `f2b3ec68e0d2146bb8b443da76a62a4766e01fce`: ShipSavedData `SavedDataType + Codec + MixinMinecraftServer` persistence boundary; P0 `35451366274` / job `105918982071`; P1 `35451366140` / job `105918981784`; artifact `10586956459`; SHA-256 `7921227c49729f5b23f8d54d19204ee5b1965c38506b59ad6da9ba3e8b4b234f`.
- `65a42e782de192f27d5bf720691d6e08f395a719`: real VS2 ship chunk-ticket lifecycle bridge; P0 `35450402081` / job `105916444806`; P1 `35450402031` / job `105916444686`; artifact `10585479315`; SHA-256 `4443fd49b99f2fed5b44ee21529b543c503b4ff8494d6ca45b06572aaf9ceede`.
- `30b9f70d3c6c71dfd30ca76339e19cfcb56461e4`: ShipAssembler block-entity ValueInput bridge.
- `45de97f06a3ab25c1e19b0dc09790ebde2d8e851`: ShipAssembler Clearable bridge.
- `e923ba7658197ff04af605e85507618c09dd390b`: RelocationUtil block-entity ValueInput bridge.
- `52a05bdae75fd2a469287234c680bf191fd5b105`: RelocationUtil pending loot-table clear proof.
- `7a7e2f320605b27bb65e9f0bb6cb88d8aa41a4e7`: RelocationUtil neighbor-update boundary proof.
- `ce6ff8bb8f06eeb8e98544f6bf9ca1e503936fdb`: RelocationUtil direct `LevelChunk.setBlockState` zero-flag proof.
- `2da9ca25e3ce6fd2f601cc2f6b626b0e3998a677`: ShipAssembler StructureProcessor adapter proof.
- `aa26d707fac479c63a6a5e097ca65818dd145262`: ShipAssembler fast-path direct chunk-write zero-flag proof.
- `12f182325f9f3e10c502afae7da567e4b1b95c28`: AssemblyUtil neighbor-dispatch proof.
- `644d108b111bed17d0f3259dc840803f7c9a3192`: AssemblyUtil block-entity Value I/O proof.
- `820ef37e8ca012fe484d9960242cbfc0eefbacc8`: AssemblyUtil ScheduledTick non-null generic proof.
- `a803150d066fdc7e0a0bfdd5bd1661b85c627417`: AssemblyUtil direct chunk-write zero-flag proof.
- `02e356638690d0413a105d409aaae4bcfd6e160c`: ShipAssembler BlockPos -> containing ChunkPos proof.
- `39e2abc40af3d785d4d6ca5f14ac7b28ef03334f`: ShipMountingEntity `kill(ServerLevel)` proof.
- `36549552477a1dd9b24cc12c6e21c6849b2e8b54`: ShipMountingEntity `hurtServer` proof.
- `0a23528d781baf280bb553a8f9fa94c21f447af2`: ShipMountingEntity Value I/O proof.
- `d258e69e46ce2f85c1ccb953dc97db7abd669841`: entity-handler projectile package proof.
- `3d8d7255d36f26da902e0d43e1c830fa5015594e`: VSGameEvents RenderType package proof.
- `24802fb75610a3ceb1614fda1a78cab1fab7cfe5`: VSGameUtils build-height / packed chunk-key proof.
- `a5e219c7036937ce0ef4b5dfe5032bd82c764ee9`: VSGameUtils ResourceKey / Identifier identity proof.
- `ee7e9c56be55fd95114d0f7e194be69185db4385`: nullable translation-argument proof.
- `169e0007dcbeb2263701e6b41e40757de6d62ff2`: TestChair entity creation / positioning proof.
- `2c763500338955135d0700b273594a87dab9d982`: VSKeyBindings Category migration.
- `5c8a80eca1b996c4b89d5a394d7cfb9115d3f070`: CreativeModeTab.Output accessibility proof.
- `4641ae31765f0d067923cc1ef54b9a26abe99a19`: TestHingeBlockEntity ValueInput / ValueOutput persistence proof.
- `ea2084954eb4edd2bd9922aa1f59342b76709809`: MassDatapackResolver registry-tag lookup proof.
- `27e181c70184b2aac38eeb1a646905d93ba45023`: MassDatapackResolver typed reload-listener proof.
- `ac739bbf0c1598087a6ae9b158117c4764ce3079`: DimensionParametersResolver typed reload-listener proof.
- `2af9d9ba1d48f8a0baf825398d3d441b1219f19d`: VSEntityHandlerDataLoader typed reload-listener proof.
- `9d82234aa769a6a0eece07f52e7d5ace2d334aab`: VSGamePackets Identifier-vocabulary proof.
- `4a657f4625f69b26b9ccef9f7235cee271325d98`, `19d15fccf7345fc80f91800356a105d3595db87c`, `a40316e93a61594018fd6f8f9d4b913d7fb2eb80`, `563cbcba7bb1c92ca27820ef785d11bb88872524`, `75a434c728f1ca020b550882967085ccc53d5c3b`: earlier exact identifier/reload/minY/chunk-key proofs.

Locked negative evidence includes:
- `a72aaef8eca34a352ef949eeb57e6bbcda81171f`: `setUnsaved(false)` is invalid current API; do not replay without direct new evidence.
- VSKeyBindings failed partial probes `e108526cbd728454c175c76bffc610d4e074da49`, `fcc65187d79c4b546883875da3597345db1e01cd`, `e9a3efd58acb2af9539628eb2875e6cb829c3cec`, `fb3c7e65a4c2089f6fa695114734d14836bde1d3` remain negative evidence.
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
- active_proof_head: `f2b3ec68e0d2146bb8b443da76a62a4766e01fce; real VS2 ShipSavedData persistence API boundary complete and frozen`
- active_proof_run: `P0 35451366274 / job 105918982071 success; P1 35451366140 / job 105918981784 failure with ShipSavedData/MixinMinecraftServer persistence diagnostics absent; independent compiler clusters remain`
- active_hypothesis: `none selected; choose exactly one remaining standalone-P1 semantic cluster only after the resulting ledger-only HEAD passes exact-head P0 provenance`
- final_ready: `false`
- user_runtime_validation: `NOT_APPLICABLE_YET`
- video_status: `NOT_APPLICABLE_YET`

## Proven P1 progress

Build/toolchain and all previously frozen source/API overlays remain green at their exact boundaries. Current canonical P1 workflow applies fail-closed overlays against the pinned upstream gitlink and audits the resulting source delta before compile.

The current P1 compiler set is materially reduced. Exact run `35451366140` no longer reports ShipSavedData persistence errors. No Create/SNR/Copycats bridge work has been used to mask standalone VS2 failures.

## Remaining compiler areas from exact run `35451366140`

These are unresolved and independent from the frozen ShipSavedData proof:

- Create compatibility intermediary/classpath/API drift in `DeployerScrollOptionSlot.kt`. This remains P1 compile residue only; it is **not** permission to begin P3 or let Create define VS2 architecture.
- Rendering/entity-handler drift in `AbstractShipyardEntityHandler.kt`, `VSEntityHandler.kt`, and `WorldEntityHandler.kt`: current renderer buffer API, two-parameter `EntityRenderer<T, S>` / render-state semantics, and changed/removed `getRenderOffset`. `MultiBufferSource` is not authorized as a package-rename guess.
- `VSGamePackets` / `EntityDragger`: removed/changed `isControlledByLocalInstance` and `lerpTo`. These are authority-sensitive and remain locked pending exact 26.2 semantics; never replace them with teleport chase, synthetic carry velocity, manual clamps, fake inertia, or camera forcing.
- Sable dependency boundary in `SableCompat.kt`: unresolved `ryanhcode` / `SableCompanion`. Sable must be satisfied by a real dependency or an upstream-compatible documented boundary, never by a fake companion/package.

The chunk-ticket and ShipSavedData clusters are **not** remaining compiler areas after exact run `35451366140`.

## Engineering locks

- First-failure classification must stay factual: build/mappings/API/loader/mixin/VSCore-native/networking/storage/transforms/rendering/collision/entity-player-camera/Create bridge/SNR-Copycats/CI/final packaging.
- Make one evidence-backed root change at a time.
- Standalone real VS2 P1 must initialize before any Create bridge work.
- P2/M1 requires real VS2 ship lifecycle, translation+rotation, ship-space, collision, standing/walking, jump-airborne-natural landing, floor/walls/ceiling, free camera, entity dragging/reference-space, rendering, and client/server sync. No floor-only or fake-carry success counts.
- Frozen ticket proof authorizes only its exact load-only radius-zero add/remove lifecycle and `tryMarkSaved()` deletion cleanup. It does not authorize force-loading redesign.
- Frozen ShipSavedData proof authorizes only the `SavedDataType + Codec` API bridge and matching server acquisition change. It does not authorize alternate storage authority, world-file migration guesses, payload redesign, or manual save management.
- Rendering and authority-sensitive networking/entity dragging require direct current API semantics before edits.
- Do not use Create/SNR/Copycats as a P1 crutch.
- Do not record ordinary compile/debug/hypothesis-test video.
- `FINAL_READY` is forbidden from CI alone and requires exact-final-JAR real-user runtime acceptance.

## next_safe_action

1. Preserve frozen implementation `f2b3ec68e0d2146bb8b443da76a62a4766e01fce` and all prior frozen-green / negative evidence. Do not edit ShipSavedData, its Mixin registration, ticket lifecycle, or earlier frozen sites unless direct regression evidence appears.
2. This ledger-only freeze commit is **not** source proof. Require exact-head P0 provenance success for the resulting ledger HEAD before any further source mutation.
3. After that gate, inspect only exact P1 run `35451366140` plus exact Minecraft 26.2 API/source for **one** remaining standalone-P1 semantic cluster. Do not patch multiple independent clusters in one step.
4. Prefer the smallest well-bounded cluster with exact evidence. Rendering/entity-handler work must be treated as one renderer-state semantic unit, not a `MultiBufferSource` package rename. `VSGamePackets`/`EntityDragger` remains authority-sensitive. Sable requires real dependency evidence. Create compatibility must not become P3 architecture during P1.
5. Legacy 1.21.1 root-path `vs_ship_data.dat` migration is not proven by the current compile proof. Do not add file copying/moving until an explicit world-upgrade/runtime gate and exact current world-path semantics justify it.
6. Remain in standalone P1. Do not use Create/SNR/Copycats to hide standalone VS2 failures. Do not record ordinary compile/debug video.

## Video and final gate

- Video is closure-only, never a debugging tool.
- `M1_COMPLETE` is forbidden until the complete P2 real-VS2 runtime matrix is proven.
- `FINAL_BUILD` / `FINAL_VERIFY` / `FINAL_READY` are not applicable during P1.
- `FINAL_READY` still requires exact-final-JAR real-user runtime acceptance.
