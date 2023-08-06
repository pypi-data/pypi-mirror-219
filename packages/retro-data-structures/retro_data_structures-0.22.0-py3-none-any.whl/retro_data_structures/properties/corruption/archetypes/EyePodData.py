# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.archetypes.EyePodStruct import EyePodStruct
from retro_data_structures.properties.corruption.archetypes.StaticGeometryTest import StaticGeometryTest
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class EyePodData(BaseProperty):
    hearing_range: float = dataclasses.field(default=20.0)
    lose_interest_distance: float = dataclasses.field(default=40.0)
    lose_interest_time: float = dataclasses.field(default=5.0)
    unknown_0x95e7a2c2: float = dataclasses.field(default=2.0)
    unknown_0x76ba1c18: float = dataclasses.field(default=5.0)
    unknown_0x64d482d5: int = dataclasses.field(default=1)
    unknown_0xc3e002ac: int = dataclasses.field(default=4)
    unknown_0x4da7906b: float = dataclasses.field(default=0.25)
    unknown_0xa2258e11: float = dataclasses.field(default=0.5)
    min_charge_time: float = dataclasses.field(default=0.25)
    max_charge_time: float = dataclasses.field(default=0.5)
    unknown_0x88f13a51: float = dataclasses.field(default=5.0)
    unknown_0x6773242b: float = dataclasses.field(default=7.0)
    rapid_fire_projectile: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    charge_shot_projectile: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    rapid_fire_damage_info: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    charge_shot_damage_info: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    shot_angle_variance: float = dataclasses.field(default=5.0)
    charge_shot_enabled: bool = dataclasses.field(default=True)
    unknown_0x3db05763: float = dataclasses.field(default=20.0)
    turn_anim_speed: float = dataclasses.field(default=2.0)
    eye_pod_struct_0x5b0a8c8a: EyePodStruct = dataclasses.field(default_factory=EyePodStruct)
    eye_pod_struct_0x0ce679bb: EyePodStruct = dataclasses.field(default_factory=EyePodStruct)
    eye_pod_struct_0xf9bbcc33: EyePodStruct = dataclasses.field(default_factory=EyePodStruct)
    starts_invulnerable: bool = dataclasses.field(default=False)
    unknown_0xa1ed5408: bool = dataclasses.field(default=False)
    shot_collision_test: StaticGeometryTest = dataclasses.field(default_factory=StaticGeometryTest)

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
        data.write(b'\x00\x1b')  # 27 properties

        data.write(b'%GEP')  # 0x25474550
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hearing_range))

        data.write(b'\xf6\xb0Q\xb3')  # 0xf6b051b3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.lose_interest_distance))

        data.write(b'\xf8\xb0\xc2\xbb')  # 0xf8b0c2bb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.lose_interest_time))

        data.write(b'\x95\xe7\xa2\xc2')  # 0x95e7a2c2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x95e7a2c2))

        data.write(b'v\xba\x1c\x18')  # 0x76ba1c18
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x76ba1c18))

        data.write(b'd\xd4\x82\xd5')  # 0x64d482d5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x64d482d5))

        data.write(b'\xc3\xe0\x02\xac')  # 0xc3e002ac
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xc3e002ac))

        data.write(b'M\xa7\x90k')  # 0x4da7906b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4da7906b))

        data.write(b'\xa2%\x8e\x11')  # 0xa2258e11
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa2258e11))

        data.write(b'\xb6\xa0FL')  # 0xb6a0464c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_charge_time))

        data.write(b'\xe5\x06^\xa8')  # 0xe5065ea8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_charge_time))

        data.write(b'\x88\xf1:Q')  # 0x88f13a51
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x88f13a51))

        data.write(b'gs$+')  # 0x6773242b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x6773242b))

        data.write(b'\xe8\xc8\x19\xe6')  # 0xe8c819e6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.rapid_fire_projectile))

        data.write(b'\xb1O\xeaR')  # 0xb14fea52
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.charge_shot_projectile))

        data.write(b'\xc91\t\xe7')  # 0xc93109e7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rapid_fire_damage_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'7\xa6\xf5b')  # 0x37a6f562
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.charge_shot_damage_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd7_\x9c\xf2')  # 0xd75f9cf2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.shot_angle_variance))

        data.write(b'pv\xd42')  # 0x7076d432
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.charge_shot_enabled))

        data.write(b'=\xb0Wc')  # 0x3db05763
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3db05763))

        data.write(b'\x19\x0c\xb8\xd7')  # 0x190cb8d7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.turn_anim_speed))

        data.write(b'[\n\x8c\x8a')  # 0x5b0a8c8a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.eye_pod_struct_0x5b0a8c8a.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x0c\xe6y\xbb')  # 0xce679bb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.eye_pod_struct_0x0ce679bb.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf9\xbb\xcc3')  # 0xf9bbcc33
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.eye_pod_struct_0xf9bbcc33.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf1\xc2G\xff')  # 0xf1c247ff
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.starts_invulnerable))

        data.write(b'\xa1\xedT\x08')  # 0xa1ed5408
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xa1ed5408))

        data.write(b'Q\x19a\xd4')  # 0x511961d4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.shot_collision_test.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            hearing_range=data['hearing_range'],
            lose_interest_distance=data['lose_interest_distance'],
            lose_interest_time=data['lose_interest_time'],
            unknown_0x95e7a2c2=data['unknown_0x95e7a2c2'],
            unknown_0x76ba1c18=data['unknown_0x76ba1c18'],
            unknown_0x64d482d5=data['unknown_0x64d482d5'],
            unknown_0xc3e002ac=data['unknown_0xc3e002ac'],
            unknown_0x4da7906b=data['unknown_0x4da7906b'],
            unknown_0xa2258e11=data['unknown_0xa2258e11'],
            min_charge_time=data['min_charge_time'],
            max_charge_time=data['max_charge_time'],
            unknown_0x88f13a51=data['unknown_0x88f13a51'],
            unknown_0x6773242b=data['unknown_0x6773242b'],
            rapid_fire_projectile=data['rapid_fire_projectile'],
            charge_shot_projectile=data['charge_shot_projectile'],
            rapid_fire_damage_info=DamageInfo.from_json(data['rapid_fire_damage_info']),
            charge_shot_damage_info=DamageInfo.from_json(data['charge_shot_damage_info']),
            shot_angle_variance=data['shot_angle_variance'],
            charge_shot_enabled=data['charge_shot_enabled'],
            unknown_0x3db05763=data['unknown_0x3db05763'],
            turn_anim_speed=data['turn_anim_speed'],
            eye_pod_struct_0x5b0a8c8a=EyePodStruct.from_json(data['eye_pod_struct_0x5b0a8c8a']),
            eye_pod_struct_0x0ce679bb=EyePodStruct.from_json(data['eye_pod_struct_0x0ce679bb']),
            eye_pod_struct_0xf9bbcc33=EyePodStruct.from_json(data['eye_pod_struct_0xf9bbcc33']),
            starts_invulnerable=data['starts_invulnerable'],
            unknown_0xa1ed5408=data['unknown_0xa1ed5408'],
            shot_collision_test=StaticGeometryTest.from_json(data['shot_collision_test']),
        )

    def to_json(self) -> dict:
        return {
            'hearing_range': self.hearing_range,
            'lose_interest_distance': self.lose_interest_distance,
            'lose_interest_time': self.lose_interest_time,
            'unknown_0x95e7a2c2': self.unknown_0x95e7a2c2,
            'unknown_0x76ba1c18': self.unknown_0x76ba1c18,
            'unknown_0x64d482d5': self.unknown_0x64d482d5,
            'unknown_0xc3e002ac': self.unknown_0xc3e002ac,
            'unknown_0x4da7906b': self.unknown_0x4da7906b,
            'unknown_0xa2258e11': self.unknown_0xa2258e11,
            'min_charge_time': self.min_charge_time,
            'max_charge_time': self.max_charge_time,
            'unknown_0x88f13a51': self.unknown_0x88f13a51,
            'unknown_0x6773242b': self.unknown_0x6773242b,
            'rapid_fire_projectile': self.rapid_fire_projectile,
            'charge_shot_projectile': self.charge_shot_projectile,
            'rapid_fire_damage_info': self.rapid_fire_damage_info.to_json(),
            'charge_shot_damage_info': self.charge_shot_damage_info.to_json(),
            'shot_angle_variance': self.shot_angle_variance,
            'charge_shot_enabled': self.charge_shot_enabled,
            'unknown_0x3db05763': self.unknown_0x3db05763,
            'turn_anim_speed': self.turn_anim_speed,
            'eye_pod_struct_0x5b0a8c8a': self.eye_pod_struct_0x5b0a8c8a.to_json(),
            'eye_pod_struct_0x0ce679bb': self.eye_pod_struct_0x0ce679bb.to_json(),
            'eye_pod_struct_0xf9bbcc33': self.eye_pod_struct_0xf9bbcc33.to_json(),
            'starts_invulnerable': self.starts_invulnerable,
            'unknown_0xa1ed5408': self.unknown_0xa1ed5408,
            'shot_collision_test': self.shot_collision_test.to_json(),
        }


