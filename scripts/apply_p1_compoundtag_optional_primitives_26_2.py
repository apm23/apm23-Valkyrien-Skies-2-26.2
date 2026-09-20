#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")

patches = {
    "common/src/main/java/org/valkyrienskies/mod/mixin/feature/teleport_reconnected_player_to_ship/MixinServerPlayer.java": [
        ('compoundTag.getLong("LastShipId")', 'compoundTag.getLong("LastShipId").orElse(0L)', 1),
        ('compoundTag.getDouble("RelativeShipX")', 'compoundTag.getDouble("RelativeShipX").orElse(0.0)', 1),
        ('compoundTag.getDouble("RelativeShipY")', 'compoundTag.getDouble("RelativeShipY").orElse(0.0)', 1),
        ('compoundTag.getDouble("RelativeShipZ")', 'compoundTag.getDouble("RelativeShipZ").orElse(0.0)', 1),
    ],
    "common/src/main/java/org/valkyrienskies/mod/mixin/feature/save_mob_location_on_ship/MixinMob.java": [
        ('nbt.getDouble("valkyrienskies$unloadedX")', 'nbt.getDouble("valkyrienskies$unloadedX").orElse(0.0)', 1),
        ('nbt.getDouble("valkyrienskies$unloadedY")', 'nbt.getDouble("valkyrienskies$unloadedY").orElse(0.0)', 1),
        ('nbt.getDouble("valkyrienskies$unloadedZ")', 'nbt.getDouble("valkyrienskies$unloadedZ").orElse(0.0)', 1),
    ],
}

changed = 0
for rel, replacements in patches.items():
    path = root / rel
    if not path.is_file():
        raise SystemExit(f"fail-closed: expected VS2 source missing: {path}")
    text = path.read_text(encoding="utf-8")
    for old, new, expected in replacements:
        actual = text.count(old)
        if actual != expected:
            raise SystemExit(
                f"fail-closed: expected {expected} occurrences of {old!r} in {rel}, found {actual}"
            )
        text = text.replace(old, new)
        changed += expected
    path.write_text(text, encoding="utf-8")

if changed != 7:
    raise SystemExit(f"fail-closed: expected exactly 7 CompoundTag Optional primitive adaptations, got {changed}")

print("P1_COMPOUNDTAG_OPTIONAL_PRIMITIVES_26_2_OVERLAY_APPLIED count=7 files=2")
