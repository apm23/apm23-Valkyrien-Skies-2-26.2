# MASTER_STATE — REAL VS2 26.2 PORT

GitHub code is the implementation source of truth. This file is the durable continuity ledger; chat memory is not authoritative.

## Project identity

- Repository: `apm23/apm23-Valkyrien-Skies-2-26.2`
- Mission: port the **actual original Valkyrien Skies 2 source** to Minecraft Java/Fabric 26.2, then integrate Create Fly / Steam 'n' Rails / Copycats only after standalone real VS2 is proven.
- Hard contract: **VS2 ASLI. BUKAN SYSTEM MIRIP VS2.**
- Architecture contract: `PORT_CONTRACT.md`
- Exact dependency/environment lock: `BASELINE_LOCK.json`
- Upstream provenance: `UPSTREAM_PROVENANCE.md`

## Authoritative upstream baseline

- repository: `ValkyrienSkies/Valkyrien-Skies-2`
- branch used to select baseline: `1.21.1/main`
- exact commit: `f39132148e717d325933b4ce6e9e9fb13d929390`
- exact root tree: `91116399605d3ecd1c93b0011560e09281ee1fa4`
- upstream mod version: `2.4.12`
- imported as git submodule/gitlink `upstream-vs2/`

The upstream baseline remains pinned. Minecraft 26.2 changes are applied by explicit fail-closed overlays so every adaptation remains traceable to upstream VS2 source.

## Current reconciliation — AssemblyUtil block-entity Value I/O boundary proven and frozen

- Current proven implementation HEAD: `644d108b111bed17d0f3259dc840803f7c9a3192` (`P1: wire AssemblyUtil block-entity Value I/O proof`).
- Exact-head P0 provenance run `35437312270`, job `105882063557`, completed `success`; the exact upstream gitlink remained `f39132148e717d325933b4ce6e9e9fb13d929390`.
- Exact-head P1 standalone compile run `35437312255`, job `105882063508`, completed `failure` only because independent Minecraft 26.2 source/API clusters remain.
- Every overlay step through this proof, including `Apply traceable P1 AssemblyUtil block-entity Value I/O overlay`, `Show and validate port delta`, Gradle runtime setup, and diagnostic artifact upload completed successfully; compilation reached the real `:common:compileKotlin` boundary.
- Root cause proven for this isolated cluster: pinned upstream 1.21.1 `AssemblyUtil.copyBlock()` serializes the source block entity with `saveWithId(level.registryAccess())`, preserves the resulting `CompoundTag`, calls the existing `level.setBlockEntity(blockentity)` in the existing order, obtains the destination block entity, then calls `loadWithComponents(data, level.registryAccess())`. Minecraft 26.2 retains the core `BlockEntity.saveWithId(ValueOutput)` and `BlockEntity.loadWithComponents(ValueInput)` methods but removes those legacy `CompoundTag` convenience signatures. The behavior-preserving adaptation therefore wraps the same serialization flow through vanilla `TagValueOutput` / `TagValueInput` with the same registry context rather than replacing the block-entity lifecycle or payload.
- `scripts/apply_p1_assemblyutil_blockentity_value_io_26_2.py` is fail-closed and targets exactly the pinned-upstream block-entity transfer context in:
  - `common/src/main/kotlin/org/valkyrienskies/mod/common/assembly/AssemblyUtil.kt`
