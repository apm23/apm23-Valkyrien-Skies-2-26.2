#!/usr/bin/env python3
from pathlib import Path
import hashlib
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "common/src/main/java/org/valkyrienskies/mod/mixin/feature/render_ship_debug_bb/MixinDebugRenderer.java"
text = path.read_text(encoding="utf-8")

EXPECTED_GIT_BLOB_SHA1 = "cf32d6c149591f19aa1acd6e885f9701bb6f8cf1"

def git_blob_sha1(value: str) -> str:
    data = value.encode("utf-8")
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()

actual_blob = git_blob_sha1(text)
if actual_blob != EXPECTED_GIT_BLOB_SHA1:
    raise SystemExit(
        f"fail-closed: expected exact pinned ship-debug-BB source blob {EXPECTED_GIT_BLOB_SHA1}, got {actual_blob} at {path}"
    )

required_upstream_anchors = [
    '@Mixin(DebugRenderer.class)',
    '@Inject(method = "render", at = @At("HEAD"))',
    'final MultiBufferSource.BufferSource bufferSource',
    'bufferSource.getBuffer(RenderType.lines())',
    'VSClientGameUtils.transformRenderWithShip(',
    'shipObjectClient.getShipAABB()',
    'shipObjectClient.getRenderAABB()',
    'Minecraft.getInstance().getEntityRenderDispatcher().shouldRenderHitBoxes()',
]
for anchor in required_upstream_anchors:
    if text.count(anchor) < 1:
        raise SystemExit(f"fail-closed: pinned upstream authority anchor missing: {anchor!r}")

target = '''package org.valkyrienskies.mod.mixin.feature.render_ship_debug_bb;

import net.minecraft.client.Minecraft;
import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.client.renderer.culling.Frustum;
import net.minecraft.client.renderer.debug.DebugRenderer;
import net.minecraft.gizmos.GizmoStyle;
import net.minecraft.gizmos.Gizmos;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;
import org.joml.Vector3d;
import org.joml.Vector3dc;
import org.joml.primitives.AABBdc;
import org.joml.primitives.AABBic;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import org.valkyrienskies.core.api.ships.ClientShip;
import org.valkyrienskies.core.api.ships.properties.ShipTransform;
import org.valkyrienskies.core.internal.world.VsiClientShipWorld;
import org.valkyrienskies.mod.common.VSGameUtilsKt;
import org.valkyrienskies.mod.common.util.VectorConversionsMCKt;

@Mixin(DebugRenderer.class)
public class MixinDebugRenderer {

    @Unique
    private static final int VS$CENTER_OF_MASS_COLOR = 0xFFFAC213;
    @Unique
    private static final int VS$VOXEL_AABB_COLOR = 0xFFFF0000;
    @Unique
    private static final int VS$RENDER_AABB_COLOR = 0xFFEA00D9;
    @Unique
    private static final float VS$DEBUG_LINE_WIDTH = 2.5F;

    /**
     * Render the original VS2 ship debug bounds through Minecraft 26.2's gizmo pass.
     *
     * <p>The center-of-mass and render AABBs are already world-space boxes and can be
     * delegated directly to vanilla Gizmos. The ship voxel AABB is ship-space and may
     * be rotated, so its eight corners are transformed with the original ship render
     * transform and its twelve edges are emitted as vanilla gizmo lines.</p>
     */
    @Inject(method = "emitGizmos", at = @At("TAIL"))
    private void postRender(final Frustum frustum, final double cameraX, final double cameraY,
        final double cameraZ, final float partialTick, final CallbackInfo ci) {
        final ClientLevel world = Minecraft.getInstance().level;
        final VsiClientShipWorld shipObjectClientWorld = VSGameUtilsKt.getShipObjectWorld(world);

        if (Minecraft.getInstance().getEntityRenderDispatcher().shouldRenderHitBoxes()) {
            for (final ClientShip shipObjectClient : shipObjectClientWorld.getLoadedShips()) {
                final ShipTransform shipRenderTransform = shipObjectClient.getRenderTransform();
                final Vector3dc shipRenderPosition = shipRenderTransform.getShipPositionInWorldCoordinates();

                final double renderRadius = .25;
                final AABB shipCenterOfMassBox =
                    new AABB(shipRenderPosition.x() - renderRadius, shipRenderPosition.y() - renderRadius,
                        shipRenderPosition.z() - renderRadius, shipRenderPosition.x() + renderRadius,
                        shipRenderPosition.y() + renderRadius, shipRenderPosition.z() + renderRadius);
                Gizmos.cuboid(shipCenterOfMassBox, GizmoStyle.stroke(VS$CENTER_OF_MASS_COLOR));

                // Render the ship's voxel AABB without losing ship rotation.
                final AABBic shipVoxelAABBic = shipObjectClient.getShipAABB();
                if (shipVoxelAABBic != null) {
                    final AABB shipVoxelAABB = new AABB(
                        shipVoxelAABBic.minX(), shipVoxelAABBic.minY(), shipVoxelAABBic.minZ(),
                        shipVoxelAABBic.maxX(), shipVoxelAABBic.maxY(), shipVoxelAABBic.maxZ()
                    );
                    vs$renderTransformedLineBox(shipVoxelAABB, shipRenderTransform, VS$VOXEL_AABB_COLOR);
                }

                // Render the ship's render AABB. This value is already world-space.
                final AABBdc shipRenderAABBdc = shipObjectClient.getRenderAABB();
                final AABB shipRenderAABB = VectorConversionsMCKt.toMinecraft(shipRenderAABBdc);
                Gizmos.cuboid(shipRenderAABB, GizmoStyle.stroke(VS$RENDER_AABB_COLOR));
            }
        }
    }

    @Unique
    private static void vs$renderTransformedLineBox(final AABB box, final ShipTransform transform, final int color) {
        final Vec3 p000 = vs$toWorld(transform, box.minX, box.minY, box.minZ);
        final Vec3 p100 = vs$toWorld(transform, box.maxX, box.minY, box.minZ);
        final Vec3 p010 = vs$toWorld(transform, box.minX, box.maxY, box.minZ);
        final Vec3 p110 = vs$toWorld(transform, box.maxX, box.maxY, box.minZ);
        final Vec3 p001 = vs$toWorld(transform, box.minX, box.minY, box.maxZ);
        final Vec3 p101 = vs$toWorld(transform, box.maxX, box.minY, box.maxZ);
        final Vec3 p011 = vs$toWorld(transform, box.minX, box.maxY, box.maxZ);
        final Vec3 p111 = vs$toWorld(transform, box.maxX, box.maxY, box.maxZ);

        vs$line(p000, p100, color);
        vs$line(p100, p110, color);
        vs$line(p110, p010, color);
        vs$line(p010, p000, color);

        vs$line(p001, p101, color);
        vs$line(p101, p111, color);
        vs$line(p111, p011, color);
        vs$line(p011, p001, color);

        vs$line(p000, p001, color);
        vs$line(p100, p101, color);
        vs$line(p110, p111, color);
        vs$line(p010, p011, color);
    }

    @Unique
    private static Vec3 vs$toWorld(final ShipTransform transform, final double x, final double y, final double z) {
        final Vector3d point = new Vector3d(x, y, z);
        transform.getShipToWorld().transformPosition(point);
        return new Vec3(point.x(), point.y(), point.z());
    }

    @Unique
    private static void vs$line(final Vec3 from, final Vec3 to, final int color) {
        Gizmos.line(from, to, color, VS$DEBUG_LINE_WIDTH);
    }
}
'''

