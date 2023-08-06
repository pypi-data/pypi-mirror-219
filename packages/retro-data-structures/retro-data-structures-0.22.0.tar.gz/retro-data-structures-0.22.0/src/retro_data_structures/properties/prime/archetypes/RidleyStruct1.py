# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.prime.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.prime.core.Color import Color


@dataclasses.dataclass()
class RidleyStruct1(BaseProperty):
    unknown_1: int = dataclasses.field(default=0)
    unknown_2: int = dataclasses.field(default=0)
    particle_1: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    particle_2: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    texture_1: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    texture_2: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    unknown_3: float = dataclasses.field(default=0.0)
    unknown_4: float = dataclasses.field(default=0.0)
    unknown_5: float = dataclasses.field(default=0.0)
    unknown_6: float = dataclasses.field(default=0.0)
    unknown_7: float = dataclasses.field(default=0.0)
    unknown_8: float = dataclasses.field(default=0.0)
    unknown_9: float = dataclasses.field(default=0.0)
    unknown_10: float = dataclasses.field(default=0.0)
    unknown_11: float = dataclasses.field(default=0.0)
    unknown_12: Color = dataclasses.field(default_factory=Color)
    unknown_13: Color = dataclasses.field(default_factory=Color)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        unknown_1 = struct.unpack('>l', data.read(4))[0]
        unknown_2 = struct.unpack('>l', data.read(4))[0]
        particle_1 = struct.unpack(">L", data.read(4))[0]
        particle_2 = struct.unpack(">L", data.read(4))[0]
        texture_1 = struct.unpack(">L", data.read(4))[0]
        texture_2 = struct.unpack(">L", data.read(4))[0]
        unknown_3 = struct.unpack('>f', data.read(4))[0]
        unknown_4 = struct.unpack('>f', data.read(4))[0]
        unknown_5 = struct.unpack('>f', data.read(4))[0]
        unknown_6 = struct.unpack('>f', data.read(4))[0]
        unknown_7 = struct.unpack('>f', data.read(4))[0]
        unknown_8 = struct.unpack('>f', data.read(4))[0]
        unknown_9 = struct.unpack('>f', data.read(4))[0]
        unknown_10 = struct.unpack('>f', data.read(4))[0]
        unknown_11 = struct.unpack('>f', data.read(4))[0]
        unknown_12 = Color.from_stream(data)
        unknown_13 = Color.from_stream(data)
        return cls(unknown_1, unknown_2, particle_1, particle_2, texture_1, texture_2, unknown_3, unknown_4, unknown_5, unknown_6, unknown_7, unknown_8, unknown_9, unknown_10, unknown_11, unknown_12, unknown_13)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(struct.pack('>l', self.unknown_1))
        data.write(struct.pack('>l', self.unknown_2))
        data.write(struct.pack(">L", self.particle_1))
        data.write(struct.pack(">L", self.particle_2))
        data.write(struct.pack(">L", self.texture_1))
        data.write(struct.pack(">L", self.texture_2))
        data.write(struct.pack('>f', self.unknown_3))
        data.write(struct.pack('>f', self.unknown_4))
        data.write(struct.pack('>f', self.unknown_5))
        data.write(struct.pack('>f', self.unknown_6))
        data.write(struct.pack('>f', self.unknown_7))
        data.write(struct.pack('>f', self.unknown_8))
        data.write(struct.pack('>f', self.unknown_9))
        data.write(struct.pack('>f', self.unknown_10))
        data.write(struct.pack('>f', self.unknown_11))
        self.unknown_12.to_stream(data)
        self.unknown_13.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_1=data['unknown_1'],
            unknown_2=data['unknown_2'],
            particle_1=data['particle_1'],
            particle_2=data['particle_2'],
            texture_1=data['texture_1'],
            texture_2=data['texture_2'],
            unknown_3=data['unknown_3'],
            unknown_4=data['unknown_4'],
            unknown_5=data['unknown_5'],
            unknown_6=data['unknown_6'],
            unknown_7=data['unknown_7'],
            unknown_8=data['unknown_8'],
            unknown_9=data['unknown_9'],
            unknown_10=data['unknown_10'],
            unknown_11=data['unknown_11'],
            unknown_12=Color.from_json(data['unknown_12']),
            unknown_13=Color.from_json(data['unknown_13']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_1': self.unknown_1,
            'unknown_2': self.unknown_2,
            'particle_1': self.particle_1,
            'particle_2': self.particle_2,
            'texture_1': self.texture_1,
            'texture_2': self.texture_2,
            'unknown_3': self.unknown_3,
            'unknown_4': self.unknown_4,
            'unknown_5': self.unknown_5,
            'unknown_6': self.unknown_6,
            'unknown_7': self.unknown_7,
            'unknown_8': self.unknown_8,
            'unknown_9': self.unknown_9,
            'unknown_10': self.unknown_10,
            'unknown_11': self.unknown_11,
            'unknown_12': self.unknown_12.to_json(),
            'unknown_13': self.unknown_13.to_json(),
        }

    def _dependencies_for_particle_1(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle_1)

    def _dependencies_for_particle_2(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle_2)

    def _dependencies_for_texture_1(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.texture_1)

    def _dependencies_for_texture_2(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.texture_2)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_particle_1, "particle_1", "AssetId"),
            (self._dependencies_for_particle_2, "particle_2", "AssetId"),
            (self._dependencies_for_texture_1, "texture_1", "AssetId"),
            (self._dependencies_for_texture_2, "texture_2", "AssetId"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for RidleyStruct1.{field_name} ({field_type}): {e}"
                )
