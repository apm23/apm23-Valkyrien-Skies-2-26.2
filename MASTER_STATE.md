# MASTER_STATE — REAL VS2 26.2 PORT

GitHub code is the implementation source of truth. This file is the durable continuity ledger; chat memory is not authoritative.

## Project identity

- Repository: `apm23/apm23-Valkyrien-Skies-2-26.2`
- Mission: port the **actual original Valkyrien Skies 2 source** to Minecraft Java/Fabric 26.2, then integrate Create Fly / Steam 'n' Rails / Copycats on top of real VS2.
- Hard contract: **VS2 ASLI. BUKAN SYSTEM MIRIP VS2.**
- Architecture contract: `PORT_CONTRACT.md`
- Exact dependency/environment lock: `BASELINE_LOCK.json`
- Upstream provenance: `UPSTREAM_PROVENANCE.md`

## Current reconciliation — 2026-09-18 watchdog continue

- Actual repository HEAD at this watchdog start: `73eb0d2c7ed8cef881acd253aadb54eddfd89eb0`.
- P0 import/provenance remains frozen green from source HEAD `04b3228435ea14bc34de0646363a985cf6b2ba59`, Actions run `35304871880` success.
- P1 first standalone compile probe ran against exact HEAD `6de134088ec6c0453d0572a2a8e7335b9d8a96d4` as Actions run `35305188689`.
- P1 first probe job `105475830280` failed before source compilation on removed Gradle 9 `archivesBaseName`; that blocker was fixed at HEAD `66b34d601fd3e7d303c798bc369243b63d781f01`.
- P1 second probe run `35305340412`, job `105476272906`, completed `failure`, but advanced past the archive-name blocker.
- Direct second blocker: regular Architectury Loom `1.17.493` requires a populated `mappings` configuration (`Configuration 'mappings' has no dependencies`) after the 26.2 overlay intentionally removed Mojang mappings.
- The no-remap adaptation landed at HEAD `01f91ddda5578d680aba3f29827775b517203828` and triggered run `35305492616`.
- Run `35305492616`, job `105476728867`, failed in the overlay application before Gradle configuration because the strict `remapJar` matcher omitted the upstream inline duplicates-strategy comment; this was fixed at HEAD `73eb0d2c7ed8cef881acd253aadb54eddfd89eb0`.
- P1 proof run `35305553848`, job `105476906233`, then applied the full no-remap overlay successfully, passed delta validation and Gradle startup, and failed during project evaluation at `common/build.gradle:7` because `loom-no-remap` does not create `modImplementation` (`Could not find method modImplementation()`).
- This is a build dependency-configuration migration blocker; no VS2 Java/Kotlin source compilation has started yet.
- No code from `apm23/VS2-Create_Interactive` has been imported.

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

P0 proof: run `35304871880`, conclusion `success`, source HEAD `04b3228435ea14bc34de0646363a985cf6b2ba59`.

No Create/SNR/Copycats integration is part of P0.

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

- project_state: `P1_BUILD_TOOLING_ADAPTATION_IN_PROGRESS`
- active_blocker: `LOOM_NO_REMAP_OMITS_MOD_DEPENDENCY_CONFIGURATIONS`
- active_hypothesis: `Translate only active modImplementation/modApi/modCompileOnly dependency configuration names to implementation/api/compileOnly while preserving exact dependency coordinates and VS2 source`
- final_ready: `false`
- user_runtime_validation: `NOT_APPLICABLE_YET`

## P1 build-port evidence

First P1 probe (`35305188689`) established:
- exact upstream submodule pin checkout succeeds;
- Java `25.0.4+1` setup succeeds;
- Gradle `9.5.1` starts successfully;
- Architect Plugin `3.5.170` and Architectury Loom `1.17.493` configure far enough to evaluate the root build;
- target metadata overlay for Minecraft `26.2`, Fabric Loader `0.19.3`, Fabric API `0.160.0+26.2`, Java 25 and Fabric-only platform is applied cleanly;
- first failure is the removed Gradle 9 `archivesBaseName` convention, before VS2 Java/Kotlin compilation.

Second P1 probe (`35305340412`) proved the Gradle-9 archive-name adaptation works and advanced configuration to Loom setup. It then failed because regular `dev.architectury.loom` requires a mappings dependency even though Minecraft 26.x is unobfuscated. Architectury's 26.1+ guidance uses `dev.architectury.loom-no-remap`, removes the mappings dependency, and removes `remapJar`. After correcting the fail-closed `remapJar` matcher, run `35305553848` proved the no-remap overlay itself applies and Gradle advances into common-project dependency evaluation. The next direct blocker is that no-remap omits Loom's `mod*` dependency configurations; 26.x builds use the plain Gradle equivalents because no remapping stage exists.

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
Frozen green at source HEAD `04b3228435ea14bc34de0646363a985cf6b2ba59`, Actions run `35304871880` success. Exact upstream gitlink, tree and license identity proven.

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

- `P0_UPSTREAM_IMPORT_PROVENANCE`: source HEAD `04b3228435ea14bc34de0646363a985cf6b2ba59`; run `35304871880`; exact upstream commit/tree/LICENSE identity verified.

## Unproven

- 26.2 compile
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
- Create bridge
- SNR
- Copycats
- final artifact

## Failed hypotheses / forbidden reintroductions

Do not reintroduce without new direct evidence:
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

1. Keep P0 and the exact upstream submodule pin frozen unchanged.
2. Translate only active no-remap-incompatible dependency configuration names in pinned upstream `common/build.gradle` and `fabric/build.gradle`: `modImplementation -> implementation`, `modApi -> api`, and `modCompileOnly -> compileOnly`; preserve dependency coordinates, scopes, include structure, and all VS2 source.
3. Run the same standalone common + Fabric compile proof.
4. If the proof advances, classify the next direct blocker from the new log before changing anything else.
5. Continue P1 only through evidence-backed Minecraft/Fabric/build/API port changes; do not add Create/SNR/Copycats.
6. Update this ledger with exact resulting HEAD/run/blocker after the next proof-changing result.

## Final gate

`FINAL_READY` is forbidden until:
- exact final source/build is verified;
- exact final JAR SHA-256 is recorded;
- the user tests that exact JAR in the real Minecraft setup and accepts runtime behavior.

CI alone cannot satisfy this gate.
