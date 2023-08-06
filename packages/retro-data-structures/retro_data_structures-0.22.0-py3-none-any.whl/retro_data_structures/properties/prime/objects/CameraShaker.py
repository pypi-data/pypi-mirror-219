# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType


@dataclasses.dataclass()
class CameraShaker(BaseObjectType):
    name: str = dataclasses.field(default='')
    horizontal_shake: float = dataclasses.field(default=0.0)
    unknown_1: float = dataclasses.field(default=0.0)
    unknown_2: float = dataclasses.field(default=0.0)
    unknown_3: float = dataclasses.field(default=0.0)
    vertical_shake: float = dataclasses.field(default=0.0)
    unknown_4: float = dataclasses.field(default=0.0)
    shake_length: float = dataclasses.field(default=0.0)
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
        return 0x1C

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        horizontal_shake = struct.unpack('>f', data.read(4))[0]
        unknown_1 = struct.unpack('>f', data.read(4))[0]
        unknown_2 = struct.unpack('>f', data.read(4))[0]
        unknown_3 = struct.unpack('>f', data.read(4))[0]
        vertical_shake = struct.unpack('>f', data.read(4))[0]
        unknown_4 = struct.unpack('>f', data.read(4))[0]
        shake_length = struct.unpack('>f', data.read(4))[0]
        active = struct.unpack('>?', data.read(1))[0]
        return cls(name, horizontal_shake, unknown_1, unknown_2, unknown_3, vertical_shake, unknown_4, shake_length, active)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\t')  # 9 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        data.write(struct.pack('>f', self.horizontal_shake))
        data.write(struct.pack('>f', self.unknown_1))
        data.write(struct.pack('>f', self.unknown_2))
        data.write(struct.pack('>f', self.unknown_3))
        data.write(struct.pack('>f', self.vertical_shake))
        data.write(struct.pack('>f', self.unknown_4))
        data.write(struct.pack('>f', self.shake_length))
        data.write(struct.pack('>?', self.active))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            horizontal_shake=data['horizontal_shake'],
            unknown_1=data['unknown_1'],
            unknown_2=data['unknown_2'],
            unknown_3=data['unknown_3'],
            vertical_shake=data['vertical_shake'],
            unknown_4=data['unknown_4'],
            shake_length=data['shake_length'],
            active=data['active'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'horizontal_shake': self.horizontal_shake,
            'unknown_1': self.unknown_1,
            'unknown_2': self.unknown_2,
            'unknown_3': self.unknown_3,
            'vertical_shake': self.vertical_shake,
            'unknown_4': self.unknown_4,
            'shake_length': self.shake_length,
            'active': self.active,
        }

    def dependencies_for(self, asset_manager):
        yield from []
