#!/usr/bin/env python3
"""Fail-closed Minecraft 26.2 entity renderer dispatcher lifecycle adaptation.

Minecraft 26.2 split EntityRenderDispatcher's old entity-based render path into
extractEntity(Entity, partialTick) followed by submit(EntityRenderState, ...).
This overlay preserves the pinned upstream VS2 ship-space renderer semantics by
carrying only the original Entity + partial tick through EntityRenderState and
re-applying the upstream dispatcher transform at the new submit boundary.

It does not add movement authority, carry velocity, camera forcing, collision
substitutes, or any VS2-like replacement system. Ship transforms still come
from the real upstream ClientShip/VSEntityManager/ShipMountedToData paths.
"""

from pathlib import Path
import sys

DISPATCHER = Path("common/src/main/java/org/valkyrienskies/mod/mixin/feature/shipyard_entities/MixinEntityRenderDispatcher.java")
RENDERER = Path("common/src/main/java/org/valkyrienskies/mod/mixin/feature/shipyard_entities/MixinEntityRenderer.java")
STATE_MIXIN = Path("common/src/main/java/org/valkyrienskies/mod/mixin/feature/shipyard_entities/MixinEntityRenderState.java")
STATE_CONTEXT = Path("common/src/main/java/org/valkyrienskies/mod/mixin/feature/shipyard_entities/VSEntityRenderStateContext.java")
CULLING_INVOKER = Path("common/src/main/java/org/valkyrienskies/mod/mixin/accessors/client/render/EntityRendererCullingInvoker.java")
MIXINS = Path("common/src/main/resources/valkyrienskies-common.mixins.json")

OLD_DISPATCHER_MARKERS = (
    'import net.minecraft.client.renderer.MultiBufferSource;',
    '@Inject(method = "distanceToSqr(DDD)D"',
    '@Inject(method = "render",',
    'entity.getBoundingBoxForCulling().inflate(0.5)',
)
OLD_RENDERER_MARKERS = (
    'import net.minecraft.client.renderer.MultiBufferSource;',
    'method = "renderNameTag(',
)

