# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.prime as enums


@dataclasses.dataclass()
class ShotParam(BaseProperty):
    unnamed: enums.WeaponType = dataclasses.field(default=enums.WeaponType.Power)
    damage: float = dataclasses.field(default=0.0)
    radius_damage: float = dataclasses.field(default=0.0)
    radius: float = dataclasses.field(default=0.0)
    knockback_power: float = dataclasses.field(default=0.0)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        unnamed = enums.WeaponType.from_stream(data)
        damage = struct.unpack('>f', data.read(4))[0]
        radius_damage = struct.unpack('>f', data.read(4))[0]
        radius = struct.unpack('>f', data.read(4))[0]
        knockback_power = struct.unpack('>f', data.read(4))[0]
        return cls(unnamed, damage, radius_damage, radius, knockback_power)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        self.unnamed.to_stream(data)
        data.write(struct.pack('>f', self.damage))
        data.write(struct.pack('>f', self.radius_damage))
        data.write(struct.pack('>f', self.radius))
        data.write(struct.pack('>f', self.knockback_power))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unnamed=enums.WeaponType.from_json(data['unnamed']),
            damage=data['damage'],
            radius_damage=data['radius_damage'],
            radius=data['radius'],
            knockback_power=data['knockback_power'],
        )

    def to_json(self) -> dict:
        return {
            'unnamed': self.unnamed.to_json(),
            'damage': self.damage,
            'radius_damage': self.radius_damage,
            'radius': self.radius,
            'knockback_power': self.knockback_power,
        }

    def dependencies_for(self, asset_manager):
        yield from []
