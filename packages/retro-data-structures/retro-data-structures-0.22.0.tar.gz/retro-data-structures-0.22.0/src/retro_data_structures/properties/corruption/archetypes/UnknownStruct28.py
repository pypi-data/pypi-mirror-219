# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct28(BaseProperty):
    common_vertical_scale: float = dataclasses.field(default=5.0)
    unknown_0x8ed32be8: float = dataclasses.field(default=5.0)
    unknown_0xcfc4146e: float = dataclasses.field(default=10.0)
    unknown_0x0479c95b: float = dataclasses.field(default=5.0)
    unknown_0xdfc69abc: float = dataclasses.field(default=15.0)
    unknown_0x9c27ea0d: float = dataclasses.field(default=30.0)
    unknown_0xe8c00bb1: float = dataclasses.field(default=30.0)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
        if default_override is None and (result := _fast_decode(data, property_count)) is not None:
            return result

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
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'\x05\n\xf3\x1e')  # 0x50af31e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.common_vertical_scale))

        data.write(b'\x8e\xd3+\xe8')  # 0x8ed32be8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8ed32be8))

        data.write(b'\xcf\xc4\x14n')  # 0xcfc4146e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xcfc4146e))

        data.write(b'\x04y\xc9[')  # 0x479c95b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0479c95b))

        data.write(b'\xdf\xc6\x9a\xbc')  # 0xdfc69abc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xdfc69abc))

        data.write(b"\x9c'\xea\r")  # 0x9c27ea0d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x9c27ea0d))

        data.write(b'\xe8\xc0\x0b\xb1')  # 0xe8c00bb1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe8c00bb1))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            common_vertical_scale=data['common_vertical_scale'],
            unknown_0x8ed32be8=data['unknown_0x8ed32be8'],
            unknown_0xcfc4146e=data['unknown_0xcfc4146e'],
            unknown_0x0479c95b=data['unknown_0x0479c95b'],
            unknown_0xdfc69abc=data['unknown_0xdfc69abc'],
            unknown_0x9c27ea0d=data['unknown_0x9c27ea0d'],
            unknown_0xe8c00bb1=data['unknown_0xe8c00bb1'],
        )

    def to_json(self) -> dict:
        return {
            'common_vertical_scale': self.common_vertical_scale,
            'unknown_0x8ed32be8': self.unknown_0x8ed32be8,
            'unknown_0xcfc4146e': self.unknown_0xcfc4146e,
            'unknown_0x0479c95b': self.unknown_0x0479c95b,
            'unknown_0xdfc69abc': self.unknown_0xdfc69abc,
            'unknown_0x9c27ea0d': self.unknown_0x9c27ea0d,
            'unknown_0xe8c00bb1': self.unknown_0xe8c00bb1,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x50af31e, 0x8ed32be8, 0xcfc4146e, 0x479c95b, 0xdfc69abc, 0x9c27ea0d, 0xe8c00bb1)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct28]:
    if property_count != 7:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(70))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct28(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
        dec[20],
    )


def _decode_common_vertical_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8ed32be8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xcfc4146e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x0479c95b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xdfc69abc(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x9c27ea0d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe8c00bb1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x50af31e: ('common_vertical_scale', _decode_common_vertical_scale),
    0x8ed32be8: ('unknown_0x8ed32be8', _decode_unknown_0x8ed32be8),
    0xcfc4146e: ('unknown_0xcfc4146e', _decode_unknown_0xcfc4146e),
    0x479c95b: ('unknown_0x0479c95b', _decode_unknown_0x0479c95b),
    0xdfc69abc: ('unknown_0xdfc69abc', _decode_unknown_0xdfc69abc),
    0x9c27ea0d: ('unknown_0x9c27ea0d', _decode_unknown_0x9c27ea0d),
    0xe8c00bb1: ('unknown_0xe8c00bb1', _decode_unknown_0xe8c00bb1),
}
