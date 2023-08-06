# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class GrappleBlock(BaseProperty):
    block_type: int = dataclasses.field(default=0)
    unknown_0x54178cb8: float = dataclasses.field(default=0.0)
    unknown_0xde38f04e: float = dataclasses.field(default=0.0)
    unknown_0x9d0c992f: float = dataclasses.field(default=1.0)
    unknown_0x8382cd42: float = dataclasses.field(default=5.0)
    unknown_0x8a40fd1b: bool = dataclasses.field(default=True)
    unknown_0xa62bf627: bool = dataclasses.field(default=True)
    unknown_0xf8a14c37: int = dataclasses.field(default=3364175296)  # Choice
    unknown_0x64fb595c: bool = dataclasses.field(default=True)
    unknown_0x0887fefe: bool = dataclasses.field(default=False)

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
        data.write(b'\x00\n')  # 10 properties

        data.write(b'\x00\x8b\xd2@')  # 0x8bd240
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.block_type))

        data.write(b'T\x17\x8c\xb8')  # 0x54178cb8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x54178cb8))

        data.write(b'\xde8\xf0N')  # 0xde38f04e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xde38f04e))

        data.write(b'\x9d\x0c\x99/')  # 0x9d0c992f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x9d0c992f))

        data.write(b'\x83\x82\xcdB')  # 0x8382cd42
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8382cd42))

        data.write(b'\x8a@\xfd\x1b')  # 0x8a40fd1b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x8a40fd1b))

        data.write(b"\xa6+\xf6'")  # 0xa62bf627
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xa62bf627))

        data.write(b'\xf8\xa1L7')  # 0xf8a14c37
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.unknown_0xf8a14c37))

        data.write(b'd\xfbY\\')  # 0x64fb595c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x64fb595c))

        data.write(b'\x08\x87\xfe\xfe')  # 0x887fefe
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x0887fefe))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            block_type=data['block_type'],
            unknown_0x54178cb8=data['unknown_0x54178cb8'],
            unknown_0xde38f04e=data['unknown_0xde38f04e'],
            unknown_0x9d0c992f=data['unknown_0x9d0c992f'],
            unknown_0x8382cd42=data['unknown_0x8382cd42'],
            unknown_0x8a40fd1b=data['unknown_0x8a40fd1b'],
            unknown_0xa62bf627=data['unknown_0xa62bf627'],
            unknown_0xf8a14c37=data['unknown_0xf8a14c37'],
            unknown_0x64fb595c=data['unknown_0x64fb595c'],
            unknown_0x0887fefe=data['unknown_0x0887fefe'],
        )

    def to_json(self) -> dict:
        return {
            'block_type': self.block_type,
            'unknown_0x54178cb8': self.unknown_0x54178cb8,
            'unknown_0xde38f04e': self.unknown_0xde38f04e,
            'unknown_0x9d0c992f': self.unknown_0x9d0c992f,
            'unknown_0x8382cd42': self.unknown_0x8382cd42,
            'unknown_0x8a40fd1b': self.unknown_0x8a40fd1b,
            'unknown_0xa62bf627': self.unknown_0xa62bf627,
            'unknown_0xf8a14c37': self.unknown_0xf8a14c37,
            'unknown_0x64fb595c': self.unknown_0x64fb595c,
            'unknown_0x0887fefe': self.unknown_0x0887fefe,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x8bd240, 0x54178cb8, 0xde38f04e, 0x9d0c992f, 0x8382cd42, 0x8a40fd1b, 0xa62bf627, 0xf8a14c37, 0x64fb595c, 0x887fefe)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[GrappleBlock]:
    if property_count != 10:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHlLHfLHfLHfLHfLH?LH?LHLLH?LH?')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(88))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27]) != _FAST_IDS:
        data.seek(before)
        return None

    return GrappleBlock(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
        dec[20],
        dec[23],
        dec[26],
        dec[29],
    )


def _decode_block_type(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x54178cb8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xde38f04e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x9d0c992f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8382cd42(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8a40fd1b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xa62bf627(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xf8a14c37(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_0x64fb595c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x0887fefe(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x8bd240: ('block_type', _decode_block_type),
    0x54178cb8: ('unknown_0x54178cb8', _decode_unknown_0x54178cb8),
    0xde38f04e: ('unknown_0xde38f04e', _decode_unknown_0xde38f04e),
    0x9d0c992f: ('unknown_0x9d0c992f', _decode_unknown_0x9d0c992f),
    0x8382cd42: ('unknown_0x8382cd42', _decode_unknown_0x8382cd42),
    0x8a40fd1b: ('unknown_0x8a40fd1b', _decode_unknown_0x8a40fd1b),
    0xa62bf627: ('unknown_0xa62bf627', _decode_unknown_0xa62bf627),
    0xf8a14c37: ('unknown_0xf8a14c37', _decode_unknown_0xf8a14c37),
    0x64fb595c: ('unknown_0x64fb595c', _decode_unknown_0x64fb595c),
    0x887fefe: ('unknown_0x0887fefe', _decode_unknown_0x0887fefe),
}
