# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.prime.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class MagdoliteStruct(BaseProperty):
    unknown_1: int = dataclasses.field(default=0)
    particle: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    unknown_2: int = dataclasses.field(default=0)
    unknown_3: float = dataclasses.field(default=0.0)
    unknown_4: float = dataclasses.field(default=0.0)
    unknown_5: float = dataclasses.field(default=0.0)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        unknown_1 = struct.unpack('>l', data.read(4))[0]
        particle = struct.unpack(">L", data.read(4))[0]
        unknown_2 = struct.unpack('>l', data.read(4))[0]
        unknown_3 = struct.unpack('>f', data.read(4))[0]
        unknown_4 = struct.unpack('>f', data.read(4))[0]
        unknown_5 = struct.unpack('>f', data.read(4))[0]
        return cls(unknown_1, particle, unknown_2, unknown_3, unknown_4, unknown_5)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(struct.pack('>l', self.unknown_1))
        data.write(struct.pack(">L", self.particle))
        data.write(struct.pack('>l', self.unknown_2))
        data.write(struct.pack('>f', self.unknown_3))
        data.write(struct.pack('>f', self.unknown_4))
        data.write(struct.pack('>f', self.unknown_5))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_1=data['unknown_1'],
            particle=data['particle'],
            unknown_2=data['unknown_2'],
            unknown_3=data['unknown_3'],
            unknown_4=data['unknown_4'],
            unknown_5=data['unknown_5'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_1': self.unknown_1,
            'particle': self.particle,
            'unknown_2': self.unknown_2,
            'unknown_3': self.unknown_3,
            'unknown_4': self.unknown_4,
            'unknown_5': self.unknown_5,
        }

    def _dependencies_for_particle(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_particle, "particle", "AssetId"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for MagdoliteStruct.{field_name} ({field_type}): {e}"
                )
