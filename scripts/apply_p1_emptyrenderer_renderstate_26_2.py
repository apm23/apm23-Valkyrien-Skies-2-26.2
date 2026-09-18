#!/usr/bin/env python3
"""Apply the isolated Minecraft 26.2 EmptyRenderer render-state adaptation.

The earlier EmptyRenderer overlay migrates only ResourceLocation -> Identifier.
Minecraft 26.2 EntityRenderer now uses an explicit EntityRenderState generic and
requires createRenderState(). Vanilla EmptyEntityRenderer uses exactly this
shape for a renderer that renders nothing, so this overlay preserves the
upstream EmptyRenderer intent without adding rendering behavior.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
rel = "common/src/main/kotlin/org/valkyrienskies/mod/client/EmptyRenderer.kt"
path = root / rel
text = path.read_text(encoding="utf-8")


def replace_count(old: str, new: str, expected: int = 1) -> None:
    global text
    count = text.count(old)
    if count != expected:
        raise SystemExit(f"expected {expected} matches in {rel}: {old!r}; found {count}")
    text = text.replace(old, new, expected)


# This overlay intentionally targets the post-Identifier-overlay form so the
# two API adaptations remain independently traceable and fail closed.
replace_count(
    "import net.minecraft.client.renderer.entity.EntityRendererProvider\n"
    "import net.minecraft.resources.Identifier\n"
    "import net.minecraft.world.entity.Entity",
    "import net.minecraft.client.renderer.entity.EntityRendererProvider\n"
    "import net.minecraft.client.renderer.entity.state.EntityRenderState\n"
    "import net.minecraft.world.entity.Entity",
)
replace_count(
    "class EmptyRenderer(context: EntityRendererProvider.Context) :\n"
    "    EntityRenderer<Entity>(context) {\n\n"
    "    override fun getTextureLocation(entity: Entity): Identifier? = null\n"
    "}",
    "class EmptyRenderer(context: EntityRendererProvider.Context) :\n"
    "    EntityRenderer<Entity, EntityRenderState>(context) {\n\n"
    "    override fun createRenderState(): EntityRenderState = EntityRenderState()\n"
    "}",
)

path.write_text(text, encoding="utf-8")
print("P1_EMPTYRENDERER_RENDERSTATE_26_2_OVERLAY_APPLIED")
