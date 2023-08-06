# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct128(BaseProperty):
    unknown_0xc5a02c2c: bool = dataclasses.field(default=True)
    unknown_0x59adc680: float = dataclasses.field(default=2.0)
    unknown_0x5dbba112: float = dataclasses.field(default=0.0)

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

        data.write(b'\xc5\xa0,,')  # 0xc5a02c2c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xc5a02c2c))

        data.write(b'Y\xad\xc6\x80')  # 0x59adc680
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x59adc680))

        data.write(b']\xbb\xa1\x12')  # 0x5dbba112
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5dbba112))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xc5a02c2c=data['unknown_0xc5a02c2c'],
            unknown_0x59adc680=data['unknown_0x59adc680'],
            unknown_0x5dbba112=data['unknown_0x5dbba112'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xc5a02c2c': self.unknown_0xc5a02c2c,
            'unknown_0x59adc680': self.unknown_0x59adc680,
            'unknown_0x5dbba112': self.unknown_0x5dbba112,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xc5a02c2c, 0x59adc680, 0x5dbba112)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct128]:
    if property_count != 3:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LH?LHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(27))
    if (dec[0], dec[3], dec[6]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct128(
        dec[2],
        dec[5],
        dec[8],
    )


def _decode_unknown_0xc5a02c2c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x59adc680(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x5dbba112(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc5a02c2c: ('unknown_0xc5a02c2c', _decode_unknown_0xc5a02c2c),
    0x59adc680: ('unknown_0x59adc680', _decode_unknown_0x59adc680),
    0x5dbba112: ('unknown_0x5dbba112', _decode_unknown_0x5dbba112),
}
