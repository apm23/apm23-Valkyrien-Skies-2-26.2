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

## Current reconciliation — EmptyRenderer Identifier proof completed

- Latest implementation/proof HEAD: `5a6f41ee258d704fdb91fa9b115854c19623a7eb` (`P1: isolate EmptyRenderer Identifier migration`).
- Parent ledger-only reconciliation HEAD `8ae08b032db583b0f064ef59c9bf52d2505f253c` had exact-head P0 run `35384153339` completed `success` and made no source-port change.
- Exact-head P0 run `35384633799` for `5a6f41ee258d704fdb91fa9b115854c19623a7eb` completed `success`.
- Exact-head P1 run `35384633761`, job `105728547942`, completed `failure` only because later independent Minecraft 26.2 API errors remain.
- All traceable overlays, including `apply_p1_emptyrenderer_identifier_26_2.py`, applied successfully; the port-delta validation step also succeeded.
- Pinned baseline `f39132148e717d325933b4ce6e9e9fb13d929390` and current `1.21.1/main` are byte-identical for `EmptyRenderer.kt` at blob `ff3253aa068256ae06c92a6b29d247acabce0532`.
- Exact EmptyRenderer delta is limited to two vocabulary changes: import `net.minecraft.resources.ResourceLocation` -> `net.minecraft.resources.Identifier`, and `getTextureLocation(...): ResourceLocation?` -> `Identifier?`.
- `EntityRenderer<Entity>(context)` inheritance, renderer lifecycle, render-state semantics, and all other behavior remain intentionally untouched by this proof.
- Run `35384633761` shows both earlier unresolved `ResourceLocation` diagnostics for `EmptyRenderer.kt` are gone.
- The intentionally independent Minecraft 26.2 diagnostic remains at `EmptyRenderer.kt:9`: `2 type arguments expected for 'class EntityRenderer<T : Entity, S : EntityRenderState> : Any'`.
- Therefore the isolated EmptyRenderer resource-vocabulary migration is proven clean and frozen independently from the later render-state migration.
- Diagnostic artifact: `p1-compile-log-5a6f41ee258d704fdb91fa9b115854c19623a7eb`, artifact ID `10563931126`, size `8323` bytes, ZIP SHA-256 `ec45c981a8589ae3a93a3e0955cff789172c487472598bd4a5803294d98475ae`.
- Earlier TestChair Direction proof remains preserved at HEAD `369d042ee7d86c109825ae00b637c1230a70e7e5`, exact-head P0 `35383401723`, P1 `35383401868` / job `105724661254`, artifact `10562768230`, ZIP SHA-256 `4f3ad14af6cf671d9c5f43a3e356dbd4c03dbd866f549ff6b8937d30c7cc5bc4`.
- `TestChairBlock.kt` line-58 private `Direction.normal` remains gone; intentionally independent line-54 entity-create/signature errors and line-57 `moveTo` error remain.
- Earlier EntityDragger Direction proof remains preserved at implementation HEAD `f86f606e2f51e42513f4ae558bb740164d3d9f23`, exact-head P0 `35381321480`, P1 `35381321453`, artifact `10563195663`, ZIP SHA-256 `619e4759fee46606f2a93e94e8b42cbd463b27110e46e8590ae98e861fe70ffa`; independent line-148 local-control error remains.
- Previous Remass permission proof remains preserved at implementation HEAD `6762f2022756506b282f176f4ea4a5d6b40b8ea7`, exact-head P0 `35379217178`, P1 `35379217305`, artifact `10561352586`, ZIP SHA-256 `4885fb7979234c4e32621cd21bfc83f21d14f6b8128c7c5b76b59338de396dd9`.
- The dynamic command-permission-only cluster remains exhausted in the exact compiler error set: Delete/GetShip/Remass retain only independent nullable-message errors; no legacy `hasPermission` error remains in those commands.
- `DeleteCommand.kt` nullable `r[0].slug: String?`, `GetShipCommand.kt` nullable `ship.slug: String?`, and `RemassCommand.kt` nullable `ship.slug: String?` remain explicitly deferred; no fallback name/string may be invented merely to satisfy Kotlin vararg nullability.
- `ShipAssemblerItem.kt`, `ShipCreatorItem.kt`, and `ShipRemoverItem.kt` nullable ship names remain deferred for the same reason.
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
- active_proof_head: `5a6f41ee258d704fdb91fa9b115854c19623a7eb; EmptyRenderer Identifier proof completed`
- active_proof_run: `35384633761; targeted EmptyRenderer Identifier proof succeeded although overall compile remains red on later independent API drift`
- active_hypothesis: `none; EmptyRenderer Identifier hypothesis is proven and frozen. Reconcile this ledger-only commit and allow its provenance workflow to settle, then select exactly one next independent Minecraft 26.2 source/API cluster from the exact compiler set of run 35384633761 before mutating source.`
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
- `EmptyRenderer.kt` resource vocabulary `ResourceLocation -> Identifier` only; render-state migration remains separate;
- `EntityData.kt` non-null generic bounds;
- `NbtUtil.kt` guarded `Optional<Double>` reads;
- `VectorConversionsMC.kt`, `ValkyrienSkies.kt`, `TestFlapBlock.kt`, `TestWingBlock.kt`, `TestThrusterBlockEntity.kt`, `EntityDragger.kt`, and the isolated facing-vector site in `TestChairBlock.kt` use the public Direction unit-vector accessor at proven sites;
- `TestThrusterBlock.kt` Minecraft 26.2 `neighborChanged` signature migration with redstone/thruster semantics unchanged;
- `RaycastUtils.kt` floating-direction API plus explicit non-null expression of its existing paired entity/location invariant;
- `MinecraftPlayer.kt` level-4 admin/config permission predicates to Minecraft 26.2 `Permissions.COMMANDS_OWNER`;
- `BackendCommand.kt`, `GetAirCommand.kt`, `GetGravityCommand.kt`, `DryCommand.kt`, `RenameCommand.kt`, `ScaleCommand.kt`, `SplittingCommand.kt`, `StaticCommand.kt`, `TeleportCommand.kt`, `DeleteCommand.kt`, `GetShipCommand.kt`, and `RemassCommand.kt` dynamic configured command-level predicates migrated to `Permission.HasCommandLevel(PermissionLevel.byId(level))` without changing command behavior.

