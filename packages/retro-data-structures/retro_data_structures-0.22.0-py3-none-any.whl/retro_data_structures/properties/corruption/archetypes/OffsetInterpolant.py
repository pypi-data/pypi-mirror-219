# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.core.Spline import Spline


@dataclasses.dataclass()
class OffsetInterpolant(BaseProperty):
    x_offset: Spline = dataclasses.field(default_factory=Spline)
    y_offset: Spline = dataclasses.field(default_factory=Spline)
    z_offset: Spline = dataclasses.field(default_factory=Spline)

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

        data.write(b'H[\x0c\x11')  # 0x485b0c11
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.x_offset.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x95\xcd\xd5\x94')  # 0x95cdd594
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.y_offset.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'(\x07\xb9Z')  # 0x2807b95a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.z_offset.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            x_offset=Spline.from_json(data['x_offset']),
            y_offset=Spline.from_json(data['y_offset']),
            z_offset=Spline.from_json(data['z_offset']),
        )

    def to_json(self) -> dict:
        return {
            'x_offset': self.x_offset.to_json(),
            'y_offset': self.y_offset.to_json(),
            'z_offset': self.z_offset.to_json(),
        }


def _decode_x_offset(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_y_offset(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_z_offset(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x485b0c11: ('x_offset', _decode_x_offset),
    0x95cdd594: ('y_offset', _decode_y_offset),
    0x2807b95a: ('z_offset', _decode_z_offset),
}
