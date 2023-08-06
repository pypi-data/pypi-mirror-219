# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class HealthInfo(BaseProperty):
    health: float = dataclasses.field(default=0.0)
    knockback_resistance: float = dataclasses.field(default=0.0)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        health = struct.unpack('>f', data.read(4))[0]
        knockback_resistance = struct.unpack('>f', data.read(4))[0]
        return cls(health, knockback_resistance)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(struct.pack('>f', self.health))
        data.write(struct.pack('>f', self.knockback_resistance))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            health=data['health'],
            knockback_resistance=data['knockback_resistance'],
        )

    def to_json(self) -> dict:
        return {
            'health': self.health,
            'knockback_resistance': self.knockback_resistance,
        }

    def dependencies_for(self, asset_manager):
        yield from []
