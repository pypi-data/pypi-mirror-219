# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct58(BaseProperty):
    unknown_0x8a58a7f8: int = dataclasses.field(default=1)
    unknown_0x72d0dc87: float = dataclasses.field(default=30.0)
    unknown_0x8686fda9: int = dataclasses.field(default=1)
    unknown_0xdd6a10b1: int = dataclasses.field(default=1)
    wait_time0: float = dataclasses.field(default=1.0)
    wait_time1: float = dataclasses.field(default=1.5)
    wait_time2: float = dataclasses.field(default=2.0)
    wait_time3: float = dataclasses.field(default=3.0)

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

        data.write(b'\x8aX\xa7\xf8')  # 0x8a58a7f8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x8a58a7f8))

        data.write(b'r\xd0\xdc\x87')  # 0x72d0dc87
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x72d0dc87))

        data.write(b'\x86\x86\xfd\xa9')  # 0x8686fda9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x8686fda9))

        data.write(b'\xddj\x10\xb1')  # 0xdd6a10b1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xdd6a10b1))

        data.write(b'\x9dE\xfa\x96')  # 0x9d45fa96
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.wait_time0))

        data.write(b'V\x19)3')  # 0x56192933
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.wait_time1))

        data.write(b'\xd0\x8d[\x9d')  # 0xd08d5b9d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.wait_time2))

        data.write(b'\x1b\xd1\x888')  # 0x1bd18838
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.wait_time3))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x8a58a7f8=data['unknown_0x8a58a7f8'],
            unknown_0x72d0dc87=data['unknown_0x72d0dc87'],
            unknown_0x8686fda9=data['unknown_0x8686fda9'],
            unknown_0xdd6a10b1=data['unknown_0xdd6a10b1'],
            wait_time0=data['wait_time0'],
            wait_time1=data['wait_time1'],
            wait_time2=data['wait_time2'],
            wait_time3=data['wait_time3'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x8a58a7f8': self.unknown_0x8a58a7f8,
            'unknown_0x72d0dc87': self.unknown_0x72d0dc87,
            'unknown_0x8686fda9': self.unknown_0x8686fda9,
            'unknown_0xdd6a10b1': self.unknown_0xdd6a10b1,
            'wait_time0': self.wait_time0,
            'wait_time1': self.wait_time1,
            'wait_time2': self.wait_time2,
            'wait_time3': self.wait_time3,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x8a58a7f8, 0x72d0dc87, 0x8686fda9, 0xdd6a10b1, 0x9d45fa96, 0x56192933, 0xd08d5b9d, 0x1bd18838)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct58]:
    if property_count != 8:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHlLHfLHlLHlLHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(80))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct58(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
        dec[20],
        dec[23],
    )


def _decode_unknown_0x8a58a7f8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x72d0dc87(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8686fda9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xdd6a10b1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_wait_time0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_wait_time1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_wait_time2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_wait_time3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x8a58a7f8: ('unknown_0x8a58a7f8', _decode_unknown_0x8a58a7f8),
    0x72d0dc87: ('unknown_0x72d0dc87', _decode_unknown_0x72d0dc87),
    0x8686fda9: ('unknown_0x8686fda9', _decode_unknown_0x8686fda9),
    0xdd6a10b1: ('unknown_0xdd6a10b1', _decode_unknown_0xdd6a10b1),
    0x9d45fa96: ('wait_time0', _decode_wait_time0),
    0x56192933: ('wait_time1', _decode_wait_time1),
    0xd08d5b9d: ('wait_time2', _decode_wait_time2),
    0x1bd18838: ('wait_time3', _decode_wait_time3),
}
