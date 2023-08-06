# Generated file
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class Vector(BaseProperty):
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(*struct.unpack('>fff', data.read(12)))

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack('>fff', self.x, self.y, self.z))

    @classmethod
    def from_json(cls, data: dict):
        return cls(data["x"], data["y"], data["z"])

    def to_json(self) -> dict:
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z,
        }

    def dependencies_for(self, asset_manager):
        yield from []

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME
