# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.archetypes.BoolFloat import BoolFloat
from retro_data_structures.properties.prime.archetypes.BoolVec3f import BoolVec3f
from retro_data_structures.properties.prime.archetypes.CameraHintStruct import CameraHintStruct
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class CameraHint(BaseObjectType):
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    rotation: Vector = dataclasses.field(default_factory=Vector)
    unknown_1: bool = dataclasses.field(default=False)
    unknown_2: int = dataclasses.field(default=0)
    unknown_3: int = dataclasses.field(default=0)
    unnamed_0x00000006: CameraHintStruct = dataclasses.field(default_factory=CameraHintStruct)
    unnamed_0x00000007: BoolFloat = dataclasses.field(default_factory=BoolFloat)
    unnamed_0x00000008: BoolFloat = dataclasses.field(default_factory=BoolFloat)
    unnamed_0x00000009: BoolFloat = dataclasses.field(default_factory=BoolFloat)
    unnamed_0x0000000a: BoolVec3f = dataclasses.field(default_factory=BoolVec3f)
    unnamed_0x0000000b: BoolVec3f = dataclasses.field(default_factory=BoolVec3f)
    unknown_36: Vector = dataclasses.field(default_factory=Vector)
    unnamed_0x0000000d: BoolFloat = dataclasses.field(default_factory=BoolFloat)
    unnamed_0x0000000e: BoolFloat = dataclasses.field(default_factory=BoolFloat)
    unnamed_0x0000000f: BoolFloat = dataclasses.field(default_factory=BoolFloat)
    unnamed_0x00000010: BoolFloat = dataclasses.field(default_factory=BoolFloat)
    unknown_45: float = dataclasses.field(default=0.0)
    unknown_46: float = dataclasses.field(default=0.0)
    unnamed_0x00000013: BoolFloat = dataclasses.field(default_factory=BoolFloat)
    unknown_49: float = dataclasses.field(default=0.0)
    unknown_50: float = dataclasses.field(default=0.0)
    unknown_51: float = dataclasses.field(default=0.0)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x10

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        position = Vector.from_stream(data)
        rotation = Vector.from_stream(data)
        unknown_1 = struct.unpack('>?', data.read(1))[0]
        unknown_2 = struct.unpack('>l', data.read(4))[0]
        unknown_3 = struct.unpack('>l', data.read(4))[0]
        unnamed_0x00000006 = CameraHintStruct.from_stream(data, property_size)
        unnamed_0x00000007 = BoolFloat.from_stream(data, property_size)
        unnamed_0x00000008 = BoolFloat.from_stream(data, property_size)
        unnamed_0x00000009 = BoolFloat.from_stream(data, property_size)
        unnamed_0x0000000a = BoolVec3f.from_stream(data, property_size)
        unnamed_0x0000000b = BoolVec3f.from_stream(data, property_size)
        unknown_36 = Vector.from_stream(data)
        unnamed_0x0000000d = BoolFloat.from_stream(data, property_size)
        unnamed_0x0000000e = BoolFloat.from_stream(data, property_size)
        unnamed_0x0000000f = BoolFloat.from_stream(data, property_size)
        unnamed_0x00000010 = BoolFloat.from_stream(data, property_size)
        unknown_45 = struct.unpack('>f', data.read(4))[0]
        unknown_46 = struct.unpack('>f', data.read(4))[0]
        unnamed_0x00000013 = BoolFloat.from_stream(data, property_size)
        unknown_49 = struct.unpack('>f', data.read(4))[0]
        unknown_50 = struct.unpack('>f', data.read(4))[0]
        unknown_51 = struct.unpack('>f', data.read(4))[0]
        return cls(name, position, rotation, unknown_1, unknown_2, unknown_3, unnamed_0x00000006, unnamed_0x00000007, unnamed_0x00000008, unnamed_0x00000009, unnamed_0x0000000a, unnamed_0x0000000b, unknown_36, unnamed_0x0000000d, unnamed_0x0000000e, unnamed_0x0000000f, unnamed_0x00000010, unknown_45, unknown_46, unnamed_0x00000013, unknown_49, unknown_50, unknown_51)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x17')  # 23 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        self.rotation.to_stream(data)
        data.write(struct.pack('>?', self.unknown_1))
        data.write(struct.pack('>l', self.unknown_2))
        data.write(struct.pack('>l', self.unknown_3))
        self.unnamed_0x00000006.to_stream(data)
        self.unnamed_0x00000007.to_stream(data)
        self.unnamed_0x00000008.to_stream(data)
        self.unnamed_0x00000009.to_stream(data)
        self.unnamed_0x0000000a.to_stream(data)
        self.unnamed_0x0000000b.to_stream(data)
        self.unknown_36.to_stream(data)
        self.unnamed_0x0000000d.to_stream(data)
        self.unnamed_0x0000000e.to_stream(data)
        self.unnamed_0x0000000f.to_stream(data)
        self.unnamed_0x00000010.to_stream(data)
        data.write(struct.pack('>f', self.unknown_45))
        data.write(struct.pack('>f', self.unknown_46))
        self.unnamed_0x00000013.to_stream(data)
        data.write(struct.pack('>f', self.unknown_49))
        data.write(struct.pack('>f', self.unknown_50))
        data.write(struct.pack('>f', self.unknown_51))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            position=Vector.from_json(data['position']),
            rotation=Vector.from_json(data['rotation']),
            unknown_1=data['unknown_1'],
            unknown_2=data['unknown_2'],
            unknown_3=data['unknown_3'],
            unnamed_0x00000006=CameraHintStruct.from_json(data['unnamed_0x00000006']),
            unnamed_0x00000007=BoolFloat.from_json(data['unnamed_0x00000007']),
            unnamed_0x00000008=BoolFloat.from_json(data['unnamed_0x00000008']),
            unnamed_0x00000009=BoolFloat.from_json(data['unnamed_0x00000009']),
            unnamed_0x0000000a=BoolVec3f.from_json(data['unnamed_0x0000000a']),
            unnamed_0x0000000b=BoolVec3f.from_json(data['unnamed_0x0000000b']),
            unknown_36=Vector.from_json(data['unknown_36']),
            unnamed_0x0000000d=BoolFloat.from_json(data['unnamed_0x0000000d']),
            unnamed_0x0000000e=BoolFloat.from_json(data['unnamed_0x0000000e']),
            unnamed_0x0000000f=BoolFloat.from_json(data['unnamed_0x0000000f']),
            unnamed_0x00000010=BoolFloat.from_json(data['unnamed_0x00000010']),
            unknown_45=data['unknown_45'],
            unknown_46=data['unknown_46'],
            unnamed_0x00000013=BoolFloat.from_json(data['unnamed_0x00000013']),
            unknown_49=data['unknown_49'],
            unknown_50=data['unknown_50'],
            unknown_51=data['unknown_51'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'position': self.position.to_json(),
            'rotation': self.rotation.to_json(),
            'unknown_1': self.unknown_1,
            'unknown_2': self.unknown_2,
            'unknown_3': self.unknown_3,
            'unnamed_0x00000006': self.unnamed_0x00000006.to_json(),
            'unnamed_0x00000007': self.unnamed_0x00000007.to_json(),
            'unnamed_0x00000008': self.unnamed_0x00000008.to_json(),
            'unnamed_0x00000009': self.unnamed_0x00000009.to_json(),
            'unnamed_0x0000000a': self.unnamed_0x0000000a.to_json(),
            'unnamed_0x0000000b': self.unnamed_0x0000000b.to_json(),
            'unknown_36': self.unknown_36.to_json(),
            'unnamed_0x0000000d': self.unnamed_0x0000000d.to_json(),
            'unnamed_0x0000000e': self.unnamed_0x0000000e.to_json(),
            'unnamed_0x0000000f': self.unnamed_0x0000000f.to_json(),
            'unnamed_0x00000010': self.unnamed_0x00000010.to_json(),
            'unknown_45': self.unknown_45,
            'unknown_46': self.unknown_46,
            'unnamed_0x00000013': self.unnamed_0x00000013.to_json(),
            'unknown_49': self.unknown_49,
            'unknown_50': self.unknown_50,
            'unknown_51': self.unknown_51,
        }

    def _dependencies_for_unnamed_0x00000006(self, asset_manager):
        yield from self.unnamed_0x00000006.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x00000007(self, asset_manager):
        yield from self.unnamed_0x00000007.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x00000008(self, asset_manager):
        yield from self.unnamed_0x00000008.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x00000009(self, asset_manager):
        yield from self.unnamed_0x00000009.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x0000000a(self, asset_manager):
        yield from self.unnamed_0x0000000a.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x0000000b(self, asset_manager):
        yield from self.unnamed_0x0000000b.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x0000000d(self, asset_manager):
        yield from self.unnamed_0x0000000d.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x0000000e(self, asset_manager):
        yield from self.unnamed_0x0000000e.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x0000000f(self, asset_manager):
        yield from self.unnamed_0x0000000f.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x00000010(self, asset_manager):
        yield from self.unnamed_0x00000010.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x00000013(self, asset_manager):
        yield from self.unnamed_0x00000013.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_unnamed_0x00000006, "unnamed_0x00000006", "CameraHintStruct"),
            (self._dependencies_for_unnamed_0x00000007, "unnamed_0x00000007", "BoolFloat"),
            (self._dependencies_for_unnamed_0x00000008, "unnamed_0x00000008", "BoolFloat"),
            (self._dependencies_for_unnamed_0x00000009, "unnamed_0x00000009", "BoolFloat"),
            (self._dependencies_for_unnamed_0x0000000a, "unnamed_0x0000000a", "BoolVec3f"),
            (self._dependencies_for_unnamed_0x0000000b, "unnamed_0x0000000b", "BoolVec3f"),
            (self._dependencies_for_unnamed_0x0000000d, "unnamed_0x0000000d", "BoolFloat"),
            (self._dependencies_for_unnamed_0x0000000e, "unnamed_0x0000000e", "BoolFloat"),
            (self._dependencies_for_unnamed_0x0000000f, "unnamed_0x0000000f", "BoolFloat"),
            (self._dependencies_for_unnamed_0x00000010, "unnamed_0x00000010", "BoolFloat"),
            (self._dependencies_for_unnamed_0x00000013, "unnamed_0x00000013", "BoolFloat"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for CameraHint.{field_name} ({field_type}): {e}"
                )
