# P1 BUILD PORT NOTES

## Scope

P1 targets standalone **Fabric** VS2 on Minecraft 26.2. Create, Steam 'n' Rails and Copycats are not part of this milestone. The exact upstream source remains pinned as `upstream-vs2`; build adaptations are applied by `scripts/apply_p1_build_baseline.py` and are therefore explicit and reproducible.

## First build-only overlay

The first compile probe changes only build/tooling metadata:

- Minecraft `1.21.1` -> `26.2`;
- enabled platform set -> `fabric` only for this port;
- Fabric Loader -> `0.19.3`;
- Fabric API -> locked `0.160.0+26.2`;
- Gradle `8.11` -> `9.5.1`;
- Architectury plugin -> `3.5.170`;
- Architectury Loom -> `1.17.493`;
- Kotlin Gradle plugin -> `2.4.20` for Gradle 9 / JVM 25 compatibility;
- Java/Kotlin bytecode target -> `25`;
- remove `loom.officialMojangMappings()` because Minecraft 26.x is unobfuscated;
- Shadow plugin -> `com.gradleup.shadow:9.2.2` for Gradle 9 compatibility;
- do not include the NeoForge subproject in the standalone Fabric P1 build.

No VS2 gameplay or runtime architecture source is changed by this overlay.

## Evidence policy

The first CI run is intentionally allowed to fail. Its job is to reach the real 26.2 configuration/compilation boundary and reveal the first concrete blocker. Optional compatibility dependencies or source sets will only be disabled/ported after the log proves they block standalone VS2.
