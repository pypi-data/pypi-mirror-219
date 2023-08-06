# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class MoleTrainManagerStructB(BaseProperty):
    spawn_delay: float = dataclasses.field(default=1.0)
    unknown_0xe1fac41a: int = dataclasses.field(default=33)
    unknown_0xdaf59171: int = dataclasses.field(default=3)
    unknown_0x2b846018: float = dataclasses.field(default=0.25)
    unknown_0xa11b39c3: float = dataclasses.field(default=0.25)
    flip_time: float = dataclasses.field(default=2.0)
    idle_time: float = dataclasses.field(default=1.25)
    unknown_0x3e5bab9d: float = dataclasses.field(default=-10.0)
    hazard_cart_time: float = dataclasses.field(default=60.0)
    unknown_0x552f8118: float = dataclasses.field(default=30.5)
    unknown_0x86daba3b: float = dataclasses.field(default=20.0)

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
        data.write(b'\x00\x0b')  # 11 properties

        data.write(b'\xd48s\x9d')  # 0xd438739d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.spawn_delay))

        data.write(b'\xe1\xfa\xc4\x1a')  # 0xe1fac41a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xe1fac41a))

        data.write(b'\xda\xf5\x91q')  # 0xdaf59171
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xdaf59171))

        data.write(b'+\x84`\x18')  # 0x2b846018
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2b846018))

        data.write(b'\xa1\x1b9\xc3')  # 0xa11b39c3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa11b39c3))

        data.write(b'@\xaeJ\t')  # 0x40ae4a09
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.flip_time))

        data.write(b'\xd1\x02\x0f,')  # 0xd1020f2c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.idle_time))

        data.write(b'>[\xab\x9d')  # 0x3e5bab9d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3e5bab9d))

        data.write(b'$D}\xc3')  # 0x24447dc3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hazard_cart_time))

        data.write(b'U/\x81\x18')  # 0x552f8118
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x552f8118))

        data.write(b'\x86\xda\xba;')  # 0x86daba3b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x86daba3b))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            spawn_delay=data['spawn_delay'],
            unknown_0xe1fac41a=data['unknown_0xe1fac41a'],
            unknown_0xdaf59171=data['unknown_0xdaf59171'],
            unknown_0x2b846018=data['unknown_0x2b846018'],
            unknown_0xa11b39c3=data['unknown_0xa11b39c3'],
            flip_time=data['flip_time'],
            idle_time=data['idle_time'],
            unknown_0x3e5bab9d=data['unknown_0x3e5bab9d'],
            hazard_cart_time=data['hazard_cart_time'],
            unknown_0x552f8118=data['unknown_0x552f8118'],
            unknown_0x86daba3b=data['unknown_0x86daba3b'],
        )

    def to_json(self) -> dict:
        return {
            'spawn_delay': self.spawn_delay,
            'unknown_0xe1fac41a': self.unknown_0xe1fac41a,
            'unknown_0xdaf59171': self.unknown_0xdaf59171,
            'unknown_0x2b846018': self.unknown_0x2b846018,
            'unknown_0xa11b39c3': self.unknown_0xa11b39c3,
            'flip_time': self.flip_time,
            'idle_time': self.idle_time,
            'unknown_0x3e5bab9d': self.unknown_0x3e5bab9d,
            'hazard_cart_time': self.hazard_cart_time,
            'unknown_0x552f8118': self.unknown_0x552f8118,
            'unknown_0x86daba3b': self.unknown_0x86daba3b,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xd438739d, 0xe1fac41a, 0xdaf59171, 0x2b846018, 0xa11b39c3, 0x40ae4a09, 0xd1020f2c, 0x3e5bab9d, 0x24447dc3, 0x552f8118, 0x86daba3b)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[MoleTrainManagerStructB]:
    if property_count != 11:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHlLHlLHfLHfLHfLHfLHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(110))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27], dec[30]) != _FAST_IDS:
        data.seek(before)
        return None

    return MoleTrainManagerStructB(
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


def _decode_spawn_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe1fac41a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xdaf59171(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x2b846018(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa11b39c3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_flip_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_idle_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x3e5bab9d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hazard_cart_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x552f8118(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x86daba3b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xd438739d: ('spawn_delay', _decode_spawn_delay),
    0xe1fac41a: ('unknown_0xe1fac41a', _decode_unknown_0xe1fac41a),
    0xdaf59171: ('unknown_0xdaf59171', _decode_unknown_0xdaf59171),
    0x2b846018: ('unknown_0x2b846018', _decode_unknown_0x2b846018),
    0xa11b39c3: ('unknown_0xa11b39c3', _decode_unknown_0xa11b39c3),
    0x40ae4a09: ('flip_time', _decode_flip_time),
    0xd1020f2c: ('idle_time', _decode_idle_time),
    0x3e5bab9d: ('unknown_0x3e5bab9d', _decode_unknown_0x3e5bab9d),
    0x24447dc3: ('hazard_cart_time', _decode_hazard_cart_time),
    0x552f8118: ('unknown_0x552f8118', _decode_unknown_0x552f8118),
    0x86daba3b: ('unknown_0x86daba3b', _decode_unknown_0x86daba3b),
}
