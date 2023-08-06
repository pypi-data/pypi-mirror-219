# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.prime_remastered.archetypes.Vector3f import Vector3f


@dataclasses.dataclass()
class EntityProperties(BaseProperty):
    unk_bool_1: bool = dataclasses.field(default=False)
    unk_bool_2: bool = dataclasses.field(default=False)
    position: Vector3f = dataclasses.field(default_factory=Vector3f)
    rotation: Vector3f = dataclasses.field(default_factory=Vector3f)
    scale: Vector3f = dataclasses.field(default_factory=Vector3f)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME_REMASTER

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        unk_bool_1 = struct.unpack('<?', data.read(1))[0]
        unk_bool_2 = struct.unpack('<?', data.read(1))[0]
        position = Vector3f.from_stream(data, property_size)
        rotation = Vector3f.from_stream(data, property_size)
        scale = Vector3f.from_stream(data, property_size)
        return cls(unk_bool_1, unk_bool_2, position, rotation, scale)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(struct.pack('<?', self.unk_bool_1))
        data.write(struct.pack('<?', self.unk_bool_2))
        self.position.to_stream(data)
        self.rotation.to_stream(data)
        self.scale.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unk_bool_1=data['unk_bool_1'],
            unk_bool_2=data['unk_bool_2'],
            position=Vector3f.from_json(data['position']),
            rotation=Vector3f.from_json(data['rotation']),
            scale=Vector3f.from_json(data['scale']),
        )

    def to_json(self) -> dict:
        return {
            'unk_bool_1': self.unk_bool_1,
            'unk_bool_2': self.unk_bool_2,
            'position': self.position.to_json(),
            'rotation': self.rotation.to_json(),
            'scale': self.scale.to_json(),
        }
