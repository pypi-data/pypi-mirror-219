# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class WallCrawlerData(BaseProperty):
    collision_radius: float = dataclasses.field(default=1.0)
    stick_radius: float = dataclasses.field(default=1.0)
    floor_turn_speed: float = dataclasses.field(default=60.0)
    waypoint_approach_distance: float = dataclasses.field(default=1.0)
    visible_distance: float = dataclasses.field(default=1.0)
    projectile_bounds_multiplier: float = dataclasses.field(default=1.0)
    unknown_0x519c7197: float = dataclasses.field(default=0.16699999570846558)
    unknown_0x1431157a: float = dataclasses.field(default=0.6000000238418579)
    unknown_0x2d5bfae8: float = dataclasses.field(default=1.5)
    unknown_0x79e70805: float = dataclasses.field(default=0.6000000238418579)
    unknown_0xed8c4058: float = dataclasses.field(default=1.5)
    is_paused: bool = dataclasses.field(default=False)

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

        data.write(b'\x8aj\xb19')  # 0x8a6ab139
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.collision_radius))

        data.write(b'Z:0\xf4')  # 0x5a3a30f4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.stick_radius))

        data.write(b'\x8eO{)')  # 0x8e4f7b29
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.floor_turn_speed))

        data.write(b's;\xd2|')  # 0x733bd27c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.waypoint_approach_distance))

        data.write(b'\xa7%0\xe8')  # 0xa72530e8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.visible_distance))

        data.write(b't.\xab ')  # 0x742eab20
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.projectile_bounds_multiplier))

        data.write(b'Q\x9cq\x97')  # 0x519c7197
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x519c7197))

        data.write(b'\x141\x15z')  # 0x1431157a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x1431157a))

        data.write(b'-[\xfa\xe8')  # 0x2d5bfae8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2d5bfae8))

        data.write(b'y\xe7\x08\x05')  # 0x79e70805
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x79e70805))

        data.write(b'\xed\x8c@X')  # 0xed8c4058
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xed8c4058))

        data.write(b'\xc5R`\x04')  # 0xc5526004
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_paused))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            collision_radius=data['collision_radius'],
            stick_radius=data['stick_radius'],
            floor_turn_speed=data['floor_turn_speed'],
            waypoint_approach_distance=data['waypoint_approach_distance'],
            visible_distance=data['visible_distance'],
            projectile_bounds_multiplier=data['projectile_bounds_multiplier'],
            unknown_0x519c7197=data['unknown_0x519c7197'],
            unknown_0x1431157a=data['unknown_0x1431157a'],
            unknown_0x2d5bfae8=data['unknown_0x2d5bfae8'],
            unknown_0x79e70805=data['unknown_0x79e70805'],
            unknown_0xed8c4058=data['unknown_0xed8c4058'],
            is_paused=data['is_paused'],
        )

    def to_json(self) -> dict:
        return {
            'collision_radius': self.collision_radius,
            'stick_radius': self.stick_radius,
            'floor_turn_speed': self.floor_turn_speed,
            'waypoint_approach_distance': self.waypoint_approach_distance,
            'visible_distance': self.visible_distance,
            'projectile_bounds_multiplier': self.projectile_bounds_multiplier,
            'unknown_0x519c7197': self.unknown_0x519c7197,
            'unknown_0x1431157a': self.unknown_0x1431157a,
            'unknown_0x2d5bfae8': self.unknown_0x2d5bfae8,
            'unknown_0x79e70805': self.unknown_0x79e70805,
            'unknown_0xed8c4058': self.unknown_0xed8c4058,
            'is_paused': self.is_paused,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x8a6ab139, 0x5a3a30f4, 0x8e4f7b29, 0x733bd27c, 0xa72530e8, 0x742eab20, 0x519c7197, 0x1431157a, 0x2d5bfae8, 0x79e70805, 0xed8c4058, 0xc5526004)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[WallCrawlerData]:
    if property_count != 12:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLH?')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(117))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27], dec[30], dec[33]) != _FAST_IDS:
        data.seek(before)
        return None

    return WallCrawlerData(
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


def _decode_collision_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_stick_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_floor_turn_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_waypoint_approach_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_visible_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_projectile_bounds_multiplier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x519c7197(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x1431157a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x2d5bfae8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x79e70805(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xed8c4058(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_is_paused(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x8a6ab139: ('collision_radius', _decode_collision_radius),
    0x5a3a30f4: ('stick_radius', _decode_stick_radius),
    0x8e4f7b29: ('floor_turn_speed', _decode_floor_turn_speed),
    0x733bd27c: ('waypoint_approach_distance', _decode_waypoint_approach_distance),
    0xa72530e8: ('visible_distance', _decode_visible_distance),
    0x742eab20: ('projectile_bounds_multiplier', _decode_projectile_bounds_multiplier),
    0x519c7197: ('unknown_0x519c7197', _decode_unknown_0x519c7197),
    0x1431157a: ('unknown_0x1431157a', _decode_unknown_0x1431157a),
    0x2d5bfae8: ('unknown_0x2d5bfae8', _decode_unknown_0x2d5bfae8),
    0x79e70805: ('unknown_0x79e70805', _decode_unknown_0x79e70805),
    0xed8c4058: ('unknown_0xed8c4058', _decode_unknown_0xed8c4058),
    0xc5526004: ('is_paused', _decode_is_paused),
}
