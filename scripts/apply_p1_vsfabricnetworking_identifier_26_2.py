#!/usr/bin/env python3
"""Adapt only Fabric VSFabricNetworking resource identifiers to Minecraft 26.2 Identifier.

Exact-head P1 compile at c5749ea1... leaves nine diagnostics in VSFabricNetworking.kt:
five ResourceLocation vocabulary diagnostics and four independent PayloadTypeRegistry
playC2S/playS2C API diagnostics. This unit changes only the already-frozen Minecraft 26.2
ResourceLocation -> Identifier vocabulary for the two VS packet IDs. Networking registration,
fragmentation, handlers, codecs, and PayloadTypeRegistry calls remain untouched.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream-vs2")
path = root / "fabric/src/main/kotlin/org/valkyrienskies/mod/fabric/common/VSFabricNetworking.kt"
if not path.is_file():
    raise SystemExit(f"fail-closed: pinned VSFabricNetworking source missing: {path}")

text = path.read_text(encoding="utf-8")
old_import = "import net.minecraft.resources.ResourceLocation"
new_import = "import net.minecraft.resources.Identifier"
old_packet = 'val VS_PACKET_RL: ResourceLocation = ResourceLocation.fromNamespaceAndPath(ValkyrienSkiesMod.MOD_ID, "vs_packet")'
new_packet = 'val VS_PACKET_RL: Identifier = Identifier.fromNamespaceAndPath(ValkyrienSkiesMod.MOD_ID, "vs_packet")'
old_fragment = 'val VS_FRAGMENT_RL: ResourceLocation = ResourceLocation.fromNamespaceAndPath(ValkyrienSkiesMod.MOD_ID, "vs_fragment")'
new_fragment = 'val VS_FRAGMENT_RL: Identifier = Identifier.fromNamespaceAndPath(ValkyrienSkiesMod.MOD_ID, "vs_fragment")'

anchors = {
    "class VSFabricNetworking(": 1,
    "PayloadTypeRegistry.playC2S().register": 2,
    "PayloadTypeRegistry.playS2C().register": 2,
    "ClientPlayNetworking.registerGlobalReceiver": 2,
    "ServerPlayNetworking.registerGlobalReceiver": 2,
    "VSPacketFragmenter.needsSplitting(data)": 2,
    "CustomPacketPayload.Type<VSPacket>(VS_PACKET_RL)": 1,
    "CustomPacketPayload.Type<VSFragmentPacket>(VS_FRAGMENT_RL)": 1,
    "StreamCodec.composite": 2,
}
for anchor, expected in anchors.items():
    actual = text.count(anchor)
    if actual != expected:
        raise SystemExit(
            f"fail-closed: VSFabricNetworking semantic anchor changed: {anchor!r} count={actual} expected={expected}"
        )

for old, expected in ((old_import, 1), (old_packet, 1), (old_fragment, 1)):
    actual = text.count(old)
    if actual != expected:
        raise SystemExit(f"fail-closed: expected {expected} VSFabricNetworking identifier anchor {old!r}; found {actual}")
if new_import in text or new_packet in text or new_fragment in text:
    raise SystemExit("fail-closed: VSFabricNetworking Identifier adaptation already partially present")

new_text = text.replace(old_import, new_import, 1)
new_text = new_text.replace(old_packet, new_packet, 1)
new_text = new_text.replace(old_fragment, new_fragment, 1)

if "ResourceLocation" in new_text:
    raise SystemExit("fail-closed: stale ResourceLocation vocabulary remains in VSFabricNetworking")
if new_text.count(new_import) != 1 or new_text.count(new_packet) != 1 or new_text.count(new_fragment) != 1:
    raise SystemExit("fail-closed: VSFabricNetworking Identifier postcondition failed")
for anchor, expected in anchors.items():
    actual = new_text.count(anchor)
    if actual != expected:
        raise SystemExit(
            f"fail-closed: VSFabricNetworking semantic anchor changed after Identifier adaptation: {anchor!r} count={actual} expected={expected}"
        )

path.write_text(new_text, encoding="utf-8")
print("P1_VSFABRICNETWORKING_IDENTIFIER_26_2_OVERLAY_APPLIED packetIds=2 payloadRegistry=untouched")
