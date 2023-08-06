# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.archetypes.HoverThenHomeProjectile import HoverThenHomeProjectile
from retro_data_structures.properties.corruption.archetypes.LaunchProjectileData import LaunchProjectileData
from retro_data_structures.properties.corruption.archetypes.PlasmaBeamInfo import PlasmaBeamInfo
from retro_data_structures.properties.corruption.archetypes.UnknownStruct37 import UnknownStruct37
from retro_data_structures.properties.corruption.core.Vector import Vector


@dataclasses.dataclass()
class GhorStructB(BaseProperty):
    mini_gun_projectile: LaunchProjectileData = dataclasses.field(default_factory=LaunchProjectileData)
    beam_info: PlasmaBeamInfo = dataclasses.field(default_factory=PlasmaBeamInfo)
    beam_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    beam_constraint_angle: float = dataclasses.field(default=30.0)
    charge_attack_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    missile_hover_then_home_projectile: HoverThenHomeProjectile = dataclasses.field(default_factory=HoverThenHomeProjectile)
    missile_projectile: LaunchProjectileData = dataclasses.field(default_factory=LaunchProjectileData)
    unknown_0x63fee872: float = dataclasses.field(default=10.0)
    missile_collision_size: Vector = dataclasses.field(default_factory=lambda: Vector(x=1.0, y=1.0, z=1.0))
    unknown_0x1ba35af4: float = dataclasses.field(default=1.0)
    unknown_struct37: UnknownStruct37 = dataclasses.field(default_factory=UnknownStruct37)
    melee_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)

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
        data.write(b'\x00\x0c')  # 12 properties

        data.write(b'\x07\x8a\x03\xd9')  # 0x78a03d9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.mini_gun_projectile.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x15\x98\x01*')  # 0x1598012a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.beam_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x13\xe3\x0eM')  # 0x13e30e4d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.beam_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'L\xac\xfa\xe3')  # 0x4cacfae3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.beam_constraint_angle))

        data.write(b'\xe7\x9e\xcf\xd4')  # 0xe79ecfd4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.charge_attack_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'`;\xfd!')  # 0x603bfd21
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.missile_hover_then_home_projectile.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8fMT\xf9')  # 0x8f4d54f9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.missile_projectile.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'c\xfe\xe8r')  # 0x63fee872
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x63fee872))

        data.write(b'\xa2\xf2\x16\x8c')  # 0xa2f2168c
        data.write(b'\x00\x0c')  # size
        self.missile_collision_size.to_stream(data)

        data.write(b'\x1b\xa3Z\xf4')  # 0x1ba35af4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x1ba35af4))

        data.write(b'\xda\xe2\x13t')  # 0xdae21374
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct37.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc9A`4')  # 0xc9416034
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.melee_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            mini_gun_projectile=LaunchProjectileData.from_json(data['mini_gun_projectile']),
            beam_info=PlasmaBeamInfo.from_json(data['beam_info']),
            beam_damage=DamageInfo.from_json(data['beam_damage']),
            beam_constraint_angle=data['beam_constraint_angle'],
            charge_attack_damage=DamageInfo.from_json(data['charge_attack_damage']),
            missile_hover_then_home_projectile=HoverThenHomeProjectile.from_json(data['missile_hover_then_home_projectile']),
            missile_projectile=LaunchProjectileData.from_json(data['missile_projectile']),
            unknown_0x63fee872=data['unknown_0x63fee872'],
            missile_collision_size=Vector.from_json(data['missile_collision_size']),
            unknown_0x1ba35af4=data['unknown_0x1ba35af4'],
            unknown_struct37=UnknownStruct37.from_json(data['unknown_struct37']),
            melee_damage=DamageInfo.from_json(data['melee_damage']),
        )

    def to_json(self) -> dict:
        return {
            'mini_gun_projectile': self.mini_gun_projectile.to_json(),
            'beam_info': self.beam_info.to_json(),
            'beam_damage': self.beam_damage.to_json(),
            'beam_constraint_angle': self.beam_constraint_angle,
            'charge_attack_damage': self.charge_attack_damage.to_json(),
            'missile_hover_then_home_projectile': self.missile_hover_then_home_projectile.to_json(),
            'missile_projectile': self.missile_projectile.to_json(),
            'unknown_0x63fee872': self.unknown_0x63fee872,
            'missile_collision_size': self.missile_collision_size.to_json(),
            'unknown_0x1ba35af4': self.unknown_0x1ba35af4,
            'unknown_struct37': self.unknown_struct37.to_json(),
            'melee_damage': self.melee_damage.to_json(),
        }


def _decode_mini_gun_projectile(data: typing.BinaryIO, property_size: int):
    return LaunchProjectileData.from_stream(data, property_size)


def _decode_beam_info(data: typing.BinaryIO, property_size: int):
    return PlasmaBeamInfo.from_stream(data, property_size)


def _decode_beam_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_beam_constraint_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_charge_attack_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_missile_hover_then_home_projectile(data: typing.BinaryIO, property_size: int):
    return HoverThenHomeProjectile.from_stream(data, property_size)


def _decode_missile_projectile(data: typing.BinaryIO, property_size: int):
    return LaunchProjectileData.from_stream(data, property_size)


def _decode_unknown_0x63fee872(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_missile_collision_size(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_unknown_0x1ba35af4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_struct37(data: typing.BinaryIO, property_size: int):
    return UnknownStruct37.from_stream(data, property_size)


def _decode_melee_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x78a03d9: ('mini_gun_projectile', _decode_mini_gun_projectile),
    0x1598012a: ('beam_info', _decode_beam_info),
    0x13e30e4d: ('beam_damage', _decode_beam_damage),
    0x4cacfae3: ('beam_constraint_angle', _decode_beam_constraint_angle),
    0xe79ecfd4: ('charge_attack_damage', _decode_charge_attack_damage),
    0x603bfd21: ('missile_hover_then_home_projectile', _decode_missile_hover_then_home_projectile),
    0x8f4d54f9: ('missile_projectile', _decode_missile_projectile),
    0x63fee872: ('unknown_0x63fee872', _decode_unknown_0x63fee872),
    0xa2f2168c: ('missile_collision_size', _decode_missile_collision_size),
    0x1ba35af4: ('unknown_0x1ba35af4', _decode_unknown_0x1ba35af4),
    0xdae21374: ('unknown_struct37', _decode_unknown_struct37),
    0xc9416034: ('melee_damage', _decode_melee_damage),
}
