# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct61(BaseProperty):
    number_of_bombs: int = dataclasses.field(default=6)
    horizontal_spread: float = dataclasses.field(default=20.0)
    unknown_0xf228ec53: float = dataclasses.field(default=15.0)
    unknown_0xd91227f1: float = dataclasses.field(default=20.0)

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
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\xf8\xd8\xd9v')  # 0xf8d8d976
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.number_of_bombs))

        data.write(b'\x8c)\xe9\x1c')  # 0x8c29e91c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.horizontal_spread))

        data.write(b'\xf2(\xecS')  # 0xf228ec53
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf228ec53))

        data.write(b"\xd9\x12'\xf1")  # 0xd91227f1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd91227f1))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            number_of_bombs=data['number_of_bombs'],
            horizontal_spread=data['horizontal_spread'],
            unknown_0xf228ec53=data['unknown_0xf228ec53'],
            unknown_0xd91227f1=data['unknown_0xd91227f1'],
        )

    def to_json(self) -> dict:
        return {
            'number_of_bombs': self.number_of_bombs,
            'horizontal_spread': self.horizontal_spread,
            'unknown_0xf228ec53': self.unknown_0xf228ec53,
            'unknown_0xd91227f1': self.unknown_0xd91227f1,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xf8d8d976, 0x8c29e91c, 0xf228ec53, 0xd91227f1)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct61]:
    if property_count != 4:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHlLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(40))
    if (dec[0], dec[3], dec[6], dec[9]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct61(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
    )


def _decode_number_of_bombs(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_horizontal_spread(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf228ec53(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd91227f1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf8d8d976: ('number_of_bombs', _decode_number_of_bombs),
    0x8c29e91c: ('horizontal_spread', _decode_horizontal_spread),
    0xf228ec53: ('unknown_0xf228ec53', _decode_unknown_0xf228ec53),
    0xd91227f1: ('unknown_0xd91227f1', _decode_unknown_0xd91227f1),
}
