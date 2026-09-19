#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/kotlin/org/valkyrienskies/mod/common/blockentity/TestHingeBlockEntity.kt"
text = path.read_text(encoding="utf-8")


def replace_once(old: str, new: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"expected exactly one occurrence of {old!r} in {path}, found {count}")
    text = text.replace(old, new)


replace_once(
    "import net.minecraft.core.BlockPos\n"
    "import net.minecraft.core.HolderLookup\n"
    "import net.minecraft.nbt.CompoundTag\n"
    "import net.minecraft.server.level.ServerLevel\n"
    "import net.minecraft.world.level.block.entity.BlockEntity\n"
    "import net.minecraft.world.level.block.state.BlockState\n",
    "import com.mojang.serialization.Codec\n"
    "import net.minecraft.core.BlockPos\n"
    "import net.minecraft.server.level.ServerLevel\n"
    "import net.minecraft.world.level.block.entity.BlockEntity\n"
    "import net.minecraft.world.level.block.state.BlockState\n"
    "import net.minecraft.world.level.storage.ValueInput\n"
    "import net.minecraft.world.level.storage.ValueOutput\n"
    "import org.joml.Quaterniond\n"
    "import org.joml.Vector3d\n",
)

for old_import in (
    "import org.valkyrienskies.mod.util.getQuatd\n",
    "import org.valkyrienskies.mod.util.getVector3d\n",
    "import org.valkyrienskies.mod.util.putQuatd\n",
    "import org.valkyrienskies.mod.util.putVector3d\n",
):
    replace_once(old_import, "")

replace_once(
    '''    override fun saveAdditional(tag: CompoundTag, provider: HolderLookup.Provider) {
        super.saveAdditional(tag, provider)
        val h = hingeConstraint ?: return

        tag.putLong("shipId0", h.shipId0 ?: -1)
        tag.putLong("shipId1", h.shipId1 ?: -1)
        tag.putVector3d("pos0", h.pose0.pos)
        tag.putVector3d("pos1", h.pose1.pos)
        tag.putQuatd("rot0", h.pose0.rot)
        tag.putQuatd("rot1", h.pose1.rot)
    }

    override fun loadAdditional(tag: CompoundTag, provider: HolderLookup.Provider) {
        super.loadAdditional(tag, provider)
        hingeConstraint = VSRevoluteJoint(
            tag.getLong("shipId0").orElse(0L), VSJointPose(tag.getVector3d("pos0") ?: return, tag.getQuatd("rot0") ?: return),
            tag.getLong("shipId1").orElse(0L), VSJointPose(tag.getVector3d("pos1") ?: return, tag.getQuatd("rot1") ?: return),
            maxForceTorque = null, driveFreeSpin = true
        )
        makeConstraint = true
    }
''',
    '''    override fun saveAdditional(output: ValueOutput) {
        super.saveAdditional(output)
        val h = hingeConstraint ?: return

        output.putLong("shipId0", h.shipId0 ?: -1)
        output.putLong("shipId1", h.shipId1 ?: -1)
        output.putDouble("pos0x", h.pose0.pos.x())
        output.putDouble("pos0y", h.pose0.pos.y())
        output.putDouble("pos0z", h.pose0.pos.z())
        output.putDouble("pos1x", h.pose1.pos.x())
        output.putDouble("pos1y", h.pose1.pos.y())
        output.putDouble("pos1z", h.pose1.pos.z())
        output.putDouble("rot0x", h.pose0.rot.x())
        output.putDouble("rot0y", h.pose0.rot.y())
        output.putDouble("rot0z", h.pose0.rot.z())
        output.putDouble("rot0w", h.pose0.rot.w())
        output.putDouble("rot1x", h.pose1.rot.x())
        output.putDouble("rot1y", h.pose1.rot.y())
        output.putDouble("rot1z", h.pose1.rot.z())
        output.putDouble("rot1w", h.pose1.rot.w())
    }

    override fun loadAdditional(input: ValueInput) {
        super.loadAdditional(input)

        val pos0 = Vector3d(
            input.read("pos0x", Codec.DOUBLE).orElse(null) ?: return,
            input.read("pos0y", Codec.DOUBLE).orElse(null) ?: return,
            input.read("pos0z", Codec.DOUBLE).orElse(null) ?: return,
        )
        val pos1 = Vector3d(
            input.read("pos1x", Codec.DOUBLE).orElse(null) ?: return,
            input.read("pos1y", Codec.DOUBLE).orElse(null) ?: return,
            input.read("pos1z", Codec.DOUBLE).orElse(null) ?: return,
        )
        val rot0 = Quaterniond(
            input.read("rot0x", Codec.DOUBLE).orElse(null) ?: return,
            input.read("rot0y", Codec.DOUBLE).orElse(null) ?: return,
            input.read("rot0z", Codec.DOUBLE).orElse(null) ?: return,
            input.read("rot0w", Codec.DOUBLE).orElse(null) ?: return,
        )
        val rot1 = Quaterniond(
            input.read("rot1x", Codec.DOUBLE).orElse(null) ?: return,
            input.read("rot1y", Codec.DOUBLE).orElse(null) ?: return,
            input.read("rot1z", Codec.DOUBLE).orElse(null) ?: return,
            input.read("rot1w", Codec.DOUBLE).orElse(null) ?: return,
        )

        hingeConstraint = VSRevoluteJoint(
            input.getLong("shipId0").orElse(0L), VSJointPose(pos0, rot0),
            input.getLong("shipId1").orElse(0L), VSJointPose(pos1, rot1),
            maxForceTorque = null, driveFreeSpin = true
        )
        makeConstraint = true
    }
''',
)

if "CompoundTag" in text or "HolderLookup.Provider" in text:
    raise SystemExit(f"legacy TestHingeBlockEntity persistence boundary still present in {path}")
if text.count("override fun saveAdditional(output: ValueOutput)") != 1:
    raise SystemExit(f"expected exactly one ValueOutput saveAdditional override in {path}")
if text.count("override fun loadAdditional(input: ValueInput)") != 1:
    raise SystemExit(f"expected exactly one ValueInput loadAdditional override in {path}")
for key in ("shipId0", "shipId1", "pos0x", "pos0y", "pos0z", "pos1x", "pos1y", "pos1z", "rot0x", "rot0y", "rot0z", "rot0w", "rot1x", "rot1y", "rot1z", "rot1w"):
    if key not in text:
        raise SystemExit(f"required persisted key {key!r} missing after overlay in {path}")

path.write_text(text, encoding="utf-8")
print("P1_TESTHINGE_BLOCKENTITY_VALUE_IO_26_2_OVERLAY_APPLIED")