DISPATCHER_CONTENT = r'''package org.valkyrienskies.mod.mixin.feature.shipyard_entities;

import com.llamalad7.mixinextras.injector.ModifyReturnValue;
import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.renderer.SubmitNodeCollector;
import net.minecraft.client.renderer.culling.Frustum;
import net.minecraft.client.renderer.entity.EntityRenderDispatcher;
import net.minecraft.client.renderer.entity.EntityRenderer;
import net.minecraft.client.renderer.entity.state.EntityRenderState;
import net.minecraft.client.renderer.state.level.CameraRenderState;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;
import org.joml.Quaternionf;
import org.joml.Vector3d;
import org.joml.Vector3dc;
import org.joml.primitives.AABBd;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;
import org.valkyrienskies.core.api.ships.ClientShip;
import org.valkyrienskies.core.api.ships.properties.ShipTransform;
import org.valkyrienskies.mod.common.VSGameUtilsKt;
import org.valkyrienskies.mod.common.entity.ShipMountedToData;
import org.valkyrienskies.mod.common.entity.handling.VSEntityManager;
import org.valkyrienskies.mod.common.util.VectorConversionsMCKt;
import org.valkyrienskies.mod.mixin.accessors.client.render.EntityRendererCullingInvoker;

@Mixin(value = EntityRenderDispatcher.class, priority = 500)
public class MixinEntityRenderDispatcher {

    @Inject(method = "distanceToSqr(Lnet/minecraft/world/entity/Entity;)D", at = @At("HEAD"), cancellable = true)
    private void preDistanceToSqr(final Entity entity, final CallbackInfoReturnable<Double> cir) {
        if (entity == null) return;
        final Vec3 pos = entity.position();
        cir.setReturnValue(VSGameUtilsKt.squaredDistanceToInclShips(entity, pos.x, pos.y, pos.z));
    }

    /**
     * Minecraft 26.2 no longer passes Entity/partialTick into the submit phase.
     * EntityRenderer.createRenderState(Entity, float) creates a fresh state for this
     * extraction, so attach only the upstream context needed by the existing VS2
     * ship-space render handler and consume it later in submit().
     */
    @Inject(method = "extractEntity", at = @At("RETURN"))
    private <E extends Entity> void vs$attachRenderContext(final E entity, final float partialTicks,
        final CallbackInfoReturnable<EntityRenderState> cir) {
        final EntityRenderState renderState = cir.getReturnValue();
        if (renderState != null) {
            ((VSEntityRenderStateContext) (Object) renderState).vs$setRenderContext(entity, partialTicks);
        }
    }

    /**
     * Port of the pinned upstream dispatcher render injection to Minecraft 26.2's
     * state submission boundary. The injection point is the direct replacement for
     * the old EntityRenderer.render invocation: vanilla has already pushed and
     * translated the pose by x/y/z + getRenderOffset(state), exactly where upstream
     * VS2 previously replaced that translation with ship-space transforms.
     */
    @Inject(
        method = "submit",
        at = @At(
            value = "INVOKE",
            target = "Lnet/minecraft/client/renderer/entity/EntityRenderer;submit(Lnet/minecraft/client/renderer/entity/state/EntityRenderState;Lcom/mojang/blaze3d/vertex/PoseStack;Lnet/minecraft/client/renderer/SubmitNodeCollector;Lnet/minecraft/client/renderer/state/level/CameraRenderState;)V",
            shift = At.Shift.BEFORE
        )
    )
    @SuppressWarnings({"rawtypes", "unchecked"})
    private <S extends EntityRenderState> void vs$submit(
        final S renderState, final CameraRenderState cameraRenderState,
        final double x, final double y, final double z,
        final PoseStack matrixStack, final SubmitNodeCollector submitNodeCollector,
        final CallbackInfo ci
    ) {
        final VSEntityRenderStateContext context = (VSEntityRenderStateContext) (Object) renderState;
        final Entity entity = context.vs$getEntity();
        if (entity == null) return;

        final float partialTicks = context.vs$getPartialTicks();
        final EntityRenderDispatcher dispatcher = (EntityRenderDispatcher) (Object) this;
        final EntityRenderer entityRenderer = dispatcher.getRenderer(renderState);
        final ShipMountedToData shipMountedToData = VSGameUtilsKt.getShipMountedToData(entity, partialTicks);

        if (shipMountedToData != null) {
            // Remove vanilla's earlier x/y/z + render-offset translation, exactly as upstream did.
            matrixStack.popPose();
            matrixStack.pushPose();

            final ShipTransform renderTransform = ((ClientShip) shipMountedToData.getShipMountedTo()).getRenderTransform();
            final Vec3 entityPosition = entity.getPosition(partialTicks);
            final Vector3dc transformed = renderTransform.getShipToWorld()
                .transformPosition(shipMountedToData.getMountPosInShip(), new Vector3d());

            final double camX = x - entityPosition.x;
            final double camY = y - entityPosition.y;
            final double camZ = z - entityPosition.z;

            final Vec3 offset = entityRenderer.getRenderOffset(renderState);
            final Vector3dc scale = renderTransform.getShipToWorldScaling();

            matrixStack.translate(transformed.x() + camX, transformed.y() + camY, transformed.z() + camZ);
            matrixStack.mulPose(new Quaternionf(renderTransform.getShipToWorldRotation()));
            matrixStack.scale((float) scale.x(), (float) scale.y(), (float) scale.z());
            matrixStack.translate(offset.x, offset.y, offset.z);
        } else {
            final ClientShip ship =
                (ClientShip) VSGameUtilsKt.getLoadedShipManagingPos(entity.level(), entity.blockPosition());
            if (ship != null) {
                // Remove vanilla's earlier translation before invoking the unchanged VS2 handler architecture.
                matrixStack.popPose();
                matrixStack.pushPose();

                VSEntityManager.INSTANCE.getHandler(entity)
                    .applyRenderTransform(ship, entity, entityRenderer, x, y, z,
                        entity.getYRot(), partialTicks, matrixStack,
                        renderState, renderState.lightCoords);
            } else if (entity.isPassenger()) {
                final ClientShip vehicleShip =
                    (ClientShip) VSGameUtilsKt.getLoadedShipManagingPos(entity.level(),
                        entity.getVehicle().blockPosition());
                if (vehicleShip != null) {
                    VSEntityManager.INSTANCE.getHandler(entity.getVehicle())
                        .applyRenderOnMountedEntity(vehicleShip, entity.getVehicle(), entity, partialTicks,
                            matrixStack);
                }
            }
        }
    }

    @ModifyReturnValue(method = "shouldRender", at = @At("RETURN"))
    boolean shouldRender(final boolean returns, final Entity entity, final Frustum frustum,
        final double camX, final double camY, final double camZ) {

        if (!returns) {
            final ClientShip ship =
                (ClientShip) VSGameUtilsKt.getLoadedShipManagingPos(entity.level(), entity.blockPosition());
            if (ship != null) {
                final EntityRenderDispatcher dispatcher = (EntityRenderDispatcher) (Object) this;
                final EntityRenderer<?, ?> renderer = dispatcher.getRenderer(entity);
                AABB aABB = ((EntityRendererCullingInvoker) (Object) renderer)
                    .vs$getBoundingBoxForCulling(entity).inflate(0.5);
                if (aABB.hasNaN() || aABB.getSize() == 0.0) {
                    aABB = new AABB(entity.getX() - 2.0, entity.getY() - 2.0,
                        entity.getZ() - 2.0, entity.getX() + 2.0,
                        entity.getY() + 2.0, entity.getZ() + 2.0);
                }
                final AABBd aabb = VectorConversionsMCKt.toJOML(aABB);
                aabb.transform(ship.getRenderTransform().getShipToWorld());
                return frustum.isVisible(VectorConversionsMCKt.toMinecraft(aabb));
            }
        }

        return returns;
    }
}
'''

