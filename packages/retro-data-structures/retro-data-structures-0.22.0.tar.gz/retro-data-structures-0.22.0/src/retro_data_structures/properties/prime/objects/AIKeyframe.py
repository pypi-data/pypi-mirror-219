# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType


@dataclasses.dataclass()
class AIKeyframe(BaseObjectType):
    name: str = dataclasses.field(default='')
    unknown_1: int = dataclasses.field(default=0)
    unknown_2: bool = dataclasses.field(default=False)
    unknown_3: float = dataclasses.field(default=0.0)
    unknown_4: bool = dataclasses.field(default=False)
    unknown_5: int = dataclasses.field(default=0)
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
        return 0x41

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        unknown_1 = struct.unpack('>l', data.read(4))[0]
        unknown_2 = struct.unpack('>?', data.read(1))[0]
        unknown_3 = struct.unpack('>f', data.read(4))[0]
        unknown_4 = struct.unpack('>?', data.read(1))[0]
        unknown_5 = struct.unpack('>l', data.read(4))[0]
        unknown_6 = struct.unpack('>f', data.read(4))[0]
        return cls(name, unknown_1, unknown_2, unknown_3, unknown_4, unknown_5, unknown_6)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x07')  # 7 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        data.write(struct.pack('>l', self.unknown_1))
        data.write(struct.pack('>?', self.unknown_2))
        data.write(struct.pack('>f', self.unknown_3))
        data.write(struct.pack('>?', self.unknown_4))
        data.write(struct.pack('>l', self.unknown_5))
        data.write(struct.pack('>f', self.unknown_6))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            unknown_1=data['unknown_1'],
            unknown_2=data['unknown_2'],
            unknown_3=data['unknown_3'],
            unknown_4=data['unknown_4'],
            unknown_5=data['unknown_5'],
            unknown_6=data['unknown_6'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'unknown_1': self.unknown_1,
            'unknown_2': self.unknown_2,
            'unknown_3': self.unknown_3,
            'unknown_4': self.unknown_4,
            'unknown_5': self.unknown_5,
            'unknown_6': self.unknown_6,
        }

    def dependencies_for(self, asset_manager):
        yield from []
