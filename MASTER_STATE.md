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

## Current reconciliation — VSEntityHandlerDataLoader Identifier vocabulary proven

- Current proven implementation HEAD: `4a657f4625f69b26b9ccef9f7235cee271325d98` (`P1: wire VSEntityHandlerDataLoader Identifier proof`).
- Exact-head P0 provenance run `35414238420`, job `105819598472`, completed `success` and re-confirmed the pinned upstream VS2 identity.
- Exact-head P1 standalone compile run `35414238535`, job `105819599047`, completed `failure` only because later independent Minecraft 26.2 source/API errors remain.
- Every traceable overlay applied successfully, including `apply_p1_vsentityhandlerdataloader_identifier_26_2.py`; explicit port-delta validation and Gradle runtime steps succeeded.
- Pinned upstream target blob is `6c8c69045bfeeffea101fc7d1fba66923ce9f986`; overlay blob is `1bf9aa3e2b10ffc9ec902020cff7b36463fd8a76`.
- Exact `VSEntityHandlerDataLoader.kt` delta replaces only the three pinned `ResourceLocation` vocabulary occurrences with `Identifier`: the import, reload-listener input-map key, and handler-id parser.
- `SimpleJsonResourceReloadListener` generic/constructor/apply semantics, `BuiltInRegistries.ENTITY_TYPE.getOptional`, JSON extraction, handler pairing, logging/error behavior, and surrounding VS2 behavior were not altered by this proof.
- Run `35414238535` contains no unresolved `ResourceLocation` diagnostic in `VSEntityHandlerDataLoader.kt`; all targeted vocabulary diagnostics disappeared.
- The only remaining `VSEntityHandlerDataLoader.kt` diagnostic is the separate Minecraft 26.2 typed reload-listener boundary: `SimpleJsonResourceReloadListener` requires one type argument. That is outside this isolated proof.
- Therefore the isolated `VSEntityHandlerDataLoader.kt` `ResourceLocation -> Identifier` migration is proven clean and frozen independently from later compiler clusters.
- Diagnostic artifact: `p1-compile-log-4a657f4625f69b26b9ccef9f7235cee271325d98`, artifact ID `10575555973`, size `6805` bytes, ZIP SHA-256 `b980ea48f7b71f3ec9d79e119ff83d567fbaf16973871cb547570ae23bc83159`.
- Prior `DimensionParametersResolver.kt` Identifier-vocabulary proof remains frozen at HEAD `19d15fccf7345fc80f91800356a105d3595db87c`, P0 `35413012083` / job `105816180721`, P1 `35413012178` / job `105816181236`, artifact `10574836065`, ZIP SHA-256 `ca585a823377e4752017103a7acbe30be1078035c084dd28a758496659f14b95`; continuity-ledger freeze HEAD `1156e5a7271a114dab9b0af0bd834f4eea9bff9c` has P0 `35414078124` / job `105819152815` success.
- Prior `MassDatapackResolver.kt` Identifier-vocabulary proof remains frozen at HEAD `a40316e93a61594018fd6f8f9d4b913d7fb2eb80`, P0 `35411562202` / job `105812049740`, P1 `35411562107` / job `105812049438`, artifact `10574698116`, ZIP SHA-256 `41dc8482808a7de1a46bf4f680c00560ae085a267118e3a9dddec1f5997d2506`.
- Prior `MassDatapackResolver` dummy-`BlockGetter` minY proof remains frozen at HEAD `563cbcba7bb1c92ca27820ef785d11bb88872524`, P0 `35410678210` / job `105809557245`, P1 `35410678254` / job `105809557590`, artifact `10573811879`, ZIP SHA-256 `ef0e33b2db1cff60f1e1d14658cbb9d50523309a227806cf3f09776fd23df3f2`.
- Prior `SeamlessChunksManager` ChunkPos packed-key proof remains frozen at HEAD `75a434c728f1ca020b550882967085ccc53d5c3b`, P0 `35409275352` / job `105805422622`, P1 `35409275363` / job `105805423593`, artifact `10574055235`, ZIP SHA-256 `cb032a68942404c798debc540ad7b387c1f06ac41d6854f570aa43e70894a9b6`.
- No code from retired `apm23/VS2-Create_Interactive` has been imported or reused as implementation source.

## Target runtime baseline

