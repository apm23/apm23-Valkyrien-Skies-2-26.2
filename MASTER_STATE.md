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

## Current reconciliation — RelocationUtil neighbor-update boundary proven and frozen

- Current proven implementation HEAD: `7a7e2f320605b27bb65e9f0bb6cb88d8aa41a4e7` (`P1: wire RelocationUtil neighbor-update proof`).
- The implementation consists of fail-closed overlay commit `916bc136a31c047d7412da2773e4cac50e05e065` plus canonical P1 workflow wiring at `7a7e2f320605b27bb65e9f0bb6cb88d8aa41a4e7`; no upstream submodule commit or gameplay implementation was replaced.
- Exact-head P0 provenance run `35444319197`, job `105900522741`, completed `success`; the exact upstream gitlink remained `f39132148e717d325933b4ce6e9e9fb13d929390`.
- Exact-head P1 standalone compile run `35444319187`, job `105900522796`, completed `failure` only because independent Minecraft 26.2 source/API clusters remain. The RelocationUtil neighbor-update overlay step, port-delta validation, Gradle runtime setup, and compile-log artifact upload completed successfully.
- Diagnostic artifact: `p1-compile-log-7a7e2f320605b27bb65e9f0bb6cb88d8aa41a4e7`, artifact ID `10584502598`, size `5102` bytes, ZIP SHA-256 `4e436a720b3cf94833a5e5bba483dad31194be04597a6ce5b5be9789cb6072c1`.
- Root cause proven for this isolated cluster: pinned upstream `RelocationUtil.updateBlock()` contains exactly two legacy `Level.blockUpdated(BlockPos, Block)` calls, each immediately following the corresponding `sendBlockUpdated(...)` phase. The legacy server neighbor-dispatch implementation maps through the same intermediary boundary now exposed as `updateNeighborsAt` in the current API. Because the upstream receiver remains typed as `Level`, the adapter preserves the old server/non-debug dispatch constraint explicitly rather than broadening execution.
- `scripts/apply_p1_relocationutil_blockupdated_26_2.py` therefore changes only those two legacy neighbor-dispatch sites to `level.updateNeighborsAt(...)` guarded by `!level.isClientSide && !level.isDebug()`. It is fail-closed on exact pinned contexts, requires exactly two guards/current calls, rejects any remaining `level.blockUpdated(`, and guards the already-frozen zero-flag direct writes plus adjacent update phases against accidental absorption.
- Exact P1 run `35444319187` contains no compiler diagnostic for either former RelocationUtil `blockUpdated` site and no new diagnostic at `updateNeighborsAt`, `isDebug`, or the inserted guards. Remaining RelocationUtil diagnostics are independent: block-entity/component ValueInput/ValueOutput boundaries and loot-key nullability.
- The prior RelocationUtil direct-chunk zero-flag proof remains frozen and unchanged: source AIR/destination rotated-state writes, ordering, direct-chunk boundary, and conditional `doUpdate -> updateBlock(...)` flow are preserved.
- This proof preserves `setBlocksDirty`, `sendBlockUpdated`, neighbor-shape propagation, analog-output notification, lighting checks, rotation and relocation ordering. It does **not** authorize changes to block-entity/component persistence, loot-table semantics, lighting policy, tickets, ship creation/allocation, transforms, physics, collision, entity dragging, rendering, networking authority, gameplay authority, or camera behavior.
- Scope reconciliation from prior ledger checkpoint `e99ceaec12be669d6e434e4bce7321d7113ad2a1` to the proven implementation HEAD changed only the new fail-closed RelocationUtil neighbor-update overlay and its canonical P1 workflow wiring; the pinned `upstream-vs2` gitlink was untouched.
- No code from retired `apm23/VS2-Create_Interactive` has been imported or reused as implementation source.

## Frozen proof ancestry / negative evidence

The immediately prior implementation proof is `ce6ff8bb8f06eeb8e98544f6bf9ca1e503936fdb` (RelocationUtil direct chunk-write flags). Its proof and all earlier historical proof records/failed probes remain frozen evidence and must not be replayed merely because a later compiler error resembles them.

