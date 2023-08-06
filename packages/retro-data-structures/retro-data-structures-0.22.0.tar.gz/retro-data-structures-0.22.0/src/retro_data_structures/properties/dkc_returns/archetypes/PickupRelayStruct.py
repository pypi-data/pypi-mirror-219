# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class PickupRelayStruct(BaseProperty):
    message1_chance: float = dataclasses.field(default=0.0)
    message2_chance: float = dataclasses.field(default=0.0)
    message3_chance: float = dataclasses.field(default=0.0)
    message4_chance: float = dataclasses.field(default=0.0)
    message5_chance: float = dataclasses.field(default=0.0)
    message6_chance: float = dataclasses.field(default=0.0)
    message7_chance: float = dataclasses.field(default=0.0)
    message8_chance: float = dataclasses.field(default=0.0)
    message9_chance: float = dataclasses.field(default=0.0)
    message10_chance: float = dataclasses.field(default=0.0)

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
        data.write(b'\x00\n')  # 10 properties

        data.write(b'\xfd\xe3\xa4\xf5')  # 0xfde3a4f5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.message1_chance))

        data.write(b'\x8a}v\x05')  # 0x8a7d7605
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.message2_chance))

        data.write(b'\x11\xd8:j')  # 0x11d83a6a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.message3_chance))

        data.write(b'e@\xd3\xe5')  # 0x6540d3e5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.message4_chance))

        data.write(b'\xfe\xe5\x9f\x8a')  # 0xfee59f8a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.message5_chance))

        data.write(b'\x89{Mz')  # 0x897b4d7a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.message6_chance))

        data.write(b'\x12\xde\x01\x15')  # 0x12de0115
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.message7_chance))

        data.write(b'`J\x9ed')  # 0x604a9e64
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.message8_chance))

        data.write(b'\xfb\xef\xd2\x0b')  # 0xfbefd20b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.message9_chance))

        data.write(b'T\xe8\xc1\x8a')  # 0x54e8c18a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.message10_chance))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            message1_chance=data['message1_chance'],
            message2_chance=data['message2_chance'],
            message3_chance=data['message3_chance'],
            message4_chance=data['message4_chance'],
            message5_chance=data['message5_chance'],
            message6_chance=data['message6_chance'],
            message7_chance=data['message7_chance'],
            message8_chance=data['message8_chance'],
            message9_chance=data['message9_chance'],
            message10_chance=data['message10_chance'],
        )

    def to_json(self) -> dict:
        return {
            'message1_chance': self.message1_chance,
            'message2_chance': self.message2_chance,
            'message3_chance': self.message3_chance,
            'message4_chance': self.message4_chance,
            'message5_chance': self.message5_chance,
            'message6_chance': self.message6_chance,
            'message7_chance': self.message7_chance,
            'message8_chance': self.message8_chance,
            'message9_chance': self.message9_chance,
            'message10_chance': self.message10_chance,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xfde3a4f5, 0x8a7d7605, 0x11d83a6a, 0x6540d3e5, 0xfee59f8a, 0x897b4d7a, 0x12de0115, 0x604a9e64, 0xfbefd20b, 0x54e8c18a)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[PickupRelayStruct]:
    if property_count != 10:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHfLHfLHfLHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(100))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27]) != _FAST_IDS:
        data.seek(before)
        return None

    return PickupRelayStruct(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
        dec[20],
        dec[23],
        dec[26],
        dec[29],
    )


def _decode_message1_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_message2_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_message3_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_message4_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_message5_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_message6_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_message7_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_message8_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_message9_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_message10_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xfde3a4f5: ('message1_chance', _decode_message1_chance),
    0x8a7d7605: ('message2_chance', _decode_message2_chance),
    0x11d83a6a: ('message3_chance', _decode_message3_chance),
    0x6540d3e5: ('message4_chance', _decode_message4_chance),
    0xfee59f8a: ('message5_chance', _decode_message5_chance),
    0x897b4d7a: ('message6_chance', _decode_message6_chance),
    0x12de0115: ('message7_chance', _decode_message7_chance),
    0x604a9e64: ('message8_chance', _decode_message8_chance),
    0xfbefd20b: ('message9_chance', _decode_message9_chance),
    0x54e8c18a: ('message10_chance', _decode_message10_chance),
}