- Minecraft `26.2`
- Java `25`
- Fabric Loader `0.19.3`
- Fabric API `0.160.0+26.2`, SHA-256 `5f3dff88e1661166e222213302b25ace6c36dc3683804cbd4b5acf93138ea05e`
- Create Fly `6.0.9-1`, SHA-256 `d9c6cb6116d5caa1174a289ecd7d3cdd463ccef6e8db1249ab0bcfcd8c935870`
- Steam 'n' Rails embedded `SNR.FLY-STABLE-1.2.2+fabric-mc26.2`, SHA-256 `33c87d5a7da0d468d3b6c0e99f726b835c63b693e7447fdaeca5e1f204caab84`
- Copycats embedded `3.0.7-createfly+mc.26.2-v1.14`, SHA-256 `1922db10a49dfab42c4c272fbaee41cdc149287cd08ca84148b497e598029858`
- Exact dependency bytes and metadata rules are locked by `BASELINE_LOCK.json`; filenames are not authoritative when embedded metadata/hash disagree.

## Project state

- project_state: `P1_SOURCE_API_ADAPTATION_IN_PROGRESS`
- active_blocker: `MINECRAFT_26_2_SOURCE_API_DRIFT`
- active_proof_head: `4a657f4625f69b26b9ccef9f7235cee271325d98; VSEntityHandlerDataLoader ResourceLocation-to-Identifier proof complete and frozen`
- active_proof_run: `P0 35414238420 / job 105819598472 success; P1 35414238535 / job 105819599047 failure with targeted ResourceLocation diagnostics cleared`
- active_hypothesis: `Pinned VSGamePackets.kt contains exactly two ResourceLocation vocabulary occurrences: the import and ResourceLocation.tryParse(handler) in PacketSyncVSEntityTypes client handling. Minecraft 26.2 uses Identifier, and the already-proven VSEntityManager.getHandler boundary accepts Identifier. Replace only those two vocabulary occurrences with Identifier while deliberately leaving registry byId/pair nullability, packet registration, entity dragging/reference-frame updates, local-control checks, lerp behavior, setPos behavior inherited from upstream VS2, server/client authority, and every other networking/gameplay semantic unchanged.`
- final_ready: `false`
- user_runtime_validation: `NOT_APPLICABLE_YET`

## Proven P1 progress

Build/toolchain frozen green:
- Java 25 + Gradle 9.5.1 starts;
- Minecraft 26.x build uses `dev.architectury.loom-no-remap` without Mojang mappings/remapJar;
- Gradle 9 `archivesBaseName` removal adapted;
- old `modImplementation` / `modApi` / `modCompileOnly` configurations migrated for no-remap Loom;
- dependency resolution reaches real `:common:compileKotlin`;
- explicit source overlays are fail-closed.

Source/API clusters proven clean in exact-head runs:
- data-provider `ResourceLocation -> Identifier` plus registry-holder `location() -> identifier()`;
- `BlockStateInfoProvider.kt`, `SimpleSoundInstanceOnShip.kt`, `VSEntityManager.kt` Identifier clusters;
- `EmptyRenderer.kt` resource vocabulary and Minecraft 26.2 `EntityRenderState` generic/create-state migration, preserving no-op renderer intent;
- `ValkyrienSkiesMod.kt` resource vocabulary only; creative-tab migration remains separate;
- `EntityData.kt` non-null generic bounds;
- `NbtUtil.kt` guarded Optional numeric reads with legacy zero defaults;
- Direction unit-vector accessor migrations in `VectorConversionsMC.kt`, `ValkyrienSkies.kt`, `TestFlapBlock.kt`, `TestWingBlock.kt`, `TestThrusterBlockEntity.kt`, `EntityDragger.kt`, and `TestChairBlock.kt`;
- `TestThrusterBlock.kt` Minecraft 26.2 `neighborChanged` signature;
- `RaycastUtils.kt` floating-direction API and paired entity/location nullability expression;
- `MinecraftPlayer.kt` admin/config permission predicates;
- dynamic command permission migrations through Backend/GetAir/GetGravity/Dry/Rename/Scale/Splitting/Static/Teleport/Delete/GetShip/Remass;
- `TestHingeBlock.kt` `getShape`, `getTicker`, four onPaste `getLong` Optional unwraps, and removal hook migration;
- `TestHingeBlockEntity.kt` two load-time `getLong` Optional unwraps;
- `ShipSavedData.kt` three load-time `getByteArray` Optional unwraps preserving empty-array behavior;
- `CompatUtil.kt` `BlockPos.center`, build-height semantics, and explicit empty collision-context migrations;
- `SeamlessChunksManager.kt` packed chunk-key migration;
- `MassDatapackResolver.kt` dummy `BlockGetter.getMinY()` and eight `ResourceLocation -> Identifier` vocabulary sites;
- `DimensionParametersResolver.kt` two `ResourceLocation -> Identifier` vocabulary sites;
- `VSEntityHandlerDataLoader.kt` three `ResourceLocation -> Identifier` vocabulary sites, with typed reload-listener generic intentionally separate.