Representative remaining compiler areas from exact run `35384633761`: Create compat classpath/API drift; `EmptyRenderer` render-state/type-argument migration; `CompatUtil` position/build-height/nullability API drift; `ShipSavedData` Optional/SaveData changes; `VSGameUtils` Identifier/build-height/chunk-position APIs; `ValkyrienSkiesMod` Identifier/creative-tab output changes; assembly/tick/ValueInput-ValueOutput/structure processor migrations; TestChair entity-create/`moveTo` APIs; TestHinge APIs; deferred nullable command/item messages; reload-listener/Identifier generics; keybinding category migration; ShipMountingEntity save/hurt APIs; entity-handler rendering APIs; networking/local-control/lerp APIs; `EntityDragger` local-control API; chunk tickets; Sable compatibility; and relocation APIs.

## Proof chain retained

- `ad922ded33ff46a3028fca1217559a60be54fad6`: `MinecraftPlayer.kt` permission predicates proven clean by P1 `35340545586`.
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
- `6762f2022756506b282f176f4ea4a5d6b40b8ea7`: `RemassCommand.kt` permission predicate proven clean by P1 `35379217305`; exact-head P0 `35379217178`; artifact `10561352586`; ZIP SHA-256 `4885fb7979234c4e32621cd21bfc83f21d14f6b8128c7c5b76b59338de396dd9`.
- `f86f606e2f51e42513f4ae558bb740164d3d9f23`: isolated `EntityDragger.kt` hit-face Direction accessor proven clean by P1 `35381321453`; exact-head P0 `35381321480`; artifact `10563195663`; ZIP SHA-256 `619e4759fee46606f2a93e94e8b42cbd463b27110e46e8590ae98e861fe70ffa`; independent line-148 local-control error remains.
- `369d042ee7d86c109825ae00b637c1230a70e7e5`: isolated `TestChairBlock.kt` facing Direction accessor proven clean by P1 `35383401868`, job `105724661254`; exact-head P0 `35383401723`; artifact `10562768230`; ZIP SHA-256 `4f3ad14af6cf671d9c5f43a3e356dbd4c03dbd866f549ff6b8937d30c7cc5bc4`; independent line-54 entity-create/signature errors and line-57 `moveTo` error remain.
- `5a6f41ee258d704fdb91fa9b115854c19623a7eb`: isolated `EmptyRenderer.kt` resource vocabulary migration proven clean by P1 `35384633761`, job `105728547942`; exact-head P0 `35384633799`; artifact `10563931126`; ZIP SHA-256 `ec45c981a8589ae3a93a3e0955cff789172c487472598bd4a5803294d98475ae`; independent `EntityRenderer<T,S>` render-state diagnostic remains.

