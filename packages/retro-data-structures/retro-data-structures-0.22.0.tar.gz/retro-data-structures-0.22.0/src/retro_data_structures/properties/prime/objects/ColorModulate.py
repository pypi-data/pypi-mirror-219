# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.core.Color import Color


@dataclasses.dataclass()
class ColorModulate(BaseObjectType):
    name: str = dataclasses.field(default='')
    unknown_1: Color = dataclasses.field(default_factory=Color)
    unknown_2: Color = dataclasses.field(default_factory=Color)
    unknown_3: int = dataclasses.field(default=0)
    unknown_4: float = dataclasses.field(default=0.0)
    unknown_5: float = dataclasses.field(default=0.0)
    unknown_6: bool = dataclasses.field(default=False)
    unknown_7: bool = dataclasses.field(default=False)
    unknown_8: bool = dataclasses.field(default=False)
    unknown_9: bool = dataclasses.field(default=False)
    unknown_10: bool = dataclasses.field(default=False)
    unknown_11: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x5E

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        unknown_1 = Color.from_stream(data)
        unknown_2 = Color.from_stream(data)
        unknown_3 = struct.unpack('>l', data.read(4))[0]
        unknown_4 = struct.unpack('>f', data.read(4))[0]
        unknown_5 = struct.unpack('>f', data.read(4))[0]
        unknown_6 = struct.unpack('>?', data.read(1))[0]
        unknown_7 = struct.unpack('>?', data.read(1))[0]
        unknown_8 = struct.unpack('>?', data.read(1))[0]
        unknown_9 = struct.unpack('>?', data.read(1))[0]
        unknown_10 = struct.unpack('>?', data.read(1))[0]
        unknown_11 = struct.unpack('>?', data.read(1))[0]
        return cls(name, unknown_1, unknown_2, unknown_3, unknown_4, unknown_5, unknown_6, unknown_7, unknown_8, unknown_9, unknown_10, unknown_11)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x0c')  # 12 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.unknown_1.to_stream(data)
        self.unknown_2.to_stream(data)
        data.write(struct.pack('>l', self.unknown_3))
        data.write(struct.pack('>f', self.unknown_4))
        data.write(struct.pack('>f', self.unknown_5))
        data.write(struct.pack('>?', self.unknown_6))
        data.write(struct.pack('>?', self.unknown_7))
        data.write(struct.pack('>?', self.unknown_8))
        data.write(struct.pack('>?', self.unknown_9))
        data.write(struct.pack('>?', self.unknown_10))
        data.write(struct.pack('>?', self.unknown_11))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            unknown_1=Color.from_json(data['unknown_1']),
            unknown_2=Color.from_json(data['unknown_2']),
            unknown_3=data['unknown_3'],
            unknown_4=data['unknown_4'],
            unknown_5=data['unknown_5'],
            unknown_6=data['unknown_6'],
            unknown_7=data['unknown_7'],
            unknown_8=data['unknown_8'],
            unknown_9=data['unknown_9'],
            unknown_10=data['unknown_10'],
            unknown_11=data['unknown_11'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'unknown_1': self.unknown_1.to_json(),
            'unknown_2': self.unknown_2.to_json(),
            'unknown_3': self.unknown_3,
            'unknown_4': self.unknown_4,
            'unknown_5': self.unknown_5,
            'unknown_6': self.unknown_6,
            'unknown_7': self.unknown_7,
            'unknown_8': self.unknown_8,
            'unknown_9': self.unknown_9,
            'unknown_10': self.unknown_10,
            'unknown_11': self.unknown_11,
        }

    def dependencies_for(self, asset_manager):
        yield from []
