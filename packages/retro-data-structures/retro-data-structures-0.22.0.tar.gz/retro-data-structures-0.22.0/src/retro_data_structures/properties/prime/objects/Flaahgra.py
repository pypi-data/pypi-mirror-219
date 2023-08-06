# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.prime.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.prime.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.prime.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.prime.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.prime.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class Flaahgra(BaseObjectType):
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    rotation: Vector = dataclasses.field(default_factory=Vector)
    scale: Vector = dataclasses.field(default_factory=Vector)
    unnamed_0x00000004: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    actor_parameters_1: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    unknown_1: float = dataclasses.field(default=0.0)
    unknown_2: float = dataclasses.field(default=0.0)
    unknown_3: float = dataclasses.field(default=0.0)
    unknown_4: float = dataclasses.field(default=0.0)
    unnamed_0x0000000a: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    wpsc_1: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    damage_info_1: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    wpsc_2: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    damage_info_2: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    particle: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    damage_info_3: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    actor_parameters_2: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    unknown_5: float = dataclasses.field(default=0.0)
    unknown_6: float = dataclasses.field(default=0.0)
    unknown_7: float = dataclasses.field(default=0.0)
    animation_parameters: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    dgrp: AssetId = dataclasses.field(metadata={'asset_types': ['DGRP']}, default=default_asset_id)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x4D

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        position = Vector.from_stream(data)
        rotation = Vector.from_stream(data)
        scale = Vector.from_stream(data)
        unnamed_0x00000004 = PatternedAITypedef.from_stream(data, property_size)
        actor_parameters_1 = ActorParameters.from_stream(data, property_size)
        unknown_1 = struct.unpack('>f', data.read(4))[0]
        unknown_2 = struct.unpack('>f', data.read(4))[0]
        unknown_3 = struct.unpack('>f', data.read(4))[0]
        unknown_4 = struct.unpack('>f', data.read(4))[0]
        unnamed_0x0000000a = DamageVulnerability.from_stream(data, property_size)
        wpsc_1 = struct.unpack(">L", data.read(4))[0]
        damage_info_1 = DamageInfo.from_stream(data, property_size)
        wpsc_2 = struct.unpack(">L", data.read(4))[0]
        damage_info_2 = DamageInfo.from_stream(data, property_size)
        particle = struct.unpack(">L", data.read(4))[0]
        damage_info_3 = DamageInfo.from_stream(data, property_size)
        actor_parameters_2 = ActorParameters.from_stream(data, property_size)
        unknown_5 = struct.unpack('>f', data.read(4))[0]
        unknown_6 = struct.unpack('>f', data.read(4))[0]
        unknown_7 = struct.unpack('>f', data.read(4))[0]
        animation_parameters = AnimationParameters.from_stream(data, property_size)
        dgrp = struct.unpack(">L", data.read(4))[0]
        return cls(name, position, rotation, scale, unnamed_0x00000004, actor_parameters_1, unknown_1, unknown_2, unknown_3, unknown_4, unnamed_0x0000000a, wpsc_1, damage_info_1, wpsc_2, damage_info_2, particle, damage_info_3, actor_parameters_2, unknown_5, unknown_6, unknown_7, animation_parameters, dgrp)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x17')  # 23 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        self.rotation.to_stream(data)
        self.scale.to_stream(data)
        self.unnamed_0x00000004.to_stream(data)
        self.actor_parameters_1.to_stream(data)
        data.write(struct.pack('>f', self.unknown_1))
        data.write(struct.pack('>f', self.unknown_2))
        data.write(struct.pack('>f', self.unknown_3))
        data.write(struct.pack('>f', self.unknown_4))
        self.unnamed_0x0000000a.to_stream(data)
        data.write(struct.pack(">L", self.wpsc_1))
        self.damage_info_1.to_stream(data)
        data.write(struct.pack(">L", self.wpsc_2))
        self.damage_info_2.to_stream(data)
        data.write(struct.pack(">L", self.particle))
        self.damage_info_3.to_stream(data)
        self.actor_parameters_2.to_stream(data)
        data.write(struct.pack('>f', self.unknown_5))
        data.write(struct.pack('>f', self.unknown_6))
        data.write(struct.pack('>f', self.unknown_7))
        self.animation_parameters.to_stream(data)
        data.write(struct.pack(">L", self.dgrp))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            position=Vector.from_json(data['position']),
            rotation=Vector.from_json(data['rotation']),
            scale=Vector.from_json(data['scale']),
            unnamed_0x00000004=PatternedAITypedef.from_json(data['unnamed_0x00000004']),
            actor_parameters_1=ActorParameters.from_json(data['actor_parameters_1']),
            unknown_1=data['unknown_1'],
            unknown_2=data['unknown_2'],
            unknown_3=data['unknown_3'],
            unknown_4=data['unknown_4'],
            unnamed_0x0000000a=DamageVulnerability.from_json(data['unnamed_0x0000000a']),
            wpsc_1=data['wpsc_1'],
            damage_info_1=DamageInfo.from_json(data['damage_info_1']),
            wpsc_2=data['wpsc_2'],
            damage_info_2=DamageInfo.from_json(data['damage_info_2']),
            particle=data['particle'],
            damage_info_3=DamageInfo.from_json(data['damage_info_3']),
            actor_parameters_2=ActorParameters.from_json(data['actor_parameters_2']),
            unknown_5=data['unknown_5'],
            unknown_6=data['unknown_6'],
            unknown_7=data['unknown_7'],
            animation_parameters=AnimationParameters.from_json(data['animation_parameters']),
            dgrp=data['dgrp'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'position': self.position.to_json(),
            'rotation': self.rotation.to_json(),
            'scale': self.scale.to_json(),
            'unnamed_0x00000004': self.unnamed_0x00000004.to_json(),
            'actor_parameters_1': self.actor_parameters_1.to_json(),
            'unknown_1': self.unknown_1,
            'unknown_2': self.unknown_2,
            'unknown_3': self.unknown_3,
            'unknown_4': self.unknown_4,
            'unnamed_0x0000000a': self.unnamed_0x0000000a.to_json(),
            'wpsc_1': self.wpsc_1,
            'damage_info_1': self.damage_info_1.to_json(),
            'wpsc_2': self.wpsc_2,
            'damage_info_2': self.damage_info_2.to_json(),
            'particle': self.particle,
            'damage_info_3': self.damage_info_3.to_json(),
            'actor_parameters_2': self.actor_parameters_2.to_json(),
            'unknown_5': self.unknown_5,
            'unknown_6': self.unknown_6,
            'unknown_7': self.unknown_7,
            'animation_parameters': self.animation_parameters.to_json(),
            'dgrp': self.dgrp,
        }

    def _dependencies_for_unnamed_0x00000004(self, asset_manager):
        yield from self.unnamed_0x00000004.dependencies_for(asset_manager)

    def _dependencies_for_actor_parameters_1(self, asset_manager):
        yield from self.actor_parameters_1.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x0000000a(self, asset_manager):
        yield from self.unnamed_0x0000000a.dependencies_for(asset_manager)

    def _dependencies_for_wpsc_1(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.wpsc_1)

    def _dependencies_for_damage_info_1(self, asset_manager):
        yield from self.damage_info_1.dependencies_for(asset_manager)

    def _dependencies_for_wpsc_2(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.wpsc_2)

    def _dependencies_for_damage_info_2(self, asset_manager):
        yield from self.damage_info_2.dependencies_for(asset_manager)

    def _dependencies_for_particle(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle)

    def _dependencies_for_damage_info_3(self, asset_manager):
        yield from self.damage_info_3.dependencies_for(asset_manager)

    def _dependencies_for_actor_parameters_2(self, asset_manager):
        yield from self.actor_parameters_2.dependencies_for(asset_manager)

    def _dependencies_for_animation_parameters(self, asset_manager):
        yield from self.animation_parameters.dependencies_for(asset_manager)

    def _dependencies_for_dgrp(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.dgrp)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_unnamed_0x00000004, "unnamed_0x00000004", "PatternedAITypedef"),
            (self._dependencies_for_actor_parameters_1, "actor_parameters_1", "ActorParameters"),
            (self._dependencies_for_unnamed_0x0000000a, "unnamed_0x0000000a", "DamageVulnerability"),
            (self._dependencies_for_wpsc_1, "wpsc_1", "AssetId"),
            (self._dependencies_for_damage_info_1, "damage_info_1", "DamageInfo"),
            (self._dependencies_for_wpsc_2, "wpsc_2", "AssetId"),
            (self._dependencies_for_damage_info_2, "damage_info_2", "DamageInfo"),
            (self._dependencies_for_particle, "particle", "AssetId"),
            (self._dependencies_for_damage_info_3, "damage_info_3", "DamageInfo"),
            (self._dependencies_for_actor_parameters_2, "actor_parameters_2", "ActorParameters"),
            (self._dependencies_for_animation_parameters, "animation_parameters", "AnimationParameters"),
            (self._dependencies_for_dgrp, "dgrp", "AssetId"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for Flaahgra.{field_name} ({field_type}): {e}"
                )