- The overlay replaces the removed convenience calls with `TagValueOutput.createWithContext(ProblemReporter.DISCARDING, level.registryAccess())`, the existing upstream `blockentity.saveWithId(...)`, `output.buildResult()`, and `TagValueInput.create(ProblemReporter.DISCARDING, level.registryAccess(), data)` passed to the existing upstream `newBlockentity?.loadWithComponents(...)` call. It rejects the old convenience signatures and verifies the expected new bridge fragments exactly once.
- This proof preserves the upstream `saveWithId` payload, the same `CompoundTag` handoff, the existing `state.hasBlockEntity() && blockentity != null` guard, `level.setBlockEntity(blockentity)` call and ordering, destination `level.getBlockEntity(to)` lookup, the existing `promotePendingBlockEntity()` TODO, and `loadWithComponents` semantics/components. It does **not** change scheduled ticks, `blockUpdated`, assembly ordering, relocation, ship allocation, transforms, physics, collision, networking, gameplay authority, or camera behavior.
- Exact run `35437312255` contains **no compiler diagnostic for the former `AssemblyUtil.kt` block-entity ValueInput/ValueOutput mismatch sites** and no new `TagValueOutput`, `TagValueInput`, or `ProblemReporter` diagnostic in `AssemblyUtil`. Remaining `AssemblyUtil` diagnostics are isolated to `blockUpdated` at current lines 68 and 78. This proof clears only the block-entity Value I/O boundary and does not make overall P1 green.
- Diagnostic artifact: `p1-compile-log-644d108b111bed17d0f3259dc840803f7c9a3192`, artifact ID `10582397242`, size `5749` bytes, ZIP SHA-256 `fd4272fe431b27cb5b027f3de0b8074d60d8955feb54bc7b349825f0d29e2544`.
- Scope reconciliation from prior ledger checkpoint `5273c6d8b475b4af914ffad9f995b0b783f065de` to the proven implementation HEAD changed only the new fail-closed AssemblyUtil block-entity Value I/O overlay and its canonical P1 workflow wiring; the pinned `upstream-vs2` gitlink was untouched.
- `ShipSavedData` remains deliberately deferred: Minecraft 26.2 moves `SavedData` persistence from an overrideable `save(...)` path to a `SavedDataType<T>` + codec/factory boundary while pinned upstream `MixinMinecraftServer` owns acquisition and the real VS2 pipeline. That boundary must migrate together while preserving the four existing Jackson byte-array payloads and single persistence authority.
- No code from retired `apm23/VS2-Create_Interactive` has been imported or reused as implementation source.

## Frozen proof ancestry / negative evidence

The immediately prior implementation proof is `820ef37e8ca012fe484d9960242cbfc0eefbacc8` (AssemblyUtil ScheduledTick non-null generic boundary). Its proof and all earlier historical proof records/failed probes remain frozen evidence and must not be replayed merely because a later compiler error resembles them.

