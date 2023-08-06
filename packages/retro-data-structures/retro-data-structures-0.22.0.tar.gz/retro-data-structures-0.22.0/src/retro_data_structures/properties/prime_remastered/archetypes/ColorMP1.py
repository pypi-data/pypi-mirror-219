# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class ColorMP1(BaseProperty):
    r: float = dataclasses.field(default=0.0)
    g: float = dataclasses.field(default=0.0)
    b: float = dataclasses.field(default=0.0)
    a: float = dataclasses.field(default=0.0)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME_REMASTER

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack("<H", data.read(2))[0]
        if default_override is None and (result := _fast_decode(data, property_count)) is not None:
            return result

        present_fields = default_override or {}
        for _ in range(property_count):
            property_id, property_size = struct.unpack("<LH", data.read(6))
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
        data.write(b'\x04\x00')  # 4 properties

        data.write(b'\xd1\x89\x08\x11')  # 0x110889d1
        data.write(b'\x04\x00')  # size
        data.write(struct.pack('<f', self.r))

        data.write(b'"\xffz\x8a')  # 0x8a7aff22
        data.write(b'\x04\x00')  # size
        data.write(struct.pack('<f', self.g))

        data.write(b'\xe9IS*')  # 0x2a5349e9
        data.write(b'\x04\x00')  # size
        data.write(struct.pack('<f', self.b))

        data.write(b':\xc9d\xe3')  # 0xe364c93a
        data.write(b'\x04\x00')  # size
        data.write(struct.pack('<f', self.a))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            r=data['r'],
            g=data['g'],
            b=data['b'],
            a=data['a'],
        )

    def to_json(self) -> dict:
        return {
            'r': self.r,
            'g': self.g,
            'b': self.b,
            'a': self.a,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x110889d1, 0x8a7aff22, 0x2a5349e9, 0xe364c93a)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[ColorMP1]:
    if property_count != 4:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('<LHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(40))
    if (dec[0], dec[3], dec[6], dec[9]) != _FAST_IDS:
        data.seek(before)
        return None

    return ColorMP1(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
    )


def _decode_r(data: typing.BinaryIO, property_size: int):
    return struct.unpack('<f', data.read(4))[0]


def _decode_g(data: typing.BinaryIO, property_size: int):
    return struct.unpack('<f', data.read(4))[0]


def _decode_b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('<f', data.read(4))[0]


def _decode_a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('<f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x110889d1: ('r', _decode_r),
    0x8a7aff22: ('g', _decode_g),
    0x2a5349e9: ('b', _decode_b),
    0xe364c93a: ('a', _decode_a),
}
