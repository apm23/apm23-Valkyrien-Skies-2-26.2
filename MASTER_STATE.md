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

- Actual implementation/source-port HEAD before this ledger-only update: `ad922ded33ff46a3028fca1217559a60be54fad6` (`P1: port MinecraftPlayer permission API`).
- Parent ledger commit before that implementation change: `8411671604dd1a30be0a9f4d0c4bfb8e2eb641c8` (`watchdog: record RaycastUtils proof result`).
- Prior implementation HEAD `8c21cb63a80678c92214c980ec40686853fe33d3` is proven clean for both targeted `RaycastUtils.kt` adaptations by P1 run `35338858979`, job `105579924065`.
- Diagnostic artifact for run `35338858979`: `p1-compile-log-8c21cb63a80678c92214c980ec40686853fe33d3`, artifact ID `10544043269`, ZIP SHA-256 `37c742271c1e79c424a93fa326b39692bb7e109cceda885371b50a109123be8a`.
- HEAD `ad922ded33ff46a3028fca1217559a60be54fad6` adds exactly one Minecraft 26.2 permission API import in `common/src/main/kotlin/org/valkyrienskies/mod/common/util/MinecraftPlayer.kt`, `net.minecraft.server.permissions.Permissions`, and replaces exactly both `player.hasPermissions(4)` callsites with `player.permissions().hasPermission(Permissions.COMMANDS_OWNER)`.
- Minecraft 26.2 defines `Permissions.COMMANDS_OWNER` as `Permission.HasCommandLevel(PermissionLevel.OWNERS)`, and `PermissionLevel.OWNERS` has id `4`, so the old VS2 level-4 admin/config threshold is preserved.
- Pinned upstream `f39132148e717d325933b4ce6e9e9fb13d929390` and current upstream `1.21.1/main` are byte-identical for `MinecraftPlayer.kt` at blob `c11d83b71dc7be4144fb9473ac76636f458898a5`.
- Exact-head P0 run `35340545446` completed `success` for implementation HEAD `ad922ded33ff46a3028fca1217559a60be54fad6`.
- Exact-head P1 run `35340545586`, job `105585206110`, completed `failure` only because later independent Minecraft 26.2 API errors remain. `MinecraftPlayer.kt` is absent from the final compiler error set, so both targeted permission predicates are proven clean.
- Diagnostic artifact for run `35340545586`: `p1-compile-log-ad922ded33ff46a3028fca1217559a60be54fad6`, artifact ID `10545291225`, ZIP SHA-256 `1d8ac9f62db58dcff1ffb10bdde0ebaeb3f496ef81121ba916db1b50545d2efd`.
- The final compiler log still reports one direct command-permission API error in `common/src/main/kotlin/org/valkyrienskies/mod/common/command/commands/BackendCommand.kt`: removed `CommandSourceStack.hasPermission(Int)`.
- `BackendCommand.kt` uses `VSGameConfig.SERVER.Commands.changeBackendCommandPerms`, whose source contract explicitly says the configured permission level must be `0 <= x <= 4` and defaults to `4`.
- Minecraft 26.2 exposes the direct level-based permission equivalent through `Permission.HasCommandLevel(PermissionLevel.byId(level))` plus `CommandSourceStack.permissions().hasPermission(...)`; `PermissionLevel.byId` covers the same 0..4 command-level domain.
- Pinned upstream and current `1.21.1/main` are byte-identical for `BackendCommand.kt` at blob `46778377f9235c4f3492ea3c7b1bb2ef4c4fb8cf`.
- `ShipAssemblerItem.kt` remains deferred: its compiler error is nullable `shipData.slug: String?` passed into non-null vararg `Any`, and inventing a fallback string would change user-visible behavior without evidence.
- `VSKeyBindings.kt` remains deferred because Minecraft 26.2's `KeyMapping.Category` migration also changes category translation-key handling; a compile-only type replacement must not silently break `category.valkyrienskies.driving` translations.
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
- active_proof_head: `none; previous proof ad922ded33ff46a3028fca1217559a60be54fad6 landed`
- active_proof_run: `none; previous P1 run 35340545586 landed`
- active_hypothesis: `The next smallest safe standalone adaptation is BackendCommand's single dynamic command-level predicate, preserving its configured 0..4 level through Minecraft 26.2 Permission.HasCommandLevel(PermissionLevel.byId(level)).`
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
- `TestThrusterBlockEntity.kt` public Direction unit-vector accessor, with upstream force semantics unchanged;
- `TestThrusterBlock.kt` Minecraft 26.2 `neighborChanged` signature migration, with upstream redstone/thruster semantics unchanged;
- `RaycastUtils.kt` floating-direction API plus Kotlin non-null expression of the existing paired entity/location invariant, with upstream world/ship raycast semantics unchanged;
- `MinecraftPlayer.kt` old level-4 permission predicates to Minecraft 26.2 `Permissions.COMMANDS_OWNER`, preserving admin/config threshold and all player/reference-state semantics.

