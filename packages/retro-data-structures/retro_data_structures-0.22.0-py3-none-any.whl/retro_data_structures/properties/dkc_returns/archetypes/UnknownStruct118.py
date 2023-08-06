# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct118(BaseProperty):
    acceleration: float = dataclasses.field(default=5.0)
    deceleration: float = dataclasses.field(default=25.0)
    max_speed: float = dataclasses.field(default=15.0)
    unknown_0x7e1338f8: float = dataclasses.field(default=2.0)
    unknown_0x3cd77ebc: float = dataclasses.field(default=0.0)
    unknown_0xe79a390f: float = dataclasses.field(default=0.10000000149011612)
    unknown_0x8f922c1c: float = dataclasses.field(default=5.0)
    unknown_0xd4c6cc95: float = dataclasses.field(default=0.5)
    unknown_0xadb1d371: float = dataclasses.field(default=0.10000000149011612)
    unknown_0x89732f60: float = dataclasses.field(default=10.0)
    unknown_0x3b774d55: float = dataclasses.field(default=15.0)
    max_additive_change: float = dataclasses.field(default=0.10000000149011612)

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
        data.write(b'\x00\x0c')  # 12 properties

        data.write(b'9\xfbyx')  # 0x39fb7978
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.acceleration))

        data.write(b'\x9e\xc4\xfc\x10')  # 0x9ec4fc10
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.deceleration))

        data.write(b'\x82\xdb\x0c\xbe')  # 0x82db0cbe
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_speed))

        data.write(b'~\x138\xf8')  # 0x7e1338f8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x7e1338f8))

        data.write(b'<\xd7~\xbc')  # 0x3cd77ebc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3cd77ebc))

        data.write(b'\xe7\x9a9\x0f')  # 0xe79a390f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe79a390f))

        data.write(b'\x8f\x92,\x1c')  # 0x8f922c1c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8f922c1c))

        data.write(b'\xd4\xc6\xcc\x95')  # 0xd4c6cc95
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd4c6cc95))

        data.write(b'\xad\xb1\xd3q')  # 0xadb1d371
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xadb1d371))

        data.write(b'\x89s/`')  # 0x89732f60
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x89732f60))

        data.write(b';wMU')  # 0x3b774d55
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3b774d55))

        data.write(b'M\xe1tr')  # 0x4de17472
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_additive_change))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            acceleration=data['acceleration'],
            deceleration=data['deceleration'],
            max_speed=data['max_speed'],
            unknown_0x7e1338f8=data['unknown_0x7e1338f8'],
            unknown_0x3cd77ebc=data['unknown_0x3cd77ebc'],
            unknown_0xe79a390f=data['unknown_0xe79a390f'],
            unknown_0x8f922c1c=data['unknown_0x8f922c1c'],
            unknown_0xd4c6cc95=data['unknown_0xd4c6cc95'],
            unknown_0xadb1d371=data['unknown_0xadb1d371'],
            unknown_0x89732f60=data['unknown_0x89732f60'],
            unknown_0x3b774d55=data['unknown_0x3b774d55'],
            max_additive_change=data['max_additive_change'],
        )

    def to_json(self) -> dict:
        return {
            'acceleration': self.acceleration,
            'deceleration': self.deceleration,
            'max_speed': self.max_speed,
            'unknown_0x7e1338f8': self.unknown_0x7e1338f8,
            'unknown_0x3cd77ebc': self.unknown_0x3cd77ebc,
            'unknown_0xe79a390f': self.unknown_0xe79a390f,
            'unknown_0x8f922c1c': self.unknown_0x8f922c1c,
            'unknown_0xd4c6cc95': self.unknown_0xd4c6cc95,
            'unknown_0xadb1d371': self.unknown_0xadb1d371,
            'unknown_0x89732f60': self.unknown_0x89732f60,
            'unknown_0x3b774d55': self.unknown_0x3b774d55,
            'max_additive_change': self.max_additive_change,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x39fb7978, 0x9ec4fc10, 0x82db0cbe, 0x7e1338f8, 0x3cd77ebc, 0xe79a390f, 0x8f922c1c, 0xd4c6cc95, 0xadb1d371, 0x89732f60, 0x3b774d55, 0x4de17472)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct118]:
    if property_count != 12:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(120))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27], dec[30], dec[33]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct118(
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
        dec[35],
    )


def _decode_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_deceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x7e1338f8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x3cd77ebc(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe79a390f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8f922c1c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd4c6cc95(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xadb1d371(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x89732f60(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x3b774d55(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_additive_change(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x39fb7978: ('acceleration', _decode_acceleration),
    0x9ec4fc10: ('deceleration', _decode_deceleration),
    0x82db0cbe: ('max_speed', _decode_max_speed),
    0x7e1338f8: ('unknown_0x7e1338f8', _decode_unknown_0x7e1338f8),
    0x3cd77ebc: ('unknown_0x3cd77ebc', _decode_unknown_0x3cd77ebc),
    0xe79a390f: ('unknown_0xe79a390f', _decode_unknown_0xe79a390f),
    0x8f922c1c: ('unknown_0x8f922c1c', _decode_unknown_0x8f922c1c),
    0xd4c6cc95: ('unknown_0xd4c6cc95', _decode_unknown_0xd4c6cc95),
    0xadb1d371: ('unknown_0xadb1d371', _decode_unknown_0xadb1d371),
    0x89732f60: ('unknown_0x89732f60', _decode_unknown_0x89732f60),
    0x3b774d55: ('unknown_0x3b774d55', _decode_unknown_0x3b774d55),
    0x4de17472: ('max_additive_change', _decode_max_additive_change),
}
