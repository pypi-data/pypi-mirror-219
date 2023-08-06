# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.prime.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.prime.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.prime.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.prime.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class ElitePirate(BaseObjectType):
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    rotation: Vector = dataclasses.field(default_factory=Vector)
    scale: Vector = dataclasses.field(default_factory=Vector)
    unnamed: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    actor_parameters_1: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    unknown_1: float = dataclasses.field(default=0.0)
    unknown_2: float = dataclasses.field(default=0.0)
    unknown_3: float = dataclasses.field(default=0.0)
    unknown_4: float = dataclasses.field(default=0.0)
    unknown_5: float = dataclasses.field(default=0.0)
    unknown_6: float = dataclasses.field(default=0.0)
    unknown_7: float = dataclasses.field(default=0.0)
    unknown_8: float = dataclasses.field(default=0.0)
    particle_1: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    sound_id_1: int = dataclasses.field(default=0, metadata={'sound': True})
    actor_parameters_2: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    animation_parameters: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    particle_2: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    sound_id_2: int = dataclasses.field(default=0, metadata={'sound': True})
    model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    damage_info_1: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_9: float = dataclasses.field(default=0.0)
    particle_3: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    particle_4: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    particle_5: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    particle_6: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    unknown_10: float = dataclasses.field(default=0.0)
    unknown_11: float = dataclasses.field(default=0.0)
    unknown_12: float = dataclasses.field(default=0.0)
    unknown_13: float = dataclasses.field(default=0.0)
    unknown_14: float = dataclasses.field(default=0.0)
    unknown_15: float = dataclasses.field(default=0.0)
    unknown_16: int = dataclasses.field(default=0)
    sound_id_3: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_id_4: int = dataclasses.field(default=0, metadata={'sound': True})
    particle_7: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    damage_info_2: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    elsc: AssetId = dataclasses.field(metadata={'asset_types': ['ELSC']}, default=default_asset_id)
    sound_id_5: int = dataclasses.field(default=0, metadata={'sound': True})
    unknown_17: bool = dataclasses.field(default=False)
    unknown_18: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x26

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        position = Vector.from_stream(data)
        rotation = Vector.from_stream(data)
        scale = Vector.from_stream(data)
        unnamed = PatternedAITypedef.from_stream(data, property_size)
        actor_parameters_1 = ActorParameters.from_stream(data, property_size)
        unknown_1 = struct.unpack('>f', data.read(4))[0]
        unknown_2 = struct.unpack('>f', data.read(4))[0]
        unknown_3 = struct.unpack('>f', data.read(4))[0]
        unknown_4 = struct.unpack('>f', data.read(4))[0]
        unknown_5 = struct.unpack('>f', data.read(4))[0]
        unknown_6 = struct.unpack('>f', data.read(4))[0]
        unknown_7 = struct.unpack('>f', data.read(4))[0]
        unknown_8 = struct.unpack('>f', data.read(4))[0]
        particle_1 = struct.unpack(">L", data.read(4))[0]
        sound_id_1 = struct.unpack('>l', data.read(4))[0]
        actor_parameters_2 = ActorParameters.from_stream(data, property_size)
        animation_parameters = AnimationParameters.from_stream(data, property_size)
        particle_2 = struct.unpack(">L", data.read(4))[0]
        sound_id_2 = struct.unpack('>l', data.read(4))[0]
        model = struct.unpack(">L", data.read(4))[0]
        damage_info_1 = DamageInfo.from_stream(data, property_size)
        unknown_9 = struct.unpack('>f', data.read(4))[0]
        particle_3 = struct.unpack(">L", data.read(4))[0]
        particle_4 = struct.unpack(">L", data.read(4))[0]
        particle_5 = struct.unpack(">L", data.read(4))[0]
        particle_6 = struct.unpack(">L", data.read(4))[0]
        unknown_10 = struct.unpack('>f', data.read(4))[0]
        unknown_11 = struct.unpack('>f', data.read(4))[0]
        unknown_12 = struct.unpack('>f', data.read(4))[0]
        unknown_13 = struct.unpack('>f', data.read(4))[0]
        unknown_14 = struct.unpack('>f', data.read(4))[0]
        unknown_15 = struct.unpack('>f', data.read(4))[0]
        unknown_16 = struct.unpack('>l', data.read(4))[0]
        sound_id_3 = struct.unpack('>l', data.read(4))[0]
        sound_id_4 = struct.unpack('>l', data.read(4))[0]
        particle_7 = struct.unpack(">L", data.read(4))[0]
        damage_info_2 = DamageInfo.from_stream(data, property_size)
        elsc = struct.unpack(">L", data.read(4))[0]
        sound_id_5 = struct.unpack('>l', data.read(4))[0]
        unknown_17 = struct.unpack('>?', data.read(1))[0]
        unknown_18 = struct.unpack('>?', data.read(1))[0]
        return cls(name, position, rotation, scale, unnamed, actor_parameters_1, unknown_1, unknown_2, unknown_3, unknown_4, unknown_5, unknown_6, unknown_7, unknown_8, particle_1, sound_id_1, actor_parameters_2, animation_parameters, particle_2, sound_id_2, model, damage_info_1, unknown_9, particle_3, particle_4, particle_5, particle_6, unknown_10, unknown_11, unknown_12, unknown_13, unknown_14, unknown_15, unknown_16, sound_id_3, sound_id_4, particle_7, damage_info_2, elsc, sound_id_5, unknown_17, unknown_18)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00*')  # 42 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        self.rotation.to_stream(data)
        self.scale.to_stream(data)
        self.unnamed.to_stream(data)
        self.actor_parameters_1.to_stream(data)
        data.write(struct.pack('>f', self.unknown_1))
        data.write(struct.pack('>f', self.unknown_2))
        data.write(struct.pack('>f', self.unknown_3))
        data.write(struct.pack('>f', self.unknown_4))
        data.write(struct.pack('>f', self.unknown_5))
        data.write(struct.pack('>f', self.unknown_6))
        data.write(struct.pack('>f', self.unknown_7))
        data.write(struct.pack('>f', self.unknown_8))
        data.write(struct.pack(">L", self.particle_1))
        data.write(struct.pack('>l', self.sound_id_1))
        self.actor_parameters_2.to_stream(data)
        self.animation_parameters.to_stream(data)
        data.write(struct.pack(">L", self.particle_2))
        data.write(struct.pack('>l', self.sound_id_2))
        data.write(struct.pack(">L", self.model))
        self.damage_info_1.to_stream(data)
        data.write(struct.pack('>f', self.unknown_9))
        data.write(struct.pack(">L", self.particle_3))
        data.write(struct.pack(">L", self.particle_4))
        data.write(struct.pack(">L", self.particle_5))
        data.write(struct.pack(">L", self.particle_6))
        data.write(struct.pack('>f', self.unknown_10))
        data.write(struct.pack('>f', self.unknown_11))
        data.write(struct.pack('>f', self.unknown_12))
        data.write(struct.pack('>f', self.unknown_13))
        data.write(struct.pack('>f', self.unknown_14))
        data.write(struct.pack('>f', self.unknown_15))
        data.write(struct.pack('>l', self.unknown_16))
        data.write(struct.pack('>l', self.sound_id_3))
        data.write(struct.pack('>l', self.sound_id_4))
        data.write(struct.pack(">L", self.particle_7))
        self.damage_info_2.to_stream(data)
        data.write(struct.pack(">L", self.elsc))
        data.write(struct.pack('>l', self.sound_id_5))
        data.write(struct.pack('>?', self.unknown_17))
        data.write(struct.pack('>?', self.unknown_18))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            position=Vector.from_json(data['position']),
            rotation=Vector.from_json(data['rotation']),
            scale=Vector.from_json(data['scale']),
            unnamed=PatternedAITypedef.from_json(data['unnamed']),
            actor_parameters_1=ActorParameters.from_json(data['actor_parameters_1']),
            unknown_1=data['unknown_1'],
            unknown_2=data['unknown_2'],
            unknown_3=data['unknown_3'],
            unknown_4=data['unknown_4'],
            unknown_5=data['unknown_5'],
            unknown_6=data['unknown_6'],
            unknown_7=data['unknown_7'],
            unknown_8=data['unknown_8'],
            particle_1=data['particle_1'],
            sound_id_1=data['sound_id_1'],
            actor_parameters_2=ActorParameters.from_json(data['actor_parameters_2']),
            animation_parameters=AnimationParameters.from_json(data['animation_parameters']),
            particle_2=data['particle_2'],
            sound_id_2=data['sound_id_2'],
            model=data['model'],
            damage_info_1=DamageInfo.from_json(data['damage_info_1']),
            unknown_9=data['unknown_9'],
            particle_3=data['particle_3'],
            particle_4=data['particle_4'],
            particle_5=data['particle_5'],
            particle_6=data['particle_6'],
            unknown_10=data['unknown_10'],
            unknown_11=data['unknown_11'],
            unknown_12=data['unknown_12'],
            unknown_13=data['unknown_13'],
            unknown_14=data['unknown_14'],
            unknown_15=data['unknown_15'],
            unknown_16=data['unknown_16'],
            sound_id_3=data['sound_id_3'],
            sound_id_4=data['sound_id_4'],
            particle_7=data['particle_7'],
            damage_info_2=DamageInfo.from_json(data['damage_info_2']),
            elsc=data['elsc'],
            sound_id_5=data['sound_id_5'],
            unknown_17=data['unknown_17'],
            unknown_18=data['unknown_18'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'position': self.position.to_json(),
            'rotation': self.rotation.to_json(),
            'scale': self.scale.to_json(),
            'unnamed': self.unnamed.to_json(),
            'actor_parameters_1': self.actor_parameters_1.to_json(),
            'unknown_1': self.unknown_1,
            'unknown_2': self.unknown_2,
            'unknown_3': self.unknown_3,
            'unknown_4': self.unknown_4,
            'unknown_5': self.unknown_5,
            'unknown_6': self.unknown_6,
            'unknown_7': self.unknown_7,
            'unknown_8': self.unknown_8,
            'particle_1': self.particle_1,
            'sound_id_1': self.sound_id_1,
            'actor_parameters_2': self.actor_parameters_2.to_json(),
            'animation_parameters': self.animation_parameters.to_json(),
            'particle_2': self.particle_2,
            'sound_id_2': self.sound_id_2,
            'model': self.model,
            'damage_info_1': self.damage_info_1.to_json(),
            'unknown_9': self.unknown_9,
            'particle_3': self.particle_3,
            'particle_4': self.particle_4,
            'particle_5': self.particle_5,
            'particle_6': self.particle_6,
            'unknown_10': self.unknown_10,
            'unknown_11': self.unknown_11,
            'unknown_12': self.unknown_12,
            'unknown_13': self.unknown_13,
            'unknown_14': self.unknown_14,
            'unknown_15': self.unknown_15,
            'unknown_16': self.unknown_16,
            'sound_id_3': self.sound_id_3,
            'sound_id_4': self.sound_id_4,
            'particle_7': self.particle_7,
            'damage_info_2': self.damage_info_2.to_json(),
            'elsc': self.elsc,
            'sound_id_5': self.sound_id_5,
            'unknown_17': self.unknown_17,
            'unknown_18': self.unknown_18,
        }

    def _dependencies_for_unnamed(self, asset_manager):
        yield from self.unnamed.dependencies_for(asset_manager)

    def _dependencies_for_actor_parameters_1(self, asset_manager):
        yield from self.actor_parameters_1.dependencies_for(asset_manager)

    def _dependencies_for_particle_1(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle_1)

    def _dependencies_for_sound_id_1(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_id_1)

    def _dependencies_for_actor_parameters_2(self, asset_manager):
        yield from self.actor_parameters_2.dependencies_for(asset_manager)

    def _dependencies_for_animation_parameters(self, asset_manager):
        yield from self.animation_parameters.dependencies_for(asset_manager)

    def _dependencies_for_particle_2(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle_2)

    def _dependencies_for_sound_id_2(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_id_2)

    def _dependencies_for_model(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.model)

    def _dependencies_for_damage_info_1(self, asset_manager):
        yield from self.damage_info_1.dependencies_for(asset_manager)

    def _dependencies_for_particle_3(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle_3)

    def _dependencies_for_particle_4(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle_4)

    def _dependencies_for_particle_5(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle_5)

    def _dependencies_for_particle_6(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle_6)

    def _dependencies_for_sound_id_3(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_id_3)

    def _dependencies_for_sound_id_4(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_id_4)

    def _dependencies_for_particle_7(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle_7)

    def _dependencies_for_damage_info_2(self, asset_manager):
        yield from self.damage_info_2.dependencies_for(asset_manager)

    def _dependencies_for_elsc(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.elsc)

    def _dependencies_for_sound_id_5(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_id_5)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_unnamed, "unnamed", "PatternedAITypedef"),
            (self._dependencies_for_actor_parameters_1, "actor_parameters_1", "ActorParameters"),
            (self._dependencies_for_particle_1, "particle_1", "AssetId"),
            (self._dependencies_for_sound_id_1, "sound_id_1", "int"),
            (self._dependencies_for_actor_parameters_2, "actor_parameters_2", "ActorParameters"),
            (self._dependencies_for_animation_parameters, "animation_parameters", "AnimationParameters"),
            (self._dependencies_for_particle_2, "particle_2", "AssetId"),
            (self._dependencies_for_sound_id_2, "sound_id_2", "int"),
            (self._dependencies_for_model, "model", "AssetId"),
            (self._dependencies_for_damage_info_1, "damage_info_1", "DamageInfo"),
            (self._dependencies_for_particle_3, "particle_3", "AssetId"),
            (self._dependencies_for_particle_4, "particle_4", "AssetId"),
            (self._dependencies_for_particle_5, "particle_5", "AssetId"),
            (self._dependencies_for_particle_6, "particle_6", "AssetId"),
            (self._dependencies_for_sound_id_3, "sound_id_3", "int"),
            (self._dependencies_for_sound_id_4, "sound_id_4", "int"),
            (self._dependencies_for_particle_7, "particle_7", "AssetId"),
            (self._dependencies_for_damage_info_2, "damage_info_2", "DamageInfo"),
            (self._dependencies_for_elsc, "elsc", "AssetId"),
            (self._dependencies_for_sound_id_5, "sound_id_5", "int"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for ElitePirate.{field_name} ({field_type}): {e}"
                )