- `820ef37e8ca012fe484d9960242cbfc0eefbacc8`: AssemblyUtil ScheduledTick non-null generic proof; P0 `35436715908` / job `105880520574`; P1 `35436715912` / job `105880520583`; artifact `10582521058`; SHA-256 `cf6aeb758b898fb145f0d3202a94637f74adb4b1378f38cde5c19e97e6f00c9b`.
- `a803150d066fdc7e0a0bfdd5bd1661b85c627417`: AssemblyUtil direct LevelChunk setBlockState zero-flags proof; P0 `35435474114` / job `105877267158`; P1 `35435474130` / job `105877267372`; artifact `10581468437`; SHA-256 `f93516bbf73daa3394f9bec8bd02e3739096426266e0da2284a64d622b364dbd`.
- `02e356638690d0413a105d409aaae4bcfd6e160c`: ShipAssembler BlockPos -> containing ChunkPos proof; P0 `35434876304` / job `105875729916`; P1 `35434876347` / job `105875729982`; artifact `10581693841`; SHA-256 `16c9d994cfca10b1566d24358aca2bff50b4a32b6500b92c9c8d1fd10d5aebf7`.
- `39e2abc40af3d785d4d6ca5f14ac7b28ef03334f`: ShipMountingEntity server-side `kill(ServerLevel)` proof; P0 `35434315954` / job `105874293333`; P1 `35434315959` / job `105874293420`; artifact `10581682906`; SHA-256 `8af4a4710cfe7d2ab1b9bcf5ffd0be3f97055609a612c8690f0c4ccde63c5b66`.
- `36549552477a1dd9b24cc12c6e21c6849b2e8b54`: ShipMountingEntity inherited damage / hurtServer proof; P0 `35432663975` / job `105869895197`; P1 `35432664106` / job `105869895568`; artifact `10581685492`; SHA-256 `ac252f8e89dcc39c07e7d63ea509261d463425cdd68e36a865defff43aa36748`.
- `0a23528d781baf280bb553a8f9fa94c21f447af2`: ShipMountingEntity empty ValueInput/ValueOutput persistence proof; P0 `35431393828` / job `105866541183`; P1 `35431393814` / job `105866541088`; artifact `10580972918`; SHA-256 `d5945476e91ed5e11d3be78eb674926c02a3257b2c94aff4ad8855852f92a3df`.
- `d258e69e46ce2f85c1ccb953dc97db7abd669841`: entity-handler projectile package proof; P0 `35430098076` / job `105863012876`; P1 `35430098141` / job `105863013026`; artifact `10580801201`; SHA-256 `fe1f4f2b5042f4c71d079648a8636b6292036293c199ade14b8f844341ac0086`.
- `3d8d7255d36f26da902e0d43e1c830fa5015594e`: VSGameEvents RenderType package proof; P0 `35428910241` / job `105859745816`; P1 `35428910211` / job `105859745706`; artifact `10579819254`; SHA-256 `06a36ed3226f0a1f22e1e0a332eb3f6b44c44c537376cb1731ea1a9831d70fea`.
- `24802fb75610a3ceb1614fda1a78cab1fab7cfe5`: VSGameUtils build-height / chunk-key proof; P0 `35427744252` / job `105856539289`; P1 `35427743996` / job `105856538642`; artifact `10579727750`; SHA-256 `35defb49532853a55d5e0b52e6d49efff3e1e5392d4766a455e068c42eea2bcb`.
- `a5e219c7036937ce0ef4b5dfe5032bd82c764ee9`: VSGameUtils ResourceKey / Identifier boundary proof; P0 `35427279261` / job `105855291717`; P1 `35427279257` / job `105855291754`; artifact `10578904709`; SHA-256 `6bbcd694cdeb5c5fe6bbb00bcaaf0b322092df30ca3e1a5b241007e836b137ad`.
- `ee7e9c56be55fd95114d0f7e194be69185db4385`: nullable translation-argument proof; P0 `35426650197` / job `105853673536`; P1 `35426650191` / job `105853673479`; artifact `10579029076`; SHA-256 `4d66cffe1cc65e689f321233c2b65aaf524699874214c41fc7b97ff1c198afba`.
- `169e0007dcbeb2263701e6b41e40757de6d62ff2`: TestChair entity creation / positioning proof; P0 `35424938143` / job `105849132808`; P1 `35424938174` / job `105849132961`; artifact `10578643862`; SHA-256 `d9e90d3e6ec99f1203285e429f69be9ba6a5c82aae7e209196f93dcb88e938d1`.
- `2c763500338955135d0700b273594a87dab9d982`: VSKeyBindings current `KeyMapping.Category` migration plus localized translation bridge; P0 `35424232816` / job `105847304720`; P1 `35424232856` / job `105847304996`; artifact `10578617703`; SHA-256 `c9e0d1f2f1e18390794ee14f41493e133d2d174c4e0fa58463c2381983013bb1`. Failed partial probes `e108526cbd728454c175c76bffc610d4e074da49`, `fcc65187d79c4b546883875da3597345db1e01cd`, `e9a3efd58acb2af9539628eb2875e6cb829c3cec`, and `fb3c7e65a4c2089f6fa695114734d14836bde1d3` are negative evidence.
- `5c8a80eca1b996c4b89d5a394d7cfb9115d3f070`: `CreativeModeTab.Output` accessibility proof; P0 `35423048611` / job `105844091418`; P1 `35423048671` / job `105844092374`; artifact `10578021452`; SHA-256 `f5691678a8ebdd7967c193846b9068836f061d83a9bb0cd1b`.
- `4641ae31765f0d067923cc1ef54b9a26abe99a19`: TestHingeBlockEntity `ValueInput` / `ValueOutput` persistence proof; P0 `35421661792` / job `105840387680`; P1 `35421661791` / job `105840387789`; artifact `10577638892`; SHA-256 `a6b44f7d7248a9364dc31f1ddc9231ffa45212a895f10db752be4b432deae47a`.
- `ea2084954eb4edd2bd9922aa1f59342b76709809`: MassDatapackResolver registry-tag lookup proof; P0 `35420504812` / job `105837166152`; P1 `35420504781` / job `105837162566`; artifact `10577252400`; SHA-256 `d0dab3e4652c4d00f62f1c9aeccaae98c8a1401e8651e86bd9de7aa12d2f28ac`.
- `27e181c70184b2aac38eeb1a646905d93ba45023`: MassDatapackResolver typed reload-listener proof.
- `ac739bbf0c1598087a6ae9b158117c4764ce3079`: DimensionParametersResolver typed reload-listener proof.
- `2af9d9ba1d48f8a0baf825398d3d441b1219f19d`: VSEntityHandlerDataLoader typed reload-listener proof.
- `9d82234aa769a6a0eece07f52e7d5ace2d334aab`: VSGamePackets Identifier-vocabulary proof.
- `4a657f4625f69b26b9ccef9f7235cee271325d98`: VSEntityHandlerDataLoader Identifier proof.
- `19d15fccf7345fc80f91800356a105d3595db87c`: DimensionParametersResolver Identifier proof.
- `a40316e93a61594018fd6f8f9d4b913d7fb2eb80`: MassDatapackResolver Identifier proof.
- `563cbcba7bb1c92ca27820ef785d11bb88872524`: MassDatapackResolver dummy BlockGetter minY proof.
- `75a434c728f1ca020b550882967085ccc53d5c3b`: SeamlessChunksManager packed ChunkPos-key proof.

