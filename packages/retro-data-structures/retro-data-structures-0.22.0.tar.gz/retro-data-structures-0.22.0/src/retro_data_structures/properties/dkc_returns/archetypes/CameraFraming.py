# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.FramingRules import FramingRules
from retro_data_structures.properties.dkc_returns.archetypes.ZoomBehaviorData import ZoomBehaviorData


@dataclasses.dataclass()
class CameraFraming(BaseProperty):
    framing_rules: FramingRules = dataclasses.field(default_factory=FramingRules)
    zoom_behavior: ZoomBehaviorData = dataclasses.field(default_factory=ZoomBehaviorData)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
        present_fields = default_override or {}
        for _ in range(property_count):
            property_id, property_size = struct.unpack(">LH", data.read(6))
            start = data.tell()
            try:
                property_name, decoder = _property_decoder[property_id]
                present_fields[property_name] = decoder(data, property_size)
            except KeyError:
                raise RuntimeError(f"Unknown property: 0x{property_id:08x}")
            assert data.tell() - start == property_size

        return cls(**present_fields)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'\xc7\x9a\xa0\xc6')  # 0xc79aa0c6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.framing_rules.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'b$0\x11')  # 0x62243011
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.zoom_behavior.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            framing_rules=FramingRules.from_json(data['framing_rules']),
            zoom_behavior=ZoomBehaviorData.from_json(data['zoom_behavior']),
        )

    def to_json(self) -> dict:
        return {
            'framing_rules': self.framing_rules.to_json(),
            'zoom_behavior': self.zoom_behavior.to_json(),
        }


def _decode_framing_rules(data: typing.BinaryIO, property_size: int):
    return FramingRules.from_stream(data, property_size)


def _decode_zoom_behavior(data: typing.BinaryIO, property_size: int):
    return ZoomBehaviorData.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc79aa0c6: ('framing_rules', _decode_framing_rules),
    0x62243011: ('zoom_behavior', _decode_zoom_behavior),
}
