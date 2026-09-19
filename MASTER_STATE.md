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

## Current reconciliation — VSGameUtils ResourceKey / Identifier boundary proven and frozen

- Current proven implementation HEAD: `a5e219c7036937ce0ef4b5dfe5032bd82c764ee9` (`p1: run VSGameUtils ResourceKey Identifier proof`).
- Exact-head P0 provenance run `35427279261`, job `105855291717`, completed `success`; the exact upstream gitlink remained `f39132148e717d325933b4ce6e9e9fb13d929390`.
- Exact-head P1 standalone compile run `35427279257`, job `105855291754`, completed `failure` only because independent Minecraft 26.2 source/API clusters remain.
- Every overlay step through this proof, `Show and validate port delta`, and Gradle runtime setup completed successfully; compilation reached the real `:common:compileKotlin` boundary.
- Root cause proven for this isolated cluster: pinned upstream VS2's `DimensionId` bridge uses Minecraft `ResourceKey` through `ResourceKeyAccessor`; Minecraft 26.2 changed the resource vocabulary from `ResourceLocation` to `Identifier` and the public key accessor from `location()` to `identifier()`, while the private `ResourceKey.create(Identifier, Identifier)` shape and `registryName` field used by the existing VS2 mixin accessor/invoker remain available.
- `scripts/apply_p1_vsgameutils_resourcekey_identifier_26_2.py` is fail-closed and targets exactly three upstream files:
  - `common/src/main/kotlin/org/valkyrienskies/mod/common/VSGameUtils.kt`
  - `common/src/main/java/org/valkyrienskies/mod/mixin/accessors/resource/ResourceKeyAccessor.java`
  - `common/src/main/java/org/valkyrienskies/mod/mixin/world/level/MixinLevel.java`
- The adaptation preserves the exact upstream dimension identity architecture: `DimensionId` is still encoded as `<registry namespace>:<registry path>:<dimension namespace>:<dimension path>`, the same cache remains authoritative, and `getResourceKey()` still reconstructs the key through the existing `ResourceKeyAccessor.callCreate(...)` invoker rather than introducing a new dimension/reference-space system.
- The patch only changes `ResourceLocation -> Identifier`, the accessor/invoker parameter/return vocabulary accordingly, and `dim.location() -> dim.identifier()`.
- No build-height semantics, chunk packing/tickets, ship lifecycle, ship/reference-space, transforms, physics, collision, entity dragging, player/camera, networking, authority, or gameplay behavior is changed by this proof.
- Exact run `35427279257` contains **no remaining compiler diagnostic for the former `ResourceLocation` sites in `VSGameUtils.kt`, `ResourceKeyAccessor.java`, or `MixinLevel.java` and no replacement diagnostic in the Java mixin files**. The only remaining `VSGameUtils.kt` diagnostics are the deliberately untouched independent sites: `minBuildHeight`, `maxBuildHeight`, and `ChunkPos.asLong`.
- Diagnostic artifact: `p1-compile-log-a5e219c7036937ce0ef4b5dfe5032bd82c764ee9`, artifact ID `10578904709`, size `6028` bytes, ZIP SHA-256 `6bbcd694cdeb5c5fe6bbb00bcaaf0b322092df30ca3e1a5b241007e836b137ad`.
- No code from retired `apm23/VS2-Create_Interactive` has been imported or reused as implementation source.

## Frozen proof ancestry / negative evidence

The immediately prior ledger checkpoint is `276720126ad05965270c5a88679f994971fdb2ae` (`ledger: freeze nullable translation argument proof`). Its historical proof records and failed probes remain frozen evidence and must not be replayed merely because a later compiler error resembles them.

