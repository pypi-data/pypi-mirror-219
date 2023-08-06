# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct29(BaseProperty):
    blinking_enabled: bool = dataclasses.field(default=True)
    unknown_0x9b131110: float = dataclasses.field(default=2.0)
    unknown_0xa5a6d998: float = dataclasses.field(default=6.0)
    unknown_0xd9f6253b: int = dataclasses.field(default=3)
    unknown_0x0896fde0: float = dataclasses.field(default=0.10000000149011612)
    unknown_0x5f98ada3: float = dataclasses.field(default=0.5)
    unknown_0xc3230652: float = dataclasses.field(default=20.0)

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
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'G\xc86\xc5')  # 0x47c836c5
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.blinking_enabled))

        data.write(b'\x9b\x13\x11\x10')  # 0x9b131110
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x9b131110))

        data.write(b'\xa5\xa6\xd9\x98')  # 0xa5a6d998
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa5a6d998))

        data.write(b'\xd9\xf6%;')  # 0xd9f6253b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xd9f6253b))

        data.write(b'\x08\x96\xfd\xe0')  # 0x896fde0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0896fde0))

        data.write(b'_\x98\xad\xa3')  # 0x5f98ada3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5f98ada3))

        data.write(b'\xc3#\x06R')  # 0xc3230652
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc3230652))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            blinking_enabled=data['blinking_enabled'],
            unknown_0x9b131110=data['unknown_0x9b131110'],
            unknown_0xa5a6d998=data['unknown_0xa5a6d998'],
            unknown_0xd9f6253b=data['unknown_0xd9f6253b'],
            unknown_0x0896fde0=data['unknown_0x0896fde0'],
            unknown_0x5f98ada3=data['unknown_0x5f98ada3'],
            unknown_0xc3230652=data['unknown_0xc3230652'],
        )

    def to_json(self) -> dict:
        return {
            'blinking_enabled': self.blinking_enabled,
            'unknown_0x9b131110': self.unknown_0x9b131110,
            'unknown_0xa5a6d998': self.unknown_0xa5a6d998,
            'unknown_0xd9f6253b': self.unknown_0xd9f6253b,
            'unknown_0x0896fde0': self.unknown_0x0896fde0,
            'unknown_0x5f98ada3': self.unknown_0x5f98ada3,
            'unknown_0xc3230652': self.unknown_0xc3230652,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x47c836c5, 0x9b131110, 0xa5a6d998, 0xd9f6253b, 0x896fde0, 0x5f98ada3, 0xc3230652)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct29]:
    if property_count != 7:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LH?LHfLHfLHlLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(67))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct29(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
        dec[20],
    )


def _decode_blinking_enabled(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x9b131110(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa5a6d998(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd9f6253b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x0896fde0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x5f98ada3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc3230652(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x47c836c5: ('blinking_enabled', _decode_blinking_enabled),
    0x9b131110: ('unknown_0x9b131110', _decode_unknown_0x9b131110),
    0xa5a6d998: ('unknown_0xa5a6d998', _decode_unknown_0xa5a6d998),
    0xd9f6253b: ('unknown_0xd9f6253b', _decode_unknown_0xd9f6253b),
    0x896fde0: ('unknown_0x0896fde0', _decode_unknown_0x0896fde0),
    0x5f98ada3: ('unknown_0x5f98ada3', _decode_unknown_0x5f98ada3),
    0xc3230652: ('unknown_0xc3230652', _decode_unknown_0xc3230652),
}
