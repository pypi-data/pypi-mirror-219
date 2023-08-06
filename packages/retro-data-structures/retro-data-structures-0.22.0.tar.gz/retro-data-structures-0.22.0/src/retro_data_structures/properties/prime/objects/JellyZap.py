# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.prime.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.prime.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class JellyZap(BaseObjectType):
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    rotation: Vector = dataclasses.field(default_factory=Vector)
    scale: Vector = dataclasses.field(default_factory=Vector)
    unnamed_0x00000004: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    unnamed_0x00000005: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    unnamed_0x00000006: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_1: float = dataclasses.field(default=0.0)
    unknown_2: float = dataclasses.field(default=0.0)
    unknown_3: float = dataclasses.field(default=0.0)
    unknown_4: float = dataclasses.field(default=0.0)
    unknown_5: float = dataclasses.field(default=0.0)
    unknown_6: float = dataclasses.field(default=0.0)
    unknown_7: float = dataclasses.field(default=0.0)
    unknown_8: float = dataclasses.field(default=0.0)
    unknown_9: float = dataclasses.field(default=0.0)
    unknown_10: float = dataclasses.field(default=0.0)
    unknown_11: float = dataclasses.field(default=0.0)
    unknown_12: float = dataclasses.field(default=0.0)
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
        return 0x54

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
        unnamed_0x00000006 = DamageInfo.from_stream(data, property_size)
        unknown_1 = struct.unpack('>f', data.read(4))[0]
        unknown_2 = struct.unpack('>f', data.read(4))[0]
        unknown_3 = struct.unpack('>f', data.read(4))[0]
        unknown_4 = struct.unpack('>f', data.read(4))[0]
        unknown_5 = struct.unpack('>f', data.read(4))[0]
        unknown_6 = struct.unpack('>f', data.read(4))[0]
        unknown_7 = struct.unpack('>f', data.read(4))[0]
        unknown_8 = struct.unpack('>f', data.read(4))[0]
        unknown_9 = struct.unpack('>f', data.read(4))[0]
        unknown_10 = struct.unpack('>f', data.read(4))[0]
        unknown_11 = struct.unpack('>f', data.read(4))[0]
        unknown_12 = struct.unpack('>f', data.read(4))[0]
        unknown_13 = struct.unpack('>?', data.read(1))[0]
        return cls(name, position, rotation, scale, unnamed_0x00000004, unnamed_0x00000005, unnamed_0x00000006, unknown_1, unknown_2, unknown_3, unknown_4, unknown_5, unknown_6, unknown_7, unknown_8, unknown_9, unknown_10, unknown_11, unknown_12, unknown_13)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x14')  # 20 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        self.rotation.to_stream(data)
        self.scale.to_stream(data)
        self.unnamed_0x00000004.to_stream(data)
        self.unnamed_0x00000005.to_stream(data)
        self.unnamed_0x00000006.to_stream(data)
        data.write(struct.pack('>f', self.unknown_1))
        data.write(struct.pack('>f', self.unknown_2))
        data.write(struct.pack('>f', self.unknown_3))
        data.write(struct.pack('>f', self.unknown_4))
        data.write(struct.pack('>f', self.unknown_5))
        data.write(struct.pack('>f', self.unknown_6))
        data.write(struct.pack('>f', self.unknown_7))
        data.write(struct.pack('>f', self.unknown_8))
        data.write(struct.pack('>f', self.unknown_9))
        data.write(struct.pack('>f', self.unknown_10))
        data.write(struct.pack('>f', self.unknown_11))
        data.write(struct.pack('>f', self.unknown_12))
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
            unnamed_0x00000006=DamageInfo.from_json(data['unnamed_0x00000006']),
            unknown_1=data['unknown_1'],
            unknown_2=data['unknown_2'],
            unknown_3=data['unknown_3'],
            unknown_4=data['unknown_4'],
            unknown_5=data['unknown_5'],
            unknown_6=data['unknown_6'],
            unknown_7=data['unknown_7'],
            unknown_8=data['unknown_8'],
            unknown_9=data['unknown_9'],
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
            'unnamed_0x00000006': self.unnamed_0x00000006.to_json(),
            'unknown_1': self.unknown_1,
            'unknown_2': self.unknown_2,
            'unknown_3': self.unknown_3,
            'unknown_4': self.unknown_4,
            'unknown_5': self.unknown_5,
            'unknown_6': self.unknown_6,
            'unknown_7': self.unknown_7,
            'unknown_8': self.unknown_8,
            'unknown_9': self.unknown_9,
            'unknown_10': self.unknown_10,
            'unknown_11': self.unknown_11,
            'unknown_12': self.unknown_12,
            'unknown_13': self.unknown_13,
        }

    def _dependencies_for_unnamed_0x00000004(self, asset_manager):
        yield from self.unnamed_0x00000004.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x00000005(self, asset_manager):
        yield from self.unnamed_0x00000005.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x00000006(self, asset_manager):
        yield from self.unnamed_0x00000006.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_unnamed_0x00000004, "unnamed_0x00000004", "PatternedAITypedef"),
            (self._dependencies_for_unnamed_0x00000005, "unnamed_0x00000005", "ActorParameters"),
            (self._dependencies_for_unnamed_0x00000006, "unnamed_0x00000006", "DamageInfo"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for JellyZap.{field_name} ({field_type}): {e}"
                )
