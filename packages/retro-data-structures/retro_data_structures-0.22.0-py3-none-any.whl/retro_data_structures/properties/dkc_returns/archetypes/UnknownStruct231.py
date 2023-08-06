# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct230 import UnknownStruct230


@dataclasses.dataclass()
class UnknownStruct231(BaseProperty):
    unknown_0xbb3c732e: bool = dataclasses.field(default=True)
    unknown_0x44749ab7: bool = dataclasses.field(default=False)
    unknown_0xd7f4ea7f: bool = dataclasses.field(default=True)
    unknown_0x46997d8a: bool = dataclasses.field(default=True)
    unknown_0xa7a8c42a: float = dataclasses.field(default=3.5)
    unknown_struct230: UnknownStruct230 = dataclasses.field(default_factory=UnknownStruct230)

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
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'\xbb<s.')  # 0xbb3c732e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xbb3c732e))

        data.write(b'Dt\x9a\xb7')  # 0x44749ab7
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x44749ab7))

        data.write(b'\xd7\xf4\xea\x7f')  # 0xd7f4ea7f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xd7f4ea7f))

        data.write(b'F\x99}\x8a')  # 0x46997d8a
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x46997d8a))

        data.write(b'\xa7\xa8\xc4*')  # 0xa7a8c42a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa7a8c42a))

        data.write(b'\xe39VU')  # 0xe3395655
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct230.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xbb3c732e=data['unknown_0xbb3c732e'],
            unknown_0x44749ab7=data['unknown_0x44749ab7'],
            unknown_0xd7f4ea7f=data['unknown_0xd7f4ea7f'],
            unknown_0x46997d8a=data['unknown_0x46997d8a'],
            unknown_0xa7a8c42a=data['unknown_0xa7a8c42a'],
            unknown_struct230=UnknownStruct230.from_json(data['unknown_struct230']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xbb3c732e': self.unknown_0xbb3c732e,
            'unknown_0x44749ab7': self.unknown_0x44749ab7,
            'unknown_0xd7f4ea7f': self.unknown_0xd7f4ea7f,
            'unknown_0x46997d8a': self.unknown_0x46997d8a,
            'unknown_0xa7a8c42a': self.unknown_0xa7a8c42a,
            'unknown_struct230': self.unknown_struct230.to_json(),
        }


def _decode_unknown_0xbb3c732e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x44749ab7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xd7f4ea7f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x46997d8a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xa7a8c42a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_struct230(data: typing.BinaryIO, property_size: int):
    return UnknownStruct230.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xbb3c732e: ('unknown_0xbb3c732e', _decode_unknown_0xbb3c732e),
    0x44749ab7: ('unknown_0x44749ab7', _decode_unknown_0x44749ab7),
    0xd7f4ea7f: ('unknown_0xd7f4ea7f', _decode_unknown_0xd7f4ea7f),
    0x46997d8a: ('unknown_0x46997d8a', _decode_unknown_0x46997d8a),
    0xa7a8c42a: ('unknown_0xa7a8c42a', _decode_unknown_0xa7a8c42a),
    0xe3395655: ('unknown_struct230', _decode_unknown_struct230),
}
