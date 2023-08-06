# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct54(BaseProperty):
    time: float = dataclasses.field(default=0.009999999776482582)
    unknown: float = dataclasses.field(default=0.0)
    damping: float = dataclasses.field(default=0.0)
    coloration: float = dataclasses.field(default=0.0)
    cross_talk: float = dataclasses.field(default=0.0)
    mix: float = dataclasses.field(default=0.30000001192092896)

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
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'D3Z\xff')  # 0x44335aff
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.time))

        data.write(b'W$\xcc\xd8')  # 0x5724ccd8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown))

        data.write(b'\xfc\xf4\xaa\xb0')  # 0xfcf4aab0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.damping))

        data.write(b']k\x10\x84')  # 0x5d6b1084
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.coloration))

        data.write(b'\xfb\x11\xa4\x12')  # 0xfb11a412
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.cross_talk))

        data.write(b'\xde\x9d\xd8\xb8')  # 0xde9dd8b8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.mix))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            time=data['time'],
            unknown=data['unknown'],
            damping=data['damping'],
            coloration=data['coloration'],
            cross_talk=data['cross_talk'],
            mix=data['mix'],
        )

    def to_json(self) -> dict:
        return {
            'time': self.time,
            'unknown': self.unknown,
            'damping': self.damping,
            'coloration': self.coloration,
            'cross_talk': self.cross_talk,
            'mix': self.mix,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x44335aff, 0x5724ccd8, 0xfcf4aab0, 0x5d6b1084, 0xfb11a412, 0xde9dd8b8)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct54]:
    if property_count != 6:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(60))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct54(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
    )


def _decode_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_damping(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_coloration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_cross_talk(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_mix(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x44335aff: ('time', _decode_time),
    0x5724ccd8: ('unknown', _decode_unknown),
    0xfcf4aab0: ('damping', _decode_damping),
    0x5d6b1084: ('coloration', _decode_coloration),
    0xfb11a412: ('cross_talk', _decode_cross_talk),
    0xde9dd8b8: ('mix', _decode_mix),
}
