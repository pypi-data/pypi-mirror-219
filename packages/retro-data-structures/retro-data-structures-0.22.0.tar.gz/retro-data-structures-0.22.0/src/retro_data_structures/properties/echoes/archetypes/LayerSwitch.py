# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class LayerSwitch(BaseProperty):
    area_id: int = dataclasses.field(default=0)
    layer_number: int = dataclasses.field(default=0)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        area_id = struct.unpack('>l', data.read(4))[0]
        layer_number = struct.unpack('>l', data.read(4))[0]
        return cls(area_id, layer_number)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(struct.pack('>l', self.area_id))
        data.write(struct.pack('>l', self.layer_number))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            area_id=data['area_id'],
            layer_number=data['layer_number'],
        )

    def to_json(self) -> dict:
        return {
            'area_id': self.area_id,
            'layer_number': self.layer_number,
        }

    def dependencies_for(self, asset_manager):
        yield from []
