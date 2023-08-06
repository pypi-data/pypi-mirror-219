# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.core.Color import Color
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class FogVolume(BaseObjectType):
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    scale: Vector = dataclasses.field(default_factory=Vector)
    flicker_speed: float = dataclasses.field(default=0.0)
    unknown: float = dataclasses.field(default=0.0)
    fog_color: Color = dataclasses.field(default_factory=Color)
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
        return 0x65

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        position = Vector.from_stream(data)
        scale = Vector.from_stream(data)
        flicker_speed = struct.unpack('>f', data.read(4))[0]
        unknown = struct.unpack('>f', data.read(4))[0]
        fog_color = Color.from_stream(data)
        active = struct.unpack('>?', data.read(1))[0]
        return cls(name, position, scale, flicker_speed, unknown, fog_color, active)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x07')  # 7 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        self.scale.to_stream(data)
        data.write(struct.pack('>f', self.flicker_speed))
        data.write(struct.pack('>f', self.unknown))
        self.fog_color.to_stream(data)
        data.write(struct.pack('>?', self.active))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            position=Vector.from_json(data['position']),
            scale=Vector.from_json(data['scale']),
            flicker_speed=data['flicker_speed'],
            unknown=data['unknown'],
            fog_color=Color.from_json(data['fog_color']),
            active=data['active'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'position': self.position.to_json(),
            'scale': self.scale.to_json(),
            'flicker_speed': self.flicker_speed,
            'unknown': self.unknown,
            'fog_color': self.fog_color.to_json(),
            'active': self.active,
        }

    def dependencies_for(self, asset_manager):
        yield from []