Recent frozen implementation proofs include:
- `7a7e2f320605b27bb65e9f0bb6cb88d8aa41a4e7`: RelocationUtil neighbor-update boundary proof; P0 `35444319197` / job `105900522741`; P1 `35444319187` / job `105900522796`; artifact `10584502598`; SHA-256 `4e436a720b3cf94833a5e5bba483dad31194be04597a6ce5b5be9789cb6072c1`.
- `ce6ff8bb8f06eeb8e98544f6bf9ca1e503936fdb`: RelocationUtil direct `LevelChunk.setBlockState` zero-flag proof; P0 `35443067305` / job `105897176803`; P1 `35443067266` / job `105897176594`; artifact `10584129694`; SHA-256 `9b77b280a4e22a9f93da1242142ee481019a899b80f024d1fca87d2bbaafeb5d`.
- `2da9ca25e3ce6fd2f601cc2f6b626b0e3998a677`: ShipAssembler StructureProcessor adapter proof; P0 `35441650029` / job `105893372295`; P1 `35441650018` / job `105893372137`; artifact `10583543403`; SHA-256 `189afa0cf3d415972c0453bb1125b7ad4148a8437a728867168bc271238d60c5`.
- `aa26d707fac479c63a6a5e097ca65818dd145262`: ShipAssembler fast-path direct `LevelChunk.setBlockState` zero-flag proof; P0 `35440115550`; P1 `35440115578`; artifact `10583975623`.
- `12f182325f9f3e10c502afae7da567e4b1b95c28`: AssemblyUtil `blockUpdated` neighbor-dispatch proof; P0 `35438749400`; P1 `35438749392`; artifact `10583103574`.
- `644d108b111bed17d0f3259dc840803f7c9a3192`: AssemblyUtil block-entity Value I/O proof; P0 `35437312270`; P1 `35437312255`; artifact `10582397242`.
- `820ef37e8ca012fe484d9960242cbfc0eefbacc8`: AssemblyUtil ScheduledTick non-null generic proof; P0 `35436715908`; P1 `35436715912`; artifact `10582521058`.
- `a803150d066fdc7e0a0bfdd5bd1661b85c627417`: AssemblyUtil direct chunk-write zero-flag proof; P0 `35435474114`; P1 `35435474130`; artifact `10581468437`.
- `02e356638690d0413a105d409aaae4bcfd6e160c`: ShipAssembler BlockPos -> containing ChunkPos proof; P0 `35434876304`; P1 `35434876347`; artifact `10581693841`.
- `39e2abc40af3d785d4d6ca5f14ac7b28ef03334f`: ShipMountingEntity `kill(ServerLevel)` proof.
- `36549552477a1dd9b24cc12c6e21c6849b2e8b54`: ShipMountingEntity `hurtServer` proof.
- `0a23528d781baf280bb553a8f9fa94c21f447af2`: ShipMountingEntity Value I/O proof.
- `d258e69e46ce2f85c1ccb953dc97db7abd669841`: entity-handler projectile package proof.
- `3d8d7255d36f26da902e0d43e1c830fa5015594e`: VSGameEvents RenderType package proof.
- `24802fb75610a3ceb1614fda1a78cab1fab7cfe5`: VSGameUtils build-height / chunk-key proof.
- `a5e219c7036937ce0ef4b5dfe5032bd82c764ee9`: VSGameUtils ResourceKey / Identifier identity proof.
- `ee7e9c56be55fd95114d0f7e194be69185db4385`: nullable translation-argument proof.
- `169e0007dcbeb2263701e6b41e40757de6d62ff2`: TestChair entity creation / positioning proof.
- `2c763500338955135d0700b273594a87dab9d982`: VSKeyBindings current Category migration. Failed partial probes `e108526cbd728454c175c76bffc610d4e074da49`, `fcc65187d79c4b546883875da3597345db1e01cd`, `e9a3efd58acb2af9539628eb2875e6cb829c3cec`, and `fb3c7e65a4c2089f6fa695114734d14836bde1d3` remain negative evidence.
- `5c8a80eca1b996c4b89d5a394d7cfb9115d3f070`: CreativeModeTab.Output accessibility proof.
- `4641ae31765f0d067923cc1ef54b9a26abe99a19`: TestHingeBlockEntity ValueInput / ValueOutput persistence proof.
- `ea2084954eb4edd2bd9922aa1f59342b76709809`: MassDatapackResolver registry-tag lookup proof.
- `27e181c70184b2aac38eeb1a646905d93ba45023`: MassDatapackResolver typed reload-listener proof.
- `ac739bbf0c1598087a6ae9b158117c4764ce3079`: DimensionParametersResolver typed reload-listener proof.
- `2af9d9ba1d48f8a0baf825398d3d441b1219f19d`: VSEntityHandlerDataLoader typed reload-listener proof.
- `9d82234aa769a6a0eece07f52e7d5ace2d334aab`: VSGamePackets Identifier-vocabulary proof.
- `4a657f4625f69b26b9ccef9f7235cee271325d98`: VSEntityHandlerDataLoader Identifier proof.
- `19d15fccf7345fc80f91800356a105d3595db87c`: DimensionParametersResolver Identifier proof.
- `a40316e93a61594018fd6f8f9d4b913d7fb2eb80`: MassDatapackResolver Identifier proof.
- `563cbcba7bb1c92ca27820ef785d11bb88872524`: MassDatapackResolver dummy BlockGetter minY proof.
- `75a434c728f1ca020b550882967085ccc53d5c3b`: SeamlessChunksManager packed ChunkPos-key proof.

