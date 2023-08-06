# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct69(BaseProperty):
    vertical_offset: float = dataclasses.field(default=3.0)
    unknown_0xc241c65a: float = dataclasses.field(default=1.0)
    look_right_distance: float = dataclasses.field(default=14.0)
    look_left_distance: float = dataclasses.field(default=11.0)
    massive_height_distance: float = dataclasses.field(default=5.5)
    large_height_distance: float = dataclasses.field(default=2.5)
    small_height_distance: float = dataclasses.field(default=0.75)
    extra_drop_distance: float = dataclasses.field(default=2.0)
    max_platform_distance: float = dataclasses.field(default=6.099999904632568)
    unknown_0x935dfcfa: bool = dataclasses.field(default=True)
    unknown_0xf2502cd2: float = dataclasses.field(default=1.100000023841858)
    unknown_0xf298dcf0: bool = dataclasses.field(default=True)
    unknown_0x84b467f0: float = dataclasses.field(default=0.10000000149011612)
    unknown_0x1b39c9ab: float = dataclasses.field(default=0.0)

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
        data.write(b'\x00\x0e')  # 14 properties

        data.write(b'\xb6\x17JN')  # 0xb6174a4e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.vertical_offset))

        data.write(b'\xc2A\xc6Z')  # 0xc241c65a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc241c65a))

        data.write(b'\xcf\xf7\x10\xd0')  # 0xcff710d0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.look_right_distance))

        data.write(b'7\xf0G\x00')  # 0x37f04700
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.look_left_distance))

        data.write(b'\xc7\xd1\x1b4')  # 0xc7d11b34
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.massive_height_distance))

        data.write(b'J\xb0\xdf\x83')  # 0x4ab0df83
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.large_height_distance))

        data.write(b'\xe0\xf4\xc8\xa2')  # 0xe0f4c8a2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.small_height_distance))

        data.write(b'\xe7\x87\x9b\x05')  # 0xe7879b05
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.extra_drop_distance))

        data.write(b'v\xdf\x85c')  # 0x76df8563
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_platform_distance))

        data.write(b'\x93]\xfc\xfa')  # 0x935dfcfa
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x935dfcfa))

        data.write(b'\xf2P,\xd2')  # 0xf2502cd2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf2502cd2))

        data.write(b'\xf2\x98\xdc\xf0')  # 0xf298dcf0
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xf298dcf0))

        data.write(b'\x84\xb4g\xf0')  # 0x84b467f0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x84b467f0))

        data.write(b'\x1b9\xc9\xab')  # 0x1b39c9ab
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x1b39c9ab))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            vertical_offset=data['vertical_offset'],
            unknown_0xc241c65a=data['unknown_0xc241c65a'],
            look_right_distance=data['look_right_distance'],
            look_left_distance=data['look_left_distance'],
            massive_height_distance=data['massive_height_distance'],
            large_height_distance=data['large_height_distance'],
            small_height_distance=data['small_height_distance'],
            extra_drop_distance=data['extra_drop_distance'],
            max_platform_distance=data['max_platform_distance'],
            unknown_0x935dfcfa=data['unknown_0x935dfcfa'],
            unknown_0xf2502cd2=data['unknown_0xf2502cd2'],
            unknown_0xf298dcf0=data['unknown_0xf298dcf0'],
            unknown_0x84b467f0=data['unknown_0x84b467f0'],
            unknown_0x1b39c9ab=data['unknown_0x1b39c9ab'],
        )

    def to_json(self) -> dict:
        return {
            'vertical_offset': self.vertical_offset,
            'unknown_0xc241c65a': self.unknown_0xc241c65a,
            'look_right_distance': self.look_right_distance,
            'look_left_distance': self.look_left_distance,
            'massive_height_distance': self.massive_height_distance,
            'large_height_distance': self.large_height_distance,
            'small_height_distance': self.small_height_distance,
            'extra_drop_distance': self.extra_drop_distance,
            'max_platform_distance': self.max_platform_distance,
            'unknown_0x935dfcfa': self.unknown_0x935dfcfa,
            'unknown_0xf2502cd2': self.unknown_0xf2502cd2,
            'unknown_0xf298dcf0': self.unknown_0xf298dcf0,
            'unknown_0x84b467f0': self.unknown_0x84b467f0,
            'unknown_0x1b39c9ab': self.unknown_0x1b39c9ab,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xb6174a4e, 0xc241c65a, 0xcff710d0, 0x37f04700, 0xc7d11b34, 0x4ab0df83, 0xe0f4c8a2, 0xe7879b05, 0x76df8563, 0x935dfcfa, 0xf2502cd2, 0xf298dcf0, 0x84b467f0, 0x1b39c9ab)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct69]:
    if property_count != 14:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHfLHfLHfLHfLHfLHfLH?LHfLH?LHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(134))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27], dec[30], dec[33], dec[36], dec[39]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct69(
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
    )


def _decode_vertical_offset(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc241c65a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_look_right_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_look_left_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_massive_height_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_large_height_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_small_height_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_extra_drop_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_platform_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x935dfcfa(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xf2502cd2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf298dcf0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x84b467f0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x1b39c9ab(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xb6174a4e: ('vertical_offset', _decode_vertical_offset),
    0xc241c65a: ('unknown_0xc241c65a', _decode_unknown_0xc241c65a),
    0xcff710d0: ('look_right_distance', _decode_look_right_distance),
    0x37f04700: ('look_left_distance', _decode_look_left_distance),
    0xc7d11b34: ('massive_height_distance', _decode_massive_height_distance),
    0x4ab0df83: ('large_height_distance', _decode_large_height_distance),
    0xe0f4c8a2: ('small_height_distance', _decode_small_height_distance),
    0xe7879b05: ('extra_drop_distance', _decode_extra_drop_distance),
    0x76df8563: ('max_platform_distance', _decode_max_platform_distance),
    0x935dfcfa: ('unknown_0x935dfcfa', _decode_unknown_0x935dfcfa),
    0xf2502cd2: ('unknown_0xf2502cd2', _decode_unknown_0xf2502cd2),
    0xf298dcf0: ('unknown_0xf298dcf0', _decode_unknown_0xf298dcf0),
    0x84b467f0: ('unknown_0x84b467f0', _decode_unknown_0x84b467f0),
    0x1b39c9ab: ('unknown_0x1b39c9ab', _decode_unknown_0x1b39c9ab),
}
