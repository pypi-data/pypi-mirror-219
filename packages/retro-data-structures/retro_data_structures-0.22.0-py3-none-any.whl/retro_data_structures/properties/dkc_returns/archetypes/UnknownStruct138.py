# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct138(BaseProperty):
    unknown_0xd4b4ad93: float = dataclasses.field(default=-1.0)
    unknown_0x035f1fd2: float = dataclasses.field(default=1.0)
    unknown_0x354d1781: float = dataclasses.field(default=-1.0)
    unknown_0xe2a6a5c0: float = dataclasses.field(default=1.0)

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

        data.write(b'\xd4\xb4\xad\x93')  # 0xd4b4ad93
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd4b4ad93))

        data.write(b'\x03_\x1f\xd2')  # 0x35f1fd2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x035f1fd2))

        data.write(b'5M\x17\x81')  # 0x354d1781
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x354d1781))

        data.write(b'\xe2\xa6\xa5\xc0')  # 0xe2a6a5c0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe2a6a5c0))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xd4b4ad93=data['unknown_0xd4b4ad93'],
            unknown_0x035f1fd2=data['unknown_0x035f1fd2'],
            unknown_0x354d1781=data['unknown_0x354d1781'],
            unknown_0xe2a6a5c0=data['unknown_0xe2a6a5c0'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xd4b4ad93': self.unknown_0xd4b4ad93,
            'unknown_0x035f1fd2': self.unknown_0x035f1fd2,
            'unknown_0x354d1781': self.unknown_0x354d1781,
            'unknown_0xe2a6a5c0': self.unknown_0xe2a6a5c0,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xd4b4ad93, 0x35f1fd2, 0x354d1781, 0xe2a6a5c0)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct138]:
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

    return UnknownStruct138(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
    )


def _decode_unknown_0xd4b4ad93(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x035f1fd2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x354d1781(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe2a6a5c0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xd4b4ad93: ('unknown_0xd4b4ad93', _decode_unknown_0xd4b4ad93),
    0x35f1fd2: ('unknown_0x035f1fd2', _decode_unknown_0x035f1fd2),
    0x354d1781: ('unknown_0x354d1781', _decode_unknown_0x354d1781),
    0xe2a6a5c0: ('unknown_0xe2a6a5c0', _decode_unknown_0xe2a6a5c0),
}
