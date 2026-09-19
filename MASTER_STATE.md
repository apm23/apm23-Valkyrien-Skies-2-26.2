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

## Current reconciliation — real VS2 ship chunk-ticket lifecycle bridge proven and frozen

- Current proven implementation HEAD: `65a42e782de192f27d5bf720691d6e08f395a719` (`P1: use current chunk saved-state API`).
- Ticket implementation ancestry for this proof: fail-closed source overlay `b0a3a18303b325d55bf9a3deb156705644ba6ed4`, canonical P1 workflow wiring `a72aaef8eca34a352ef949eeb57e6bbcda81171f`, and same-cluster saved-state API correction `65a42e782de192f27d5bf720691d6e08f395a719`.
- The immediately preceding ledger-only HEAD `c0e371dec6a805ecc31bd94fc58b7a0549aac9bf` had exact-head P0 provenance success before this source mutation. No upstream submodule commit was changed.
- Exact-head P0 provenance for implementation HEAD `65a42e782de192f27d5bf720691d6e08f395a719`: run `35450402081`, job `105916444806`, completed `success`; exact upstream identity remained pinned to `f39132148e717d325933b4ce6e9e9fb13d929390`.
- Exact-head P1 standalone compile: run `35450402031`, job `105916444686`, completed `failure` only because independent P1 compiler clusters remain. The ticket overlay step, port-delta validation, Gradle runtime setup, and compile-log artifact upload all completed successfully.
- Diagnostic artifact: `p1-compile-log-65a42e782de192f27d5bf720691d6e08f395a719`, artifact ID `10585479315`, size `4617` bytes, ZIP SHA-256 `4443fd49b99f2fed5b44ee21529b543c503b4ff8494d6ca45b06572aaf9ceede`.
- Exact P1 run `35450402031` contains **no compiler diagnostic** for `ShipAssembler.kt`, `ChunkManagement.kt`, `VSTicketType.kt`, `addRegionTicket`, `removeRegionTicket`, `addTicketWithRadius`, `removeTicketWithRadius`, `TicketType`, `isUnsaved`, `setUnsaved`, or `tryMarkSaved`.
- Root cause proven for this semantic cluster:
  - pinned upstream uses generic `TicketType<ChunkPos>` plus `TicketType.create(name, comparator)` and value-bearing `addRegionTicket/removeRegionTicket(type, pos, radius, value)`;
  - current Minecraft removes the arbitrary per-ticket value at this boundary and uses radius-ticket add/remove methods;
  - current `ChunkAccess` no longer provides the old writable saved-state API; the current clean transition is `tryMarkSaved()`;
  - real VS2 relies on this ticket lifecycle to retain watched shipyard chunks while the ship exists and to remove the ticket only after the ship is actually gone.
- Minimal Minecraft 26.2 adaptation now proven:
  - `VSTicketType.SHIP_CHUNK` becomes non-generic `TicketType(0L, TicketType.FLAG_LOADING)`: permanent until explicit removal and **load-only**, with no `FLAG_SIMULATION` broadening;
  - all three real VS2 ticket sites preserve radius `0` and use the current add/remove radius pair;
  - `ShipAssembler` preserves its original batch order: add ticket -> distance-manager update -> synchronous FULL chunk acquisition;
  - `ChunkManagement` preserves add-on-watch, keeps the ticket while `shipStillAlive`, removes it only inside the existing `!shipStillAlive` deletion branch, and leaves non-shipyard `updateChunkForced(..., true/false)` behavior untouched;
  - the preexisting actual-ship-delete clean-marker site becomes `chunk?.tryMarkSaved()` only; no persistence authority or save lifecycle is added.
- Failed same-cluster probe retained as negative evidence: implementation HEAD `a72aaef8eca34a352ef949eeb57e6bbcda81171f`, P0 run `35450050046` success, P1 run `35450050048` / job `105915510997` failure. Its ticket add/remove and `TicketType` migration were already compiler-clean, but the guessed `chunk?.setUnsaved(false)` call failed because that current API does not exist. Artifact `10585964821`, size `4655`, SHA-256 `0bb0e33794c93535f1ca714716f43ee6078fb643ee347b919d67033ddee4c7e7`. Do not replay `setUnsaved(false)` without new direct API evidence.
- This proof is **not** a permanent-force-load redesign: ticket radius/lifetime intent, ship existence test, unload condition, assembly ordering, ship creation/allocation, transforms, physics, collision, entity dragging, rendering, networking/gameplay authority, and camera behavior remain upstream VS2 behavior.
- This proof does **not** authorize `FLAG_SIMULATION`, changed radius, extra force-loading, ticket persistence redesign, altered ship deletion semantics, renderer/network/entity authority changes, SavedData redesign, Sable replacement, or Create integration.
- No code from retired `apm23/VS2-Create_Interactive` was imported or reused as implementation source.
- No video was recorded: this was compile/API evidence, not a closure-ready user-visible runtime blocker.