Representative remaining compiler areas from exact run `35414238535`: Create compat classpath/API drift; separate `ShipSavedData` SavedData persistence migration; deferred `VSGameUtils` resource-key/Identifier plus build-height/chunk-position APIs; `ValkyrienSkiesMod` creative-tab output API; assembly/tick/ValueInput-ValueOutput/structure processor migrations; TestChair entity-create/`moveTo`; TestHingeBlockEntity persistence; deferred nullable command/item messages; typed reload-listener generic in `DimensionParametersResolver`, `MassDatapackResolver`, and `VSEntityHandlerDataLoader`; `MassDatapackResolver` registry tag lookup; deferred keybinding category; ShipMountingEntity persistence/hurt; entity-handler rendering; `VSGamePackets` ResourceLocation vocabulary plus independent local-control/lerp/networking API drift; `EntityDragger` local-control; chunk tickets; Sable; relocation.

## Proof chain retained

- `ad922ded33ff46a3028fca1217559a60be54fad6`: `MinecraftPlayer.kt` permission predicates; P1 `35340545586`.
- `6253d38ff84785921c95c175563a5b24800979ef`: Backend permission; P1 `35342297011`; artifact `10545204522`; SHA-256 `72de18f36f7538bf818ee59f090fea3d009e7c6f4265a9f7f5261517344b4c03`.
- `b1a8d44abb54150a5b97e03677a37977702ed65e`: GetAir permission; P1 `35355388045`; artifact `10552130508`; SHA-256 `f921fc35d29e54d827fafbb5ca4c2d5664092a72579e3e394e15cede87e212b3`.
- `7700e2194f96b79db0ffc67b6b754fecd29cc04f`: GetGravity permission; P1 `35357765377`; artifact `10552603034`; SHA-256 `dfa0c9eae9e1fc118784975bcf7adcbaa0d2ddca29a4f8318b290b1f30cea877`.
- `bd796323fa1b49bd4844c0a4089edb1025ca89f9`: Dry permission; P1 `35359836381`; artifact `10554023210`; SHA-256 `54086e93046ff3e7f113d0dd80e622e7ee4b39a5ee63e5dfed836041dce35b8d`.
- `18959ca9823cd790e51580bf9911d1757890acb0`: Rename permission; P1 `35361901965`; artifact `10555046879`; SHA-256 `b7c5ee49f8049a48e81b6879a519da0724787cbdbac6012aa07c7517ab9e57be`.
- `915d88e3c64ecc49bb502c8fe849b5744d99cea4`: Scale permission; P1 `35364622301`; artifact `10554444674`; SHA-256 `a663d408b9fc0f08ed96545827b1c4e9030d83a77c79e3590798fd5f17870763`.
- `d919b45d6f35c9917c13e69c3faf8011e0057057`: Splitting permission; P1 `35366811861`; artifact `10557430465`; SHA-256 `af0a83997d92d431f31c215ba985d502fc7b35edc1ac8c7fc6f5585e84ea4d8b`.
- `e1fa31795ba5901fdde0c1238e434faf06be2f49`: Static permission; P1 `35370436174`; artifact `10558762061`; SHA-256 `958012e1dd3cdf1a8bae2d40f423061487c7e9a4b57cd0094e7ad90ebd7328a0`.
- `c75047ae1f38b92fc39a56911a967ce914952c5c`: Teleport permission; P1 `35372443583`; artifact `10559450323`; SHA-256 `5319fc6386f0a87c23893e84c26aeb871c6453ad5c3fa7374134a4cf35024faf`.
- `6a2901ccbb359d867209195c58dc652b0a39e594`: Delete permission; P1 `35375165938`; artifact `10559548159`; SHA-256 `d1ed6dd29874c3dc4c45d1e55d4042315697856e69de18b393f9e97c214666b3`.
- `3d93c0041a59c0b78adfa9e2ff313cdbbe5f74aa`: GetShip permission; P1 `35377209937`; artifact `10560773482`; SHA-256 `8697b7badb3f739a29be29be14e2b0e0373ac7b98057a7e47245d565b535ad34`.
- `6762f2022756506b282f176f4ea4a5d6b40b8ea7`: Remass permission; P0 `35379217178`; P1 `35379217305`; artifact `10561352586`; SHA-256 `4885fb7979234c4e32621cd21bfc83f21d14f6b8128c7c5b76b59338de396dd9`.
- `f86f606e2f51e42513f4ae558bb740164d3d9f23`: EntityDragger Direction; P0 `35381321480`; P1 `35381321453`; artifact `10563195663`; SHA-256 `619e4759fee46606f2a93e94e8b42cbd463b27110e46e8590ae98e861fe70ffa`.
- `369d042ee7d86c109825ae00b637c1230a70e7e5`: TestChair Direction; P0 `35383401723`; P1 `35383401868`; job `105724661254`; artifact `10562768230`; SHA-256 `4f3ad14af6cf671d9c5f43a3e356dbd4c03dbd866f549ff6b8937d30c7cc5bc4`.
- `5a6f41ee258d704fdb91fa9b115854c19623a7eb`: EmptyRenderer Identifier; P0 `35384633799`; P1 `35384633761`; job `105728547942`; artifact `10563931126`; SHA-256 `ec45c981a8589ae3a93a3e0955cff789172c487472598bd4a5803294d98475ae`.
- `4a1ea3c136ab6640c51405129e5286896e00b483`: ValkyrienSkiesMod Identifier; P0 `35388500261`; P1 `35388500277`; job `105741071163`; artifact `10564054948`; SHA-256 `2d6ebab805f74338db600dd94870753c5f11f2d75bf502827aad0c8056091685`.
- `01e86b1dba7f483a6f8363f22e72100a61b887a8`: TestHinge getShape; P0 `35392499266`; P1 `35392499337`; job `105753820631`; artifact `10567085228`; SHA-256 `b0022b364c646cf3c65df478a98132b09877b5758768ac9d04abe9721b067f56`.
- `a4bb9db1749b0cd79e23e2f90cbfbad95202f46d`: TestHinge getTicker bound; P0 `35395323531`; P1 `35395323604`; job `105762731288`; artifact `10567955398`; SHA-256 `53b4e9a70dfac7122d5f2fe9b040fa2b3097e69f0ad8b7d3fb284e4b678b99d2`.
- `4e3dbdd2d26b1861f93f5ac651c3f8cf615ffde6`: TestHinge onPaste getLong; P0 `35396104505`; job `105765179878`; P1 `35396104498`; job `105765179621`; artifact `10567986686`; SHA-256 `4f06b192a022770df0687a244ae0db2da049c2a227dcd117202404ac440e8425`.
- `2152734918d4e4938af5aad17476f35f1ae361cf`: TestHingeBlockEntity getLong; P0 `35396770555`; job `105767287832`; P1 `35396770532`; job `105767287715`; artifact `10568142768`; SHA-256 `c677210fb53c9b716521063eb6e48d567559bb76b4154dc88d24a38aad3505d9`.
- `58e978bf8841e8bbb26e4658e9b7b566d4800e14`: TestHinge removal hook; P0 `35398688368`; job `105773330399`; P1 `35398688325`; job `105773336393`; artifact `10570252019`; SHA-256 `9ec5ff7f63122b365dfa8460e176dfbcd4be0d86235fa35b9fe803e9959a2f58`.
- `262f6140ea3f94239d47541d46c694b8b076444e`: ShipSavedData byte-array Optional; P0 `35400474206`; job `105778970673`; P1 `35400474672`; job `105778971617`; artifact `10571260073`; SHA-256 `9c118a71c2a9c207110fd7e6fe85bef7f11f56ee12aa1d5fac72e6d38f9e404d`.
- `108dd78c09e76a147020c637b80ba915d7716935`: CompatUtil BlockPos center; P0 `35402468337`; job `105785129691`; P1 `35402468328`; job `105785129719`; artifact `10571277244`; SHA-256 `2bf8a56926f2363d766119988c6eec2f8c03743806b03e77efb769fa1daa32a9`.
- `b544a504d4b9fe82b0bddfde113f6b386e295f71`: CompatUtil build-height semantics; P0 `35405820754`; job `105795255194`; P1 `35405820745`; job `105795253518`; artifact `10572194074`; SHA-256 `ecbbfd86b28720dcd1b397ad57807eb3f3a6aec026b7099983be704b4db5d53b`.
- `d2cd775048bb9620bde6b3f524451cea8bf1dab6`: CompatUtil explicit empty collision-context; P0 `35406397283`; job `105796934724`; P1 `35406397269`; job `105796934449`; artifact `10572521917`; SHA-256 `6ec56046e2163a36044250441a823ac6d56fbbd7e6874279ca92a958d2a88238`.
- `869322d6d1dc040e9b72782844c1662fb9cc8fea`: EmptyRenderer render-state; P0 `35407775818`; job `105800997900`; P1 `35407775628`; job `105800997361`; artifact `10572987722`; SHA-256 `c246e0e9438526069582f39474d11b1c4728063bcf84e155e7019203fc7b3960`.
- `75a434c728f1ca020b550882967085ccc53d5c3b`: SeamlessChunksManager ChunkPos packed-key API; P0 `35409275352`; job `105805422622`; P1 `35409275363`; job `105805423593`; artifact `10574055235`; SHA-256 `cb032a68942404c798debc540ad7b387c1f06ac41d6854f570aa43e70894a9b6`.
- `563cbcba7bb1c92ca27820ef785d11bb88872524`: MassDatapackResolver dummy BlockGetter minY; P0 `35410678210`; job `105809557245`; P1 `35410678254`; job `105809557590`; artifact `10573811879`; SHA-256 `ef0e33b2db1cff60f1e1d14658cbb9d50523309a227806cf3f09776fd23df3f2`.
- `a40316e93a61594018fd6f8f9d4b913d7fb2eb80`: MassDatapackResolver ResourceLocation-to-Identifier vocabulary; P0 `35411562202`; job `105812049740`; P1 `35411562107`; job `105812049438`; artifact `10574698116`; SHA-256 `41dc8482808a7de1a46bf4f680c00560ae085a267118e3a9dddec1f5997d2506`.
- `19d15fccf7345fc80f91800356a105d3595db87c`: DimensionParametersResolver ResourceLocation-to-Identifier vocabulary; P0 `35413012083`; job `105816180721`; P1 `35413012178`; job `105816181236`; artifact `10574836065`; SHA-256 `ca585a823377e4752017103a7acbe30be1078035c084dd28a758496659f14b95`.
- `4a657f4625f69b26b9ccef9f7235cee271325d98`: VSEntityHandlerDataLoader ResourceLocation-to-Identifier vocabulary; P0 `35414238420`; job `105819598472`; P1 `35414238535`; job `105819599047`; artifact `10575555973`; SHA-256 `b980ea48f7b71f3ec9d79e119ff83d567fbaf16973871cb547570ae23bc83159`.

