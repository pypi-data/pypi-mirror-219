# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.prime.archetypes.FluidLayerMotion import FluidLayerMotion


@dataclasses.dataclass()
class FluidUVMotion(BaseProperty):
    fluid_layer_motion_1: FluidLayerMotion = dataclasses.field(default_factory=FluidLayerMotion)
    fluid_layer_motion_2: FluidLayerMotion = dataclasses.field(default_factory=FluidLayerMotion)
    fluid_layer_motion_3: FluidLayerMotion = dataclasses.field(default_factory=FluidLayerMotion)
    unknown_1: float = dataclasses.field(default=0.0)
    unknown_2: float = dataclasses.field(default=0.0)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        fluid_layer_motion_1 = FluidLayerMotion.from_stream(data, property_size)
        fluid_layer_motion_2 = FluidLayerMotion.from_stream(data, property_size)
        fluid_layer_motion_3 = FluidLayerMotion.from_stream(data, property_size)
        unknown_1 = struct.unpack('>f', data.read(4))[0]
        unknown_2 = struct.unpack('>f', data.read(4))[0]
        return cls(fluid_layer_motion_1, fluid_layer_motion_2, fluid_layer_motion_3, unknown_1, unknown_2)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        self.fluid_layer_motion_1.to_stream(data)
        self.fluid_layer_motion_2.to_stream(data)
        self.fluid_layer_motion_3.to_stream(data)
        data.write(struct.pack('>f', self.unknown_1))
        data.write(struct.pack('>f', self.unknown_2))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            fluid_layer_motion_1=FluidLayerMotion.from_json(data['fluid_layer_motion_1']),
            fluid_layer_motion_2=FluidLayerMotion.from_json(data['fluid_layer_motion_2']),
            fluid_layer_motion_3=FluidLayerMotion.from_json(data['fluid_layer_motion_3']),
            unknown_1=data['unknown_1'],
            unknown_2=data['unknown_2'],
        )

    def to_json(self) -> dict:
        return {
            'fluid_layer_motion_1': self.fluid_layer_motion_1.to_json(),
            'fluid_layer_motion_2': self.fluid_layer_motion_2.to_json(),
            'fluid_layer_motion_3': self.fluid_layer_motion_3.to_json(),
            'unknown_1': self.unknown_1,
            'unknown_2': self.unknown_2,
        }

    def _dependencies_for_fluid_layer_motion_1(self, asset_manager):
        yield from self.fluid_layer_motion_1.dependencies_for(asset_manager)

    def _dependencies_for_fluid_layer_motion_2(self, asset_manager):
        yield from self.fluid_layer_motion_2.dependencies_for(asset_manager)

    def _dependencies_for_fluid_layer_motion_3(self, asset_manager):
        yield from self.fluid_layer_motion_3.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_fluid_layer_motion_1, "fluid_layer_motion_1", "FluidLayerMotion"),
            (self._dependencies_for_fluid_layer_motion_2, "fluid_layer_motion_2", "FluidLayerMotion"),
            (self._dependencies_for_fluid_layer_motion_3, "fluid_layer_motion_3", "FluidLayerMotion"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for FluidUVMotion.{field_name} ({field_type}): {e}"
                )
