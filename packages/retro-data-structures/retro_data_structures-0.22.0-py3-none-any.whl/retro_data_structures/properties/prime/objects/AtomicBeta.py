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
class AtomicBeta(BaseObjectType):
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    rotation: Vector = dataclasses.field(default_factory=Vector)
    scale: Vector = dataclasses.field(default_factory=Vector)
    unnamed_0x00000004: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    unnamed_0x00000005: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    elsc: AssetId = dataclasses.field(metadata={'asset_types': ['ELSC']}, default=default_asset_id)
    wpsc: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    unnamed_0x00000008: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    particle: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    unknown_1: float = dataclasses.field(default=0.0)
    unknown_2: float = dataclasses.field(default=0.0)
    unknown_3: float = dataclasses.field(default=0.0)
    unnamed_0x0000000d: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    unknown_4: float = dataclasses.field(default=0.0)
    unknown_5: float = dataclasses.field(default=0.0)
    unknown_6: float = dataclasses.field(default=0.0)
    unknown_7: int = dataclasses.field(default=0, metadata={'sound': True})
    unknown_8: int = dataclasses.field(default=0, metadata={'sound': True})
    unknown_9: int = dataclasses.field(default=0, metadata={'sound': True})
    unknown_10: float = dataclasses.field(default=0.0)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x77

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
        elsc = struct.unpack(">L", data.read(4))[0]
        wpsc = struct.unpack(">L", data.read(4))[0]
        unnamed_0x00000008 = DamageInfo.from_stream(data, property_size)
        particle = struct.unpack(">L", data.read(4))[0]
        unknown_1 = struct.unpack('>f', data.read(4))[0]
        unknown_2 = struct.unpack('>f', data.read(4))[0]
        unknown_3 = struct.unpack('>f', data.read(4))[0]
        unnamed_0x0000000d = DamageVulnerability.from_stream(data, property_size)
        unknown_4 = struct.unpack('>f', data.read(4))[0]
        unknown_5 = struct.unpack('>f', data.read(4))[0]
        unknown_6 = struct.unpack('>f', data.read(4))[0]
        unknown_7 = struct.unpack('>l', data.read(4))[0]
        unknown_8 = struct.unpack('>l', data.read(4))[0]
        unknown_9 = struct.unpack('>l', data.read(4))[0]
        unknown_10 = struct.unpack('>f', data.read(4))[0]
        return cls(name, position, rotation, scale, unnamed_0x00000004, unnamed_0x00000005, elsc, wpsc, unnamed_0x00000008, particle, unknown_1, unknown_2, unknown_3, unnamed_0x0000000d, unknown_4, unknown_5, unknown_6, unknown_7, unknown_8, unknown_9, unknown_10)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x15')  # 21 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        self.rotation.to_stream(data)
        self.scale.to_stream(data)
        self.unnamed_0x00000004.to_stream(data)
        self.unnamed_0x00000005.to_stream(data)
        data.write(struct.pack(">L", self.elsc))
        data.write(struct.pack(">L", self.wpsc))
        self.unnamed_0x00000008.to_stream(data)
        data.write(struct.pack(">L", self.particle))
        data.write(struct.pack('>f', self.unknown_1))
        data.write(struct.pack('>f', self.unknown_2))
        data.write(struct.pack('>f', self.unknown_3))
        self.unnamed_0x0000000d.to_stream(data)
        data.write(struct.pack('>f', self.unknown_4))
        data.write(struct.pack('>f', self.unknown_5))
        data.write(struct.pack('>f', self.unknown_6))
        data.write(struct.pack('>l', self.unknown_7))
        data.write(struct.pack('>l', self.unknown_8))
        data.write(struct.pack('>l', self.unknown_9))
        data.write(struct.pack('>f', self.unknown_10))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            position=Vector.from_json(data['position']),
            rotation=Vector.from_json(data['rotation']),
            scale=Vector.from_json(data['scale']),
            unnamed_0x00000004=PatternedAITypedef.from_json(data['unnamed_0x00000004']),
            unnamed_0x00000005=ActorParameters.from_json(data['unnamed_0x00000005']),
            elsc=data['elsc'],
            wpsc=data['wpsc'],
            unnamed_0x00000008=DamageInfo.from_json(data['unnamed_0x00000008']),
            particle=data['particle'],
            unknown_1=data['unknown_1'],
            unknown_2=data['unknown_2'],
            unknown_3=data['unknown_3'],
            unnamed_0x0000000d=DamageVulnerability.from_json(data['unnamed_0x0000000d']),
            unknown_4=data['unknown_4'],
            unknown_5=data['unknown_5'],
            unknown_6=data['unknown_6'],
            unknown_7=data['unknown_7'],
            unknown_8=data['unknown_8'],
            unknown_9=data['unknown_9'],
            unknown_10=data['unknown_10'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'position': self.position.to_json(),
            'rotation': self.rotation.to_json(),
            'scale': self.scale.to_json(),
            'unnamed_0x00000004': self.unnamed_0x00000004.to_json(),
            'unnamed_0x00000005': self.unnamed_0x00000005.to_json(),
            'elsc': self.elsc,
            'wpsc': self.wpsc,
            'unnamed_0x00000008': self.unnamed_0x00000008.to_json(),
            'particle': self.particle,
            'unknown_1': self.unknown_1,
            'unknown_2': self.unknown_2,
            'unknown_3': self.unknown_3,
            'unnamed_0x0000000d': self.unnamed_0x0000000d.to_json(),
            'unknown_4': self.unknown_4,
            'unknown_5': self.unknown_5,
            'unknown_6': self.unknown_6,
            'unknown_7': self.unknown_7,
            'unknown_8': self.unknown_8,
            'unknown_9': self.unknown_9,
            'unknown_10': self.unknown_10,
        }

    def _dependencies_for_unnamed_0x00000004(self, asset_manager):
        yield from self.unnamed_0x00000004.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x00000005(self, asset_manager):
        yield from self.unnamed_0x00000005.dependencies_for(asset_manager)

    def _dependencies_for_elsc(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.elsc)

    def _dependencies_for_wpsc(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.wpsc)

    def _dependencies_for_unnamed_0x00000008(self, asset_manager):
        yield from self.unnamed_0x00000008.dependencies_for(asset_manager)

    def _dependencies_for_particle(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle)

    def _dependencies_for_unnamed_0x0000000d(self, asset_manager):
        yield from self.unnamed_0x0000000d.dependencies_for(asset_manager)

    def _dependencies_for_unknown_7(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.unknown_7)

    def _dependencies_for_unknown_8(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.unknown_8)

    def _dependencies_for_unknown_9(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.unknown_9)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_unnamed_0x00000004, "unnamed_0x00000004", "PatternedAITypedef"),
            (self._dependencies_for_unnamed_0x00000005, "unnamed_0x00000005", "ActorParameters"),
            (self._dependencies_for_elsc, "elsc", "AssetId"),
            (self._dependencies_for_wpsc, "wpsc", "AssetId"),
            (self._dependencies_for_unnamed_0x00000008, "unnamed_0x00000008", "DamageInfo"),
            (self._dependencies_for_particle, "particle", "AssetId"),
            (self._dependencies_for_unnamed_0x0000000d, "unnamed_0x0000000d", "DamageVulnerability"),
            (self._dependencies_for_unknown_7, "unknown_7", "int"),
            (self._dependencies_for_unknown_8, "unknown_8", "int"),
            (self._dependencies_for_unknown_9, "unknown_9", "int"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for AtomicBeta.{field_name} ({field_type}): {e}"
                )
