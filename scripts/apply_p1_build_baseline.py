#!/usr/bin/env python3
"""Apply the minimal P1 Minecraft 26.2/Fabric build baseline to exact upstream VS2.

This script deliberately changes build/tooling metadata only. It does not alter VS2 gameplay,
ship-space, physics, collision, player/camera, networking, rendering, or entity-dragging code.
Every replacement is exact and fails closed if the pinned upstream source no longer matches.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")


def replace_once(rel, old, new):
    path = root / rel
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"expected exactly one match in {rel}: {old!r}; found {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def replace_active_dependency_config(rel, old, new, expected):
    """Replace a Gradle dependency configuration only on non-comment source lines."""
    path = root / rel
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    count = 0
    out = []
    for line in lines:
        if not line.lstrip().startswith("//"):
            hits = line.count(old)
            if hits:
                count += hits
                line = line.replace(old, new)
        out.append(line)
    if count != expected:
        raise SystemExit(
            f"expected {expected} active {old!r} references in {rel}; found {count}"
        )
    path.write_text("".join(out), encoding="utf-8")

# Exact target/runtime lock.
replace_once("gradle.properties", "minecraft_version=1.21.1", "minecraft_version=26.2")
replace_once("gradle.properties", "enabled_platforms=fabric,neoforge", "enabled_platforms=fabric")
replace_once("gradle.properties", "archives_base_name=valkyrienskies-1-21-1", "archives_base_name=valkyrienskies-26-2")
replace_once("gradle.properties", "fabric_loader_version=0.18.4", "fabric_loader_version=0.19.3")
replace_once("gradle.properties", "fabric_api_version=0.115.1+1.21.1", "fabric_api_version=0.160.0+26.2")
replace_once("gradle.properties", "fcap_version = 21.1.0", "fcap_version = 26.2.1")

# P1 is Fabric-only standalone VS2. NeoForge is intentionally outside this target.
replace_once("settings.gradle", 'include("forge")\n', "")

# Minecraft 26.2 baseline: Gradle 9.5.1, Architectury/Loom 1.17, Java 25,
# and no Mojang-mappings dependency because the game is unobfuscated.
replace_once(
    "gradle/wrapper/gradle-wrapper.properties",
    "distributionUrl=https\\://services.gradle.org/distributions/gradle-8.11-all.zip",
    "distributionUrl=https\\://services.gradle.org/distributions/gradle-9.5.1-all.zip",
)
replace_once("build.gradle", 'id "architectury-plugin" version "3.4.161"', 'id "architectury-plugin" version "3.5.170"')
replace_once("build.gradle", 'id "dev.architectury.loom" version "1.9.428" apply false', 'id "dev.architectury.loom-no-remap" version "1.17.493" apply false')
replace_once("build.gradle", 'id "org.jetbrains.kotlin.jvm" version "2.0.0" apply false', 'id "org.jetbrains.kotlin.jvm" version "2.4.20" apply false')
replace_once("build.gradle", '    apply plugin: "dev.architectury.loom"', '    apply plugin: "dev.architectury.loom-no-remap"')
replace_once("build.gradle", '        mappings loom.officialMojangMappings()\n', "")
replace_once("build.gradle", "        options.release = 21", "        options.release = 25")
replace_once(
    "build.gradle",
    '''    tasks.withType(KotlinJvmCompile).configureEach {\n        kotlinOptions {\n            jvmTarget = "21"\n            freeCompilerArgs += "-Xjvm-default=all"\n        }\n    }''',
    '''    tasks.withType(KotlinJvmCompile).configureEach {\n        compilerOptions {\n            jvmTarget.set(org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_25)\n            freeCompilerArgs.add("-Xjvm-default=all")\n        }\n    }''',
)

# Gradle 9 removed the legacy base-plugin convention property archivesBaseName.
# Preserve the upstream archive identity through the supported BasePluginExtension instead.
replace_once(
    "build.gradle",
    "    archivesBaseName = rootProject.archives_base_name",
    '''    base {\n        archivesName = rootProject.archives_base_name\n    }''',
)

# Minecraft 26.2 is unobfuscated and loom-no-remap uses the official namespace directly.
# The pinned upstream AW was authored against the older named namespace, so adapt only
# its namespace header first; individual entries remain untouched until Loom gives direct evidence.
replace_once(
    "common/src/main/resources/valkyrienskies-common.accesswidener",
    "accessWidener\tv2\tnamed\n",
    "accessWidener\tv2\tofficial\n",
)

# Shadow 7.x predates the Gradle-9 toolchain used by Minecraft 26.2.
replace_once(
    "fabric/build.gradle",
    'id "com.github.johnrengelman.shadow" version "7.1.2"',
    'id "com.gradleup.shadow" version "9.2.2"',
)

# P1 compile/boot does not publish artifacts. The upstream publication script is wired
# directly to Loom's remapJar task, which intentionally does not exist under no-remap.
# Disable only that distribution-time script here; production publishing is revisited
# after the standalone 26.2 build/runtime path is proven.
replace_once(
    "fabric/build.gradle",
    "apply from: '../gradle-scripts/publish-curseforge.gradle'\n",
    "",
)

# 26.x is unobfuscated: use Architectury Loom's no-remap path and remove the
# upstream remapJar task, which is not part of the no-remap build model.
replace_once(
    "fabric/build.gradle",
    '''remapJar {\n    input.set shadowJar.archiveFile\n    dependsOn shadowJar\n    archiveClassifier.set null\n    duplicatesStrategy DuplicatesStrategy.EXCLUDE // Ignore duplicate valkyrienskies-common.accesswidener files\n}\n\n''',
    "",
)

# loom-no-remap intentionally omits Loom's remapping dependency configurations.
# Keep the exact upstream dependency coordinates, scopes, and include() structure; only
# translate the active configuration names to their plain Gradle equivalents.
replace_active_dependency_config("common/build.gradle", "modImplementation", "implementation", 3)
replace_active_dependency_config("common/build.gradle", "modApi", "api", 1)
replace_active_dependency_config("common/build.gradle", "modCompileOnly", "compileOnly", 18)
replace_active_dependency_config("fabric/build.gradle", "modImplementation", "implementation", 6)
replace_active_dependency_config("fabric/build.gradle", "modCompileOnly", "compileOnly", 11)

# Forge Config API Port is required by the real Fabric initializer to register VS2's
# NeoForge-style ModConfig specs. Keep that upstream integration, but move its Maven
# coordinate from the pinned 1.21.1 line to the official Minecraft 26.2 release. The
# pinned Fabric build also carries a redundant old Curse compile-only FCAP jar; remove
# only that duplicate so Loom does not process its intermediary access widener.
replace_once(
    "fabric/build.gradle",
    '    compileOnly("curse.maven:forge-config-api-port-fabric-547434:$config_api_id")\n',
    "",
)

# The pinned upstream itself documents this common-side Sable coordinate as an old
# optional compatibility dependency that does not resolve on newer Minecraft lines.
# It is not imported by VS2 source, so omit only this unavailable compile-only artifact.
replace_once(
    "common/build.gradle",
    '    compileOnly("dev.ryanhcode.sable:sable-common-${minecraft_version}:${sable_version}")\n',
    "",
)

# CC:Tweaked 1.115.1 has no 26.2 common artifact at the upstream coordinate. The pinned
# VS2 dependency is used only by the isolated optional cc_tweaked mixin package, not by
# core ship-space/physics/player code. Disable only that optional common compatibility
# surface for the standalone 26.2 port; keep the original source baseline untouched.
replace_once(
    "common/build.gradle",
    '    compileOnly("cc.tweaked:cc-tweaked-${minecraft_version}-common:${cc_tweaked_version}")\n',
    "",
)
replace_once(
    "common/build.gradle",
    '            exclude "org/valkyrienskies/mod/mixin/mod_compat/alex_caves/**"\n',
    '            exclude "org/valkyrienskies/mod/mixin/mod_compat/alex_caves/**"\n            exclude "org/valkyrienskies/mod/mixin/mod_compat/cc_tweaked/**"\n',
)
replace_once(
    "common/src/main/resources/valkyrienskies-common.mixins.json",
    '''    "mod_compat.cc_tweaked.MixinCustomLecternRenderer",\n    "mod_compat.cc_tweaked.MixinSpeakerPosition",\n    "mod_compat.cc_tweaked.MixinSpeakerSound",\n    "mod_compat.cc_tweaked.MixinTurtleBrain",\n    "mod_compat.cc_tweaked.MixinTurtleMoveCommand",\n    "mod_compat.cc_tweaked.MixinWirelessNetwork",\n''',
    "",
)

# The pinned Moonlight dependency is present only to support Supplementaries/Moonlight
# compatibility. On the 26.2 no-remap path its older jar carries an intermediary AW,
# which Loom cannot process in an official-only Minecraft namespace. The exact pinned
# VS2 tree contains only MixinFakeServerLevel under mod_compat/moonlight, so disable only
# this optional compat surface during standalone P1 instead of rewriting a third-party jar.
replace_once(
    "common/build.gradle",
    '    implementation("maven.modrinth:moonlight:$moonlight_version")\n',
    "",
)
replace_once(
    "common/build.gradle",
    '            exclude "org/valkyrienskies/mod/mixin/mod_compat/cc_tweaked/**"\n',
    '            exclude "org/valkyrienskies/mod/mixin/mod_compat/cc_tweaked/**"\n            exclude "org/valkyrienskies/mod/mixin/mod_compat/moonlight/**"\n',
)
replace_once(
    "common/src/main/resources/valkyrienskies-common.mixins.json",
    '    "mod_compat.moonlight.MixinFakeServerLevel",\n',
    "",
)

print("P1_BUILD_BASELINE_APPLIED")