## Frozen proof ancestry / negative evidence

All frozen-green and negative-evidence records that existed in Git history through ledger HEAD `c0e371dec6a805ecc31bd94fc58b7a0549aac9bf` remain binding. Ledger compaction does not unfreeze or supersede any earlier proof. Do not replay a failed probe or edit a frozen site merely because a later compiler error looks similar.

Recent implementation proofs that remain explicitly frozen include:
- `65a42e782de192f27d5bf720691d6e08f395a719`: real VS2 ship chunk-ticket lifecycle bridge; P0 `35450402081` / job `105916444806`; P1 `35450402031` / job `105916444686`; artifact `10585479315`; SHA-256 `4443fd49b99f2fed5b44ee21529b543c503b4ff8494d6ca45b06572aaf9ceede`.
- `30b9f70d3c6c71dfd30ca76339e19cfcb56461e4`: ShipAssembler block-entity ValueInput bridge; P0 `35449327885` / job `105913627681`; P1 `35449327899` / job `105913627933`; artifact `10586298547`; SHA-256 `96a45d028aa15f9f40fae05e3af7319ee25e04ebbb43014095fbf54f057358da`.
- `45de97f06a3ab25c1e19b0dc09790ebde2d8e851`: ShipAssembler Clearable bridge; P0 `35447608712` / job `105909150192`; P1 `35447608701` / job `105909150252`; artifact `10586550933`; SHA-256 `c373b0dd58a6f9a3bb4249b7dde1d9157023c1a173db5a1185445c3489ddaf87`.
- `e923ba7658197ff04af605e85507618c09dd390b`: RelocationUtil block-entity ValueInput bridge; P0 `35446235563` / job `105905519369`; P1 `35446235562` / job `105905519515`; canonical artifact `10585438767`; SHA-256 `5d86810672cbbfe03fc7c455542dba838cbf07847bd81256ece32d344d037e13`.
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
- `2c763500338955135d0700b273594a87dab9d982`: VSKeyBindings Category migration; failed partial probes `e108526cbd728454c175c76bffc610d4e074da49`, `fcc65187d79c4b546883875da3597345db1e01cd`, `e9a3efd58acb2af9539628eb2875e6cb829c3cec`, and `fb3c7e65a4c2089f6fa695114734d14836bde1d3` remain negative evidence.
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

The failed `a72aaef8eca34a352ef949eeb57e6bbcda81171f` `setUnsaved(false)` partial probe is specifically locked as negative evidence. All older frozen proof metadata and failed hypotheses remain available in Git history and remain authoritative even when not expanded here.

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
- active_proof_head: `65a42e782de192f27d5bf720691d6e08f395a719; real VS2 ship chunk-ticket lifecycle bridge complete and frozen`
- active_proof_run: `P0 35450402081 / job 105916444806 success; P1 35450402031 / job 105916444686 failure with the complete ticket-lifecycle cluster absent from diagnostics; independent compiler clusters remain`
- active_hypothesis: `none selected; choose exactly one remaining standalone-P1 semantic cluster only after the resulting ledger-only HEAD passes exact-head P0 provenance`
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

Recent source/API clusters proven clean include:
- TestHingeBlockEntity, ShipMountingEntity, AssemblyUtil, RelocationUtil and ShipAssembler block-entity Value I/O boundaries already frozen;
- VSGameUtils identity/height/chunk-key migrations, VSGameEvents RenderType, entity projectile packages, and recent entity signature bridges;
- ShipAssembler containing-ChunkPos, direct chunk-write flags, StructureProcessor, Clearable, and block-entity ValueInput boundaries;
- AssemblyUtil direct chunk-write flags, ScheduledTick non-null bound, block-entity Value I/O, and neighbor dispatch;
- RelocationUtil direct chunk-write flags, neighbor dispatch, pending loot-table clear, and block-entity ValueInput;
- **real VS2 ship chunk-ticket lifecycle across `ShipAssembler` + `ChunkManagement` + `VSTicketType`**, preserving radius-zero load-only tickets, exact add/remove lifecycle, ship-alive retention, actual-delete cleanup, and ShipAssembler preload ordering.

`ShipAssembler.kt`, `ChunkManagement.kt`, `VSTicketType.kt`, `RelocationUtil.kt`, and `AssemblyUtil.kt` have no remaining compiler diagnostic in exact run `35450402031`.

## Remaining compiler areas from exact run `35450402031`

These remain unresolved and independent from the frozen ticket proof:

