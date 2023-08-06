# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.prime as enums


@dataclasses.dataclass()
class DamageInfo(BaseProperty):
    weapon_type: enums.WeaponType = dataclasses.field(default=enums.WeaponType.Power)
    damage: float = dataclasses.field(default=0.0)
    radius: float = dataclasses.field(default=0.0)
    knockback_power: float = dataclasses.field(default=0.0)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        weapon_type = enums.WeaponType.from_stream(data)
        damage = struct.unpack('>f', data.read(4))[0]
        radius = struct.unpack('>f', data.read(4))[0]
        knockback_power = struct.unpack('>f', data.read(4))[0]
        return cls(weapon_type, damage, radius, knockback_power)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        self.weapon_type.to_stream(data)
        data.write(struct.pack('>f', self.damage))
        data.write(struct.pack('>f', self.radius))
        data.write(struct.pack('>f', self.knockback_power))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            weapon_type=enums.WeaponType.from_json(data['weapon_type']),
            damage=data['damage'],
            radius=data['radius'],
            knockback_power=data['knockback_power'],
        )

    def to_json(self) -> dict:
        return {
            'weapon_type': self.weapon_type.to_json(),
            'damage': self.damage,
            'radius': self.radius,
            'knockback_power': self.knockback_power,
        }

    def dependencies_for(self, asset_manager):
        yield from []