path.write_text(target, encoding="utf-8")
rewritten = path.read_text(encoding="utf-8")

required_26_2_anchors = [
    '@Inject(method = "emitGizmos", at = @At("TAIL"))',
    'Gizmos.cuboid(shipCenterOfMassBox, GizmoStyle.stroke(VS$CENTER_OF_MASS_COLOR));',
    'vs$renderTransformedLineBox(shipVoxelAABB, shipRenderTransform, VS$VOXEL_AABB_COLOR);',
    'transform.getShipToWorld().transformPosition(point);',
    'Gizmos.cuboid(shipRenderAABB, GizmoStyle.stroke(VS$RENDER_AABB_COLOR));',
    'Gizmos.line(from, to, color, VS$DEBUG_LINE_WIDTH);',
    'Minecraft.getInstance().getEntityRenderDispatcher().shouldRenderHitBoxes()',
]
for anchor in required_26_2_anchors:
    if rewritten.count(anchor) != 1:
        raise SystemExit(f"fail-closed: expected exactly one adapted authority anchor {anchor!r}, found {rewritten.count(anchor)}")

for forbidden in (
    'MultiBufferSource',
    'RenderType',
    'LevelRenderer.renderLineBox',
    'VSClientGameUtils.transformRenderWithShip',
    '@Inject(method = "render"',
    'bufferSource.endBatch()',
):
    if forbidden in rewritten:
        raise SystemExit(f"fail-closed: obsolete pre-26.2 render authority survived: {forbidden!r}")

print("P1_SHIP_DEBUG_BB_GIZMO_26_2_OVERLAY_APPLIED")
