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

## Current reconciliation — after ScaleCommand proof

- Latest proven implementation/source-port HEAD: `915d88e3c64ecc49bb502c8fe849b5744d99cea4` (`P1: port ScaleCommand permission API`).
- Its parent ledger commit is `0ba955182128cbabc9006561fb581e22bf4420e8` (`watchdog: record RenameCommand permission proof`).
- `915d88e3c64ecc49bb502c8fe849b5744d99cea4` adds only the isolated fail-closed `ScaleCommand` permission overlay plus P1 workflow wiring/diff-display path.
- The overlay changes exactly one legacy predicate from `CommandSourceStack.hasPermission(VSGameConfig.SERVER.Commands.scaleShipCommandPerms)` to `CommandSourceStack.permissions().hasPermission(Permission.HasCommandLevel(PermissionLevel.byId(VSGameConfig.SERVER.Commands.scaleShipCommandPerms)))`, adding only the required `Permission` and `PermissionLevel` imports.
- `VSGameConfig.SERVER.Commands.scaleShipCommandPerms` remains explicitly constrained to `0 <= x <= 4`, default `2`.
- Pinned upstream and current `1.21.1/main` are byte-identical for `ScaleCommand.kt` at blob `ae2dc875d8bf146a8e3ffa4c76fae14984866a96`.
- Exact-head P0 run `35364622268` completed `success` for HEAD `915d88e3c64ecc49bb502c8fe849b5744d99cea4`.
- Exact-head P1 run `35364622301`, job `105663932648`, completed `failure` only because later independent Minecraft 26.2 API errors remain. `ScaleCommand.kt` is absent from the final compiler error set, so its targeted permission adaptation is proven clean.
- Diagnostic artifact: `p1-compile-log-915d88e3c64ecc49bb502c8fe849b5744d99cea4`, artifact ID `10554444674`, size `8524` bytes, ZIP SHA-256 `a663d408b9fc0f08ed96545827b1c4e9030d83a77c79e3590798fd5f17870763`.
- Remaining permission-only command errors include `SplittingCommand.kt`, `StaticCommand.kt`, and `TeleportCommand.kt`.
- `DeleteCommand.kt`, `GetShipCommand.kt`, and `RemassCommand.kt` also have independent nullable-message errors and are not the smallest isolated permission proof.
- `SplittingCommand.kt` reports exactly one compiler error: removed legacy `CommandSourceStack.hasPermission(Int)`. No second compile error is reported for that file.
- Pinned upstream and current `1.21.1/main` are byte-identical for `SplittingCommand.kt` at blob `0aa62977a9a722fa9ef93b2313a27661b7be6697`.
- `VSGameConfig.SERVER.Commands.deleteShipCommandPerms`, reused by `/vs splitting`, is explicitly constrained to `0 <= x <= 4`, default `2`, so Minecraft 26.2 `Permission.HasCommandLevel(PermissionLevel.byId(level))` preserves the configured threshold.
- `ShipAssemblerItem.kt` remains deferred: nullable `shipData.slug: String?` into non-null vararg `Any` must not be papered over with an invented fallback string.
- `VSKeyBindings.kt` remains deferred because Minecraft 26.2 `KeyMapping.Category` migration changes category translation-key handling; a compile-only type swap must not silently break `category.valkyrienskies.driving`.
- No code from retired `apm23/VS2-Create_Interactive` has been imported or reused as implementation source.

## Target runtime baseline

- Minecraft `26.2`
- Java `25`
- Fabric Loader `0.19.3`
- Fabric API `0.160.0+26.2`
- Create Fly `6.0.9-1`
- Steam 'n' Rails embedded `SNR.FLY-STABLE-1.2.2+fabric-mc26.2`
- Copycats embedded `3.0.7-createfly+mc.26.2-v1.14`
- Exact dependency bytes are locked by SHA-256 in `BASELINE_LOCK.json`.

## Project state

- project_state: `P1_SOURCE_API_ADAPTATION_IN_PROGRESS`
- active_blocker: `MINECRAFT_26_2_SOURCE_API_DRIFT`
- active_proof_head: `none; previous proof 915d88e3c64ecc49bb502c8fe849b5744d99cea4 landed`
- active_proof_run: `none; previous P1 run 35364622301 landed`
- active_hypothesis: `The next smallest safe standalone adaptation is SplittingCommand's single dynamic command-level predicate, preserving its existing deleteShipCommandPerms 0..4 threshold through Minecraft 26.2 Permission.HasCommandLevel(PermissionLevel.byId(level)).`
- final_ready: `false`
- user_runtime_validation: `NOT_APPLICABLE_YET`

