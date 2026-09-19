#!/usr/bin/env python3
"""Fail-closed Sable Companion compile-classpath probe for standalone VS2 P1.

The pinned VS2 tree imports dev.ryanhcode.sable.companion.SableCompanion from
SableCompat.kt, while the current P1 build baseline removes the old unresolved
`dev.ryanhcode.sable:sable-common-${minecraft_version}` compile-only coordinate.

Current official Sable Companion documents the companion API as a lightweight,
safe-default compatibility library. Its currently published/source line is for
Minecraft 1.21.1, so this overlay deliberately adds it as *compileOnly* only to
probe whether the API surface remains source-compatible with the VS2 26.2 port.
It is not bundled, not added to runtime, and does not alter SableCompat,
LoadedMods, shipyard logic, ship transforms, physics, rendering, networking,
entity dragging, camera, or gameplay authority.
"""

from pathlib import Path
import sys


COMMON_BUILD = Path("common/build.gradle")
ROOT_BUILD = Path("build.gradle")
OLD_COORD_FRAGMENT = "dev.ryanhcode.sable:sable-common-${minecraft_version}:${sable_version}"
NEW_COORD = 'compileOnly("dev.ryanhcode.sable-companion:sable-companion-common-1.21.1:1.6.0")'
ANCHOR = "    // Platform-specific compat remains under fabric/forge where available.\n"
REPO_URL = 'url = "https://maven.ryanhcode.dev/releases"'


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {sys.argv[0]} <upstream-vs2-root>")

    root = Path(sys.argv[1])
    common_path = root / COMMON_BUILD
    root_build_path = root / ROOT_BUILD

    common = common_path.read_text(encoding="utf-8")
    root_build = root_build_path.read_text(encoding="utf-8")

    if OLD_COORD_FRAGMENT in common:
        raise SystemExit(
            "fail-closed: old Sable coordinate still present; this overlay must run after the canonical P1 build baseline"
        )
    if NEW_COORD in common:
        raise SystemExit("fail-closed: Sable Companion compile-only probe coordinate already present")
    if common.count(ANCHOR) != 1:
        raise SystemExit(
            f"fail-closed: expected exactly one Sable compatibility anchor in {COMMON_BUILD}, found {common.count(ANCHOR)}"
        )
    if root_build.count(REPO_URL) != 1:
        raise SystemExit(
            f"fail-closed: expected exactly one RyanHCode Maven repository in {ROOT_BUILD}, found {root_build.count(REPO_URL)}"
        )

    common = common.replace(ANCHOR, ANCHOR + f"    {NEW_COORD}\n", 1)

    if common.count(NEW_COORD) != 1:
        raise SystemExit("fail-closed: expected exactly one Sable Companion compile-only dependency after insertion")
    if "implementation(\"dev.ryanhcode.sable-companion" in common:
        raise SystemExit("fail-closed: Sable Companion must not be promoted to runtime implementation")
    if "api(\"dev.ryanhcode.sable-companion" in common:
        raise SystemExit("fail-closed: Sable Companion probe must remain compileOnly")

    common_path.write_text(common, encoding="utf-8")
    print("P1_SABLE_COMPANION_COMPILEONLY_26_2_PROBE_APPLIED")


if __name__ == "__main__":
    main()
