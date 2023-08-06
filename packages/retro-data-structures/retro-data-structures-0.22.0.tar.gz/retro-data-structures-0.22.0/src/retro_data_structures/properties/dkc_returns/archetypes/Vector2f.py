# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class Vector2f(BaseProperty):
    x: float = dataclasses.field(default=0.0)
    y: float = dataclasses.field(default=0.0)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

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
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'\xa1g}N')  # 0xa1677d4e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.x))

        data.write(b'j;\xae\xeb')  # 0x6a3baeeb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.y))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            x=data['x'],
            y=data['y'],
        )

    def to_json(self) -> dict:
        return {
            'x': self.x,
            'y': self.y,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xa1677d4e, 0x6a3baeeb)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[Vector2f]:
    if property_count != 2:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(20))
    if (dec[0], dec[3]) != _FAST_IDS:
        data.seek(before)
        return None

    return Vector2f(
        dec[2],
        dec[5],
    )


def _decode_x(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_y(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa1677d4e: ('x', _decode_x),
    0x6a3baeeb: ('y', _decode_y),
}
