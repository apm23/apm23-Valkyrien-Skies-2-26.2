#!/usr/bin/env python3
"""Apply the isolated Minecraft 26.2 nullable translation-argument adaptation.

Pinned upstream VS2 intentionally passes nullable ship slug values directly as
arguments to Minecraft translatable components. Minecraft 26.2 keeps the Java
Component.translatable(String, Object...) factory, but Kotlin now treats those
vararg elements as non-null Any at these call sites, so the unchanged upstream
String? values no longer compile.

This fail-closed overlay does NOT invent, normalize, or substitute a ship name.
It routes only the six proven nullable-slug translation calls through a tiny Java
compatibility bridge whose parameters explicitly remain @Nullable String, then
forwards those exact values into vanilla Component.translatable. No ship
lifecycle, physics, collision, entity-dragging, camera, authority, persistence,
or gameplay behavior is replaced here.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")

helper_rel = "common/src/main/java/org/valkyrienskies/mod/common/util/NullableTranslatableCompat.java"
helper_path = root / helper_rel

helper_source = """package org.valkyrienskies.mod.common.util;

import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.MutableComponent;
import org.jetbrains.annotations.Nullable;

/**
 * Minecraft 26.2 Kotlin-nullability bridge for upstream VS2 translation args.
 *
 * <p>Upstream VS2 intentionally forwards nullable ship slugs to vanilla
 * translatable components. Keep that exact value, including null, rather than
 * manufacturing a fallback name solely to satisfy Kotlin's tightened view of
 * Component.translatable(String, Object...).</p>
 */
public final class NullableTranslatableCompat {
    private NullableTranslatableCompat() {
    }

    public static MutableComponent translatable(final String key, @Nullable final String nullableArg) {
        return Component.translatable(key, nullableArg);
    }