def _decode_hearing_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_lose_interest_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_lose_interest_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x95e7a2c2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x76ba1c18(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x64d482d5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xc3e002ac(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x4da7906b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa2258e11(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_charge_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_charge_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x88f13a51(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x6773242b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rapid_fire_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_charge_shot_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_rapid_fire_damage_info(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_charge_shot_damage_info(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_shot_angle_variance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_charge_shot_enabled(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x3db05763(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_turn_anim_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_eye_pod_struct_0x5b0a8c8a(data: typing.BinaryIO, property_size: int):
    return EyePodStruct.from_stream(data, property_size)


def _decode_eye_pod_struct_0x0ce679bb(data: typing.BinaryIO, property_size: int):
    return EyePodStruct.from_stream(data, property_size)


def _decode_eye_pod_struct_0xf9bbcc33(data: typing.BinaryIO, property_size: int):
    return EyePodStruct.from_stream(data, property_size)


def _decode_starts_invulnerable(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xa1ed5408(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_shot_collision_test(data: typing.BinaryIO, property_size: int):
    return StaticGeometryTest.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x25474550: ('hearing_range', _decode_hearing_range),
    0xf6b051b3: ('lose_interest_distance', _decode_lose_interest_distance),
    0xf8b0c2bb: ('lose_interest_time', _decode_lose_interest_time),
    0x95e7a2c2: ('unknown_0x95e7a2c2', _decode_unknown_0x95e7a2c2),
    0x76ba1c18: ('unknown_0x76ba1c18', _decode_unknown_0x76ba1c18),
    0x64d482d5: ('unknown_0x64d482d5', _decode_unknown_0x64d482d5),
    0xc3e002ac: ('unknown_0xc3e002ac', _decode_unknown_0xc3e002ac),
    0x4da7906b: ('unknown_0x4da7906b', _decode_unknown_0x4da7906b),
    0xa2258e11: ('unknown_0xa2258e11', _decode_unknown_0xa2258e11),
    0xb6a0464c: ('min_charge_time', _decode_min_charge_time),
    0xe5065ea8: ('max_charge_time', _decode_max_charge_time),
    0x88f13a51: ('unknown_0x88f13a51', _decode_unknown_0x88f13a51),
    0x6773242b: ('unknown_0x6773242b', _decode_unknown_0x6773242b),
    0xe8c819e6: ('rapid_fire_projectile', _decode_rapid_fire_projectile),
    0xb14fea52: ('charge_shot_projectile', _decode_charge_shot_projectile),
    0xc93109e7: ('rapid_fire_damage_info', _decode_rapid_fire_damage_info),
    0x37a6f562: ('charge_shot_damage_info', _decode_charge_shot_damage_info),
    0xd75f9cf2: ('shot_angle_variance', _decode_shot_angle_variance),
    0x7076d432: ('charge_shot_enabled', _decode_charge_shot_enabled),
    0x3db05763: ('unknown_0x3db05763', _decode_unknown_0x3db05763),
    0x190cb8d7: ('turn_anim_speed', _decode_turn_anim_speed),
    0x5b0a8c8a: ('eye_pod_struct_0x5b0a8c8a', _decode_eye_pod_struct_0x5b0a8c8a),
    0xce679bb: ('eye_pod_struct_0x0ce679bb', _decode_eye_pod_struct_0x0ce679bb),
    0xf9bbcc33: ('eye_pod_struct_0xf9bbcc33', _decode_eye_pod_struct_0xf9bbcc33),
    0xf1c247ff: ('starts_invulnerable', _decode_starts_invulnerable),
    0xa1ed5408: ('unknown_0xa1ed5408', _decode_unknown_0xa1ed5408),
    0x511961d4: ('shot_collision_test', _decode_shot_collision_test),
}
