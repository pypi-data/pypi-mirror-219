# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.prime.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.prime.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.prime.archetypes.HealthInfo import HealthInfo
from retro_data_structures.properties.prime.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.prime.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class ActorContraption(BaseObjectType):
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    rotation: Vector = dataclasses.field(default_factory=Vector)
    scale: Vector = dataclasses.field(default_factory=Vector)
    collision_extent: Vector = dataclasses.field(default_factory=Vector)
    collision_scan_offset: Vector = dataclasses.field(default_factory=Vector)
    mass: float = dataclasses.field(default=0.0)
    z_momentum: float = dataclasses.field(default=0.0)
    unnamed_0x00000008: HealthInfo = dataclasses.field(default_factory=HealthInfo)
    unnamed_0x00000009: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    animation_parameters: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    unnamed_0x0000000b: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    flame_particle: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    unnamed_0x0000000d: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    active: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x6E

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        position = Vector.from_stream(data)
        rotation = Vector.from_stream(data)
        scale = Vector.from_stream(data)
        collision_extent = Vector.from_stream(data)
        collision_scan_offset = Vector.from_stream(data)
        mass = struct.unpack('>f', data.read(4))[0]
        z_momentum = struct.unpack('>f', data.read(4))[0]
        unnamed_0x00000008 = HealthInfo.from_stream(data, property_size)
        unnamed_0x00000009 = DamageVulnerability.from_stream(data, property_size)
        animation_parameters = AnimationParameters.from_stream(data, property_size)
        unnamed_0x0000000b = ActorParameters.from_stream(data, property_size)
        flame_particle = struct.unpack(">L", data.read(4))[0]
        unnamed_0x0000000d = DamageInfo.from_stream(data, property_size)
        active = struct.unpack('>?', data.read(1))[0]
        return cls(name, position, rotation, scale, collision_extent, collision_scan_offset, mass, z_momentum, unnamed_0x00000008, unnamed_0x00000009, animation_parameters, unnamed_0x0000000b, flame_particle, unnamed_0x0000000d, active)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x0f')  # 15 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        self.rotation.to_stream(data)
        self.scale.to_stream(data)
        self.collision_extent.to_stream(data)
        self.collision_scan_offset.to_stream(data)
        data.write(struct.pack('>f', self.mass))
        data.write(struct.pack('>f', self.z_momentum))
        self.unnamed_0x00000008.to_stream(data)
        self.unnamed_0x00000009.to_stream(data)
        self.animation_parameters.to_stream(data)
        self.unnamed_0x0000000b.to_stream(data)
        data.write(struct.pack(">L", self.flame_particle))
        self.unnamed_0x0000000d.to_stream(data)
        data.write(struct.pack('>?', self.active))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            position=Vector.from_json(data['position']),
            rotation=Vector.from_json(data['rotation']),
            scale=Vector.from_json(data['scale']),
            collision_extent=Vector.from_json(data['collision_extent']),
            collision_scan_offset=Vector.from_json(data['collision_scan_offset']),
            mass=data['mass'],
            z_momentum=data['z_momentum'],
            unnamed_0x00000008=HealthInfo.from_json(data['unnamed_0x00000008']),
            unnamed_0x00000009=DamageVulnerability.from_json(data['unnamed_0x00000009']),
            animation_parameters=AnimationParameters.from_json(data['animation_parameters']),
            unnamed_0x0000000b=ActorParameters.from_json(data['unnamed_0x0000000b']),
            flame_particle=data['flame_particle'],
            unnamed_0x0000000d=DamageInfo.from_json(data['unnamed_0x0000000d']),
            active=data['active'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'position': self.position.to_json(),
            'rotation': self.rotation.to_json(),
            'scale': self.scale.to_json(),
            'collision_extent': self.collision_extent.to_json(),
            'collision_scan_offset': self.collision_scan_offset.to_json(),
            'mass': self.mass,
            'z_momentum': self.z_momentum,
            'unnamed_0x00000008': self.unnamed_0x00000008.to_json(),
            'unnamed_0x00000009': self.unnamed_0x00000009.to_json(),
            'animation_parameters': self.animation_parameters.to_json(),
            'unnamed_0x0000000b': self.unnamed_0x0000000b.to_json(),
            'flame_particle': self.flame_particle,
            'unnamed_0x0000000d': self.unnamed_0x0000000d.to_json(),
            'active': self.active,
        }

    def _dependencies_for_unnamed_0x00000008(self, asset_manager):
        yield from self.unnamed_0x00000008.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x00000009(self, asset_manager):
        yield from self.unnamed_0x00000009.dependencies_for(asset_manager)

    def _dependencies_for_animation_parameters(self, asset_manager):
        yield from self.animation_parameters.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x0000000b(self, asset_manager):
        yield from self.unnamed_0x0000000b.dependencies_for(asset_manager)

    def _dependencies_for_flame_particle(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.flame_particle)

    def _dependencies_for_unnamed_0x0000000d(self, asset_manager):
        yield from self.unnamed_0x0000000d.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_unnamed_0x00000008, "unnamed_0x00000008", "HealthInfo"),
            (self._dependencies_for_unnamed_0x00000009, "unnamed_0x00000009", "DamageVulnerability"),
            (self._dependencies_for_animation_parameters, "animation_parameters", "AnimationParameters"),
            (self._dependencies_for_unnamed_0x0000000b, "unnamed_0x0000000b", "ActorParameters"),
            (self._dependencies_for_flame_particle, "flame_particle", "AssetId"),
            (self._dependencies_for_unnamed_0x0000000d, "unnamed_0x0000000d", "DamageInfo"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for ActorContraption.{field_name} ({field_type}): {e}"
                )
