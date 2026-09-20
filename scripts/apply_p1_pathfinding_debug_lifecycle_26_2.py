#!/usr/bin/env python3
"""Adapt upstream VS2 pathfinding debug rendering to Minecraft 26.2's vanilla gizmo lifecycle.

Exact 26.2 API proof is recorded by P1 Pathfinding Debug API inspection run 35494083822.
This overlay preserves the upstream VS config as the extra-enable authority while delegating
all actual debug-data access and rendering to vanilla DebugRenderer's SimpleDebugRenderer /
DebugValueAccess / gizmo dispatch. It never calls PathfindingRenderer directly.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/feature/render_pathfinding/MixinDebugRenderer.java"

old = '''package org.valkyrienskies.mod.mixin.feature.render_pathfinding;

import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.renderer.MultiBufferSource.BufferSource;
import net.minecraft.client.renderer.debug.DebugRenderer;
import net.minecraft.client.renderer.debug.PathfindingRenderer;
import org.spongepowered.asm.mixin.Final;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import org.valkyrienskies.mod.common.config.VSGameConfig;

@Mixin(DebugRenderer.class)
public class MixinDebugRenderer {

    @Shadow
    @Final
    public PathfindingRenderer pathfindingRenderer;

    @Inject(method = "render", at = @At("HEAD"))
    void render(
        final PoseStack matrixStack,
        final BufferSource buffer,
        final double camX, final double camY, final double camZ,
        final CallbackInfo ci) {
        if (VSGameConfig.COMMON.ADVANCED.getRenderPathfinding()) {
            pathfindingRenderer.render(matrixStack, buffer, camX, camY, camZ);
        }
    }

}
'''

new = '''package org.valkyrienskies.mod.mixin.feature.render_pathfinding;

import java.util.List;
import net.minecraft.client.renderer.culling.Frustum;
import net.minecraft.client.renderer.debug.DebugRenderer;
import net.minecraft.client.renderer.debug.PathfindingRenderer;
import org.spongepowered.asm.mixin.Final;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import org.valkyrienskies.mod.common.config.VSGameConfig;

@Mixin(DebugRenderer.class)
public class MixinDebugRenderer {

    @Shadow
    @Final
    private List<DebugRenderer.SimpleDebugRenderer> renderers;

    @Unique
    private PathfindingRenderer vs$ownedPathfindingRenderer;

    @Inject(
        method = "emitGizmos",
        at = @At(
            value = "INVOKE",
            target = "Ljava/util/List;iterator()Ljava/util/Iterator;",
            ordinal = 0,
            shift = At.Shift.BEFORE
        )
    )
    private void vs$beforeDebugRendererIteration(
        final Frustum frustum,
        final double camX, final double camY, final double camZ,
        final float partialTick,
        final CallbackInfo ci) {
        if (VSGameConfig.COMMON.ADVANCED.getRenderPathfinding()) {
            final boolean pathfindingAlreadyPresent =
                renderers.stream().anyMatch(PathfindingRenderer.class::isInstance);
            if (!pathfindingAlreadyPresent) {
                if (vs$ownedPathfindingRenderer == null) {
                    vs$ownedPathfindingRenderer = new PathfindingRenderer();
                }
                renderers.add(vs$ownedPathfindingRenderer);
            }
        } else if (vs$ownedPathfindingRenderer != null) {
            renderers.remove(vs$ownedPathfindingRenderer);
        }
    }

}
'''

text = path.read_text(encoding="utf-8")
if text != old:
    raise SystemExit(
        "fail-closed: pinned upstream pathfinding debug mixin no longer matches exact expected source"
    )
path.write_text(new, encoding="utf-8")
print("P1_PATHFINDING_DEBUG_LIFECYCLE_26_2_OVERLAY_APPLIED")
