# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.prime as enums
from retro_data_structures.properties.prime.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.prime.archetypes.HealthInfo import HealthInfo
from retro_data_structures.properties.prime.archetypes.VisorParameters import VisorParameters
from retro_data_structures.properties.prime.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class DamageableTrigger(BaseObjectType):
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    scale: Vector = dataclasses.field(default_factory=Vector)
    unnamed_0x00000003: HealthInfo = dataclasses.field(default_factory=HealthInfo)
    unnamed_0x00000004: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    render_side: enums.RenderSide = dataclasses.field(default=enums.RenderSide._None)
    texture_1: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    texture_2: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    texture_3: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    enable_lock_on: bool = dataclasses.field(default=False)
    active: bool = dataclasses.field(default=False)
    unnamed_0x0000000b: VisorParameters = dataclasses.field(default_factory=VisorParameters)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x1A

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        position = Vector.from_stream(data)
        scale = Vector.from_stream(data)
        unnamed_0x00000003 = HealthInfo.from_stream(data, property_size)
        unnamed_0x00000004 = DamageVulnerability.from_stream(data, property_size)
        render_side = enums.RenderSide.from_stream(data)
        texture_1 = struct.unpack(">L", data.read(4))[0]
        texture_2 = struct.unpack(">L", data.read(4))[0]
        texture_3 = struct.unpack(">L", data.read(4))[0]
        enable_lock_on = struct.unpack('>?', data.read(1))[0]
        active = struct.unpack('>?', data.read(1))[0]
        unnamed_0x0000000b = VisorParameters.from_stream(data, property_size)
        return cls(name, position, scale, unnamed_0x00000003, unnamed_0x00000004, render_side, texture_1, texture_2, texture_3, enable_lock_on, active, unnamed_0x0000000b)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x0c')  # 12 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        self.scale.to_stream(data)
        self.unnamed_0x00000003.to_stream(data)
        self.unnamed_0x00000004.to_stream(data)
        self.render_side.to_stream(data)
        data.write(struct.pack(">L", self.texture_1))
        data.write(struct.pack(">L", self.texture_2))
        data.write(struct.pack(">L", self.texture_3))
        data.write(struct.pack('>?', self.enable_lock_on))
        data.write(struct.pack('>?', self.active))
        self.unnamed_0x0000000b.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            position=Vector.from_json(data['position']),
            scale=Vector.from_json(data['scale']),
            unnamed_0x00000003=HealthInfo.from_json(data['unnamed_0x00000003']),
            unnamed_0x00000004=DamageVulnerability.from_json(data['unnamed_0x00000004']),
            render_side=enums.RenderSide.from_json(data['render_side']),
            texture_1=data['texture_1'],
            texture_2=data['texture_2'],
            texture_3=data['texture_3'],
            enable_lock_on=data['enable_lock_on'],
            active=data['active'],
            unnamed_0x0000000b=VisorParameters.from_json(data['unnamed_0x0000000b']),
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'position': self.position.to_json(),
            'scale': self.scale.to_json(),
            'unnamed_0x00000003': self.unnamed_0x00000003.to_json(),
            'unnamed_0x00000004': self.unnamed_0x00000004.to_json(),
            'render_side': self.render_side.to_json(),
            'texture_1': self.texture_1,
            'texture_2': self.texture_2,
            'texture_3': self.texture_3,
            'enable_lock_on': self.enable_lock_on,
            'active': self.active,
            'unnamed_0x0000000b': self.unnamed_0x0000000b.to_json(),
        }

    def _dependencies_for_unnamed_0x00000003(self, asset_manager):
        yield from self.unnamed_0x00000003.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x00000004(self, asset_manager):
        yield from self.unnamed_0x00000004.dependencies_for(asset_manager)

    def _dependencies_for_texture_1(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.texture_1)

    def _dependencies_for_texture_2(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.texture_2)

    def _dependencies_for_texture_3(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.texture_3)

    def _dependencies_for_unnamed_0x0000000b(self, asset_manager):
        yield from self.unnamed_0x0000000b.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_unnamed_0x00000003, "unnamed_0x00000003", "HealthInfo"),
            (self._dependencies_for_unnamed_0x00000004, "unnamed_0x00000004", "DamageVulnerability"),
            (self._dependencies_for_texture_1, "texture_1", "AssetId"),
            (self._dependencies_for_texture_2, "texture_2", "AssetId"),
            (self._dependencies_for_texture_3, "texture_3", "AssetId"),
            (self._dependencies_for_unnamed_0x0000000b, "unnamed_0x0000000b", "VisorParameters"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for DamageableTrigger.{field_name} ({field_type}): {e}"
                )
