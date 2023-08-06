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
class Beetle(BaseObjectType):
    name: str = dataclasses.field(default='')
    unknown_1: int = dataclasses.field(default=0)
    position: Vector = dataclasses.field(default_factory=Vector)
    rotation: Vector = dataclasses.field(default_factory=Vector)
    scale: Vector = dataclasses.field(default_factory=Vector)
    unnamed_0x00000005: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    unnamed_0x00000006: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    unnamed_0x00000007: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    orbit_offset: Vector = dataclasses.field(default_factory=Vector)
    unknown_3: float = dataclasses.field(default=0.0)
    abdomen_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    armor_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    abdomen_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    unknown_4: int = dataclasses.field(default=0)
    unknown_5: float = dataclasses.field(default=0.0)
    unknown_6: float = dataclasses.field(default=0.0)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x16

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
        unnamed_0x00000007 = DamageInfo.from_stream(data, property_size)
        orbit_offset = Vector.from_stream(data)
        unknown_3 = struct.unpack('>f', data.read(4))[0]
        abdomen_vulnerability = DamageVulnerability.from_stream(data, property_size)
        armor_vulnerability = DamageVulnerability.from_stream(data, property_size)
        abdomen_model = struct.unpack(">L", data.read(4))[0]
        unknown_4 = struct.unpack('>l', data.read(4))[0]
        unknown_5 = struct.unpack('>f', data.read(4))[0]
        unknown_6 = struct.unpack('>f', data.read(4))[0]
        return cls(name, unknown_1, position, rotation, scale, unnamed_0x00000005, unnamed_0x00000006, unnamed_0x00000007, orbit_offset, unknown_3, abdomen_vulnerability, armor_vulnerability, abdomen_model, unknown_4, unknown_5, unknown_6)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x10')  # 16 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        data.write(struct.pack('>l', self.unknown_1))
        self.position.to_stream(data)
        self.rotation.to_stream(data)
        self.scale.to_stream(data)
        self.unnamed_0x00000005.to_stream(data)
        self.unnamed_0x00000006.to_stream(data)
        self.unnamed_0x00000007.to_stream(data)
        self.orbit_offset.to_stream(data)
        data.write(struct.pack('>f', self.unknown_3))
        self.abdomen_vulnerability.to_stream(data)
        self.armor_vulnerability.to_stream(data)
        data.write(struct.pack(">L", self.abdomen_model))
        data.write(struct.pack('>l', self.unknown_4))
        data.write(struct.pack('>f', self.unknown_5))
        data.write(struct.pack('>f', self.unknown_6))

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
            unnamed_0x00000007=DamageInfo.from_json(data['unnamed_0x00000007']),
            orbit_offset=Vector.from_json(data['orbit_offset']),
            unknown_3=data['unknown_3'],
            abdomen_vulnerability=DamageVulnerability.from_json(data['abdomen_vulnerability']),
            armor_vulnerability=DamageVulnerability.from_json(data['armor_vulnerability']),
            abdomen_model=data['abdomen_model'],
            unknown_4=data['unknown_4'],
            unknown_5=data['unknown_5'],
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
            'unnamed_0x00000007': self.unnamed_0x00000007.to_json(),
            'orbit_offset': self.orbit_offset.to_json(),
            'unknown_3': self.unknown_3,
            'abdomen_vulnerability': self.abdomen_vulnerability.to_json(),
            'armor_vulnerability': self.armor_vulnerability.to_json(),
            'abdomen_model': self.abdomen_model,
            'unknown_4': self.unknown_4,
            'unknown_5': self.unknown_5,
            'unknown_6': self.unknown_6,
        }

    def _dependencies_for_unnamed_0x00000005(self, asset_manager):
        yield from self.unnamed_0x00000005.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x00000006(self, asset_manager):
        yield from self.unnamed_0x00000006.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x00000007(self, asset_manager):
        yield from self.unnamed_0x00000007.dependencies_for(asset_manager)

    def _dependencies_for_abdomen_vulnerability(self, asset_manager):
        yield from self.abdomen_vulnerability.dependencies_for(asset_manager)

    def _dependencies_for_armor_vulnerability(self, asset_manager):
        yield from self.armor_vulnerability.dependencies_for(asset_manager)

    def _dependencies_for_abdomen_model(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.abdomen_model)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_unnamed_0x00000005, "unnamed_0x00000005", "PatternedAITypedef"),
            (self._dependencies_for_unnamed_0x00000006, "unnamed_0x00000006", "ActorParameters"),
            (self._dependencies_for_unnamed_0x00000007, "unnamed_0x00000007", "DamageInfo"),
            (self._dependencies_for_abdomen_vulnerability, "abdomen_vulnerability", "DamageVulnerability"),
            (self._dependencies_for_armor_vulnerability, "armor_vulnerability", "DamageVulnerability"),
            (self._dependencies_for_abdomen_model, "abdomen_model", "AssetId"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for Beetle.{field_name} ({field_type}): {e}"
                )
