# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.UnknownStruct10 import UnknownStruct10


@dataclasses.dataclass()
class SpriteStruct(BaseProperty):
    loop: bool = dataclasses.field(default=False)
    unknown_struct10_0x30613ecc: UnknownStruct10 = dataclasses.field(default_factory=UnknownStruct10)
    unknown_struct10_0x19a98a3e: UnknownStruct10 = dataclasses.field(default_factory=UnknownStruct10)
    unknown_struct10_0xb7c11baf: UnknownStruct10 = dataclasses.field(default_factory=UnknownStruct10)
    unknown_struct10_0x4a38e3da: UnknownStruct10 = dataclasses.field(default_factory=UnknownStruct10)
    unknown_struct10_0xe450724b: UnknownStruct10 = dataclasses.field(default_factory=UnknownStruct10)
    unknown_struct10_0xcd98c6b9: UnknownStruct10 = dataclasses.field(default_factory=UnknownStruct10)
    unknown_struct10_0x63f05728: UnknownStruct10 = dataclasses.field(default_factory=UnknownStruct10)
    unknown_struct10_0xed1a3012: UnknownStruct10 = dataclasses.field(default_factory=UnknownStruct10)
    unknown_struct10_0x4372a183: UnknownStruct10 = dataclasses.field(default_factory=UnknownStruct10)
    unknown_struct10_0x2060e2f5: UnknownStruct10 = dataclasses.field(default_factory=UnknownStruct10)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
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

        data.write(b'\xed\xa4\x7f\xf6')  # 0xeda47ff6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.loop))

        data.write(b'0a>\xcc')  # 0x30613ecc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct10_0x30613ecc.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x19\xa9\x8a>')  # 0x19a98a3e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct10_0x19a98a3e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb7\xc1\x1b\xaf')  # 0xb7c11baf
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct10_0xb7c11baf.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'J8\xe3\xda')  # 0x4a38e3da
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct10_0x4a38e3da.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe4PrK')  # 0xe450724b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct10_0xe450724b.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcd\x98\xc6\xb9')  # 0xcd98c6b9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct10_0xcd98c6b9.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'c\xf0W(')  # 0x63f05728
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct10_0x63f05728.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xed\x1a0\x12')  # 0xed1a3012
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct10_0xed1a3012.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Cr\xa1\x83')  # 0x4372a183
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct10_0x4372a183.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b' `\xe2\xf5')  # 0x2060e2f5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct10_0x2060e2f5.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            loop=data['loop'],
            unknown_struct10_0x30613ecc=UnknownStruct10.from_json(data['unknown_struct10_0x30613ecc']),
            unknown_struct10_0x19a98a3e=UnknownStruct10.from_json(data['unknown_struct10_0x19a98a3e']),
            unknown_struct10_0xb7c11baf=UnknownStruct10.from_json(data['unknown_struct10_0xb7c11baf']),
            unknown_struct10_0x4a38e3da=UnknownStruct10.from_json(data['unknown_struct10_0x4a38e3da']),
            unknown_struct10_0xe450724b=UnknownStruct10.from_json(data['unknown_struct10_0xe450724b']),
            unknown_struct10_0xcd98c6b9=UnknownStruct10.from_json(data['unknown_struct10_0xcd98c6b9']),
            unknown_struct10_0x63f05728=UnknownStruct10.from_json(data['unknown_struct10_0x63f05728']),
            unknown_struct10_0xed1a3012=UnknownStruct10.from_json(data['unknown_struct10_0xed1a3012']),
            unknown_struct10_0x4372a183=UnknownStruct10.from_json(data['unknown_struct10_0x4372a183']),
            unknown_struct10_0x2060e2f5=UnknownStruct10.from_json(data['unknown_struct10_0x2060e2f5']),
        )

    def to_json(self) -> dict:
        return {
            'loop': self.loop,
            'unknown_struct10_0x30613ecc': self.unknown_struct10_0x30613ecc.to_json(),
            'unknown_struct10_0x19a98a3e': self.unknown_struct10_0x19a98a3e.to_json(),
            'unknown_struct10_0xb7c11baf': self.unknown_struct10_0xb7c11baf.to_json(),
            'unknown_struct10_0x4a38e3da': self.unknown_struct10_0x4a38e3da.to_json(),
            'unknown_struct10_0xe450724b': self.unknown_struct10_0xe450724b.to_json(),
            'unknown_struct10_0xcd98c6b9': self.unknown_struct10_0xcd98c6b9.to_json(),
            'unknown_struct10_0x63f05728': self.unknown_struct10_0x63f05728.to_json(),
            'unknown_struct10_0xed1a3012': self.unknown_struct10_0xed1a3012.to_json(),
            'unknown_struct10_0x4372a183': self.unknown_struct10_0x4372a183.to_json(),
            'unknown_struct10_0x2060e2f5': self.unknown_struct10_0x2060e2f5.to_json(),
        }


