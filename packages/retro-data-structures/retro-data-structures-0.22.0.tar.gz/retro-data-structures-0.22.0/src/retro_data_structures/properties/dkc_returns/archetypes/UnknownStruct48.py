# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct23 import UnknownStruct23
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct59 import UnknownStruct59
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct60 import UnknownStruct60
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct61 import UnknownStruct61
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct62 import UnknownStruct62


@dataclasses.dataclass()
class UnknownStruct48(BaseProperty):
    attack_type: enums.AttackType = dataclasses.field(default=enums.AttackType.Unknown1)
    unknown: int = dataclasses.field(default=3)
    unknown_struct23: UnknownStruct23 = dataclasses.field(default_factory=UnknownStruct23)
    unknown_struct59: UnknownStruct59 = dataclasses.field(default_factory=UnknownStruct59)
    unknown_struct60: UnknownStruct60 = dataclasses.field(default_factory=UnknownStruct60)
    unknown_struct61: UnknownStruct61 = dataclasses.field(default_factory=UnknownStruct61)
    unknown_struct62: UnknownStruct62 = dataclasses.field(default_factory=UnknownStruct62)

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
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'\x07\xd99\xa1')  # 0x7d939a1
        data.write(b'\x00\x04')  # size
        self.attack_type.to_stream(data)

        data.write(b'\x8aX\xa7\xf8')  # 0x8a58a7f8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown))

        data.write(b'\x93\xfaH\xa4')  # 0x93fa48a4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct23.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc3+\xddw')  # 0xc32bdd77
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct59.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Y\x02\xa3\xab')  # 0x5902a3ab
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct60.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc7z\x8b\xf8')  # 0xc77a8bf8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct61.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'!17\x85')  # 0x21313785
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct62.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            attack_type=enums.AttackType.from_json(data['attack_type']),
            unknown=data['unknown'],
            unknown_struct23=UnknownStruct23.from_json(data['unknown_struct23']),
            unknown_struct59=UnknownStruct59.from_json(data['unknown_struct59']),
            unknown_struct60=UnknownStruct60.from_json(data['unknown_struct60']),
            unknown_struct61=UnknownStruct61.from_json(data['unknown_struct61']),
            unknown_struct62=UnknownStruct62.from_json(data['unknown_struct62']),
        )

    def to_json(self) -> dict:
        return {
            'attack_type': self.attack_type.to_json(),
            'unknown': self.unknown,
            'unknown_struct23': self.unknown_struct23.to_json(),
            'unknown_struct59': self.unknown_struct59.to_json(),
            'unknown_struct60': self.unknown_struct60.to_json(),
            'unknown_struct61': self.unknown_struct61.to_json(),
            'unknown_struct62': self.unknown_struct62.to_json(),
        }


def _decode_attack_type(data: typing.BinaryIO, property_size: int):
    return enums.AttackType.from_stream(data)


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_struct23(data: typing.BinaryIO, property_size: int):
    return UnknownStruct23.from_stream(data, property_size)


def _decode_unknown_struct59(data: typing.BinaryIO, property_size: int):
    return UnknownStruct59.from_stream(data, property_size)


def _decode_unknown_struct60(data: typing.BinaryIO, property_size: int):
    return UnknownStruct60.from_stream(data, property_size)


def _decode_unknown_struct61(data: typing.BinaryIO, property_size: int):
    return UnknownStruct61.from_stream(data, property_size)


def _decode_unknown_struct62(data: typing.BinaryIO, property_size: int):
    return UnknownStruct62.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x7d939a1: ('attack_type', _decode_attack_type),
    0x8a58a7f8: ('unknown', _decode_unknown),
    0x93fa48a4: ('unknown_struct23', _decode_unknown_struct23),
    0xc32bdd77: ('unknown_struct59', _decode_unknown_struct59),
    0x5902a3ab: ('unknown_struct60', _decode_unknown_struct60),
    0xc77a8bf8: ('unknown_struct61', _decode_unknown_struct61),
    0x21313785: ('unknown_struct62', _decode_unknown_struct62),
}
