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

## Current reconciliation — canonical P1 chain through LevelChunk serialization boundary

Current proven implementation boundary before this documentation-only reconciliation commit:

- canonical implementation HEAD: `9b229bbadfc3bab5ed918556144ad566ca37e448` (`ci: adapt LevelChunk serialization API for 26.2`).
- exact-head P0 provenance run `35490917259`: **success**.
- exact-head standalone P1 compile run `35490917263` (#122): **frontier-only failure** after all overlay/apply and port-delta validation steps succeeded.
- compile artifact: `p1-compile-log-9b229bbadfc3bab5ed918556144ad566ca37e448`, ID `10598698213`, digest `sha256:3570994e4fa4ca17c9e64b5ccd0aee49f51e09583829d3931e3624b65fedf80d`.
- extracted compile log contains **69 `: error:` diagnostics across 8 normalized source files**.
- `MixinLevelChunk.java`, `ChunkSerializer`, and `SerializableChunkData` have **zero mentions** in the exact-head compile log.
- immediately prior exact-head `82887915b04b1546129ab0dba610d4ba0ed7e075` had P0 run `35490652424` success and P1 run `35490652399` frontier-only failure with artifact `10598289555`; that artifact contained **72 diagnostics across 9 normalized source files**. `MixinNoiseBasedChunkGenerator.java`, `GenerationStep.Carving`, and `applyCarvers` were absent, proving the preceding applyCarvers adaptation clean.
- therefore the LevelChunk serialization bridge removed exactly the LevelChunk source unit from the observed frontier without reopening previously frozen units.

### LevelChunk serialization boundary — frozen green

Pinned upstream target:
`common/src/main/java/org/valkyrienskies/mod/mixin/world/chunk/MixinLevelChunk.java`.

Minimal Minecraft 26.2 bridge installed by canonical HEAD `9b229bbadfc3bab5ed918556144ad566ca37e448`:

- `ChunkSerializer` import -> `SerializableChunkData`.
- `ChunkSerializer.write((ServerLevel) srcChunk.getLevel(), srcChunk)` -> `SerializableChunkData.copyOf((ServerLevel) srcChunk.getLevel(), srcChunk).write()`.
- `ChunkSerializer.read(...)` -> `SerializableChunkData.parse((ServerLevel) level, level.registryAccess(), compoundTag).read(...)` using the same target level, POI manager, `RegionStorageInfo`, and `ChunkPos` already selected by upstream VS2.

Authority preserved exactly:

- the existing VS2 copy-between-dimensions flow remains authoritative;
- source/target chunk selection is unchanged;
- block/entity transfer, pending block-entity NBT, post-processing, structures/references, tick containers, light flag, and heightmap recomputation remain unchanged;
- no ship lifecycle, ticket lifecycle, transform, movement, collision, entity dragging, camera, rendering, or reference-space authority was introduced or replaced.

Evidence:

- fail-closed replacement counts passed in run `35490917263`.
- port-delta validation passed in run `35490917263`.
- exact-head compile artifact `10598698213` contains 69 diagnostics / 8 source files and zero LevelChunk/ChunkSerializer/SerializableChunkData mentions.

Do not reopen this boundary absent direct contradictory compile/runtime evidence.

### Recent mechanical Java convergence — preserved

The following already-landed changes are preserved and must not be repeated blindly:

- `28ee0eabe77778dd2f9bbd84e528d9c3a6718531`: client sound mixin `ResourceLocation` -> `Identifier`; exact-head run `35489919714` proved the targeted sound frontier absent.
- `4aa395c810476d78c2f8cfb1bee423d2f5248616`: `MixinMinecraftServer` `BlockUtil` package relocation to `net.minecraft.util.BlockUtil`; exact-head run `35490199268` proved the target absent.
- `880df3aa1ecbdaf2a5b9974d65dd68a266fbc764`: `MixinChunkMap` `DimensionDataStorage` -> `SavedDataStorage`; P0 run `35490412205` succeeded and subsequent compile state moved beyond that type failure.
- `82887915b04b1546129ab0dba610d4ba0ed7e075`: remove obsolete `GenerationStep.Carving` import/handler argument from the existing `applyCarvers` injection; P0 `35490652424` success and artifact `10598289555` contains zero target mentions.
- `9b229bbadfc3bab5ed918556144ad566ca37e448`: LevelChunk serialization vocabulary bridge described above; P0 `35490917259` success and artifact `10598698213` proves target absence.

These are API/mapping adaptations only. None authorize a replacement VS2 architecture.

## Frozen architecture-sensitive boundaries

All frozen-green records and all negative evidence already committed in Git history remain binding even where this ledger is compacted. Ledger compaction does **not** unfreeze or supersede prior proof.

Key frozen boundaries include:

- **Real VS2 ship chunk-ticket lifecycle** — implementation `65a42e782de192f27d5bf720691d6e08f395a719`; proof `35450402031`. Load-only radius-zero explicit ticket add/remove lifecycle, flush/order, ship-alive removal guard, and deletion cleanup remain authority.
- **DistanceManager / TicketStorage read bridge** — implementation `8a338f95103227ed6a5acb35804d573bbae0d96c`; proof HEAD `ca07a2fff0fd922cbbd578a0531d3377313827de`; P0 `35463018487`; proof `35463018541`. Read-only compatibility only; never expand it into replacement ticket lifecycle.
- **ShipSavedData persistence** — implementation `f2b3ec68e0d2146bb8b443da76a62a4766e01fce`; proof `35451366140`. Overworld saved-data storage remains authority; codec/type changes are API bridges only.
- **Entity local authority / interpolation** — implementation `b7e583af13598b6ddcc583380872f578b8a40bb8`; proof HEAD `9f2719be070e79b91b7f47ceddaec61d7f5cff40`; proof `35455551701`. Existing dragging information, ship transforms, and interpolation authority remain intact; no synthetic carry system.
- **Entity renderer submit lifecycle** — implementation `a87512437f40a3bfa1325d78f8e2588587ec7cc8`; proof HEAD `58d8554ba623896d486b91f18771df9bdcd6f2b3`; proof `35458380245`. Real VS2 render authorities remain authoritative.
- **Shipyard teleport API mapping** — P0 `35467615792`; proof `35467615790`. Real VS2 ship-to-world transform remains authority; no manual packet/setPos/teleport chase.
- **NaturalSpawner, particle collision, EntitySectionStorage, WaterFluid, POIManager, AirAndWaterRandomPos, tick-ship-chunks, ship-debug overlay, world-weather, clip-replace, LavaFluid, Explosion, and StructureTemplate** canonical proof boundaries remain frozen green.
- **Clip-replace Direction vocabulary** — canonical `5d0fd81810a824b2da989b834dd6d2f92475dc33`; P0 `35478903000`; proof `35478902949`.
- **LavaFluid randomTick ServerLevel boundary** — canonical `19b0e356b34dae20c3aa8d9409d90fc0b96838b2`; P0 `35479600636`; proof `35479600673`.
- **Explosion Level client accessor boundary** — canonical `322dcf22e2baf25192682d4b9ee942f4a35dc86b`; P0 `35480514635`; proof `35480514714`.
- **Optional Sable Companion boundary** — compile-only. It does not authorize bundling or claiming a 1.21.1 Sable runtime on Minecraft 26.2.
- **Optional Create deployer helper isolation** — P1 compile isolation only, never a substitute for later real Create integration.

## Locked negative evidence

- `3bcbf90c75dc4d02448cfdb4590cc9c9674e0ed6` / run `35454717409`: wrong Kotlin-source-set exclusion for `DeployerScrollOptionSlot.kt`; do not replay.
- `a72aaef8eca34a352ef949eeb57e6bbcda81171f`: `setUnsaved(false)` is invalid current API; do not replay absent direct new evidence.
- VSKeyBindings failed probes `e108526cbd728454c175c76bffc610d4e074da49`, `fcc65187d79c4b546883875da3597345db1e01cd`, `e9a3efd58acb2af9539628eb2875e6cb829c3cec`, `fb3c7e65a4c2089f6fa695114734d14836bde1d3` remain negative evidence.
- Actions self-push of workflow changes without `workflows` permission is a locked failed transport hypothesis; do not use it as the actual transport step.
- retired `apm23/VS2-Create_Interactive` workarounds remain historical warning evidence only and are forbidden as implementation source.

## Current remaining Java compile frontier

Exact-head artifact `10598698213` at implementation HEAD `9b229bbadfc3bab5ed918556144ad566ca37e448` contains **69 `: error:` diagnostics across 8 normalized source files**:

1. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/vanilla_renderer/MixinLevelRendererVanilla.java` — 24 diagnostics.
2. `common/src/main/java/org/valkyrienskies/mod/mixin/feature/render_ship_debug_bb/MixinDebugRenderer.java` — 9 diagnostics.
3. `common/src/main/java/org/valkyrienskies/mod/mixin/client/renderer/MixinLevelRenderer.java` — 6 diagnostics.
4. `common/src/main/java/org/valkyrienskies/mod/mixin/feature/render_pathfinding/MixinDebugRenderer.java` — 6 diagnostics.
5. `common/src/main/java/org/valkyrienskies/mod/mixin/feature/vs2_alpha_hud/MixinGui.java` — 6 diagnostics.
6. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/sable/MixinActiveSableCompanion.java` — 6 diagnostics.
7. `common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/sable/MixinSubLevelHoldingChunkMap.java` — 6 diagnostics.
8. `common/src/main/java/org/valkyrienskies/mod/mixin/server/world/MixinChunkMapClose.java` — 6 diagnostics.

Classification:

- renderer/debug/HUD units are rendering/camera-adjacent and must not be blind-patched;
- Sable units are optional-compat residue and remain compile-only isolation territory, not runtime authority;
- `MixinChunkMapClose.java` is the only remaining non-render core Java unit in this observed frontier, but it is shutdown/chunk-ticket-work sensitive. Its old `ChunkTaskPriorityQueueSorter`/queue-work assumptions no longer map mechanically to the 26.2 `ChunkMap` task-dispatch structure. Do not rename fields/classes by guesswork.

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
- active_proof_head: `9b229bbadfc3bab5ed918556144ad566ca37e448; canonical P1 chain through frozen LevelChunk serialization boundary`
- active_proof_run: `P0 35490917259 success; P1 compile 35490917263 frontier-only failure; artifact 10598698213; 69 diagnostics / 8 normalized source files; MixinLevelChunk absent`
- active_hypothesis: `next non-render core unit is MixinChunkMapClose shutdown-work API drift, but it is authority-sensitive and requires exact 26.2 ChunkMap task-dispatch/hasWork semantics before any mutation`
- final_ready: `false`
- user_runtime_validation: `NOT_APPLICABLE_YET`
- video_status: `NOT_APPLICABLE_YET`

## Engineering locks

- First-failure classification stays factual: provenance, build/mappings/API/loader/mixin/VSCore-native/networking/storage/transforms/rendering/collision/entity-player-camera/Create/SNR-Copycats/CI/final packaging.
- Make one evidence-backed root/semantic change at a time.
- Standalone real VS2 P1 must initialize before Create integration.
- Every core ported subsystem must remain traceable to upstream VS2 or be documented as a minimal 26.2 compatibility bridge.
- Never replace ship-space/physics/collision/entity-dragging/player-camera systems with a new custom implementation.
- Never use synthetic carry/inertia, fake gravity, manual floor/wall/ceiling clamps, per-tick teleport/setPos chase, camera counter-rotation/forcing, duplicate authority, or floor-only success as final architecture.
- Frozen TicketStorage read bridge is read-only compatibility; it may not be expanded into a replacement ticket lifecycle.
- Frozen real ship-ticket lifecycle remains the add/remove/load authority.
- Frozen renderer submit/state bridge may not be expanded into movement/camera/collision/gameplay authority.
- Frozen authority/interpolation bridge may not be expanded into a custom movement/carry system.
- Frozen Sable proof is compile-only and does not authorize bundling a 1.21.1 Sable runtime on 26.2.
- Frozen Create helper exclusion is P1 compile isolation only, not P3.
- Frozen ShipSavedData proof authorizes only its persistence API bridge and matching server acquisition change.
- Frozen shipyard teleport mapping may not be replaced by manual packet/setPos/teleport-chase authority.
- Frozen clip/LavaFluid/Explosion/StructureTemplate/LevelChunk boundaries may not be expanded into unrelated authority.
- `FINAL_READY` is forbidden from CI alone.
- Video is closure-only and must not be used for ordinary compile/debug hypothesis testing.

## next_safe_action

1. This reconciliation commit is documentation-only. Require exact-head P0 provenance success before another source/workflow mutation.
2. Preserve every frozen boundary and all negative evidence in Git history. Do not repeat any landed patch above.
3. Use exact-head compile artifact `10598698213` as the current canonical **69-diagnostic / 8-source-file** frontier until HEAD/compiler state changes.
4. Inspect only pinned upstream `common/src/main/java/org/valkyrienskies/mod/mixin/server/world/MixinChunkMapClose.java` plus the exact resolved Minecraft 26.2 `ChunkMap.hasWork` / chunk-task-dispatch fields and methods. The mixin is a defense-in-depth shutdown guard; the primary real VS2 ticket cleanup remains `MixinMinecraftServer.preStopServer()` and must remain authoritative.
5. Do **not** mutate `MixinChunkMapClose` unless the current 26.2 structure proves a bounded compatibility bridge that preserves the original intent without inventing ticket/work authority. If exact semantics are not established, HOLD.
6. Do not combine that inspection with renderer, HUD, camera, Sable, Create/Copycat, movement, collision, teleport, or reference-space changes.
7. Remain standalone P1. Do not use optional compatibility exclusions to hide core real-VS2 failures.
8. Do not record ordinary compile/debug video.

## Video and milestone gate

- `M1_COMPLETE` is forbidden until full P2 real-VS2 runtime proof exists: real ship lifecycle, translation+rotation, ship-space, collision, standing/walking, jump-airborne-natural landing, floor/walls/ceiling, free stable camera/look, entity dragging/reference space, rendering, and client/server sync.
- `FINAL_BUILD`, `FINAL_VERIFY`, and `FINAL_READY` are not applicable during P1.