Representative remaining compiler areas include Create compat classpath/API drift, position/build-height changes, renderer/render-state APIs, SavedData/NBT `ValueInput`/`ValueOutput`, command permissions, resource reload listener generics, entity save/hurt/network APIs, tickets/ticks/structure processors, keybinding category migration, and Sable compatibility.

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
Frozen green. Original proof run `35304871880`; later confirmations include `35324164899`, `35324792335`, `35325575601`, `35327172660`, `35327644515`, `35327819629`, `35329592607`, `35331485247`, `35333733917`, `35334205890`, `35336506332`, `35337116561`, `35338858973`, and exact implementation confirmation `35340545446`.

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
- fixture/input mutations solely to manufacture green;
- compile-only `VSKeyBindings` category type replacement that drops or changes the existing category translations without explicitly migrating that resource contract;
- inventing a fallback value for nullable ship slug/name merely to satisfy Kotlin vararg nullability.

## next_safe_action

1. Preserve implementation HEAD `ad922ded33ff46a3028fca1217559a60be54fad6`, P0 run `35340545446`, and P1 run `35340545586` as proven clean for `MinecraftPlayer.kt`.
2. Preserve diagnostic artifact `p1-compile-log-ad922ded33ff46a3028fca1217559a60be54fad6`, artifact ID `10545291225`, ZIP SHA-256 `1d8ac9f62db58dcff1ffb10bdde0ebaeb3f496ef81121ba916db1b50545d2efd`.
3. Use the confirmed byte-identical pinned/current `BackendCommand.kt` source at blob `46778377f9235c4f3492ea3c7b1bb2ef4c4fb8cf`.
4. Adapt exactly the one `BackendCommand` permission predicate from `CommandSourceStack.hasPermission(configuredLevel)` to `CommandSourceStack.permissions().hasPermission(Permission.HasCommandLevel(PermissionLevel.byId(configuredLevel)))`, adding only the two Minecraft 26.2 permission imports required for that expression.
5. Preserve the configured `changeBackendCommandPerms` 0..4 contract and all backend/lod command execution, config mutation, messages, and physics backend selection unchanged.
6. Add only `BackendCommand.kt` to the P1 workflow diff-display path and trigger the smallest exact-head P0/P1 proof. If its P1 run is active, do not stack another source patch.
7. Do not batch the other command permission errors into this patch; each command may carry separate nullable-message or command behavior errors and needs its own evidence.
8. Do not alter Create compat, renderer, Sable/entity-dragging, physics architecture, collision, networking, player/camera, or unrelated semantics merely to remove compiler errors.
9. Stay in standalone P1. Do not integrate Create/SNR/Copycats yet.
10. Update this ledger after the next proof lands before any subsequent source patch.

## Video validation

No video is authorized during compile/API-port debugging. Video is closure-only for a user-visible runtime blocker that is already closure-ready from runtime/data proof.

## Final gate

`FINAL_READY` is forbidden until the exact final source/build and JAR SHA-256 are recorded and the user tests and accepts that exact JAR in the real Minecraft setup. CI alone cannot satisfy the final gate.
