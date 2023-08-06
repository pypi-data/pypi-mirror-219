# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.core.Spline import Spline


@dataclasses.dataclass()
class UnknownStruct2(BaseProperty):
    unknown_0x4b435047: float = dataclasses.field(default=500.0)
    unknown_0x0ece183c: float = dataclasses.field(default=-0.10000000149011612)
    unknown_0xab03dcb9: float = dataclasses.field(default=0.6000000238418579)
    unknown_0xc0120b9e: float = dataclasses.field(default=0.44999998807907104)
    unknown_0xf5230e61: float = dataclasses.field(default=0.75)
    unknown_0x70caf349: float = dataclasses.field(default=45.0)
    unknown_0x955a5177: float = dataclasses.field(default=15.0)
    unknown_0x95ed96c2: float = dataclasses.field(default=0.5)
    unknown_0x138b3979: Spline = dataclasses.field(default_factory=Spline)
    unknown_0xdfa46325: Spline = dataclasses.field(default_factory=Spline)

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
        data.write(b'\x00\n')  # 10 properties

        data.write(b'KCPG')  # 0x4b435047
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4b435047))

        data.write(b'\x0e\xce\x18<')  # 0xece183c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0ece183c))

        data.write(b'\xab\x03\xdc\xb9')  # 0xab03dcb9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xab03dcb9))

        data.write(b'\xc0\x12\x0b\x9e')  # 0xc0120b9e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc0120b9e))

        data.write(b'\xf5#\x0ea')  # 0xf5230e61
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf5230e61))

        data.write(b'p\xca\xf3I')  # 0x70caf349
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x70caf349))

        data.write(b'\x95ZQw')  # 0x955a5177
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x955a5177))

        data.write(b'\x95\xed\x96\xc2')  # 0x95ed96c2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x95ed96c2))

        data.write(b'\x13\x8b9y')  # 0x138b3979
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x138b3979.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdf\xa4c%')  # 0xdfa46325
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xdfa46325.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x4b435047=data['unknown_0x4b435047'],
            unknown_0x0ece183c=data['unknown_0x0ece183c'],
            unknown_0xab03dcb9=data['unknown_0xab03dcb9'],
            unknown_0xc0120b9e=data['unknown_0xc0120b9e'],
            unknown_0xf5230e61=data['unknown_0xf5230e61'],
            unknown_0x70caf349=data['unknown_0x70caf349'],
            unknown_0x955a5177=data['unknown_0x955a5177'],
            unknown_0x95ed96c2=data['unknown_0x95ed96c2'],
            unknown_0x138b3979=Spline.from_json(data['unknown_0x138b3979']),
            unknown_0xdfa46325=Spline.from_json(data['unknown_0xdfa46325']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x4b435047': self.unknown_0x4b435047,
            'unknown_0x0ece183c': self.unknown_0x0ece183c,
            'unknown_0xab03dcb9': self.unknown_0xab03dcb9,
            'unknown_0xc0120b9e': self.unknown_0xc0120b9e,
            'unknown_0xf5230e61': self.unknown_0xf5230e61,
            'unknown_0x70caf349': self.unknown_0x70caf349,
            'unknown_0x955a5177': self.unknown_0x955a5177,
            'unknown_0x95ed96c2': self.unknown_0x95ed96c2,
            'unknown_0x138b3979': self.unknown_0x138b3979.to_json(),
            'unknown_0xdfa46325': self.unknown_0xdfa46325.to_json(),
        }


def _decode_unknown_0x4b435047(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x0ece183c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xab03dcb9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc0120b9e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf5230e61(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x70caf349(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x955a5177(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x95ed96c2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x138b3979(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_unknown_0xdfa46325(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x4b435047: ('unknown_0x4b435047', _decode_unknown_0x4b435047),
    0xece183c: ('unknown_0x0ece183c', _decode_unknown_0x0ece183c),
    0xab03dcb9: ('unknown_0xab03dcb9', _decode_unknown_0xab03dcb9),
    0xc0120b9e: ('unknown_0xc0120b9e', _decode_unknown_0xc0120b9e),
    0xf5230e61: ('unknown_0xf5230e61', _decode_unknown_0xf5230e61),
    0x70caf349: ('unknown_0x70caf349', _decode_unknown_0x70caf349),
    0x955a5177: ('unknown_0x955a5177', _decode_unknown_0x955a5177),
    0x95ed96c2: ('unknown_0x95ed96c2', _decode_unknown_0x95ed96c2),
    0x138b3979: ('unknown_0x138b3979', _decode_unknown_0x138b3979),
    0xdfa46325: ('unknown_0xdfa46325', _decode_unknown_0xdfa46325),
}
