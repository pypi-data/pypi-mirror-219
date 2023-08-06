# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct70(BaseProperty):
    unknown_0x3b6740f1: float = dataclasses.field(default=2.0)
    unknown_0x8130b0d8: float = dataclasses.field(default=1.0)
    ignore_upper_lower_bounds: bool = dataclasses.field(default=False)

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
        data.write(b'\x00\x03')  # 3 properties

        data.write(b';g@\xf1')  # 0x3b6740f1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3b6740f1))

        data.write(b'\x810\xb0\xd8')  # 0x8130b0d8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8130b0d8))

        data.write(b'hYR\xe3')  # 0x685952e3
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.ignore_upper_lower_bounds))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x3b6740f1=data['unknown_0x3b6740f1'],
            unknown_0x8130b0d8=data['unknown_0x8130b0d8'],
            ignore_upper_lower_bounds=data['ignore_upper_lower_bounds'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x3b6740f1': self.unknown_0x3b6740f1,
            'unknown_0x8130b0d8': self.unknown_0x8130b0d8,
            'ignore_upper_lower_bounds': self.ignore_upper_lower_bounds,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x3b6740f1, 0x8130b0d8, 0x685952e3)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct70]:
    if property_count != 3:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLH?')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(27))
    if (dec[0], dec[3], dec[6]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct70(
        dec[2],
        dec[5],
        dec[8],
    )


def _decode_unknown_0x3b6740f1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8130b0d8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ignore_upper_lower_bounds(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x3b6740f1: ('unknown_0x3b6740f1', _decode_unknown_0x3b6740f1),
    0x8130b0d8: ('unknown_0x8130b0d8', _decode_unknown_0x8130b0d8),
    0x685952e3: ('ignore_upper_lower_bounds', _decode_ignore_upper_lower_bounds),
}
