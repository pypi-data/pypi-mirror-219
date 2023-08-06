# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct279 import UnknownStruct279
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct280 import UnknownStruct280
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct281 import UnknownStruct281
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct282 import UnknownStruct282
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct283 import UnknownStruct283
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct284 import UnknownStruct284
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct58 import UnknownStruct58


@dataclasses.dataclass()
class UnknownStruct285(BaseProperty):
    unknown_struct279: UnknownStruct279 = dataclasses.field(default_factory=UnknownStruct279)
    unknown_struct58_0xc9045a02: UnknownStruct58 = dataclasses.field(default_factory=UnknownStruct58)
    unknown_struct280: UnknownStruct280 = dataclasses.field(default_factory=UnknownStruct280)
    unknown_struct58_0xfab2f514: UnknownStruct58 = dataclasses.field(default_factory=UnknownStruct58)
    unknown_struct281: UnknownStruct281 = dataclasses.field(default_factory=UnknownStruct281)
    unknown_0x7a5e5e73: UnknownStruct281 = dataclasses.field(default_factory=UnknownStruct281)
    unknown_struct282: UnknownStruct282 = dataclasses.field(default_factory=UnknownStruct282)
    unknown_struct283: UnknownStruct283 = dataclasses.field(default_factory=UnknownStruct283)
    unknown_struct284: UnknownStruct284 = dataclasses.field(default_factory=UnknownStruct284)
    unknown_0x016768be: UnknownStruct284 = dataclasses.field(default_factory=UnknownStruct284)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

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
        data.write(b'\x00\n')  # 10 properties

        data.write(b'\x16\xd2\x06@')  # 0x16d20640
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct279.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc9\x04Z\x02')  # 0xc9045a02
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct58_0xc9045a02.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc5\xa3\x1f\xc4')  # 0xc5a31fc4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct280.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfa\xb2\xf5\x14')  # 0xfab2f514
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct58_0xfab2f514.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'jUI\xa3')  # 0x6a5549a3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct281.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'z^^s')  # 0x7a5e5e73
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x7a5e5e73.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'c\xcd\x83\x9f')  # 0x63cd839f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct282.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf1z\xef\x10')  # 0xf17aef10
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct283.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc92\xf0\x84')  # 0xc932f084
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct284.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x01gh\xbe')  # 0x16768be
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x016768be.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_struct279=UnknownStruct279.from_json(data['unknown_struct279']),
            unknown_struct58_0xc9045a02=UnknownStruct58.from_json(data['unknown_struct58_0xc9045a02']),
            unknown_struct280=UnknownStruct280.from_json(data['unknown_struct280']),
            unknown_struct58_0xfab2f514=UnknownStruct58.from_json(data['unknown_struct58_0xfab2f514']),
            unknown_struct281=UnknownStruct281.from_json(data['unknown_struct281']),
            unknown_0x7a5e5e73=UnknownStruct281.from_json(data['unknown_0x7a5e5e73']),
            unknown_struct282=UnknownStruct282.from_json(data['unknown_struct282']),
            unknown_struct283=UnknownStruct283.from_json(data['unknown_struct283']),
            unknown_struct284=UnknownStruct284.from_json(data['unknown_struct284']),
            unknown_0x016768be=UnknownStruct284.from_json(data['unknown_0x016768be']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_struct279': self.unknown_struct279.to_json(),
            'unknown_struct58_0xc9045a02': self.unknown_struct58_0xc9045a02.to_json(),
            'unknown_struct280': self.unknown_struct280.to_json(),
            'unknown_struct58_0xfab2f514': self.unknown_struct58_0xfab2f514.to_json(),
            'unknown_struct281': self.unknown_struct281.to_json(),
            'unknown_0x7a5e5e73': self.unknown_0x7a5e5e73.to_json(),
            'unknown_struct282': self.unknown_struct282.to_json(),
            'unknown_struct283': self.unknown_struct283.to_json(),
            'unknown_struct284': self.unknown_struct284.to_json(),
            'unknown_0x016768be': self.unknown_0x016768be.to_json(),
        }


def _decode_unknown_struct279(data: typing.BinaryIO, property_size: int):
    return UnknownStruct279.from_stream(data, property_size)


def _decode_unknown_struct58_0xc9045a02(data: typing.BinaryIO, property_size: int):
    return UnknownStruct58.from_stream(data, property_size)


def _decode_unknown_struct280(data: typing.BinaryIO, property_size: int):
    return UnknownStruct280.from_stream(data, property_size)


def _decode_unknown_struct58_0xfab2f514(data: typing.BinaryIO, property_size: int):
    return UnknownStruct58.from_stream(data, property_size)


def _decode_unknown_struct281(data: typing.BinaryIO, property_size: int):
    return UnknownStruct281.from_stream(data, property_size)


def _decode_unknown_0x7a5e5e73(data: typing.BinaryIO, property_size: int):
    return UnknownStruct281.from_stream(data, property_size)


def _decode_unknown_struct282(data: typing.BinaryIO, property_size: int):
    return UnknownStruct282.from_stream(data, property_size)


def _decode_unknown_struct283(data: typing.BinaryIO, property_size: int):
    return UnknownStruct283.from_stream(data, property_size)


def _decode_unknown_struct284(data: typing.BinaryIO, property_size: int):
    return UnknownStruct284.from_stream(data, property_size)


def _decode_unknown_0x016768be(data: typing.BinaryIO, property_size: int):
    return UnknownStruct284.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x16d20640: ('unknown_struct279', _decode_unknown_struct279),
    0xc9045a02: ('unknown_struct58_0xc9045a02', _decode_unknown_struct58_0xc9045a02),
    0xc5a31fc4: ('unknown_struct280', _decode_unknown_struct280),
    0xfab2f514: ('unknown_struct58_0xfab2f514', _decode_unknown_struct58_0xfab2f514),
    0x6a5549a3: ('unknown_struct281', _decode_unknown_struct281),
    0x7a5e5e73: ('unknown_0x7a5e5e73', _decode_unknown_0x7a5e5e73),
    0x63cd839f: ('unknown_struct282', _decode_unknown_struct282),
    0xf17aef10: ('unknown_struct283', _decode_unknown_struct283),
    0xc932f084: ('unknown_struct284', _decode_unknown_struct284),
    0x16768be: ('unknown_0x016768be', _decode_unknown_0x016768be),
}