    public static MutableComponent translatable(
        final String key, @Nullable final String nullableArg, final Object secondArg
    ) {
        return Component.translatable(key, nullableArg, secondArg);
    }
}
"""

if helper_path.exists():
    raise SystemExit(f"refusing to overwrite unexpected upstream file: {helper_rel}")

patches = {
    "common/src/main/kotlin/org/valkyrienskies/mod/common/command/commands/DeleteCommand.kt": [
        (
            "import net.minecraft.network.chat.Component\n",
            "import net.minecraft.network.chat.Component\n"
            "import org.valkyrienskies.mod.common.util.NullableTranslatableCompat\n",
        ),
        (
            "Component.translatable(DELETED_ONE_SHIP_MESSAGE, r[0].slug)",
            "NullableTranslatableCompat.translatable(DELETED_ONE_SHIP_MESSAGE, r[0].slug)",
        ),
    ],
    "common/src/main/kotlin/org/valkyrienskies/mod/common/command/commands/GetShipCommand.kt": [
        (
            "import net.minecraft.network.chat.Component.translatable\n",
            "import net.minecraft.network.chat.Component.translatable\n"
            "import org.valkyrienskies.mod.common.util.NullableTranslatableCompat\n",
        ),
        (
            "translatable(GET_SHIP_SUCCESS_MESSAGE, ship.slug, ship.id)",
            "NullableTranslatableCompat.translatable(GET_SHIP_SUCCESS_MESSAGE, ship.slug, ship.id)",
        ),
    ],
    "common/src/main/kotlin/org/valkyrienskies/mod/common/command/commands/RemassCommand.kt": [
        (
            "import net.minecraft.network.chat.Component.translatable\n",
            "import net.minecraft.network.chat.Component.translatable\n"
            "import org.valkyrienskies.mod.common.util.NullableTranslatableCompat\n",
        ),
        (
            "translatable(\n                                        REMASSED_SHIP_FAIL_MESSAGE, ship.slug\n                                    )",
            "NullableTranslatableCompat.translatable(\n                                        REMASSED_SHIP_FAIL_MESSAGE, ship.slug\n                                    )",
        ),
    ],
    "common/src/main/kotlin/org/valkyrienskies/mod/common/item/ShipAssemblerItem.kt": [
        (
            "import org.valkyrienskies.mod.common.isChunkInShipyard\n",
            "import org.valkyrienskies.mod.common.isChunkInShipyard\n"
            "import org.valkyrienskies.mod.common.util.NullableTranslatableCompat\n",
        ),
        (
            "Component.translatable(\"command.valkyrienskies.shipify.success_one\", shipData.slug)",
            "NullableTranslatableCompat.translatable(\"command.valkyrienskies.shipify.success_one\", shipData.slug)",
        ),
    ],
    "common/src/main/kotlin/org/valkyrienskies/mod/common/item/ShipCreatorItem.kt": [
        (
            "import org.valkyrienskies.mod.common.util.EntityShipCollisionUtils\n",
            "import org.valkyrienskies.mod.common.util.EntityShipCollisionUtils\n"
            "import org.valkyrienskies.mod.common.util.NullableTranslatableCompat\n",
        ),
        (
            "Component.translatable(\"command.valkyrienskies.shipify.success_one\", serverShip.slug)",
            "NullableTranslatableCompat.translatable(\"command.valkyrienskies.shipify.success_one\", serverShip.slug)",
        ),
    ],
    "common/src/main/kotlin/org/valkyrienskies/mod/common/item/ShipRemoverItem.kt": [
        (
            "import org.valkyrienskies.mod.common.getShipManagingPos\n",
            "import org.valkyrienskies.mod.common.getShipManagingPos\n"
            "import org.valkyrienskies.mod.common.util.NullableTranslatableCompat\n",
        ),
        (
            "Component.translatable(\"command.valkyrienskies.delete.success_one\", ship.slug)",
            "NullableTranslatableCompat.translatable(\"command.valkyrienskies.delete.success_one\", ship.slug)",
        ),
    ],
}

for rel, replacements in patches.items():
    path = root / rel
    text = path.read_text(encoding="utf-8")
    for old, new in replacements:
        count = text.count(old)
        if count != 1:
            raise SystemExit(f"expected exactly 1 replacement target in {rel}: {old!r}; found {count}")
        text = text.replace(old, new, 1)
    path.write_text(text, encoding="utf-8")

helper_path.parent.mkdir(parents=True, exist_ok=True)
helper_path.write_text(helper_source, encoding="utf-8")

# Reassert the narrow semantic envelope after mutation. Every nullable slug still
# reaches the translation call directly; no fallback expression is introduced.
post_needles = {
    "common/src/main/kotlin/org/valkyrienskies/mod/common/command/commands/DeleteCommand.kt":
        "NullableTranslatableCompat.translatable(DELETED_ONE_SHIP_MESSAGE, r[0].slug)",
    "common/src/main/kotlin/org/valkyrienskies/mod/common/command/commands/GetShipCommand.kt":
        "NullableTranslatableCompat.translatable(GET_SHIP_SUCCESS_MESSAGE, ship.slug, ship.id)",
    "common/src/main/kotlin/org/valkyrienskies/mod/common/command/commands/RemassCommand.kt":
        "REMASSED_SHIP_FAIL_MESSAGE, ship.slug",
    "common/src/main/kotlin/org/valkyrienskies/mod/common/item/ShipAssemblerItem.kt":
        "NullableTranslatableCompat.translatable(\"command.valkyrienskies.shipify.success_one\", shipData.slug)",
    "common/src/main/kotlin/org/valkyrienskies/mod/common/item/ShipCreatorItem.kt":
        "NullableTranslatableCompat.translatable(\"command.valkyrienskies.shipify.success_one\", serverShip.slug)",
    "common/src/main/kotlin/org/valkyrienskies/mod/common/item/ShipRemoverItem.kt":
        "NullableTranslatableCompat.translatable(\"command.valkyrienskies.delete.success_one\", ship.slug)",
}
for rel, needle in post_needles.items():
    text = (root / rel).read_text(encoding="utf-8")
    if text.count(needle) != 1:
        raise SystemExit(f"postcondition failed in {rel}: {needle!r}")
    if "slug ?:" in text or "slug?:" in text:
        raise SystemExit(f"forbidden nullable-slug fallback introduced in {rel}")

print("P1_NULLABLE_TRANSLATION_ARGS_26_2_OVERLAY_APPLIED")
