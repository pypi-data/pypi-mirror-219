# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.core.Color import Color


@dataclasses.dataclass()
class Gauge(BaseProperty):
    unknown_0xd032c2a1: float = dataclasses.field(default=0.0)
    unknown_0xa118e250: float = dataclasses.field(default=90.0)
    unknown_0xdb1ac8ee: float = dataclasses.field(default=150.0)
    unknown_0xecd100f8: float = dataclasses.field(default=210.0)
    charge_gauge_scale: float = dataclasses.field(default=1.0)
    charge_gauge_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xed78e6eb: int = dataclasses.field(default=14)
    unknown_0x2c3d9e27: float = dataclasses.field(default=8.5)

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
        data.write(b'\x00\x08')  # 8 properties

        data.write(b'\xd02\xc2\xa1')  # 0xd032c2a1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd032c2a1))

        data.write(b'\xa1\x18\xe2P')  # 0xa118e250
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa118e250))

        data.write(b'\xdb\x1a\xc8\xee')  # 0xdb1ac8ee
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xdb1ac8ee))

        data.write(b'\xec\xd1\x00\xf8')  # 0xecd100f8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xecd100f8))

        data.write(b'I\xf8\x16\x1f')  # 0x49f8161f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.charge_gauge_scale))

        data.write(b'Rn`\xf4')  # 0x526e60f4
        data.write(b'\x00\x10')  # size
        self.charge_gauge_color.to_stream(data)

        data.write(b'\xedx\xe6\xeb')  # 0xed78e6eb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xed78e6eb))

        data.write(b",=\x9e'")  # 0x2c3d9e27
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2c3d9e27))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xd032c2a1=data['unknown_0xd032c2a1'],
            unknown_0xa118e250=data['unknown_0xa118e250'],
            unknown_0xdb1ac8ee=data['unknown_0xdb1ac8ee'],
            unknown_0xecd100f8=data['unknown_0xecd100f8'],
            charge_gauge_scale=data['charge_gauge_scale'],
            charge_gauge_color=Color.from_json(data['charge_gauge_color']),
            unknown_0xed78e6eb=data['unknown_0xed78e6eb'],
            unknown_0x2c3d9e27=data['unknown_0x2c3d9e27'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xd032c2a1': self.unknown_0xd032c2a1,
            'unknown_0xa118e250': self.unknown_0xa118e250,
            'unknown_0xdb1ac8ee': self.unknown_0xdb1ac8ee,
            'unknown_0xecd100f8': self.unknown_0xecd100f8,
            'charge_gauge_scale': self.charge_gauge_scale,
            'charge_gauge_color': self.charge_gauge_color.to_json(),
            'unknown_0xed78e6eb': self.unknown_0xed78e6eb,
            'unknown_0x2c3d9e27': self.unknown_0x2c3d9e27,
        }


def _decode_unknown_0xd032c2a1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa118e250(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xdb1ac8ee(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xecd100f8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_charge_gauge_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_charge_gauge_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xed78e6eb(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x2c3d9e27(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xd032c2a1: ('unknown_0xd032c2a1', _decode_unknown_0xd032c2a1),
    0xa118e250: ('unknown_0xa118e250', _decode_unknown_0xa118e250),
    0xdb1ac8ee: ('unknown_0xdb1ac8ee', _decode_unknown_0xdb1ac8ee),
    0xecd100f8: ('unknown_0xecd100f8', _decode_unknown_0xecd100f8),
    0x49f8161f: ('charge_gauge_scale', _decode_charge_gauge_scale),
    0x526e60f4: ('charge_gauge_color', _decode_charge_gauge_color),
    0xed78e6eb: ('unknown_0xed78e6eb', _decode_unknown_0xed78e6eb),
    0x2c3d9e27: ('unknown_0x2c3d9e27', _decode_unknown_0x2c3d9e27),
}
