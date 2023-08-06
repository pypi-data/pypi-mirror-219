# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct33(BaseProperty):
    initial_morph_time: float = dataclasses.field(default=15.0)
    unknown_0x41ed6a42: float = dataclasses.field(default=10.0)
    unknown_0x420da002: float = dataclasses.field(default=50.0)
    unknown_0xa2675081: float = dataclasses.field(default=20.0)
    unknown_0x413aee5b: float = dataclasses.field(default=30.0)
    unknown_0x9fe347b5: float = dataclasses.field(default=9.0)
    unknown_0xc8ed17f6: float = dataclasses.field(default=11.0)
    cloak_time: float = dataclasses.field(default=1.0)
    decloak_time: float = dataclasses.field(default=0.25)
    unknown_0x587fa387: float = dataclasses.field(default=3.0)
    unknown_0x3e9ac5f3: float = dataclasses.field(default=4.0)

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
        data.write(b'\x00\x0b')  # 11 properties

        data.write(b'E\x16\x11\t')  # 0x45161109
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.initial_morph_time))

        data.write(b'A\xedjB')  # 0x41ed6a42
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x41ed6a42))

        data.write(b'B\r\xa0\x02')  # 0x420da002
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x420da002))

        data.write(b'\xa2gP\x81')  # 0xa2675081
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa2675081))

        data.write(b'A:\xee[')  # 0x413aee5b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x413aee5b))

        data.write(b'\x9f\xe3G\xb5')  # 0x9fe347b5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x9fe347b5))

        data.write(b'\xc8\xed\x17\xf6')  # 0xc8ed17f6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc8ed17f6))

        data.write(b'8\x8b\xc3\x1f')  # 0x388bc31f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.cloak_time))

        data.write(b'C\x19\xc8@')  # 0x4319c840
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.decloak_time))

        data.write(b'X\x7f\xa3\x87')  # 0x587fa387
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x587fa387))

        data.write(b'>\x9a\xc5\xf3')  # 0x3e9ac5f3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3e9ac5f3))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            initial_morph_time=data['initial_morph_time'],
            unknown_0x41ed6a42=data['unknown_0x41ed6a42'],
            unknown_0x420da002=data['unknown_0x420da002'],
            unknown_0xa2675081=data['unknown_0xa2675081'],
            unknown_0x413aee5b=data['unknown_0x413aee5b'],
            unknown_0x9fe347b5=data['unknown_0x9fe347b5'],
            unknown_0xc8ed17f6=data['unknown_0xc8ed17f6'],
            cloak_time=data['cloak_time'],
            decloak_time=data['decloak_time'],
            unknown_0x587fa387=data['unknown_0x587fa387'],
            unknown_0x3e9ac5f3=data['unknown_0x3e9ac5f3'],
        )

    def to_json(self) -> dict:
        return {
            'initial_morph_time': self.initial_morph_time,
            'unknown_0x41ed6a42': self.unknown_0x41ed6a42,
            'unknown_0x420da002': self.unknown_0x420da002,
            'unknown_0xa2675081': self.unknown_0xa2675081,
            'unknown_0x413aee5b': self.unknown_0x413aee5b,
            'unknown_0x9fe347b5': self.unknown_0x9fe347b5,
            'unknown_0xc8ed17f6': self.unknown_0xc8ed17f6,
            'cloak_time': self.cloak_time,
            'decloak_time': self.decloak_time,
            'unknown_0x587fa387': self.unknown_0x587fa387,
            'unknown_0x3e9ac5f3': self.unknown_0x3e9ac5f3,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x45161109, 0x41ed6a42, 0x420da002, 0xa2675081, 0x413aee5b, 0x9fe347b5, 0xc8ed17f6, 0x388bc31f, 0x4319c840, 0x587fa387, 0x3e9ac5f3)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct33]:
    if property_count != 11:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(110))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27], dec[30]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct33(
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
        dec[32],
    )


def _decode_initial_morph_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x41ed6a42(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x420da002(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa2675081(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x413aee5b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x9fe347b5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc8ed17f6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_cloak_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_decloak_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x587fa387(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x3e9ac5f3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x45161109: ('initial_morph_time', _decode_initial_morph_time),
    0x41ed6a42: ('unknown_0x41ed6a42', _decode_unknown_0x41ed6a42),
    0x420da002: ('unknown_0x420da002', _decode_unknown_0x420da002),
    0xa2675081: ('unknown_0xa2675081', _decode_unknown_0xa2675081),
    0x413aee5b: ('unknown_0x413aee5b', _decode_unknown_0x413aee5b),
    0x9fe347b5: ('unknown_0x9fe347b5', _decode_unknown_0x9fe347b5),
    0xc8ed17f6: ('unknown_0xc8ed17f6', _decode_unknown_0xc8ed17f6),
    0x388bc31f: ('cloak_time', _decode_cloak_time),
    0x4319c840: ('decloak_time', _decode_decloak_time),
    0x587fa387: ('unknown_0x587fa387', _decode_unknown_0x587fa387),
    0x3e9ac5f3: ('unknown_0x3e9ac5f3', _decode_unknown_0x3e9ac5f3),
}
