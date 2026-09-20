#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")

patches = {
    "common/src/main/java/org/valkyrienskies/mod/mixin/entity/MixinEntity.java": (
        "level.isClientSide)",
        "level.isClientSide())",
        5,
    ),
    "common/src/main/java/org/valkyrienskies/mod/mixin/feature/spawn_player_on_ship/MixinPlayer.java": (
        "level().isClientSide)",
        "level().isClientSide())",
        2,
    ),
}

changed = 0
for rel, (old, new, expected) in patches.items():
    path = root / rel
    if not path.is_file():
        raise SystemExit(f"fail-closed: expected VS2 source missing: {path}")
    text = path.read_text(encoding="utf-8")
    actual = text.count(old)
    if actual != expected:
        raise SystemExit(
            f"fail-closed: expected {expected} active pre-26.2 Level client-side field accesses {old!r} in {rel}, found {actual}"
        )
    text = text.replace(old, new)
    if text.count(old) != 0:
        raise SystemExit(f"fail-closed: stale Level client-side field access survived in {rel}")
    path.write_text(text, encoding="utf-8")
    changed += expected

if changed != 7:
    raise SystemExit(f"fail-closed: expected exactly 7 Level client-side accessor adaptations, got {changed}")

print("P1_LEVEL_CLIENTSIDE_ACCESSOR_26_2_OVERLAY_APPLIED count=7 files=2")
