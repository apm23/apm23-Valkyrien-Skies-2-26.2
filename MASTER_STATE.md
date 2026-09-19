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

## Current reconciliation — VSKeyBindings KeyMapping.Category migration proven

- Current proven implementation HEAD: `2c763500338955135d0700b273594a87dab9d982` (`P1: normalize touched keybinding locale lines`).
- Exact-head P0 provenance run `35424232816`, job `105847304720`, completed `success` and re-confirmed the pinned upstream VS2 identity.
- Exact-head P1 standalone compile run `35424232856`, job `105847304996`, completed `failure` only because independent remaining Minecraft 26.2 source/API errors remain.
- All traceable overlays applied successfully; explicit `git diff --check` / port-delta validation and Gradle runtime steps succeeded; compilation reached the real `:common:compileKotlin` boundary.
- The isolated Minecraft 26.2 keybinding adaptation changes only the category representation required by current vanilla: one shared category is registered as `KeyMapping.Category.register(Identifier.fromNamespaceAndPath("valkyrienskies", "driving"))`; the existing `shipDown` and `shipCruise` key mappings retain their names, default keys, registration flow, and shared category semantics.
- Minecraft 26.2 derives the category translation key as `key.category.valkyrienskies.driving`. To preserve the upstream VS2 user-visible category text, `apply_p1_vskeybindings_category_26_2.py` keeps the legacy `category.valkyrienskies.driving` entry and adds `key.category.valkyrienskies.driving` with the **exact same localized value** in every upstream locale that carried the legacy entry: `ar_sa`, `en_pt`, `en_us`, `es_es`, `fi_fi`, `fr_fr`, `hi_in`, `ja_jp`, `ko_kr`, `pl_pl`, `ru_ru`, `sv_se`, `tr_tr`, `zh_cn`.
- Locale mutation is fail-closed. Untouched locale bytes are preserved; only the two touched category lines are emitted with clean LF endings where needed so Git's whitespace checker does not reject CRLF on newly changed lines. The JSON is re-parsed and exact old/new translation-value equality is asserted before the overlay succeeds.
- Exact run `35424232856` contains **no compiler diagnostic for `VSKeyBindings.kt`**. The prior `String` versus `KeyMapping.Category` type-mismatch diagnostic is cleared with no replacement diagnostic in that file.
- Diagnostic artifact: `p1-compile-log-2c763500338955135d0700b273594a87dab9d982`, artifact ID `10578617703`, size `6291` bytes, ZIP SHA-256 `c9e0d1f2f1e18390794ee14f41493e133d2d174c4e0fa58463c2381983013bb1`.
- Failed partial probes within this same hypothesis are retained as negative evidence: `e108526cbd728454c175c76bffc610d4e074da49` incorrectly assumed every legacy locale entry had a following JSON entry/comma; `fcc65187d79c4b546883875da3597345db1e01cd` used a whitespace regex that could span line boundaries; `e9a3efd58acb2af9539628eb2875e6cb829c3cec` used text I/O that normalized unrelated CRLF; `fb3c7e65a4c2089f6fa695114734d14836bde1d3` byte-preserved files but still emitted CRLF on touched lines, which `git diff --check` rejected as trailing whitespace. None reached a false compiler proof.
- No networking, entity dragging/reference-space behavior, local-control authority, interpolation, ship lifecycle, collision, physics, player/camera behavior, rendering, persistence, or unrelated gameplay semantics were changed by this proof.
- No code from retired `apm23/VS2-Create_Interactive` has been imported or reused as implementation source.

### Immediately prior frozen proofs

