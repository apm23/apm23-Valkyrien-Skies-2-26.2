#!/usr/bin/env python3
"""Fail-closed Minecraft 26.2 EntityRenderer render-state adaptation for VS2 entity handlers.

Minecraft 26.2 changed EntityRenderer from EntityRenderer<T> to EntityRenderer<T, S>
and moved getRenderOffset from (entity, partialTicks) to (renderState). The old
MultiBufferSource argument is no longer part of the renderer submit boundary.

This overlay adapts only the three upstream VS2 entity-handler contracts to the
new render-state API. It deliberately does NOT alter ship transforms, camera,
culling, entity dragging, movement, networking, gameplay authority, or the
EntityRenderDispatcher mixin lifecycle. The dispatcher lifecycle is inspected
and adapted separately within the same renderer semantic cluster after this
layer is compiler-proven.
"""

from pathlib import Path
import sys


FILES = (
    Path("common/src/main/kotlin/org/valkyrienskies/mod/common/entity/handling/VSEntityHandler.kt"),
    Path("common/src/main/kotlin/org/valkyrienskies/mod/common/entity/handling/AbstractShipyardEntityHandler.kt"),
    Path("common/src/main/kotlin/org/valkyrienskies/mod/common/entity/handling/WorldEntityHandler.kt"),
)


def replace_once(text: str, old: str, new: str, path: Path) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"fail-closed: expected exactly one {old!r} in {path}, found {count}")
    if new in text:
        raise SystemExit(f"fail-closed: target text already present unexpectedly in {path}: {new!r}")
    return text.replace(old, new, 1)


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {sys.argv[0]} <upstream-vs2-root>")

    root = Path(sys.argv[1])

    for relative_path in FILES:
        path = root / relative_path
        text = path.read_text(encoding="utf-8")

        text = replace_once(
            text,
            "import net.minecraft.client.renderer.MultiBufferSource",
            "import net.minecraft.client.renderer.entity.state.EntityRenderState",
            relative_path,
        )
        text = replace_once(
            text,
            "fun <T : Entity> applyRenderTransform(",
            "fun <T : Entity, S : EntityRenderState> applyRenderTransform(",
            relative_path,
        )
        text = replace_once(
            text,
            "entityRenderer: EntityRenderer<T>,",
            "entityRenderer: EntityRenderer<T, S>,",
            relative_path,
        )
        text = replace_once(
            text,
            "matrixStack: PoseStack, buffer: MultiBufferSource, packedLight: Int",
            "matrixStack: PoseStack, renderState: S, packedLight: Int",
            relative_path,
        )

        if relative_path.name != "VSEntityHandler.kt":
            text = replace_once(
                text,
                "val offset = entityRenderer.getRenderOffset(entity, partialTicks)",
                "val offset = entityRenderer.getRenderOffset(renderState)",
                relative_path,
            )

        forbidden = (
            "MultiBufferSource",
            "EntityRenderer<T>,",
            "getRenderOffset(entity, partialTicks)",
        )
        for token in forbidden:
            if token in text:
                raise SystemExit(f"fail-closed: legacy renderer token remains in {relative_path}: {token!r}")

        if text.count("EntityRenderState") != 2:
            raise SystemExit(
                f"fail-closed: expected import + generic bound EntityRenderState in {relative_path}, "
                f"found {text.count('EntityRenderState')}"
            )

        path.write_text(text, encoding="utf-8")

    print("P1_ENTITYHANDLER_RENDERSTATE_26_2_OVERLAY_APPLIED")


if __name__ == "__main__":
    main()
