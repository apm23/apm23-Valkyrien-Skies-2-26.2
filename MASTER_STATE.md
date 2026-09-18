# MASTER_STATE — REAL VS2 26.2 PORT

GitHub code is the implementation source of truth. This file is the durable continuity ledger; chat memory is not authoritative.

## Project identity

- Repository: `apm23/apm23-Valkyrien-Skies-2-26.2`
- Mission: port the **actual original Valkyrien Skies 2 source** to Minecraft Java/Fabric 26.2, then integrate Create Fly / Steam 'n' Rails / Copycats on top of real VS2.
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

The upstream baseline remains byte-for-byte pinned. Minecraft 26.2 changes are applied by explicit fail-closed overlay scripts so every adaptation stays traceable to upstream VS2 source.

## Current reconciliation — 2026-09-18

- Actual repository HEAD before this ledger-only update: `71245da2d1fa83f76859c4ed722518dd8a524f05` (`watchdog: sync TestFlapBlock proof state`).
- Current implementation/source-port HEAD remains `c8128c30bb29d9c454bf0045b873dea3bc76a17c` (`P1: port TestFlapBlock Direction accessor`).
- Prior implementation HEAD `d0a33c0c7ff2ca49db1a69420c0b51d0064a92dc` is proven clean for its targeted `ValkyrienSkies.kt` accessor cluster by P1 run `35331485313`, job `105556599506`.
- Diagnostic artifact for run `35331485313`: `p1-compile-log-d0a33c0c7ff2ca49db1a69420c0b51d0064a92dc`, artifact ID `10541221766`, ZIP SHA-256 `2a1d8ef765e1770e8f67970d66253ad337470a012e7ed45450b2a0b4a8be9b47`.
- HEAD `c8128c30bb29d9c454bf0045b873dea3bc76a17c` adds one fail-closed source adaptation in `common/src/main/kotlin/org/valkyrienskies/mod/common/block/TestFlapBlock.kt`: `blockState.getValue(FACING).normal.toJOMLD()` -> `blockState.getValue(FACING).getUnitVec3i().toJOMLD()`, plus that file's P1 workflow diff-display path.
- Pinned upstream `f39132148e717d325933b4ce6e9e9fb13d929390` and current upstream `1.21.1/main` are byte-identical for `TestFlapBlock.kt` at blob `03f9db336c337fb1d531e00ebad81ed61db1f4b1`; Wing construction, coefficients, and `toJOMLD()` conversion are otherwise unchanged.
- Exact-head P0 run `35333733917` completed `success` for `c8128c30bb29d9c454bf0045b873dea3bc76a17c`.
- Exact-head P1 run `35333733932`, job `105563689862`, completed `failure` only because later independent Minecraft 26.2 API errors remain. The exact targeted `TestFlapBlock.kt` error is absent from the final compiler error set, so the accessor adaptation is proven clean.
- Diagnostic artifact for run `35333733932`: `p1-compile-log-c8128c30bb29d9c454bf0045b873dea3bc76a17c`, artifact ID `10542133841`, ZIP SHA-256 `053cc414fab9522a53e0ba055a604d432359b06ade6e3c86fdd3cdd7286ade7b`.
- Representative remaining direct private `Direction.normal` errors include standalone VS2 callsites in `TestWingBlock.kt`, `TestThrusterBlockEntity.kt`, `TestChairBlock.kt`, and `EntityDragger.kt`, plus a Create-compat callsite that is intentionally not the next target during standalone P1.
- No code from `apm23/VS2-Create_Interactive` has been imported. The retired workaround project remains forbidden as implementation source.

## Target runtime baseline

- Minecraft `26.2`
- Java `25`
- Fabric Loader `0.19.3`
- Fabric API `0.160.0+26.2`
- Create Fly `6.0.9-1`
- Steam 'n' Rails embedded version `SNR.FLY-STABLE-1.2.2+fabric-mc26.2`
- Copycats embedded version `3.0.7-createfly+mc.26.2-v1.14`
- Exact dependency bytes are locked by SHA-256 in `BASELINE_LOCK.json`.

## Project state

- project_state: `P1_SOURCE_API_ADAPTATION_IN_PROGRESS`
- active_blocker: `MINECRAFT_26_2_SOURCE_API_DRIFT`
- active_proof_head: `none; previous proof c8128c30bb29d9c454bf0045b873dea3bc76a17c landed`
- active_proof_run: `none; previous P1 run 35333733932 landed`
- active_hypothesis: `Select the next smallest direct compiler-proven standalone VS2 API callsite without touching Create compat or runtime semantics.`
- final_ready: `false`
- user_runtime_validation: `NOT_APPLICABLE_YET`

## Proven P1 progress

Build/toolchain work already established:
- Java 25 + Gradle 9.5.1 starts;
- Minecraft 26.x build uses `dev.architectury.loom-no-remap` without Mojang mappings/remapJar;
- Gradle 9 `archivesBaseName` removal adapted;
- old `modImplementation` / `modApi` / `modCompileOnly` configurations migrated for no-remap Loom;
- dependency resolution advances into real `:common:compileKotlin`;
- explicit source overlay is active and fail-closed.

Source API clusters proven clean in successive runs:
- data-provider `ResourceLocation -> Identifier` plus registry-holder `location() -> identifier()`;
- `BlockStateInfoProvider.kt` Identifier cluster;
- `SimpleSoundInstanceOnShip.kt` Identifier cluster;
- `VSEntityManager.kt` Identifier cluster;
- `EntityData.kt` non-null generic bounds;
- `NbtUtil.kt` guarded `Optional<Double>` reads;
- `VectorConversionsMC.kt` public Direction unit-vector accessor;
- `ValkyrienSkies.kt` public Direction unit-vector accessor;
- `TestFlapBlock.kt` public Direction unit-vector accessor.

Representative remaining compiler areas include Create compat classpath/API drift, other Direction/position/build-height changes, renderer/render-state APIs, SavedData/NBT `ValueInput`/`ValueOutput`, command permissions, resource reload listener generics, entity save/hurt/network APIs, tickets/ticks/structure processors, and Sable compatibility.

## Sable contract

A previous hypothesis that no VS2 source imported Sable was disproven by compiler output and upstream source inspection. `common/src/main/kotlin/org/valkyrienskies/mod/compat/SableCompat.kt` is real upstream VS2 code and uses Sable companion state for entity-dragging/reference behavior.

Official upstream `1.21.1/main` still carries Sable compat with newer coordinates/API. The current build overlay's omission of the unavailable pinned artifact is **temporary compile-probe scaffolding only**. Final architecture must resolve Sable through a traceable compatible dependency/API path or an explicitly documented minimal compatibility shim into existing VS2 architecture. Deleting/replacing VS2 entity-dragging semantics is forbidden.

## Mandatory architecture

Final behavior must remain based on real upstream VS2 machinery for:
- ship lifecycle / ship-space;
- transforms;
- physics-core integration;
- collision integration;
- entity dragging/reference-frame behavior;
- player/body/camera integration;
- networking/synchronization;
- rendering.

Forbidden final substitutes include custom VS2-style reference frames, synthetic carry velocity/inertia, fake gravity, manual floor/wall/ceiling clamps, per-tick teleport/setPos chase, camera counter-rotation/forcing, duplicate authority, floor-only success, and the retired `VS2-Create_Interactive` workaround chain.

## Milestones

### P0 — Upstream import + provenance
Frozen green. Original proof run `35304871880`; later confirmations include `35324164899`, `35324792335`, `35325575601`, `35327172660`, `35327644515`, `35327819629`, `35329592607`, `35331485247`, and exact current implementation confirmation `35333733917`.

### P1 — Standalone VS2 26.2 compile/boot
Port actual VS2 until common/Fabric compile, standalone client/server boot, and core/native initialization are proven without Create/SNR/Copycats hiding failures.

### P2 / M1 — Standalone real VS2 runtime
Must prove a real VS2 ship: lifecycle, translation/rotation, standing/walking, jump-airborne-natural landing, solid floor/walls/ceiling, stable free camera, entity dragging/reference frame, client/server sync, and no fake carry/teleport chase.

### P3 — Create Fly bridge
Only after standalone VS2 is frozen green. Create owns railway gameplay/trajectory; VS2 owns the real moving ship/reference-space semantics.

### P4 — SNR + Copycats
Only after Create bridge is proven.

### P5 — Production/final
Exact final build, final verification, and exact-JAR real-user acceptance.

## Failed hypotheses / forbidden reintroductions

Do not reintroduce without new direct evidence:
- `no VS2 source imports Sable` — FALSE;
- treating temporary Sable dependency omission as final architecture;
- regular `dev.architectury.loom` + mappings on Minecraft 26.x;
- old Gradle `archivesBaseName`;
- `modImplementation` / `modApi` / `modCompileOnly` under no-remap Loom;
- custom imitation ship/reference-frame implementation;
- grounded-floor behavior as sufficient runtime proof;
- synthetic carry/inertia/gravity;
- manual collision clamps;
- camera forcing;
- per-tick teleport/reanchor;
- retired project gameplay patches;
- fixture/input mutations solely to manufacture green.

## next_safe_action

1. Preserve implementation HEAD `c8128c30bb29d9c454bf0045b873dea3bc76a17c` and P1 run `35333733932` as proven clean for `TestFlapBlock.kt`.
2. Inspect the exact pinned and current-upstream source for `common/src/main/kotlin/org/valkyrienskies/mod/common/block/TestWingBlock.kt`, which run `35333733932` reports with a single direct private `Direction.normal` error.
3. If pinned/current source identity and local semantics confirm the same already-proven public unit-vector accessor migration, add exactly one fail-closed `Direction.normal -> Direction.getUnitVec3i()` adaptation for that callsite and its workflow diff-display path.
4. Trigger the smallest exact-head P0/P1 proof. If the run is active, do not stack another source patch.
5. Do not alter Create compat, renderer, Sable/entity-dragging, physics, collision, networking, player/camera, or unrelated semantics merely to remove compiler errors; each needs its own evidence-backed adaptation.
6. Stay in standalone P1. Do not integrate Create/SNR/Copycats yet.
7. Update this ledger after the next proof lands before any subsequent source patch.

## Video validation

No video is authorized during compile/API-port debugging. Video is closure-only for a user-visible runtime blocker that is already closure-ready from runtime/data proof.

## Final gate

`FINAL_READY` is forbidden until the exact final source/build and JAR SHA-256 are recorded and the user tests and accepts that exact JAR in the real Minecraft setup. CI alone cannot satisfy the final gate.