All other earlier frozen-green proofs recorded by prior ledgers remain frozen even when not expanded here.

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
- active_proof_head: `644d108b111bed17d0f3259dc840803f7c9a3192; AssemblyUtil block-entity Value I/O boundary complete and frozen`
- active_proof_run: `P0 35437312270 / job 105882063557 success; P1 35437312255 / job 105882063508 failure with the AssemblyUtil block-entity Value I/O diagnostics cleared; remaining AssemblyUtil diagnostics are only blockUpdated at current lines 68 and 78`
- active_hypothesis: `none selected; choose the next isolated cluster only after exact Minecraft 26.2 API inspection`
- final_ready: `false`
- user_runtime_validation: `NOT_APPLICABLE_YET`
- video_status: `NOT_APPLICABLE_YET`

## Proven P1 progress

Build/toolchain frozen green:
- Java 25 + Gradle 9.5.1 starts;
- Minecraft 26.x build uses `dev.architectury.loom-no-remap` without Mojang mappings/remapJar;
- Gradle 9 archive API migration is applied;
- old mod dependency configurations are adapted for no-remap Loom;
- dependency resolution reaches the real `:common:compileKotlin` boundary;
- all explicit source overlays are fail-closed.

Source/API clusters already proven clean include:
- data-provider and registry-holder `ResourceLocation -> Identifier` migrations;
- BlockStateInfoProvider, SimpleSoundInstanceOnShip, VSEntityManager, DimensionParametersResolver, MassDatapackResolver, VSEntityHandlerDataLoader, and isolated VSGamePackets resource-vocabulary sites;
- EntityData non-null generic bounds and guarded Optional numeric/NBT reads;
- previously frozen Direction accessor migrations;
- TestThrusterBlock neighborChanged signature and RaycastUtils directional/nullability boundary;
- Minecraft player and dynamic command permission migrations;
- TestHingeBlock shape/ticker/onPaste/removal migrations;
- TestHingeBlockEntity exact ValueInput/ValueOutput persistence adaptation;
- ShipSavedData load-time byte-array Optional unwraps only;
- CompatUtil center/build-height/collision-context migrations;
- SeamlessChunksManager packed chunk-key migration;
- typed raw-JSON reload listeners and MassDatapackResolver registry-tag lookup;
- EmptyRenderer Identifier/render-state migration;
- ValkyrienSkiesMod resource vocabulary + CreativeModeTab.Output accessibility;
- VSKeyBindings current Category migration with legacy localization semantics preserved;
- TestChairBlock current entity-create / `snapTo` adaptation while preserving original VS2 mounting/riding flow;
- six nullable ship-slug translation sites through `NullableTranslatableCompat`, preserving exact nullable values without fallback;
- `VSGameUtils` / `ResourceKeyAccessor` / `MixinLevel` ResourceKey identity bridge migrated to Minecraft 26.2 `Identifier` vocabulary while preserving the existing VS2 DimensionId encoding, cache, accessor/invoker path, and dimension semantics;
- `VSGameUtils` build-height range and packed ticking-chunk key migrated to `getMinY()` / `getHeight()` / `ChunkPos.pack(...)` with the original inclusive range and packed-coordinate semantics preserved;
- `VSGameEvents` RenderType package migrated to Minecraft 26.2 `net.minecraft.client.renderer.rendertype.RenderType` while preserving the two upstream event payloads and existing renderer emitter architecture;
- `AbstractShipyardEntityHandler` and `WorldEntityHandler` projectile imports migrated to the Minecraft 26.2 `projectile.arrow` / `projectile.hurtingprojectile` subpackages while preserving the original VS2 projectile branch behavior unchanged;
- `ShipMountingEntity` empty entity-persistence hooks migrated from `CompoundTag` to Minecraft 26.2 `ValueInput` / `ValueOutput`, preserving the intentionally empty upstream behavior and vanilla entity persistence lifecycle;
- `ShipMountingEntity` inherited generic damage behavior bridged to Minecraft 26.2 `hurtServer(...)` using the current base invulnerability predicate and `markHurt()` while preserving the upstream inherited always-false result and without adding new damage authority;
- `ShipMountingEntity` server-only empty-passenger self-removal migrated from upstream `kill()` to Minecraft 26.2 `kill(level() as ServerLevel)` while preserving the existing branch, timing, and authority;
- `ShipAssembler.getDistinctChunksFromBlockPosSet()` migrated from legacy `ChunkPos(BlockPos)` construction to current `ChunkPos.containing(BlockPos)`, preserving only the original containing-chunk set semantics;
- `AssemblyUtil.removeBlock()` and `AssemblyUtil.copyBlock()` direct `LevelChunk.setBlockState` third arguments migrated from legacy `false` moved-state booleans to Minecraft 26.2 zero integer flags, preserving the original no-moving/no-additional-flags direct chunk-write semantics while leaving the explicit update flow untouched;
- `AssemblyUtil.copyBlock()` pending block-tick explicit generic migrated from `ScheduledTick<Block?>` to `ScheduledTick<Block>` while preserving the exact upstream `state.block`, destination `to`, `0` trigger tick, `0` sub-tick order, guard, default priority, and `LevelTicks.schedule` flow;
- `AssemblyUtil.copyBlock()` block-entity transfer migrated from the removed CompoundTag convenience signatures to vanilla Minecraft 26.2 `TagValueOutput` / `TagValueInput` around the same upstream `saveWithId` / `loadWithComponents` flow, preserving the same registry context, serialized payload/tag handoff, null guard, `setBlockEntity` ordering, destination lookup, and component-loading semantics.

