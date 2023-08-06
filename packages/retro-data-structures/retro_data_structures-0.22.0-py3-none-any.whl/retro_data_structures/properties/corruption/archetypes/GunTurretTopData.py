# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.archetypes.StaticGeometryTest import StaticGeometryTest
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class GunTurretTopData(BaseProperty):
    is_pirate_turret: bool = dataclasses.field(default=False)
    unknown_0xf54e1111: bool = dataclasses.field(default=False)
    shoots_at_player: bool = dataclasses.field(default=False)
    unknown_0x5219dccd: bool = dataclasses.field(default=True)
    instant_hit_range: float = dataclasses.field(default=100.0)
    static_geometry_test: StaticGeometryTest = dataclasses.field(default_factory=StaticGeometryTest)
    tracking_speed: float = dataclasses.field(default=180.0)
    panning_speed: float = dataclasses.field(default=10.0)
    unknown_0x4b106481: float = dataclasses.field(default=0.0)
    unknown_0xa1dd15f6: float = dataclasses.field(default=0.0)
    unknown_0x95e7a2c2: float = dataclasses.field(default=1.0)
    unknown_0x76ba1c18: float = dataclasses.field(default=3.0)
    unknown_0x3eb2de35: float = dataclasses.field(default=1.0)
    unknown_0xe50d8dd2: float = dataclasses.field(default=1.0)
    unknown_0x64d482d5: int = dataclasses.field(default=1)
    unknown_0xc3e002ac: int = dataclasses.field(default=5)
    crsc: AssetId = dataclasses.field(metadata={'asset_types': ['CRSC']}, default=default_asset_id)
    wpsc: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    projectile_damage_info: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0x4173ec53: float = dataclasses.field(default=10.0)
    shot_angle_variance: float = dataclasses.field(default=5.0)

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

        data.write(b'p\x1de\xcd')  # 0x701d65cd
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_pirate_turret))

        data.write(b'\xf5N\x11\x11')  # 0xf54e1111
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xf54e1111))

        data.write(b'\nxF\xec')  # 0xa7846ec
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.shoots_at_player))

        data.write(b'R\x19\xdc\xcd')  # 0x5219dccd
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x5219dccd))

        data.write(b'\x0b\xd3yM')  # 0xbd3794d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.instant_hit_range))

        data.write(b'\xcf\xa1\xac\xe2')  # 0xcfa1ace2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.static_geometry_test.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfeh)\xec')  # 0xfe6829ec
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.tracking_speed))

        data.write(b'M(R>')  # 0x4d28523e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.panning_speed))

        data.write(b'K\x10d\x81')  # 0x4b106481
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4b106481))

        data.write(b'\xa1\xdd\x15\xf6')  # 0xa1dd15f6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa1dd15f6))

        data.write(b'\x95\xe7\xa2\xc2')  # 0x95e7a2c2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x95e7a2c2))

        data.write(b'v\xba\x1c\x18')  # 0x76ba1c18
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x76ba1c18))

        data.write(b'>\xb2\xde5')  # 0x3eb2de35
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3eb2de35))

        data.write(b'\xe5\r\x8d\xd2')  # 0xe50d8dd2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe50d8dd2))

        data.write(b'd\xd4\x82\xd5')  # 0x64d482d5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x64d482d5))

        data.write(b'\xc3\xe0\x02\xac')  # 0xc3e002ac
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xc3e002ac))

        data.write(b'\x16\xe7\xd7J')  # 0x16e7d74a
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.crsc))

        data.write(b'\x00\xe9\xc7,')  # 0xe9c72c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.wpsc))

        data.write(b'\xbe\x7f\xb5\xcc')  # 0xbe7fb5cc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.projectile_damage_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'As\xecS')  # 0x4173ec53
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4173ec53))

        data.write(b'\xd7_\x9c\xf2')  # 0xd75f9cf2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.shot_angle_variance))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            is_pirate_turret=data['is_pirate_turret'],
            unknown_0xf54e1111=data['unknown_0xf54e1111'],
            shoots_at_player=data['shoots_at_player'],
            unknown_0x5219dccd=data['unknown_0x5219dccd'],
            instant_hit_range=data['instant_hit_range'],
            static_geometry_test=StaticGeometryTest.from_json(data['static_geometry_test']),
            tracking_speed=data['tracking_speed'],
            panning_speed=data['panning_speed'],
            unknown_0x4b106481=data['unknown_0x4b106481'],
            unknown_0xa1dd15f6=data['unknown_0xa1dd15f6'],
            unknown_0x95e7a2c2=data['unknown_0x95e7a2c2'],
            unknown_0x76ba1c18=data['unknown_0x76ba1c18'],
            unknown_0x3eb2de35=data['unknown_0x3eb2de35'],
            unknown_0xe50d8dd2=data['unknown_0xe50d8dd2'],
            unknown_0x64d482d5=data['unknown_0x64d482d5'],
            unknown_0xc3e002ac=data['unknown_0xc3e002ac'],
            crsc=data['crsc'],
            wpsc=data['wpsc'],
            projectile_damage_info=DamageInfo.from_json(data['projectile_damage_info']),
            unknown_0x4173ec53=data['unknown_0x4173ec53'],
            shot_angle_variance=data['shot_angle_variance'],
        )

    def to_json(self) -> dict:
        return {
            'is_pirate_turret': self.is_pirate_turret,
            'unknown_0xf54e1111': self.unknown_0xf54e1111,
            'shoots_at_player': self.shoots_at_player,
            'unknown_0x5219dccd': self.unknown_0x5219dccd,
            'instant_hit_range': self.instant_hit_range,
            'static_geometry_test': self.static_geometry_test.to_json(),
            'tracking_speed': self.tracking_speed,
            'panning_speed': self.panning_speed,
            'unknown_0x4b106481': self.unknown_0x4b106481,
            'unknown_0xa1dd15f6': self.unknown_0xa1dd15f6,
            'unknown_0x95e7a2c2': self.unknown_0x95e7a2c2,
            'unknown_0x76ba1c18': self.unknown_0x76ba1c18,
            'unknown_0x3eb2de35': self.unknown_0x3eb2de35,
            'unknown_0xe50d8dd2': self.unknown_0xe50d8dd2,
            'unknown_0x64d482d5': self.unknown_0x64d482d5,
            'unknown_0xc3e002ac': self.unknown_0xc3e002ac,
            'crsc': self.crsc,
            'wpsc': self.wpsc,
            'projectile_damage_info': self.projectile_damage_info.to_json(),
            'unknown_0x4173ec53': self.unknown_0x4173ec53,
            'shot_angle_variance': self.shot_angle_variance,
        }


