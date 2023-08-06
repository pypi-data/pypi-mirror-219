# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.Spline import Spline


@dataclasses.dataclass()
class UnknownStruct198(BaseProperty):
    x_motion: Spline = dataclasses.field(default_factory=Spline)
    y_motion: Spline = dataclasses.field(default_factory=Spline)
    z_motion: Spline = dataclasses.field(default_factory=Spline)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

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

        data.write(b'\x97\xf6\xeay')  # 0x97f6ea79
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.x_motion.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'J`3\xfc')  # 0x4a6033fc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.y_motion.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf7\xaa_2')  # 0xf7aa5f32
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.z_motion.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            x_motion=Spline.from_json(data['x_motion']),
            y_motion=Spline.from_json(data['y_motion']),
            z_motion=Spline.from_json(data['z_motion']),
        )

    def to_json(self) -> dict:
        return {
            'x_motion': self.x_motion.to_json(),
            'y_motion': self.y_motion.to_json(),
            'z_motion': self.z_motion.to_json(),
        }


def _decode_x_motion(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_y_motion(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_z_motion(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x97f6ea79: ('x_motion', _decode_x_motion),
    0x4a6033fc: ('y_motion', _decode_y_motion),
    0xf7aa5f32: ('z_motion', _decode_z_motion),
}
