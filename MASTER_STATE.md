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

## Current reconciliation — after GetShipCommand permission proof

- Latest proven implementation/source-port HEAD: `3d93c0041a59c0b78adfa9e2ff313cdbbe5f74aa` (`P1: port GetShipCommand permission API`).
- Its parent ledger commit is `0abe4c7de493683a3b7461f283e1e8b4e5cad100` (`watchdog: record DeleteCommand permission proof`).
- `3d93c0041a59c0b78adfa9e2ff313cdbbe5f74aa` adds only the isolated fail-closed `GetShipCommand` permission overlay plus P1 workflow wiring/diff-display path.
- The overlay changes exactly one legacy predicate from `CommandSourceStack.hasPermission(VSGameConfig.SERVER.Commands.getShipCommandPerms)` to `CommandSourceStack.permissions().hasPermission(Permission.HasCommandLevel(PermissionLevel.byId(VSGameConfig.SERVER.Commands.getShipCommandPerms)))`, adding only the required `Permission` and `PermissionLevel` imports.
- `/vs get-ship` uses `VSGameConfig.SERVER.Commands.getShipCommandPerms`, documented as `0 <= x <= 4`, default `0`; the adaptation preserves that configured threshold.
- Pinned upstream and current `1.21.1/main` are byte-identical for `GetShipCommand.kt` at blob `056766bf1ee40ebd266d88a3e28c8f6b87d22a7d`.
- Exact-head P0 run `35377210067` completed `success` for HEAD `3d93c0041a59c0b78adfa9e2ff313cdbbe5f74aa`.
- Exact-head P1 run `35377209937`, job `105704591262`, completed `failure` only because later independent Minecraft 26.2 API errors remain. The `GetShipCommand.kt` legacy permission error is absent from the final compiler error set; the intentionally untouched nullable `ship.slug: String?` success-message error remains at line 32, so the targeted permission adaptation is proven clean in isolation.
- Diagnostic artifact: `p1-compile-log-3d93c0041a59c0b78adfa9e2ff313cdbbe5f74aa`, artifact ID `10560773482`, size `8437` bytes, ZIP SHA-256 `8697b7badb3f739a29be29be14e2b0e0373ac7b98057a7e47245d565b535ad34`.
- `DeleteCommand.kt`'s nullable `r[0].slug: String?` message argument remains explicitly deferred; no fallback name/string may be invented merely to satisfy Kotlin vararg nullability.
- `GetShipCommand.kt`'s nullable `ship.slug: String?` success-message argument remains explicitly deferred; no fallback name/string may be invented merely to satisfy Kotlin vararg nullability.
- `RemassCommand.kt` still reports one removed legacy `CommandSourceStack.hasPermission(Int)` error at line 22 plus an independent nullable `ship.slug: String?` message error at line 32. It is only a candidate for the next isolated permission proof; no patch is authorized until its pinned/current provenance and configured permission semantics are checked read-only.
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
- active_proof_head: `none; previous proof 3d93c0041a59c0b78adfa9e2ff313cdbbe5f74aa landed`
- active_proof_run: `none; previous P1 run 35377209937 landed`
- active_hypothesis: `none after GetShipCommand proof; select the next smallest source/API cluster only after this proof is durably recorded and its candidate provenance/semantics are checked read-only.`
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
- `ScaleCommand.kt` same dynamic permission migration, ship argument/minimum-scale parsing and `vsCore.scaleShip` behavior unchanged;
- `SplittingCommand.kt` same dynamic permission migration, ship selection/boolean argument/loaded-ship attachment behavior and messages unchanged;
- `StaticCommand.kt` same dynamic permission migration, ship selection/boolean `is-static` assignment and messages unchanged;
- `TeleportCommand.kt` same dynamic permission migration, all position/euler/velocity/angular-velocity branches, `ShipTeleportData`, teleport calls, messages, and return values unchanged;
- `DeleteCommand.kt` same dynamic permission migration, literal/ship selection/optional `deleteBlocks`/`ShipAssembler.deleteShip`/success-failure branching/messages/return values unchanged; nullable ship slug remains deferred;
- `GetShipCommand.kt` same dynamic permission migration, literal/source-entity check/ray trace/ship lookup/success-failure branching/message keys/ship ID/return values unchanged; nullable ship slug remains deferred.

Representative remaining compiler areas: Create compat classpath/API drift, position/build-height changes, renderer/render-state APIs, SavedData/NBT `ValueInput`/`ValueOutput`, remaining command permission/nullability work, resource reload listener generics, entity save/hurt/network APIs, tickets/ticks/structure processors, keybinding category migration, and Sable compatibility.

## Proof chain retained