## Deferred / boundary locks

Do not collapse these broader boundaries into compile-only edits:
- `ShipSavedData.save`: Minecraft 26.2 SavedData persistence is broader than a signature-only edit and must reconcile SavedDataType/codec/factory semantics.
- `VSGameUtils.kt`: resource-key migration crosses `ResourceKeyAccessor` and `MixinLevel`; do not apply a partial one-file ResourceLocation replacement. Build-height and chunk-position API drift is also present.
- `VSKeyBindings.kt`: `KeyMapping.Category` migration changes category translation-key behavior; do not silently drop `category.valkyrienskies.driving`.
- Nullable ship slug/name command/item messages: do not invent fallback values merely to satisfy Kotlin vararg nullability.
- Typed `SimpleJsonResourceReloadListener<T>` migration is separate from already-frozen Identifier vocabulary proofs and must preserve parser/apply semantics.

## Sable contract

A previous hypothesis that no VS2 source imported Sable was disproven. `common/src/main/kotlin/org/valkyrienskies/mod/compat/SableCompat.kt` is real upstream VS2 code and uses Sable companion state for entity-dragging/reference behavior.

The current build overlay's omission of an unavailable pinned Sable artifact is temporary compile-probe scaffolding only. Final architecture must resolve Sable through a traceable compatible dependency/API path or an explicitly documented minimal compatibility shim into existing VS2 architecture. Deleting or replacing VS2 entity-dragging semantics is forbidden.

