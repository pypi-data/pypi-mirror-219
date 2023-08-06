# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct188(BaseProperty):
    unknown_0xe84a887b: float = dataclasses.field(default=1.0)
    unknown_0x8a58a7f8: int = dataclasses.field(default=2)
    unknown_0x1d18ec45: bool = dataclasses.field(default=False)
    stun_duration: float = dataclasses.field(default=2.0)
    unknown_0x634415f0: float = dataclasses.field(default=1.0)
    unknown_0x82090854: float = dataclasses.field(default=0.5)
    unknown_0x0c7f57a5: float = dataclasses.field(default=0.5)
    unknown_0x1a75dce7: float = dataclasses.field(default=0.5)
    unknown_0x89c8bb60: float = dataclasses.field(default=4.0)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

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
        data.write(b'\x00\t')  # 9 properties

        data.write(b'\xe8J\x88{')  # 0xe84a887b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe84a887b))

        data.write(b'\x8aX\xa7\xf8')  # 0x8a58a7f8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x8a58a7f8))

        data.write(b'\x1d\x18\xecE')  # 0x1d18ec45
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x1d18ec45))

        data.write(b'-\x8d\xb3\x1d')  # 0x2d8db31d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.stun_duration))

        data.write(b'cD\x15\xf0')  # 0x634415f0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x634415f0))

        data.write(b'\x82\t\x08T')  # 0x82090854
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x82090854))

        data.write(b'\x0c\x7fW\xa5')  # 0xc7f57a5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0c7f57a5))

        data.write(b'\x1au\xdc\xe7')  # 0x1a75dce7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x1a75dce7))

        data.write(b'\x89\xc8\xbb`')  # 0x89c8bb60
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x89c8bb60))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xe84a887b=data['unknown_0xe84a887b'],
            unknown_0x8a58a7f8=data['unknown_0x8a58a7f8'],
            unknown_0x1d18ec45=data['unknown_0x1d18ec45'],
            stun_duration=data['stun_duration'],
            unknown_0x634415f0=data['unknown_0x634415f0'],
            unknown_0x82090854=data['unknown_0x82090854'],
            unknown_0x0c7f57a5=data['unknown_0x0c7f57a5'],
            unknown_0x1a75dce7=data['unknown_0x1a75dce7'],
            unknown_0x89c8bb60=data['unknown_0x89c8bb60'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xe84a887b': self.unknown_0xe84a887b,
            'unknown_0x8a58a7f8': self.unknown_0x8a58a7f8,
            'unknown_0x1d18ec45': self.unknown_0x1d18ec45,
            'stun_duration': self.stun_duration,
            'unknown_0x634415f0': self.unknown_0x634415f0,
            'unknown_0x82090854': self.unknown_0x82090854,
            'unknown_0x0c7f57a5': self.unknown_0x0c7f57a5,
            'unknown_0x1a75dce7': self.unknown_0x1a75dce7,
            'unknown_0x89c8bb60': self.unknown_0x89c8bb60,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xe84a887b, 0x8a58a7f8, 0x1d18ec45, 0x2d8db31d, 0x634415f0, 0x82090854, 0xc7f57a5, 0x1a75dce7, 0x89c8bb60)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct188]:
    if property_count != 9:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHlLH?LHfLHfLHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(87))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct188(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
        dec[20],
        dec[23],
        dec[26],
    )


def _decode_unknown_0xe84a887b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8a58a7f8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x1d18ec45(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_stun_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x634415f0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x82090854(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x0c7f57a5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x1a75dce7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x89c8bb60(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xe84a887b: ('unknown_0xe84a887b', _decode_unknown_0xe84a887b),
    0x8a58a7f8: ('unknown_0x8a58a7f8', _decode_unknown_0x8a58a7f8),
    0x1d18ec45: ('unknown_0x1d18ec45', _decode_unknown_0x1d18ec45),
    0x2d8db31d: ('stun_duration', _decode_stun_duration),
    0x634415f0: ('unknown_0x634415f0', _decode_unknown_0x634415f0),
    0x82090854: ('unknown_0x82090854', _decode_unknown_0x82090854),
    0xc7f57a5: ('unknown_0x0c7f57a5', _decode_unknown_0x0c7f57a5),
    0x1a75dce7: ('unknown_0x1a75dce7', _decode_unknown_0x1a75dce7),
    0x89c8bb60: ('unknown_0x89c8bb60', _decode_unknown_0x89c8bb60),
}
