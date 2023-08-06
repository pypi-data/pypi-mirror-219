# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.prime.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.prime.archetypes.FlareDef import FlareDef
from retro_data_structures.properties.prime.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.prime.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class Drone(BaseObjectType):
    name: str = dataclasses.field(default='')
    unknown_1: int = dataclasses.field(default=0)
    position: Vector = dataclasses.field(default_factory=Vector)
    rotation: Vector = dataclasses.field(default_factory=Vector)
    scale: Vector = dataclasses.field(default_factory=Vector)
    unknown_2: float = dataclasses.field(default=0.0)
    unnamed_0x00000006: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    unnamed_0x00000007: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    damage_info_1: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_3: int = dataclasses.field(default=0)
    damage_info_2: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    particle_1: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    particle_2: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    model_1: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    flare_def_1: FlareDef = dataclasses.field(default_factory=FlareDef)
    flare_def_2: FlareDef = dataclasses.field(default_factory=FlareDef)
    flare_def_3: FlareDef = dataclasses.field(default_factory=FlareDef)
    flare_def_4: FlareDef = dataclasses.field(default_factory=FlareDef)
    flare_def_5: FlareDef = dataclasses.field(default_factory=FlareDef)
    unknown_7: float = dataclasses.field(default=0.0)
    unknown_8: float = dataclasses.field(default=0.0)
    unknown_9: float = dataclasses.field(default=0.0)
    unknown_10: float = dataclasses.field(default=0.0)
    unknown_11: float = dataclasses.field(default=0.0)
    unknown_12: float = dataclasses.field(default=0.0)
    unknown_13: float = dataclasses.field(default=0.0)
    unknown_14: float = dataclasses.field(default=0.0)
    unknown_15: float = dataclasses.field(default=0.0)
    unknown_16: float = dataclasses.field(default=0.0)
    unknown_17: float = dataclasses.field(default=0.0)
    unknown_18: float = dataclasses.field(default=0.0)
    unknown_19: float = dataclasses.field(default=0.0)
    unknown_20: float = dataclasses.field(default=0.0)
    unknown_21: float = dataclasses.field(default=0.0)
    unknown_22: float = dataclasses.field(default=0.0)
    unknown_23: float = dataclasses.field(default=0.0)
    unknown_24: float = dataclasses.field(default=0.0)
    unknown_25: float = dataclasses.field(default=0.0)
    crsc: AssetId = dataclasses.field(metadata={'asset_types': ['CRSC']}, default=default_asset_id)
    unknown_26: float = dataclasses.field(default=0.0)
    unknown_27: float = dataclasses.field(default=0.0)
    unknown_28: float = dataclasses.field(default=0.0)
    unknown_29: float = dataclasses.field(default=0.0)
    sound: int = dataclasses.field(default=0, metadata={'sound': True})
    unknown_30: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x43

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        unknown_1 = struct.unpack('>l', data.read(4))[0]
        position = Vector.from_stream(data)
        rotation = Vector.from_stream(data)
        scale = Vector.from_stream(data)
        unknown_2 = struct.unpack('>f', data.read(4))[0]
        unnamed_0x00000006 = PatternedAITypedef.from_stream(data, property_size)
        unnamed_0x00000007 = ActorParameters.from_stream(data, property_size)
        damage_info_1 = DamageInfo.from_stream(data, property_size)
        unknown_3 = struct.unpack('>l', data.read(4))[0]
        damage_info_2 = DamageInfo.from_stream(data, property_size)
        particle_1 = struct.unpack(">L", data.read(4))[0]
        particle_2 = struct.unpack(">L", data.read(4))[0]
        model_1 = struct.unpack(">L", data.read(4))[0]
        flare_def_1 = FlareDef.from_stream(data, property_size)
        flare_def_2 = FlareDef.from_stream(data, property_size)
        flare_def_3 = FlareDef.from_stream(data, property_size)
        flare_def_4 = FlareDef.from_stream(data, property_size)
        flare_def_5 = FlareDef.from_stream(data, property_size)
        unknown_7 = struct.unpack('>f', data.read(4))[0]
        unknown_8 = struct.unpack('>f', data.read(4))[0]
        unknown_9 = struct.unpack('>f', data.read(4))[0]
        unknown_10 = struct.unpack('>f', data.read(4))[0]
        unknown_11 = struct.unpack('>f', data.read(4))[0]
        unknown_12 = struct.unpack('>f', data.read(4))[0]
        unknown_13 = struct.unpack('>f', data.read(4))[0]
        unknown_14 = struct.unpack('>f', data.read(4))[0]
        unknown_15 = struct.unpack('>f', data.read(4))[0]
        unknown_16 = struct.unpack('>f', data.read(4))[0]
        unknown_17 = struct.unpack('>f', data.read(4))[0]
        unknown_18 = struct.unpack('>f', data.read(4))[0]
        unknown_19 = struct.unpack('>f', data.read(4))[0]
        unknown_20 = struct.unpack('>f', data.read(4))[0]
        unknown_21 = struct.unpack('>f', data.read(4))[0]
        unknown_22 = struct.unpack('>f', data.read(4))[0]
        unknown_23 = struct.unpack('>f', data.read(4))[0]
        unknown_24 = struct.unpack('>f', data.read(4))[0]
        unknown_25 = struct.unpack('>f', data.read(4))[0]
        crsc = struct.unpack(">L", data.read(4))[0]
        unknown_26 = struct.unpack('>f', data.read(4))[0]
        unknown_27 = struct.unpack('>f', data.read(4))[0]
        unknown_28 = struct.unpack('>f', data.read(4))[0]
        unknown_29 = struct.unpack('>f', data.read(4))[0]
        sound = struct.unpack('>l', data.read(4))[0]
        unknown_30 = struct.unpack('>?', data.read(1))[0]
        return cls(name, unknown_1, position, rotation, scale, unknown_2, unnamed_0x00000006, unnamed_0x00000007, damage_info_1, unknown_3, damage_info_2, particle_1, particle_2, model_1, flare_def_1, flare_def_2, flare_def_3, flare_def_4, flare_def_5, unknown_7, unknown_8, unknown_9, unknown_10, unknown_11, unknown_12, unknown_13, unknown_14, unknown_15, unknown_16, unknown_17, unknown_18, unknown_19, unknown_20, unknown_21, unknown_22, unknown_23, unknown_24, unknown_25, crsc, unknown_26, unknown_27, unknown_28, unknown_29, sound, unknown_30)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00-')  # 45 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        data.write(struct.pack('>l', self.unknown_1))
        self.position.to_stream(data)
        self.rotation.to_stream(data)
        self.scale.to_stream(data)
        data.write(struct.pack('>f', self.unknown_2))
        self.unnamed_0x00000006.to_stream(data)
        self.unnamed_0x00000007.to_stream(data)
        self.damage_info_1.to_stream(data)
        data.write(struct.pack('>l', self.unknown_3))
        self.damage_info_2.to_stream(data)
        data.write(struct.pack(">L", self.particle_1))
        data.write(struct.pack(">L", self.particle_2))
        data.write(struct.pack(">L", self.model_1))
        self.flare_def_1.to_stream(data)
        self.flare_def_2.to_stream(data)
        self.flare_def_3.to_stream(data)
        self.flare_def_4.to_stream(data)
        self.flare_def_5.to_stream(data)
        data.write(struct.pack('>f', self.unknown_7))
        data.write(struct.pack('>f', self.unknown_8))
        data.write(struct.pack('>f', self.unknown_9))
        data.write(struct.pack('>f', self.unknown_10))
        data.write(struct.pack('>f', self.unknown_11))
        data.write(struct.pack('>f', self.unknown_12))
        data.write(struct.pack('>f', self.unknown_13))
        data.write(struct.pack('>f', self.unknown_14))
        data.write(struct.pack('>f', self.unknown_15))
        data.write(struct.pack('>f', self.unknown_16))
        data.write(struct.pack('>f', self.unknown_17))
        data.write(struct.pack('>f', self.unknown_18))
        data.write(struct.pack('>f', self.unknown_19))
        data.write(struct.pack('>f', self.unknown_20))
        data.write(struct.pack('>f', self.unknown_21))
        data.write(struct.pack('>f', self.unknown_22))
        data.write(struct.pack('>f', self.unknown_23))
        data.write(struct.pack('>f', self.unknown_24))
        data.write(struct.pack('>f', self.unknown_25))
        data.write(struct.pack(">L", self.crsc))
        data.write(struct.pack('>f', self.unknown_26))
        data.write(struct.pack('>f', self.unknown_27))
        data.write(struct.pack('>f', self.unknown_28))
        data.write(struct.pack('>f', self.unknown_29))
        data.write(struct.pack('>l', self.sound))
        data.write(struct.pack('>?', self.unknown_30))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            unknown_1=data['unknown_1'],
            position=Vector.from_json(data['position']),
            rotation=Vector.from_json(data['rotation']),
            scale=Vector.from_json(data['scale']),
            unknown_2=data['unknown_2'],
            unnamed_0x00000006=PatternedAITypedef.from_json(data['unnamed_0x00000006']),
            unnamed_0x00000007=ActorParameters.from_json(data['unnamed_0x00000007']),
            damage_info_1=DamageInfo.from_json(data['damage_info_1']),
            unknown_3=data['unknown_3'],
            damage_info_2=DamageInfo.from_json(data['damage_info_2']),
            particle_1=data['particle_1'],
            particle_2=data['particle_2'],
            model_1=data['model_1'],
            flare_def_1=FlareDef.from_json(data['flare_def_1']),
            flare_def_2=FlareDef.from_json(data['flare_def_2']),
            flare_def_3=FlareDef.from_json(data['flare_def_3']),
            flare_def_4=FlareDef.from_json(data['flare_def_4']),
            flare_def_5=FlareDef.from_json(data['flare_def_5']),
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
            unknown_23=data['unknown_23'],
            unknown_24=data['unknown_24'],
            unknown_25=data['unknown_25'],
            crsc=data['crsc'],
            unknown_26=data['unknown_26'],
            unknown_27=data['unknown_27'],
            unknown_28=data['unknown_28'],
            unknown_29=data['unknown_29'],
            sound=data['sound'],
            unknown_30=data['unknown_30'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'unknown_1': self.unknown_1,
            'position': self.position.to_json(),
            'rotation': self.rotation.to_json(),
            'scale': self.scale.to_json(),
            'unknown_2': self.unknown_2,
            'unnamed_0x00000006': self.unnamed_0x00000006.to_json(),
            'unnamed_0x00000007': self.unnamed_0x00000007.to_json(),
            'damage_info_1': self.damage_info_1.to_json(),
            'unknown_3': self.unknown_3,
            'damage_info_2': self.damage_info_2.to_json(),
            'particle_1': self.particle_1,
            'particle_2': self.particle_2,
            'model_1': self.model_1,
            'flare_def_1': self.flare_def_1.to_json(),
            'flare_def_2': self.flare_def_2.to_json(),
            'flare_def_3': self.flare_def_3.to_json(),
            'flare_def_4': self.flare_def_4.to_json(),
            'flare_def_5': self.flare_def_5.to_json(),
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
            'unknown_23': self.unknown_23,
            'unknown_24': self.unknown_24,
            'unknown_25': self.unknown_25,
            'crsc': self.crsc,
            'unknown_26': self.unknown_26,
            'unknown_27': self.unknown_27,
            'unknown_28': self.unknown_28,
            'unknown_29': self.unknown_29,
            'sound': self.sound,
            'unknown_30': self.unknown_30,
        }

    def _dependencies_for_unnamed_0x00000006(self, asset_manager):
        yield from self.unnamed_0x00000006.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x00000007(self, asset_manager):
        yield from self.unnamed_0x00000007.dependencies_for(asset_manager)

    def _dependencies_for_damage_info_1(self, asset_manager):
        yield from self.damage_info_1.dependencies_for(asset_manager)

    def _dependencies_for_damage_info_2(self, asset_manager):
        yield from self.damage_info_2.dependencies_for(asset_manager)

    def _dependencies_for_particle_1(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle_1)

    def _dependencies_for_particle_2(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle_2)

    def _dependencies_for_model_1(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.model_1)

    def _dependencies_for_flare_def_1(self, asset_manager):
        yield from self.flare_def_1.dependencies_for(asset_manager)

    def _dependencies_for_flare_def_2(self, asset_manager):
        yield from self.flare_def_2.dependencies_for(asset_manager)

    def _dependencies_for_flare_def_3(self, asset_manager):
        yield from self.flare_def_3.dependencies_for(asset_manager)

    def _dependencies_for_flare_def_4(self, asset_manager):
        yield from self.flare_def_4.dependencies_for(asset_manager)

    def _dependencies_for_flare_def_5(self, asset_manager):
        yield from self.flare_def_5.dependencies_for(asset_manager)

    def _dependencies_for_crsc(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.crsc)

    def _dependencies_for_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_unnamed_0x00000006, "unnamed_0x00000006", "PatternedAITypedef"),
            (self._dependencies_for_unnamed_0x00000007, "unnamed_0x00000007", "ActorParameters"),
            (self._dependencies_for_damage_info_1, "damage_info_1", "DamageInfo"),
            (self._dependencies_for_damage_info_2, "damage_info_2", "DamageInfo"),
            (self._dependencies_for_particle_1, "particle_1", "AssetId"),
            (self._dependencies_for_particle_2, "particle_2", "AssetId"),
            (self._dependencies_for_model_1, "model_1", "AssetId"),
            (self._dependencies_for_flare_def_1, "flare_def_1", "FlareDef"),
            (self._dependencies_for_flare_def_2, "flare_def_2", "FlareDef"),
            (self._dependencies_for_flare_def_3, "flare_def_3", "FlareDef"),
            (self._dependencies_for_flare_def_4, "flare_def_4", "FlareDef"),
            (self._dependencies_for_flare_def_5, "flare_def_5", "FlareDef"),
            (self._dependencies_for_crsc, "crsc", "AssetId"),
            (self._dependencies_for_sound, "sound", "int"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for Drone.{field_name} ({field_type}): {e}"
                )