## Mandatory architecture

Final behavior must remain based on real upstream VS2 machinery for ship lifecycle/ship-space, transforms, physics-core integration, collision integration, entity dragging/reference-frame behavior, player/body/camera integration, networking/synchronization, and rendering.

Forbidden final substitutes: custom VS2-style reference frames, synthetic carry velocity/inertia, fake gravity, manual floor/wall/ceiling clamps, per-tick teleport/setPos chase, camera counter-rotation/forcing, duplicate authority, floor-only success, and the retired `VS2-Create_Interactive` workaround chain.

## Milestones

### P0 — Upstream import + provenance
Frozen green. Exact upstream identity/pin/license/provenance is established and repeatedly re-confirmed. Latest proven implementation HEAD `4a657f4625f69b26b9ccef9f7235cee271325d98` has exact-head P0 run `35414238420` / job `105819598472` success.

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
- camera forcing/counter-rotation;
- per-tick teleport/reanchor chase as a substitute for VS2 moving-space semantics;
- retired project gameplay patches;
- fixture/input mutations solely to manufacture green;
- compile-only `VSKeyBindings` category replacement that changes/drops existing translation behavior;
- invented fallback values for nullable ship slug/name just to satisfy Kotlin vararg nullability;
- partial `VSGameUtils` ResourceLocation replacement without reconciling the `ResourceKeyAccessor`/`MixinLevel` boundary;
- treating `ShipSavedData.save` as a signature-only `ValueOutput` migration without reconciling the Minecraft 26.2 SavedDataType/codec/factory persistence path;
- substituting CompatUtil old exclusive `maxBuildHeight` directly with current inclusive `getMaxY()`.

