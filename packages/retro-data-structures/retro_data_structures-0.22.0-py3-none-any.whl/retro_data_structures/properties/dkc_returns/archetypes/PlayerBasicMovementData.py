# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class PlayerBasicMovementData(BaseProperty):
    use5_cycle_locomotion_set: bool = dataclasses.field(default=False)
    fidget_delay_minimum: float = dataclasses.field(default=20.0)
    fidget_delay_maximum: float = dataclasses.field(default=40.0)
    allow_edge_fidgets: bool = dataclasses.field(default=True)
    max_perch_angle: float = dataclasses.field(default=30.0)
    max_perch_movement_speed: float = dataclasses.field(default=3.0)
    off_balance_perch_fraction_threshold: float = dataclasses.field(default=0.949999988079071)
    min_perch_distance_from_edge: float = dataclasses.field(default=0.0)
    bump_into_wall_speed: float = dataclasses.field(default=8.899999618530273)
    bump_into_wall_knockback_amount: float = dataclasses.field(default=0.5)
    bump_into_wall_knockback_time: float = dataclasses.field(default=0.5)
    wall_hit_response_default_min_velocity: float = dataclasses.field(default=4.0)
    wall_hit_response_medium_min_velocity: float = dataclasses.field(default=8.0)
    wall_hit_response_heavy_min_velocity: float = dataclasses.field(default=12.0)
    wall_hit_response_default_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    wall_hit_response_medium_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    wall_hit_response_heavy_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    collision_response_default_min_velocity: float = dataclasses.field(default=15.0)
    collision_response_medium_min_velocity: float = dataclasses.field(default=22.0)
    collision_response_heavy_min_velocity: float = dataclasses.field(default=28.0)

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
        data.write(b'\x00\x14')  # 20 properties

        data.write(b'\xa6\xb7]\x03')  # 0xa6b75d03
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use5_cycle_locomotion_set))

        data.write(b'\x13u)\n')  # 0x1375290a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fidget_delay_minimum))

        data.write(b'\x83\x069\xe0')  # 0x830639e0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fidget_delay_maximum))

        data.write(b'\xa3b3V')  # 0xa3623356
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.allow_edge_fidgets))

        data.write(b'D?\xb4\xe4')  # 0x443fb4e4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_perch_angle))

        data.write(b'-o\x84H')  # 0x2d6f8448
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_perch_movement_speed))

        data.write(b'\x0e:\xf7Q')  # 0xe3af751
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.off_balance_perch_fraction_threshold))

        data.write(b'\x959\xca\xb4')  # 0x9539cab4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_perch_distance_from_edge))

        data.write(b'\x03\xc1 \xfc')  # 0x3c120fc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.bump_into_wall_speed))

        data.write(b'\xdd\xe4\xdal')  # 0xdde4da6c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.bump_into_wall_knockback_amount))

        data.write(b'\xa6\x93\x8c\x8e')  # 0xa6938c8e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.bump_into_wall_knockback_time))

        data.write(b'74g[')  # 0x3734675b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.wall_hit_response_default_min_velocity))

        data.write(b'R(:"')  # 0x52283a22
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.wall_hit_response_medium_min_velocity))

        data.write(b'\xd1?\xcd\x0e')  # 0xd13fcd0e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.wall_hit_response_heavy_min_velocity))

        data.write(b'\xfd\x15\x0b?')  # 0xfd150b3f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.wall_hit_response_default_effect))

        data.write(b'\x8c\x04\x1cM')  # 0x8c041c4d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.wall_hit_response_medium_effect))

        data.write(b'\xf0f\xf7G')  # 0xf066f747
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.wall_hit_response_heavy_effect))

        data.write(b'r\xf4\xa5\x96')  # 0x72f4a596
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.collision_response_default_min_velocity))

        data.write(b'M\xb6\x82\x0f')  # 0x4db6820f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.collision_response_medium_min_velocity))

        data.write(b'\x95\x04\x8e\xdd')  # 0x95048edd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.collision_response_heavy_min_velocity))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            use5_cycle_locomotion_set=data['use5_cycle_locomotion_set'],
            fidget_delay_minimum=data['fidget_delay_minimum'],
            fidget_delay_maximum=data['fidget_delay_maximum'],
            allow_edge_fidgets=data['allow_edge_fidgets'],
            max_perch_angle=data['max_perch_angle'],
            max_perch_movement_speed=data['max_perch_movement_speed'],
            off_balance_perch_fraction_threshold=data['off_balance_perch_fraction_threshold'],
            min_perch_distance_from_edge=data['min_perch_distance_from_edge'],
            bump_into_wall_speed=data['bump_into_wall_speed'],
            bump_into_wall_knockback_amount=data['bump_into_wall_knockback_amount'],
            bump_into_wall_knockback_time=data['bump_into_wall_knockback_time'],
            wall_hit_response_default_min_velocity=data['wall_hit_response_default_min_velocity'],
            wall_hit_response_medium_min_velocity=data['wall_hit_response_medium_min_velocity'],
            wall_hit_response_heavy_min_velocity=data['wall_hit_response_heavy_min_velocity'],
            wall_hit_response_default_effect=data['wall_hit_response_default_effect'],
            wall_hit_response_medium_effect=data['wall_hit_response_medium_effect'],
            wall_hit_response_heavy_effect=data['wall_hit_response_heavy_effect'],
            collision_response_default_min_velocity=data['collision_response_default_min_velocity'],
            collision_response_medium_min_velocity=data['collision_response_medium_min_velocity'],
            collision_response_heavy_min_velocity=data['collision_response_heavy_min_velocity'],
        )

    def to_json(self) -> dict:
        return {
            'use5_cycle_locomotion_set': self.use5_cycle_locomotion_set,
            'fidget_delay_minimum': self.fidget_delay_minimum,
            'fidget_delay_maximum': self.fidget_delay_maximum,
            'allow_edge_fidgets': self.allow_edge_fidgets,
            'max_perch_angle': self.max_perch_angle,
            'max_perch_movement_speed': self.max_perch_movement_speed,
            'off_balance_perch_fraction_threshold': self.off_balance_perch_fraction_threshold,
            'min_perch_distance_from_edge': self.min_perch_distance_from_edge,
            'bump_into_wall_speed': self.bump_into_wall_speed,
            'bump_into_wall_knockback_amount': self.bump_into_wall_knockback_amount,
            'bump_into_wall_knockback_time': self.bump_into_wall_knockback_time,
            'wall_hit_response_default_min_velocity': self.wall_hit_response_default_min_velocity,
            'wall_hit_response_medium_min_velocity': self.wall_hit_response_medium_min_velocity,
            'wall_hit_response_heavy_min_velocity': self.wall_hit_response_heavy_min_velocity,
            'wall_hit_response_default_effect': self.wall_hit_response_default_effect,
            'wall_hit_response_medium_effect': self.wall_hit_response_medium_effect,
            'wall_hit_response_heavy_effect': self.wall_hit_response_heavy_effect,
            'collision_response_default_min_velocity': self.collision_response_default_min_velocity,
            'collision_response_medium_min_velocity': self.collision_response_medium_min_velocity,
            'collision_response_heavy_min_velocity': self.collision_response_heavy_min_velocity,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xa6b75d03, 0x1375290a, 0x830639e0, 0xa3623356, 0x443fb4e4, 0x2d6f8448, 0xe3af751, 0x9539cab4, 0x3c120fc, 0xdde4da6c, 0xa6938c8e, 0x3734675b, 0x52283a22, 0xd13fcd0e, 0xfd150b3f, 0x8c041c4d, 0xf066f747, 0x72f4a596, 0x4db6820f, 0x95048edd)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[PlayerBasicMovementData]:
    if property_count != 20:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LH?LHfLHfLH?LHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHQLHQLHQLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(206))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27], dec[30], dec[33], dec[36], dec[39], dec[42], dec[45], dec[48], dec[51], dec[54], dec[57]) != _FAST_IDS:
        data.seek(before)
        return None

    return PlayerBasicMovementData(
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
        dec[50],
        dec[53],
        dec[56],
        dec[59],
    )


