# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.prime.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.prime.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.prime.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class Eyeball(BaseObjectType):
    name: str = dataclasses.field(default='')
    unknown_1: int = dataclasses.field(default=0)
    position: Vector = dataclasses.field(default_factory=Vector)
    rotation: Vector = dataclasses.field(default_factory=Vector)
    scale: Vector = dataclasses.field(default_factory=Vector)
    unnamed_0x00000005: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    unnamed_0x00000006: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    unknown_2: float = dataclasses.field(default=0.0)
    unknown_3: float = dataclasses.field(default=0.0)
    wpsc: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    unnamed_0x0000000a: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    particle_1: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    particle_2: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    texture_1: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    texture_2: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    unknown_4: int = dataclasses.field(default=0)
    always_ffffffff_1: int = dataclasses.field(default=0)
    always_ffffffff_2: int = dataclasses.field(default=0)
    always_ffffffff_3: int = dataclasses.field(default=0)
    laser_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    unknown_6: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x67

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        unknown_1 = struct.unpack('>l', data.read(4))[0]
        position = Vector.from_stream(data)
        rotation = Vector.from_stream(data)
        scale = Vector.from_stream(data)
        unnamed_0x00000005 = PatternedAITypedef.from_stream(data, property_size)
        unnamed_0x00000006 = ActorParameters.from_stream(data, property_size)
        unknown_2 = struct.unpack('>f', data.read(4))[0]
        unknown_3 = struct.unpack('>f', data.read(4))[0]
        wpsc = struct.unpack(">L", data.read(4))[0]
        unnamed_0x0000000a = DamageInfo.from_stream(data, property_size)
        particle_1 = struct.unpack(">L", data.read(4))[0]
        particle_2 = struct.unpack(">L", data.read(4))[0]
        texture_1 = struct.unpack(">L", data.read(4))[0]
        texture_2 = struct.unpack(">L", data.read(4))[0]
        unknown_4 = struct.unpack('>l', data.read(4))[0]
        always_ffffffff_1 = struct.unpack('>l', data.read(4))[0]
        always_ffffffff_2 = struct.unpack('>l', data.read(4))[0]
        always_ffffffff_3 = struct.unpack('>l', data.read(4))[0]
        laser_sound = struct.unpack('>l', data.read(4))[0]
        unknown_6 = struct.unpack('>?', data.read(1))[0]
        return cls(name, unknown_1, position, rotation, scale, unnamed_0x00000005, unnamed_0x00000006, unknown_2, unknown_3, wpsc, unnamed_0x0000000a, particle_1, particle_2, texture_1, texture_2, unknown_4, always_ffffffff_1, always_ffffffff_2, always_ffffffff_3, laser_sound, unknown_6)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x15')  # 21 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        data.write(struct.pack('>l', self.unknown_1))
        self.position.to_stream(data)
        self.rotation.to_stream(data)
        self.scale.to_stream(data)
        self.unnamed_0x00000005.to_stream(data)
        self.unnamed_0x00000006.to_stream(data)
        data.write(struct.pack('>f', self.unknown_2))
        data.write(struct.pack('>f', self.unknown_3))
        data.write(struct.pack(">L", self.wpsc))
        self.unnamed_0x0000000a.to_stream(data)
        data.write(struct.pack(">L", self.particle_1))
        data.write(struct.pack(">L", self.particle_2))
        data.write(struct.pack(">L", self.texture_1))
        data.write(struct.pack(">L", self.texture_2))
        data.write(struct.pack('>l', self.unknown_4))
        data.write(struct.pack('>l', self.always_ffffffff_1))
        data.write(struct.pack('>l', self.always_ffffffff_2))
        data.write(struct.pack('>l', self.always_ffffffff_3))
        data.write(struct.pack('>l', self.laser_sound))
        data.write(struct.pack('>?', self.unknown_6))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            unknown_1=data['unknown_1'],
            position=Vector.from_json(data['position']),
            rotation=Vector.from_json(data['rotation']),
            scale=Vector.from_json(data['scale']),
            unnamed_0x00000005=PatternedAITypedef.from_json(data['unnamed_0x00000005']),
            unnamed_0x00000006=ActorParameters.from_json(data['unnamed_0x00000006']),
            unknown_2=data['unknown_2'],
            unknown_3=data['unknown_3'],
            wpsc=data['wpsc'],
            unnamed_0x0000000a=DamageInfo.from_json(data['unnamed_0x0000000a']),
            particle_1=data['particle_1'],
            particle_2=data['particle_2'],
            texture_1=data['texture_1'],
            texture_2=data['texture_2'],
            unknown_4=data['unknown_4'],
            always_ffffffff_1=data['always_ffffffff_1'],
            always_ffffffff_2=data['always_ffffffff_2'],
            always_ffffffff_3=data['always_ffffffff_3'],
            laser_sound=data['laser_sound'],
            unknown_6=data['unknown_6'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'unknown_1': self.unknown_1,
            'position': self.position.to_json(),
            'rotation': self.rotation.to_json(),
            'scale': self.scale.to_json(),
            'unnamed_0x00000005': self.unnamed_0x00000005.to_json(),
            'unnamed_0x00000006': self.unnamed_0x00000006.to_json(),
            'unknown_2': self.unknown_2,
            'unknown_3': self.unknown_3,
            'wpsc': self.wpsc,
            'unnamed_0x0000000a': self.unnamed_0x0000000a.to_json(),
            'particle_1': self.particle_1,
            'particle_2': self.particle_2,
            'texture_1': self.texture_1,
            'texture_2': self.texture_2,
            'unknown_4': self.unknown_4,
            'always_ffffffff_1': self.always_ffffffff_1,
            'always_ffffffff_2': self.always_ffffffff_2,
            'always_ffffffff_3': self.always_ffffffff_3,
            'laser_sound': self.laser_sound,
            'unknown_6': self.unknown_6,
        }

    def _dependencies_for_unnamed_0x00000005(self, asset_manager):
        yield from self.unnamed_0x00000005.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x00000006(self, asset_manager):
        yield from self.unnamed_0x00000006.dependencies_for(asset_manager)

    def _dependencies_for_wpsc(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.wpsc)

    def _dependencies_for_unnamed_0x0000000a(self, asset_manager):
        yield from self.unnamed_0x0000000a.dependencies_for(asset_manager)

    def _dependencies_for_particle_1(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle_1)

    def _dependencies_for_particle_2(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle_2)

    def _dependencies_for_texture_1(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.texture_1)

    def _dependencies_for_texture_2(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.texture_2)

    def _dependencies_for_laser_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.laser_sound)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_unnamed_0x00000005, "unnamed_0x00000005", "PatternedAITypedef"),
            (self._dependencies_for_unnamed_0x00000006, "unnamed_0x00000006", "ActorParameters"),
            (self._dependencies_for_wpsc, "wpsc", "AssetId"),
            (self._dependencies_for_unnamed_0x0000000a, "unnamed_0x0000000a", "DamageInfo"),
            (self._dependencies_for_particle_1, "particle_1", "AssetId"),
            (self._dependencies_for_particle_2, "particle_2", "AssetId"),
            (self._dependencies_for_texture_1, "texture_1", "AssetId"),
            (self._dependencies_for_texture_2, "texture_2", "AssetId"),
            (self._dependencies_for_laser_sound, "laser_sound", "int"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for Eyeball.{field_name} ({field_type}): {e}"
                )