## Remaining compiler areas from exact run `35437312255`

These remain unresolved and independent from the frozen AssemblyUtil block-entity Value I/O proof:

- Create compatibility intermediary/classpath/API drift in `DeployerScrollOptionSlot.kt`; this must not be used to pull P3/Create architecture into P1.
- `ShipSavedData` broader persistence lifecycle/factory boundary. Exact Minecraft 26.2 API inspection shows this requires a current SavedData type/codec/factory boundary and the corresponding `MixinMinecraftServer` storage registration to migrate together while preserving the existing VS2 byte-array payloads and pipeline ownership.
- `AssemblyUtil` now has only `blockUpdated` API drift at current lines 68 and 78. The block-entity Value I/O transfer, line-39 `ScheduledTick<Block?>` explicit generic mismatch, and the two direct `LevelChunk.setBlockState(..., false)` Boolean-to-Int flag sites are **not** remaining compiler areas.
- `ShipAssembler` line-248+ areas only: `tryClear`, component ValueInput/ValueOutput, shipyard allocation/API, structure processor API, its own update-flag sites, chunk tickets and related semantics. The line-94 BlockPos-to-ChunkPos conversion is **not** a remaining compiler area.
- rendering/entity-handler drift: `MultiBufferSource` renderer-buffer API rework, current `EntityRenderer` generic/API boundary, and `getRenderOffset`. Projectile class relocation is **not** a remaining compiler area.
- `VSGamePackets` / `EntityDragger`: removed/changed local-control and interpolation APIs (`isControlledByLocalInstance`, `lerpTo`) are authority-sensitive and remain locked pending exact semantics.
- chunk-ticket APIs in `ChunkManagement` / `VSTicketType` and ShipAssembler.
- Sable dependency boundary.
- `RelocationUtil`: ValueInput/ValueOutput/component loading, loot-key nullability, update flags, and related relocation semantics.

