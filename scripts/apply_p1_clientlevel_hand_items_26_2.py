#!/usr/bin/env python3
"""Adapt only MixinClientLevel creative barrier two-hand access to Minecraft 26.2.

Pinned VS2 checks LocalPlayer.getHandSlots() and marks barrier particles visible when
EITHER hand contains a barrier. Minecraft 26.2 removed getHandSlots() while retaining
public LivingEntity.getMainHandItem()/getOffhandItem(). Replace only that two-hand read;
particle spawning, creative-mode gating, player-scale math, ship-space transforms, and
all renderer/physics authority stay unchanged.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/client/world/MixinClientLevel.java"
if not path.is_file():
    raise SystemExit(f"fail-closed: expected pinned VS2 MixinClientLevel source missing: {path}")

text = path.read_text(encoding="utf-8")

old_import = "import net.minecraft.world.item.ItemStack;\n"
old_block = """        boolean holdingBarrierItem = false;
        if (this.minecraft.gameMode.getPlayerMode() == GameType.CREATIVE) {
            for (final ItemStack itemStack : this.minecraft.player.getHandSlots()) {
                if (itemStack.getItem() == Blocks.BARRIER.asItem()) {
                    holdingBarrierItem = true;
                    break;
                }
            }
        }
"""
new_block = """        boolean holdingBarrierItem = false;
        if (this.minecraft.gameMode.getPlayerMode() == GameType.CREATIVE) {
            holdingBarrierItem =
                this.minecraft.player.getMainHandItem().getItem() == Blocks.BARRIER.asItem()
                    || this.minecraft.player.getOffhandItem().getItem() == Blocks.BARRIER.asItem();
        }
"""

if text.count(old_import) != 1:
    raise SystemExit(f"fail-closed: expected one ItemStack import, found {text.count(old_import)}")
if text.count(old_block) != 1:
    raise SystemExit(f"fail-closed: expected one pinned getHandSlots barrier block, found {text.count(old_block)}")
if text.count("getHandSlots()") != 1:
    raise SystemExit(f"fail-closed: expected one legacy getHandSlots call, found {text.count('getHandSlots()')}")
if "getMainHandItem()" in text or "getOffhandItem()" in text:
    raise SystemExit("fail-closed: MixinClientLevel hand-item adaptation already partially present")

# Guard the independent next frontier and the surrounding real-VS2 particle/ship-space path.
anchors = {
    "if (this.minecraft.gameMode.getPlayerMode() == GameType.CREATIVE) {": 1,
    "final double playerScale = player.getBbWidth() / Player.STANDING_DIMENSIONS.width();": 1,
    "for (final Ship ship : VSGameUtilsKt.getShipsIntersecting(ClientLevel.class.cast(this), shipIntersectBB)) {": 1,
    "biggerBB.transform(ship.getWorldToShip(), temp0)": 1,
    "smallerBB.transform(ship.getWorldToShip(), temp2)": 1,
    "if (holdingBarrierItem && blockState.is(Blocks.BARRIER)) {": 1,
    "thisAsClientLevel.addParticle(new BlockParticleOption(ParticleTypes.BLOCK_MARKER, blockState),": 1,
}
for anchor, expected in anchors.items():
    count = text.count(anchor)
    if count != expected:
        raise SystemExit(f"fail-closed: preserved MixinClientLevel anchor changed: {anchor!r} count={count} expected={expected}")

text = text.replace(old_import, "", 1)
text = text.replace(old_block, new_block, 1)

if "getHandSlots()" in text:
    raise SystemExit("fail-closed: legacy getHandSlots call remains")
if text.count("getMainHandItem()") != 1 or text.count("getOffhandItem()") != 1:
    raise SystemExit("fail-closed: expected exactly one public main/offhand read after adaptation")
if old_import in text:
    raise SystemExit("fail-closed: obsolete ItemStack import remains")
if text.count("Player.STANDING_DIMENSIONS.width()") != 1:
    raise SystemExit("fail-closed: independent standing-dimensions frontier changed unexpectedly")
for anchor, expected in anchors.items():
    count = text.count(anchor)
    if count != expected:
        raise SystemExit(f"fail-closed: MixinClientLevel anchor changed after adaptation: {anchor!r} count={count} expected={expected}")

path.write_text(text, encoding="utf-8")
print("P1_CLIENTLEVEL_HAND_ITEMS_26_2_OVERLAY_APPLIED calls=2")
