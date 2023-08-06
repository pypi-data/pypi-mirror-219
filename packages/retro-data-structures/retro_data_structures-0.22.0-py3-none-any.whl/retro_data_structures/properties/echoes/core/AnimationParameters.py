# Generated file
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from .AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class AnimationParameters(BaseProperty):
    ancs: AssetId = default_asset_id
    character_index: int = 0
    initial_anim: int = 0

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(*struct.unpack('>LLL', data.read(12)))

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack('>LLL', self.ancs, self.character_index, self.initial_anim))

    @classmethod
    def from_json(cls, data: dict):
        return cls(data["ancs"], data["character_index"], data["initial_anim"])

    def to_json(self) -> dict:
        return {
            "ancs": self.ancs,
            "character_index": self.character_index,
            "initial_anim": self.initial_anim,
        }

    def dependencies_for(self, asset_manager):
        yield from asset_manager.get_dependencies_for_ancs(self.ancs, self.character_index)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES
