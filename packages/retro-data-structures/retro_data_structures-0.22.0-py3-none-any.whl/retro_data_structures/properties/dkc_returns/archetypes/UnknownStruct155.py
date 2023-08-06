# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct155(BaseProperty):
    unknown_0xac6cbf9d: float = dataclasses.field(default=0.0)
    start_duration: float = dataclasses.field(default=0.25)
    unknown_0x65d00bdd: float = dataclasses.field(default=0.25)
    unknown_0xf8f69c42: float = dataclasses.field(default=0.25)
    unknown_0x3e89443d: float = dataclasses.field(default=0.25)
    unknown_0xccc8bdd4: float = dataclasses.field(default=0.25)
    unknown_0xcc04105e: float = dataclasses.field(default=0.25)
    unknown_0x945c9764: float = dataclasses.field(default=0.25)
    unknown_0x9a4be38b: float = dataclasses.field(default=0.25)
    unknown_0xb844a839: float = dataclasses.field(default=0.25)
    puzzle_display_duration: float = dataclasses.field(default=0.25)
    unknown_0xbae63352: float = dataclasses.field(default=0.25)
    puzzle_done_duration: float = dataclasses.field(default=0.25)
    unknown_0xde68f38f: float = dataclasses.field(default=0.25)
    unknown_0xdee65317: float = dataclasses.field(default=0.25)
    unknown_0xf0c51c84: float = dataclasses.field(default=0.25)

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
        data.write(b'\x00\x10')  # 16 properties

        data.write(b'\xacl\xbf\x9d')  # 0xac6cbf9d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xac6cbf9d))

        data.write(b'@\x1a8#')  # 0x401a3823
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.start_duration))

        data.write(b'e\xd0\x0b\xdd')  # 0x65d00bdd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x65d00bdd))

        data.write(b'\xf8\xf6\x9cB')  # 0xf8f69c42
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf8f69c42))

        data.write(b'>\x89D=')  # 0x3e89443d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3e89443d))

        data.write(b'\xcc\xc8\xbd\xd4')  # 0xccc8bdd4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xccc8bdd4))

        data.write(b'\xcc\x04\x10^')  # 0xcc04105e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xcc04105e))

        data.write(b'\x94\\\x97d')  # 0x945c9764
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x945c9764))

        data.write(b'\x9aK\xe3\x8b')  # 0x9a4be38b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x9a4be38b))

        data.write(b'\xb8D\xa89')  # 0xb844a839
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb844a839))

        data.write(b'\xee`*\xbc')  # 0xee602abc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.puzzle_display_duration))

        data.write(b'\xba\xe63R')  # 0xbae63352
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xbae63352))

        data.write(b'\x95\x1c\xadp')  # 0x951cad70
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.puzzle_done_duration))

        data.write(b'\xdeh\xf3\x8f')  # 0xde68f38f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xde68f38f))

        data.write(b'\xde\xe6S\x17')  # 0xdee65317
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xdee65317))

        data.write(b'\xf0\xc5\x1c\x84')  # 0xf0c51c84
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf0c51c84))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xac6cbf9d=data['unknown_0xac6cbf9d'],
            start_duration=data['start_duration'],
            unknown_0x65d00bdd=data['unknown_0x65d00bdd'],
            unknown_0xf8f69c42=data['unknown_0xf8f69c42'],
            unknown_0x3e89443d=data['unknown_0x3e89443d'],
            unknown_0xccc8bdd4=data['unknown_0xccc8bdd4'],
            unknown_0xcc04105e=data['unknown_0xcc04105e'],
            unknown_0x945c9764=data['unknown_0x945c9764'],
            unknown_0x9a4be38b=data['unknown_0x9a4be38b'],
            unknown_0xb844a839=data['unknown_0xb844a839'],
            puzzle_display_duration=data['puzzle_display_duration'],
            unknown_0xbae63352=data['unknown_0xbae63352'],
            puzzle_done_duration=data['puzzle_done_duration'],
            unknown_0xde68f38f=data['unknown_0xde68f38f'],
            unknown_0xdee65317=data['unknown_0xdee65317'],
            unknown_0xf0c51c84=data['unknown_0xf0c51c84'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xac6cbf9d': self.unknown_0xac6cbf9d,
            'start_duration': self.start_duration,
            'unknown_0x65d00bdd': self.unknown_0x65d00bdd,
            'unknown_0xf8f69c42': self.unknown_0xf8f69c42,
            'unknown_0x3e89443d': self.unknown_0x3e89443d,
            'unknown_0xccc8bdd4': self.unknown_0xccc8bdd4,
            'unknown_0xcc04105e': self.unknown_0xcc04105e,
            'unknown_0x945c9764': self.unknown_0x945c9764,
            'unknown_0x9a4be38b': self.unknown_0x9a4be38b,
            'unknown_0xb844a839': self.unknown_0xb844a839,
            'puzzle_display_duration': self.puzzle_display_duration,
            'unknown_0xbae63352': self.unknown_0xbae63352,
            'puzzle_done_duration': self.puzzle_done_duration,
            'unknown_0xde68f38f': self.unknown_0xde68f38f,
            'unknown_0xdee65317': self.unknown_0xdee65317,
            'unknown_0xf0c51c84': self.unknown_0xf0c51c84,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xac6cbf9d, 0x401a3823, 0x65d00bdd, 0xf8f69c42, 0x3e89443d, 0xccc8bdd4, 0xcc04105e, 0x945c9764, 0x9a4be38b, 0xb844a839, 0xee602abc, 0xbae63352, 0x951cad70, 0xde68f38f, 0xdee65317, 0xf0c51c84)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct155]:
    if property_count != 16:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(160))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27], dec[30], dec[33], dec[36], dec[39], dec[42], dec[45]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct155(
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
        dec[35],
        dec[38],
        dec[41],
        dec[44],
        dec[47],
    )


