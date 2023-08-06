# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.archetypes.PathCameraStruct import PathCameraStruct
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class PathCamera(BaseObjectType):
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    rotation: Vector = dataclasses.field(default_factory=Vector)
    unknown_1: bool = dataclasses.field(default=False)
    unnamed: PathCameraStruct = dataclasses.field(default_factory=PathCameraStruct)
    unknown_8: float = dataclasses.field(default=0.0)
    unknown_9: float = dataclasses.field(default=0.0)
    unknown_10: float = dataclasses.field(default=0.0)
    unknown_11: int = dataclasses.field(default=0)
    unknown_12: float = dataclasses.field(default=0.0)
    unknown_13: float = dataclasses.field(default=0.0)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x2F

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        position = Vector.from_stream(data)
        rotation = Vector.from_stream(data)
        unknown_1 = struct.unpack('>?', data.read(1))[0]
        unnamed = PathCameraStruct.from_stream(data, property_size)
        unknown_8 = struct.unpack('>f', data.read(4))[0]
        unknown_9 = struct.unpack('>f', data.read(4))[0]
        unknown_10 = struct.unpack('>f', data.read(4))[0]
        unknown_11 = struct.unpack('>l', data.read(4))[0]
        unknown_12 = struct.unpack('>f', data.read(4))[0]
        unknown_13 = struct.unpack('>f', data.read(4))[0]
        return cls(name, position, rotation, unknown_1, unnamed, unknown_8, unknown_9, unknown_10, unknown_11, unknown_12, unknown_13)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x0b')  # 11 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        self.rotation.to_stream(data)
        data.write(struct.pack('>?', self.unknown_1))
        self.unnamed.to_stream(data)
        data.write(struct.pack('>f', self.unknown_8))
        data.write(struct.pack('>f', self.unknown_9))
        data.write(struct.pack('>f', self.unknown_10))
        data.write(struct.pack('>l', self.unknown_11))
        data.write(struct.pack('>f', self.unknown_12))
        data.write(struct.pack('>f', self.unknown_13))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            position=Vector.from_json(data['position']),
            rotation=Vector.from_json(data['rotation']),
            unknown_1=data['unknown_1'],
            unnamed=PathCameraStruct.from_json(data['unnamed']),
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
            'unknown_1': self.unknown_1,
            'unnamed': self.unnamed.to_json(),
            'unknown_8': self.unknown_8,
            'unknown_9': self.unknown_9,
            'unknown_10': self.unknown_10,
            'unknown_11': self.unknown_11,
            'unknown_12': self.unknown_12,
            'unknown_13': self.unknown_13,
        }

    def _dependencies_for_unnamed(self, asset_manager):
        yield from self.unnamed.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_unnamed, "unnamed", "PathCameraStruct"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for PathCamera.{field_name} ({field_type}): {e}"
                )
