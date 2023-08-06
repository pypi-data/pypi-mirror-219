# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class CounterConditions(BaseProperty):
    counter_condition1: int = dataclasses.field(default=1)
    counter_condition2: int = dataclasses.field(default=2)
    counter_condition3: int = dataclasses.field(default=3)
    counter_condition4: int = dataclasses.field(default=4)
    counter_condition5: int = dataclasses.field(default=5)
    counter_condition6: int = dataclasses.field(default=6)
    counter_condition7: int = dataclasses.field(default=7)
    counter_condition8: int = dataclasses.field(default=8)
    counter_condition9: int = dataclasses.field(default=9)
    counter_condition10: int = dataclasses.field(default=10)

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

        data.write(b'\x16(\xf2:')  # 0x1628f23a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.counter_condition1))

        data.write(b'\x04\x9d]\xd4')  # 0x49d5dd4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.counter_condition2))

        data.write(b'\xbc!:\xb1')  # 0xbc213ab1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.counter_condition3))

        data.write(b'!\xf6\x02\x08')  # 0x21f60208
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.counter_condition4))

        data.write(b'\x99Jem')  # 0x994a656d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.counter_condition5))

        data.write(b'\x8b\xff\xca\x83')  # 0x8bffca83
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.counter_condition6))

        data.write(b'3C\xad\xe6')  # 0x3343ade6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.counter_condition7))

        data.write(b'k \xbd\xb0')  # 0x6b20bdb0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.counter_condition8))

        data.write(b'\xd3\x9c\xda\xd5')  # 0xd39cdad5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.counter_condition9))

        data.write(b'\x92\x15\xe8\x13')  # 0x9215e813
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.counter_condition10))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            counter_condition1=data['counter_condition1'],
            counter_condition2=data['counter_condition2'],
            counter_condition3=data['counter_condition3'],
            counter_condition4=data['counter_condition4'],
            counter_condition5=data['counter_condition5'],
            counter_condition6=data['counter_condition6'],
            counter_condition7=data['counter_condition7'],
            counter_condition8=data['counter_condition8'],
            counter_condition9=data['counter_condition9'],
            counter_condition10=data['counter_condition10'],
        )

    def to_json(self) -> dict:
        return {
            'counter_condition1': self.counter_condition1,
            'counter_condition2': self.counter_condition2,
            'counter_condition3': self.counter_condition3,
            'counter_condition4': self.counter_condition4,
            'counter_condition5': self.counter_condition5,
            'counter_condition6': self.counter_condition6,
            'counter_condition7': self.counter_condition7,
            'counter_condition8': self.counter_condition8,
            'counter_condition9': self.counter_condition9,
            'counter_condition10': self.counter_condition10,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x1628f23a, 0x49d5dd4, 0xbc213ab1, 0x21f60208, 0x994a656d, 0x8bffca83, 0x3343ade6, 0x6b20bdb0, 0xd39cdad5, 0x9215e813)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[CounterConditions]:
    if property_count != 10:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHlLHlLHlLHlLHlLHlLHlLHlLHlLHl')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(100))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27]) != _FAST_IDS:
        data.seek(before)
        return None

    return CounterConditions(
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


def _decode_counter_condition1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_counter_condition2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_counter_condition3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_counter_condition4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_counter_condition5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_counter_condition6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_counter_condition7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_counter_condition8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_counter_condition9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_counter_condition10(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x1628f23a: ('counter_condition1', _decode_counter_condition1),
    0x49d5dd4: ('counter_condition2', _decode_counter_condition2),
    0xbc213ab1: ('counter_condition3', _decode_counter_condition3),
    0x21f60208: ('counter_condition4', _decode_counter_condition4),
    0x994a656d: ('counter_condition5', _decode_counter_condition5),
    0x8bffca83: ('counter_condition6', _decode_counter_condition6),
    0x3343ade6: ('counter_condition7', _decode_counter_condition7),
    0x6b20bdb0: ('counter_condition8', _decode_counter_condition8),
    0xd39cdad5: ('counter_condition9', _decode_counter_condition9),
    0x9215e813: ('counter_condition10', _decode_counter_condition10),
}