def _decode_loop(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_struct10_0x30613ecc(data: typing.BinaryIO, property_size: int):
    return UnknownStruct10.from_stream(data, property_size)


def _decode_unknown_struct10_0x19a98a3e(data: typing.BinaryIO, property_size: int):
    return UnknownStruct10.from_stream(data, property_size)


def _decode_unknown_struct10_0xb7c11baf(data: typing.BinaryIO, property_size: int):
    return UnknownStruct10.from_stream(data, property_size)


def _decode_unknown_struct10_0x4a38e3da(data: typing.BinaryIO, property_size: int):
    return UnknownStruct10.from_stream(data, property_size)


def _decode_unknown_struct10_0xe450724b(data: typing.BinaryIO, property_size: int):
    return UnknownStruct10.from_stream(data, property_size)


def _decode_unknown_struct10_0xcd98c6b9(data: typing.BinaryIO, property_size: int):
    return UnknownStruct10.from_stream(data, property_size)


def _decode_unknown_struct10_0x63f05728(data: typing.BinaryIO, property_size: int):
    return UnknownStruct10.from_stream(data, property_size)


def _decode_unknown_struct10_0xed1a3012(data: typing.BinaryIO, property_size: int):
    return UnknownStruct10.from_stream(data, property_size)


def _decode_unknown_struct10_0x4372a183(data: typing.BinaryIO, property_size: int):
    return UnknownStruct10.from_stream(data, property_size)


def _decode_unknown_struct10_0x2060e2f5(data: typing.BinaryIO, property_size: int):
    return UnknownStruct10.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xeda47ff6: ('loop', _decode_loop),
    0x30613ecc: ('unknown_struct10_0x30613ecc', _decode_unknown_struct10_0x30613ecc),
    0x19a98a3e: ('unknown_struct10_0x19a98a3e', _decode_unknown_struct10_0x19a98a3e),
    0xb7c11baf: ('unknown_struct10_0xb7c11baf', _decode_unknown_struct10_0xb7c11baf),
    0x4a38e3da: ('unknown_struct10_0x4a38e3da', _decode_unknown_struct10_0x4a38e3da),
    0xe450724b: ('unknown_struct10_0xe450724b', _decode_unknown_struct10_0xe450724b),
    0xcd98c6b9: ('unknown_struct10_0xcd98c6b9', _decode_unknown_struct10_0xcd98c6b9),
    0x63f05728: ('unknown_struct10_0x63f05728', _decode_unknown_struct10_0x63f05728),
    0xed1a3012: ('unknown_struct10_0xed1a3012', _decode_unknown_struct10_0xed1a3012),
    0x4372a183: ('unknown_struct10_0x4372a183', _decode_unknown_struct10_0x4372a183),
    0x2060e2f5: ('unknown_struct10_0x2060e2f5', _decode_unknown_struct10_0x2060e2f5),
}
