# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class PickupGenerator(BaseObjectType):
    name: str = dataclasses.field(default='')
    offset: Vector = dataclasses.field(default_factory=Vector)
    active: bool = dataclasses.field(default=False)
    frequency: float = dataclasses.field(default=0.0)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x40

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        offset = Vector.from_stream(data)
        active = struct.unpack('>?', data.read(1))[0]
        frequency = struct.unpack('>f', data.read(4))[0]
        return cls(name, offset, active, frequency)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x04')  # 4 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.offset.to_stream(data)
        data.write(struct.pack('>?', self.active))
        data.write(struct.pack('>f', self.frequency))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            offset=Vector.from_json(data['offset']),
            active=data['active'],
            frequency=data['frequency'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'offset': self.offset.to_json(),
            'active': self.active,
            'frequency': self.frequency,
        }

    def dependencies_for(self, asset_manager):
        yield from []