## Sable contract

A previous hypothesis that no VS2 source imported Sable was disproven. `common/src/main/kotlin/org/valkyrienskies/mod/compat/SableCompat.kt` is real upstream VS2 code and uses Sable companion state for entity-dragging/reference behavior.

The current build overlay's omission of an unavailable pinned Sable artifact is temporary compile-probe scaffolding only. Final architecture must resolve Sable through a traceable compatible dependency/API path or an explicitly documented minimal compatibility shim into existing VS2 architecture. Deleting or replacing VS2 entity-dragging semantics is forbidden.

## Mandatory architecture

Final behavior must remain based on real upstream VS2 machinery for ship lifecycle/ship-space, transforms, physics-core integration, collision integration, entity dragging/reference-frame behavior, player/body/camera integration, networking/synchronization, and rendering.

Forbidden final substitutes: custom VS2-style reference frames, synthetic carry velocity/inertia, fake gravity, manual floor/wall/ceiling clamps, per-tick teleport/setPos chase, camera counter-rotation/forcing, duplicate authority, floor-only success, and the retired `VS2-Create_Interactive` workaround chain.

## Milestones

### P0 — Upstream import + provenance
Frozen green. Exact upstream identity/pin/license/provenance is established and repeatedly re-confirmed, including exact proof-head P0 run `35384633799` for `5a6f41ee258d704fdb91fa9b115854c19623a7eb`.

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

1. Preserve exact EmptyRenderer Identifier proof HEAD `5a6f41ee258d704fdb91fa9b115854c19623a7eb`, exact-head P0 `35384633799`, P1 `35384633761` / job `105728547942`, and artifact `10563931126` / ZIP SHA-256 `ec45c981a8589ae3a93a3e0955cff789172c487472598bd4a5803294d98475ae`.
2. Preserve `EmptyRenderer.kt` `Identifier` import/texture-return adaptation and keep `EntityRenderer<Entity>(context)`, render-state/lifecycle semantics, and all other renderer behavior untouched until that render-state migration becomes its own evidenced hypothesis.
3. Reconcile actual HEAD after this ledger-only commit and allow any automatically triggered provenance workflow to settle before source mutation.
4. Then select exactly one smallest independent Minecraft 26.2 source/API cluster from the exact compiler set of run `35384633761`, using direct upstream/source/API evidence before patching. Record the selected hypothesis in this ledger before or together with its isolated proof setup.
5. Do not batch deferred nullable-message fixes, `VSKeyBindings`, Create compat, render-state migration, Sable dependency work, tickets, networking/local-control semantics, TestChair create/`moveTo`, or unrelated clusters unless that exact subsystem becomes the separately evidenced active hypothesis.
6. Stay in standalone P1. Do not integrate Create/SNR/Copycats yet.
7. No video is authorized during compile/API-port work.

## Video validation

No video is authorized during compile/API-port debugging. Video is closure-only for a user-visible runtime blocker already closure-ready from runtime/data proof.

## Final gate

`FINAL_READY` is forbidden until the exact final source/build and JAR SHA-256 are recorded and the user tests and accepts that exact JAR in the real Minecraft setup. CI alone cannot satisfy the final gate.