- `ad922ded33ff46a3028fca1217559a60be54fad6`: `MinecraftPlayer.kt` permission predicates proven clean by P1 run `35340545586`.
- `6253d38ff84785921c95c175563a5b24800979ef`: `BackendCommand.kt` proven clean by P1 `35342297011`; artifact `10545204522`; ZIP SHA-256 `72de18f36f7538bf818ee59f090fea3d009e7c6f4265a9f7f5261517344b4c03`.
- `b1a8d44abb54150a5b97e03677a37977702ed65e`: `GetAirCommand.kt` proven clean by P1 `35355388045`; artifact `10552130508`; ZIP SHA-256 `f921fc35d29e54d827fafbb5ca4c2d5664092a72579e3e394e15cede87e212b3`.
- `7700e2194f96b79db0ffc67b6b754fecd29cc04f`: `GetGravityCommand.kt` proven clean by P1 `35357765377`; artifact `10552603034`; ZIP SHA-256 `dfa0c9eae9e1fc118784975bcf7adcbaa0d2ddca29a4f8318b290b1f30cea877`.
- `bd796323fa1b49bd4844c0a4089edb1025ca89f9`: `DryCommand.kt` proven clean by P1 `35359836381`; artifact `10554023210`; ZIP SHA-256 `54086e93046ff3e7f113d0dd80e622e7ee4b39a5ee63e5dfed836041dce35b8d`.
- `18959ca9823cd790e51580bf9911d1757890acb0`: `RenameCommand.kt` proven clean by P1 `35361901965`; artifact `10555046879`; ZIP SHA-256 `b7c5ee49f8049a48e81b6879a519da0724787cbdbac6012aa07c7517ab9e57be`.
- `915d88e3c64ecc49bb502c8fe849b5744d99cea4`: `ScaleCommand.kt` proven clean by P1 `35364622301`; artifact `10554444674`; ZIP SHA-256 `a663d408b9fc0f08ed96545827b1c4e9030d83a77c79e3590798fd5f17870763`.
- `d919b45d6f35c9917c13e69c3faf8011e0057057`: `SplittingCommand.kt` proven clean by P1 `35366811861`; artifact `10557430465`; ZIP SHA-256 `af0a83997d92d431f31c215ba985d502fc7b35edc1ac8c7fc6f5585e84ea4d8b`.
- `e1fa31795ba5901fdde0c1238e434faf06be2f49`: `StaticCommand.kt` proven clean by P1 `35370436174`; artifact `10558762061`; ZIP SHA-256 `958012e1dd3cdf1a8bae2d40f423061487c7e9a4b57cd0094e7ad90ebd7328a0`.
- `c75047ae1f38b92fc39a56911a967ce914952c5c`: `TeleportCommand.kt` proven clean by P1 `35372443583`; artifact `10559450323`; ZIP SHA-256 `5319fc6386f0a87c23893e84c26aeb871c6453ad5c3fa7374134a4cf35024faf`.
- `6a2901ccbb359d867209195c58dc652b0a39e594`: `DeleteCommand.kt` permission predicate proven clean by P1 `35375165938`; artifact `10559548159`; ZIP SHA-256 `d1ed6dd29874c3dc4c45d1e55d4042315697856e69de18b393f9e97c214666b3`.
- `3d93c0041a59c0b78adfa9e2ff313cdbbe5f74aa`: `GetShipCommand.kt` permission predicate proven clean by P1 `35377209937`; artifact `10560773482`; ZIP SHA-256 `8697b7badb3f739a29be29be14e2b0e0373ac7b98057a7e47245d565b535ad34`.

## Sable contract

A previous hypothesis that no VS2 source imported Sable was disproven. `common/src/main/kotlin/org/valkyrienskies/mod/compat/SableCompat.kt` is real upstream VS2 code and uses Sable companion state for entity-dragging/reference behavior.

The current build overlay's omission of an unavailable pinned Sable artifact is temporary compile-probe scaffolding only. Final architecture must resolve Sable through a traceable compatible dependency/API path or an explicitly documented minimal compatibility shim into existing VS2 architecture. Deleting or replacing VS2 entity-dragging semantics is forbidden.

## Mandatory architecture

Final behavior must remain based on real upstream VS2 machinery for ship lifecycle/ship-space, transforms, physics-core integration, collision integration, entity dragging/reference-frame behavior, player/body/camera integration, networking/synchronization, and rendering.

Forbidden final substitutes: custom VS2-style reference frames, synthetic carry velocity/inertia, fake gravity, manual floor/wall/ceiling clamps, per-tick teleport/setPos chase, camera counter-rotation/forcing, duplicate authority, floor-only success, and the retired `VS2-Create_Interactive` workaround chain.

## Milestones

### P0 — Upstream import + provenance
Frozen green. Exact upstream identity/pin/license/provenance is established and repeatedly re-confirmed, including exact implementation P0 run `35377210067` for the latest proven implementation HEAD.

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

1. Preserve implementation HEAD `3d93c0041a59c0b78adfa9e2ff313cdbbe5f74aa`, exact-head P0 `35377210067`, and P1 `35377209937` as the `GetShipCommand.kt` permission proof.
2. Preserve artifact `p1-compile-log-3d93c0041a59c0b78adfa9e2ff313cdbbe5f74aa`, ID `10560773482`, size `8437` bytes, ZIP SHA-256 `8697b7badb3f739a29be29be14e2b0e0373ac7b98057a7e47245d565b535ad34`.
3. Reconcile the remaining exact compiler evidence from run `35377209937`; do not infer the next patch from older chat state.
4. The smallest obvious remaining command candidate is `RemassCommand.kt`, but first perform read-only checks only: confirm pinned baseline versus current `1.21.1/main` blob identity and inspect the exact `VSGameConfig.SERVER.Commands.remassCommandPerms` range/default semantics.
5. If and only if those read-only checks confirm a traceable permission-only adaptation, record that candidate/hypothesis durably before patching it. Keep the independent nullable `ship.slug` message error untouched.
6. Do not batch nullable-message fixes, Create compat, renderer, Sable/entity-dragging, physics, collision, networking, player/camera, or unrelated semantics.
7. Stay in standalone P1. Do not integrate Create/SNR/Copycats yet.
8. No video is authorized during compile/API-port work.

## Video validation

No video is authorized during compile/API-port debugging. Video is closure-only for a user-visible runtime blocker already closure-ready from runtime/data proof.

## Final gate

`FINAL_READY` is forbidden until the exact final source/build and JAR SHA-256 are recorded and the user tests and accepts that exact JAR in the real Minecraft setup. CI alone cannot satisfy the final gate.