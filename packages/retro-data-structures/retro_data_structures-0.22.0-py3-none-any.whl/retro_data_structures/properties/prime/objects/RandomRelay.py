# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType


@dataclasses.dataclass()
class RandomRelay(BaseObjectType):
    name: str = dataclasses.field(default='')
    connection_count: int = dataclasses.field(default=0)
    variance: int = dataclasses.field(default=0)
    unknown: bool = dataclasses.field(default=False)
    active: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x14

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        connection_count = struct.unpack('>l', data.read(4))[0]
        variance = struct.unpack('>l', data.read(4))[0]
        unknown = struct.unpack('>?', data.read(1))[0]
        active = struct.unpack('>?', data.read(1))[0]
        return cls(name, connection_count, variance, unknown, active)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x05')  # 5 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        data.write(struct.pack('>l', self.connection_count))
        data.write(struct.pack('>l', self.variance))
        data.write(struct.pack('>?', self.unknown))
        data.write(struct.pack('>?', self.active))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            connection_count=data['connection_count'],
            variance=data['variance'],
            unknown=data['unknown'],
            active=data['active'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'connection_count': self.connection_count,
            'variance': self.variance,
            'unknown': self.unknown,
            'active': self.active,
        }

    def dependencies_for(self, asset_manager):
        yield from []