- `ee7e9c56be55fd95114d0f7e194be69185db4385`: nullable translation-argument proof; P0 `35426650197` / job `105853673536`; P1 `35426650191` / job `105853673479`; artifact `10579029076`; SHA-256 `4d66cffe1cc65e689f321233c2b65aaf524699874214c41fc7b97ff1c198afba`.
- `169e0007dcbeb2263701e6b41e40757de6d62ff2`: TestChair entity creation / positioning proof; P0 `35424938143` / job `105849132808`; P1 `35424938174` / job `105849132961`; artifact `10578643862`; SHA-256 `d9e90d3e6ec99f1203285e429f69be9ba6a5c82aae7e209196f93dcb88e938d1`.
- `2c763500338955135d0700b273594a87dab9d982`: VSKeyBindings current `KeyMapping.Category` migration plus localized translation bridge; P0 `35424232816` / job `105847304720`; P1 `35424232856` / job `105847304996`; artifact `10578617703`; SHA-256 `c9e0d1f2f1e18390794ee14f41493e133d2d174c4e0fa58463c2381983013bb1`. Failed partial probes `e108526cbd728454c175c76bffc610d4e074da49`, `fcc65187d79c4b546883875da3597345db1e01cd`, `e9a3efd58acb2af9539628eb2875e6cb829c3cec`, and `fb3c7e65a4c2089f6fa695114734d14836bde1d3` are negative evidence.
- `5c8a80eca1b996c4b89d5a394d7cfb9115d3f070`: `CreativeModeTab.Output` accessibility proof; P0 `35423048611` / job `105844091418`; P1 `35423048671` / job `105844092374`; artifact `10578021452`; SHA-256 `f5691678a8ebdd7967c193846b906b8114fa4bacd9068836f061d83a9bb0cd1b`.
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
- active_proof_head: `a5e219c7036937ce0ef4b5dfe5032bd82c764ee9; VSGameUtils ResourceKey / Identifier boundary complete and frozen`
- active_proof_run: `P0 35427279261 / job 105855291717 success; P1 35427279257 / job 105855291754 failure with ResourceKey/Identifier/mixin diagnostics cleared; remaining VSGameUtils diagnostics are only minBuildHeight, maxBuildHeight, and asLong`
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
- `VSGameUtils` / `ResourceKeyAccessor` / `MixinLevel` ResourceKey identity bridge migrated to Minecraft 26.2 `Identifier` vocabulary while preserving the existing VS2 DimensionId encoding, cache, accessor/invoker path, and dimension semantics.

## Remaining compiler areas from exact run `35427279257`

These remain unresolved and independent from the frozen VSGameUtils ResourceKey/Identifier proof:

- Create compatibility intermediary/classpath/API drift in `DeployerScrollOptionSlot.kt`; this must not be used to pull P3/Create architecture into P1.
- `ShipSavedData` broader SavedData `save` lifecycle/factory boundary.
- `VSGameUtils` now has only the untouched build-height / chunk-position sites: `minBuildHeight`, `maxBuildHeight`, and `ChunkPos.asLong`; the ResourceKey/Identifier/mixin-facing vocabulary subcluster is proven clear.
- `AssemblyUtil` and `ShipAssembler`: block update flags, scheduled ticks, ValueInput/ValueOutput component persistence, shipyard allocation, structure processor API, chunk tickets, and related semantics.
- `ShipMountingEntity`: current entity persistence (`ValueInput`/`ValueOutput`), server hurt contract, and constructor/level boundary.
- rendering/entity-handler drift: render-state generics, buffer/render type classes, projectile class relocations, and render-offset boundary.
- `VSGamePackets` / `EntityDragger`: removed/changed local-control and interpolation APIs (`isControlledByLocalInstance`, `lerpTo`) are authority-sensitive and remain locked pending exact semantics.
- chunk-ticket APIs in `ChunkManagement` / `VSTicketType` and ShipAssembler.
- Sable dependency boundary.
- `RelocationUtil`: ValueInput/ValueOutput/component loading, loot-key nullability, update flags, and related relocation semantics.

The ResourceKey/Identifier/mixin-vocabulary subcluster is **not** a remaining compiler area after `a5e219c7036937ce0ef4b5dfe5032bd82c764ee9`.

