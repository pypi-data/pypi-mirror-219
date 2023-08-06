# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.prime.archetypes.LightParameters import LightParameters
from retro_data_structures.properties.prime.archetypes.ScannableParameters import ScannableParameters
from retro_data_structures.properties.prime.archetypes.VisorParameters import VisorParameters
from retro_data_structures.properties.prime.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class ActorParameters(BaseProperty):
    unnamed_0x00000000: LightParameters = dataclasses.field(default_factory=LightParameters)
    unnamed_0x00000001: ScannableParameters = dataclasses.field(default_factory=ScannableParameters)
    x_ray_visor_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    x_ray_visor_skin: AssetId = dataclasses.field(metadata={'asset_types': ['CSKR']}, default=default_asset_id)
    thermal_visor_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    thermal_visor_skin: AssetId = dataclasses.field(metadata={'asset_types': ['CSKR']}, default=default_asset_id)
    unknown_1: bool = dataclasses.field(default=False)
    unknown_2: float = dataclasses.field(default=0.0)
    unknown_3: float = dataclasses.field(default=0.0)
    unnamed_0x00000009: VisorParameters = dataclasses.field(default_factory=VisorParameters)
    enable_thermal_heat: bool = dataclasses.field(default=False)
    unknown_4: bool = dataclasses.field(default=False)
    unknown_5: bool = dataclasses.field(default=False)
    unknown_6: float = dataclasses.field(default=0.0)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        unnamed_0x00000000 = LightParameters.from_stream(data, property_size)
        unnamed_0x00000001 = ScannableParameters.from_stream(data, property_size)
        x_ray_visor_model = struct.unpack(">L", data.read(4))[0]
        x_ray_visor_skin = struct.unpack(">L", data.read(4))[0]
        thermal_visor_model = struct.unpack(">L", data.read(4))[0]
        thermal_visor_skin = struct.unpack(">L", data.read(4))[0]
        unknown_1 = struct.unpack('>?', data.read(1))[0]
        unknown_2 = struct.unpack('>f', data.read(4))[0]
        unknown_3 = struct.unpack('>f', data.read(4))[0]
        unnamed_0x00000009 = VisorParameters.from_stream(data, property_size)
        enable_thermal_heat = struct.unpack('>?', data.read(1))[0]
        unknown_4 = struct.unpack('>?', data.read(1))[0]
        unknown_5 = struct.unpack('>?', data.read(1))[0]
        unknown_6 = struct.unpack('>f', data.read(4))[0]
        return cls(unnamed_0x00000000, unnamed_0x00000001, x_ray_visor_model, x_ray_visor_skin, thermal_visor_model, thermal_visor_skin, unknown_1, unknown_2, unknown_3, unnamed_0x00000009, enable_thermal_heat, unknown_4, unknown_5, unknown_6)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        self.unnamed_0x00000000.to_stream(data)
        self.unnamed_0x00000001.to_stream(data)
        data.write(struct.pack(">L", self.x_ray_visor_model))
        data.write(struct.pack(">L", self.x_ray_visor_skin))
        data.write(struct.pack(">L", self.thermal_visor_model))
        data.write(struct.pack(">L", self.thermal_visor_skin))
        data.write(struct.pack('>?', self.unknown_1))
        data.write(struct.pack('>f', self.unknown_2))
        data.write(struct.pack('>f', self.unknown_3))
        self.unnamed_0x00000009.to_stream(data)
        data.write(struct.pack('>?', self.enable_thermal_heat))
        data.write(struct.pack('>?', self.unknown_4))
        data.write(struct.pack('>?', self.unknown_5))
        data.write(struct.pack('>f', self.unknown_6))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unnamed_0x00000000=LightParameters.from_json(data['unnamed_0x00000000']),
            unnamed_0x00000001=ScannableParameters.from_json(data['unnamed_0x00000001']),
            x_ray_visor_model=data['x_ray_visor_model'],
            x_ray_visor_skin=data['x_ray_visor_skin'],
            thermal_visor_model=data['thermal_visor_model'],
            thermal_visor_skin=data['thermal_visor_skin'],
            unknown_1=data['unknown_1'],
            unknown_2=data['unknown_2'],
            unknown_3=data['unknown_3'],
            unnamed_0x00000009=VisorParameters.from_json(data['unnamed_0x00000009']),
            enable_thermal_heat=data['enable_thermal_heat'],
            unknown_4=data['unknown_4'],
            unknown_5=data['unknown_5'],
            unknown_6=data['unknown_6'],
        )

    def to_json(self) -> dict:
        return {
            'unnamed_0x00000000': self.unnamed_0x00000000.to_json(),
            'unnamed_0x00000001': self.unnamed_0x00000001.to_json(),
            'x_ray_visor_model': self.x_ray_visor_model,
            'x_ray_visor_skin': self.x_ray_visor_skin,
            'thermal_visor_model': self.thermal_visor_model,
            'thermal_visor_skin': self.thermal_visor_skin,
            'unknown_1': self.unknown_1,
            'unknown_2': self.unknown_2,
            'unknown_3': self.unknown_3,
            'unnamed_0x00000009': self.unnamed_0x00000009.to_json(),
            'enable_thermal_heat': self.enable_thermal_heat,
            'unknown_4': self.unknown_4,
            'unknown_5': self.unknown_5,
            'unknown_6': self.unknown_6,
        }

    def _dependencies_for_unnamed_0x00000000(self, asset_manager):
        yield from self.unnamed_0x00000000.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x00000001(self, asset_manager):
        yield from self.unnamed_0x00000001.dependencies_for(asset_manager)

    def _dependencies_for_x_ray_visor_model(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.x_ray_visor_model)

    def _dependencies_for_x_ray_visor_skin(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.x_ray_visor_skin)

    def _dependencies_for_thermal_visor_model(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.thermal_visor_model)

    def _dependencies_for_thermal_visor_skin(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.thermal_visor_skin)

    def _dependencies_for_unnamed_0x00000009(self, asset_manager):
        yield from self.unnamed_0x00000009.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_unnamed_0x00000000, "unnamed_0x00000000", "LightParameters"),
            (self._dependencies_for_unnamed_0x00000001, "unnamed_0x00000001", "ScannableParameters"),
            (self._dependencies_for_x_ray_visor_model, "x_ray_visor_model", "AssetId"),
            (self._dependencies_for_x_ray_visor_skin, "x_ray_visor_skin", "AssetId"),
            (self._dependencies_for_thermal_visor_model, "thermal_visor_model", "AssetId"),
            (self._dependencies_for_thermal_visor_skin, "thermal_visor_skin", "AssetId"),
            (self._dependencies_for_unnamed_0x00000009, "unnamed_0x00000009", "VisorParameters"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for ActorParameters.{field_name} ({field_type}): {e}"
                )
