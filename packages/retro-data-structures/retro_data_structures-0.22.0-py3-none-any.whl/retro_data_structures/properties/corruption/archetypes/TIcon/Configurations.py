# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class Configurations(BaseProperty):
    unknown_0x3058aff2: float = dataclasses.field(default=0.0)
    unknown_0xf1d67032: float = dataclasses.field(default=0.0)
    unknown_0x68341633: float = dataclasses.field(default=0.0)
    unknown_0xa9bac9f3: float = dataclasses.field(default=0.0)
    unknown_0x8081dc70: float = dataclasses.field(default=0.0)
    unknown_0x410f03b0: float = dataclasses.field(default=0.0)
    unknown_0xd8ed65b1: float = dataclasses.field(default=0.0)
    unknown_0x1963ba71: float = dataclasses.field(default=0.0)
    unknown_0x8a9b4eb7: float = dataclasses.field(default=0.0)

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
        data.write(b'\x00\t')  # 9 properties

        data.write(b'0X\xaf\xf2')  # 0x3058aff2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3058aff2))

        data.write(b'\xf1\xd6p2')  # 0xf1d67032
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf1d67032))

        data.write(b'h4\x163')  # 0x68341633
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x68341633))

        data.write(b'\xa9\xba\xc9\xf3')  # 0xa9bac9f3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa9bac9f3))

        data.write(b'\x80\x81\xdcp')  # 0x8081dc70
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8081dc70))

        data.write(b'A\x0f\x03\xb0')  # 0x410f03b0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x410f03b0))

        data.write(b'\xd8\xede\xb1')  # 0xd8ed65b1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd8ed65b1))

        data.write(b'\x19c\xbaq')  # 0x1963ba71
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x1963ba71))

        data.write(b'\x8a\x9bN\xb7')  # 0x8a9b4eb7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8a9b4eb7))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x3058aff2=data['unknown_0x3058aff2'],
            unknown_0xf1d67032=data['unknown_0xf1d67032'],
            unknown_0x68341633=data['unknown_0x68341633'],
            unknown_0xa9bac9f3=data['unknown_0xa9bac9f3'],
            unknown_0x8081dc70=data['unknown_0x8081dc70'],
            unknown_0x410f03b0=data['unknown_0x410f03b0'],
            unknown_0xd8ed65b1=data['unknown_0xd8ed65b1'],
            unknown_0x1963ba71=data['unknown_0x1963ba71'],
            unknown_0x8a9b4eb7=data['unknown_0x8a9b4eb7'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x3058aff2': self.unknown_0x3058aff2,
            'unknown_0xf1d67032': self.unknown_0xf1d67032,
            'unknown_0x68341633': self.unknown_0x68341633,
            'unknown_0xa9bac9f3': self.unknown_0xa9bac9f3,
            'unknown_0x8081dc70': self.unknown_0x8081dc70,
            'unknown_0x410f03b0': self.unknown_0x410f03b0,
            'unknown_0xd8ed65b1': self.unknown_0xd8ed65b1,
            'unknown_0x1963ba71': self.unknown_0x1963ba71,
            'unknown_0x8a9b4eb7': self.unknown_0x8a9b4eb7,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x3058aff2, 0xf1d67032, 0x68341633, 0xa9bac9f3, 0x8081dc70, 0x410f03b0, 0xd8ed65b1, 0x1963ba71, 0x8a9b4eb7)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[Configurations]:
    if property_count != 9:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHfLHfLHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(90))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24]) != _FAST_IDS:
        data.seek(before)
        return None

    return Configurations(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
        dec[20],
        dec[23],
        dec[26],
    )


def _decode_unknown_0x3058aff2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf1d67032(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x68341633(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa9bac9f3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8081dc70(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x410f03b0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd8ed65b1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x1963ba71(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8a9b4eb7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x3058aff2: ('unknown_0x3058aff2', _decode_unknown_0x3058aff2),
    0xf1d67032: ('unknown_0xf1d67032', _decode_unknown_0xf1d67032),
    0x68341633: ('unknown_0x68341633', _decode_unknown_0x68341633),
    0xa9bac9f3: ('unknown_0xa9bac9f3', _decode_unknown_0xa9bac9f3),
    0x8081dc70: ('unknown_0x8081dc70', _decode_unknown_0x8081dc70),
    0x410f03b0: ('unknown_0x410f03b0', _decode_unknown_0x410f03b0),
    0xd8ed65b1: ('unknown_0xd8ed65b1', _decode_unknown_0xd8ed65b1),
    0x1963ba71: ('unknown_0x1963ba71', _decode_unknown_0x1963ba71),
    0x8a9b4eb7: ('unknown_0x8a9b4eb7', _decode_unknown_0x8a9b4eb7),
}
