# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.prime.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.prime.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.prime.archetypes.RidleyStruct1 import RidleyStruct1
from retro_data_structures.properties.prime.archetypes.RidleyStruct2 import RidleyStruct2
from retro_data_structures.properties.prime.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class Ridley(BaseObjectType):
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    rotation: Vector = dataclasses.field(default_factory=Vector)
    scale: Vector = dataclasses.field(default_factory=Vector)
    unnamed_0x00000004: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    unnamed_0x00000005: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    model_1: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    model_2: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    model_3: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    model_4: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    model_5: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    model_6: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    model_7: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    model_8: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    model_9: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    model_10: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    model_11: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    model_12: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    particle: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    unknown_1: float = dataclasses.field(default=0.0)
    unknown_2: float = dataclasses.field(default=0.0)
    unknown_3: float = dataclasses.field(default=0.0)
    unknown_4: float = dataclasses.field(default=0.0)
    wpsc_1: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    damage_info_1: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unnamed_0x00000019: RidleyStruct1 = dataclasses.field(default_factory=RidleyStruct1)
    sound_id_1: int = dataclasses.field(default=0, metadata={'sound': True})
    wpsc_2: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    damage_info_2: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    ridley_struct2_1: RidleyStruct2 = dataclasses.field(default_factory=RidleyStruct2)
    wpsc_3: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    damage_info_3: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    ridley_struct2_2: RidleyStruct2 = dataclasses.field(default_factory=RidleyStruct2)
    sound_id_2: int = dataclasses.field(default=0, metadata={'sound': True})
    damage_info_4: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    ridley_struct2_3: RidleyStruct2 = dataclasses.field(default_factory=RidleyStruct2)
    unknown_18: float = dataclasses.field(default=0.0)
    unknown_19: float = dataclasses.field(default=0.0)
    damage_info_5: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_20: float = dataclasses.field(default=0.0)
    damage_info_6: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_21: float = dataclasses.field(default=0.0)
    damage_info_7: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_22: float = dataclasses.field(default=0.0)
    elsc: AssetId = dataclasses.field(metadata={'asset_types': ['ELSC']}, default=default_asset_id)
    unknown_23: float = dataclasses.field(default=0.0)
    sound_id_3: int = dataclasses.field(default=0, metadata={'sound': True})
    damage_info_8: DamageInfo = dataclasses.field(default_factory=DamageInfo)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x7B

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
        model_1 = struct.unpack(">L", data.read(4))[0]
        model_2 = struct.unpack(">L", data.read(4))[0]
        model_3 = struct.unpack(">L", data.read(4))[0]
        model_4 = struct.unpack(">L", data.read(4))[0]
        model_5 = struct.unpack(">L", data.read(4))[0]
        model_6 = struct.unpack(">L", data.read(4))[0]
        model_7 = struct.unpack(">L", data.read(4))[0]
        model_8 = struct.unpack(">L", data.read(4))[0]
        model_9 = struct.unpack(">L", data.read(4))[0]
        model_10 = struct.unpack(">L", data.read(4))[0]
        model_11 = struct.unpack(">L", data.read(4))[0]
        model_12 = struct.unpack(">L", data.read(4))[0]
        particle = struct.unpack(">L", data.read(4))[0]
        unknown_1 = struct.unpack('>f', data.read(4))[0]
        unknown_2 = struct.unpack('>f', data.read(4))[0]
        unknown_3 = struct.unpack('>f', data.read(4))[0]
        unknown_4 = struct.unpack('>f', data.read(4))[0]
        wpsc_1 = struct.unpack(">L", data.read(4))[0]
        damage_info_1 = DamageInfo.from_stream(data, property_size)
        unnamed_0x00000019 = RidleyStruct1.from_stream(data, property_size)
        sound_id_1 = struct.unpack('>l', data.read(4))[0]
        wpsc_2 = struct.unpack(">L", data.read(4))[0]
        damage_info_2 = DamageInfo.from_stream(data, property_size)
        ridley_struct2_1 = RidleyStruct2.from_stream(data, property_size)
        wpsc_3 = struct.unpack(">L", data.read(4))[0]
        damage_info_3 = DamageInfo.from_stream(data, property_size)
        ridley_struct2_2 = RidleyStruct2.from_stream(data, property_size)
        sound_id_2 = struct.unpack('>l', data.read(4))[0]
        damage_info_4 = DamageInfo.from_stream(data, property_size)
        ridley_struct2_3 = RidleyStruct2.from_stream(data, property_size)
        unknown_18 = struct.unpack('>f', data.read(4))[0]
        unknown_19 = struct.unpack('>f', data.read(4))[0]
        damage_info_5 = DamageInfo.from_stream(data, property_size)
        unknown_20 = struct.unpack('>f', data.read(4))[0]
        damage_info_6 = DamageInfo.from_stream(data, property_size)
        unknown_21 = struct.unpack('>f', data.read(4))[0]
        damage_info_7 = DamageInfo.from_stream(data, property_size)
        unknown_22 = struct.unpack('>f', data.read(4))[0]
        elsc = struct.unpack(">L", data.read(4))[0]
        unknown_23 = struct.unpack('>f', data.read(4))[0]
        sound_id_3 = struct.unpack('>l', data.read(4))[0]
        damage_info_8 = DamageInfo.from_stream(data, property_size)
        return cls(name, position, rotation, scale, unnamed_0x00000004, unnamed_0x00000005, model_1, model_2, model_3, model_4, model_5, model_6, model_7, model_8, model_9, model_10, model_11, model_12, particle, unknown_1, unknown_2, unknown_3, unknown_4, wpsc_1, damage_info_1, unnamed_0x00000019, sound_id_1, wpsc_2, damage_info_2, ridley_struct2_1, wpsc_3, damage_info_3, ridley_struct2_2, sound_id_2, damage_info_4, ridley_struct2_3, unknown_18, unknown_19, damage_info_5, unknown_20, damage_info_6, unknown_21, damage_info_7, unknown_22, elsc, unknown_23, sound_id_3, damage_info_8)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x000')  # 48 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        self.rotation.to_stream(data)
        self.scale.to_stream(data)
        self.unnamed_0x00000004.to_stream(data)
        self.unnamed_0x00000005.to_stream(data)
        data.write(struct.pack(">L", self.model_1))
        data.write(struct.pack(">L", self.model_2))
        data.write(struct.pack(">L", self.model_3))
        data.write(struct.pack(">L", self.model_4))
        data.write(struct.pack(">L", self.model_5))
        data.write(struct.pack(">L", self.model_6))
        data.write(struct.pack(">L", self.model_7))
        data.write(struct.pack(">L", self.model_8))
        data.write(struct.pack(">L", self.model_9))
        data.write(struct.pack(">L", self.model_10))
        data.write(struct.pack(">L", self.model_11))
        data.write(struct.pack(">L", self.model_12))
        data.write(struct.pack(">L", self.particle))
        data.write(struct.pack('>f', self.unknown_1))
        data.write(struct.pack('>f', self.unknown_2))
        data.write(struct.pack('>f', self.unknown_3))
        data.write(struct.pack('>f', self.unknown_4))
        data.write(struct.pack(">L", self.wpsc_1))
        self.damage_info_1.to_stream(data)
        self.unnamed_0x00000019.to_stream(data)
        data.write(struct.pack('>l', self.sound_id_1))
        data.write(struct.pack(">L", self.wpsc_2))
        self.damage_info_2.to_stream(data)
        self.ridley_struct2_1.to_stream(data)
        data.write(struct.pack(">L", self.wpsc_3))
        self.damage_info_3.to_stream(data)
        self.ridley_struct2_2.to_stream(data)
        data.write(struct.pack('>l', self.sound_id_2))
        self.damage_info_4.to_stream(data)
        self.ridley_struct2_3.to_stream(data)
        data.write(struct.pack('>f', self.unknown_18))
        data.write(struct.pack('>f', self.unknown_19))
        self.damage_info_5.to_stream(data)
        data.write(struct.pack('>f', self.unknown_20))
        self.damage_info_6.to_stream(data)
        data.write(struct.pack('>f', self.unknown_21))
        self.damage_info_7.to_stream(data)
        data.write(struct.pack('>f', self.unknown_22))
        data.write(struct.pack(">L", self.elsc))
        data.write(struct.pack('>f', self.unknown_23))
        data.write(struct.pack('>l', self.sound_id_3))
        self.damage_info_8.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            position=Vector.from_json(data['position']),
            rotation=Vector.from_json(data['rotation']),
            scale=Vector.from_json(data['scale']),
            unnamed_0x00000004=PatternedAITypedef.from_json(data['unnamed_0x00000004']),
            unnamed_0x00000005=ActorParameters.from_json(data['unnamed_0x00000005']),
            model_1=data['model_1'],
            model_2=data['model_2'],
            model_3=data['model_3'],
            model_4=data['model_4'],
            model_5=data['model_5'],
            model_6=data['model_6'],
            model_7=data['model_7'],
            model_8=data['model_8'],
            model_9=data['model_9'],
            model_10=data['model_10'],
            model_11=data['model_11'],
            model_12=data['model_12'],
            particle=data['particle'],
            unknown_1=data['unknown_1'],
            unknown_2=data['unknown_2'],
            unknown_3=data['unknown_3'],
            unknown_4=data['unknown_4'],
            wpsc_1=data['wpsc_1'],
            damage_info_1=DamageInfo.from_json(data['damage_info_1']),
            unnamed_0x00000019=RidleyStruct1.from_json(data['unnamed_0x00000019']),
            sound_id_1=data['sound_id_1'],
            wpsc_2=data['wpsc_2'],
            damage_info_2=DamageInfo.from_json(data['damage_info_2']),
            ridley_struct2_1=RidleyStruct2.from_json(data['ridley_struct2_1']),
            wpsc_3=data['wpsc_3'],
            damage_info_3=DamageInfo.from_json(data['damage_info_3']),
            ridley_struct2_2=RidleyStruct2.from_json(data['ridley_struct2_2']),
            sound_id_2=data['sound_id_2'],
            damage_info_4=DamageInfo.from_json(data['damage_info_4']),
            ridley_struct2_3=RidleyStruct2.from_json(data['ridley_struct2_3']),
            unknown_18=data['unknown_18'],
            unknown_19=data['unknown_19'],
            damage_info_5=DamageInfo.from_json(data['damage_info_5']),
            unknown_20=data['unknown_20'],
            damage_info_6=DamageInfo.from_json(data['damage_info_6']),
            unknown_21=data['unknown_21'],
            damage_info_7=DamageInfo.from_json(data['damage_info_7']),
            unknown_22=data['unknown_22'],
            elsc=data['elsc'],
            unknown_23=data['unknown_23'],
            sound_id_3=data['sound_id_3'],
            damage_info_8=DamageInfo.from_json(data['damage_info_8']),
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'position': self.position.to_json(),
            'rotation': self.rotation.to_json(),
            'scale': self.scale.to_json(),
            'unnamed_0x00000004': self.unnamed_0x00000004.to_json(),
            'unnamed_0x00000005': self.unnamed_0x00000005.to_json(),
            'model_1': self.model_1,
            'model_2': self.model_2,
            'model_3': self.model_3,
            'model_4': self.model_4,
            'model_5': self.model_5,
            'model_6': self.model_6,
            'model_7': self.model_7,
            'model_8': self.model_8,
            'model_9': self.model_9,
            'model_10': self.model_10,
            'model_11': self.model_11,
            'model_12': self.model_12,
            'particle': self.particle,
            'unknown_1': self.unknown_1,
            'unknown_2': self.unknown_2,
            'unknown_3': self.unknown_3,
            'unknown_4': self.unknown_4,
            'wpsc_1': self.wpsc_1,
            'damage_info_1': self.damage_info_1.to_json(),
            'unnamed_0x00000019': self.unnamed_0x00000019.to_json(),
            'sound_id_1': self.sound_id_1,
            'wpsc_2': self.wpsc_2,
            'damage_info_2': self.damage_info_2.to_json(),
            'ridley_struct2_1': self.ridley_struct2_1.to_json(),
            'wpsc_3': self.wpsc_3,
            'damage_info_3': self.damage_info_3.to_json(),
            'ridley_struct2_2': self.ridley_struct2_2.to_json(),
            'sound_id_2': self.sound_id_2,
            'damage_info_4': self.damage_info_4.to_json(),
            'ridley_struct2_3': self.ridley_struct2_3.to_json(),
            'unknown_18': self.unknown_18,
            'unknown_19': self.unknown_19,
            'damage_info_5': self.damage_info_5.to_json(),
            'unknown_20': self.unknown_20,
            'damage_info_6': self.damage_info_6.to_json(),
            'unknown_21': self.unknown_21,
            'damage_info_7': self.damage_info_7.to_json(),
            'unknown_22': self.unknown_22,
            'elsc': self.elsc,
            'unknown_23': self.unknown_23,
            'sound_id_3': self.sound_id_3,
            'damage_info_8': self.damage_info_8.to_json(),
        }

    def _dependencies_for_unnamed_0x00000004(self, asset_manager):
        yield from self.unnamed_0x00000004.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x00000005(self, asset_manager):
        yield from self.unnamed_0x00000005.dependencies_for(asset_manager)

    def _dependencies_for_model_1(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.model_1)

    def _dependencies_for_model_2(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.model_2)

    def _dependencies_for_model_3(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.model_3)

    def _dependencies_for_model_4(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.model_4)

    def _dependencies_for_model_5(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.model_5)

    def _dependencies_for_model_6(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.model_6)

    def _dependencies_for_model_7(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.model_7)

    def _dependencies_for_model_8(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.model_8)

    def _dependencies_for_model_9(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.model_9)

    def _dependencies_for_model_10(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.model_10)

    def _dependencies_for_model_11(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.model_11)

    def _dependencies_for_model_12(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.model_12)

    def _dependencies_for_particle(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle)

    def _dependencies_for_wpsc_1(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.wpsc_1)

    def _dependencies_for_damage_info_1(self, asset_manager):
        yield from self.damage_info_1.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x00000019(self, asset_manager):
        yield from self.unnamed_0x00000019.dependencies_for(asset_manager)

    def _dependencies_for_sound_id_1(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_id_1)

    def _dependencies_for_wpsc_2(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.wpsc_2)

    def _dependencies_for_damage_info_2(self, asset_manager):
        yield from self.damage_info_2.dependencies_for(asset_manager)

    def _dependencies_for_ridley_struct2_1(self, asset_manager):
        yield from self.ridley_struct2_1.dependencies_for(asset_manager)

    def _dependencies_for_wpsc_3(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.wpsc_3)

    def _dependencies_for_damage_info_3(self, asset_manager):
        yield from self.damage_info_3.dependencies_for(asset_manager)

    def _dependencies_for_ridley_struct2_2(self, asset_manager):
        yield from self.ridley_struct2_2.dependencies_for(asset_manager)

    def _dependencies_for_sound_id_2(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_id_2)

    def _dependencies_for_damage_info_4(self, asset_manager):
        yield from self.damage_info_4.dependencies_for(asset_manager)

    def _dependencies_for_ridley_struct2_3(self, asset_manager):
        yield from self.ridley_struct2_3.dependencies_for(asset_manager)

    def _dependencies_for_damage_info_5(self, asset_manager):
        yield from self.damage_info_5.dependencies_for(asset_manager)

    def _dependencies_for_damage_info_6(self, asset_manager):
        yield from self.damage_info_6.dependencies_for(asset_manager)

    def _dependencies_for_damage_info_7(self, asset_manager):
        yield from self.damage_info_7.dependencies_for(asset_manager)

    def _dependencies_for_elsc(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.elsc)

    def _dependencies_for_sound_id_3(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_id_3)

    def _dependencies_for_damage_info_8(self, asset_manager):
        yield from self.damage_info_8.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_unnamed_0x00000004, "unnamed_0x00000004", "PatternedAITypedef"),
            (self._dependencies_for_unnamed_0x00000005, "unnamed_0x00000005", "ActorParameters"),
            (self._dependencies_for_model_1, "model_1", "AssetId"),
            (self._dependencies_for_model_2, "model_2", "AssetId"),
            (self._dependencies_for_model_3, "model_3", "AssetId"),
            (self._dependencies_for_model_4, "model_4", "AssetId"),
            (self._dependencies_for_model_5, "model_5", "AssetId"),
            (self._dependencies_for_model_6, "model_6", "AssetId"),
            (self._dependencies_for_model_7, "model_7", "AssetId"),
            (self._dependencies_for_model_8, "model_8", "AssetId"),
            (self._dependencies_for_model_9, "model_9", "AssetId"),
            (self._dependencies_for_model_10, "model_10", "AssetId"),
            (self._dependencies_for_model_11, "model_11", "AssetId"),
            (self._dependencies_for_model_12, "model_12", "AssetId"),
            (self._dependencies_for_particle, "particle", "AssetId"),
            (self._dependencies_for_wpsc_1, "wpsc_1", "AssetId"),
            (self._dependencies_for_damage_info_1, "damage_info_1", "DamageInfo"),
            (self._dependencies_for_unnamed_0x00000019, "unnamed_0x00000019", "RidleyStruct1"),
            (self._dependencies_for_sound_id_1, "sound_id_1", "int"),
            (self._dependencies_for_wpsc_2, "wpsc_2", "AssetId"),
            (self._dependencies_for_damage_info_2, "damage_info_2", "DamageInfo"),
            (self._dependencies_for_ridley_struct2_1, "ridley_struct2_1", "RidleyStruct2"),
            (self._dependencies_for_wpsc_3, "wpsc_3", "AssetId"),
            (self._dependencies_for_damage_info_3, "damage_info_3", "DamageInfo"),
            (self._dependencies_for_ridley_struct2_2, "ridley_struct2_2", "RidleyStruct2"),
            (self._dependencies_for_sound_id_2, "sound_id_2", "int"),
            (self._dependencies_for_damage_info_4, "damage_info_4", "DamageInfo"),
            (self._dependencies_for_ridley_struct2_3, "ridley_struct2_3", "RidleyStruct2"),
            (self._dependencies_for_damage_info_5, "damage_info_5", "DamageInfo"),
            (self._dependencies_for_damage_info_6, "damage_info_6", "DamageInfo"),
            (self._dependencies_for_damage_info_7, "damage_info_7", "DamageInfo"),
            (self._dependencies_for_elsc, "elsc", "AssetId"),
            (self._dependencies_for_sound_id_3, "sound_id_3", "int"),
            (self._dependencies_for_damage_info_8, "damage_info_8", "DamageInfo"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for Ridley.{field_name} ({field_type}): {e}"
                )
