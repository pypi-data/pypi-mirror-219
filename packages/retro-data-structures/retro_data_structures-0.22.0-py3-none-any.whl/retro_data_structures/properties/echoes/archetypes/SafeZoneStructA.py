# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.Vector2f import Vector2f
from retro_data_structures.properties.echoes.core.Color import Color


@dataclasses.dataclass()
class SafeZoneStructA(BaseProperty):
    enabled: bool = dataclasses.field(default=True)
    mode: int = dataclasses.field(default=0)
    color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    near_far_plane: Vector2f = dataclasses.field(default_factory=Vector2f)
    color_rate: float = dataclasses.field(default=0.0)
    distance_rate: Vector2f = dataclasses.field(default_factory=Vector2f)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
        present_fields = default_override or {}
        for _ in range(property_count):
            property_id, property_size = struct.unpack(">LH", data.read(6))
            start = data.tell()
            try:
                property_name, decoder = _property_decoder[property_id]
                present_fields[property_name] = decoder(data, property_size)
            except KeyError:
                raise RuntimeError(f"Unknown property: 0x{property_id:08x}")
            assert data.tell() - start == property_size

        return cls(**present_fields)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x06')  # 6 properties

        data.write(b")\xc7}'")  # 0x29c77d27
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.enabled))

        data.write(b'\t\xadc\xde')  # 0x9ad63de
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.mode))

        data.write(b'7\xc7\xd0\x9d')  # 0x37c7d09d
        data.write(b'\x00\x10')  # size
        self.color.to_stream(data)

        data.write(b'e \x08\xda')  # 0x652008da
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.near_far_plane.to_stream(data, default_override={'x': 1.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b")\xabG'")  # 0x29ab4727
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.color_rate))

        data.write(b'\xcc\x8e\x0f\x98')  # 0xcc8e0f98
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.distance_rate.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            enabled=data['enabled'],
            mode=data['mode'],
            color=Color.from_json(data['color']),
            near_far_plane=Vector2f.from_json(data['near_far_plane']),
            color_rate=data['color_rate'],
            distance_rate=Vector2f.from_json(data['distance_rate']),
        )

    def to_json(self) -> dict:
        return {
            'enabled': self.enabled,
            'mode': self.mode,
            'color': self.color.to_json(),
            'near_far_plane': self.near_far_plane.to_json(),
            'color_rate': self.color_rate,
            'distance_rate': self.distance_rate.to_json(),
        }

    def _dependencies_for_near_far_plane(self, asset_manager):
        yield from self.near_far_plane.dependencies_for(asset_manager)

    def _dependencies_for_distance_rate(self, asset_manager):
        yield from self.distance_rate.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_near_far_plane, "near_far_plane", "Vector2f"),
            (self._dependencies_for_distance_rate, "distance_rate", "Vector2f"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for SafeZoneStructA.{field_name} ({field_type}): {e}"
                )


def _decode_enabled(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_mode(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_near_far_plane(data: typing.BinaryIO, property_size: int):
    return Vector2f.from_stream(data, property_size, default_override={'x': 1.0})


def _decode_color_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_distance_rate(data: typing.BinaryIO, property_size: int):
    return Vector2f.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x29c77d27: ('enabled', _decode_enabled),
    0x9ad63de: ('mode', _decode_mode),
    0x37c7d09d: ('color', _decode_color),
    0x652008da: ('near_far_plane', _decode_near_far_plane),
    0x29ab4727: ('color_rate', _decode_color_rate),
    0xcc8e0f98: ('distance_rate', _decode_distance_rate),
}
