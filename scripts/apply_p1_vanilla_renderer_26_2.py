#!/usr/bin/env python3
from pathlib import Path
import subprocess, sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
rel = "common/src/main/java/org/valkyrienskies/mod/mixin/mod_compat/vanilla_renderer/MixinLevelRendererVanilla.java"
path = root / rel
expected = "824e1ac56a99bc6480cc80c32c085d18c2425b09"
actual = subprocess.check_output(["git", "-C", str(root), "hash-object", rel], text=True).strip()
if actual != expected:
    raise SystemExit(f"fail-closed: vanilla renderer upstream drift: expected {expected}, got {actual}")
old = path.read_text(encoding="utf-8")
for anchor in (
    "VSGameUtilsKt.squaredDistanceBetweenInclShips(",
    "public void vs$addShipVisibleChunks(final Frustum frustum)",
    "shipObject.getRenderTransform().getShipToWorld()",
    "VSClientGameUtils.transformRenderWithShip(",
    "private void redirectRenderChunkLayer(",
    "ShaderInstance shaderInstance = RenderSystem.getShader();",
    "VertexBuffer vertexBuffer = renderChunk.getBuffer(renderType);",
):
    if anchor not in old:
        raise SystemExit(f"fail-closed: pinned renderer anchor missing: {anchor!r}")