`VSGameUtils.kt`, `VSGameEvents.kt`, the `AbstractArrow` / `AbstractHurtingProjectile` package sites, all three proven `ShipMountingEntity` adaptation boundaries (empty persistence hooks, `hurtServer(...)`, and server-side `kill(ServerLevel)`), the `ShipAssembler.getDistinctChunksFromBlockPosSet()` containing-chunk conversion, the two `AssemblyUtil` direct chunk-write flag arguments, the `AssemblyUtil` ScheduledTick explicit generic bound, and the `AssemblyUtil` block-entity Value I/O bridge are **not** remaining compiler areas after their frozen proofs.

## Locked / deferred lessons

- Never mechanically invent a 26.2 API name from an old symbol. Inspect exact API semantics first.
- Frozen nullable ship-slug semantics: do not add `slug ?: ...`, synthetic names, empty-string fallback, or any alternate naming authority. The bridge forwards the original nullable value directly.
- Frozen VSGameUtils ResourceKey identity semantics: retain the upstream four-part DimensionId encoding, existing cache, and ResourceKey accessor/invoker architecture; do not replace it with a new dimension identifier or reference-space authority merely because 26.2 renamed resource classes/accessors.
- Frozen VSGameUtils height semantics: preserve `minY` and the original inclusive maximum as `getMinY() + getHeight() - 1`; do not reinterpret the Y range.
- Frozen VSGameUtils packed chunk-key semantics: use Minecraft's current `ChunkPos.pack(x, z)` equivalent for the original packed `(x,z)` key; do not invent a custom key or alter chunk ticking policy.
- Frozen VSGameEvents RenderType proof authorizes only the event payload package migration. It does **not** authorize renderer/entity-handler rewrites, render-state/generic changes, pass reordering, alternate buffer ownership, or any replacement rendering pipeline.
- Frozen entity-handler projectile proof authorizes only the `AbstractArrow` / `AbstractHurtingProjectile` package relocation. It does **not** authorize movement, velocity, rotation, dragging, renderer, interpolation, or authority changes.
- Frozen ShipMountingEntity persistence proof authorizes only the two intentionally empty entity-persistence hook signatures (`CompoundTag` to `ValueInput` / `ValueOutput`). It does not authorize constructor/level changes, movement/reference-space behavior, or any new persisted payload.
- Frozen ShipMountingEntity hurtServer proof authorizes only the exact Minecraft 26.2 bridge for the generic inherited 1.21.1 Entity damage contract: base invulnerability check, `markHurt()` for the same hurt/velocity-sync marking, and `false` return. It does **not** authorize new damage/destruction behavior, mounting/controller changes, movement/reference-space behavior, networking authority, or camera logic.
- Frozen ShipMountingEntity kill(ServerLevel) proof authorizes only passing the existing server-side entity level to Minecraft 26.2 `Entity.kill(ServerLevel)` inside the already-existing empty-passenger branch. It does **not** authorize new removal timing, passenger handling, constructor/level redesign, mounting/controller behavior, movement/reference-space changes, networking authority, or camera logic.
- Frozen ShipAssembler containing-chunk proof authorizes only the `getDistinctChunksFromBlockPosSet()` BlockPos-to-containing-ChunkPos conversion. It does **not** authorize `tryClear`, allocation, block movement, component persistence, structure processors, update flags, ticketing, transforms, physics, collision, networking, or any assembly lifecycle redesign.
- Frozen AssemblyUtil direct chunk-write-flags proof authorizes only replacing the two pinned `LevelChunk.setBlockState(..., false)` third arguments with `0` to preserve the original non-moving/no-additional-flags semantics. It does **not** authorize changing `updateBlock()` / `updateBlockFast()`, scheduled-tick transfer, block-entity/component persistence, `blockUpdated`, relocation, assembly order, ship allocation, transforms, physics, networking, or gameplay authority.
- Frozen AssemblyUtil ScheduledTick non-null proof authorizes only changing the pinned explicit generic from `ScheduledTick<Block?>` to `ScheduledTick<Block>`. It does **not** authorize changing the scheduled block type, source/destination, trigger tick, sub-tick order, priority, deduplication/guard semantics, transfer policy, block-entity persistence, neighbor updates, relocation, assembly, transforms, physics, networking, or gameplay authority.
- Frozen AssemblyUtil block-entity Value I/O proof authorizes only the vanilla Minecraft 26.2 NBT-backed `TagValueOutput` / `TagValueInput` bridge around the upstream `saveWithId` / `loadWithComponents` flow with the same registry context, tag handoff, guard, `setBlockEntity` order, destination lookup, and component-loading semantics. It does **not** authorize changing the component/persistence payload, block-entity lifecycle/order, `blockUpdated`, relocation, assembly logic, ship lifecycle, transforms, physics, networking, or gameplay authority.
- Exact Minecraft 26.2 API evidence shows `MultiBufferSource` is not a simple package rename. Do not mechanically import-rewrite or fabricate an equivalent; inspect current renderer-buffer semantics before adaptation.
- `ShipSavedData` broader persistence lifecycle is a semantic boundary: migrate `ShipSavedData` together with its `MixinMinecraftServer` storage registration, preserve the exact four existing Jackson byte-array payloads and real VS2 pipeline ownership, and do not introduce a second persistence authority.
- TestChair proof authorizes only its existing chair create/place flow; it does not authorize ShipMountingEntity internals or moving-space changes.
- `VSGamePackets` / `EntityDragger` local-control and interpolation APIs are authority-sensitive; never replace them with guessed per-tick movement, manual carry, teleports, or camera forcing.
- Assembly/Relocation ValueInput/ValueOutput migrations must preserve block-entity/component semantics rather than merely compile.
- Chunk tickets must retain real loading/lifetime semantics; no permanent-force-load shortcut.
- Create compatibility errors are not permission to integrate Create early or use Create as a P1 crutch.
- Rendering changes must stay inside real VS2 rendering architecture.
- Sable must be satisfied by a real dependency or documented upstream-compatible boundary; no local mock pretending to be Sable.
- Retired `apm23/VS2-Create_Interactive` is historical warning evidence only and must never become implementation source.

