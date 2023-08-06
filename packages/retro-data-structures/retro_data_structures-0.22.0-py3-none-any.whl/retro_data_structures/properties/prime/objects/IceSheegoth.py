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
from retro_data_structures.properties.prime.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class IceSheegoth(BaseObjectType):
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    rotation: Vector = dataclasses.field(default_factory=Vector)
    scale: Vector = dataclasses.field(default_factory=Vector)
    unnamed_0x00000004: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    unnamed_0x00000005: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    unknown_1: float = dataclasses.field(default=0.0)
    unknown_2: float = dataclasses.field(default=0.0)
    unknown_3: Vector = dataclasses.field(default_factory=Vector)
    unknown_4: float = dataclasses.field(default=0.0)
    damage_vulnerability_1: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    damage_vulnerability_2: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    damage_vulnerability_3: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    wpsc_1: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    damage_info_1: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_5: float = dataclasses.field(default=0.0)
    unknown_6: float = dataclasses.field(default=0.0)
    wpsc_2: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    particle_1: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    damage_info_2: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    particle_2: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    particle_3: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    particle_4: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    particle_5: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    elsc: AssetId = dataclasses.field(metadata={'asset_types': ['ELSC']}, default=default_asset_id)
    unknown_7: float = dataclasses.field(default=0.0)
    unknown_8: float = dataclasses.field(default=0.0)
    damage_info_3: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    sound_id_1: int = dataclasses.field(default=0, metadata={'sound': True})
    unknown_9: float = dataclasses.field(default=0.0)
    unknown_10: float = dataclasses.field(default=0.0)
    unknown_11: float = dataclasses.field(default=0.0)
    texture: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    sound_id_2: int = dataclasses.field(default=0, metadata={'sound': True})
    particle_6: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    unknown_12: bool = dataclasses.field(default=False)
    unknown_13: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x4B

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
        unknown_3 = Vector.from_stream(data)
        unknown_4 = struct.unpack('>f', data.read(4))[0]
        damage_vulnerability_1 = DamageVulnerability.from_stream(data, property_size)
        damage_vulnerability_2 = DamageVulnerability.from_stream(data, property_size)
        damage_vulnerability_3 = DamageVulnerability.from_stream(data, property_size)
        wpsc_1 = struct.unpack(">L", data.read(4))[0]
        damage_info_1 = DamageInfo.from_stream(data, property_size)
        unknown_5 = struct.unpack('>f', data.read(4))[0]
        unknown_6 = struct.unpack('>f', data.read(4))[0]
        wpsc_2 = struct.unpack(">L", data.read(4))[0]
        particle_1 = struct.unpack(">L", data.read(4))[0]
        damage_info_2 = DamageInfo.from_stream(data, property_size)
        particle_2 = struct.unpack(">L", data.read(4))[0]
        particle_3 = struct.unpack(">L", data.read(4))[0]
        particle_4 = struct.unpack(">L", data.read(4))[0]
        particle_5 = struct.unpack(">L", data.read(4))[0]
        elsc = struct.unpack(">L", data.read(4))[0]
        unknown_7 = struct.unpack('>f', data.read(4))[0]
        unknown_8 = struct.unpack('>f', data.read(4))[0]
        damage_info_3 = DamageInfo.from_stream(data, property_size)
        sound_id_1 = struct.unpack('>l', data.read(4))[0]
        unknown_9 = struct.unpack('>f', data.read(4))[0]
        unknown_10 = struct.unpack('>f', data.read(4))[0]
        unknown_11 = struct.unpack('>f', data.read(4))[0]
        texture = struct.unpack(">L", data.read(4))[0]
        sound_id_2 = struct.unpack('>l', data.read(4))[0]
        particle_6 = struct.unpack(">L", data.read(4))[0]
        unknown_12 = struct.unpack('>?', data.read(1))[0]
        unknown_13 = struct.unpack('>?', data.read(1))[0]
        return cls(name, position, rotation, scale, unnamed_0x00000004, unnamed_0x00000005, unknown_1, unknown_2, unknown_3, unknown_4, damage_vulnerability_1, damage_vulnerability_2, damage_vulnerability_3, wpsc_1, damage_info_1, unknown_5, unknown_6, wpsc_2, particle_1, damage_info_2, particle_2, particle_3, particle_4, particle_5, elsc, unknown_7, unknown_8, damage_info_3, sound_id_1, unknown_9, unknown_10, unknown_11, texture, sound_id_2, particle_6, unknown_12, unknown_13)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00%')  # 37 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        self.rotation.to_stream(data)
        self.scale.to_stream(data)
        self.unnamed_0x00000004.to_stream(data)
        self.unnamed_0x00000005.to_stream(data)
        data.write(struct.pack('>f', self.unknown_1))
        data.write(struct.pack('>f', self.unknown_2))
        self.unknown_3.to_stream(data)
        data.write(struct.pack('>f', self.unknown_4))
        self.damage_vulnerability_1.to_stream(data)
        self.damage_vulnerability_2.to_stream(data)
        self.damage_vulnerability_3.to_stream(data)
        data.write(struct.pack(">L", self.wpsc_1))
        self.damage_info_1.to_stream(data)
        data.write(struct.pack('>f', self.unknown_5))
        data.write(struct.pack('>f', self.unknown_6))
        data.write(struct.pack(">L", self.wpsc_2))
        data.write(struct.pack(">L", self.particle_1))
        self.damage_info_2.to_stream(data)
        data.write(struct.pack(">L", self.particle_2))
        data.write(struct.pack(">L", self.particle_3))
        data.write(struct.pack(">L", self.particle_4))
        data.write(struct.pack(">L", self.particle_5))
        data.write(struct.pack(">L", self.elsc))
        data.write(struct.pack('>f', self.unknown_7))
        data.write(struct.pack('>f', self.unknown_8))
        self.damage_info_3.to_stream(data)
        data.write(struct.pack('>l', self.sound_id_1))
        data.write(struct.pack('>f', self.unknown_9))
        data.write(struct.pack('>f', self.unknown_10))
        data.write(struct.pack('>f', self.unknown_11))
        data.write(struct.pack(">L", self.texture))
        data.write(struct.pack('>l', self.sound_id_2))
        data.write(struct.pack(">L", self.particle_6))
        data.write(struct.pack('>?', self.unknown_12))
        data.write(struct.pack('>?', self.unknown_13))

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
            unknown_3=Vector.from_json(data['unknown_3']),
            unknown_4=data['unknown_4'],
            damage_vulnerability_1=DamageVulnerability.from_json(data['damage_vulnerability_1']),
            damage_vulnerability_2=DamageVulnerability.from_json(data['damage_vulnerability_2']),
            damage_vulnerability_3=DamageVulnerability.from_json(data['damage_vulnerability_3']),
            wpsc_1=data['wpsc_1'],
            damage_info_1=DamageInfo.from_json(data['damage_info_1']),
            unknown_5=data['unknown_5'],
            unknown_6=data['unknown_6'],
            wpsc_2=data['wpsc_2'],
            particle_1=data['particle_1'],
            damage_info_2=DamageInfo.from_json(data['damage_info_2']),
            particle_2=data['particle_2'],
            particle_3=data['particle_3'],
            particle_4=data['particle_4'],
            particle_5=data['particle_5'],
            elsc=data['elsc'],
            unknown_7=data['unknown_7'],
            unknown_8=data['unknown_8'],
            damage_info_3=DamageInfo.from_json(data['damage_info_3']),
            sound_id_1=data['sound_id_1'],
            unknown_9=data['unknown_9'],
            unknown_10=data['unknown_10'],
            unknown_11=data['unknown_11'],
            texture=data['texture'],
            sound_id_2=data['sound_id_2'],
            particle_6=data['particle_6'],
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
            'unknown_3': self.unknown_3.to_json(),
            'unknown_4': self.unknown_4,
            'damage_vulnerability_1': self.damage_vulnerability_1.to_json(),
            'damage_vulnerability_2': self.damage_vulnerability_2.to_json(),
            'damage_vulnerability_3': self.damage_vulnerability_3.to_json(),
            'wpsc_1': self.wpsc_1,
            'damage_info_1': self.damage_info_1.to_json(),
            'unknown_5': self.unknown_5,
            'unknown_6': self.unknown_6,
            'wpsc_2': self.wpsc_2,
            'particle_1': self.particle_1,
            'damage_info_2': self.damage_info_2.to_json(),
            'particle_2': self.particle_2,
            'particle_3': self.particle_3,
            'particle_4': self.particle_4,
            'particle_5': self.particle_5,
            'elsc': self.elsc,
            'unknown_7': self.unknown_7,
            'unknown_8': self.unknown_8,
            'damage_info_3': self.damage_info_3.to_json(),
            'sound_id_1': self.sound_id_1,
            'unknown_9': self.unknown_9,
            'unknown_10': self.unknown_10,
            'unknown_11': self.unknown_11,
            'texture': self.texture,
            'sound_id_2': self.sound_id_2,
            'particle_6': self.particle_6,
            'unknown_12': self.unknown_12,
            'unknown_13': self.unknown_13,
        }

    def _dependencies_for_unnamed_0x00000004(self, asset_manager):
        yield from self.unnamed_0x00000004.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x00000005(self, asset_manager):
        yield from self.unnamed_0x00000005.dependencies_for(asset_manager)

    def _dependencies_for_damage_vulnerability_1(self, asset_manager):
        yield from self.damage_vulnerability_1.dependencies_for(asset_manager)

    def _dependencies_for_damage_vulnerability_2(self, asset_manager):
        yield from self.damage_vulnerability_2.dependencies_for(asset_manager)

    def _dependencies_for_damage_vulnerability_3(self, asset_manager):
        yield from self.damage_vulnerability_3.dependencies_for(asset_manager)

    def _dependencies_for_wpsc_1(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.wpsc_1)

    def _dependencies_for_damage_info_1(self, asset_manager):
        yield from self.damage_info_1.dependencies_for(asset_manager)

    def _dependencies_for_wpsc_2(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.wpsc_2)

    def _dependencies_for_particle_1(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle_1)

    def _dependencies_for_damage_info_2(self, asset_manager):
        yield from self.damage_info_2.dependencies_for(asset_manager)

    def _dependencies_for_particle_2(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle_2)

    def _dependencies_for_particle_3(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle_3)

    def _dependencies_for_particle_4(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle_4)

    def _dependencies_for_particle_5(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle_5)

    def _dependencies_for_elsc(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.elsc)

    def _dependencies_for_damage_info_3(self, asset_manager):
        yield from self.damage_info_3.dependencies_for(asset_manager)

    def _dependencies_for_sound_id_1(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_id_1)

    def _dependencies_for_texture(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.texture)

    def _dependencies_for_sound_id_2(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_id_2)

    def _dependencies_for_particle_6(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle_6)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_unnamed_0x00000004, "unnamed_0x00000004", "PatternedAITypedef"),
            (self._dependencies_for_unnamed_0x00000005, "unnamed_0x00000005", "ActorParameters"),
            (self._dependencies_for_damage_vulnerability_1, "damage_vulnerability_1", "DamageVulnerability"),
            (self._dependencies_for_damage_vulnerability_2, "damage_vulnerability_2", "DamageVulnerability"),
            (self._dependencies_for_damage_vulnerability_3, "damage_vulnerability_3", "DamageVulnerability"),
            (self._dependencies_for_wpsc_1, "wpsc_1", "AssetId"),
            (self._dependencies_for_damage_info_1, "damage_info_1", "DamageInfo"),
            (self._dependencies_for_wpsc_2, "wpsc_2", "AssetId"),
            (self._dependencies_for_particle_1, "particle_1", "AssetId"),
            (self._dependencies_for_damage_info_2, "damage_info_2", "DamageInfo"),
            (self._dependencies_for_particle_2, "particle_2", "AssetId"),
            (self._dependencies_for_particle_3, "particle_3", "AssetId"),
            (self._dependencies_for_particle_4, "particle_4", "AssetId"),
            (self._dependencies_for_particle_5, "particle_5", "AssetId"),
            (self._dependencies_for_elsc, "elsc", "AssetId"),
            (self._dependencies_for_damage_info_3, "damage_info_3", "DamageInfo"),
            (self._dependencies_for_sound_id_1, "sound_id_1", "int"),
            (self._dependencies_for_texture, "texture", "AssetId"),
            (self._dependencies_for_sound_id_2, "sound_id_2", "int"),
            (self._dependencies_for_particle_6, "particle_6", "AssetId"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for IceSheegoth.{field_name} ({field_type}): {e}"
                )
