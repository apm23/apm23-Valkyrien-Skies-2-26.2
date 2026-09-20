#!/usr/bin/env python3
"""Adapt the pinned upstream VS2 LevelRenderer mixin to Minecraft 26.2's renderer split.

Exact 26.2 proof:
- LevelRenderer/GameRenderer split: run 35494987861.
- relocated block-damage distance hook: run 35495140731.

This preserves the two active upstream VS2 behaviors only:
1) invalidate vanilla SectionOcclusionGraph when the already-existing VS-mounted vanilla camera transform changes;
2) remove vanilla's 1024 block-damage distance cap, now at LevelExtractor extraction time.
No camera transform, movement, ship-space, physics, collision, or rendering authority is replaced here.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
level_path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/client/renderer/MixinLevelRenderer.java"
mixins_path = root / "common/src/main/resources/valkyrienskies-common.mixins.json"
extractor_path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/client/renderer/MixinLevelExtractor.java"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"fail-closed: expected exactly one {label}, found {count}")
    return text.replace(old, new, 1)


text = level_path.read_text(encoding="utf-8")

# Exact import migration for the current LevelRenderer.render(...) boundary.
text = replace_once(
    text,
    "import com.llamalad7.mixinextras.injector.ModifyExpressionValue;\n",
    "import com.mojang.blaze3d.buffers.GpuBufferSlice;\nimport com.mojang.blaze3d.resource.GraphicsResourceAllocator;\n",
    "old MixinExtras import",
)
text = replace_once(
    text,
    "import net.minecraft.client.renderer.LightTexture;\n",
    "import net.minecraft.client.renderer.state.level.CameraRenderState;\n",
    "obsolete LightTexture import",
)
text = replace_once(
    text,
    "import org.joml.Matrix4f;\n",
    "import org.joml.Matrix4fc;\nimport org.joml.Vector4f;\n",
    "old Matrix4f callback import",
)

# Current LevelRenderer owns GameRenderer and SectionOcclusionGraph. Read the same vanilla
# main Camera instance that upstream VS2 already modifies through IVSCamera; do not create or force a camera.
old_shadow = '''    @Shadow
    @Final
    private SectionOcclusionGraph sectionOcclusionGraph;
'''
new_shadow = '''    @Shadow
    @Final
    private GameRenderer gameRenderer;

    @Shadow
    @Final
    private SectionOcclusionGraph sectionOcclusionGraph;
'''
text = replace_once(text, old_shadow, new_shadow, "SectionOcclusionGraph shadow block")

# Minecraft 26.2 relocated this exact vanilla 1024 distance filter from LevelRenderer to
# LevelExtractor.extractBlockDestroyAnimation. Remove only the stale owner hook here; a new
# MixinLevelExtractor below preserves the same Double.MAX_VALUE behavior at the proven owner.
old_distance_hook = '''    /**
     * @reason This mixin forces the game to always render block damage.
     */
    @ModifyExpressionValue(
        method = "renderLevel",
        at = @At(value = "CONSTANT", args = "doubleValue=1024", ordinal = 0)
    )
    private double disableBlockDamageDistanceCheck(final double originalBlockDamageDistanceConstant) {
        return Double.MAX_VALUE;
    }

'''
text = replace_once(text, old_distance_hook, "", "stale LevelRenderer block-damage distance hook")

old_callback = '''    @Inject(method = "renderLevel", at = @At("HEAD"))
    private void preRenderLevel(DeltaTracker deltaTracker, boolean bl, Camera camera, GameRenderer gameRenderer,
        LightTexture lightTexture, Matrix4f matrix4f, Matrix4f matrix4f2, CallbackInfo ci) {
        final ShipTransform shipMountedRenderTransform = ((IVSCamera) camera).getShipMountedRenderTransform();
'''
new_callback = '''    @Inject(method = "render", at = @At("HEAD"))
    private void preRenderLevel(
        GraphicsResourceAllocator graphicsResourceAllocator,
        DeltaTracker deltaTracker,
        boolean renderBlockOutline,
        CameraRenderState cameraRenderState,
        Matrix4fc matrix4fc,
        GpuBufferSlice gpuBufferSlice,
        Vector4f vector4f,
        boolean renderEntityOutlines,
        CallbackInfo ci) {
        final Camera camera = gameRenderer.mainCamera();
        final ShipTransform shipMountedRenderTransform = ((IVSCamera) camera).getShipMountedRenderTransform();
'''
text = replace_once(text, old_callback, new_callback, "old LevelRenderer.renderLevel callback")

# Fail closed on authority anchors: the existing VS camera transform comparison and vanilla graph
# invalidation must remain exactly present after the API-only callback migration.
authority_anchors = [
    "((IVSCamera) camera).getShipMountedRenderTransform()",
    "valkyrienskies$prevShipMountedToTransform.getShipToWorldRotation().dot(shipMountedRenderTransform.getShipToWorldRotation())",
    "Math.toDegrees(angle) > 1.0",
    "sectionOcclusionGraph.invalidate();",
]
for anchor in authority_anchors:
    if anchor == "sectionOcclusionGraph.invalidate();":
        expected = 2
    else:
        expected = 1
    if text.count(anchor) != expected:
        raise SystemExit(f"fail-closed: authority anchor count changed for {anchor!r}: {text.count(anchor)} != {expected}")

if "LightTexture" in text or 'method = "renderLevel"' in text.split('/*', 1)[0]:
    raise SystemExit("fail-closed: active stale LevelRenderer renderLevel/LightTexture surface remains")
level_path.write_text(text, encoding="utf-8")

# Preserve upstream's block-damage behavior at the exact current owner proven from 26.2 bytecode.
extractor_source = '''package org.valkyrienskies.mod.mixin.client.renderer;

import com.llamalad7.mixinextras.injector.ModifyExpressionValue;
import net.minecraft.client.renderer.extract.LevelExtractor;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;

@Mixin(LevelExtractor.class)
public abstract class MixinLevelExtractor {

    /**
     * @reason This mixin forces the game to always render block damage.
     */
    @ModifyExpressionValue(
        method = "extractBlockDestroyAnimation",
        at = @At(value = "CONSTANT", args = "doubleValue=1024", ordinal = 0)
    )
    private double disableBlockDamageDistanceCheck(final double originalBlockDamageDistanceConstant) {
        return Double.MAX_VALUE;
    }
}
'''
if extractor_path.exists():
    raise SystemExit(f"fail-closed: unexpected pre-existing LevelExtractor VS mixin: {extractor_path}")
extractor_path.write_text(extractor_source, encoding="utf-8")

# Register exactly one new client mixin adjacent to the existing upstream LevelRenderer mixin.
mixins = mixins_path.read_text(encoding="utf-8")
if '"client.renderer.MixinLevelExtractor"' in mixins:
    raise SystemExit("fail-closed: MixinLevelExtractor already registered")
old_entry = '    "client.renderer.MixinGameRenderer",\n    "client.renderer.MixinLevelRenderer",\n'
new_entry = '    "client.renderer.MixinGameRenderer",\n    "client.renderer.MixinLevelExtractor",\n    "client.renderer.MixinLevelRenderer",\n'
mixins = replace_once(mixins, old_entry, new_entry, "client GameRenderer/LevelRenderer mixin adjacency")
if mixins.count('"client.renderer.MixinLevelExtractor"') != 1:
    raise SystemExit("fail-closed: LevelExtractor mixin registration did not converge exactly once")
mixins_path.write_text(mixins, encoding="utf-8")

print("P1_LEVELRENDERER_SPLIT_26_2_OVERLAY_APPLIED")
