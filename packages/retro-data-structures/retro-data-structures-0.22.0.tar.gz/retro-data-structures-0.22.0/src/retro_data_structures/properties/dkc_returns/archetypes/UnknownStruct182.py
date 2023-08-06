# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct165 import UnknownStruct165
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct166 import UnknownStruct166
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct168 import UnknownStruct168
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct169 import UnknownStruct169
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct174 import UnknownStruct174
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct175 import UnknownStruct175
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct176 import UnknownStruct176
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct177 import UnknownStruct177
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct178 import UnknownStruct178
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct179 import UnknownStruct179
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct180 import UnknownStruct180
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct181 import UnknownStruct181
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct34 import UnknownStruct34
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct35 import UnknownStruct35


@dataclasses.dataclass()
class UnknownStruct182(BaseProperty):
    unknown_struct35: UnknownStruct35 = dataclasses.field(default_factory=UnknownStruct35)
    unknown_struct165: UnknownStruct165 = dataclasses.field(default_factory=UnknownStruct165)
    unknown_struct166: UnknownStruct166 = dataclasses.field(default_factory=UnknownStruct166)
    unknown_struct168: UnknownStruct168 = dataclasses.field(default_factory=UnknownStruct168)
    unknown_struct169: UnknownStruct169 = dataclasses.field(default_factory=UnknownStruct169)
    unknown_struct174: UnknownStruct174 = dataclasses.field(default_factory=UnknownStruct174)
    unknown_struct175: UnknownStruct175 = dataclasses.field(default_factory=UnknownStruct175)
    unknown_struct176: UnknownStruct176 = dataclasses.field(default_factory=UnknownStruct176)
    unknown_struct177: UnknownStruct177 = dataclasses.field(default_factory=UnknownStruct177)
    unknown_struct34: UnknownStruct34 = dataclasses.field(default_factory=UnknownStruct34)
    unknown_struct178: UnknownStruct178 = dataclasses.field(default_factory=UnknownStruct178)
    unknown_struct179: UnknownStruct179 = dataclasses.field(default_factory=UnknownStruct179)
    unknown_struct180: UnknownStruct180 = dataclasses.field(default_factory=UnknownStruct180)
    unknown_struct181: UnknownStruct181 = dataclasses.field(default_factory=UnknownStruct181)

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
        data.write(b'\x00\x0e')  # 14 properties

        data.write(b'\xd8U$\xdb')  # 0xd85524db
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct35.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xba\xb9\x07Y')  # 0xbab90759
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct165.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf9gE\x17')  # 0xf9674517
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct166.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b',y\x16\xec')  # 0x2c7916ec
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct168.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'L\xeaS\xf4')  # 0x4cea53f4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct169.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x90\xa6\xae\x10')  # 0x90a6ae10
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct174.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'cb\xf9\x10')  # 0x6362f910
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct175.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'7(f\xd4')  # 0x372866d4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct176.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xea/u\n')  # 0xea2f750a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct177.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Q\xad\xb9h')  # 0x51adb968
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct34.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd8\xba\x1e\x9a')  # 0xd8ba1e9a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct178.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'*\xa4\x87#')  # 0x2aa48723
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct179.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc6Gl}')  # 0xc6476c7d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct180.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbc#y\xa9')  # 0xbc2379a9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct181.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_struct35=UnknownStruct35.from_json(data['unknown_struct35']),
            unknown_struct165=UnknownStruct165.from_json(data['unknown_struct165']),
            unknown_struct166=UnknownStruct166.from_json(data['unknown_struct166']),
            unknown_struct168=UnknownStruct168.from_json(data['unknown_struct168']),
            unknown_struct169=UnknownStruct169.from_json(data['unknown_struct169']),
            unknown_struct174=UnknownStruct174.from_json(data['unknown_struct174']),
            unknown_struct175=UnknownStruct175.from_json(data['unknown_struct175']),
            unknown_struct176=UnknownStruct176.from_json(data['unknown_struct176']),
            unknown_struct177=UnknownStruct177.from_json(data['unknown_struct177']),
            unknown_struct34=UnknownStruct34.from_json(data['unknown_struct34']),
            unknown_struct178=UnknownStruct178.from_json(data['unknown_struct178']),
            unknown_struct179=UnknownStruct179.from_json(data['unknown_struct179']),
            unknown_struct180=UnknownStruct180.from_json(data['unknown_struct180']),
            unknown_struct181=UnknownStruct181.from_json(data['unknown_struct181']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_struct35': self.unknown_struct35.to_json(),
            'unknown_struct165': self.unknown_struct165.to_json(),
            'unknown_struct166': self.unknown_struct166.to_json(),
            'unknown_struct168': self.unknown_struct168.to_json(),
            'unknown_struct169': self.unknown_struct169.to_json(),
            'unknown_struct174': self.unknown_struct174.to_json(),
            'unknown_struct175': self.unknown_struct175.to_json(),
            'unknown_struct176': self.unknown_struct176.to_json(),
            'unknown_struct177': self.unknown_struct177.to_json(),
            'unknown_struct34': self.unknown_struct34.to_json(),
            'unknown_struct178': self.unknown_struct178.to_json(),
            'unknown_struct179': self.unknown_struct179.to_json(),
            'unknown_struct180': self.unknown_struct180.to_json(),
            'unknown_struct181': self.unknown_struct181.to_json(),
        }


