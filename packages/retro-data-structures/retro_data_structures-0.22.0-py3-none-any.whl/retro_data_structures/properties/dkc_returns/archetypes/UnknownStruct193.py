# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct47 import UnknownStruct47


@dataclasses.dataclass()
class UnknownStruct193(BaseProperty):
    unknown_struct47_0xd6554c1a: UnknownStruct47 = dataclasses.field(default_factory=UnknownStruct47)
    unknown_struct47_0xe59c4016: UnknownStruct47 = dataclasses.field(default_factory=UnknownStruct47)
    unknown_struct47_0x2416759c: UnknownStruct47 = dataclasses.field(default_factory=UnknownStruct47)

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
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\xd6UL\x1a')  # 0xd6554c1a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct47_0xd6554c1a.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe5\x9c@\x16')  # 0xe59c4016
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct47_0xe59c4016.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'$\x16u\x9c')  # 0x2416759c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct47_0x2416759c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_struct47_0xd6554c1a=UnknownStruct47.from_json(data['unknown_struct47_0xd6554c1a']),
            unknown_struct47_0xe59c4016=UnknownStruct47.from_json(data['unknown_struct47_0xe59c4016']),
            unknown_struct47_0x2416759c=UnknownStruct47.from_json(data['unknown_struct47_0x2416759c']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_struct47_0xd6554c1a': self.unknown_struct47_0xd6554c1a.to_json(),
            'unknown_struct47_0xe59c4016': self.unknown_struct47_0xe59c4016.to_json(),
            'unknown_struct47_0x2416759c': self.unknown_struct47_0x2416759c.to_json(),
        }


def _decode_unknown_struct47_0xd6554c1a(data: typing.BinaryIO, property_size: int):
    return UnknownStruct47.from_stream(data, property_size)


def _decode_unknown_struct47_0xe59c4016(data: typing.BinaryIO, property_size: int):
    return UnknownStruct47.from_stream(data, property_size)


def _decode_unknown_struct47_0x2416759c(data: typing.BinaryIO, property_size: int):
    return UnknownStruct47.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xd6554c1a: ('unknown_struct47_0xd6554c1a', _decode_unknown_struct47_0xd6554c1a),
    0xe59c4016: ('unknown_struct47_0xe59c4016', _decode_unknown_struct47_0xe59c4016),
    0x2416759c: ('unknown_struct47_0x2416759c', _decode_unknown_struct47_0x2416759c),
}