## Sable contract

Do not create a fake `SableCompanion`, dummy `ryanhcode` package, or locally reimplemented Sable behavior merely to clear compilation. Resolve the real dependency/API boundary or document a minimal legitimate compatibility adaptation.

## Mandatory architecture

Every core ported subsystem must remain traceable to upstream VS2 or be documented as a minimal 26.2 adaptation. The final architecture must retain real VS2 ship lifecycle/reference space, ship transforms, physics/collision, player standing/walking/jumping/landing, wall/floor/ceiling interaction, entity dragging/reference-space behavior, free stable camera/look, rendering, and client/server sync.

Forbidden as final architecture: custom VS2-style replacement frames, synthetic carry velocity/inertia, fake gravity, manual floor/wall/ceiling clamps, per-tick teleport/setPos chase, camera counter-rotation/forcing, duplicate authority, floor-only success, or helper matrices called VS2 without real VS2 ship lifecycle/reference space.

## Milestone order — do not skip

1. P0 upstream import/provenance.
2. P1 standalone real VS2 26.2 boot/compile/initialize. No Create/SNR/Copycats masking.
3. P2 / M1 standalone real-VS2 ship lifecycle with translation+rotation, ship-space, collisions, standing/walking, jump->airborne->natural landing, floor/walls/ceiling, free stable camera, entity dragging/reference-space, rendering, and client/server sync.
4. P3 Create Fly bridge: only after P2 is frozen green; Create owns railway trajectory semantics while the carriage is one real VS2 ship/reference space through a legitimate VS2 integration boundary.
5. P4 add exact locked SNR + Copycats.
6. P5 production final stack -> exact final JAR -> final verify -> exact-JAR real-user runtime gate.