def _decode_unknown_struct35(data: typing.BinaryIO, property_size: int):
    return UnknownStruct35.from_stream(data, property_size)


def _decode_unknown_struct165(data: typing.BinaryIO, property_size: int):
    return UnknownStruct165.from_stream(data, property_size)


def _decode_unknown_struct166(data: typing.BinaryIO, property_size: int):
    return UnknownStruct166.from_stream(data, property_size)


def _decode_unknown_struct168(data: typing.BinaryIO, property_size: int):
    return UnknownStruct168.from_stream(data, property_size)


def _decode_unknown_struct169(data: typing.BinaryIO, property_size: int):
    return UnknownStruct169.from_stream(data, property_size)


def _decode_unknown_struct174(data: typing.BinaryIO, property_size: int):
    return UnknownStruct174.from_stream(data, property_size)


def _decode_unknown_struct175(data: typing.BinaryIO, property_size: int):
    return UnknownStruct175.from_stream(data, property_size)


def _decode_unknown_struct176(data: typing.BinaryIO, property_size: int):
    return UnknownStruct176.from_stream(data, property_size)


def _decode_unknown_struct177(data: typing.BinaryIO, property_size: int):
    return UnknownStruct177.from_stream(data, property_size)


def _decode_unknown_struct34(data: typing.BinaryIO, property_size: int):
    return UnknownStruct34.from_stream(data, property_size)


def _decode_unknown_struct178(data: typing.BinaryIO, property_size: int):
    return UnknownStruct178.from_stream(data, property_size)


def _decode_unknown_struct179(data: typing.BinaryIO, property_size: int):
    return UnknownStruct179.from_stream(data, property_size)


def _decode_unknown_struct180(data: typing.BinaryIO, property_size: int):
    return UnknownStruct180.from_stream(data, property_size)


def _decode_unknown_struct181(data: typing.BinaryIO, property_size: int):
    return UnknownStruct181.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xd85524db: ('unknown_struct35', _decode_unknown_struct35),
    0xbab90759: ('unknown_struct165', _decode_unknown_struct165),
    0xf9674517: ('unknown_struct166', _decode_unknown_struct166),
    0x2c7916ec: ('unknown_struct168', _decode_unknown_struct168),
    0x4cea53f4: ('unknown_struct169', _decode_unknown_struct169),
    0x90a6ae10: ('unknown_struct174', _decode_unknown_struct174),
    0x6362f910: ('unknown_struct175', _decode_unknown_struct175),
    0x372866d4: ('unknown_struct176', _decode_unknown_struct176),
    0xea2f750a: ('unknown_struct177', _decode_unknown_struct177),
    0x51adb968: ('unknown_struct34', _decode_unknown_struct34),
    0xd8ba1e9a: ('unknown_struct178', _decode_unknown_struct178),
    0x2aa48723: ('unknown_struct179', _decode_unknown_struct179),
    0xc6476c7d: ('unknown_struct180', _decode_unknown_struct180),
    0xbc2379a9: ('unknown_struct181', _decode_unknown_struct181),
}