## next_safe_action

1. Preserve exact `VSEntityHandlerDataLoader.kt` Identifier-vocabulary proof HEAD `4a657f4625f69b26b9ccef9f7235cee271325d98`, P0 `35414238420` / job `105819598472`, P1 `35414238535` / job `105819599047`, artifact `10575555973`, ZIP SHA-256 `b980ea48f7b71f3ec9d79e119ff83d567fbaf16973871cb547570ae23bc83159`.
2. Before source mutation, require the exact-head P0 provenance run for this ledger commit to complete successfully.
3. Add one fail-closed overlay for pinned `common/src/main/kotlin/org/valkyrienskies/mod/common/networking/VSGamePackets.kt` (pinned blob `97c01c038edf1083bf86e5f46afebccce3531e50`) that replaces exactly its two `ResourceLocation` vocabulary occurrences with `Identifier`: the import and `ResourceLocation.tryParse(handler)`. Fail closed if the pinned count differs or `Identifier` is already present before this overlay.
4. Wire only that overlay into P1 after all currently frozen overlays and add `VSGamePackets.kt` to the explicit port-delta display. Do not change `BuiltInRegistries.ENTITY_TYPE.byId`, `VSEntityManager.pair` nullability, packet registration, entity dragging/reference-space state, local-control checks, lerp/setPos behavior, client/server authority, Create/SNR/Copycats, or unrelated files.
5. Proof target: the unresolved `ResourceLocation` import/reference diagnostics in `VSGamePackets.kt` disappear. Independent `pair`/nullability inference, `isControlledByLocalInstance`, `lerpTo`, and other networking diagnostics may remain; overall compile may remain red.
6. After proof completes, record exact HEAD, P0/P1 run/job/artifact/hash and targeted diagnostic result before selecting another cluster.
7. Stay in standalone P1. Do not integrate Create/SNR/Copycats yet. No video is authorized during compile/API-port work.

## Video validation

No video is authorized during compile/API-port debugging. Video is closure-only for a user-visible runtime blocker already closure-ready from runtime/data proof. A media failure permits at most one media-only repair and never gameplay changes. Visible failure overrides telemetry green. If a separate closure review turn is needed, emit the required `VIDEO_REVIEW_REQUIRED` line and HOLD; do not use `BLOCKED_USER` for video.

## Final gate

`FINAL_READY` is forbidden until the exact final source/build and JAR SHA-256 are recorded and the user tests and accepts that exact JAR in the real Minecraft setup. CI alone cannot satisfy the final gate.