# PORT_CONTRACT — REAL VS2, NOT A VS2-LIKE SYSTEM

## Absolute rule

**VS2 ASLI. BUKAN SYSTEM MIRIP VS2.**

The deliverable is a port of the actual official Valkyrien Skies 2 source code to Minecraft Java/Fabric 26.2.

A result is invalid if it merely reproduces some VS2 behavior using a new home-grown movement/reference-frame/collision system.

## Provenance rule

For every core subsystem used by the final port, engineering must be able to identify its upstream VS2 origin or explain the minimal Minecraft-26.2 adaptation.

Preserve upstream license/notices. Do not silently replace:
- VS2 ship-space / shipyard model;
- ship transforms;
- physics-core integration;
- collision integration;
- entity dragging / moving-reference-space behavior;
- player/body/camera integration;
- client/server ship state;
- rendering integration;
with unrelated custom substitutes.

A Minecraft 26.2 compatibility shim is allowed only when it adapts changed Minecraft/Fabric APIs to the existing VS2 architecture.

## Previous project isolation

Repository `apm23/VS2-Create_Interactive` is historical evidence only.

Do NOT import its gameplay patches, carry chains, floor fixes, camera corrections, wall clamps, synthetic velocity, per-tick reanchor/setPos logic, or assumptions into this repository unless a specific fragment is independently proven to be an upstream-derived version-port adaptation.

The previous project's exact-JAR runtime result is retained only as a warning:
- floor behavior could appear correct while jump, turns, camera, and walls were still fundamentally wrong.

Therefore a floor-only or grounded-only green result is never sufficient evidence for this project.

## Mandatory milestone order

### P0 — Upstream import and provenance
- Import official VS2 source from the pinned upstream commit.
- Preserve license.
- Record the source pin and any source-file deviations.
- Establish a reproducible 26.2 build environment.

### P1 — Standalone VS2 26.2 boot
No Create, Steam 'n' Rails, or Copycats dependency is allowed to hide VS2 port failures.
- Minecraft 26.2 boots with the port.
- server/client initialization works;
- VSCore/Krunch/native chain loads;
- networking, serialization, registries and mixins initialize.

### P2 / M1 — Standalone real-VS2 ship runtime
Before Create integration, prove a real VS2 ship/reference space on 26.2:
- actual VS2 ship creation/lifecycle;
- ship blocks / ship-space transform;
- translation and rotation;
- player standing and walking;
- jump -> airborne -> natural landing while staying in the ship frame;
- solid floor/walls/ceiling;
- free stable mouse look/camera;
- entity dragging/reference-frame behavior;
- client/server synchronization;
- no fake carry, no per-tick teleport chase.

Only after this may `M1_COMPLETE` be used.

### P3 — Create Fly bridge
Create remains authoritative for railway gameplay:
- track graph;
- bogeys;
- stations;
- schedules;
- desired carriage trajectory/transform.

The moving carriage interior must be represented by **real VS2 ship/reference space**, not a fake proxy that only copies matrices.

Initial architecture target: **one Create carriage = one real VS2 ship** because articulated carriages may have distinct transforms.

Prefer driving/controlling the actual VS2 ship transform through a legitimate VS2 integration/kinematic boundary instead of cloning VS2 physics outside VS2.

Do not begin this milestone until P2 is frozen green.

### P4 — Steam 'n' Rails + Copycats
Add exact locked SNR/Copycats compatibility after the Create bridge works with real VS2.

### P5 — Production integration and final artifact
- full target stack;
- regression proof;
- exact candidate JAR hash;
- real-user runtime acceptance.

## Forbidden shortcuts

Never accept these as substitutes for real VS2:
- custom "VS2-style" reference frame;
- grounded floor carry as proof of full ship space;
- synthetic carry velocity/inertia;
- fake gravity;
- manual wall/ceiling clamps;
- collision cancellation to hide penetration;
- camera counter-rotation/forcing;
- per-tick player teleport/setPos chase;
- duplicate Create + custom + VS2 ownership;
- replacing real VS2 ship lifecycle with a plain Create contraption plus helper matrix;
- modifying test fixtures/input to manufacture green;
- declaring FINAL_READY from CI alone.

## Watchdog engineering discipline

- GitHub HEAD + complete `MASTER_STATE.md` are authoritative.
- Inspect/reconcile before every mutation.
- One evidence-backed root change at a time.
- Freeze proven subsystems.
- Revert regressions before stacking workarounds.
- Record failed hypotheses.
- Timeout recovery must reconcile actual GitHub state before retrying.
- Final exact JAR still requires real-user Minecraft acceptance.
