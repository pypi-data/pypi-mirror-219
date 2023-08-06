# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class Connection(BaseProperty):
    connection_index: int = dataclasses.field(default=0)
    activation_times: list[float] = dataclasses.field(default_factory=list)
    unknown: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        connection_index = struct.unpack('>h', data.read(2))[0]
        activation_times = [struct.unpack('>f', data.read(4))[0] for _ in range(struct.unpack(">L", data.read(4))[0])]
        unknown = struct.unpack('>?', data.read(1))[0]
        return cls(connection_index, activation_times, unknown)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(struct.pack('>h', self.connection_index))
        array = self.activation_times
        data.write(struct.pack(">L", len(array)))
        for item in array:
            data.write(struct.pack('>f', item))
        data.write(struct.pack('>?', self.unknown))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            connection_index=data['connection_index'],
            activation_times=[item for item in data['activation_times']],
            unknown=data['unknown'],
        )

    def to_json(self) -> dict:
        return {
            'connection_index': self.connection_index,
            'activation_times': [item for item in self.activation_times],
            'unknown': self.unknown,
        }

    def dependencies_for(self, asset_manager):
        yield from []
