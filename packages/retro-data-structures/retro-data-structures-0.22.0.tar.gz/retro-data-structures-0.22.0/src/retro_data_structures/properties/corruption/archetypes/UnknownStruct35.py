# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.GhorStructA import GhorStructA


@dataclasses.dataclass()
class UnknownStruct35(BaseProperty):
    ghor_struct_a_0x8b5db983: GhorStructA = dataclasses.field(default_factory=GhorStructA)
    ghor_struct_a_0x04cdc6a6: GhorStructA = dataclasses.field(default_factory=GhorStructA)
    ghor_struct_a_0xe451d02c: GhorStructA = dataclasses.field(default_factory=GhorStructA)
    ghor_struct_a_0x72f708f2: GhorStructA = dataclasses.field(default_factory=GhorStructA)
    ghor_struct_a_0x8cb41734: GhorStructA = dataclasses.field(default_factory=GhorStructA)

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
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'\x8b]\xb9\x83')  # 0x8b5db983
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ghor_struct_a_0x8b5db983.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x04\xcd\xc6\xa6')  # 0x4cdc6a6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ghor_struct_a_0x04cdc6a6.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe4Q\xd0,')  # 0xe451d02c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ghor_struct_a_0xe451d02c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'r\xf7\x08\xf2')  # 0x72f708f2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ghor_struct_a_0x72f708f2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8c\xb4\x174')  # 0x8cb41734
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ghor_struct_a_0x8cb41734.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            ghor_struct_a_0x8b5db983=GhorStructA.from_json(data['ghor_struct_a_0x8b5db983']),
            ghor_struct_a_0x04cdc6a6=GhorStructA.from_json(data['ghor_struct_a_0x04cdc6a6']),
            ghor_struct_a_0xe451d02c=GhorStructA.from_json(data['ghor_struct_a_0xe451d02c']),
            ghor_struct_a_0x72f708f2=GhorStructA.from_json(data['ghor_struct_a_0x72f708f2']),
            ghor_struct_a_0x8cb41734=GhorStructA.from_json(data['ghor_struct_a_0x8cb41734']),
        )

    def to_json(self) -> dict:
        return {
            'ghor_struct_a_0x8b5db983': self.ghor_struct_a_0x8b5db983.to_json(),
            'ghor_struct_a_0x04cdc6a6': self.ghor_struct_a_0x04cdc6a6.to_json(),
            'ghor_struct_a_0xe451d02c': self.ghor_struct_a_0xe451d02c.to_json(),
            'ghor_struct_a_0x72f708f2': self.ghor_struct_a_0x72f708f2.to_json(),
            'ghor_struct_a_0x8cb41734': self.ghor_struct_a_0x8cb41734.to_json(),
        }


def _decode_ghor_struct_a_0x8b5db983(data: typing.BinaryIO, property_size: int):
    return GhorStructA.from_stream(data, property_size)


def _decode_ghor_struct_a_0x04cdc6a6(data: typing.BinaryIO, property_size: int):
    return GhorStructA.from_stream(data, property_size)


def _decode_ghor_struct_a_0xe451d02c(data: typing.BinaryIO, property_size: int):
    return GhorStructA.from_stream(data, property_size)


def _decode_ghor_struct_a_0x72f708f2(data: typing.BinaryIO, property_size: int):
    return GhorStructA.from_stream(data, property_size)


def _decode_ghor_struct_a_0x8cb41734(data: typing.BinaryIO, property_size: int):
    return GhorStructA.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x8b5db983: ('ghor_struct_a_0x8b5db983', _decode_ghor_struct_a_0x8b5db983),
    0x4cdc6a6: ('ghor_struct_a_0x04cdc6a6', _decode_ghor_struct_a_0x04cdc6a6),
    0xe451d02c: ('ghor_struct_a_0xe451d02c', _decode_ghor_struct_a_0xe451d02c),
    0x72f708f2: ('ghor_struct_a_0x72f708f2', _decode_ghor_struct_a_0x72f708f2),
    0x8cb41734: ('ghor_struct_a_0x8cb41734', _decode_ghor_struct_a_0x8cb41734),
}
