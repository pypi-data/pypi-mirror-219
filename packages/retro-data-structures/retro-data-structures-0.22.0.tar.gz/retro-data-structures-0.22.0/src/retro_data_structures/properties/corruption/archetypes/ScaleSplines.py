# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.core.Spline import Spline


@dataclasses.dataclass()
class ScaleSplines(BaseProperty):
    x_scale: Spline = dataclasses.field(default_factory=Spline)
    y_scale: Spline = dataclasses.field(default_factory=Spline)
    z_scale: Spline = dataclasses.field(default_factory=Spline)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

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
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\xf47\xa6/')  # 0xf437a62f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.x_scale.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'o\x92\xea@')  # 0x6f92ea40
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.y_scale.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x18\x0c8\xb0')  # 0x180c38b0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.z_scale.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            x_scale=Spline.from_json(data['x_scale']),
            y_scale=Spline.from_json(data['y_scale']),
            z_scale=Spline.from_json(data['z_scale']),
        )

    def to_json(self) -> dict:
        return {
            'x_scale': self.x_scale.to_json(),
            'y_scale': self.y_scale.to_json(),
            'z_scale': self.z_scale.to_json(),
        }


def _decode_x_scale(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_y_scale(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_z_scale(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf437a62f: ('x_scale', _decode_x_scale),
    0x6f92ea40: ('y_scale', _decode_y_scale),
    0x180c38b0: ('z_scale', _decode_z_scale),
}
