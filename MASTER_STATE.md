# MASTER_STATE — REAL VS2 26.2 PORT

GitHub code is the implementation source of truth. This file is the durable continuity ledger; chat memory is not authoritative.

## Project identity

- Repository: `apm23/apm23-Valkyrien-Skies-2-26.2`
- Mission: port the **actual original Valkyrien Skies 2 source** to Minecraft Java/Fabric 26.2, then integrate Create Fly / Steam 'n' Rails / Copycats on top of real VS2.
- Hard contract: **VS2 ASLI. BUKAN SYSTEM MIRIP VS2.**
- Architecture contract: `PORT_CONTRACT.md`
- Exact dependency/environment lock: `BASELINE_LOCK.json`
- Upstream provenance: `UPSTREAM_PROVENANCE.md`

## Current reconciliation — 2026-09-18 watchdog timeout recovery

- Actual source-port HEAD reconciled at watchdog start: `b38ff3f36b3c5ad831cbfee6999423f0df08a038` (`P1: port first 26.2 Identifier API cluster`).
- Previous P1 run `35322680307`, job `105528498940`, completed `failure` at that exact HEAD **after reaching real `:common:compileKotlin` source compilation**. Build/toolchain setup, Java 25, no-remap Loom setup, dependency resolution, and the first source overlay all completed before compiler errors.
- The compiler proved the first source overlay worked and exposed a broad Minecraft-26.2 source-API migration surface. It also proved the old ledger statement that no VS2 source imports Sable was false: pinned upstream `common/src/main/kotlin/org/valkyrienskies/mod/compat/SableCompat.kt` imports and uses Sable companion APIs for real VS2 entity-dragging state.
- Official upstream branch `1.21.1/main` still contains `SableCompat.kt` and still declares a Sable common dependency (with newer coordinates/API). Therefore Sable is a real upstream compatibility dependency/API gap, not dead code that may be discarded from final architecture.
- The earlier build overlay currently omits the unavailable pinned Sable artifact only to let the standalone compile probe reach source compilation. That omission is **temporary compile-probe scaffolding**, not an accepted final removal of Sable/entity-dragging behavior.
- Smallest compiler-proven next source adaptation landed at source-port HEAD `7043d6dc2916ce86268ad2501bfc6d24cf781daf`: the exact four `ResourceLocation` references in upstream `BlockStateInfoProvider.kt` are adapted to Minecraft 26.2 `Identifier`. No VS2 registry/block-state/physics semantics were changed.
- P0 provenance at source-port HEAD `7043d6dc2916ce86268ad2501bfc6d24cf781daf`: run `35324164899` completed `success`.
- P1 compile proof for source-port HEAD `7043d6dc2916ce86268ad2501bfc6d24cf781daf`: run `35324164902`, job `105533249735`, is in progress at the time of this ledger update. It has already passed checkout, Java 25 setup, build overlay, 26.2 source overlay, delta validation, and Gradle runtime; it is currently executing the standalone common + Fabric compile step.
- No code from `apm23/VS2-Create_Interactive` has been imported. The retired workaround project remains forbidden as an implementation source.

## Official upstream baseline

- repository: `ValkyrienSkies/Valkyrien-Skies-2`
- branch used to select baseline: `1.21.1/main`
- exact commit: `f39132148e717d325933b4ce6e9e9fb13d929390`
- exact upstream root tree: `91116399605d3ecd1c93b0011560e09281ee1fa4`
- upstream mod version: `2.4.12`
- upstream `LICENSE` blob: `0a041280bd00a9d068f503b8ee7ce35214bd24a1`

## P0 import implementation

The exact official source baseline is imported as the Git submodule/gitlink `upstream-vs2/` pinned directly to `f39132148e717d325933b4ce6e9e9fb13d929390`.

This is intentional: the baseline remains byte-for-byte upstream source instead of being reconstructed through the connector. Minecraft 26.2 adaptations are explicit, reviewable port changes layered on that exact baseline. `.github/workflows/p0-provenance.yml` verifies the gitlink commit, checked-out submodule HEAD, root tree, upstream LICENSE blob, and clean checkout.

P0 original frozen proof: run `35304871880`, conclusion `success`, source HEAD `04b3228435ea14bc34de0646363a985cf6b2ba59`.
Latest P0 confirmation for current source-port patch: run `35324164899`, conclusion `success`, source-port HEAD `7043d6dc2916ce86268ad2501bfc6d24cf781daf`.

No Create/SNR/Copycats integration is part of P0/P1.

## Target runtime baseline