## Locked / deferred lessons

- Never mechanically invent a 26.2 API name from an old symbol. Inspect exact API semantics first.
- Frozen nullable ship-slug semantics: do not add `slug ?: ...`, synthetic names, empty-string fallback, or any alternate naming authority. The bridge forwards the original nullable value directly.
- Frozen VSGameUtils ResourceKey identity semantics: retain the upstream four-part DimensionId encoding, existing cache, and ResourceKey accessor/invoker architecture; do not replace it with a new dimension identifier or reference-space authority merely because 26.2 renamed resource classes/accessors.
- `ShipSavedData` broader SavedData save/factory lifecycle is a semantic boundary; prior byte-array Optional proof does not authorize a broad persistence rewrite.
- The remaining `VSGameUtils` build-height and chunk-key sites are separate from the frozen ResourceKey identity proof; inspect exact 26.2 semantics before mutation even though equivalent APIs have been proven elsewhere.
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
3. P2 / M1 standalone real-VS2 ship lifecycle with translation+rotation, ship-space, collisions, standing/walking, jump→airborne→natural landing, floor/walls/ceiling, free stable camera, entity dragging/reference-space, rendering, and client/server sync.
4. P3 Create Fly bridge: only after P2 is frozen green; Create owns railway trajectory semantics while the carriage is one real VS2 ship/reference space through a legitimate VS2 integration boundary.
5. P4 add exact locked SNR + Copycats.
6. P5 production final stack → exact final JAR → final verify → exact-JAR real-user runtime gate.

`M1_COMPLETE` is forbidden before P2 evidence is complete. `FINAL_READY` cannot come from CI alone.

## Failed hypotheses / negative evidence

- Preserve every failed probe recorded in prior ledgers, especially the four VSKeyBindings probes listed above; do not replay them without new evidence.
- A timeout/disconnect never authorizes falling back to retired-project code, a simplified VS2-like architecture, speculative API names, broad stubs, or deleting difficult subsystems.
- A compile-green result for one isolated boundary proves only that boundary; it does not authorize adjacent semantic changes.

## next_safe_action

1. Preserve the frozen `a5e219c7036937ce0ef4b5dfe5032bd82c764ee9` VSGameUtils ResourceKey/Identifier proof, the prior `ee7e9c56be55fd95114d0f7e194be69185db4385` nullable-translation proof, and all earlier frozen-green proofs. Do not edit those sites unless direct regression evidence appears.
2. After this ledger-only commit, require exact-head P0 provenance success before any further source mutation.
3. Then inspect only the newest compiler evidence plus the exact Minecraft 26.2 API for **one** remaining isolated cluster. Do not mechanically patch the locked ShipSavedData, ShipMountingEntity, assembly/relocation, authority-sensitive entity/networking, rendering, ticketing, Sable, remaining VSGameUtils build-height/chunk-key, or Create-compat boundaries without semantic proof.
4. Choose exactly one root hypothesis only after API inspection, then use the smallest fail-closed traceable overlay and prove that cluster separately.
5. Remain in standalone P1. Do not use Create/SNR/Copycats to hide standalone VS2 failures. Do not record ordinary compile/debug/hypothesis-test video.

## Video and final gate

Video is closure-only, never an ordinary debugging tool. A short video is allowed only when a user-visible runtime blocker is already closure-ready from data/runtime proof, using the exact same source HEAD/build and unaltered gameplay/physics/input/fixture/route/timing. Visible failure overrides telemetry green. Media failure permits at most one media-only repair and never gameplay changes. If separate review is required, emit the exact `VIDEO_REVIEW_REQUIRED: ...` handoff and HOLD. Any actual video review must be recorded as `VIDEO_AUTO_REVIEW` with artifacts preserved.

`FINAL_READY = false`. Exact-final-JAR real-user runtime acceptance remains mandatory.