#!/usr/bin/env python3
"""Fail-closed isolation of legacy optional Sable mixins from standalone VS2 P1.

Pinned upstream VS2 2.4.12 compiles its legacy Sable integration against
`dev.ryanhcode.sable:sable-core` as `modCompileOnly`. The locked Minecraft 26.2
standalone P1 baseline intentionally does not provide that legacy 1.21.1 Sable
runtime. These two Java mixins are therefore optional compatibility sources,
not standalone VS2 core authority.

This overlay removes only the two exact pinned legacy Sable source files and
the one exact common-mixin registration that exists for ActiveSableCompanion.
It adds no stub classes, runtime dependency, substitute behavior, ship-space
logic, movement/collision authority, or gameplay implementation. Exact Sable /
Create-family integration belongs to the later locked integration milestones.
"""

from pathlib import Path
import hashlib
import sys

ACTIVE = Path("common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/sable/MixinActiveSableCompanion.java")
HOLDING = Path("common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/sable/MixinSubLevelHoldingChunkMap.java")
COMMON_MIXINS = Path("common/src/main/resources/valkyrienskies-common.mixins.json")
FABRIC_MIXINS = Path("fabric/src/main/resources/valkyrienskies-fabric.mixins.json")
FORGE_MIXINS = Path("forge/src/main/resources/valkyrienskies-forge.mixins.json")

# Exact git-blob identities at upstream pin f39132148e717d325933b4ce6e9e9fb13d929390.
ACTIVE_BLOB = "7e60769a28964b165c4b7d772507ec7cf864fd8c"
HOLDING_BLOB = "27b6f13752629caa0631436f264757eb953923e5"
ACTIVE_ENTRY = '    "mod_compat.sable.MixinActiveSableCompanion",\n'


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def verify_source(path: Path, expected_blob: str, anchors: tuple[str, ...]) -> None:
    if not path.is_file():
        raise SystemExit(f"fail-closed: expected pinned Sable source missing: {path}")
    data = path.read_bytes()
    actual_blob = git_blob_sha1(data)
    if actual_blob != expected_blob:
        raise SystemExit(
            f"fail-closed: unexpected pinned Sable source identity for {path}: {actual_blob} != {expected_blob}"
        )
    text = data.decode("utf-8")
    for anchor in anchors:
        if text.count(anchor) != 1:
            raise SystemExit(
                f"fail-closed: expected exactly one Sable semantic anchor {anchor!r} in {path}, found {text.count(anchor)}"
            )


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {sys.argv[0]} <upstream-vs2-root>")

    root = Path(sys.argv[1])
    active = root / ACTIVE
    holding = root / HOLDING
    common_path = root / COMMON_MIXINS
    fabric_path = root / FABRIC_MIXINS
    forge_path = root / FORGE_MIXINS

    verify_source(
        active,
        ACTIVE_BLOB,
        (
            "dev.ryanhcode.sable.ActiveSableCompanion",
            "@Mixin(ActiveSableCompanion.class)",
            "projectOutOfSubLevel(Lnet/minecraft/world/level/Level;Lorg/joml/Vector3dc;Lorg/joml/Vector3d;)Lorg/joml/Vector3d;",
            "getVelocity(Lnet/minecraft/world/level/Level;Lorg/joml/Vector3dc;Lorg/joml/Vector3d;)Lorg/joml/Vector3d;",
        ),
    )
    verify_source(
        holding,
        HOLDING_BLOB,
        (
            "dev.ryanhcode.sable.sublevel.storage.holding.SubLevelHoldingChunkMap",
            "@Mixin(SubLevelHoldingChunkMap.class)",
            'method = "updateChunkStatus"',
            "VSGameUtilsKt.isChunkInShipyard",
        ),
    )

    configs = {}
    for path in (common_path, fabric_path, forge_path):
        if not path.is_file():
            raise SystemExit(f"fail-closed: expected pinned mixin config missing: {path}")
        configs[path] = path.read_text(encoding="utf-8")

    common = configs[common_path]
    if common.count(ACTIVE_ENTRY) != 1:
        raise SystemExit(
            f"fail-closed: expected exactly one ActiveSableCompanion common registration, found {common.count(ACTIVE_ENTRY)}"
        )
    if "MixinSubLevelHoldingChunkMap" in common:
        raise SystemExit("fail-closed: unexpected HoldingChunkMap registration in common mixin config")
    for path in (fabric_path, forge_path):
        text = configs[path]
        if "MixinActiveSableCompanion" in text or "MixinSubLevelHoldingChunkMap" in text:
            raise SystemExit(f"fail-closed: unexpected legacy Sable registration outside common config: {path}")

    common = common.replace(ACTIVE_ENTRY, "", 1)
    if "MixinActiveSableCompanion" in common or "MixinSubLevelHoldingChunkMap" in common:
        raise SystemExit("fail-closed: legacy Sable mixin registration remains after isolation")

    common_path.write_text(common, encoding="utf-8")
    active.unlink()
    holding.unlink()

    if active.exists() or holding.exists():
        raise SystemExit("fail-closed: legacy Sable source isolation did not converge")

    print("P1_LEGACY_SABLE_COMPILEONLY_ISOLATION_26_2_APPLIED")


if __name__ == "__main__":
    main()
