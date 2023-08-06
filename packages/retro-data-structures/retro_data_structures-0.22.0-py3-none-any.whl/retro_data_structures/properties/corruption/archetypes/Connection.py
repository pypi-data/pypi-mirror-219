# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.ActivationTime import ActivationTime


@dataclasses.dataclass()
class Connection(BaseProperty):
    connection_index: int = dataclasses.field(default=0)
    activation_times: list[ActivationTime] = dataclasses.field(default_factory=list)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        connection_index = struct.unpack('>h', data.read(2))[0]
        activation_times = [ActivationTime.from_stream(data, property_size) for _ in range(struct.unpack(">L", data.read(4))[0])]
        return cls(connection_index, activation_times)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(struct.pack('>h', self.connection_index))
        array = self.activation_times
        data.write(struct.pack(">L", len(array)))
        for item in array:
            item.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            connection_index=data['connection_index'],
            activation_times=[ActivationTime.from_json(item) for item in data['activation_times']],
        )

    def to_json(self) -> dict:
        return {
            'connection_index': self.connection_index,
            'activation_times': [item.to_json() for item in self.activation_times],
        }