## Proven P1 progress

Build/toolchain:
- Java 25 + Gradle 9.5.1 starts;
- Minecraft 26.x build uses `dev.architectury.loom-no-remap` without Mojang mappings/remapJar;
- Gradle 9 `archivesBaseName` removal adapted;
- old `modImplementation` / `modApi` / `modCompileOnly` configurations migrated for no-remap Loom;
- dependency resolution reaches real `:common:compileKotlin`;
- explicit source overlays are fail-closed.

Source/API clusters proven clean in exact-head runs:
- data-provider `ResourceLocation -> Identifier` plus registry-holder `location() -> identifier()`;
- `BlockStateInfoProvider.kt` Identifier cluster;
- `SimpleSoundInstanceOnShip.kt` Identifier cluster;
- `VSEntityManager.kt` Identifier cluster;
- `EntityData.kt` non-null generic bounds;
- `NbtUtil.kt` guarded `Optional<Double>` reads;
- `VectorConversionsMC.kt`, `ValkyrienSkies.kt`, `TestFlapBlock.kt`, `TestWingBlock.kt`, and `TestThrusterBlockEntity.kt` public Direction unit-vector accessor migration;
- `TestThrusterBlock.kt` Minecraft 26.2 `neighborChanged` signature migration with redstone/thruster semantics unchanged;
- `RaycastUtils.kt` floating-direction API plus explicit non-null expression of its existing paired entity/location invariant;
- `MinecraftPlayer.kt` level-4 admin/config permission predicates to Minecraft 26.2 `Permissions.COMMANDS_OWNER`;
- `BackendCommand.kt` dynamic configured permission migrated to `Permission.HasCommandLevel(PermissionLevel.byId(level))`;
- `GetAirCommand.kt` same dynamic permission migration, aerodynamic/dimension/message behavior unchanged;
- `GetGravityCommand.kt` same dynamic permission migration, gravity/aerodynamic/dimension/message behavior unchanged;
- `DryCommand.kt` same dynamic permission migration, ship-AABB iteration and liquid/waterlogged handling unchanged;
- `RenameCommand.kt` same dynamic permission migration, ship argument/new-name parsing and `vsCore.renameShip` behavior unchanged;
- `ScaleCommand.kt` same dynamic permission migration, ship argument/minimum-scale parsing and `vsCore.scaleShip` behavior unchanged.

Representative remaining compiler areas: Create compat classpath/API drift, position/build-height changes, renderer/render-state APIs, SavedData/NBT `ValueInput`/`ValueOutput`, remaining command permissions, resource reload listener generics, entity save/hurt/network APIs, tickets/ticks/structure processors, keybinding category migration, and Sable compatibility.

## Proof chain retained

- `ad922ded33ff46a3028fca1217559a60be54fad6`: `MinecraftPlayer.kt` permission predicates proven clean by P1 run `35340545586`.
- `6253d38ff84785921c95c175563a5b24800979ef`: `BackendCommand.kt` proven clean by P1 `35342297011`; artifact `10545204522`; ZIP SHA-256 `72de18f36f7538bf818ee59f090fea3d009e7c6f4265a9f7f5261517344b4c03`.
- `b1a8d44abb54150a5b97e03677a37977702ed65e`: `GetAirCommand.kt` proven clean by P1 `35355388045`; artifact `10552130508`; ZIP SHA-256 `f921fc35d29e54d827fafbb5ca4c2d5664092a72579e3e394e15cede87e212b3`.
- `7700e2194f96b79db0ffc67b6b754fecd29cc04f`: `GetGravityCommand.kt` proven clean by P1 `35357765377`; artifact `10552603034`; ZIP SHA-256 `dfa0c9eae9e1fc118784975bcf7adcbaa0d2ddca29a4f8318b290b1f30cea877`.
- `bd796323fa1b49bd4844c0a4089edb1025ca89f9`: `DryCommand.kt` proven clean by P1 `35359836381`; artifact `10554023210`; ZIP SHA-256 `54086e93046ff3e7f113d0dd80e622e7ee4b39a5ee63e5dfed836041dce35b8d`.
- `18959ca9823cd790e51580bf9911d1757890acb0`: `RenameCommand.kt` proven clean by P1 `35361901965`; artifact `10555046879`; ZIP SHA-256 `b7c5ee49f8049a48e81b6879a519da0724787cbdbac6012aa07c7517ab9e57be`.
- `915d88e3c64ecc49bb502c8fe849b5744d99cea4`: `ScaleCommand.kt` proven clean by P1 `35364622301`; artifact `10554444674`; ZIP SHA-256 `a663d408b9fc0f08ed96545827b1c4e9030d83a77c79e3590798fd5f17870763`.