def _decode_unknown_0xac6cbf9d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_start_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x65d00bdd(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf8f69c42(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x3e89443d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xccc8bdd4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xcc04105e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x945c9764(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x9a4be38b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb844a839(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_puzzle_display_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xbae63352(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_puzzle_done_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xde68f38f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xdee65317(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf0c51c84(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xac6cbf9d: ('unknown_0xac6cbf9d', _decode_unknown_0xac6cbf9d),
    0x401a3823: ('start_duration', _decode_start_duration),
    0x65d00bdd: ('unknown_0x65d00bdd', _decode_unknown_0x65d00bdd),
    0xf8f69c42: ('unknown_0xf8f69c42', _decode_unknown_0xf8f69c42),
    0x3e89443d: ('unknown_0x3e89443d', _decode_unknown_0x3e89443d),
    0xccc8bdd4: ('unknown_0xccc8bdd4', _decode_unknown_0xccc8bdd4),
    0xcc04105e: ('unknown_0xcc04105e', _decode_unknown_0xcc04105e),
    0x945c9764: ('unknown_0x945c9764', _decode_unknown_0x945c9764),
    0x9a4be38b: ('unknown_0x9a4be38b', _decode_unknown_0x9a4be38b),
    0xb844a839: ('unknown_0xb844a839', _decode_unknown_0xb844a839),
    0xee602abc: ('puzzle_display_duration', _decode_puzzle_display_duration),
    0xbae63352: ('unknown_0xbae63352', _decode_unknown_0xbae63352),
    0x951cad70: ('puzzle_done_duration', _decode_puzzle_done_duration),
    0xde68f38f: ('unknown_0xde68f38f', _decode_unknown_0xde68f38f),
    0xdee65317: ('unknown_0xdee65317', _decode_unknown_0xdee65317),
    0xf0c51c84: ('unknown_0xf0c51c84', _decode_unknown_0xf0c51c84),
}
