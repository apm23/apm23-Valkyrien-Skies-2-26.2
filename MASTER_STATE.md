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

- Actual repository HEAD before this ledger-only update: `d9b7199337352999381f7713a3ec22325592e87a` (`watchdog: record TestThrusterBlockEntity active proof state`).
- Current implementation/source-port HEAD remains `7485e9503a53b4fd086cbd29087aedbb2dfc5056` (`P1: port TestThrusterBlockEntity Direction accessor`).
- Prior implementation HEAD `555cc6ddc575061a5e5b9d1f771b9d77d0039324` is proven clean for its targeted `TestWingBlock.kt` accessor by P1 run `35334206051`, job `105565187606`.
- Diagnostic artifact for run `35334206051`: `p1-compile-log-555cc6ddc575061a5e5b9d1f771b9d77d0039324`, artifact ID `10542480562`, ZIP SHA-256 `0bea91a95095500948ecad45d630b86a2e5fe1b875509cd869f76e2951c05fbc`.
- HEAD `7485e9503a53b4fd086cbd29087aedbb2dfc5056` adds exactly one fail-closed source adaptation in `common/src/main/kotlin/org/valkyrienskies/mod/common/blockentity/TestThrusterBlockEntity.kt`: `facing.normal.toJOMLD()` -> `facing.getUnitVec3i().toJOMLD()`, plus only that file's P1 workflow diff-display path.
- Pinned upstream `f39132148e717d325933b4ce6e9e9fb13d929390` and current upstream `1.21.1/main` are byte-identical for `TestThrusterBlockEntity.kt` at blob `e1491b05b5b8f91cb8a6ffd1de2fdd3df7554e53`; `applyModelForce`, force magnitude `100000.0`, block-center force position, activity/null guards, and physics-listener semantics are otherwise unchanged.
- Exact-head P0 run `35336506332`, job `105572463059`, completed `success` for implementation HEAD `7485e9503a53b4fd086cbd29087aedbb2dfc5056`.
- Exact-head P1 run `35336506362`, job `105572463018`, completed `failure` only because later independent Minecraft 26.2 API errors remain. `TestThrusterBlockEntity.kt` is absent from the final compiler error set, so the targeted Direction accessor adaptation is proven clean.
- Diagnostic artifact for run `35336506362`: `p1-compile-log-7485e9503a53b4fd086cbd29087aedbb2dfc5056`, artifact ID `10543132608`, ZIP SHA-256 `1e545474aa2bd062156ee09d42524cc1eae741b95aaed6a40a369d2c976a338f`.
- The same compiler log reports exactly one direct standalone error in `common/src/main/kotlin/org/valkyrienskies/mod/common/block/TestThrusterBlock.kt:40`: its old `neighborChanged(..., blockPos2: BlockPos, bl: Boolean)` override no longer matches Minecraft 26.2, whose compiler-reported signature is `neighborChanged(state: BlockState, level: Level, pos: BlockPos, block: Block, orientation: Orientation?, movedByPiston: Boolean)`.
- Pinned upstream and current `1.21.1/main` are byte-identical for `TestThrusterBlock.kt` at blob `d8bd39c9d3c92de942968cfb95bd807f1cfd3f19`. The obsolete `blockPos2` and boolean parameter names are unused by the VS2 method body, so the next candidate can be restricted to the 26.2 override signature/import while preserving all redstone state, block-entity activation, and tick behavior unchanged.
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
- active_proof_head: `none; previous proof 7485e9503a53b4fd086cbd29087aedbb2dfc5056 landed`
- active_proof_run: `none; previous P1 run 35336506362 landed`
- active_hypothesis: `The next smallest compiler-proven standalone VS2 adaptation is the single TestThrusterBlock.neighborChanged Minecraft 26.2 signature migration; its removed BlockPos parameter was unused, so VS2 redstone/thruster semantics can remain unchanged.`
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
- `TestFlapBlock.kt` public Direction unit-vector accessor;
- `TestWingBlock.kt` public Direction unit-vector accessor;
- `TestThrusterBlockEntity.kt` public Direction unit-vector accessor, with upstream force semantics unchanged.

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
Frozen green. Original proof run `35304871880`; later confirmations include `35324164899`, `35324792335`, `35325575601`, `35327172660`, `35327644515`, `35327819629`, `35329592607`, `35331485247`, `35333733917`, `35334205890`, and exact implementation confirmation `35336506332`.

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

1. Preserve implementation HEAD `7485e9503a53b4fd086cbd29087aedbb2dfc5056`, P0 run `35336506332`, and P1 run `35336506362` as proven clean for `TestThrusterBlockEntity.kt`.
2. Preserve diagnostic artifact `p1-compile-log-7485e9503a53b4fd086cbd29087aedbb2dfc5056`, artifact ID `10543132608`, ZIP SHA-256 `1e545474aa2bd062156ee09d42524cc1eae741b95aaed6a40a369d2c976a338f`.
3. Use the confirmed byte-identical pinned/current `TestThrusterBlock.kt` source at blob `d8bd39c9d3c92de942968cfb95bd807f1cfd3f19`.
4. Add exactly one fail-closed 26.2 signature adaptation in that file: import `net.minecraft.world.level.redstone.Orientation` and change the unused final parameters of `neighborChanged` from `blockPos2: BlockPos, bl: Boolean` to `orientation: Orientation?, movedByPiston: Boolean`. Preserve the method body, redstone state transition, block-entity lookup/activation, placement behavior, tick behavior, and all other semantics unchanged.
5. Add only `TestThrusterBlock.kt` to the P1 workflow diff-display path and trigger the smallest exact-head P0/P1 proof. If its P1 run is active, do not stack another source patch.
6. Do not alter Create compat, renderer, Sable/entity-dragging, physics architecture, collision, networking, player/camera, or unrelated semantics merely to remove compiler errors; each needs its own evidence-backed adaptation.
7. Stay in standalone P1. Do not integrate Create/SNR/Copycats yet.
8. Update this ledger after the next proof lands before any subsequent source patch.

## Video validation

No video is authorized during compile/API-port debugging. Video is closure-only for a user-visible runtime blocker that is already closure-ready from runtime/data proof.

## Final gate

`FINAL_READY` is forbidden until the exact final source/build and JAR SHA-256 are recorded and the user tests and accepts that exact JAR in the real Minecraft setup. CI alone cannot satisfy the final gate.
