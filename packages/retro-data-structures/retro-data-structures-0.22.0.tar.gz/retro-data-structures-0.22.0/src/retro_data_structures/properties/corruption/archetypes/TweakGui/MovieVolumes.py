# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class MovieVolumes(BaseProperty):
    unknown_0xae149646: int = dataclasses.field(default=127)
    unknown_0xc1a2e858: int = dataclasses.field(default=127)
    unknown_0x138c3bb8: int = dataclasses.field(default=127)
    unknown_0xe5587648: int = dataclasses.field(default=127)
    unknown_0x9ed00248: int = dataclasses.field(default=127)
    unknown_0x6f135424: int = dataclasses.field(default=127)
    unknown_0xdb2260b7: int = dataclasses.field(default=127)
    unknown_0xf38093f5: int = dataclasses.field(default=127)

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
        data.write(b'\x00\x08')  # 8 properties

        data.write(b'\xae\x14\x96F')  # 0xae149646
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xae149646))

        data.write(b'\xc1\xa2\xe8X')  # 0xc1a2e858
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xc1a2e858))

        data.write(b'\x13\x8c;\xb8')  # 0x138c3bb8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x138c3bb8))

        data.write(b'\xe5XvH')  # 0xe5587648
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xe5587648))

        data.write(b'\x9e\xd0\x02H')  # 0x9ed00248
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x9ed00248))

        data.write(b'o\x13T$')  # 0x6f135424
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x6f135424))

        data.write(b'\xdb"`\xb7')  # 0xdb2260b7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xdb2260b7))

        data.write(b'\xf3\x80\x93\xf5')  # 0xf38093f5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xf38093f5))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xae149646=data['unknown_0xae149646'],
            unknown_0xc1a2e858=data['unknown_0xc1a2e858'],
            unknown_0x138c3bb8=data['unknown_0x138c3bb8'],
            unknown_0xe5587648=data['unknown_0xe5587648'],
            unknown_0x9ed00248=data['unknown_0x9ed00248'],
            unknown_0x6f135424=data['unknown_0x6f135424'],
            unknown_0xdb2260b7=data['unknown_0xdb2260b7'],
            unknown_0xf38093f5=data['unknown_0xf38093f5'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xae149646': self.unknown_0xae149646,
            'unknown_0xc1a2e858': self.unknown_0xc1a2e858,
            'unknown_0x138c3bb8': self.unknown_0x138c3bb8,
            'unknown_0xe5587648': self.unknown_0xe5587648,
            'unknown_0x9ed00248': self.unknown_0x9ed00248,
            'unknown_0x6f135424': self.unknown_0x6f135424,
            'unknown_0xdb2260b7': self.unknown_0xdb2260b7,
            'unknown_0xf38093f5': self.unknown_0xf38093f5,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xae149646, 0xc1a2e858, 0x138c3bb8, 0xe5587648, 0x9ed00248, 0x6f135424, 0xdb2260b7, 0xf38093f5)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[MovieVolumes]:
    if property_count != 8:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHlLHlLHlLHlLHlLHlLHlLHl')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(80))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21]) != _FAST_IDS:
        data.seek(before)
        return None

    return MovieVolumes(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
        dec[20],
        dec[23],
    )


def _decode_unknown_0xae149646(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xc1a2e858(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x138c3bb8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xe5587648(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x9ed00248(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x6f135424(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xdb2260b7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xf38093f5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xae149646: ('unknown_0xae149646', _decode_unknown_0xae149646),
    0xc1a2e858: ('unknown_0xc1a2e858', _decode_unknown_0xc1a2e858),
    0x138c3bb8: ('unknown_0x138c3bb8', _decode_unknown_0x138c3bb8),
    0xe5587648: ('unknown_0xe5587648', _decode_unknown_0xe5587648),
    0x9ed00248: ('unknown_0x9ed00248', _decode_unknown_0x9ed00248),
    0x6f135424: ('unknown_0x6f135424', _decode_unknown_0x6f135424),
    0xdb2260b7: ('unknown_0xdb2260b7', _decode_unknown_0xdb2260b7),
    0xf38093f5: ('unknown_0xf38093f5', _decode_unknown_0xf38093f5),
}
