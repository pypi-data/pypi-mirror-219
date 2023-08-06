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
class WallCrawlerSwarm(BaseObjectType):
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    rotation: Vector = dataclasses.field(default_factory=Vector)
    scale: Vector = dataclasses.field(default_factory=Vector)
    active: bool = dataclasses.field(default=False)
    unnamed_0x00000005: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    unknown_1: int = dataclasses.field(default=0)
    animation_parameters: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    unknown_2: int = dataclasses.field(default=0)
    unknown_3: int = dataclasses.field(default=0)
    particle_1: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    particle_2: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    always_ffffffff_1: int = dataclasses.field(default=0)
    always_ffffffff_2: int = dataclasses.field(default=0)
    damage_info_1: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_4: float = dataclasses.field(default=0.0)
    damage_info_2: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_5: float = dataclasses.field(default=0.0)
    unknown_6: float = dataclasses.field(default=0.0)
    unknown_7: float = dataclasses.field(default=0.0)
    unknown_8: float = dataclasses.field(default=0.0)
    unknown_9: int = dataclasses.field(default=0)
    unknown_10: int = dataclasses.field(default=0)
    unknown_11: float = dataclasses.field(default=0.0)
    unknown_12: float = dataclasses.field(default=0.0)
    unknown_13: float = dataclasses.field(default=0.0)
    unknown_14: float = dataclasses.field(default=0.0)
    unknown_15: float = dataclasses.field(default=0.0)
    unknown_16: float = dataclasses.field(default=0.0)
    unknown_17: float = dataclasses.field(default=0.0)
    unknown_18: float = dataclasses.field(default=0.0)
    unknown_19: int = dataclasses.field(default=0)
    unknown_20: float = dataclasses.field(default=0.0)
    unknown_21: float = dataclasses.field(default=0.0)
    unknown_22: float = dataclasses.field(default=0.0)
    unnamed_0x00000023: HealthInfo = dataclasses.field(default_factory=HealthInfo)
    unnamed_0x00000024: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    sound_1: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_2: int = dataclasses.field(default=0, metadata={'sound': True})

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x5A

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        position = Vector.from_stream(data)
        rotation = Vector.from_stream(data)
        scale = Vector.from_stream(data)
        active = struct.unpack('>?', data.read(1))[0]
        unnamed_0x00000005 = ActorParameters.from_stream(data, property_size)
        unknown_1 = struct.unpack('>l', data.read(4))[0]
        animation_parameters = AnimationParameters.from_stream(data, property_size)
        unknown_2 = struct.unpack('>l', data.read(4))[0]
        unknown_3 = struct.unpack('>l', data.read(4))[0]
        particle_1 = struct.unpack(">L", data.read(4))[0]
        particle_2 = struct.unpack(">L", data.read(4))[0]
        always_ffffffff_1 = struct.unpack('>l', data.read(4))[0]
        always_ffffffff_2 = struct.unpack('>l', data.read(4))[0]
        damage_info_1 = DamageInfo.from_stream(data, property_size)
        unknown_4 = struct.unpack('>f', data.read(4))[0]
        damage_info_2 = DamageInfo.from_stream(data, property_size)
        unknown_5 = struct.unpack('>f', data.read(4))[0]
        unknown_6 = struct.unpack('>f', data.read(4))[0]
        unknown_7 = struct.unpack('>f', data.read(4))[0]
        unknown_8 = struct.unpack('>f', data.read(4))[0]
        unknown_9 = struct.unpack('>l', data.read(4))[0]
        unknown_10 = struct.unpack('>l', data.read(4))[0]
        unknown_11 = struct.unpack('>f', data.read(4))[0]
        unknown_12 = struct.unpack('>f', data.read(4))[0]
        unknown_13 = struct.unpack('>f', data.read(4))[0]
        unknown_14 = struct.unpack('>f', data.read(4))[0]
        unknown_15 = struct.unpack('>f', data.read(4))[0]
        unknown_16 = struct.unpack('>f', data.read(4))[0]
        unknown_17 = struct.unpack('>f', data.read(4))[0]
        unknown_18 = struct.unpack('>f', data.read(4))[0]
        unknown_19 = struct.unpack('>l', data.read(4))[0]
        unknown_20 = struct.unpack('>f', data.read(4))[0]
        unknown_21 = struct.unpack('>f', data.read(4))[0]
        unknown_22 = struct.unpack('>f', data.read(4))[0]
        unnamed_0x00000023 = HealthInfo.from_stream(data, property_size)
        unnamed_0x00000024 = DamageVulnerability.from_stream(data, property_size)
        sound_1 = struct.unpack('>l', data.read(4))[0]
        sound_2 = struct.unpack('>l', data.read(4))[0]
        return cls(name, position, rotation, scale, active, unnamed_0x00000005, unknown_1, animation_parameters, unknown_2, unknown_3, particle_1, particle_2, always_ffffffff_1, always_ffffffff_2, damage_info_1, unknown_4, damage_info_2, unknown_5, unknown_6, unknown_7, unknown_8, unknown_9, unknown_10, unknown_11, unknown_12, unknown_13, unknown_14, unknown_15, unknown_16, unknown_17, unknown_18, unknown_19, unknown_20, unknown_21, unknown_22, unnamed_0x00000023, unnamed_0x00000024, sound_1, sound_2)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b"\x00\x00\x00'")  # 39 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        self.rotation.to_stream(data)
        self.scale.to_stream(data)
        data.write(struct.pack('>?', self.active))
        self.unnamed_0x00000005.to_stream(data)
        data.write(struct.pack('>l', self.unknown_1))
        self.animation_parameters.to_stream(data)
        data.write(struct.pack('>l', self.unknown_2))
        data.write(struct.pack('>l', self.unknown_3))
        data.write(struct.pack(">L", self.particle_1))
        data.write(struct.pack(">L", self.particle_2))
        data.write(struct.pack('>l', self.always_ffffffff_1))
        data.write(struct.pack('>l', self.always_ffffffff_2))
        self.damage_info_1.to_stream(data)
        data.write(struct.pack('>f', self.unknown_4))
        self.damage_info_2.to_stream(data)
        data.write(struct.pack('>f', self.unknown_5))
        data.write(struct.pack('>f', self.unknown_6))
        data.write(struct.pack('>f', self.unknown_7))
        data.write(struct.pack('>f', self.unknown_8))
        data.write(struct.pack('>l', self.unknown_9))
        data.write(struct.pack('>l', self.unknown_10))
        data.write(struct.pack('>f', self.unknown_11))
        data.write(struct.pack('>f', self.unknown_12))
        data.write(struct.pack('>f', self.unknown_13))
        data.write(struct.pack('>f', self.unknown_14))
        data.write(struct.pack('>f', self.unknown_15))
        data.write(struct.pack('>f', self.unknown_16))
        data.write(struct.pack('>f', self.unknown_17))
        data.write(struct.pack('>f', self.unknown_18))
        data.write(struct.pack('>l', self.unknown_19))
        data.write(struct.pack('>f', self.unknown_20))
        data.write(struct.pack('>f', self.unknown_21))
        data.write(struct.pack('>f', self.unknown_22))
        self.unnamed_0x00000023.to_stream(data)
        self.unnamed_0x00000024.to_stream(data)
        data.write(struct.pack('>l', self.sound_1))
        data.write(struct.pack('>l', self.sound_2))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            position=Vector.from_json(data['position']),
            rotation=Vector.from_json(data['rotation']),
            scale=Vector.from_json(data['scale']),
            active=data['active'],
            unnamed_0x00000005=ActorParameters.from_json(data['unnamed_0x00000005']),
            unknown_1=data['unknown_1'],
            animation_parameters=AnimationParameters.from_json(data['animation_parameters']),
            unknown_2=data['unknown_2'],
            unknown_3=data['unknown_3'],
            particle_1=data['particle_1'],
            particle_2=data['particle_2'],
            always_ffffffff_1=data['always_ffffffff_1'],
            always_ffffffff_2=data['always_ffffffff_2'],
            damage_info_1=DamageInfo.from_json(data['damage_info_1']),
            unknown_4=data['unknown_4'],
            damage_info_2=DamageInfo.from_json(data['damage_info_2']),
            unknown_5=data['unknown_5'],
            unknown_6=data['unknown_6'],
            unknown_7=data['unknown_7'],
            unknown_8=data['unknown_8'],
            unknown_9=data['unknown_9'],
            unknown_10=data['unknown_10'],
            unknown_11=data['unknown_11'],
            unknown_12=data['unknown_12'],
            unknown_13=data['unknown_13'],
            unknown_14=data['unknown_14'],
            unknown_15=data['unknown_15'],
            unknown_16=data['unknown_16'],
            unknown_17=data['unknown_17'],
            unknown_18=data['unknown_18'],
            unknown_19=data['unknown_19'],
            unknown_20=data['unknown_20'],
            unknown_21=data['unknown_21'],
            unknown_22=data['unknown_22'],
            unnamed_0x00000023=HealthInfo.from_json(data['unnamed_0x00000023']),
            unnamed_0x00000024=DamageVulnerability.from_json(data['unnamed_0x00000024']),
            sound_1=data['sound_1'],
            sound_2=data['sound_2'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'position': self.position.to_json(),
            'rotation': self.rotation.to_json(),
            'scale': self.scale.to_json(),
            'active': self.active,
            'unnamed_0x00000005': self.unnamed_0x00000005.to_json(),
            'unknown_1': self.unknown_1,
            'animation_parameters': self.animation_parameters.to_json(),
            'unknown_2': self.unknown_2,
            'unknown_3': self.unknown_3,
            'particle_1': self.particle_1,
            'particle_2': self.particle_2,
            'always_ffffffff_1': self.always_ffffffff_1,
            'always_ffffffff_2': self.always_ffffffff_2,
            'damage_info_1': self.damage_info_1.to_json(),
            'unknown_4': self.unknown_4,
            'damage_info_2': self.damage_info_2.to_json(),
            'unknown_5': self.unknown_5,
            'unknown_6': self.unknown_6,
            'unknown_7': self.unknown_7,
            'unknown_8': self.unknown_8,
            'unknown_9': self.unknown_9,
            'unknown_10': self.unknown_10,
            'unknown_11': self.unknown_11,
            'unknown_12': self.unknown_12,
            'unknown_13': self.unknown_13,
            'unknown_14': self.unknown_14,
            'unknown_15': self.unknown_15,
            'unknown_16': self.unknown_16,
            'unknown_17': self.unknown_17,
            'unknown_18': self.unknown_18,
            'unknown_19': self.unknown_19,
            'unknown_20': self.unknown_20,
            'unknown_21': self.unknown_21,
            'unknown_22': self.unknown_22,
            'unnamed_0x00000023': self.unnamed_0x00000023.to_json(),
            'unnamed_0x00000024': self.unnamed_0x00000024.to_json(),
            'sound_1': self.sound_1,
            'sound_2': self.sound_2,
        }

    def _dependencies_for_unnamed_0x00000005(self, asset_manager):
        yield from self.unnamed_0x00000005.dependencies_for(asset_manager)

    def _dependencies_for_animation_parameters(self, asset_manager):
        yield from self.animation_parameters.dependencies_for(asset_manager)

    def _dependencies_for_particle_1(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle_1)

    def _dependencies_for_particle_2(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle_2)

    def _dependencies_for_damage_info_1(self, asset_manager):
        yield from self.damage_info_1.dependencies_for(asset_manager)

    def _dependencies_for_damage_info_2(self, asset_manager):
        yield from self.damage_info_2.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x00000023(self, asset_manager):
        yield from self.unnamed_0x00000023.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x00000024(self, asset_manager):
        yield from self.unnamed_0x00000024.dependencies_for(asset_manager)

    def _dependencies_for_sound_1(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_1)

    def _dependencies_for_sound_2(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_2)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_unnamed_0x00000005, "unnamed_0x00000005", "ActorParameters"),
            (self._dependencies_for_animation_parameters, "animation_parameters", "AnimationParameters"),
            (self._dependencies_for_particle_1, "particle_1", "AssetId"),
            (self._dependencies_for_particle_2, "particle_2", "AssetId"),
            (self._dependencies_for_damage_info_1, "damage_info_1", "DamageInfo"),
            (self._dependencies_for_damage_info_2, "damage_info_2", "DamageInfo"),
            (self._dependencies_for_unnamed_0x00000023, "unnamed_0x00000023", "HealthInfo"),
            (self._dependencies_for_unnamed_0x00000024, "unnamed_0x00000024", "DamageVulnerability"),
            (self._dependencies_for_sound_1, "sound_1", "int"),
            (self._dependencies_for_sound_2, "sound_2", "int"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for WallCrawlerSwarm.{field_name} ({field_type}): {e}"
                )
