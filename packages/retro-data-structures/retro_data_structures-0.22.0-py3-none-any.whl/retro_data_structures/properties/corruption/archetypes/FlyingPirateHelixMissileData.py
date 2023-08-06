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
class FlyingPirateHelixMissileData(BaseProperty):
    projectile_static_geometry_test: StaticGeometryTest = dataclasses.field(default_factory=StaticGeometryTest)
    projectile_left: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    projectile_right: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    visor_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART', 'ELSC']}, default=default_asset_id)
    visor_impact_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    stop_homing_range: float = dataclasses.field(default=10.0)
    min_attack_range: float = dataclasses.field(default=20.0)
    max_attack_range: float = dataclasses.field(default=50.0)
    min_attack_time: float = dataclasses.field(default=3.0)
    attack_time_variance: float = dataclasses.field(default=1.0)

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
        data.write(b'\x00\x0b')  # 11 properties

        data.write(b'\x9a\x89(\x18')  # 0x9a892818
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.projectile_static_geometry_test.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf0\xd2RV')  # 0xf0d25256
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.projectile_left))

        data.write(b'd^\x8c\xc5')  # 0x645e8cc5
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.projectile_right))

        data.write(b'3\x7f\x95$')  # 0x337f9524
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe9\xc8\xe2\xbd')  # 0xe9c8e2bd
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.visor_effect))

        data.write(b'\x86\xff\xb3\xf6')  # 0x86ffb3f6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.visor_impact_sound))

        data.write(b'\x05:\xe4\xa7')  # 0x53ae4a7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.stop_homing_range))

        data.write(b'XCI\x16')  # 0x58434916
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_attack_range))

        data.write(b'\xffw\xc9o')  # 0xff77c96f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_attack_range))

        data.write(b'.\xdf3h')  # 0x2edf3368
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_attack_time))

        data.write(b'\x9f&\x96\x14')  # 0x9f269614
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.attack_time_variance))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            projectile_static_geometry_test=StaticGeometryTest.from_json(data['projectile_static_geometry_test']),
            projectile_left=data['projectile_left'],
            projectile_right=data['projectile_right'],
            damage=DamageInfo.from_json(data['damage']),
            visor_effect=data['visor_effect'],
            visor_impact_sound=data['visor_impact_sound'],
            stop_homing_range=data['stop_homing_range'],
            min_attack_range=data['min_attack_range'],
            max_attack_range=data['max_attack_range'],
            min_attack_time=data['min_attack_time'],
            attack_time_variance=data['attack_time_variance'],
        )

    def to_json(self) -> dict:
        return {
            'projectile_static_geometry_test': self.projectile_static_geometry_test.to_json(),
            'projectile_left': self.projectile_left,
            'projectile_right': self.projectile_right,
            'damage': self.damage.to_json(),
            'visor_effect': self.visor_effect,
            'visor_impact_sound': self.visor_impact_sound,
            'stop_homing_range': self.stop_homing_range,
            'min_attack_range': self.min_attack_range,
            'max_attack_range': self.max_attack_range,
            'min_attack_time': self.min_attack_time,
            'attack_time_variance': self.attack_time_variance,
        }


def _decode_projectile_static_geometry_test(data: typing.BinaryIO, property_size: int):
    return StaticGeometryTest.from_stream(data, property_size)


def _decode_projectile_left(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_projectile_right(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_visor_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_visor_impact_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_stop_homing_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_attack_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_attack_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_attack_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_attack_time_variance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x9a892818: ('projectile_static_geometry_test', _decode_projectile_static_geometry_test),
    0xf0d25256: ('projectile_left', _decode_projectile_left),
    0x645e8cc5: ('projectile_right', _decode_projectile_right),
    0x337f9524: ('damage', _decode_damage),
    0xe9c8e2bd: ('visor_effect', _decode_visor_effect),
    0x86ffb3f6: ('visor_impact_sound', _decode_visor_impact_sound),
    0x53ae4a7: ('stop_homing_range', _decode_stop_homing_range),
    0x58434916: ('min_attack_range', _decode_min_attack_range),
    0xff77c96f: ('max_attack_range', _decode_max_attack_range),
    0x2edf3368: ('min_attack_time', _decode_min_attack_time),
    0x9f269614: ('attack_time_variance', _decode_attack_time_variance),
}
