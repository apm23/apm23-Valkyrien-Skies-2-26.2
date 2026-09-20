#!/usr/bin/env python3
from pathlib import Path
import hashlib
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
rel = "common/src/main/java/org/valkyrienskies/mod/mixin/feature/fix_render_chunk_sorting/MixinRenderChunk.java"
path = root / rel
text = path.read_text(encoding="utf-8")

raw = text.encode("utf-8")
blob_sha = hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()
expected_blob = "d58f5271eb14269a9edacfdb9de7187048ebbbdc"
if blob_sha != expected_blob:
    raise SystemExit(f"fail-closed: unexpected pinned render-chunk-sorting blob {blob_sha}; expected {expected_blob}")

old_camera = "Minecraft.getInstance().gameRenderer.getMainCamera()"
new_camera = "Minecraft.getInstance().gameRenderer.mainCamera()"
old_pos = "camera.getPosition()"
new_pos = "camera.position()"
if text.count(old_camera) != 1:
    raise SystemExit(f"fail-closed: expected one GameRenderer.getMainCamera() call, found {text.count(old_camera)}")
if text.count(old_pos) != 3:
    raise SystemExit(f"fail-closed: expected three Camera.getPosition() calls, found {text.count(old_pos)}")
if new_camera in text or new_pos in text:
    raise SystemExit("fail-closed: render-chunk camera vocabulary already adapted before this helper")

# Preserve the original VS2 render-sorting authority and ship/world distance semantics.
anchors = [
    ("VSGameUtilsKt.getLoadedShipManagingPos(world, origin)", 1),
    ("shipObject.getRenderTransform().getShipToWorldMatrix().transformPosition(", 1),
    ("new Vector3d(bb.minX + 8.0, bb.minY + 8.0, bb.minZ + 8.0)", 1),
    ("cir.setReturnValue(relDistanceSq);", 1),
    ("VSGameUtilsKt.isBlockInShipyard(world, origin)", 1),
]
for token, count in anchors:
    actual = text.count(token)
    if actual != count:
        raise SystemExit(f"fail-closed: authority anchor {token!r}: {actual} != {count}")

text = text.replace(old_camera, new_camera, 1)
text = text.replace(old_pos, new_pos, 3)

if old_camera in text or old_pos in text or text.count(new_camera) != 1 or text.count(new_pos) != 3:
    raise SystemExit("fail-closed: render-chunk camera API adaptation did not converge exactly")
for token, count in anchors:
    if text.count(token) != count:
        raise SystemExit(f"fail-closed: authority anchor changed unexpectedly: {token!r}")

path.write_text(text, encoding="utf-8")
print("P1_RENDER_CHUNK_SORTING_CAMERA_26_2_OVERLAY_APPLIED count=4")
