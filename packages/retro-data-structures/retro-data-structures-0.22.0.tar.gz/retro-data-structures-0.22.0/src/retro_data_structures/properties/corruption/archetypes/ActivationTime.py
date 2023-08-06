# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class ActivationTime(BaseProperty):
    time: float = dataclasses.field(default=0.0)
    unknown_1: int = dataclasses.field(default=0)
    unknown_2: int = dataclasses.field(default=0)
    unknown_3: int = dataclasses.field(default=0)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        time = struct.unpack('>f', data.read(4))[0]
        unknown_1 = struct.unpack('>l', data.read(4))[0]
        unknown_2 = struct.unpack('>l', data.read(4))[0]
        unknown_3 = struct.unpack('>l', data.read(4))[0]
        return cls(time, unknown_1, unknown_2, unknown_3)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(struct.pack('>f', self.time))
        data.write(struct.pack('>l', self.unknown_1))
        data.write(struct.pack('>l', self.unknown_2))
        data.write(struct.pack('>l', self.unknown_3))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            time=data['time'],
            unknown_1=data['unknown_1'],
            unknown_2=data['unknown_2'],
            unknown_3=data['unknown_3'],
        )

    def to_json(self) -> dict:
        return {
            'time': self.time,
            'unknown_1': self.unknown_1,
            'unknown_2': self.unknown_2,
            'unknown_3': self.unknown_3,
        }