- `5c8a80eca1b996c4b89d5a394d7cfb9115d3f070`: `ValkyrienSkiesMod` `CreativeModeTab.Output` accessibility via one common access-widener line mirroring Fabric 26.2's explicit transitive-access contract, with creative-tab source behavior unchanged; P0 `35423048611` / job `105844091418`; P1 `35423048671` / job `105844092374`; artifact `10578021452`; SHA-256 `f5691678a8ebdd7967c193846b906b8114fa4bacd9068836f061d83a9bb0cd1b`.
- `4641ae31765f0d067923cc1ef54b9a26abe99a19`: TestHingeBlockEntity `ValueInput` / `ValueOutput` persistence boundary preserving the flat key schema and hinge joint-load semantics; P0 `35421661792` / job `105840387680`; P1 `35421661791` / job `105840387789`; artifact `10577638892`; SHA-256 `a6b44f7d7248a9364dc31f1ddc9231ffa45212a895f10db752be4b432deae47a`.
- `ea2084954eb4edd2bd9922aa1f59342b76709809`: MassDatapackResolver registry-tag lookup `getTag(TagKey) -> get(TagKey)` with deferred tag semantics preserved; P0 `35420504812` / job `105837166152`; P1 `35420504781` / job `105837162566`; artifact `10577252400`; SHA-256 `d0dab3e4652c4d00f62f1c9aeccaae98c8a1401e8651e86bd9de7aa12d2f28ac`.
- `27e181c70184b2aac38eeb1a646905d93ba45023`: MassDatapackResolver typed reload-listener constructor/generic/apply boundary; P0 `35419426729` / job `105834163091`; P1 `35419426780` / job `105834163164`; artifact `10577550502`; SHA-256 `cf373d90a2b42bc5bc92866fe39d97a43ce6ae6e7deb4fd3f2f37d307719fd57`.
- `ac739bbf0c1598087a6ae9b158117c4764ce3079`: DimensionParametersResolver typed reload-listener boundary; P0 `35418630206` / job `105831997380`; P1 `35418630221` / job `105831997436`; artifact `10576109658`; SHA-256 `58f0e1a82a74ebc096c610a8d98dd51efc56c1e9248a79e446517cdb7f30ea97`.
- `2af9d9ba1d48f8a0baf825398d3d441b1219f19d`: VSEntityHandlerDataLoader typed reload-listener boundary; P0 `35417874772` / job `105829899174`; P1 `35417874723` / job `105829899066`; artifact `10575914762`; SHA-256 `51518277e80d405539aba99f690b27bfe4883be95d929b489b9d97a98cc8e7f3`.
- `9d82234aa769a6a0eece07f52e7d5ace2d334aab`: VSGamePackets Identifier-vocabulary proof; P0 `35415473227` / job `105823166889`; P1 `35415473246` / job `105823166851`; artifact `10575144592`; SHA-256 `0aae19b487b1088166b7ea1e8e72e4cb30ad3101c8c6e88c5620c797d9dd8ab1`.
- `4a657f4625f69b26b9ccef9f7235cee271325d98`: VSEntityHandlerDataLoader Identifier proof; P0 `35414238420` / job `105819598472`; P1 `35414238535` / job `105819599047`; artifact `10575555973`; SHA-256 `b980ea48f7b71f3ec9d79e119ff83d567fbaf16973871cb547570ae23bc83159`.
- `19d15fccf7345fc80f91800356a105d3595db87c`: DimensionParametersResolver Identifier proof; P0 `35413012083` / job `105816180721`; P1 `35413012178` / job `105816181236`; artifact `10574836065`; SHA-256 `ca585a823377e4752017103a7acbe30be1078035c084dd28a758496659f14b95`.
- `a40316e93a61594018fd6f8f9d4b913d7fb2eb80`: MassDatapackResolver Identifier proof; P0 `35411562202` / job `105812049740`; P1 `35411562107` / job `105812049438`; artifact `10574698116`; SHA-256 `41dc8482808a7de1a46bf4f680c00560ae085a267118e3a9dddec1f5997d2506`.
- `563cbcba7bb1c92ca27820ef785d11bb88872524`: MassDatapackResolver dummy BlockGetter minY proof; P0 `35410678210` / job `105809557245`; P1 `35410678254` / job `105809557590`; artifact `10573811879`; SHA-256 `ef0e33b2db1cff60f1e1d14658cbb9d50523309a227806cf3f09776fd23df3f2`.
- `75a434c728f1ca020b550882967085ccc53d5c3b`: SeamlessChunksManager ChunkPos packed-key proof; P0 `35409275352` / job `105805422622`; P1 `35409275363` / job `105805423593`; artifact `10574055235`; SHA-256 `cb032a68942404c798debc540ad7b387c1f06ac41d6854f570aa43e70894a9b6`.

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
- active_proof_head: `2c763500338955135d0700b273594a87dab9d982; VSKeyBindings KeyMapping.Category + localized translation bridge proof complete and frozen`
- active_proof_run: `P0 35424232816 / job 105847304720 success; P1 35424232856 / job 105847304996 failure with all VSKeyBindings diagnostics cleared`
- active_hypothesis: `none selected yet; inspect the exact Minecraft 26.2 API boundary for one isolated remaining compiler cluster before source mutation. Preserve the ShipSavedData lifecycle/factory boundary, ShipMountingEntity entity persistence/hurt boundary, assembly/relocation component semantics, authority-sensitive VSGamePackets/EntityDragger local-control and lerp boundary, VSGameUtils resource/mixin boundary, nullable message semantics, rendering, ticketing, Sable, Create-compat classpath boundary, and all other deferred locks. Do not reinterpret the proven keybinding translation bridge as authorization to drop legacy localization or change input behavior.`
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

