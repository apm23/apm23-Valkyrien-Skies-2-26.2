#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/kotlin/org/valkyrienskies/mod/common/block/TestHingeBlock.kt"
text = path.read_text(encoding="utf-8")

old = '''    override fun onRemove(
        blockState: BlockState, level: Level, blockPos: BlockPos, blockState2: BlockState, bl: Boolean
    ) {
        if (level is ServerLevel) run {
            val be = level.getBlockEntity(blockPos) as? TestHingeBlockEntity ?: return@run
            ValkyrienSkiesMod.getOrCreateGTPA(level.dimensionId).removeJoint(be.constraintId ?: return@run)
        }

        super.onRemove(blockState, level, blockPos, blockState2, bl)
    }
'''

new = '''    override fun affectNeighborsAfterRemoval(
        blockState: BlockState, level: ServerLevel, blockPos: BlockPos, movedByPiston: Boolean
    ) {
        run {
            val be = level.getBlockEntity(blockPos) as? TestHingeBlockEntity ?: return@run
            ValkyrienSkiesMod.getOrCreateGTPA(level.dimensionId).removeJoint(be.constraintId ?: return@run)
        }

        super.affectNeighborsAfterRemoval(blockState, level, blockPos, movedByPiston)
    }
'''

count = text.count(old)
if count != 1:
    raise SystemExit(f"expected exactly one pinned TestHinge onRemove block in {path}, found {count}")

text = text.replace(old, new)
path.write_text(text, encoding="utf-8")
print("P1_TESTHINGE_REMOVAL_HOOK_26_2_OVERLAY_APPLIED")
