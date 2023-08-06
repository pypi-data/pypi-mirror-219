# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class MazeNode(BaseObjectType):
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    rotation: Vector = dataclasses.field(default_factory=Vector)
    unknown_1: bool = dataclasses.field(default=False)
    unknown_2: int = dataclasses.field(default=0)
    unknown_3: int = dataclasses.field(default=0)
    unknown_4: int = dataclasses.field(default=0)
    unknown_5: Vector = dataclasses.field(default_factory=Vector)
    unknown_6: Vector = dataclasses.field(default_factory=Vector)
    unknown_7: Vector = dataclasses.field(default_factory=Vector)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x85

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
        unknown_4 = struct.unpack('>l', data.read(4))[0]
        unknown_5 = Vector.from_stream(data)
        unknown_6 = Vector.from_stream(data)
        unknown_7 = Vector.from_stream(data)
        return cls(name, position, rotation, unknown_1, unknown_2, unknown_3, unknown_4, unknown_5, unknown_6, unknown_7)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\n')  # 10 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        self.rotation.to_stream(data)
        data.write(struct.pack('>?', self.unknown_1))
        data.write(struct.pack('>l', self.unknown_2))
        data.write(struct.pack('>l', self.unknown_3))
        data.write(struct.pack('>l', self.unknown_4))
        self.unknown_5.to_stream(data)
        self.unknown_6.to_stream(data)
        self.unknown_7.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            position=Vector.from_json(data['position']),
            rotation=Vector.from_json(data['rotation']),
            unknown_1=data['unknown_1'],
            unknown_2=data['unknown_2'],
            unknown_3=data['unknown_3'],
            unknown_4=data['unknown_4'],
            unknown_5=Vector.from_json(data['unknown_5']),
            unknown_6=Vector.from_json(data['unknown_6']),
            unknown_7=Vector.from_json(data['unknown_7']),
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'position': self.position.to_json(),
            'rotation': self.rotation.to_json(),
            'unknown_1': self.unknown_1,
            'unknown_2': self.unknown_2,
            'unknown_3': self.unknown_3,
            'unknown_4': self.unknown_4,
            'unknown_5': self.unknown_5.to_json(),
            'unknown_6': self.unknown_6.to_json(),
            'unknown_7': self.unknown_7.to_json(),
        }

    def dependencies_for(self, asset_manager):
        yield from []
