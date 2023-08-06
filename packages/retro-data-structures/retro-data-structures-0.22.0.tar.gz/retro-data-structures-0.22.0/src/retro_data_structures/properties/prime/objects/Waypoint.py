# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class Waypoint(BaseObjectType):
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    rotation: Vector = dataclasses.field(default_factory=Vector)
    active: bool = dataclasses.field(default=False)
    unknown_2: float = dataclasses.field(default=0.0)
    delay: float = dataclasses.field(default=0.0)
    unknown_4: int = dataclasses.field(default=0)
    unknown_5: int = dataclasses.field(default=0)
    unknown_6: int = dataclasses.field(default=0)
    unknown_7: int = dataclasses.field(default=0)
    unknown_8: int = dataclasses.field(default=0)
    unknown_9: int = dataclasses.field(default=0)
    unknown_10: int = dataclasses.field(default=0)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x2

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        position = Vector.from_stream(data)
        rotation = Vector.from_stream(data)
        active = struct.unpack('>?', data.read(1))[0]
        unknown_2 = struct.unpack('>f', data.read(4))[0]
        delay = struct.unpack('>f', data.read(4))[0]
        unknown_4 = struct.unpack('>l', data.read(4))[0]
        unknown_5 = struct.unpack('>l', data.read(4))[0]
        unknown_6 = struct.unpack('>l', data.read(4))[0]
        unknown_7 = struct.unpack('>l', data.read(4))[0]
        unknown_8 = struct.unpack('>l', data.read(4))[0]
        unknown_9 = struct.unpack('>l', data.read(4))[0]
        unknown_10 = struct.unpack('>l', data.read(4))[0]
        return cls(name, position, rotation, active, unknown_2, delay, unknown_4, unknown_5, unknown_6, unknown_7, unknown_8, unknown_9, unknown_10)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\r')  # 13 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        self.rotation.to_stream(data)
        data.write(struct.pack('>?', self.active))
        data.write(struct.pack('>f', self.unknown_2))
        data.write(struct.pack('>f', self.delay))
        data.write(struct.pack('>l', self.unknown_4))
        data.write(struct.pack('>l', self.unknown_5))
        data.write(struct.pack('>l', self.unknown_6))
        data.write(struct.pack('>l', self.unknown_7))
        data.write(struct.pack('>l', self.unknown_8))
        data.write(struct.pack('>l', self.unknown_9))
        data.write(struct.pack('>l', self.unknown_10))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            position=Vector.from_json(data['position']),
            rotation=Vector.from_json(data['rotation']),
            active=data['active'],
            unknown_2=data['unknown_2'],
            delay=data['delay'],
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
            'active': self.active,
            'unknown_2': self.unknown_2,
            'delay': self.delay,
            'unknown_4': self.unknown_4,
            'unknown_5': self.unknown_5,
            'unknown_6': self.unknown_6,
            'unknown_7': self.unknown_7,
            'unknown_8': self.unknown_8,
            'unknown_9': self.unknown_9,
            'unknown_10': self.unknown_10,
        }

    def dependencies_for(self, asset_manager):
        yield from []
