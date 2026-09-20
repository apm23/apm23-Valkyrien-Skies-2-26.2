#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
rel = "common/src/main/java/org/valkyrienskies/mod/mixin/world/level/levelgen/MixinNoiseBasedChunkGenerator.java"
path = root / rel
text = path.read_text(encoding="utf-8")

old = "levelHeightAccessor.getMinBuildHeight()"
new = "levelHeightAccessor.getMinY()"
if text.count(old) != 1:
    raise SystemExit(f"fail-closed: expected one {old!r} in {rel}, found {text.count(old)}")
if new in text:
    raise SystemExit(f"fail-closed: height accessor already adapted before this helper in {rel}")

# This helper runs after the canonical ChunkPos-record overlay; anchor that exact
# mechanical predecessor state and preserve the original VS2 shipyard-generation authority.
predecessor_anchors = [
    ("chunkPos.x()", 4),
    ("chunkPos.z()", 4),
]
authority_anchors = [
    ("VS2ChunkAllocator.INSTANCE.isChunkInShipyardCompanion(i, j)", 1),
    ("this.settings.value().noiseSettings()", 1),
    ("cir.setReturnValue(new NoiseColumn(k, new BlockState[0]));", 1),
    ("cir.setReturnValue(CompletableFuture.completedFuture(chunkAccess));", 1),
]
for token, count in predecessor_anchors + authority_anchors:
    actual = text.count(token)
    if actual != count:
        raise SystemExit(f"fail-closed: expected {count} occurrences of anchor {token!r} in {rel}, found {actual}")

text = text.replace(old, new, 1)

if old in text or text.count(new) != 1:
    raise SystemExit("fail-closed: NoiseBasedChunkGenerator height accessor adaptation did not converge exactly")
for token, count in predecessor_anchors + authority_anchors:
    if text.count(token) != count:
        raise SystemExit(f"fail-closed: authority/predecessor anchor changed unexpectedly: {token!r}")

path.write_text(text, encoding="utf-8")
print("P1_NOISEBASED_HEIGHT_ACCESSOR_26_2_OVERLAY_APPLIED count=1")
