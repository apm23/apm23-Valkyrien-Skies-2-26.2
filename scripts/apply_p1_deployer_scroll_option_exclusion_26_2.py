#!/usr/bin/env python3
"""Fail-closed standalone-P1 exclusion for one unreferenced upstream Create helper.

At the pinned VS2 baseline, DeployerScrollOptionSlot.kt is an optional Create
compatibility helper with no caller in common Java/Kotlin source and no matching
mixin registration. Its old Create/intermediary API currently blocks Minecraft
26.2 standalone compilation even though P1 must not port Create internals before
P3.

This overlay excludes only that single helper from the common Kotlin source set.
It does not modify Create APIs, VS2 ship-space/physics/collision/entity authority,
or any runtime/mixin registration.
"""

from pathlib import Path
import sys

TARGET = "org/valkyrienskies/mod/compat/create/DeployerScrollOptionSlot.kt"
SYMBOL = "DeployerScrollOptionSlot"


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {sys.argv[0]} <upstream-vs2-root>")

    root = Path(sys.argv[1])
    helper = root / "common/src/main/java" / TARGET
    build = root / "common/build.gradle"
    mixins = root / "common/src/main/resources/valkyrienskies-common.mixins.json"

    if not helper.is_file():
        raise SystemExit(f"fail-closed: pinned Create helper missing: {helper}")

    helper_text = helper.read_text(encoding="utf-8")
    if f"class {SYMBOL}(" not in helper_text:
        raise SystemExit("fail-closed: helper no longer matches pinned class declaration")
    if "DirectionalExtenderScrollOptionSlot" not in helper_text:
        raise SystemExit("fail-closed: helper no longer matches pinned Create compatibility role")

    # Prove the exact pinned common source has no caller before excluding the helper.
    references = []
    source_root = root / "common/src/main"
    for path in source_root.rglob("*"):
        if not path.is_file() or path == helper:
            continue
        if path.suffix not in {".java", ".kt"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if SYMBOL in text:
            references.append(path.relative_to(root).as_posix())
    if references:
        raise SystemExit(
            "fail-closed: DeployerScrollOptionSlot gained source references; cannot exclude: "
            + ", ".join(references)
        )

    mixin_text = mixins.read_text(encoding="utf-8")
    if SYMBOL in mixin_text or '"mod_compat.create.' in mixin_text:
        raise SystemExit("fail-closed: matching direct Create runtime/mixin registration now exists")

    text = build.read_text(encoding="utf-8")
    old = '''        kotlin {\n            exclude "org/valkyrienskies/mod/compat/hexcasting/**"\n            exclude "org/valkyrienskies/mod/compat/flywheel/**"\n'''
    new = '''        kotlin {\n            exclude "org/valkyrienskies/mod/compat/hexcasting/**"\n            exclude "org/valkyrienskies/mod/compat/flywheel/**"\n            exclude "org/valkyrienskies/mod/compat/create/DeployerScrollOptionSlot.kt"\n'''
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"fail-closed: expected exactly one common Kotlin sourceSet anchor, found {count}")
    if TARGET in text:
        raise SystemExit("fail-closed: DeployerScrollOptionSlot exclusion already present unexpectedly")

    build.write_text(text.replace(old, new, 1), encoding="utf-8")

    result = build.read_text(encoding="utf-8")
    if result.count(f'exclude "{TARGET}"') != 1:
        raise SystemExit("fail-closed: expected exactly one helper exclusion after edit")

    print("P1_DEPLOYER_SCROLL_OPTION_EXCLUSION_26_2_APPLIED")


if __name__ == "__main__":
    main()