- Minecraft `26.2`
- Java `25`
- Fabric Loader `0.19.3`
- Fabric API `0.160.0+26.2`
- Create Fly `6.0.9-1`
- Steam 'n' Rails embedded version `SNR.FLY-STABLE-1.2.2+fabric-mc26.2`
- Copycats embedded version `3.0.7-createfly+mc.26.2-v1.14`
- Dependency bytes are locked by SHA-256 in `BASELINE_LOCK.json`. Filenames are not authoritative when they disagree with embedded metadata.

## Project state

- project_state: `P1_SOURCE_API_ADAPTATION_IN_PROGRESS`
- active_blocker: `MINECRAFT_26_2_SOURCE_API_DRIFT`
- active_hypothesis: `Continue only compiler-proven, traceable Minecraft/Fabric 26.2 API adaptations in small clusters; preserve real upstream VS2 subsystem semantics. Resolve Sable with a traceable compatibility path rather than deleting VS2 entity-dragging behavior.`
- active_proof_head: `7043d6dc2916ce86268ad2501bfc6d24cf781daf`
- active_proof_run: `35324164902`
- final_ready: `false`
- user_runtime_validation: `NOT_APPLICABLE_YET`

## P1 build-port evidence

Early P1 probes established and preserved:
- exact upstream submodule checkout succeeds;
- Java 25 and Gradle 9.5.1 start correctly;
- Gradle-9 `archivesBaseName` removal was adapted;
- Minecraft 26.x uses `dev.architectury.loom-no-remap` with no mappings/remapJar path;
- dependency configurations were migrated away from `modImplementation`/`modApi`/`modCompileOnly` under no-remap Loom;
- common/Fabric dependency selection was adapted far enough to enter source compilation.

Important run history:
- `35305188689`: first P1 probe; stopped on removed Gradle 9 `archivesBaseName`.
- `35305340412`: advanced to Loom mappings blocker.
- `35305492616`: exposed strict overlay matcher issue.
- `35305553848`: no-remap overlay applied; exposed missing `modImplementation` under no-remap Loom.
- `35306643156`: advanced dependency resolution to Sable artifact issue.
- Subsequent build-overlay work omitted the unavailable pinned Sable artifact for compile probing and advanced to actual source compilation.
- `35322680307` at `b38ff3f36b3c5ad831cbfee6999423f0df08a038`: reached `:common:compileKotlin`, proving the first explicit 26.2 source overlay is active. Compiler errors now primarily reflect Minecraft/Fabric API drift rather than build-system setup.
- `35324164902` at `7043d6dc2916ce86268ad2501bfc6d24cf781daf`: active proof after adding the compiler-proven `BlockStateInfoProvider.kt` `ResourceLocation -> Identifier` cluster; run still in progress when this ledger entry was written.

Representative compiler-proven source migration areas from `35322680307` include:
- additional `ResourceLocation -> Identifier` and related registry/key API renames;
- block/direction/position/build-height API changes;
- saved-data / NBT / `ValueInput` / `ValueOutput` changes;
- command permission API changes;
- resource reload listener generics;
- renderer/render-state changes;
- entity save/hurt/networking/data-tracker changes;
- ticket/tick/processor API changes;
- Create-compat source references that must remain isolated until standalone VS2 P1 is proven;
- Sable API/dependency incompatibility in upstream `SableCompat.kt`.

These compiler errors authorize only narrow, source-traceable port adaptations. They do not authorize replacing VS2 architecture.

## Mandatory architecture

This repository is a version port of real VS2. Porting Minecraft/Fabric APIs is allowed. Replacing VS2 internals with a new home-grown system that only imitates VS2 behavior is forbidden.

Core final behavior must remain based on actual upstream VS2 machinery for:
- ship lifecycle / ship-space;
- transforms;
- physics-core integration;
- collision integration;
- entity/reference-frame behavior;
- player/body/camera integration;
- networking / synchronization;
- rendering.

The previous project's custom carry/reference-frame chains, floor fixes, camera corrections, manual clamps, synthetic velocity, per-tick teleport/reanchor logic, and workaround history are not an implementation source.

## Milestones

### P0 — Upstream import + provenance
Frozen green at source HEAD `04b3228435ea14bc34de0646363a985cf6b2ba59`, Actions run `35304871880` success. Exact upstream commit/tree/license identity proven. Current source-port patch also reconfirmed by P0 run `35324164899` success.

### P1 — Standalone VS2 26.2 boot
Port real VS2 to 26.2 until client/server boot and core/native initialization work without Create/SNR/Copycats hiding failures.

