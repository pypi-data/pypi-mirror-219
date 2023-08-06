# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.prime.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.prime.archetypes.HealthInfo import HealthInfo
from retro_data_structures.properties.prime.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class AmbientAI(BaseObjectType):
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    rotation: Vector = dataclasses.field(default_factory=Vector)
    scale: Vector = dataclasses.field(default_factory=Vector)
    unknown_1: Vector = dataclasses.field(default_factory=Vector)
    scan_offset: Vector = dataclasses.field(default_factory=Vector)
    unknown_2: float = dataclasses.field(default=0.0)
    unnamed_0x00000007: HealthInfo = dataclasses.field(default_factory=HealthInfo)
    unnamed_0x00000008: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    animation_parameters: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    unnamed_0x0000000a: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    unknown_3: float = dataclasses.field(default=0.0)
    unknown_4: float = dataclasses.field(default=0.0)
    unknown_5: int = dataclasses.field(default=0)
    unknown_6: int = dataclasses.field(default=0)
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
        return 0x75

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        position = Vector.from_stream(data)
        rotation = Vector.from_stream(data)
        scale = Vector.from_stream(data)
        unknown_1 = Vector.from_stream(data)
        scan_offset = Vector.from_stream(data)
        unknown_2 = struct.unpack('>f', data.read(4))[0]
        unnamed_0x00000007 = HealthInfo.from_stream(data, property_size)
        unnamed_0x00000008 = DamageVulnerability.from_stream(data, property_size)
        animation_parameters = AnimationParameters.from_stream(data, property_size)
        unnamed_0x0000000a = ActorParameters.from_stream(data, property_size)
        unknown_3 = struct.unpack('>f', data.read(4))[0]
        unknown_4 = struct.unpack('>f', data.read(4))[0]
        unknown_5 = struct.unpack('>l', data.read(4))[0]
        unknown_6 = struct.unpack('>l', data.read(4))[0]
        active = struct.unpack('>?', data.read(1))[0]
        return cls(name, position, rotation, scale, unknown_1, scan_offset, unknown_2, unnamed_0x00000007, unnamed_0x00000008, animation_parameters, unnamed_0x0000000a, unknown_3, unknown_4, unknown_5, unknown_6, active)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x10')  # 16 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        self.rotation.to_stream(data)
        self.scale.to_stream(data)
        self.unknown_1.to_stream(data)
        self.scan_offset.to_stream(data)
        data.write(struct.pack('>f', self.unknown_2))
        self.unnamed_0x00000007.to_stream(data)
        self.unnamed_0x00000008.to_stream(data)
        self.animation_parameters.to_stream(data)
        self.unnamed_0x0000000a.to_stream(data)
        data.write(struct.pack('>f', self.unknown_3))
        data.write(struct.pack('>f', self.unknown_4))
        data.write(struct.pack('>l', self.unknown_5))
        data.write(struct.pack('>l', self.unknown_6))
        data.write(struct.pack('>?', self.active))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            position=Vector.from_json(data['position']),
            rotation=Vector.from_json(data['rotation']),
            scale=Vector.from_json(data['scale']),
            unknown_1=Vector.from_json(data['unknown_1']),
            scan_offset=Vector.from_json(data['scan_offset']),
            unknown_2=data['unknown_2'],
            unnamed_0x00000007=HealthInfo.from_json(data['unnamed_0x00000007']),
            unnamed_0x00000008=DamageVulnerability.from_json(data['unnamed_0x00000008']),
            animation_parameters=AnimationParameters.from_json(data['animation_parameters']),
            unnamed_0x0000000a=ActorParameters.from_json(data['unnamed_0x0000000a']),
            unknown_3=data['unknown_3'],
            unknown_4=data['unknown_4'],
            unknown_5=data['unknown_5'],
            unknown_6=data['unknown_6'],
            active=data['active'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'position': self.position.to_json(),
            'rotation': self.rotation.to_json(),
            'scale': self.scale.to_json(),
            'unknown_1': self.unknown_1.to_json(),
            'scan_offset': self.scan_offset.to_json(),
            'unknown_2': self.unknown_2,
            'unnamed_0x00000007': self.unnamed_0x00000007.to_json(),
            'unnamed_0x00000008': self.unnamed_0x00000008.to_json(),
            'animation_parameters': self.animation_parameters.to_json(),
            'unnamed_0x0000000a': self.unnamed_0x0000000a.to_json(),
            'unknown_3': self.unknown_3,
            'unknown_4': self.unknown_4,
            'unknown_5': self.unknown_5,
            'unknown_6': self.unknown_6,
            'active': self.active,
        }

    def _dependencies_for_unnamed_0x00000007(self, asset_manager):
        yield from self.unnamed_0x00000007.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x00000008(self, asset_manager):
        yield from self.unnamed_0x00000008.dependencies_for(asset_manager)

    def _dependencies_for_animation_parameters(self, asset_manager):
        yield from self.animation_parameters.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x0000000a(self, asset_manager):
        yield from self.unnamed_0x0000000a.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_unnamed_0x00000007, "unnamed_0x00000007", "HealthInfo"),
            (self._dependencies_for_unnamed_0x00000008, "unnamed_0x00000008", "DamageVulnerability"),
            (self._dependencies_for_animation_parameters, "animation_parameters", "AnimationParameters"),
            (self._dependencies_for_unnamed_0x0000000a, "unnamed_0x0000000a", "ActorParameters"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for AmbientAI.{field_name} ({field_type}): {e}"
                )
