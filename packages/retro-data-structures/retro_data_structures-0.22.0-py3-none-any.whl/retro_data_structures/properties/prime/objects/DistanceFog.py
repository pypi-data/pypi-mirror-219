# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.archetypes.Vector2f import Vector2f
from retro_data_structures.properties.prime.core.Color import Color


@dataclasses.dataclass()
class DistanceFog(BaseObjectType):
    name: str = dataclasses.field(default='')
    mode: int = dataclasses.field(default=0)
    color: Color = dataclasses.field(default_factory=Color)
    range: Vector2f = dataclasses.field(default_factory=Vector2f)
    color_delta: float = dataclasses.field(default=0.0)
    range_delta: Vector2f = dataclasses.field(default_factory=Vector2f)
    explicit: bool = dataclasses.field(default=False)
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
        return 0x35

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        mode = struct.unpack('>l', data.read(4))[0]
        color = Color.from_stream(data)
        range = Vector2f.from_stream(data, property_size)
        color_delta = struct.unpack('>f', data.read(4))[0]
        range_delta = Vector2f.from_stream(data, property_size)
        explicit = struct.unpack('>?', data.read(1))[0]
        active = struct.unpack('>?', data.read(1))[0]
        return cls(name, mode, color, range, color_delta, range_delta, explicit, active)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x08')  # 8 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        data.write(struct.pack('>l', self.mode))
        self.color.to_stream(data)
        self.range.to_stream(data)
        data.write(struct.pack('>f', self.color_delta))
        self.range_delta.to_stream(data)
        data.write(struct.pack('>?', self.explicit))
        data.write(struct.pack('>?', self.active))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            mode=data['mode'],
            color=Color.from_json(data['color']),
            range=Vector2f.from_json(data['range']),
            color_delta=data['color_delta'],
            range_delta=Vector2f.from_json(data['range_delta']),
            explicit=data['explicit'],
            active=data['active'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'mode': self.mode,
            'color': self.color.to_json(),
            'range': self.range.to_json(),
            'color_delta': self.color_delta,
            'range_delta': self.range_delta.to_json(),
            'explicit': self.explicit,
            'active': self.active,
        }

    def _dependencies_for_range(self, asset_manager):
        yield from self.range.dependencies_for(asset_manager)

    def _dependencies_for_range_delta(self, asset_manager):
        yield from self.range_delta.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_range, "range", "Vector2f"),
            (self._dependencies_for_range_delta, "range_delta", "Vector2f"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for DistanceFog.{field_name} ({field_type}): {e}"
                )
