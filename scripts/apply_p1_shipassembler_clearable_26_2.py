#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
PATH = ROOT / "common/src/main/kotlin/org/valkyrienskies/mod/common/assembly/ShipAssembler.kt"

text = PATH.read_text(encoding="utf-8")
old = "Clearable.tryClear(it)"
new = "it.clearContent()"

# Minecraft 26.2 removed the legacy static Clearable.tryClear helper while
# retaining Clearable.clearContent().  These three calls are the exact upstream
# ShipAssembler source-block-entity clear sites.  Keep this adaptation isolated
# from the independent ValueInput/component and chunk-ticket migrations.
if text.count(old) != 3:
    raise SystemExit(f"expected exactly 3 legacy ShipAssembler Clearable.tryClear sites, found {text.count(old)}")
if text.count("it.loadWithComponents(CompoundTag(), level.registryAccess())") != 3:
    raise SystemExit("unexpected ShipAssembler empty-tag fallback shape; refusing to absorb ValueInput migration")
if text.count("import net.minecraft.world.Clearable") != 1:
    raise SystemExit("unexpected ShipAssembler Clearable import shape")

text = text.replace(old, new)

if old in text:
    raise SystemExit("legacy Clearable.tryClear remained after replacement")
if text.count(new) != 3:
    raise SystemExit(f"expected exactly 3 direct Clearable.clearContent calls after replacement, found {text.count(new)}")
if text.count("it.loadWithComponents(CompoundTag(), level.registryAccess())") != 3:
    raise SystemExit("ValueInput/component fallback changed unexpectedly")

PATH.write_text(text, encoding="utf-8")
print("Applied Minecraft 26.2 ShipAssembler Clearable.clearContent compatibility overlay")
