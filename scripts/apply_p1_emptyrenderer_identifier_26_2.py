#!/usr/bin/env python3
"""Apply the isolated Minecraft 26.2 EmptyRenderer Identifier adaptation.

Exact P1 run 35383401868 leaves two independent EmptyRenderer.kt API areas:
ResourceLocation no longer resolves at the import/texture return type, while the
EntityRenderer render-state generic migration is a separate compiler failure.
This fail-closed overlay changes only the resource identifier vocabulary and
leaves renderer inheritance/render-state semantics untouched.
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
    text = text.replace(old, new)


# Pinned baseline f39132148e... and current 1.21.1/main are byte-identical
# at blob ff3253aa068256ae06c92a6b29d247acabce0532. Minecraft 26.2 uses
# Identifier where this upstream source used ResourceLocation. Keep the
# independent EntityRenderer<Entity>(context) render-state migration untouched.
replace_count(
    "import net.minecraft.resources.ResourceLocation",
    "import net.minecraft.resources.Identifier",
)
replace_count(
    "override fun getTextureLocation(entity: Entity): ResourceLocation? = null",
    "override fun getTextureLocation(entity: Entity): Identifier? = null",
)

path.write_text(text, encoding="utf-8")
print("P1_EMPTYRENDERER_IDENTIFIER_26_2_OVERLAY_APPLIED")
