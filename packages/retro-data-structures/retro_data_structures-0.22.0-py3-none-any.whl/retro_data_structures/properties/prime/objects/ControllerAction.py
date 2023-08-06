# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.prime as enums


@dataclasses.dataclass()
class ControllerAction(BaseObjectType):
    name: str = dataclasses.field(default='')
    active: bool = dataclasses.field(default=False)
    action: enums.PlayerAction = dataclasses.field(default=enums.PlayerAction.Forward)
    deactivate_when_used: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x55

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        active = struct.unpack('>?', data.read(1))[0]
        action = enums.PlayerAction.from_stream(data)
        deactivate_when_used = struct.unpack('>?', data.read(1))[0]
        return cls(name, active, action, deactivate_when_used)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x04')  # 4 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        data.write(struct.pack('>?', self.active))
        self.action.to_stream(data)
        data.write(struct.pack('>?', self.deactivate_when_used))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            active=data['active'],
            action=enums.PlayerAction.from_json(data['action']),
            deactivate_when_used=data['deactivate_when_used'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'active': self.active,
            'action': self.action.to_json(),
            'deactivate_when_used': self.deactivate_when_used,
        }

    def dependencies_for(self, asset_manager):
        yield from []
