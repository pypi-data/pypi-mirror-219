# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.prime as enums
from retro_data_structures.properties.prime.core.Color import Color
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class LightParameters(BaseProperty):
    unknown_1: bool = dataclasses.field(default=False)
    unknown_2: float = dataclasses.field(default=0.0)
    shadow_tessellation: int = dataclasses.field(default=0)
    unknown_3: float = dataclasses.field(default=0.0)
    unknown_4: float = dataclasses.field(default=0.0)
    unknown_5: Color = dataclasses.field(default_factory=Color)
    unknown_6: bool = dataclasses.field(default=False)
    world_lighting_options: enums.WorldLightingOptions = dataclasses.field(default=enums.WorldLightingOptions.Unknown1)
    light_recalculation_options: enums.LightRecalculationOptions = dataclasses.field(default=enums.LightRecalculationOptions.Never)
    unknown_7: Vector = dataclasses.field(default_factory=Vector)
    unknown_8: int = dataclasses.field(default=0)
    unknown_9: int = dataclasses.field(default=0)
    unknown_10: bool = dataclasses.field(default=False)
    light_layer_index: int = dataclasses.field(default=0)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        unknown_1 = struct.unpack('>?', data.read(1))[0]
        unknown_2 = struct.unpack('>f', data.read(4))[0]
        shadow_tessellation = struct.unpack('>l', data.read(4))[0]
        unknown_3 = struct.unpack('>f', data.read(4))[0]
        unknown_4 = struct.unpack('>f', data.read(4))[0]
        unknown_5 = Color.from_stream(data)
        unknown_6 = struct.unpack('>?', data.read(1))[0]
        world_lighting_options = enums.WorldLightingOptions.from_stream(data)
        light_recalculation_options = enums.LightRecalculationOptions.from_stream(data)
        unknown_7 = Vector.from_stream(data)
        unknown_8 = struct.unpack('>l', data.read(4))[0]
        unknown_9 = struct.unpack('>l', data.read(4))[0]
        unknown_10 = struct.unpack('>?', data.read(1))[0]
        light_layer_index = struct.unpack('>l', data.read(4))[0]
        return cls(unknown_1, unknown_2, shadow_tessellation, unknown_3, unknown_4, unknown_5, unknown_6, world_lighting_options, light_recalculation_options, unknown_7, unknown_8, unknown_9, unknown_10, light_layer_index)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(struct.pack('>?', self.unknown_1))
        data.write(struct.pack('>f', self.unknown_2))
        data.write(struct.pack('>l', self.shadow_tessellation))
        data.write(struct.pack('>f', self.unknown_3))
        data.write(struct.pack('>f', self.unknown_4))
        self.unknown_5.to_stream(data)
        data.write(struct.pack('>?', self.unknown_6))
        self.world_lighting_options.to_stream(data)
        self.light_recalculation_options.to_stream(data)
        self.unknown_7.to_stream(data)
        data.write(struct.pack('>l', self.unknown_8))
        data.write(struct.pack('>l', self.unknown_9))
        data.write(struct.pack('>?', self.unknown_10))
        data.write(struct.pack('>l', self.light_layer_index))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_1=data['unknown_1'],
            unknown_2=data['unknown_2'],
            shadow_tessellation=data['shadow_tessellation'],
            unknown_3=data['unknown_3'],
            unknown_4=data['unknown_4'],
            unknown_5=Color.from_json(data['unknown_5']),
            unknown_6=data['unknown_6'],
            world_lighting_options=enums.WorldLightingOptions.from_json(data['world_lighting_options']),
            light_recalculation_options=enums.LightRecalculationOptions.from_json(data['light_recalculation_options']),
            unknown_7=Vector.from_json(data['unknown_7']),
            unknown_8=data['unknown_8'],
            unknown_9=data['unknown_9'],
            unknown_10=data['unknown_10'],
            light_layer_index=data['light_layer_index'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_1': self.unknown_1,
            'unknown_2': self.unknown_2,
            'shadow_tessellation': self.shadow_tessellation,
            'unknown_3': self.unknown_3,
            'unknown_4': self.unknown_4,
            'unknown_5': self.unknown_5.to_json(),
            'unknown_6': self.unknown_6,
            'world_lighting_options': self.world_lighting_options.to_json(),
            'light_recalculation_options': self.light_recalculation_options.to_json(),
            'unknown_7': self.unknown_7.to_json(),
            'unknown_8': self.unknown_8,
            'unknown_9': self.unknown_9,
            'unknown_10': self.unknown_10,
            'light_layer_index': self.light_layer_index,
        }

    def dependencies_for(self, asset_manager):
        yield from []