- Create compatibility intermediary/classpath/API drift in `DeployerScrollOptionSlot.kt`. This must not be used to pull P3/Create architecture into P1 or let Create mask standalone failures.
- `ShipSavedData`: broader SavedData persistence lifecycle/factory boundary (`save` no longer overrides). Exact Minecraft 26.2 semantics and the corresponding `MixinMinecraftServer` storage acquisition/registration must be migrated together while preserving the four existing Jackson byte-array payloads and one persistence authority.
- Rendering/entity-handler drift: current renderer-buffer API (`MultiBufferSource` is not a simple package rename), current two-parameter `EntityRenderer<T, S>` / render-state boundary, and removed/changed `getRenderOffset` behavior.
- `VSGamePackets` / `EntityDragger`: removed/changed local-control and interpolation APIs (`isControlledByLocalInstance`, `lerpTo`). These are authority-sensitive and remain locked pending exact semantics.
- Sable dependency boundary in `SableCompat.kt`.

The chunk-ticket cluster is **not** a remaining compiler area after exact run `35450402031`.

## Locked / deferred lessons

- Never invent a 26.2 API name from an old symbol. Inspect exact API semantics and then prove the smallest change.
- Frozen proofs authorize only their exact isolated adaptation; superficially similar sites require independent inspection.
- Frozen ticket proof authorizes only the current non-generic permanent load-only `TicketType(0L, FLAG_LOADING)`, radius-zero add/remove pair, preserved ship-alive removal guard, preserved ShipAssembler preload ordering, and `tryMarkSaved()` at the existing actual-delete cleanup site. It does not authorize simulation tickets, larger radius, permanent force-loading shortcuts, changed deletion semantics, saved-data redesign, transforms, physics, collision, entity dragging, renderer/network authority, camera behavior, or Create integration.
- `setUnsaved(false)` is a failed hypothesis for the current API and must not be replayed without new direct evidence.
- `ShipSavedData` is a semantic persistence boundary: migrate its SavedData type/codec/factory together with `MixinMinecraftServer` storage acquisition/registration, preserve exact payloads, and do not introduce a second persistence authority.
- `MultiBufferSource` is not a simple package rename. Do not fabricate an equivalent renderer path.
- `VSGamePackets` / `EntityDragger` local-control/interpolation changes are authority-sensitive. Never replace them with guessed per-tick movement, manual carry, teleport/setPos chase, synthetic velocity, or camera forcing.
- Create compatibility diagnostics are not permission to integrate Create early or use Create as a P1 crutch.
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

- Preserve every failed probe recorded by this ledger and earlier ledger commits; do not replay them without new evidence.
- Ticket same-cluster failed probe `a72aaef8eca34a352ef949eeb57e6bbcda81171f`: `setUnsaved(false)` is invalid on current `LevelChunk`; exact corrected implementation uses `tryMarkSaved()` and is compiler-clean at `65a42e782de192f27d5bf720691d6e08f395a719`.
- A timeout/disconnect never authorizes falling back to retired-project code, a simplified VS2-like architecture, speculative API names, broad stubs, or deleting difficult subsystems.
- A compile-green result for one isolated boundary proves only that boundary; it does not authorize adjacent semantic changes.

## next_safe_action

1. Preserve frozen implementation `65a42e782de192f27d5bf720691d6e08f395a719` and all prior frozen-green/negative evidence. Do not edit the ticket lifecycle or earlier frozen sites unless direct regression evidence appears.
2. This ledger-only freeze commit is **not** source proof. Require exact-head P0 provenance success for the resulting ledger HEAD before any further source mutation.
3. After that provenance gate, inspect only exact P1 run `35450402031` plus exact Minecraft 26.2 API/source for **one** remaining standalone-P1 semantic cluster. Do not patch multiple independent clusters in one step.
4. `ShipSavedData` remains deliberately deferred unless its SavedData type/codec/factory plus `MixinMinecraftServer` storage acquisition/registration are inspected and migrated as one persistence semantic unit.
5. Do not mechanically extend the frozen ticket, serialization, Clearable, relocation, or AssemblyUtil proofs into renderer, authority-sensitive entity/networking, Sable, or Create compatibility.
6. Remain in standalone P1. Do not use Create/SNR/Copycats to hide standalone VS2 failures. Do not record ordinary compile/debug/hypothesis-test video.

## Video and final gate

Video is closure-only, never an ordinary debugging tool. A short video is allowed only when a user-visible runtime blocker is already closure-ready from data/runtime proof, using the exact same source HEAD/build and unaltered gameplay/physics/input/fixture/route/timing. Visible failure overrides telemetry green. Media failure permits at most one media-only repair and never gameplay changes. If separate review is required, emit the exact `VIDEO_REVIEW_REQUIRED: ...` handoff and HOLD. Any actual video review must be recorded as `VIDEO_AUTO_REVIEW` with artifacts preserved.

`FINAL_READY = false`. Exact-final-JAR real-user runtime acceptance remains mandatory.
