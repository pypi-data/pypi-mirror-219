# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.corruption as enums


@dataclasses.dataclass()
class UnknownStruct63(BaseProperty):
    unknown_0x04131a2a: enums.Unknown = dataclasses.field(default=enums.Unknown.Unknown1)
    unknown_0x868cfe92: bool = dataclasses.field(default=True)
    unknown_0xf1943b5a: bool = dataclasses.field(default=False)
    unknown_0x44bf1dc9: int = dataclasses.field(default=0)
    unknown_0x7c538ed3: int = dataclasses.field(default=0)
    unknown_0xfcd2a1a0: int = dataclasses.field(default=0)
    unknown_0x1aec3e02: int = dataclasses.field(default=0)
    unknown_0xe0e4573d: int = dataclasses.field(default=0)
    unknown_0x21103ec1: int = dataclasses.field(default=0)
    unknown_0xc7c06435: int = dataclasses.field(default=0)

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
        data.write(b'\x00\n')  # 10 properties

        data.write(b'\x04\x13\x1a*')  # 0x4131a2a
        data.write(b'\x00\x04')  # size
        self.unknown_0x04131a2a.to_stream(data)

        data.write(b'\x86\x8c\xfe\x92')  # 0x868cfe92
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x868cfe92))

        data.write(b'\xf1\x94;Z')  # 0xf1943b5a
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xf1943b5a))

        data.write(b'D\xbf\x1d\xc9')  # 0x44bf1dc9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x44bf1dc9))

        data.write(b'|S\x8e\xd3')  # 0x7c538ed3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x7c538ed3))

        data.write(b'\xfc\xd2\xa1\xa0')  # 0xfcd2a1a0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xfcd2a1a0))

        data.write(b'\x1a\xec>\x02')  # 0x1aec3e02
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x1aec3e02))

        data.write(b'\xe0\xe4W=')  # 0xe0e4573d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xe0e4573d))

        data.write(b'!\x10>\xc1')  # 0x21103ec1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x21103ec1))

        data.write(b'\xc7\xc0d5')  # 0xc7c06435
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xc7c06435))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x04131a2a=enums.Unknown.from_json(data['unknown_0x04131a2a']),
            unknown_0x868cfe92=data['unknown_0x868cfe92'],
            unknown_0xf1943b5a=data['unknown_0xf1943b5a'],
            unknown_0x44bf1dc9=data['unknown_0x44bf1dc9'],
            unknown_0x7c538ed3=data['unknown_0x7c538ed3'],
            unknown_0xfcd2a1a0=data['unknown_0xfcd2a1a0'],
            unknown_0x1aec3e02=data['unknown_0x1aec3e02'],
            unknown_0xe0e4573d=data['unknown_0xe0e4573d'],
            unknown_0x21103ec1=data['unknown_0x21103ec1'],
            unknown_0xc7c06435=data['unknown_0xc7c06435'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x04131a2a': self.unknown_0x04131a2a.to_json(),
            'unknown_0x868cfe92': self.unknown_0x868cfe92,
            'unknown_0xf1943b5a': self.unknown_0xf1943b5a,
            'unknown_0x44bf1dc9': self.unknown_0x44bf1dc9,
            'unknown_0x7c538ed3': self.unknown_0x7c538ed3,
            'unknown_0xfcd2a1a0': self.unknown_0xfcd2a1a0,
            'unknown_0x1aec3e02': self.unknown_0x1aec3e02,
            'unknown_0xe0e4573d': self.unknown_0xe0e4573d,
            'unknown_0x21103ec1': self.unknown_0x21103ec1,
            'unknown_0xc7c06435': self.unknown_0xc7c06435,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x4131a2a, 0x868cfe92, 0xf1943b5a, 0x44bf1dc9, 0x7c538ed3, 0xfcd2a1a0, 0x1aec3e02, 0xe0e4573d, 0x21103ec1, 0xc7c06435)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct63]:
    if property_count != 10:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHLLH?LH?LHlLHlLHlLHlLHlLHlLHl')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(94))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct63(
        enums.Unknown(dec[2]),
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


def _decode_unknown_0x04131a2a(data: typing.BinaryIO, property_size: int):
    return enums.Unknown.from_stream(data)


def _decode_unknown_0x868cfe92(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xf1943b5a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x44bf1dc9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x7c538ed3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xfcd2a1a0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x1aec3e02(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xe0e4573d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x21103ec1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xc7c06435(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x4131a2a: ('unknown_0x04131a2a', _decode_unknown_0x04131a2a),
    0x868cfe92: ('unknown_0x868cfe92', _decode_unknown_0x868cfe92),
    0xf1943b5a: ('unknown_0xf1943b5a', _decode_unknown_0xf1943b5a),
    0x44bf1dc9: ('unknown_0x44bf1dc9', _decode_unknown_0x44bf1dc9),
    0x7c538ed3: ('unknown_0x7c538ed3', _decode_unknown_0x7c538ed3),
    0xfcd2a1a0: ('unknown_0xfcd2a1a0', _decode_unknown_0xfcd2a1a0),
    0x1aec3e02: ('unknown_0x1aec3e02', _decode_unknown_0x1aec3e02),
    0xe0e4573d: ('unknown_0xe0e4573d', _decode_unknown_0xe0e4573d),
    0x21103ec1: ('unknown_0x21103ec1', _decode_unknown_0x21103ec1),
    0xc7c06435: ('unknown_0xc7c06435', _decode_unknown_0xc7c06435),
}
