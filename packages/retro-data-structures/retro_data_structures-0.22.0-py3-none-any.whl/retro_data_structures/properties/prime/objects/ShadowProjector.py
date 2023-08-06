# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class ShadowProjector(BaseObjectType):
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    active: bool = dataclasses.field(default=False)
    shadow_scale: float = dataclasses.field(default=0.0)
    shadow_offset: Vector = dataclasses.field(default_factory=Vector)
    unknown_4: float = dataclasses.field(default=0.0)
    shadow_opacity: float = dataclasses.field(default=0.0)
    unknown_6: float = dataclasses.field(default=0.0)
    unknown_7: bool = dataclasses.field(default=False)
    unknown_8: int = dataclasses.field(default=0)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x8A

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        position = Vector.from_stream(data)
        active = struct.unpack('>?', data.read(1))[0]
        shadow_scale = struct.unpack('>f', data.read(4))[0]
        shadow_offset = Vector.from_stream(data)
        unknown_4 = struct.unpack('>f', data.read(4))[0]
        shadow_opacity = struct.unpack('>f', data.read(4))[0]
        unknown_6 = struct.unpack('>f', data.read(4))[0]
        unknown_7 = struct.unpack('>?', data.read(1))[0]
        unknown_8 = struct.unpack('>l', data.read(4))[0]
        return cls(name, position, active, shadow_scale, shadow_offset, unknown_4, shadow_opacity, unknown_6, unknown_7, unknown_8)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\n')  # 10 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        data.write(struct.pack('>?', self.active))
        data.write(struct.pack('>f', self.shadow_scale))
        self.shadow_offset.to_stream(data)
        data.write(struct.pack('>f', self.unknown_4))
        data.write(struct.pack('>f', self.shadow_opacity))
        data.write(struct.pack('>f', self.unknown_6))
        data.write(struct.pack('>?', self.unknown_7))
        data.write(struct.pack('>l', self.unknown_8))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            position=Vector.from_json(data['position']),
            active=data['active'],
            shadow_scale=data['shadow_scale'],
            shadow_offset=Vector.from_json(data['shadow_offset']),
            unknown_4=data['unknown_4'],
            shadow_opacity=data['shadow_opacity'],
            unknown_6=data['unknown_6'],
            unknown_7=data['unknown_7'],
            unknown_8=data['unknown_8'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'position': self.position.to_json(),
            'active': self.active,
            'shadow_scale': self.shadow_scale,
            'shadow_offset': self.shadow_offset.to_json(),
            'unknown_4': self.unknown_4,
            'shadow_opacity': self.shadow_opacity,
            'unknown_6': self.unknown_6,
            'unknown_7': self.unknown_7,
            'unknown_8': self.unknown_8,
        }

    def dependencies_for(self, asset_manager):
        yield from []
