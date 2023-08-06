# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct3(BaseProperty):
    center_x: float = dataclasses.field(default=320.0)
    center_y: float = dataclasses.field(default=224.0)
    width: float = dataclasses.field(default=32.0)
    height: float = dataclasses.field(default=32.0)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
        if default_override is None and (result := _fast_decode(data, property_count)) is not None:
            return result

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
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\x8c\x93\x8c?')  # 0x8c938c3f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.center_x))

        data.write(b'G\xcf_\x9a')  # 0x47cf5f9a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.center_y))

        data.write(b'\x10\xdbC\x81')  # 0x10db4381
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.width))

        data.write(b'\xc2\xbe\x03\r')  # 0xc2be030d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.height))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            center_x=data['center_x'],
            center_y=data['center_y'],
            width=data['width'],
            height=data['height'],
        )

    def to_json(self) -> dict:
        return {
            'center_x': self.center_x,
            'center_y': self.center_y,
            'width': self.width,
            'height': self.height,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x8c938c3f, 0x47cf5f9a, 0x10db4381, 0xc2be030d)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct3]:
    if property_count != 4:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(40))
    if (dec[0], dec[3], dec[6], dec[9]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct3(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
    )


def _decode_center_x(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_center_y(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_width(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x8c938c3f: ('center_x', _decode_center_x),
    0x47cf5f9a: ('center_y', _decode_center_y),
    0x10db4381: ('width', _decode_width),
    0xc2be030d: ('height', _decode_height),
}
