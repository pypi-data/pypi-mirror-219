# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.prime.archetypes.ScriptBeamStruct import ScriptBeamStruct
from retro_data_structures.properties.prime.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class ScriptBeam(BaseObjectType):
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    rotation: Vector = dataclasses.field(default_factory=Vector)
    unknown_1: bool = dataclasses.field(default=False)
    wpsc: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    unnamed_0x00000005: ScriptBeamStruct = dataclasses.field(default_factory=ScriptBeamStruct)
    unnamed_0x00000006: DamageInfo = dataclasses.field(default_factory=DamageInfo)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x81

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        position = Vector.from_stream(data)
        rotation = Vector.from_stream(data)
        unknown_1 = struct.unpack('>?', data.read(1))[0]
        wpsc = struct.unpack(">L", data.read(4))[0]
        unnamed_0x00000005 = ScriptBeamStruct.from_stream(data, property_size)
        unnamed_0x00000006 = DamageInfo.from_stream(data, property_size)
        return cls(name, position, rotation, unknown_1, wpsc, unnamed_0x00000005, unnamed_0x00000006)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x07')  # 7 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        self.rotation.to_stream(data)
        data.write(struct.pack('>?', self.unknown_1))
        data.write(struct.pack(">L", self.wpsc))
        self.unnamed_0x00000005.to_stream(data)
        self.unnamed_0x00000006.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            position=Vector.from_json(data['position']),
            rotation=Vector.from_json(data['rotation']),
            unknown_1=data['unknown_1'],
            wpsc=data['wpsc'],
            unnamed_0x00000005=ScriptBeamStruct.from_json(data['unnamed_0x00000005']),
            unnamed_0x00000006=DamageInfo.from_json(data['unnamed_0x00000006']),
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'position': self.position.to_json(),
            'rotation': self.rotation.to_json(),
            'unknown_1': self.unknown_1,
            'wpsc': self.wpsc,
            'unnamed_0x00000005': self.unnamed_0x00000005.to_json(),
            'unnamed_0x00000006': self.unnamed_0x00000006.to_json(),
        }

    def _dependencies_for_wpsc(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.wpsc)

    def _dependencies_for_unnamed_0x00000005(self, asset_manager):
        yield from self.unnamed_0x00000005.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x00000006(self, asset_manager):
        yield from self.unnamed_0x00000006.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_wpsc, "wpsc", "AssetId"),
            (self._dependencies_for_unnamed_0x00000005, "unnamed_0x00000005", "ScriptBeamStruct"),
            (self._dependencies_for_unnamed_0x00000006, "unnamed_0x00000006", "DamageInfo"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for ScriptBeam.{field_name} ({field_type}): {e}"
                )