All other earlier frozen-green proofs recorded by prior ledger commits remain frozen even when not expanded here; Git history is retained as durable evidence.

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
- active_proof_head: `7a7e2f320605b27bb65e9f0bb6cb88d8aa41a4e7; RelocationUtil neighbor-update boundary complete and frozen`
- active_proof_run: `P0 35444319197 / job 105900522741 success; P1 35444319187 / job 105900522796 failure with both RelocationUtil legacy blockUpdated diagnostics cleared and no updateNeighborsAt/guard diagnostics; independent compiler clusters remain`
- active_hypothesis: `none selected; choose the next isolated standalone-P1 cluster only after exact Minecraft 26.2 API/source inspection`
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

Source/API clusters already proven clean include the earlier frozen items recorded in Git history plus these recent boundaries:
- exact ValueInput/ValueOutput migrations already frozen for TestHingeBlockEntity, ShipMountingEntity, and AssemblyUtil block-entity transfer;
- VSGameUtils ResourceKey/Identifier identity, height and packed chunk-key migrations;
- VSGameEvents RenderType package and projectile package relocations;
- ShipMountingEntity damage/removal/persistence signature bridges;
- ShipAssembler containing-ChunkPos conversion;
- ShipAssembler small-set direct LevelChunk zero-flag conversion;
- AssemblyUtil direct chunk-write flags, ScheduledTick non-null bound, block-entity Value I/O, and neighbor-dispatch bridges;
- ShipAssembler `ICopyableProcessor` current Minecraft 26.2 StructureProcessor interface/signature/codec adapter, preserving upstream processed destination block position/state/NBT and `onPaste` behavior;
- `RelocationUtil.relocateBlock()` two direct `LevelChunk.setBlockState(..., false)` third arguments migrated to Minecraft 26.2 zero integer flags while preserving the rotated state, source/destination writes, ordering, and the original conditional explicit `doUpdate -> updateBlock(...)` flow;
- `RelocationUtil.updateBlock()` two removed legacy `blockUpdated` neighbor-dispatch sites migrated to current `updateNeighborsAt(...)` with explicit server/non-debug guards preserving the legacy dispatch boundary.

## Remaining compiler areas from exact run `35444319187`

These remain unresolved and independent from the frozen RelocationUtil neighbor-update proof:

- Create compatibility intermediary/classpath/API drift in `DeployerScrollOptionSlot.kt`; this must not be used to pull P3/Create architecture into P1 or let Create mask standalone failures.
- `ShipSavedData`: broader SavedData persistence lifecycle/factory boundary (`save` no longer overrides). Exact Minecraft 26.2 semantics and the corresponding `MixinMinecraftServer` storage acquisition/registration must be migrated together while preserving the four existing Jackson byte-array payloads and one persistence authority.
- `ShipAssembler`: `tryClear` plus block-entity/component ValueInput/ValueOutput boundaries, including fast-path `loadWithComponents` sites; current chunk-ticket API drift around the former `addRegionTicket` site. The containing-ChunkPos conversion, two fast-path direct chunk-write flag arguments, and `ICopyableProcessor` StructureProcessor boundary are **not** remaining compiler areas.
- rendering/entity-handler drift: current renderer-buffer API (`MultiBufferSource` is not a simple package rename), current `EntityRenderer` generic/API boundary, and removed/changed `getRenderOffset` behavior.
- `VSGamePackets` / `EntityDragger`: removed/changed local-control and interpolation APIs (`isControlledByLocalInstance`, `lerpTo`) are authority-sensitive and remain locked pending exact semantics.
- chunk-ticket APIs in `ChunkManagement` / `VSTicketType` and the independent ShipAssembler ticket site.
- Sable dependency boundary.
- `RelocationUtil`: block-entity/component ValueInput/ValueOutput boundaries and loot-key nullability. Its two direct `LevelChunk.setBlockState` flag arguments and its two legacy `blockUpdated` neighbor-dispatch sites are **not** remaining compiler areas after the frozen proofs at `ce6ff8bb8f06eeb8e98544f6bf9ca1e503936fdb` and `7a7e2f320605b27bb65e9f0bb6cb88d8aa41a4e7`.

`AssemblyUtil.kt` has no remaining compiler diagnostic in exact run `35444319187`. The frozen ShipAssembler StructureProcessor boundary and both frozen RelocationUtil boundaries are no longer remaining compiler areas.

## Locked / deferred lessons

- Never mechanically invent a 26.2 API name from an old symbol. Inspect exact API semantics first.
- Frozen proofs authorize only their exact isolated adaptation; superficially similar sites require independent inspection.
- Frozen RelocationUtil neighbor-update proof authorizes only replacing the two pinned legacy `level.blockUpdated(...)` sites with guarded `level.updateNeighborsAt(...)`, preserving server/non-debug dispatch and all surrounding update phases. It does **not** authorize changing block-entity/component ValueInput/ValueOutput, loot-table handling, lighting, neighbor-shape ordering, analog-output handling, relocation ordering, ship lifecycle, transforms, physics, collision, networking, gameplay authority, or camera behavior.
- Frozen RelocationUtil direct chunk-write-flags proof authorizes only replacing the two pinned `LevelChunk.setBlockState(..., false)` third arguments with `0`, preserving the upstream rotated state, source/destination direct writes, ordering, no moved/additional direct-write bits, and conditional explicit `doUpdate` flow.
- Frozen ShipAssembler StructureProcessor proof authorizes only the current interface/signature/codec migration for `ICopyableProcessor` while continuing to use `processedBlockInfo.pos/state/nbt` for the upstream `onPaste` flow. It does not authorize structure-placement redesign, serialization of this runtime-only processor, assembly lifecycle changes, tickets, component transfer, transforms, physics, networking, or gameplay authority.
- Frozen ShipAssembler fast-path chunk-write proof authorizes only replacing the two pinned direct `LevelChunk.setBlockState(..., false)` third arguments with `0`, preserving no moved/additional flag bits and the upstream direct-chunk bypass.
- Frozen AssemblyUtil direct-write, ScheduledTick, block-entity Value I/O, and neighbor-dispatch proofs remain limited to those exact sites and semantics; they do not authorize mechanical copying into other relocation/assembly sites.
- `ShipSavedData` broader persistence lifecycle is a semantic boundary: migrate it together with the existing server storage registration/acquisition path, preserve exact payloads, and do not introduce a second persistence authority.
- Exact Minecraft 26.2 API evidence shows `MultiBufferSource` is not a simple package rename. Do not fabricate an equivalent renderer path.
- `VSGamePackets` / `EntityDragger` local-control and interpolation changes are authority-sensitive; never replace them with guessed per-tick movement, manual carry, teleport/setPos chase, synthetic velocity, or camera forcing.
- Chunk tickets must retain real loading/lifetime semantics; no permanent-force-load shortcut.
- Create compatibility errors are not permission to integrate Create early or use Create as a P1 crutch.
- Sable must be satisfied by a real dependency or documented upstream-compatible boundary; do not create a fake companion/package merely to compile.
- Retired `apm23/VS2-Create_Interactive` is historical warning evidence only and must never become implementation source.

## Mandatory architecture

