# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class VectorMP1(BaseProperty):
    x: float = dataclasses.field(default=0.0)
    y: float = dataclasses.field(default=0.0)
    z: float = dataclasses.field(default=0.0)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME_REMASTER

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack("<H", data.read(2))[0]
        if default_override is None and (result := _fast_decode(data, property_count)) is not None:
            return result

        present_fields = default_override or {}
        for _ in range(property_count):
            property_id, property_size = struct.unpack("<LH", data.read(6))
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
        num_properties_offset = data.tell()
        data.write(b'\x00\x00')  # 0 properties
        num_properties_written = 0

        if self.x != default_override.get('x', 0.0):
            num_properties_written += 1
            data.write(b'Q\xe5I&')  # 0x2649e551
            data.write(b'\x04\x00')  # size
            data.write(struct.pack('<f', self.x))

        if self.y != default_override.get('y', 0.0):
            num_properties_written += 1
            data.write(b'\xc6[\xbb\xd2')  # 0xd2bb5bc6
            data.write(b'\x04\x00')  # size
            data.write(struct.pack('<f', self.y))

        if self.z != default_override.get('z', 0.0):
            num_properties_written += 1
            data.write(b'\xb2\x99\x94\x7f')  # 0x7f9499b2
            data.write(b'\x04\x00')  # size
            data.write(struct.pack('<f', self.z))

        if num_properties_written != 0:
            struct_end_offset = data.tell()
            data.seek(num_properties_offset)
            data.write(struct.pack("<H", num_properties_written))
            data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            x=data['x'],
            y=data['y'],
            z=data['z'],
        )

    def to_json(self) -> dict:
        return {
            'x': self.x,
            'y': self.y,
            'z': self.z,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x2649e551, 0xd2bb5bc6, 0x7f9499b2)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[VectorMP1]:
    if property_count != 3:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('<LHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(30))
    if (dec[0], dec[3], dec[6]) != _FAST_IDS:
        data.seek(before)
        return None

    return VectorMP1(
        dec[2],
        dec[5],
        dec[8],
    )


def _decode_x(data: typing.BinaryIO, property_size: int):
    return struct.unpack('<f', data.read(4))[0]


def _decode_y(data: typing.BinaryIO, property_size: int):
    return struct.unpack('<f', data.read(4))[0]


def _decode_z(data: typing.BinaryIO, property_size: int):
    return struct.unpack('<f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x2649e551: ('x', _decode_x),
    0xd2bb5bc6: ('y', _decode_y),
    0x7f9499b2: ('z', _decode_z),
}
