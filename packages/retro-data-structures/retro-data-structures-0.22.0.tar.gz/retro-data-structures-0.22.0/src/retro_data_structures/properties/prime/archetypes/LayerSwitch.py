# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.prime.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class LayerSwitch(BaseProperty):
    room_id: AssetId = dataclasses.field(metadata={'asset_types': ['MREA']}, default=default_asset_id)
    layer_no: int = dataclasses.field(default=0)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        room_id = struct.unpack(">L", data.read(4))[0]
        layer_no = struct.unpack('>l', data.read(4))[0]
        return cls(room_id, layer_no)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(struct.pack(">L", self.room_id))
        data.write(struct.pack('>l', self.layer_no))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            room_id=data['room_id'],
            layer_no=data['layer_no'],
        )

    def to_json(self) -> dict:
        return {
            'room_id': self.room_id,
            'layer_no': self.layer_no,
        }

    def dependencies_for(self, asset_manager):
        yield from []