new = r'''package org.valkyrienskies.mod.mixin.mod_compat.vanilla_renderer;

import com.llamalad7.mixinextras.injector.wrapoperation.Operation;
import com.llamalad7.mixinextras.injector.wrapoperation.WrapOperation;
import com.mojang.blaze3d.vertex.PoseStack;
import it.unimi.dsi.fastutil.objects.ObjectArrayList;
import java.util.WeakHashMap;
import net.minecraft.client.Minecraft;
import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.client.renderer.LevelRenderer;
import net.minecraft.client.renderer.SubmitNodeCollector;
import net.minecraft.client.renderer.ViewArea;
import net.minecraft.client.renderer.chunk.ChunkSectionsToRender;
import net.minecraft.client.renderer.chunk.SectionRenderDispatcher;
import net.minecraft.client.renderer.culling.Frustum;
import net.minecraft.client.renderer.state.level.LevelRenderState;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Vec3i;
import net.minecraft.world.level.chunk.LevelChunk;
import net.minecraft.world.level.chunk.LevelChunkSection;
import net.minecraft.world.phys.Vec3;
import org.jetbrains.annotations.Nullable;
import org.joml.Matrix4f;
import org.joml.Matrix4fc;
import org.joml.primitives.AABBd;
import org.spongepowered.asm.mixin.Final;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.ModifyArgs;
import org.spongepowered.asm.mixin.injection.Redirect;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;
import org.spongepowered.asm.mixin.injection.invoke.arg.Args;
import org.valkyrienskies.core.api.ships.ClientShip;
import org.valkyrienskies.core.api.ships.Ship;
import org.valkyrienskies.core.util.datastructures.BlockPos2ByteOpenHashMap;
import org.valkyrienskies.mod.common.VSClientGameUtils;
import org.valkyrienskies.mod.common.VSGameUtilsKt;
import org.valkyrienskies.mod.common.assembly.SeamlessChunksManager;
import org.valkyrienskies.mod.common.config.ShipRenderer;
import org.valkyrienskies.mod.common.config.ShipRendererKt;
import org.valkyrienskies.mod.common.util.VectorConversionsMCKt;
import org.valkyrienskies.mod.mixinducks.client.render.IVSViewAreaMethods;
import org.valkyrienskies.mod.mixinducks.client.render.LevelRendererVanillaDuck;
import org.valkyrienskies.mod.mixinducks.mod_compat.vanilla_renderer.LevelRendererDuck;

@Mixin(value = LevelRenderer.class, priority = 999)
public abstract class MixinLevelRendererVanilla implements LevelRendererDuck, LevelRendererVanillaDuck {
    @Unique
    private final WeakHashMap<ClientShip, ObjectArrayList<SectionRenderDispatcher.RenderSection>> vs$shipRenderChunks = new WeakHashMap<>();
    @Shadow @Final private ObjectArrayList<SectionRenderDispatcher.RenderSection> visibleSections;
    @Shadow private @Nullable ViewArea viewArea;
    @Shadow @Final private LevelRenderState levelRenderState;
    @Unique private BlockPos2ByteOpenHashMap vs$visibileShipChunks = new BlockPos2ByteOpenHashMap();

    @Unique
    private @Nullable ClientLevel vs$getClientLevel() {
        return Minecraft.getInstance().level;
    }

    @Redirect(
        method = "compileSections",
        at = @At(value = "INVOKE", target = "Lnet/minecraft/core/BlockPos;distSqr(Lnet/minecraft/core/Vec3i;)D"),
        require = 0
    )
    private double includeShipChunksInNearChunks(final BlockPos b, final Vec3i v) {
        final ClientLevel level = vs$getClientLevel();
        if (level == null) return b.distSqr(v);
        return VSGameUtilsKt.squaredDistanceBetweenInclShips(
            level, b.getX(), b.getY(), b.getZ(), v.getX(), v.getY(), v.getZ()
        );
    }

    @Override
    public void vs$setNeedsFrustumUpdate() {
        // Pinned upstream already made this a no-op after the 1.21 renderer invalidation change.
    }

    @Inject(method = "prepareChunkRenders", at = @At("HEAD"))
    private void vs$prepareVisibleShipSections(
        final Matrix4fc modelView,
        final CallbackInfoReturnable<ChunkSectionsToRender> cir
    ) {
        final SeamlessChunksManager manager = SeamlessChunksManager.get();
        if (manager != null) manager.drainDeferredBatch();

        vs$shipRenderChunks.forEach((ship, chunks) -> {
            chunks.forEach(visibleSections::remove);
            chunks.clear();
        });
        vs$visibileShipChunks = new BlockPos2ByteOpenHashMap();

        if (levelRenderState != null && levelRenderState.cameraRenderState != null) {
            vs$addShipVisibleChunks(levelRenderState.cameraRenderState.cullFrustum);
        }
    }

    @Override
    public void vs$addShipVisibleChunks(final Frustum frustum) {
        final ClientLevel level = vs$getClientLevel();
        if (level == null || viewArea == null || frustum == null) return;

        final IVSViewAreaMethods shipViewArea = (IVSViewAreaMethods) viewArea;
        for (final ClientShip shipObject : VSGameUtilsKt.getShipObjectWorld(level).getLoadedShips()) {
            if (ShipRendererKt.getShipRenderer(shipObject) != ShipRenderer.VANILLA) continue;
            if (!frustum.isVisible(VectorConversionsMCKt.toMinecraft(shipObject.getRenderAABB()))) continue;

            shipObject.getActiveChunksSet().forEach((x, z) -> {
                final LevelChunk levelChunk = level.getChunk(x, z);
                for (int y = level.getMinSection(); y < level.getMaxSection(); y++) {
                    if (vs$visibileShipChunks.contains(x, y, z)) continue;
                    final LevelChunkSection section = levelChunk.getSection(y - level.getMinSection());
                    if (section.hasOnlyAir()) continue;

                    SectionRenderDispatcher.RenderSection renderChunk = shipViewArea.vs$getShipRenderSection(x, y, z);
                    if (renderChunk == null) renderChunk = shipViewArea.vs$getOrCreateShipRenderSection(x, y, z);
                    if (renderChunk == null) continue;

                    final AABBd bounds = new AABBd(
                        (x << 4) - 6e-1, (y << 4) - 6e-1, (z << 4) - 6e-1,
                        (x << 4) + 15.6, (y << 4) + 15.6, (z << 4) + 15.6
                    ).transform(shipObject.getRenderTransform().getShipToWorld());
                    if (!frustum.isVisible(VectorConversionsMCKt.toMinecraft(bounds))) continue;

                    vs$shipRenderChunks.computeIfAbsent(shipObject, k -> new ObjectArrayList<>()).add(renderChunk);
                    vs$visibileShipChunks.put(x, y, z, (byte) 1);
                    visibleSections.add(renderChunk);
                }
            });
        }
    }

    @ModifyArgs(
        method = "prepareChunkRenders",
        at = @At(
            value = "INVOKE",
            target = "Lnet/minecraft/client/renderer/DynamicUniforms$ChunkSectionInfo;<init>(Lorg/joml/Matrix4fc;IIIFII)V"
        )
    )
    private void vs$transformShipChunkUniform(final Args args) {
        final ClientLevel level = vs$getClientLevel();
        if (level == null || levelRenderState == null || levelRenderState.cameraRenderState == null) return;

        final int x = (Integer) args.get(1);
        final int y = (Integer) args.get(2);
        final int z = (Integer) args.get(3);
        final Ship ship = VSGameUtilsKt.getShipManagingPos(level, x, y, z);
        if (!(ship instanceof final ClientShip clientShip)) return;
        if (ShipRendererKt.getShipRenderer(clientShip) != ShipRenderer.VANILLA) return;

        final Vec3 cameraPos = levelRenderState.cameraRenderState.pos;
        final Matrix4f shipModelView = new Matrix4f((Matrix4fc) args.get(0));
        VSClientGameUtils.transformRenderWithShip(
            clientShip.getRenderTransform(), shipModelView,
            cameraPos.x, cameraPos.y, cameraPos.z,
            cameraPos.x, cameraPos.y, cameraPos.z
        );
        args.set(0, shipModelView);
    }

    @WrapOperation(
        method = "submitBlockEntities",
        at = @At(value = "INVOKE", target = "Lcom/mojang/blaze3d/vertex/PoseStack;translate(DDD)V")
    )
    private void vs$fixBlockEntityTransform(
        final PoseStack instance,
        final double renderX,
        final double renderY,
        final double renderZ,
        final Operation<Void> original,
        final PoseStack methodPoseStack,
        final LevelRenderState renderState,
        final SubmitNodeCollector collector
    ) {
        final ClientLevel level = vs$getClientLevel();
        if (level == null || renderState == null || renderState.cameraRenderState == null) {
            original.call(instance, renderX, renderY, renderZ);
            return;
        }
        final Vec3 cam = renderState.cameraRenderState.pos;
        final double x = renderX + cam.x;
        final double y = renderY + cam.y;
        final double z = renderZ + cam.z;
        final Ship ship = VSGameUtilsKt.getShipManagingPos(level, x, y, z);
        if (ship instanceof final ClientShip clientShip) {
            VSClientGameUtils.transformRenderWithShip(
                clientShip.getRenderTransform(), instance,
                x, y, z, cam.x, cam.y, cam.z
            );
        } else {
            original.call(instance, renderX, renderY, renderZ);
        }
    }
}
'''

for obsolete in ("ShaderInstance", "VertexBuffer", "Uniform", "renderSectionLayer", "LightTexture", "RenderSystem"):
    if obsolete in new:
        raise SystemExit(f"fail-closed: obsolete renderer authority leaked into overlay: {obsolete}")
for anchor in (
    'method = "prepareChunkRenders"',
    'DynamicUniforms$ChunkSectionInfo;<init>(Lorg/joml/Matrix4fc;IIIFII)V',
    'levelRenderState.cameraRenderState.cullFrustum',
    'VSClientGameUtils.transformRenderWithShip(',
    'method = "submitBlockEntities"',
    'VSGameUtilsKt.squaredDistanceBetweenInclShips(',
    'shipObject.getRenderTransform().getShipToWorld()',
):
    if anchor not in new:
        raise SystemExit(f"fail-closed: new renderer semantic anchor missing: {anchor!r}")
path.write_text(new, encoding="utf-8")
print("P1_VANILLA_RENDERER_26_2_OVERLAY_APPLIED")