RENDERER_CONTENT = r'''package org.valkyrienskies.mod.mixin.feature.shipyard_entities;

import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.renderer.SubmitNodeCollector;
import net.minecraft.client.renderer.entity.EntityRenderer;
import net.minecraft.client.renderer.entity.state.EntityRenderState;
import net.minecraft.client.renderer.state.level.CameraRenderState;
import net.minecraft.world.entity.Entity;
import org.joml.Quaternionf;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import org.valkyrienskies.core.api.ships.ClientShip;
import org.valkyrienskies.mod.common.VSGameUtilsKt;

@Mixin(EntityRenderer.class)
public class MixinEntityRenderer {
    /**
     * Upstream VS2 keeps name tags vertically readable by undoing ship rotation
     * inside the name-tag-only pose scope. Minecraft 26.2 moved name submission
     * to submitNameDisplay(state,...); inject immediately after its internal push
     * so the inverse rotation is popped again before shadows/fire/other features.
     */
    @Inject(
        method = "submitNameDisplay(Lnet/minecraft/client/renderer/entity/state/EntityRenderState;Lcom/mojang/blaze3d/vertex/PoseStack;Lnet/minecraft/client/renderer/SubmitNodeCollector;Lnet/minecraft/client/renderer/state/level/CameraRenderState;I)V",
        at = @At(
            value = "INVOKE",
            target = "Lcom/mojang/blaze3d/vertex/PoseStack;pushPose()V",
            shift = At.Shift.AFTER
        )
    )
    private void vs$revertShipRotation(final EntityRenderState renderState, final PoseStack matrices,
        final SubmitNodeCollector submitNodeCollector, final CameraRenderState cameraRenderState,
        final int verticalOffset, final CallbackInfo ci) {
        final Entity entity = ((VSEntityRenderStateContext) (Object) renderState).vs$getEntity();
        if (entity == null) return;

        final ClientShip ship =
            (ClientShip) VSGameUtilsKt.getLoadedShipManagingPos(entity.level(), entity.blockPosition());
        if (ship != null) {
            matrices.mulPose(new Quaternionf(ship.getRenderTransform().getShipToWorldRotation()).invert());
        }
    }
}
'''

STATE_CONTEXT_CONTENT = r'''package org.valkyrienskies.mod.mixin.feature.shipyard_entities;

import net.minecraft.world.entity.Entity;

/**
 * Minecraft 26.2 compatibility carrier between dispatcher extraction and submit.
 * This does not own gameplay state; it only preserves the entity/partial-tick
 * context that the pinned upstream VS2 render callback received directly.
 */
public interface VSEntityRenderStateContext {
    Entity vs$getEntity();

    float vs$getPartialTicks();

    void vs$setRenderContext(Entity entity, float partialTicks);
}
'''

STATE_MIXIN_CONTENT = r'''package org.valkyrienskies.mod.mixin.feature.shipyard_entities;

import net.minecraft.client.renderer.entity.state.EntityRenderState;
import net.minecraft.world.entity.Entity;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;

@Mixin(EntityRenderState.class)
public class MixinEntityRenderState implements VSEntityRenderStateContext {
    @Unique
    private Entity vs$entity;

    @Unique
    private float vs$partialTicks;

    @Override
    public Entity vs$getEntity() {
        return vs$entity;
    }

    @Override
    public float vs$getPartialTicks() {
        return vs$partialTicks;
    }

    @Override
    public void vs$setRenderContext(final Entity entity, final float partialTicks) {
        this.vs$entity = entity;
        this.vs$partialTicks = partialTicks;
    }
}
'''

