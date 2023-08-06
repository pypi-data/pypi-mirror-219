# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class Dock(BaseObjectType):
    name: str = dataclasses.field(default='')
    active: bool = dataclasses.field(default=False)
    position: Vector = dataclasses.field(default_factory=Vector)
    scale: Vector = dataclasses.field(default_factory=Vector)
    dock_number: int = dataclasses.field(default=0)
    area_number: int = dataclasses.field(default=0)
    load_connected_immediate: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0xB

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        active = struct.unpack('>?', data.read(1))[0]
        position = Vector.from_stream(data)
        scale = Vector.from_stream(data)
        dock_number = struct.unpack('>l', data.read(4))[0]
        area_number = struct.unpack('>l', data.read(4))[0]
        load_connected_immediate = struct.unpack('>?', data.read(1))[0]
        return cls(name, active, position, scale, dock_number, area_number, load_connected_immediate)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x07')  # 7 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        data.write(struct.pack('>?', self.active))
        self.position.to_stream(data)
        self.scale.to_stream(data)
        data.write(struct.pack('>l', self.dock_number))
        data.write(struct.pack('>l', self.area_number))
        data.write(struct.pack('>?', self.load_connected_immediate))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            active=data['active'],
            position=Vector.from_json(data['position']),
            scale=Vector.from_json(data['scale']),
            dock_number=data['dock_number'],
            area_number=data['area_number'],
            load_connected_immediate=data['load_connected_immediate'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'active': self.active,
            'position': self.position.to_json(),
            'scale': self.scale.to_json(),
            'dock_number': self.dock_number,
            'area_number': self.area_number,
            'load_connected_immediate': self.load_connected_immediate,
        }

    def dependencies_for(self, asset_manager):
        yield from []