## Sable contract

A previous hypothesis that no VS2 source imported Sable was disproven. `common/src/main/kotlin/org/valkyrienskies/mod/compat/SableCompat.kt` is real upstream VS2 code and uses Sable companion state for entity-dragging/reference behavior.

The current build overlay's omission of an unavailable pinned Sable artifact is temporary compile-probe scaffolding only. Final architecture must resolve Sable through a traceable compatible dependency/API path or an explicitly documented minimal compatibility shim into existing VS2 architecture. Deleting or replacing VS2 entity-dragging semantics is forbidden.

## Mandatory architecture

Final behavior must remain based on real upstream VS2 machinery for ship lifecycle/ship-space, transforms, physics-core integration, collision integration, entity dragging/reference-frame behavior, player/body/camera integration, networking/synchronization, and rendering.

Forbidden final substitutes: custom VS2-style reference frames, synthetic carry velocity/inertia, fake gravity, manual floor/wall/ceiling clamps, per-tick teleport/setPos chase, camera counter-rotation/forcing, duplicate authority, floor-only success, and the retired `VS2-Create_Interactive` workaround chain.

## Milestones

### P0 — Upstream import + provenance
Frozen green. Exact upstream identity/pin/license/provenance is established and repeatedly re-confirmed, including exact implementation P0 run `35364622268` for the latest proven implementation HEAD.

### P1 — Standalone VS2 26.2 compile/boot
Port actual VS2 until common/Fabric compile, standalone client/server boot, and core/native initialization are proven without Create/SNR/Copycats hiding failures.

### P2 / M1 — Standalone real VS2 runtime
Must prove a real VS2 ship: lifecycle, translation/rotation, standing/walking, jump-airborne-natural landing, solid floor/walls/ceiling, stable free camera, entity dragging/reference frame, client/server sync, and no fake carry/teleport chase.

### P3 — Create Fly bridge
Only after standalone VS2 is frozen green. Create owns railway gameplay/trajectory; VS2 owns real moving ship/reference-space semantics.

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
- compile-only `VSKeyBindings` category replacement that changes/drops existing translation behavior;
- invented fallback values for nullable ship slug/name just to satisfy Kotlin vararg nullability.

## next_safe_action

1. Preserve implementation HEAD `915d88e3c64ecc49bb502c8fe849b5744d99cea4`, exact-head P0 `35364622268`, and P1 `35364622301` as the `ScaleCommand.kt` proof.
2. Preserve artifact `p1-compile-log-915d88e3c64ecc49bb502c8fe849b5744d99cea4`, ID `10554444674`, ZIP SHA-256 `a663d408b9fc0f08ed96545827b1c4e9030d83a77c79e3590798fd5f17870763`.
3. Use confirmed byte-identical pinned/current `SplittingCommand.kt` blob `0aa62977a9a722fa9ef93b2313a27661b7be6697`.
4. Adapt exactly the one `SplittingCommand` predicate from `CommandSourceStack.hasPermission(VSGameConfig.SERVER.Commands.deleteShipCommandPerms)` to `CommandSourceStack.permissions().hasPermission(Permission.HasCommandLevel(PermissionLevel.byId(VSGameConfig.SERVER.Commands.deleteShipCommandPerms)))`, adding only the two required Minecraft 26.2 permission imports.
5. Preserve the existing use of `deleteShipCommandPerms` explicit 0..4/default `2`, ship selection, boolean `enable` argument, loaded-ship attachment update, success message, return value, and command structure unchanged.
6. Add only `SplittingCommand.kt` to the P1 workflow diff-display path and trigger the smallest exact-head P0/P1 proof. If P1 is active, do not stack another source patch.
7. Do not batch another permission command into this proof.
8. Do not alter Create compat, renderer, Sable/entity-dragging, physics, collision, networking, player/camera, or unrelated semantics merely to remove compiler errors.
9. Stay in standalone P1. Do not integrate Create/SNR/Copycats yet.
10. After the Splitting proof completes, update this ledger before any subsequent source patch.

## Video validation

No video is authorized during compile/API-port debugging. Video is closure-only for a user-visible runtime blocker already closure-ready from runtime/data proof.

## Final gate

`FINAL_READY` is forbidden until the exact final source/build and JAR SHA-256 are recorded and the user tests and accepts that exact JAR in the real Minecraft setup. CI alone cannot satisfy the final gate.
