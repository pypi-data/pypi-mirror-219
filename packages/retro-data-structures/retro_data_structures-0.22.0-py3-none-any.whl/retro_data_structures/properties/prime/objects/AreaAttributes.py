# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.prime as enums
from retro_data_structures.base_resource import Dependency
from retro_data_structures.properties.prime.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class AreaAttributes(BaseObjectType):
    unknown: int = dataclasses.field(default=0)
    show_skybox: bool = dataclasses.field(default=False)
    environmental_effect: enums.EnvironmentalEffect = dataclasses.field(default=enums.EnvironmentalEffect._None)
    initial_environmental_effect_density: float = dataclasses.field(default=0.0)
    initial_thermal_heat_level: float = dataclasses.field(default=0.0)
    x_ray_fog_distance: float = dataclasses.field(default=0.0)
    initial_world_lighting_level: float = dataclasses.field(default=0.0)
    skybox_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL'], 'ignore_dependencies_mlvl': True}, default=default_asset_id)
    phazon_type: enums.PhazonType = dataclasses.field(default=enums.PhazonType._None)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return None

    def set_name(self, name: str) -> None:
        raise RuntimeError(f"{self.__class__.__name__} does not have name")

    @classmethod
    def object_type(cls) -> int:
        return 0x4E

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        unknown = struct.unpack('>l', data.read(4))[0]
        show_skybox = struct.unpack('>?', data.read(1))[0]
        environmental_effect = enums.EnvironmentalEffect.from_stream(data)
        initial_environmental_effect_density = struct.unpack('>f', data.read(4))[0]
        initial_thermal_heat_level = struct.unpack('>f', data.read(4))[0]
        x_ray_fog_distance = struct.unpack('>f', data.read(4))[0]
        initial_world_lighting_level = struct.unpack('>f', data.read(4))[0]
        skybox_model = struct.unpack(">L", data.read(4))[0]
        phazon_type = enums.PhazonType.from_stream(data)
        return cls(unknown, show_skybox, environmental_effect, initial_environmental_effect_density, initial_thermal_heat_level, x_ray_fog_distance, initial_world_lighting_level, skybox_model, phazon_type)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\t')  # 9 properties
        data.write(struct.pack('>l', self.unknown))
        data.write(struct.pack('>?', self.show_skybox))
        self.environmental_effect.to_stream(data)
        data.write(struct.pack('>f', self.initial_environmental_effect_density))
        data.write(struct.pack('>f', self.initial_thermal_heat_level))
        data.write(struct.pack('>f', self.x_ray_fog_distance))
        data.write(struct.pack('>f', self.initial_world_lighting_level))
        data.write(struct.pack(">L", self.skybox_model))
        self.phazon_type.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown=data['unknown'],
            show_skybox=data['show_skybox'],
            environmental_effect=enums.EnvironmentalEffect.from_json(data['environmental_effect']),
            initial_environmental_effect_density=data['initial_environmental_effect_density'],
            initial_thermal_heat_level=data['initial_thermal_heat_level'],
            x_ray_fog_distance=data['x_ray_fog_distance'],
            initial_world_lighting_level=data['initial_world_lighting_level'],
            skybox_model=data['skybox_model'],
            phazon_type=enums.PhazonType.from_json(data['phazon_type']),
        )

    def to_json(self) -> dict:
        return {
            'unknown': self.unknown,
            'show_skybox': self.show_skybox,
            'environmental_effect': self.environmental_effect.to_json(),
            'initial_environmental_effect_density': self.initial_environmental_effect_density,
            'initial_thermal_heat_level': self.initial_thermal_heat_level,
            'x_ray_fog_distance': self.x_ray_fog_distance,
            'initial_world_lighting_level': self.initial_world_lighting_level,
            'skybox_model': self.skybox_model,
            'phazon_type': self.phazon_type.to_json(),
        }

    def _dependencies_for_skybox_model(self, asset_manager):
        for it in asset_manager.get_dependencies_for_asset(self.skybox_model):
            yield Dependency(it.type, it.id, True)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_skybox_model, "skybox_model", "AssetId"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for AreaAttributes.{field_name} ({field_type}): {e}"
                )
