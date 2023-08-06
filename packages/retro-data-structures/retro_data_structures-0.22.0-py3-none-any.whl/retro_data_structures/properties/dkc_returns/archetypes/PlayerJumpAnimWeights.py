# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class PlayerJumpAnimWeights(BaseProperty):
    animation_count: int = dataclasses.field(default=0)
    random_weight1: float = dataclasses.field(default=0.0)
    random_weight2: float = dataclasses.field(default=0.0)
    random_weight3: float = dataclasses.field(default=0.0)
    random_weight4: float = dataclasses.field(default=0.0)
    random_weight5: float = dataclasses.field(default=0.0)
    random_weight6: float = dataclasses.field(default=0.0)
    random_weight7: float = dataclasses.field(default=0.0)
    random_weight8: float = dataclasses.field(default=0.0)
    random_weight9: float = dataclasses.field(default=0.0)
    random_weight10: float = dataclasses.field(default=0.0)

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
        data.write(b'\x00\x0b')  # 11 properties

        data.write(b'9\xe9\xfa5')  # 0x39e9fa35
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.animation_count))

        data.write(b'\x18RI\xcf')  # 0x185249cf
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.random_weight1))

        data.write(b'\x9e\xc6;a')  # 0x9ec63b61
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.random_weight2))

        data.write(b'U\x9a\xe8\xc4')  # 0x559ae8c4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.random_weight3))

        data.write(b'H\x9f\xd8|')  # 0x489fd87c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.random_weight4))

        data.write(b'\x83\xc3\x0b\xd9')  # 0x83c30bd9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.random_weight5))

        data.write(b'\x05Wyw')  # 0x5577977
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.random_weight6))

        data.write(b'\xce\x0b\xaa\xd2')  # 0xce0baad2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.random_weight7))

        data.write(b'?]\x18\x07')  # 0x3f5d1807
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.random_weight8))

        data.write(b'\xf4\x01\xcb\xa2')  # 0xf401cba2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.random_weight9))

        data.write(b'\xe3R\xaf\xf6')  # 0xe352aff6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.random_weight10))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            animation_count=data['animation_count'],
            random_weight1=data['random_weight1'],
            random_weight2=data['random_weight2'],
            random_weight3=data['random_weight3'],
            random_weight4=data['random_weight4'],
            random_weight5=data['random_weight5'],
            random_weight6=data['random_weight6'],
            random_weight7=data['random_weight7'],
            random_weight8=data['random_weight8'],
            random_weight9=data['random_weight9'],
            random_weight10=data['random_weight10'],
        )

    def to_json(self) -> dict:
        return {
            'animation_count': self.animation_count,
            'random_weight1': self.random_weight1,
            'random_weight2': self.random_weight2,
            'random_weight3': self.random_weight3,
            'random_weight4': self.random_weight4,
            'random_weight5': self.random_weight5,
            'random_weight6': self.random_weight6,
            'random_weight7': self.random_weight7,
            'random_weight8': self.random_weight8,
            'random_weight9': self.random_weight9,
            'random_weight10': self.random_weight10,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x39e9fa35, 0x185249cf, 0x9ec63b61, 0x559ae8c4, 0x489fd87c, 0x83c30bd9, 0x5577977, 0xce0baad2, 0x3f5d1807, 0xf401cba2, 0xe352aff6)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[PlayerJumpAnimWeights]:
    if property_count != 11:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHlLHfLHfLHfLHfLHfLHfLHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(110))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27], dec[30]) != _FAST_IDS:
        data.seek(before)
        return None

    return PlayerJumpAnimWeights(
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
        dec[32],
    )


def _decode_animation_count(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_random_weight1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_random_weight2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_random_weight3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_random_weight4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_random_weight5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_random_weight6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_random_weight7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_random_weight8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_random_weight9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_random_weight10(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x39e9fa35: ('animation_count', _decode_animation_count),
    0x185249cf: ('random_weight1', _decode_random_weight1),
    0x9ec63b61: ('random_weight2', _decode_random_weight2),
    0x559ae8c4: ('random_weight3', _decode_random_weight3),
    0x489fd87c: ('random_weight4', _decode_random_weight4),
    0x83c30bd9: ('random_weight5', _decode_random_weight5),
    0x5577977: ('random_weight6', _decode_random_weight6),
    0xce0baad2: ('random_weight7', _decode_random_weight7),
    0x3f5d1807: ('random_weight8', _decode_random_weight8),
    0xf401cba2: ('random_weight9', _decode_random_weight9),
    0xe352aff6: ('random_weight10', _decode_random_weight10),
}
