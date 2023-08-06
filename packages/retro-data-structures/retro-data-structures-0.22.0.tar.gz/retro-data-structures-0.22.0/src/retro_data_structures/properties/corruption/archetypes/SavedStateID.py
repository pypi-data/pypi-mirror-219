# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class SavedStateID(BaseProperty):
    state_id_1: int = dataclasses.field(default=0)
    state_id_2: int = dataclasses.field(default=0)
    state_id_3: int = dataclasses.field(default=0)
    state_id_4: int = dataclasses.field(default=0)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        state_id_1 = struct.unpack('>l', data.read(4))[0]
        state_id_2 = struct.unpack('>l', data.read(4))[0]
        state_id_3 = struct.unpack('>l', data.read(4))[0]
        state_id_4 = struct.unpack('>l', data.read(4))[0]
        return cls(state_id_1, state_id_2, state_id_3, state_id_4)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(struct.pack('>l', self.state_id_1))
        data.write(struct.pack('>l', self.state_id_2))
        data.write(struct.pack('>l', self.state_id_3))
        data.write(struct.pack('>l', self.state_id_4))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            state_id_1=data['state_id_1'],
            state_id_2=data['state_id_2'],
            state_id_3=data['state_id_3'],
            state_id_4=data['state_id_4'],
        )

    def to_json(self) -> dict:
        return {
            'state_id_1': self.state_id_1,
            'state_id_2': self.state_id_2,
            'state_id_3': self.state_id_3,
            'state_id_4': self.state_id_4,
        }
