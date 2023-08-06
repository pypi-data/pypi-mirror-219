# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct115(BaseProperty):
    target_idle_range: float = dataclasses.field(default=5.0)
    unknown_0x0a42c7af: float = dataclasses.field(default=1.0)
    max_patrol_distance: float = dataclasses.field(default=5.0)
    chase_speed: float = dataclasses.field(default=5.0)
    patrol_speed: float = dataclasses.field(default=5.0)
    unknown_0x6cce17a9: float = dataclasses.field(default=1.0)
    unknown_0xaad0b493: float = dataclasses.field(default=10.0)
    unknown_0xe1cf6014: float = dataclasses.field(default=40.0)
    unknown_0x29a27cb9: float = dataclasses.field(default=8.0)
    unknown_0x3311ba2b: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)

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
        data.write(b'\x00\n')  # 10 properties

        data.write(b'\x80-27')  # 0x802d3237
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.target_idle_range))

        data.write(b'\nB\xc7\xaf')  # 0xa42c7af
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0a42c7af))

        data.write(b'[\xbbn\xc9')  # 0x5bbb6ec9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_patrol_distance))

        data.write(b'\x92\xfb\xc1a')  # 0x92fbc161
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.chase_speed))

        data.write(b'v\\7\x15')  # 0x765c3715
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.patrol_speed))

        data.write(b'l\xce\x17\xa9')  # 0x6cce17a9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x6cce17a9))

        data.write(b'\xaa\xd0\xb4\x93')  # 0xaad0b493
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xaad0b493))

        data.write(b'\xe1\xcf`\x14')  # 0xe1cf6014
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe1cf6014))

        data.write(b')\xa2|\xb9')  # 0x29a27cb9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x29a27cb9))

        data.write(b'3\x11\xba+')  # 0x3311ba2b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x3311ba2b))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            target_idle_range=data['target_idle_range'],
            unknown_0x0a42c7af=data['unknown_0x0a42c7af'],
            max_patrol_distance=data['max_patrol_distance'],
            chase_speed=data['chase_speed'],
            patrol_speed=data['patrol_speed'],
            unknown_0x6cce17a9=data['unknown_0x6cce17a9'],
            unknown_0xaad0b493=data['unknown_0xaad0b493'],
            unknown_0xe1cf6014=data['unknown_0xe1cf6014'],
            unknown_0x29a27cb9=data['unknown_0x29a27cb9'],
            unknown_0x3311ba2b=data['unknown_0x3311ba2b'],
        )

    def to_json(self) -> dict:
        return {
            'target_idle_range': self.target_idle_range,
            'unknown_0x0a42c7af': self.unknown_0x0a42c7af,
            'max_patrol_distance': self.max_patrol_distance,
            'chase_speed': self.chase_speed,
            'patrol_speed': self.patrol_speed,
            'unknown_0x6cce17a9': self.unknown_0x6cce17a9,
            'unknown_0xaad0b493': self.unknown_0xaad0b493,
            'unknown_0xe1cf6014': self.unknown_0xe1cf6014,
            'unknown_0x29a27cb9': self.unknown_0x29a27cb9,
            'unknown_0x3311ba2b': self.unknown_0x3311ba2b,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x802d3237, 0xa42c7af, 0x5bbb6ec9, 0x92fbc161, 0x765c3715, 0x6cce17a9, 0xaad0b493, 0xe1cf6014, 0x29a27cb9, 0x3311ba2b)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct115]:
    if property_count != 10:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHfLHfLHfLHfLHfLHfLHQ')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(104))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct115(
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


def _decode_target_idle_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x0a42c7af(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_patrol_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_chase_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_patrol_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x6cce17a9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xaad0b493(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe1cf6014(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x29a27cb9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x3311ba2b(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x802d3237: ('target_idle_range', _decode_target_idle_range),
    0xa42c7af: ('unknown_0x0a42c7af', _decode_unknown_0x0a42c7af),
    0x5bbb6ec9: ('max_patrol_distance', _decode_max_patrol_distance),
    0x92fbc161: ('chase_speed', _decode_chase_speed),
    0x765c3715: ('patrol_speed', _decode_patrol_speed),
    0x6cce17a9: ('unknown_0x6cce17a9', _decode_unknown_0x6cce17a9),
    0xaad0b493: ('unknown_0xaad0b493', _decode_unknown_0xaad0b493),
    0xe1cf6014: ('unknown_0xe1cf6014', _decode_unknown_0xe1cf6014),
    0x29a27cb9: ('unknown_0x29a27cb9', _decode_unknown_0x29a27cb9),
    0x3311ba2b: ('unknown_0x3311ba2b', _decode_unknown_0x3311ba2b),
}
