# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class BoolVec3f(BaseProperty):
    unknown_1: bool = dataclasses.field(default=False)
    unknown_2: Vector = dataclasses.field(default_factory=Vector)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        unknown_1 = struct.unpack('>?', data.read(1))[0]
        unknown_2 = Vector.from_stream(data)
        return cls(unknown_1, unknown_2)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(struct.pack('>?', self.unknown_1))
        self.unknown_2.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_1=data['unknown_1'],
            unknown_2=Vector.from_json(data['unknown_2']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_1': self.unknown_1,
            'unknown_2': self.unknown_2.to_json(),
        }

    def dependencies_for(self, asset_manager):
        yield from []
