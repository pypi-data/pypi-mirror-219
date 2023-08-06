# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.core.Color import Color


@dataclasses.dataclass()
class OuterBeamIcon(BaseProperty):
    unknown_0x383e2b2d: float = dataclasses.field(default=1.100000023841858)
    unknown_0xeaac42d0: float = dataclasses.field(default=0.800000011920929)
    but_settings_color: float = dataclasses.field(default=1.0)
    but_settings_scale: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xe7d57d6a: int = dataclasses.field(default=4)

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
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'8>+-')  # 0x383e2b2d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x383e2b2d))

        data.write(b'\xea\xacB\xd0')  # 0xeaac42d0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xeaac42d0))

        data.write(b'Ig\xa6<')  # 0x4967a63c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.but_settings_color))

        data.write(b'R\xf1\xd0\xd7')  # 0x52f1d0d7
        data.write(b'\x00\x10')  # size
        self.but_settings_scale.to_stream(data)

        data.write(b'\xe7\xd5}j')  # 0xe7d57d6a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xe7d57d6a))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x383e2b2d=data['unknown_0x383e2b2d'],
            unknown_0xeaac42d0=data['unknown_0xeaac42d0'],
            but_settings_color=data['but_settings_color'],
            but_settings_scale=Color.from_json(data['but_settings_scale']),
            unknown_0xe7d57d6a=data['unknown_0xe7d57d6a'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x383e2b2d': self.unknown_0x383e2b2d,
            'unknown_0xeaac42d0': self.unknown_0xeaac42d0,
            'but_settings_color': self.but_settings_color,
            'but_settings_scale': self.but_settings_scale.to_json(),
            'unknown_0xe7d57d6a': self.unknown_0xe7d57d6a,
        }


def _decode_unknown_0x383e2b2d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xeaac42d0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_but_settings_color(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_but_settings_scale(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xe7d57d6a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x383e2b2d: ('unknown_0x383e2b2d', _decode_unknown_0x383e2b2d),
    0xeaac42d0: ('unknown_0xeaac42d0', _decode_unknown_0xeaac42d0),
    0x4967a63c: ('but_settings_color', _decode_but_settings_color),
    0x52f1d0d7: ('but_settings_scale', _decode_but_settings_scale),
    0xe7d57d6a: ('unknown_0xe7d57d6a', _decode_unknown_0xe7d57d6a),
}
