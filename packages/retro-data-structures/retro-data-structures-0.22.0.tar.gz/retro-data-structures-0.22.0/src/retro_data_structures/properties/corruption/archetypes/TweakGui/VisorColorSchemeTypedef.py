# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.core.Color import Color


@dataclasses.dataclass()
class VisorColorSchemeTypedef(BaseProperty):
    hud_hue: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

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

        data.write(b'Y\x14\x81s')  # 0x59148173
        data.write(b'\x00\x10')  # size
        self.hud_hue.to_stream(data)

        data.write(b'\x9d\xa5\xd1\xd7')  # 0x9da5d1d7
        data.write(b'\x00\x10')  # size
        self.unknown.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            hud_hue=Color.from_json(data['hud_hue']),
            unknown=Color.from_json(data['unknown']),
        )

    def to_json(self) -> dict:
        return {
            'hud_hue': self.hud_hue.to_json(),
            'unknown': self.unknown.to_json(),
        }


def _decode_hud_hue(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x59148173: ('hud_hue', _decode_hud_hue),
    0x9da5d1d7: ('unknown', _decode_unknown),
}
