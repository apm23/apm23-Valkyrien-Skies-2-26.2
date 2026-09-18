# apm23-Valkyrien-Skies-2-26.2

This repository is a clean-room **version port of the real upstream Valkyrien Skies 2 source** to Minecraft Java/Fabric 26.2.

## Non-negotiable identity

This project MUST use the **actual original VS2 codebase** as the physics / ship-space / transform / collision / player-camera foundation.

It is **NOT** a project to:
- imitate VS2 with a custom carry/reference-frame system;
- recreate only selected VS2 behavior;
- stack per-tick teleport/setPos, synthetic carry velocity, fake gravity, camera compensation, wall clamps, or floor-only fixes;
- copy the previous `VS2-Create_Interactive` workaround chain.

Every ported subsystem must remain traceable to official upstream VS2 source. Minecraft-26.2 adaptations are allowed; replacing VS2 architecture with an unrelated custom implementation is not.

## Upstream source baseline

- Upstream: `ValkyrienSkies/Valkyrien-Skies-2`
- Branch: `1.21.1/main`
- Initial pinned HEAD: `f39132148e717d325933b4ce6e9e9fb13d929390`
- Upstream mod version at that pin: `2.4.12`

The pin may only change deliberately, with provenance recorded in `MASTER_STATE.md`.

## Port order

1. Import/preserve upstream VS2 source and license.
2. Port VS2 itself to Minecraft 26.2 / Java 25 / Fabric.
3. Prove standalone real-VS2 runtime before any Create train bridge.
4. Integrate Create Fly using real VS2 ships/reference spaces.
5. Integrate Steam 'n' Rails and Copycats.
6. Build/verify exact candidate.
7. Final readiness requires a real-user runtime test of the exact final JAR.

See `PORT_CONTRACT.md`, `BASELINE_LOCK.json`, and `MASTER_STATE.md`.