def _decode_is_pirate_turret(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xf54e1111(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_shoots_at_player(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x5219dccd(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_instant_hit_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_static_geometry_test(data: typing.BinaryIO, property_size: int):
    return StaticGeometryTest.from_stream(data, property_size)


def _decode_tracking_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_panning_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4b106481(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa1dd15f6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x95e7a2c2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x76ba1c18(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x3eb2de35(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe50d8dd2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x64d482d5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xc3e002ac(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_crsc(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_wpsc(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_projectile_damage_info(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_unknown_0x4173ec53(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_shot_angle_variance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x701d65cd: ('is_pirate_turret', _decode_is_pirate_turret),
    0xf54e1111: ('unknown_0xf54e1111', _decode_unknown_0xf54e1111),
    0xa7846ec: ('shoots_at_player', _decode_shoots_at_player),
    0x5219dccd: ('unknown_0x5219dccd', _decode_unknown_0x5219dccd),
    0xbd3794d: ('instant_hit_range', _decode_instant_hit_range),
    0xcfa1ace2: ('static_geometry_test', _decode_static_geometry_test),
    0xfe6829ec: ('tracking_speed', _decode_tracking_speed),
    0x4d28523e: ('panning_speed', _decode_panning_speed),
    0x4b106481: ('unknown_0x4b106481', _decode_unknown_0x4b106481),
    0xa1dd15f6: ('unknown_0xa1dd15f6', _decode_unknown_0xa1dd15f6),
    0x95e7a2c2: ('unknown_0x95e7a2c2', _decode_unknown_0x95e7a2c2),
    0x76ba1c18: ('unknown_0x76ba1c18', _decode_unknown_0x76ba1c18),
    0x3eb2de35: ('unknown_0x3eb2de35', _decode_unknown_0x3eb2de35),
    0xe50d8dd2: ('unknown_0xe50d8dd2', _decode_unknown_0xe50d8dd2),
    0x64d482d5: ('unknown_0x64d482d5', _decode_unknown_0x64d482d5),
    0xc3e002ac: ('unknown_0xc3e002ac', _decode_unknown_0xc3e002ac),
    0x16e7d74a: ('crsc', _decode_crsc),
    0xe9c72c: ('wpsc', _decode_wpsc),
    0xbe7fb5cc: ('projectile_damage_info', _decode_projectile_damage_info),
    0x4173ec53: ('unknown_0x4173ec53', _decode_unknown_0x4173ec53),
    0xd75f9cf2: ('shot_angle_variance', _decode_shot_angle_variance),
}
