#!/usr/bin/env python3
from pathlib import Path
import hashlib
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")

TARGETS = {
    "common/src/main/java/org/valkyrienskies/mod/mixin/feature/render_blockentity_distance_check/MixinBlockEntityRenderDispatcher.java": {
        "blob": "efa6689323dd93e5b5b57bb3ab9da3c513fd4c69",
        "replacements": [
            ("this.camera.getPosition()", "this.camera.position()", 1),
        ],
        "anchors": [
            ("VSGameUtilsKt.getLoadedShipManagingPos(level, bePos)", 1),
            ("ship.getRenderTransform().getShipToWorld()", 1),
            ("instance.getViewDistance()", 1),
        ],
    },
    "common/src/main/java/org/valkyrienskies/mod/mixin/client/renderer/MixinGameRenderer.java": {
        "blob": "48b9592d2ec98b38b541db1edd9e5d2c17fcf160",
        "replacements": [
            ("camera.getPosition()", "camera.position()", 1),
            ("this.mainCamera.getPosition()", "this.mainCamera.position()", 1),
        ],
        "anchors": [
            ("((IVSCamera) camera).setupWithShipMounted(", 1),
            ("rotationMatrix.set(newRotationMatrix);", 1),
            ("prepareCullFrustum.call(instance,", 5),
            ("VSGameUtilsKt.getShipObjectWorld(Minecraft.getInstance()).getLoadedShips()", 1),
        ],
    },
}


def git_blob_sha(text: str) -> str:
    raw = text.encode("utf-8")
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


changed = 0
for rel, spec in TARGETS.items():
    path = root / rel
    if not path.is_file():
        raise SystemExit(f"fail-closed: expected pinned VS2 source missing: {path}")
    text = path.read_text(encoding="utf-8")
    actual_blob = git_blob_sha(text)
    if actual_blob != spec["blob"]:
        raise SystemExit(
            f"fail-closed: unexpected pinned blob for {rel}: {actual_blob}; expected {spec['blob']}"
        )

    for token, count in spec["anchors"]:
        actual = text.count(token)
        if actual != count:
            raise SystemExit(f"fail-closed: authority anchor {token!r} in {rel}: {actual} != {count}")

    for old, new, count in spec["replacements"]:
        actual = text.count(old)
        if actual != count:
            raise SystemExit(f"fail-closed: expected {count} occurrences of {old!r} in {rel}, found {actual}")
        if new in text:
            raise SystemExit(f"fail-closed: replacement already present in pinned source {rel}: {new!r}")
        text = text.replace(old, new, count)
        changed += count

    for token, count in spec["anchors"]:
        if text.count(token) != count:
            raise SystemExit(f"fail-closed: authority anchor changed unexpectedly in {rel}: {token!r}")
    path.write_text(text, encoding="utf-8")

if changed != 3:
    raise SystemExit(f"fail-closed: expected exactly 3 Camera position accessor adaptations, got {changed}")

print("P1_CAMERA_POSITION_ACCESSOR_26_2_OVERLAY_APPLIED count=3 files=2")
