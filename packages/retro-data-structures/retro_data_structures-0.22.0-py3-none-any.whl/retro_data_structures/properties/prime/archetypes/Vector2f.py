# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class Vector2f(BaseProperty):
    x: float = dataclasses.field(default=0.0)
    y: float = dataclasses.field(default=0.0)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        x = struct.unpack('>f', data.read(4))[0]
        y = struct.unpack('>f', data.read(4))[0]
        return cls(x, y)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(struct.pack('>f', self.x))
        data.write(struct.pack('>f', self.y))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            x=data['x'],
            y=data['y'],
        )

    def to_json(self) -> dict:
        return {
            'x': self.x,
            'y': self.y,
        }

    def dependencies_for(self, asset_manager):
        yield from []
