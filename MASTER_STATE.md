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

- Actual repository HEAD before this ledger-only update: `d801971fd7e26f7f5335a301e48069ed1462d641` (`watchdog: sync EntityData active proof state`). This is ledger-only; latest implementation/source-port HEAD remains `166c39f21d7ce5703e20a9cc73a53f952f737c65` (`P1: port entity data non-null bounds`).
- Prior implementation HEAD `a2951cab7d0a5b32756b45dc361a040d7212cdea` remains proven clean for its targeted `VSEntityManager.kt` cluster by P1 run `35325476529`.
- P1 at exact implementation HEAD `166c39f21d7ce5703e20a9cc73a53f952f737c65`: run `35327172496`, job `105542829942`, completed `failure` at `:common:compileKotlin` after checkout, Java 25, both overlays, diff validation, and Gradle startup succeeded.
- Run `35327172496` proves the `EntityData.kt` non-null-bound adaptation worked: `EntityData.kt` no longer appears anywhere in compiler errors.
- Diagnostic artifact for run `35327172496`: `p1-compile-log-166c39f21d7ce5703e20a9cc73a53f952f737c65`, artifact ID `10539941266`, uploaded ZIP SHA-256 `6576ec914a83786a70850b346c0153eee1efa80e8463a7f9b9e5164d2f2c847b`.
- P0 at `166c39f21d7ce5703e20a9cc73a53f952f737c65`: run `35327172660` completed `success`.
- The next smallest direct compiler-proven standalone cluster is `common/src/main/kotlin/org/valkyrienskies/mod/util/NbtUtil.kt`: all seven errors are Minecraft 26.2 `CompoundTag.getDouble()` now returning `Optional<Double>` instead of primitive `Double`. Both pinned upstream and current `1.21.1/main` are identical. The source already checks `contains(...)` for every key before reading, so adapting the seven reads with `.orElse(0.0)` preserves the old primitive/default semantics without altering VS2 vector/quaternion serialization logic.
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
- active_proof_head: `166c39f21d7ce5703e20a9cc73a53f952f737c65`
- active_proof_run: `35327172496` (`completed/failure`; EntityData cluster proven clean)
- active_hypothesis: `Adapt only NbtUtil.kt getDouble Optional return values with explicit old-default semantics; do not change serialization or VS2 behavior.`
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
- `EntityData.kt` non-null generic bounds.

Next candidate:
- `NbtUtil.kt` seven `Optional<Double>` return adaptations preserving old `Double` default semantics.

Representative remaining compiler areas include renderer/render-state APIs, direction/position/build-height changes, SavedData/NBT `ValueInput`/`ValueOutput`, command permissions, resource reload listener generics, entity save/hurt/network APIs, tickets/ticks/structure processors, Create-compat classpath/API drift, and Sable compatibility.

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
Frozen green. Original proof run `35304871880`; later confirmations include `35324164899`, `35324792335`, `35325575601`, and `35327172660`.

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

1. Preserve implementation HEAD `166c39f21d7ce5703e20a9cc73a53f952f737c65`; run `35327172496` proves its `EntityData.kt` cluster clean.
2. Apply the smallest next source adaptation only in `NbtUtil.kt`: unwrap the seven Minecraft 26.2 `Optional<Double>` values with `.orElse(0.0)`, preserving the old primitive/default behavior and existing `contains(...)` guards.
3. Include `NbtUtil.kt` in P1 workflow delta display, commit atomically, and let the resulting P1 run prove whether that file disappears from compiler errors.
4. Do not stack another source patch while that new P1 workflow is active.
5. Do not alter renderer, Sable/entity-dragging, physics, collision, networking, player/camera, or Create semantics merely to remove unrelated compiler errors; each needs its own evidence-backed adaptation.
6. Stay in standalone P1. Do not integrate Create/SNR/Copycats yet.
7. Update this ledger with the new implementation HEAD/run after the patch lands.

## Video validation

No video is authorized during compile/API-port debugging. Video is closure-only for a user-visible runtime blocker that is already closure-ready from runtime/data proof.

## Final gate

`FINAL_READY` is forbidden until the exact final source/build and JAR SHA-256 are recorded and the user tests and accepts that exact JAR in the real Minecraft setup. CI alone cannot satisfy the final gate.
