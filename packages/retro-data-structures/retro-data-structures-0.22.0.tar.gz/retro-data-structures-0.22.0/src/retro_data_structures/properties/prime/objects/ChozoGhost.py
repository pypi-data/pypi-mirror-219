# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.prime.archetypes.BehaveChance import BehaveChance
from retro_data_structures.properties.prime.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.prime.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.prime.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class ChozoGhost(BaseObjectType):
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    rotation: Vector = dataclasses.field(default_factory=Vector)
    scale: Vector = dataclasses.field(default_factory=Vector)
    unnamed_0x00000004: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    unnamed_0x00000005: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    unknown_1: float = dataclasses.field(default=0.0)
    unknown_2: float = dataclasses.field(default=0.0)
    unknown_3: float = dataclasses.field(default=0.0)
    unknown_4: float = dataclasses.field(default=0.0)
    wpsc_1: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    damage_info_1: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    wpsc_2: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    damage_info_2: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    behave_chance_1: BehaveChance = dataclasses.field(default_factory=BehaveChance)
    behave_chance_2: BehaveChance = dataclasses.field(default_factory=BehaveChance)
    behave_chance_3: BehaveChance = dataclasses.field(default_factory=BehaveChance)
    sound_id_1: int = dataclasses.field(default=0, metadata={'sound': True})
    unknown_5: float = dataclasses.field(default=0.0)
    sound_id_2: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_id_3: int = dataclasses.field(default=0, metadata={'sound': True})
    unknown_6: int = dataclasses.field(default=0)
    unknown_7: float = dataclasses.field(default=0.0)
    unknown_8: int = dataclasses.field(default=0)
    unknown_9: float = dataclasses.field(default=0.0)
    particle: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    sound_id_4: int = dataclasses.field(default=0, metadata={'sound': True})
    unknown_10: float = dataclasses.field(default=0.0)
    unknown_11: float = dataclasses.field(default=0.0)
    unknown_12: int = dataclasses.field(default=0)
    unknown_13: int = dataclasses.field(default=0)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x28

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        position = Vector.from_stream(data)
        rotation = Vector.from_stream(data)
        scale = Vector.from_stream(data)
        unnamed_0x00000004 = PatternedAITypedef.from_stream(data, property_size)
        unnamed_0x00000005 = ActorParameters.from_stream(data, property_size)
        unknown_1 = struct.unpack('>f', data.read(4))[0]
        unknown_2 = struct.unpack('>f', data.read(4))[0]
        unknown_3 = struct.unpack('>f', data.read(4))[0]
        unknown_4 = struct.unpack('>f', data.read(4))[0]
        wpsc_1 = struct.unpack(">L", data.read(4))[0]
        damage_info_1 = DamageInfo.from_stream(data, property_size)
        wpsc_2 = struct.unpack(">L", data.read(4))[0]
        damage_info_2 = DamageInfo.from_stream(data, property_size)
        behave_chance_1 = BehaveChance.from_stream(data, property_size)
        behave_chance_2 = BehaveChance.from_stream(data, property_size)
        behave_chance_3 = BehaveChance.from_stream(data, property_size)
        sound_id_1 = struct.unpack('>l', data.read(4))[0]
        unknown_5 = struct.unpack('>f', data.read(4))[0]
        sound_id_2 = struct.unpack('>l', data.read(4))[0]
        sound_id_3 = struct.unpack('>l', data.read(4))[0]
        unknown_6 = struct.unpack('>l', data.read(4))[0]
        unknown_7 = struct.unpack('>f', data.read(4))[0]
        unknown_8 = struct.unpack('>l', data.read(4))[0]
        unknown_9 = struct.unpack('>f', data.read(4))[0]
        particle = struct.unpack(">L", data.read(4))[0]
        sound_id_4 = struct.unpack('>l', data.read(4))[0]
        unknown_10 = struct.unpack('>f', data.read(4))[0]
        unknown_11 = struct.unpack('>f', data.read(4))[0]
        unknown_12 = struct.unpack('>l', data.read(4))[0]
        unknown_13 = struct.unpack('>l', data.read(4))[0]
        return cls(name, position, rotation, scale, unnamed_0x00000004, unnamed_0x00000005, unknown_1, unknown_2, unknown_3, unknown_4, wpsc_1, damage_info_1, wpsc_2, damage_info_2, behave_chance_1, behave_chance_2, behave_chance_3, sound_id_1, unknown_5, sound_id_2, sound_id_3, unknown_6, unknown_7, unknown_8, unknown_9, particle, sound_id_4, unknown_10, unknown_11, unknown_12, unknown_13)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x1f')  # 31 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        self.rotation.to_stream(data)
        self.scale.to_stream(data)
        self.unnamed_0x00000004.to_stream(data)
        self.unnamed_0x00000005.to_stream(data)
        data.write(struct.pack('>f', self.unknown_1))
        data.write(struct.pack('>f', self.unknown_2))
        data.write(struct.pack('>f', self.unknown_3))
        data.write(struct.pack('>f', self.unknown_4))
        data.write(struct.pack(">L", self.wpsc_1))
        self.damage_info_1.to_stream(data)
        data.write(struct.pack(">L", self.wpsc_2))
        self.damage_info_2.to_stream(data)
        self.behave_chance_1.to_stream(data)
        self.behave_chance_2.to_stream(data)
        self.behave_chance_3.to_stream(data)
        data.write(struct.pack('>l', self.sound_id_1))
        data.write(struct.pack('>f', self.unknown_5))
        data.write(struct.pack('>l', self.sound_id_2))
        data.write(struct.pack('>l', self.sound_id_3))
        data.write(struct.pack('>l', self.unknown_6))
        data.write(struct.pack('>f', self.unknown_7))
        data.write(struct.pack('>l', self.unknown_8))
        data.write(struct.pack('>f', self.unknown_9))
        data.write(struct.pack(">L", self.particle))
        data.write(struct.pack('>l', self.sound_id_4))
        data.write(struct.pack('>f', self.unknown_10))
        data.write(struct.pack('>f', self.unknown_11))
        data.write(struct.pack('>l', self.unknown_12))
        data.write(struct.pack('>l', self.unknown_13))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            position=Vector.from_json(data['position']),
            rotation=Vector.from_json(data['rotation']),
            scale=Vector.from_json(data['scale']),
            unnamed_0x00000004=PatternedAITypedef.from_json(data['unnamed_0x00000004']),
            unnamed_0x00000005=ActorParameters.from_json(data['unnamed_0x00000005']),
            unknown_1=data['unknown_1'],
            unknown_2=data['unknown_2'],
            unknown_3=data['unknown_3'],
            unknown_4=data['unknown_4'],
            wpsc_1=data['wpsc_1'],
            damage_info_1=DamageInfo.from_json(data['damage_info_1']),
            wpsc_2=data['wpsc_2'],
            damage_info_2=DamageInfo.from_json(data['damage_info_2']),
            behave_chance_1=BehaveChance.from_json(data['behave_chance_1']),
            behave_chance_2=BehaveChance.from_json(data['behave_chance_2']),
            behave_chance_3=BehaveChance.from_json(data['behave_chance_3']),
            sound_id_1=data['sound_id_1'],
            unknown_5=data['unknown_5'],
            sound_id_2=data['sound_id_2'],
            sound_id_3=data['sound_id_3'],
            unknown_6=data['unknown_6'],
            unknown_7=data['unknown_7'],
            unknown_8=data['unknown_8'],
            unknown_9=data['unknown_9'],
            particle=data['particle'],
            sound_id_4=data['sound_id_4'],
            unknown_10=data['unknown_10'],
            unknown_11=data['unknown_11'],
            unknown_12=data['unknown_12'],
            unknown_13=data['unknown_13'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'position': self.position.to_json(),
            'rotation': self.rotation.to_json(),
            'scale': self.scale.to_json(),
            'unnamed_0x00000004': self.unnamed_0x00000004.to_json(),
            'unnamed_0x00000005': self.unnamed_0x00000005.to_json(),
            'unknown_1': self.unknown_1,
            'unknown_2': self.unknown_2,
            'unknown_3': self.unknown_3,
            'unknown_4': self.unknown_4,
            'wpsc_1': self.wpsc_1,
            'damage_info_1': self.damage_info_1.to_json(),
            'wpsc_2': self.wpsc_2,
            'damage_info_2': self.damage_info_2.to_json(),
            'behave_chance_1': self.behave_chance_1.to_json(),
            'behave_chance_2': self.behave_chance_2.to_json(),
            'behave_chance_3': self.behave_chance_3.to_json(),
            'sound_id_1': self.sound_id_1,
            'unknown_5': self.unknown_5,
            'sound_id_2': self.sound_id_2,
            'sound_id_3': self.sound_id_3,
            'unknown_6': self.unknown_6,
            'unknown_7': self.unknown_7,
            'unknown_8': self.unknown_8,
            'unknown_9': self.unknown_9,
            'particle': self.particle,
            'sound_id_4': self.sound_id_4,
            'unknown_10': self.unknown_10,
            'unknown_11': self.unknown_11,
            'unknown_12': self.unknown_12,
            'unknown_13': self.unknown_13,
        }

    def _dependencies_for_unnamed_0x00000004(self, asset_manager):
        yield from self.unnamed_0x00000004.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x00000005(self, asset_manager):
        yield from self.unnamed_0x00000005.dependencies_for(asset_manager)

    def _dependencies_for_wpsc_1(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.wpsc_1)

    def _dependencies_for_damage_info_1(self, asset_manager):
        yield from self.damage_info_1.dependencies_for(asset_manager)

    def _dependencies_for_wpsc_2(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.wpsc_2)

    def _dependencies_for_damage_info_2(self, asset_manager):
        yield from self.damage_info_2.dependencies_for(asset_manager)

    def _dependencies_for_behave_chance_1(self, asset_manager):
        yield from self.behave_chance_1.dependencies_for(asset_manager)

    def _dependencies_for_behave_chance_2(self, asset_manager):
        yield from self.behave_chance_2.dependencies_for(asset_manager)

    def _dependencies_for_behave_chance_3(self, asset_manager):
        yield from self.behave_chance_3.dependencies_for(asset_manager)

    def _dependencies_for_sound_id_1(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_id_1)

    def _dependencies_for_sound_id_2(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_id_2)

    def _dependencies_for_sound_id_3(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_id_3)

    def _dependencies_for_particle(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle)

    def _dependencies_for_sound_id_4(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_id_4)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_unnamed_0x00000004, "unnamed_0x00000004", "PatternedAITypedef"),
            (self._dependencies_for_unnamed_0x00000005, "unnamed_0x00000005", "ActorParameters"),
            (self._dependencies_for_wpsc_1, "wpsc_1", "AssetId"),
            (self._dependencies_for_damage_info_1, "damage_info_1", "DamageInfo"),
            (self._dependencies_for_wpsc_2, "wpsc_2", "AssetId"),
            (self._dependencies_for_damage_info_2, "damage_info_2", "DamageInfo"),
            (self._dependencies_for_behave_chance_1, "behave_chance_1", "BehaveChance"),
            (self._dependencies_for_behave_chance_2, "behave_chance_2", "BehaveChance"),
            (self._dependencies_for_behave_chance_3, "behave_chance_3", "BehaveChance"),
            (self._dependencies_for_sound_id_1, "sound_id_1", "int"),
            (self._dependencies_for_sound_id_2, "sound_id_2", "int"),
            (self._dependencies_for_sound_id_3, "sound_id_3", "int"),
            (self._dependencies_for_particle, "particle", "AssetId"),
            (self._dependencies_for_sound_id_4, "sound_id_4", "int"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for ChozoGhost.{field_name} ({field_type}): {e}"
                )