### P2 / M1 — Standalone real VS2 ship runtime
Prove on 26.2 using a real VS2 ship:
- actual VS2 ship creation/lifecycle;
- ship transform translation + rotation;
- player standing and walking;
- jump -> airborne -> natural landing while staying in the ship frame;
- solid floor/walls/ceiling;
- free stable mouse look/camera;
- entity dragging/reference-frame behavior;
- client/server synchronization;
- no fake carry, no per-tick teleport chase.

Only after all of this may `M1_COMPLETE` be emitted.

### P3 — Create Fly bridge
Only after standalone VS2 is frozen green. Initial architecture target:
- one Create carriage = one real VS2 ship/reference space;
- Create owns track graph, bogey, station, schedule, speed and desired carriage trajectory;
- VS2 owns the moving ship/reference-space semantics;
- do not fake a VS2 ship with a matrix/helper object.

### P4 — Steam 'n' Rails + Copycats
Integrate exact locked dependencies after the Create bridge works.

### P5 — Production/final
Full target stack, final exact JAR, final verification, then exact-JAR real-user runtime acceptance.

## Frozen green

- `P0_UPSTREAM_IMPORT_PROVENANCE`: original frozen source HEAD `04b3228435ea14bc34de0646363a985cf6b2ba59`; run `35304871880`; exact upstream commit/tree/LICENSE identity verified.
- Current P0 reconfirmation: source-port HEAD `7043d6dc2916ce86268ad2501bfc6d24cf781daf`; run `35324164899`; success.

## Unproven

- 26.2 full compile
- standalone client/server boot
- VSCore/Krunch/native chain
- ship lifecycle
- ship transforms
- physics
- rendering
- networking
- collision
- player/body/camera
- entity dragging
- Sable compatibility on 26.2
- Create bridge
- SNR
- Copycats
- final artifact

## Failed hypotheses / forbidden reintroductions

Do not reintroduce without new direct evidence:
- **FALSE HYPOTHESIS RETIRED:** `no VS2 source imports Sable`. Compiler evidence and upstream source inspection prove `SableCompat.kt` imports/uses Sable for real entity-dragging state. Never use that false premise to delete the subsystem.
- treating temporary omission of the unavailable pinned Sable artifact as final architecture; a traceable 26.2 Sable compatibility solution is still required before entity-dragging can be considered ported;
- Gradle 9 with the removed legacy `archivesBaseName` convention property;
- regular `dev.architectury.loom` on Minecraft 26.x with the mappings dependency removed;
- `modImplementation`/`modApi`/`modCompileOnly` configurations under `dev.architectury.loom-no-remap`;
- custom "VS2-style" reference-frame system as a substitute for VS2;
- grounded floor carry as proof of real ship-space correctness;
- per-tick player teleport/setPos chase;
- synthetic carry velocity/inertia;
- fake gravity;
- manual floor/wall/ceiling clamps;
- camera forcing/counter-rotation;
- duplicate Create/custom/VS2 ownership;
- old `VS2-Create_Interactive` gameplay patches as a starting architecture;
- fixture/input mutations whose purpose is only to manufacture green.

## Direct user-runtime evidence from retired project

Historical warning only, not implementation source:
- exact previous candidate had floor/grounded behavior working;
- jump teleported/failed badly;
- camera was dragged on turns;
- walls were penetrable;
- turns could throw the player out of the train.

This proves that floor-only automated green is insufficient. It does NOT authorize copying or patching the retired project here.

## next_safe_action

1. Treat source-port HEAD `7043d6dc2916ce86268ad2501bfc6d24cf781daf` and P1 run `35324164902` as the active proof pair; do not patch again while that workflow is still active.
2. When run `35324164902` completes, inspect its exact compile log and classify the next direct compiler blocker/cluster.
3. If the `BlockStateInfoProvider.kt` Identifier cluster is gone, preserve it and choose only the smallest next compiler-proven API adaptation. If it regressed, repair only that direct regression.
4. Do not alter Sable/entity-dragging semantics merely to make compilation green. Resolve Sable as a separate traceable compatibility gap based on upstream architecture/API evidence.
5. Continue P1 standalone only. Do not add Create/SNR/Copycats until real standalone VS2 26.2 boot/core initialization is proven.
6. Update this ledger with the exact run conclusion, next blocker, resulting HEAD, and next safe action after the proof result lands.

## Video validation state

- No video is authorized or needed during compile/API-port debugging.
- Video is closure-only after a user-visible runtime blocker is already closure-ready from data/runtime proof.

## Final gate

`FINAL_READY` is forbidden until:
- exact final source/build is verified;
- exact final JAR SHA-256 is recorded;
- the user tests that exact JAR in the real Minecraft setup and accepts runtime behavior.

CI alone cannot satisfy this gate.
