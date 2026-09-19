#!/usr/bin/env python3
from pathlib import Path
import json
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
source_path = root / "common/src/main/kotlin/org/valkyrienskies/mod/common/config/VSKeyBindings.kt"
lang_dir = root / "common/src/main/resources/assets/valkyrienskies/lang"
text = source_path.read_text(encoding="utf-8")


def replace_once(old: str, new: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"expected exactly one occurrence of {old!r} in {source_path}, found {count}")
    text = text.replace(old, new)


replace_once(
    "import net.minecraft.client.KeyMapping\n",
    "import net.minecraft.client.KeyMapping\n"
    "import net.minecraft.resources.Identifier\n",
)

replace_once(
    "    private val toBeRegistered = mutableListOf<Consumer<Consumer<KeyMapping>>>()\n",
    "    private val toBeRegistered = mutableListOf<Consumer<Consumer<KeyMapping>>>()\n"
    "    private val drivingCategory = KeyMapping.Category.register(Identifier.fromNamespaceAndPath(\"valkyrienskies\", \"driving\"))\n",
)

replace_once(
    '    val shipDown = register("key.valkyrienskies.ship_down", GLFW.GLFW_KEY_V, "category.valkyrienskies.driving")\n'
    '    val shipCruise = register("key.valkyrienskies.ship_cruise", GLFW.GLFW_KEY_C, "category.valkyrienskies.driving")\n',
    '    val shipDown = register("key.valkyrienskies.ship_down", GLFW.GLFW_KEY_V, drivingCategory)\n'
    '    val shipCruise = register("key.valkyrienskies.ship_cruise", GLFW.GLFW_KEY_C, drivingCategory)\n',
)

replace_once(
    "    private fun register(name: String, keyCode: Int, category: String): Supplier<KeyMapping> =\n",
    "    private fun register(name: String, keyCode: Int, category: KeyMapping.Category): Supplier<KeyMapping> =\n",
)

if text.count("KeyMapping.Category.register(Identifier.fromNamespaceAndPath(\"valkyrienskies\", \"driving\"))") != 1:
    raise SystemExit(f"expected exactly one registered driving category in {source_path}")
if 'category: String' in text:
    raise SystemExit(f"legacy String category boundary still present in {source_path}")
if text.count("drivingCategory)") != 2:
    raise SystemExit(f"expected both active VS2 key mappings to use drivingCategory in {source_path}")

source_path.write_text(text, encoding="utf-8")

old_key = "category.valkyrienskies.driving"
new_key = "key.category.valkyrienskies.driving"
updated_locales = []

for path in sorted(lang_dir.glob("*.json")):
    lang_text = path.read_text(encoding="utf-8")
    data = json.loads(lang_text)
    if old_key not in data:
        continue
    if new_key in data:
        raise SystemExit(f"new Minecraft 26.2 category translation key already present in {path}")

    lines = lang_text.splitlines(keepends=True)
    candidates = [i for i, line in enumerate(lines) if f'"{old_key}"' in line]
    if len(candidates) != 1:
        raise SystemExit(f"expected exactly one {old_key!r} line in {path}, found {len(candidates)}")

    index = candidates[0]
    original = lines[index]
    newline = "\r\n" if original.endswith("\r\n") else "\n" if original.endswith("\n") else ""
    body = original[:-len(newline)] if newline else original
    indent = body[: len(body) - len(body.lstrip(" \t"))]
    trimmed = body.rstrip(" \t")
    had_comma = trimmed.endswith(",")

    value_json = json.dumps(data[old_key], ensure_ascii=False)
    old_line = f'{indent}"{old_key}": {value_json},{newline}'
    new_line = f'{indent}"{new_key}": {value_json}' + ("," if had_comma else "") + newline
    lines[index:index + 1] = [old_line, new_line]

    updated = "".join(lines)
    parsed = json.loads(updated)
    if parsed.get(old_key) != data[old_key] or parsed.get(new_key) != data[old_key]:
        raise SystemExit(f"category translation value was not preserved in {path}")
    path.write_text(updated, encoding="utf-8", newline="")
    updated_locales.append(path.name)

if "en_us.json" not in updated_locales:
    raise SystemExit("expected en_us.json to preserve the VS2 driving category label")
if not updated_locales:
    raise SystemExit("expected at least one existing VS2 driving category translation")

print(f"P1_VSKEYBINDINGS_CATEGORY_26_2_OVERLAY_APPLIED locales={','.join(updated_locales)}")
