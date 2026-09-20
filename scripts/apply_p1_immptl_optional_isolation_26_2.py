#!/usr/bin/env python3
"""Isolate pinned optional Immersive Portals 1.21.1 compat from standalone P1 MC 26.2.

The exact upstream VS2 pin compiles three optional Immersive Portals mixins against
ImmersivePortalsMod v6.0.6-mc1.21.1. On the loom-no-remap Minecraft 26.2 path that
old external jar exposes stale Minecraft descriptors (currently net.minecraft.class_5321),
so P1 must not force that unrelated optional integration into the standalone real-VS2
boot gate. Keep the upstream submodule untouched; remove only the copied-worktree
compile-only dependency, source package, and matching mixin registrations.
"""
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
gradle_path = root / "common/build.gradle"
mixins_path = root / "common/src/main/resources/valkyrienskies-common.mixins.json"
ip_dir = root / "common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/immersive_portals"

for path in (gradle_path, mixins_path, ip_dir):
    if not path.exists():
        raise SystemExit(f"fail-closed: pinned Immersive Portals isolation anchor missing: {path}")

expected_java = {
    "MixinImmPtlChunkTracking.java",
    "MixinMyBuiltChunkStorage.java",
    "MixinVisibleSectionDiscovery.java",
}
actual_java = {path.name for path in ip_dir.glob("*.java")}
if actual_java != expected_java:
    raise SystemExit(
        "fail-closed: pinned Immersive Portals source surface changed: "
        f"actual={sorted(actual_java)} expected={sorted(expected_java)}"
    )

gradle = gradle_path.read_text(encoding="utf-8")
dependency = '    compileOnly("com.github.iPortalTeam:ImmersivePortalsMod:${immptl_version}")\n'
exclude_anchor = '            exclude "org/valkyrienskies/mod/mixin/mod_compat/etf/**"\n'
exclude_line = '            exclude "org/valkyrienskies/mod/mixin/mod_compat/immersive_portals/**"\n'

if gradle.count(dependency) != 1:
    raise SystemExit(
        f"fail-closed: expected one transformed Immersive Portals compileOnly dependency; found {gradle.count(dependency)}"
    )
if gradle.count(exclude_anchor) != 1:
    raise SystemExit(
        f"fail-closed: expected one P1 ETF exclusion anchor; found {gradle.count(exclude_anchor)}"
    )
if exclude_line in gradle:
    raise SystemExit("fail-closed: Immersive Portals source exclusion already present")

gradle = gradle.replace(dependency, "", 1)
gradle = gradle.replace(exclude_anchor, exclude_anchor + exclude_line, 1)
if dependency in gradle or gradle.count(exclude_line) != 1:
    raise SystemExit("fail-closed: Immersive Portals Gradle isolation postcondition failed")
gradle_path.write_text(gradle, encoding="utf-8")

mixins = mixins_path.read_text(encoding="utf-8")
entries = (
    '    "mod_compat.immersive_portals.MixinImmPtlChunkTracking",\n',
    '    "mod_compat.immersive_portals.MixinMyBuiltChunkStorage",\n',
    '    "mod_compat.immersive_portals.MixinVisibleSectionDiscovery",\n',
)
for entry in entries:
    count = mixins.count(entry)
    if count != 1:
        raise SystemExit(
            f"fail-closed: expected one Immersive Portals mixin registration {entry.strip()!r}; found {count}"
        )
    mixins = mixins.replace(entry, "", 1)

if "mod_compat.immersive_portals." in mixins:
    raise SystemExit("fail-closed: stale Immersive Portals mixin registration remained")
mixins_path.write_text(mixins, encoding="utf-8")

print(
    "P1_IMMPTL_OPTIONAL_ISOLATION_26_2_APPLIED "
    "dependency=removed javaMixins=3 mixinRegistrations=3 upstream=untouched"
)

# Transport-only chaining. The optional Immersive Portals isolation is complete before
# entering the newly exposed Fabric Kotlin compile frontier; keep the Fabric data-component
# Identifier migration isolated in its own fail-closed helper.
vsdatacomponents_identifier_helper = Path(__file__).with_name("apply_p1_vsdatacomponents_identifier_26_2.py")
if not vsdatacomponents_identifier_helper.is_file():
    raise SystemExit(
        f"fail-closed: required Fabric VSDataComponents Identifier helper missing: {vsdatacomponents_identifier_helper}"
    )
subprocess.run([sys.executable, str(vsdatacomponents_identifier_helper), str(root)], check=True)
print("P1_VSDATACOMPONENTS_IDENTIFIER_26_2_CHAINED")