CULLING_INVOKER_CONTENT = r'''package org.valkyrienskies.mod.mixin.accessors.client.render;

import net.minecraft.client.renderer.entity.EntityRenderer;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.phys.AABB;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.gen.Invoker;

/** Preserve the renderer-specific Minecraft 26.2 culling box used by vanilla. */
@Mixin(EntityRenderer.class)
public interface EntityRendererCullingInvoker {
    @Invoker("getBoundingBoxForCulling")
    AABB vs$getBoundingBoxForCulling(Entity entity);
}
'''


def require_once(text: str, needle: str, path: Path) -> None:
    count = text.count(needle)
    if count != 1:
        raise SystemExit(f"fail-closed: expected exactly one {needle!r} in {path}, found {count}")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {sys.argv[0]} <upstream-vs2-root>")

    root = Path(sys.argv[1])
    dispatcher_path = root / DISPATCHER
    renderer_path = root / RENDERER
    mixins_path = root / MIXINS

    dispatcher = dispatcher_path.read_text(encoding="utf-8")
    renderer = renderer_path.read_text(encoding="utf-8")
    mixins = mixins_path.read_text(encoding="utf-8")

    for marker in OLD_DISPATCHER_MARKERS:
        if marker not in dispatcher:
            raise SystemExit(f"fail-closed: pinned dispatcher marker missing: {marker!r}")
    for marker in OLD_RENDERER_MARKERS:
        if marker not in renderer:
            raise SystemExit(f"fail-closed: pinned renderer marker missing: {marker!r}")

    for relative in (STATE_MIXIN, STATE_CONTEXT, CULLING_INVOKER):
        if (root / relative).exists():
            raise SystemExit(f"fail-closed: compatibility source already exists unexpectedly: {relative}")

    accessor_anchor = '    "accessors.client.render.LevelRendererAccessor",\n'
    dispatcher_anchor = '    "feature.shipyard_entities.MixinEntityRenderDispatcher",\n'
    require_once(mixins, accessor_anchor, MIXINS)
    require_once(mixins, dispatcher_anchor, MIXINS)
    if "EntityRendererCullingInvoker" in mixins or "MixinEntityRenderState" in mixins:
        raise SystemExit("fail-closed: renderer 26.2 compatibility mixins already registered")

    dispatcher_path.write_text(DISPATCHER_CONTENT, encoding="utf-8")
    renderer_path.write_text(RENDERER_CONTENT, encoding="utf-8")

    for relative, content in (
        (STATE_CONTEXT, STATE_CONTEXT_CONTENT),
        (STATE_MIXIN, STATE_MIXIN_CONTENT),
        (CULLING_INVOKER, CULLING_INVOKER_CONTENT),
    ):
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    mixins = mixins.replace(
        accessor_anchor,
        accessor_anchor + '    "accessors.client.render.EntityRendererCullingInvoker",\n',
        1,
    )
    mixins = mixins.replace(
        dispatcher_anchor,
        dispatcher_anchor + '    "feature.shipyard_entities.MixinEntityRenderState",\n',
        1,
    )
    mixins_path.write_text(mixins, encoding="utf-8")

    final_dispatcher = dispatcher_path.read_text(encoding="utf-8")
    final_renderer = renderer_path.read_text(encoding="utf-8")
    forbidden = (
        "MultiBufferSource",
        'distanceToSqr(DDD)D',
        'method = "render",',
        "getBoundingBoxForCulling().inflate",
        "renderNameTag(",
    )
    combined = final_dispatcher + "\n" + final_renderer
    for token in forbidden:
        if token in combined:
            raise SystemExit(f"fail-closed: legacy renderer token remains after adaptation: {token!r}")

    required = (
        "extractEntity",
        "EntityRenderState",
        "SubmitNodeCollector",
        "VSEntityRenderStateContext",
        "getShipMountedToData",
        "VSEntityManager.INSTANCE.getHandler",
        "getRenderTransform",
        "EntityRendererCullingInvoker",
        "submitNameDisplay",
    )
    for token in required:
        if token not in combined + mixins:
            raise SystemExit(f"fail-closed: required upstream/26.2 renderer token missing after adaptation: {token!r}")

    print("P1_ENTITY_RENDERER_SUBMIT_26_2_OVERLAY_APPLIED")


if __name__ == "__main__":
    main()
