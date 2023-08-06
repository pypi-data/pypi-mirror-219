# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct264(BaseProperty):
    unknown: bool = dataclasses.field(default=False)
    is_percentage: bool = dataclasses.field(default=False)
    percentage_chance: int = dataclasses.field(default=50)
    minimum_count: int = dataclasses.field(default=1)
    maximum_count: int = dataclasses.field(default=1)
    minimum_percentage: int = dataclasses.field(default=50)
    maximum_percentage: int = dataclasses.field(default=50)
    choose_inactive: bool = dataclasses.field(default=False)

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
        data.write(b'\x00\x08')  # 8 properties

        data.write(b'\x19\xa9\x1b;')  # 0x19a91b3b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown))

        data.write(b'T\xa2\xd2\xb1')  # 0x54a2d2b1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_percentage))

        data.write(b'\xab\xbd\xd0G')  # 0xabbdd047
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.percentage_chance))

        data.write(b'\xf3\xfcnS')  # 0xf3fc6e53
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.minimum_count))

        data.write(b'\xd4G\tb')  # 0xd4470962
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.maximum_count))

        data.write(b'\xf5\x0b\x11\xeb')  # 0xf50b11eb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.minimum_percentage))

        data.write(b'\xdcu\xec\xf3')  # 0xdc75ecf3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.maximum_percentage))

        data.write(b'C.\x9ds')  # 0x432e9d73
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.choose_inactive))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown=data['unknown'],
            is_percentage=data['is_percentage'],
            percentage_chance=data['percentage_chance'],
            minimum_count=data['minimum_count'],
            maximum_count=data['maximum_count'],
            minimum_percentage=data['minimum_percentage'],
            maximum_percentage=data['maximum_percentage'],
            choose_inactive=data['choose_inactive'],
        )

    def to_json(self) -> dict:
        return {
            'unknown': self.unknown,
            'is_percentage': self.is_percentage,
            'percentage_chance': self.percentage_chance,
            'minimum_count': self.minimum_count,
            'maximum_count': self.maximum_count,
            'minimum_percentage': self.minimum_percentage,
            'maximum_percentage': self.maximum_percentage,
            'choose_inactive': self.choose_inactive,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x19a91b3b, 0x54a2d2b1, 0xabbdd047, 0xf3fc6e53, 0xd4470962, 0xf50b11eb, 0xdc75ecf3, 0x432e9d73)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct264]:
    if property_count != 8:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LH?LH?LHlLHlLHlLHlLHlLH?')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(71))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct264(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
        dec[20],
        dec[23],
    )


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_is_percentage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_percentage_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_minimum_count(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_maximum_count(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_minimum_percentage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_maximum_percentage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_choose_inactive(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x19a91b3b: ('unknown', _decode_unknown),
    0x54a2d2b1: ('is_percentage', _decode_is_percentage),
    0xabbdd047: ('percentage_chance', _decode_percentage_chance),
    0xf3fc6e53: ('minimum_count', _decode_minimum_count),
    0xd4470962: ('maximum_count', _decode_maximum_count),
    0xf50b11eb: ('minimum_percentage', _decode_minimum_percentage),
    0xdc75ecf3: ('maximum_percentage', _decode_maximum_percentage),
    0x432e9d73: ('choose_inactive', _decode_choose_inactive),
}