`M1_COMPLETE` is forbidden before P2 evidence is complete. `FINAL_READY` cannot come from CI alone.

## Failed hypotheses / negative evidence

- Preserve every failed probe recorded in prior ledgers, especially the four VSKeyBindings probes listed above; do not replay them without new evidence.
- A timeout/disconnect never authorizes falling back to retired-project code, a simplified VS2-like architecture, speculative API names, broad stubs, or deleting difficult subsystems.
- A compile-green result for one isolated boundary proves only that boundary; it does not authorize adjacent semantic changes.

## next_safe_action

1. Preserve the frozen `644d108b111bed17d0f3259dc840803f7c9a3192` AssemblyUtil block-entity Value I/O proof, `820ef37e8ca012fe484d9960242cbfc0eefbacc8` AssemblyUtil ScheduledTick non-null proof, `a803150d066fdc7e0a0bfdd5bd1661b85c627417` AssemblyUtil direct chunk-write-flags proof, `02e356638690d0413a105d409aaae4bcfd6e160c` ShipAssembler containing-chunk proof, `39e2abc40af3d785d4d6ca5f14ac7b28ef03334f` ShipMountingEntity kill(ServerLevel) proof, `36549552477a1dd9b24cc12c6e21c6849b2e8b54` ShipMountingEntity hurtServer proof, `0a23528d781baf280bb553a8f9fa94c21f447af2` ShipMountingEntity Value I/O proof, `d258e69e46ce2f85c1ccb953dc97db7abd669841` entity-handler projectile package proof, `3d8d7255d36f26da902e0d43e1c830fa5015594e` VSGameEvents RenderType proof, `24802fb75610a3ceb1614fda1a78cab1fab7cfe5` VSGameUtils build-height/chunk-key proof, `a5e219c7036937ce0ef4b5dfe5032bd82c764ee9` ResourceKey/Identifier proof, `ee7e9c56be55fd95114d0f7e194be69185db4385` nullable-translation proof, and all earlier frozen-green proofs. Do not edit those sites unless direct regression evidence appears.
2. After this ledger-only commit, require exact-head P0 provenance success before any further source mutation.
3. Then inspect only the newest compiler evidence from exact run `35437312255` plus the exact Minecraft 26.2 API for **one** remaining isolated cluster. `AssemblyUtil.blockUpdated` at current lines 68/78 is a candidate only after exact API semantics are proven; do not mechanically replace it. Do not patch `ShipSavedData`, remaining `ShipAssembler` semantic boundaries, renderer-buffer / `EntityRenderer` / `getRenderOffset`, assembly/relocation persistence, authority-sensitive entity/networking, ticketing, Sable, or Create-compat boundaries without semantic proof.
4. Choose exactly one root hypothesis only after API inspection, then use the smallest fail-closed traceable overlay and prove that cluster separately.
5. Remain in standalone P1. Do not use Create/SNR/Copycats to hide standalone VS2 failures. Do not record ordinary compile/debug/hypothesis-test video.

## Video and final gate

Video is closure-only, never an ordinary debugging tool. A short video is allowed only when a user-visible runtime blocker is already closure-ready from data/runtime proof, using the exact same source HEAD/build and unaltered gameplay/physics/input/fixture/route/timing. Visible failure overrides telemetry green. Media failure permits at most one media-only repair and never gameplay changes. If separate review is required, emit the exact `VIDEO_REVIEW_REQUIRED: ...` handoff and HOLD. Any actual video review must be recorded as `VIDEO_AUTO_REVIEW` with artifacts preserved.

`FINAL_READY = false`. Exact-final-JAR real-user runtime acceptance remains mandatory.
