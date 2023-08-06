# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct51 import UnknownStruct51
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct60 import UnknownStruct60


@dataclasses.dataclass()
class RobotChickenFlyerStructB(BaseProperty):
    attack_type: enums.AttackType = dataclasses.field(default=enums.AttackType.Unknown1)
    unknown_0x8a58a7f8: int = dataclasses.field(default=3)
    unknown_0x584b5df1: UnknownStruct60 = dataclasses.field(default_factory=UnknownStruct60)
    unknown_struct51_0x1d366d8e: UnknownStruct51 = dataclasses.field(default_factory=UnknownStruct51)
    unknown_struct51_0x525191c2: UnknownStruct51 = dataclasses.field(default_factory=UnknownStruct51)
    unknown_struct51_0x1b80811c: UnknownStruct51 = dataclasses.field(default_factory=UnknownStruct51)
    unknown_struct51_0xed21c295: UnknownStruct51 = dataclasses.field(default_factory=UnknownStruct51)

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
        data.write(struct.pack('>l', self.unknown_0x8a58a7f8))

        data.write(b'XK]\xf1')  # 0x584b5df1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x584b5df1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1d6m\x8e')  # 0x1d366d8e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct51_0x1d366d8e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'RQ\x91\xc2')  # 0x525191c2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct51_0x525191c2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1b\x80\x81\x1c')  # 0x1b80811c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct51_0x1b80811c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xed!\xc2\x95')  # 0xed21c295
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct51_0xed21c295.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            attack_type=enums.AttackType.from_json(data['attack_type']),
            unknown_0x8a58a7f8=data['unknown_0x8a58a7f8'],
            unknown_0x584b5df1=UnknownStruct60.from_json(data['unknown_0x584b5df1']),
            unknown_struct51_0x1d366d8e=UnknownStruct51.from_json(data['unknown_struct51_0x1d366d8e']),
            unknown_struct51_0x525191c2=UnknownStruct51.from_json(data['unknown_struct51_0x525191c2']),
            unknown_struct51_0x1b80811c=UnknownStruct51.from_json(data['unknown_struct51_0x1b80811c']),
            unknown_struct51_0xed21c295=UnknownStruct51.from_json(data['unknown_struct51_0xed21c295']),
        )

    def to_json(self) -> dict:
        return {
            'attack_type': self.attack_type.to_json(),
            'unknown_0x8a58a7f8': self.unknown_0x8a58a7f8,
            'unknown_0x584b5df1': self.unknown_0x584b5df1.to_json(),
            'unknown_struct51_0x1d366d8e': self.unknown_struct51_0x1d366d8e.to_json(),
            'unknown_struct51_0x525191c2': self.unknown_struct51_0x525191c2.to_json(),
            'unknown_struct51_0x1b80811c': self.unknown_struct51_0x1b80811c.to_json(),
            'unknown_struct51_0xed21c295': self.unknown_struct51_0xed21c295.to_json(),
        }


def _decode_attack_type(data: typing.BinaryIO, property_size: int):
    return enums.AttackType.from_stream(data)


def _decode_unknown_0x8a58a7f8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x584b5df1(data: typing.BinaryIO, property_size: int):
    return UnknownStruct60.from_stream(data, property_size)


def _decode_unknown_struct51_0x1d366d8e(data: typing.BinaryIO, property_size: int):
    return UnknownStruct51.from_stream(data, property_size)


def _decode_unknown_struct51_0x525191c2(data: typing.BinaryIO, property_size: int):
    return UnknownStruct51.from_stream(data, property_size)


def _decode_unknown_struct51_0x1b80811c(data: typing.BinaryIO, property_size: int):
    return UnknownStruct51.from_stream(data, property_size)


def _decode_unknown_struct51_0xed21c295(data: typing.BinaryIO, property_size: int):
    return UnknownStruct51.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x7d939a1: ('attack_type', _decode_attack_type),
    0x8a58a7f8: ('unknown_0x8a58a7f8', _decode_unknown_0x8a58a7f8),
    0x584b5df1: ('unknown_0x584b5df1', _decode_unknown_0x584b5df1),
    0x1d366d8e: ('unknown_struct51_0x1d366d8e', _decode_unknown_struct51_0x1d366d8e),
    0x525191c2: ('unknown_struct51_0x525191c2', _decode_unknown_struct51_0x525191c2),
    0x1b80811c: ('unknown_struct51_0x1b80811c', _decode_unknown_struct51_0x1b80811c),
    0xed21c295: ('unknown_struct51_0xed21c295', _decode_unknown_struct51_0xed21c295),
}