Source/API clusters proven clean in exact-head runs include:
- data-provider `ResourceLocation -> Identifier` and registry-holder identifier migrations;
- `BlockStateInfoProvider`, `SimpleSoundInstanceOnShip`, `VSEntityManager`, `DimensionParametersResolver`, `MassDatapackResolver`, `VSEntityHandlerDataLoader`, and the isolated `VSGamePackets` resource-vocabulary sites;
- `EntityData` non-null generic bounds and guarded Optional numeric/NBT reads;
- Direction accessor migrations in the previously frozen vector/block/entity sites;
- `TestThrusterBlock` neighborChanged signature; `RaycastUtils` floating-direction/nullability boundary;
- Minecraft player and dynamic command permission migrations;
- `TestHingeBlock` shape/ticker/onPaste/removal migrations;
- `TestHingeBlockEntity` load reads plus exact `ValueInput`/`ValueOutput` flat persistence schema;
- `ShipSavedData` load-time byte-array Optional unwraps only; its broader SavedData save/factory lifecycle remains deferred;
- `CompatUtil` center/build-height/collision-context migrations;
- `SeamlessChunksManager` packed chunk-key migration;
- typed raw-JSON reload listeners for VSEntityHandlerDataLoader, DimensionParametersResolver, and MassDatapackResolver;
- MassDatapackResolver registry-tag lookup through current `Registry.get(TagKey)` while preserving deferred tag semantics;
- `EmptyRenderer` Identifier + render-state migration;
- `ValkyrienSkiesMod` resource vocabulary plus exact `CreativeModeTab.Output` accessibility contract, with upstream creative-tab item population unchanged;
- `VSKeyBindings` current `KeyMapping.Category` migration using registered `valkyrienskies:driving`, with new generated translation key bridged to the exact upstream localized category values while retaining the legacy translation entries.

Representative remaining compiler areas from exact run `35424232856`: Create compat classpath/intermediary/API drift; separate `ShipSavedData` SavedData persistence migration; deferred `VSGameUtils` resource-key/Identifier plus build-height/chunk-position APIs; assembly/tick/ValueInput-ValueOutput/structure processor migrations; TestChair entity-create/`moveTo`; deferred nullable command/item messages; ShipMountingEntity persistence/hurt; entity-handler rendering; VSGamePackets/EntityDragger local-control and VSGamePackets lerp API drift; chunk tickets/VSTicketType; Sable; relocation. `VSKeyBindings`, `ValkyrienSkiesMod`, `TestHingeBlockEntity`, and `MassDatapackResolver` have no remaining compiler diagnostic in this run.

## Earlier proof chain retained

The following exact-head proofs remain frozen and must not be mechanically redone: `ad922ded33ff46a3028fca1217559a60be54fad6` MinecraftPlayer permissions; `6253d38ff84785921c95c175563a5b24800979ef` Backend permission; `b1a8d44abb54150a5b97e03677a37977702ed65e` GetAir; `7700e2194f96b79db0ffc67b6b754fecd29cc04f` GetGravity; `bd796323fa1b49bd4844c0a4089edb1025ca89f9` Dry; `18959ca9823cd790e51580bf9911d1757890acb0` Rename; `915d88e3c64ecc49bb502c8fe849b5744d99cea4` Scale; `d919b45d6f35c9917c13e69c3faf8011e0057057` Splitting; `e1fa31795ba5901fdde0c1238e434faf06be2f49` Static; `c75047ae1f38b92fc39a56911a967ce914952c5c` Teleport; `6a2901ccbb359d867209195c58dc652b0a39e594` Delete; `3d93c0041a59c0b78adfa9e2ff313cdbbe5f74aa` GetShip; `6762f2022756506b282f176f4ea4a5d6b40b8ea7` Remass; `f86f606e2f51e42513f4ae558bb740164d3d9f23` EntityDragger Direction; `369d042ee7d86c109825ae00b637c1230a70e7e5` TestChair Direction; `5a6f41ee258d704fdb91fa9b115854c19623a7eb` EmptyRenderer Identifier; `4a1ea3c136ab6640c51405129e5286896e00b483` ValkyrienSkiesMod Identifier; `01e86b1dba7f483a6f8363f22e72100a61b887a8` TestHinge shape; `a4bb9db1749b0cd79e23e2f90cbfbad95202f46d` TestHinge ticker bound; `4e3dbdd2d26b1861f93f5ac651c3f8cf615ffde6` TestHinge onPaste Optional; `2152734918d4e4938af5aad17476f35f1ae361cf` TestHingeBlockEntity Optional; `58e978bf8841e8bbb26e4658e9b7b566d4800e14` TestHinge removal hook; `262f6140ea3f94239d47541d46c694b8b076444e` ShipSavedData byte-array Optional; `108dd78c09e76a147020c637b80ba915d7716935` CompatUtil center; `b544a504d4b9fe82b0bddfde113f6b386e295f71` CompatUtil build height; `d2cd775048bb9620bde6b3f524451cea8bf1dab6` CompatUtil collision context; `869322d6d1dc040e9b72782844c1662fb9cc8fea` EmptyRenderer render state; and the detailed recent proof hashes listed above.

## Deferred / boundary locks

Do not collapse these broader boundaries into compile-only edits:
- `ShipSavedData.save`: Minecraft 26.2 SavedData persistence is broader than a signature-only edit and must reconcile SavedDataType/codec/factory semantics.
- `VSGameUtils.kt`: resource-key migration crosses `ResourceKeyAccessor` and `MixinLevel`; do not apply a partial one-file ResourceLocation replacement. Build-height and chunk-position API drift is also present.
- `VSKeyBindings.kt` is now frozen green independently: current category `Identifier` is `valkyrienskies:driving`, vanilla derives `key.category.valkyrienskies.driving`, and the overlay bridges that generated key to the exact existing localized values while retaining `category.valkyrienskies.driving`. Do not remove the bridge or change default key/input behavior without separate evidence.
- Nullable ship slug/name command/item messages: do not invent fallback values merely to satisfy Kotlin vararg nullability.
- Typed `SimpleJsonResourceReloadListener<T>` migration is frozen green independently for `VSEntityHandlerDataLoader`, `DimensionParametersResolver`, and `MassDatapackResolver`.
- `MassDatapackResolver` registry-tag lookup is frozen green independently: the 26.2 `Registry.get(TagKey)` path is proven while preserving upstream deferred `tagsAreLoaded`, Optional/HolderSet, missing-tag, priority/application, and registration semantics.
- `TestHingeBlockEntity` persistence proves only that block entity's exact flat-key `ValueInput`/`ValueOutput` boundary. It does **not** authorize mechanical migration of `ShipSavedData`, `ShipMountingEntity`, `AssemblyUtil`, `ShipAssembler`, or `RelocationUtil`.
- `ValkyrienSkiesMod` creative-tab access mirrors the explicit Fabric 26.2 `CreativeModeTab$Output` transitive-access contract only. Do not broadly widen unrelated Minecraft classes or rewrite upstream creative-tab population without separate evidence.
- `VSGamePackets.kt` / `EntityDragger.kt` local-control and lerp API drift is authority-sensitive; do not replace removed vanilla APIs with synthetic carry, custom authority, teleport chase, or invented client-control semantics.

## Sable contract

A previous hypothesis that no VS2 source imported Sable was disproven. `common/src/main/kotlin/org/valkyrienskies/mod/compat/SableCompat.kt` is real upstream VS2 code and uses Sable companion state for entity-dragging/reference behavior.

The current build overlay's omission of an unavailable pinned Sable artifact is temporary compile-probe scaffolding only. Final architecture must resolve Sable through a traceable compatible dependency/API path or an explicitly documented minimal compatibility shim into existing VS2 architecture. Deleting or replacing VS2 entity-dragging semantics is forbidden.

## Mandatory architecture

Final behavior must remain based on real upstream VS2 machinery for ship lifecycle/ship-space, transforms, physics-core integration, collision integration, entity dragging/reference-frame behavior, player/body/camera integration, networking/synchronization, and rendering.

