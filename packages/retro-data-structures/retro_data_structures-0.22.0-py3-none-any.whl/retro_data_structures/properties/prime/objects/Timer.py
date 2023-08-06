# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType


@dataclasses.dataclass()
class Timer(BaseObjectType):
    name: str = dataclasses.field(default='')
    start_time: float = dataclasses.field(default=0.0)
    max_random_delay: float = dataclasses.field(default=0.0)
    loop: bool = dataclasses.field(default=False)
    auto_start: bool = dataclasses.field(default=False)
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
        return 0x5

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        start_time = struct.unpack('>f', data.read(4))[0]
        max_random_delay = struct.unpack('>f', data.read(4))[0]
        loop = struct.unpack('>?', data.read(1))[0]
        auto_start = struct.unpack('>?', data.read(1))[0]
        active = struct.unpack('>?', data.read(1))[0]
        return cls(name, start_time, max_random_delay, loop, auto_start, active)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x06')  # 6 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        data.write(struct.pack('>f', self.start_time))
        data.write(struct.pack('>f', self.max_random_delay))
        data.write(struct.pack('>?', self.loop))
        data.write(struct.pack('>?', self.auto_start))
        data.write(struct.pack('>?', self.active))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            start_time=data['start_time'],
            max_random_delay=data['max_random_delay'],
            loop=data['loop'],
            auto_start=data['auto_start'],
            active=data['active'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'start_time': self.start_time,
            'max_random_delay': self.max_random_delay,
            'loop': self.loop,
            'auto_start': self.auto_start,
            'active': self.active,
        }

    def dependencies_for(self, asset_manager):
        yield from []
