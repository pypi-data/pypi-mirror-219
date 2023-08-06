# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class PTCNoseTurretData(BaseProperty):
    aiming_prediction: float = dataclasses.field(default=0.5)
    scanning_range_min: float = dataclasses.field(default=-90.0)
    scanning_range_max: float = dataclasses.field(default=90.0)
    scanning_speed: float = dataclasses.field(default=90.0)
    max_detection_angle: float = dataclasses.field(default=90.0)
    unknown_0x494be648: float = dataclasses.field(default=0.0)
    max_attack_angle: float = dataclasses.field(default=15.0)
    max_rotation_speed: float = dataclasses.field(default=360.0)
    max_rotation: float = dataclasses.field(default=135.0)
    min_rotation: float = dataclasses.field(default=-135.0)
    max_pitch_speed: float = dataclasses.field(default=360.0)
    max_pitch: float = dataclasses.field(default=45.0)
    min_pitch: float = dataclasses.field(default=-45.0)
    projectile: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    burst_delay: float = dataclasses.field(default=1.0)
    unknown_0xb5702ca3: int = dataclasses.field(default=3)
    burst_shot_delay: float = dataclasses.field(default=0.10000000149011612)
    unknown_0xaf28dc00: int = dataclasses.field(default=2)
    sound_shot: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    unknown_0x55d9abef: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
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
        data.write(b'\x00\x15')  # 21 properties

        data.write(b'9[\x81\xef')  # 0x395b81ef
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.aiming_prediction))

        data.write(b'D\xe0\x13w')  # 0x44e01377
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.scanning_range_min))

        data.write(b'\xa2\x80\xbc\x96')  # 0xa280bc96
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.scanning_range_max))

        data.write(b'\xf7\x1cm\xd7')  # 0xf71c6dd7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.scanning_speed))

        data.write(b'g\x90(\xba')  # 0x679028ba
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_detection_angle))

        data.write(b'IK\xe6H')  # 0x494be648
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x494be648))

        data.write(b'\xf1\x1fs\x84')  # 0xf11f7384
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_attack_angle))

        data.write(b'P\xee\xb9\xe3')  # 0x50eeb9e3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_rotation_speed))

        data.write(b'w!\xde\xea')  # 0x7721deea
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_rotation))

        data.write(b'&\xd8e\xb7')  # 0x26d865b7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_rotation))

        data.write(b'\x95\x97\xa3)')  # 0x9597a329
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_pitch_speed))

        data.write(b'\xcd\x8c\x87c')  # 0xcd8c8763
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_pitch))

        data.write(b'\x8d\xc3\xff\x15')  # 0x8dc3ff15
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_pitch))

        data.write(b'\xefH]\xb9')  # 0xef485db9
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.projectile))

        data.write(b'3\x7f\x95$')  # 0x337f9524
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xeb\x904s')  # 0xeb903473
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.burst_delay))

        data.write(b'\xb5p,\xa3')  # 0xb5702ca3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xb5702ca3))

        data.write(b'\xe8\xf2\x9e\x1e')  # 0xe8f29e1e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.burst_shot_delay))

        data.write(b'\xaf(\xdc\x00')  # 0xaf28dc00
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xaf28dc00))

        data.write(b'\xc2:\x19U')  # 0xc23a1955
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound_shot))

        data.write(b'U\xd9\xab\xef')  # 0x55d9abef
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x55d9abef))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            aiming_prediction=data['aiming_prediction'],
            scanning_range_min=data['scanning_range_min'],
            scanning_range_max=data['scanning_range_max'],
            scanning_speed=data['scanning_speed'],
            max_detection_angle=data['max_detection_angle'],
            unknown_0x494be648=data['unknown_0x494be648'],
            max_attack_angle=data['max_attack_angle'],
            max_rotation_speed=data['max_rotation_speed'],
            max_rotation=data['max_rotation'],
            min_rotation=data['min_rotation'],
            max_pitch_speed=data['max_pitch_speed'],
            max_pitch=data['max_pitch'],
            min_pitch=data['min_pitch'],
            projectile=data['projectile'],
            damage=DamageInfo.from_json(data['damage']),
            burst_delay=data['burst_delay'],
            unknown_0xb5702ca3=data['unknown_0xb5702ca3'],
            burst_shot_delay=data['burst_shot_delay'],
            unknown_0xaf28dc00=data['unknown_0xaf28dc00'],
            sound_shot=data['sound_shot'],
            unknown_0x55d9abef=data['unknown_0x55d9abef'],
        )

    def to_json(self) -> dict:
        return {
            'aiming_prediction': self.aiming_prediction,
            'scanning_range_min': self.scanning_range_min,
            'scanning_range_max': self.scanning_range_max,
            'scanning_speed': self.scanning_speed,
            'max_detection_angle': self.max_detection_angle,
            'unknown_0x494be648': self.unknown_0x494be648,
            'max_attack_angle': self.max_attack_angle,
            'max_rotation_speed': self.max_rotation_speed,
            'max_rotation': self.max_rotation,
            'min_rotation': self.min_rotation,
            'max_pitch_speed': self.max_pitch_speed,
            'max_pitch': self.max_pitch,
            'min_pitch': self.min_pitch,
            'projectile': self.projectile,
            'damage': self.damage.to_json(),
            'burst_delay': self.burst_delay,
            'unknown_0xb5702ca3': self.unknown_0xb5702ca3,
            'burst_shot_delay': self.burst_shot_delay,
            'unknown_0xaf28dc00': self.unknown_0xaf28dc00,
            'sound_shot': self.sound_shot,
            'unknown_0x55d9abef': self.unknown_0x55d9abef,
        }


def _decode_aiming_prediction(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_scanning_range_min(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_scanning_range_max(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_scanning_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_detection_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x494be648(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_attack_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_rotation_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_rotation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_rotation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_pitch_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_pitch(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_pitch(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_burst_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb5702ca3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_burst_shot_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xaf28dc00(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_shot(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x55d9abef(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x395b81ef: ('aiming_prediction', _decode_aiming_prediction),
    0x44e01377: ('scanning_range_min', _decode_scanning_range_min),
    0xa280bc96: ('scanning_range_max', _decode_scanning_range_max),
    0xf71c6dd7: ('scanning_speed', _decode_scanning_speed),
    0x679028ba: ('max_detection_angle', _decode_max_detection_angle),
    0x494be648: ('unknown_0x494be648', _decode_unknown_0x494be648),
    0xf11f7384: ('max_attack_angle', _decode_max_attack_angle),
    0x50eeb9e3: ('max_rotation_speed', _decode_max_rotation_speed),
    0x7721deea: ('max_rotation', _decode_max_rotation),
    0x26d865b7: ('min_rotation', _decode_min_rotation),
    0x9597a329: ('max_pitch_speed', _decode_max_pitch_speed),
    0xcd8c8763: ('max_pitch', _decode_max_pitch),
    0x8dc3ff15: ('min_pitch', _decode_min_pitch),
    0xef485db9: ('projectile', _decode_projectile),
    0x337f9524: ('damage', _decode_damage),
    0xeb903473: ('burst_delay', _decode_burst_delay),
    0xb5702ca3: ('unknown_0xb5702ca3', _decode_unknown_0xb5702ca3),
    0xe8f29e1e: ('burst_shot_delay', _decode_burst_shot_delay),
    0xaf28dc00: ('unknown_0xaf28dc00', _decode_unknown_0xaf28dc00),
    0xc23a1955: ('sound_shot', _decode_sound_shot),
    0x55d9abef: ('unknown_0x55d9abef', _decode_unknown_0x55d9abef),
}