def _decode_use5_cycle_locomotion_set(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_fidget_delay_minimum(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fidget_delay_maximum(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_allow_edge_fidgets(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_max_perch_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_perch_movement_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_off_balance_perch_fraction_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_perch_distance_from_edge(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_bump_into_wall_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_bump_into_wall_knockback_amount(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_bump_into_wall_knockback_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_wall_hit_response_default_min_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_wall_hit_response_medium_min_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_wall_hit_response_heavy_min_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_wall_hit_response_default_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_wall_hit_response_medium_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_wall_hit_response_heavy_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_collision_response_default_min_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_collision_response_medium_min_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_collision_response_heavy_min_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa6b75d03: ('use5_cycle_locomotion_set', _decode_use5_cycle_locomotion_set),
    0x1375290a: ('fidget_delay_minimum', _decode_fidget_delay_minimum),
    0x830639e0: ('fidget_delay_maximum', _decode_fidget_delay_maximum),
    0xa3623356: ('allow_edge_fidgets', _decode_allow_edge_fidgets),
    0x443fb4e4: ('max_perch_angle', _decode_max_perch_angle),
    0x2d6f8448: ('max_perch_movement_speed', _decode_max_perch_movement_speed),
    0xe3af751: ('off_balance_perch_fraction_threshold', _decode_off_balance_perch_fraction_threshold),
    0x9539cab4: ('min_perch_distance_from_edge', _decode_min_perch_distance_from_edge),
    0x3c120fc: ('bump_into_wall_speed', _decode_bump_into_wall_speed),
    0xdde4da6c: ('bump_into_wall_knockback_amount', _decode_bump_into_wall_knockback_amount),
    0xa6938c8e: ('bump_into_wall_knockback_time', _decode_bump_into_wall_knockback_time),
    0x3734675b: ('wall_hit_response_default_min_velocity', _decode_wall_hit_response_default_min_velocity),
    0x52283a22: ('wall_hit_response_medium_min_velocity', _decode_wall_hit_response_medium_min_velocity),
    0xd13fcd0e: ('wall_hit_response_heavy_min_velocity', _decode_wall_hit_response_heavy_min_velocity),
    0xfd150b3f: ('wall_hit_response_default_effect', _decode_wall_hit_response_default_effect),
    0x8c041c4d: ('wall_hit_response_medium_effect', _decode_wall_hit_response_medium_effect),
    0xf066f747: ('wall_hit_response_heavy_effect', _decode_wall_hit_response_heavy_effect),
    0x72f4a596: ('collision_response_default_min_velocity', _decode_collision_response_default_min_velocity),
    0x4db6820f: ('collision_response_medium_min_velocity', _decode_collision_response_medium_min_velocity),
    0x95048edd: ('collision_response_heavy_min_velocity', _decode_collision_response_heavy_min_velocity),
}