Every core ported subsystem must remain traceable to upstream VS2 or be documented as a minimal 26.2 adaptation. The final architecture must retain real VS2 ship lifecycle/reference space, ship transforms, physics/collision, player standing/walking/jumping/landing, wall/floor/ceiling interaction, entity dragging/reference-space behavior, free stable camera/look, rendering, and client/server sync.

Forbidden as final architecture: custom VS2-style replacement frames, synthetic carry velocity/inertia, fake gravity, manual floor/wall/ceiling clamps, per-tick teleport/setPos chase, camera counter-rotation/forcing, duplicate authority, floor-only success, or helper matrices called VS2 without real VS2 ship lifecycle/reference space.

## Milestone order — do not skip

1. P0 upstream import/provenance.
2. P1 standalone real VS2 26.2 boot/compile/initialize. No Create/SNR/Copycats masking.
3. P2 / M1 standalone real-VS2 ship lifecycle with translation+rotation, ship-space, collisions, standing/walking, jump->airborne->natural landing, floor/walls/ceiling, free stable camera, entity dragging/reference-space, rendering, and client/server sync.
4. P3 Create Fly bridge only after P2 is frozen green; Create owns railway trajectory semantics while the carriage is one real VS2 ship/reference space through a legitimate VS2 integration boundary.
5. P4 add exact locked SNR + Copycats.
6. P5 production final stack -> exact final JAR -> final verify -> exact-JAR real-user runtime gate.

`M1_COMPLETE` is forbidden before P2 evidence is complete. `FINAL_READY` cannot come from CI alone.

## Failed hypotheses / negative evidence

- Preserve every failed probe recorded by prior ledger commits; do not replay them without new evidence.
- A timeout/disconnect never authorizes falling back to retired-project code, a simplified VS2-like architecture, speculative API names, broad stubs, or deleting difficult subsystems.
- A compile-green result for one isolated boundary proves only that boundary; it does not authorize adjacent semantic changes.

## next_safe_action

1. Preserve the frozen `7a7e2f320605b27bb65e9f0bb6cb88d8aa41a4e7` RelocationUtil neighbor-update proof, `ce6ff8bb8f06eeb8e98544f6bf9ca1e503936fdb` RelocationUtil direct chunk-write-flags proof, `2da9ca25e3ce6fd2f601cc2f6b626b0e3998a677` ShipAssembler StructureProcessor proof, all recent AssemblyUtil proofs, and all earlier frozen-green/negative evidence. Do not edit those sites unless direct regression evidence appears.
2. This ledger-only freeze commit must not be treated as source proof. Require exact-head P0 provenance success for the resulting ledger HEAD before any further source mutation.
3. Then inspect only exact run `35444319187` plus exact Minecraft 26.2 API/source for **one** remaining standalone-P1 compiler cluster. Do not patch multiple clusters in one step.
4. `ShipSavedData` remains deliberately deferred until its SavedData type/codec/factory plus `MixinMinecraftServer` storage boundary can be proven as one semantic unit. Do not guess it from the isolated `save overrides nothing` diagnostic.
5. Do not mechanically extend either frozen RelocationUtil proof into its remaining ValueInput/ValueOutput/component or loot-key boundaries. Likewise do not mechanically extend prior ShipAssembler/AssemblyUtil changes into ticketing, renderer, authority-sensitive entity/networking, Sable, or Create compatibility. Choose exactly one root hypothesis only after semantic inspection, then use the smallest fail-closed traceable overlay and prove it separately.
6. Remain in standalone P1. Do not use Create/SNR/Copycats to hide standalone VS2 failures. Do not record ordinary compile/debug/hypothesis-test video.

## Video and final gate

Video is closure-only, never an ordinary debugging tool. A short video is allowed only when a user-visible runtime blocker is already closure-ready from data/runtime proof, using the exact same source HEAD/build and unaltered gameplay/physics/input/fixture/route/timing. Visible failure overrides telemetry green. Media failure permits at most one media-only repair and never gameplay changes. If separate review is required, emit the exact `VIDEO_REVIEW_REQUIRED: ...` handoff and HOLD. Any actual video review must be recorded as `VIDEO_AUTO_REVIEW` with artifacts preserved.

`FINAL_READY = false`. Exact-final-JAR real-user runtime acceptance remains mandatory.