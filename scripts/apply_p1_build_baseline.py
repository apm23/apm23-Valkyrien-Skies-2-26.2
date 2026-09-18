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

# Exact target/runtime lock.
replace_once("gradle.properties", "minecraft_version=1.21.1", "minecraft_version=26.2")
replace_once("gradle.properties", "enabled_platforms=fabric,neoforge", "enabled_platforms=fabric")
replace_once("gradle.properties", "archives_base_name=valkyrienskies-1-21-1", "archives_base_name=valkyrienskies-26-2")
replace_once("gradle.properties", "fabric_loader_version=0.18.4", "fabric_loader_version=0.19.3")
replace_once("gradle.properties", "fabric_api_version=0.115.1+1.21.1", "fabric_api_version=0.160.0+26.2")

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
replace_once("build.gradle", 'id "dev.architectury.loom" version "1.9.428" apply false', 'id "dev.architectury.loom" version "1.17.493" apply false')
replace_once("build.gradle", 'id "org.jetbrains.kotlin.jvm" version "2.0.0" apply false', 'id "org.jetbrains.kotlin.jvm" version "2.4.20" apply false')
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

# Shadow 7.x predates the Gradle-9 toolchain used by Minecraft 26.2.
replace_once(
    "fabric/build.gradle",
    'id "com.github.johnrengelman.shadow" version "7.1.2"',
    'id "com.gradleup.shadow" version "9.2.2"',
)

print("P1_BUILD_BASELINE_APPLIED")
