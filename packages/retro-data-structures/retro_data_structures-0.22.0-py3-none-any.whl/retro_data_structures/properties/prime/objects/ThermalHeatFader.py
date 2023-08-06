# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType


@dataclasses.dataclass()
class ThermalHeatFader(BaseObjectType):
    name: str = dataclasses.field(default='')
    active: bool = dataclasses.field(default=False)
    faded_heat_level: float = dataclasses.field(default=0.0)
    initial_heat_level: float = dataclasses.field(default=0.0)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x7D

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        active = struct.unpack('>?', data.read(1))[0]
        faded_heat_level = struct.unpack('>f', data.read(4))[0]
        initial_heat_level = struct.unpack('>f', data.read(4))[0]
        return cls(name, active, faded_heat_level, initial_heat_level)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x04')  # 4 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        data.write(struct.pack('>?', self.active))
        data.write(struct.pack('>f', self.faded_heat_level))
        data.write(struct.pack('>f', self.initial_heat_level))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            active=data['active'],
            faded_heat_level=data['faded_heat_level'],
            initial_heat_level=data['initial_heat_level'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'active': self.active,
            'faded_heat_level': self.faded_heat_level,
            'initial_heat_level': self.initial_heat_level,
        }

    def dependencies_for(self, asset_manager):
        yield from []