Forbidden final substitutes: custom VS2-style reference frames, synthetic carry velocity/inertia, fake gravity, manual floor/wall/ceiling clamps, per-tick teleport/setPos chase, camera counter-rotation/forcing, duplicate authority, floor-only success, and the retired `VS2-Create_Interactive` workaround chain.

## Milestones

### P0 — Upstream import + provenance
Frozen green. Exact upstream identity/pin/license/provenance is established and repeatedly re-confirmed. Latest proven implementation HEAD `2c763500338955135d0700b273594a87dab9d982` has exact-head P0 run `35424232816` / job `105847304720` success.

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
- assuming every legacy keybinding-category locale entry has a following JSON entry/comma — disproven by exact fail-closed probe `e108526cbd728454c175c76bffc610d4e074da49`;
- using a whitespace regex or whole-file newline normalization for the keybinding localization bridge — disproven by probes `fcc65187d79c4b546883875da3597345db1e01cd` and `e9a3efd58acb2af9539628eb2875e6cb829c3cec`;
- emitting source CRLF on newly touched category lines under the repository's `git diff --check` gate — disproven by `fb3c7e65a4c2089f6fa695114734d14836bde1d3`;
- invented fallback values for nullable ship slug/name just to satisfy Kotlin vararg nullability;
- partial `VSGameUtils` ResourceLocation replacement without reconciling the `ResourceKeyAccessor`/`MixinLevel` boundary;
- treating `ShipSavedData.save` as a signature-only `ValueOutput` migration without reconciling the Minecraft 26.2 SavedDataType/codec/factory persistence path;
- substituting CompatUtil old exclusive `maxBuildHeight` directly with current inclusive `getMaxY()`;
- assuming legacy nullable `Map<Identifier?, JsonElement?>` still overrides Minecraft 26.2 typed `SimpleJsonResourceReloadListener<JsonElement>.apply`;
- assuming `MassDatapackResolver.VSMassDataLoader.apply` can be ported by making only its `objects` map non-null while leaving `ResourceManager?` / `ProfilerFiller?`;
- mechanically copying the proven `TestHingeBlockEntity` Value I/O shape into broader persistence/component/entity paths without first proving their Minecraft 26.2 lifecycle and codec/component semantics;
- treating the proven `CreativeModeTab.Output` access line as authorization for broad access widening or replacing upstream creative-tab source behavior with event-driven population without independent evidence;
- mechanically replacing removed `isControlledByLocalInstance` / `lerpTo` calls without proving the current Minecraft 26.2 authority/interpolation boundary and preserving upstream VS2 semantics.

## next_safe_action

1. Preserve exact `VSKeyBindings` category proof HEAD `2c763500338955135d0700b273594a87dab9d982`, P0 `35424232816` / job `105847304720`, P1 `35424232856` / job `105847304996`, artifact `10578617703`, ZIP SHA-256 `c9e0d1f2f1e18390794ee14f41493e133d2d174c4e0fa58463c2381983013bb1`.
2. Reconcile actual HEAD after this proof-ledger commit and require its exact-head P0 provenance run to settle successfully before any new source mutation.
3. After provenance settles, inspect only the newest exact-head compiler evidence plus the exact Minecraft 26.2 API boundary for **one** isolated remaining compiler cluster. Do not mechanically select from the locked broad persistence, VSGameUtils/mixin, authority/local-control/lerp, nullable-message, assembly/relocation, rendering, ticketing, Sable, or Create-compat boundaries.
4. Select and document exactly one next root hypothesis only after that API-boundary inspection. Preserve all frozen proofs, deferred boundaries, and failed-hypothesis locks.
5. Stay in standalone P1. Do not integrate Create/SNR/Copycats yet. No video is authorized during compile/API-port work.

## Video validation

No video is authorized during compile/API-port debugging. Video is closure-only for a user-visible runtime blocker already closure-ready from runtime/data proof. A media failure permits at most one media-only repair and never gameplay changes. Visible failure overrides telemetry green. If a separate closure review turn is needed, emit the required `VIDEO_REVIEW_REQUIRED` line and HOLD; do not use `BLOCKED_USER` for video.

## Final gate

`FINAL_READY` is forbidden until the exact final source/build and JAR SHA-256 are recorded and the user tests and accepts that exact JAR in the real Minecraft setup. CI alone cannot satisfy the final gate.
