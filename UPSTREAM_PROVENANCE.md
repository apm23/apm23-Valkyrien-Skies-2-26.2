# UPSTREAM_PROVENANCE — Valkyrien Skies 2 baseline

This repository ports the real upstream Valkyrien Skies 2 source. The canonical baseline is imported as a Git submodule/gitlink so the source identity remains exact and independently verifiable.

## Canonical upstream identity

- Repository: `https://github.com/ValkyrienSkies/Valkyrien-Skies-2.git`
- Branch used to select the baseline: `1.21.1/main`
- Exact commit: `f39132148e717d325933b4ce6e9e9fb13d929390`
- Exact root tree: `91116399605d3ecd1c93b0011560e09281ee1fa4`
- Upstream mod version at the pin: `2.4.12`
- Upstream `LICENSE` blob: `0a041280bd00a9d068f503b8ee7ce35214bd24a1`

## Import form

`upstream-vs2/` is a Git submodule entry pinned to the exact upstream commit above. A normal checkout with submodules enabled materializes the real original VS2 source tree without reconstructing, reformatting, or copying it from the retired `VS2-Create_Interactive` project.

The pinned source is the architectural baseline. Minecraft 26.2 adaptations must be explicit, reviewable port changes layered onto this source. They may adapt mappings, Fabric/Minecraft APIs, mixin targets, rendering/network hooks, native loading, dependency coordinates, and build tooling, but must not replace VS2 ship-space, physics, collision, entity dragging/reference-space, camera/player, networking, or rendering architecture with a custom imitation.

## Source-tree identity proof

The P0 provenance workflow verifies all of the following after submodule checkout:

1. the root gitlink equals `f39132148e717d325933b4ce6e9e9fb13d929390`;
2. the checked-out submodule HEAD equals that exact commit;
3. the checked-out source root tree equals `91116399605d3ecd1c93b0011560e09281ee1fa4`;
4. `upstream-vs2/LICENSE` hashes to the upstream Git blob `0a041280bd00a9d068f503b8ee7ce35214bd24a1`;
5. the baseline checkout is clean.

Any mismatch blocks P0.

## Isolation rule

No gameplay implementation from `apm23/VS2-Create_Interactive` is imported here. That repository is historical runtime evidence only.
