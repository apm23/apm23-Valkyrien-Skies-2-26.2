# MASTER_STATE — REAL VS2 26.2 PORT

GitHub code is the implementation source of truth. This file is the durable continuity ledger; chat memory is not authoritative.

## Project identity

- Repository: `apm23/apm23-Valkyrien-Skies-2-26.2`
- Mission: port the **actual original Valkyrien Skies 2 source** to Minecraft Java/Fabric 26.2, then integrate Create Fly / Steam 'n' Rails / Copycats on top of real VS2.
- Hard contract: **VS2 ASLI. BUKAN SYSTEM MIRIP VS2.**
- Architecture contract: `PORT_CONTRACT.md`
- Exact dependency/environment lock: `BASELINE_LOCK.json`
- Upstream provenance: `UPSTREAM_PROVENANCE.md`

## Current reconciliation — 2026-09-18 watchdog resume

- Actual repository HEAD at watchdog start: `1e90c3aa93240092a1c1a3f3dd8b0c9afb7afc89`.
- No GitHub Actions runs existed at restart reconciliation time.
- P0 import/provenance landed at `04b3228435ea14bc34de0646363a985cf6b2ba59`.
- P0 provenance Actions run `35304871880` completed `success` against that exact HEAD.
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

This is intentional: the baseline remains byte-for-byte upstream source instead of being reconstructed through the connector. Minecraft 26.2 adaptations must be explicit, reviewable port changes layered on that exact baseline. `.github/workflows/p0-provenance.yml` verifies the gitlink commit, checked-out submodule HEAD, root tree, upstream LICENSE blob, and clean checkout.

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

- project_state: `P1_BUILD_BASELINE_PENDING`
- active_blocker: `FIRST_26_2_STANDALONE_COMPILE_SIGNAL_NOT_YET_RUN`
- active_hypothesis: `Minecraft 26.2 requires a Java-25/no-remap build path; begin with the smallest traceable build-only adaptation before touching VS2 gameplay code`
- final_ready: `false`
- user_runtime_validation: `NOT_APPLICABLE_YET`

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
- actual ship creation/lifecycle;
- ship transform translation + rotation;
- player standing/walking;
- jump -> airborne -> natural landing in ship frame;
- solid floor/walls/ceiling;
- free stable camera/mouse look;
- entity dragging/reference-space behavior;
- client/server sync;
- no fake carry or per-tick teleport chase.

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

- 26.2 build
- standalone boot
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

1. Keep the exact upstream submodule pin unchanged and treat P0 as frozen green.
2. Add the smallest deterministic, reviewable P1 build-port overlay for Minecraft `26.2`, Java `25`, Fabric Loader `0.19.3`, and Fabric API `0.160.0+26.2`.
3. Adapt only build/mapping/loader mechanics required by 26.2 first; do not make gameplay/carry/collision changes to manufacture a compile result.
4. Run the smallest standalone Fabric compile/configuration proof from the real upstream source with the overlay applied.
5. Classify the first direct blocker from that run before making the next patch.
6. Do not add Create/SNR/Copycats integration during P1.
7. Update this ledger with exact resulting HEAD/run/blocker after every proof-changing action.

## Final gate

`FINAL_READY` is forbidden until:
- exact final source/build is verified;
- exact final JAR SHA-256 is recorded;
- the user tests that exact JAR in the real Minecraft setup and accepts runtime behavior.

CI alone cannot satisfy this gate.
