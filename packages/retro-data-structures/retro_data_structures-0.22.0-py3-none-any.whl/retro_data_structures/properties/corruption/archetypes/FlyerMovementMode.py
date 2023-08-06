# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class FlyerMovementMode(BaseProperty):
    speed: float = dataclasses.field(default=10.0)
    acceleration: float = dataclasses.field(default=5.0)
    turn_rate: float = dataclasses.field(default=1080.0)
    facing_turn_rate: float = dataclasses.field(default=90.0)
    turn_threshold: float = dataclasses.field(default=30.0)
    use_avoidance: bool = dataclasses.field(default=True)
    avoidance_range: float = dataclasses.field(default=3.0)
    unknown: float = dataclasses.field(default=2.0)
    height_variation_max: float = dataclasses.field(default=2.0)
    height_variation_min: float = dataclasses.field(default=0.0)
    floor_buffer: float = dataclasses.field(default=1.0)
    ceiling_buffer: float = dataclasses.field(default=1.0)

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
        data.write(b'\x00\x0c')  # 12 properties

        data.write(b'c\x92@N')  # 0x6392404e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.speed))

        data.write(b'9\xfbyx')  # 0x39fb7978
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.acceleration))

        data.write(b'\xe3M\xc7\x03')  # 0xe34dc703
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.turn_rate))

        data.write(b'ld&\xc8')  # 0x6c6426c8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.facing_turn_rate))

        data.write(b"\xc0\xac'\x1e")  # 0xc0ac271e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.turn_threshold))

        data.write(b'\x96\x99\xfaE')  # 0x9699fa45
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_avoidance))

        data.write(b'P\xa9\xbd\r')  # 0x50a9bd0d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.avoidance_range))

        data.write(b'\x1a{w\xab')  # 0x1a7b77ab
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown))

        data.write(b'\xdc\xd1Y}')  # 0xdcd1597d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.height_variation_max))

        data.write(b':\xb1\xf6\x9c')  # 0x3ab1f69c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.height_variation_min))

        data.write(b'e\x815\x8c')  # 0x6581358c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.floor_buffer))

        data.write(b'\x11[\xb3\x8c')  # 0x115bb38c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ceiling_buffer))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            speed=data['speed'],
            acceleration=data['acceleration'],
            turn_rate=data['turn_rate'],
            facing_turn_rate=data['facing_turn_rate'],
            turn_threshold=data['turn_threshold'],
            use_avoidance=data['use_avoidance'],
            avoidance_range=data['avoidance_range'],
            unknown=data['unknown'],
            height_variation_max=data['height_variation_max'],
            height_variation_min=data['height_variation_min'],
            floor_buffer=data['floor_buffer'],
            ceiling_buffer=data['ceiling_buffer'],
        )

    def to_json(self) -> dict:
        return {
            'speed': self.speed,
            'acceleration': self.acceleration,
            'turn_rate': self.turn_rate,
            'facing_turn_rate': self.facing_turn_rate,
            'turn_threshold': self.turn_threshold,
            'use_avoidance': self.use_avoidance,
            'avoidance_range': self.avoidance_range,
            'unknown': self.unknown,
            'height_variation_max': self.height_variation_max,
            'height_variation_min': self.height_variation_min,
            'floor_buffer': self.floor_buffer,
            'ceiling_buffer': self.ceiling_buffer,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x6392404e, 0x39fb7978, 0xe34dc703, 0x6c6426c8, 0xc0ac271e, 0x9699fa45, 0x50a9bd0d, 0x1a7b77ab, 0xdcd1597d, 0x3ab1f69c, 0x6581358c, 0x115bb38c)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[FlyerMovementMode]:
    if property_count != 12:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHfLHfLH?LHfLHfLHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(117))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27], dec[30], dec[33]) != _FAST_IDS:
        data.seek(before)
        return None

    return FlyerMovementMode(
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
    )


def _decode_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_turn_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_facing_turn_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_turn_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_use_avoidance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_avoidance_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_height_variation_max(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_height_variation_min(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_floor_buffer(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ceiling_buffer(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x6392404e: ('speed', _decode_speed),
    0x39fb7978: ('acceleration', _decode_acceleration),
    0xe34dc703: ('turn_rate', _decode_turn_rate),
    0x6c6426c8: ('facing_turn_rate', _decode_facing_turn_rate),
    0xc0ac271e: ('turn_threshold', _decode_turn_threshold),
    0x9699fa45: ('use_avoidance', _decode_use_avoidance),
    0x50a9bd0d: ('avoidance_range', _decode_avoidance_range),
    0x1a7b77ab: ('unknown', _decode_unknown),
    0xdcd1597d: ('height_variation_max', _decode_height_variation_max),
    0x3ab1f69c: ('height_variation_min', _decode_height_variation_min),
    0x6581358c: ('floor_buffer', _decode_floor_buffer),
    0x115bb38c: ('ceiling_buffer', _decode_ceiling_buffer),
}
