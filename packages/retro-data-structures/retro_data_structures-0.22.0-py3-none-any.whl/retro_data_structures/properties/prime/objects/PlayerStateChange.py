# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.prime as enums


@dataclasses.dataclass()
class PlayerStateChange(BaseObjectType):
    name: str = dataclasses.field(default='')
    active: bool = dataclasses.field(default=False)
    unnamed: enums.PlayerItem = dataclasses.field(default=enums.PlayerItem.PowerBeam)
    amount: int = dataclasses.field(default=0)
    capacity: int = dataclasses.field(default=0)
    unknown_4: int = dataclasses.field(default=0)
    unknown_5: int = dataclasses.field(default=0)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x57

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        active = struct.unpack('>?', data.read(1))[0]
        unnamed = enums.PlayerItem.from_stream(data)
        amount = struct.unpack('>l', data.read(4))[0]
        capacity = struct.unpack('>l', data.read(4))[0]
        unknown_4 = struct.unpack('>l', data.read(4))[0]
        unknown_5 = struct.unpack('>l', data.read(4))[0]
        return cls(name, active, unnamed, amount, capacity, unknown_4, unknown_5)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x07')  # 7 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        data.write(struct.pack('>?', self.active))
        self.unnamed.to_stream(data)
        data.write(struct.pack('>l', self.amount))
        data.write(struct.pack('>l', self.capacity))
        data.write(struct.pack('>l', self.unknown_4))
        data.write(struct.pack('>l', self.unknown_5))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            active=data['active'],
            unnamed=enums.PlayerItem.from_json(data['unnamed']),
            amount=data['amount'],
            capacity=data['capacity'],
            unknown_4=data['unknown_4'],
            unknown_5=data['unknown_5'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'active': self.active,
            'unnamed': self.unnamed.to_json(),
            'amount': self.amount,
            'capacity': self.capacity,
            'unknown_4': self.unknown_4,
            'unknown_5': self.unknown_5,
        }

    def dependencies_for(self, asset_manager):
        yield from []
