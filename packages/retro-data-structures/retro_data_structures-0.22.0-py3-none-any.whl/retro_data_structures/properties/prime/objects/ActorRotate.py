# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class ActorRotate(BaseObjectType):
    name: str = dataclasses.field(default='')
    rotation_offset: Vector = dataclasses.field(default_factory=Vector)
    time_scale_: float = dataclasses.field(default=0.0)
    unknown_1: bool = dataclasses.field(default=False)
    unknown_2: bool = dataclasses.field(default=False)
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
        return 0x39

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        rotation_offset = Vector.from_stream(data)
        time_scale_ = struct.unpack('>f', data.read(4))[0]
        unknown_1 = struct.unpack('>?', data.read(1))[0]
        unknown_2 = struct.unpack('>?', data.read(1))[0]
        active = struct.unpack('>?', data.read(1))[0]
        return cls(name, rotation_offset, time_scale_, unknown_1, unknown_2, active)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x06')  # 6 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.rotation_offset.to_stream(data)
        data.write(struct.pack('>f', self.time_scale_))
        data.write(struct.pack('>?', self.unknown_1))
        data.write(struct.pack('>?', self.unknown_2))
        data.write(struct.pack('>?', self.active))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            rotation_offset=Vector.from_json(data['rotation_offset']),
            time_scale_=data['time_scale_'],
            unknown_1=data['unknown_1'],
            unknown_2=data['unknown_2'],
            active=data['active'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'rotation_offset': self.rotation_offset.to_json(),
            'time_scale_': self.time_scale_,
            'unknown_1': self.unknown_1,
            'unknown_2': self.unknown_2,
            'active': self.active,
        }

    def dependencies_for(self, asset_manager):
        yield from []
