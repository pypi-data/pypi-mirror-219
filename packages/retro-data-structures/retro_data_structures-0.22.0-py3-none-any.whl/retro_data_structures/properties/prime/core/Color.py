# Generated file
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class Color(BaseProperty):
    r: float = 0.0
    g: float = 0.0
    b: float = 0.0
    a: float = 0.0

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(*struct.unpack('>ffff', data.read(16)))

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack('>ffff', self.r, self.g, self.b, self.a))

    @classmethod
    def from_json(cls, data: dict):
        return cls(data["r"], data["g"], data["b"], data["a"])

    def to_json(self) -> dict:
        return {
            "r": self.r,
            "g": self.g,
            "b": self.b,
            "a": self.a,
        }

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME
