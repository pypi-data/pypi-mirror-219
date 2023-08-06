# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType


@dataclasses.dataclass()
class Counter(BaseObjectType):
    name: str = dataclasses.field(default='')
    start_value: int = dataclasses.field(default=0)
    max_value: int = dataclasses.field(default=0)
    reset_when_max_zero_reached: bool = dataclasses.field(default=False)
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
        return 0x6

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        start_value = struct.unpack('>l', data.read(4))[0]
        max_value = struct.unpack('>l', data.read(4))[0]
        reset_when_max_zero_reached = struct.unpack('>?', data.read(1))[0]
        active = struct.unpack('>?', data.read(1))[0]
        return cls(name, start_value, max_value, reset_when_max_zero_reached, active)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x05')  # 5 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        data.write(struct.pack('>l', self.start_value))
        data.write(struct.pack('>l', self.max_value))
        data.write(struct.pack('>?', self.reset_when_max_zero_reached))
        data.write(struct.pack('>?', self.active))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            start_value=data['start_value'],
            max_value=data['max_value'],
            reset_when_max_zero_reached=data['reset_when_max_zero_reached'],
            active=data['active'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'start_value': self.start_value,
            'max_value': self.max_value,
            'reset_when_max_zero_reached': self.reset_when_max_zero_reached,
            'active': self.active,
        }

    def dependencies_for(self, asset_manager):
        yield from []
