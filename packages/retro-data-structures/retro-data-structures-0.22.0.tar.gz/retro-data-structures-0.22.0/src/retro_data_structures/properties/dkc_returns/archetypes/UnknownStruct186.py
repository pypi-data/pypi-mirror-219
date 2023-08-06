# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct52 import UnknownStruct52


@dataclasses.dataclass()
class UnknownStruct186(BaseProperty):
    unknown_0x8a58a7f8: int = dataclasses.field(default=1)
    unknown_0xa9ac7ded: float = dataclasses.field(default=2.0)
    unknown_struct52_0x17a93807: UnknownStruct52 = dataclasses.field(default_factory=UnknownStruct52)
    unknown_struct52_0x8c219932: UnknownStruct52 = dataclasses.field(default_factory=UnknownStruct52)

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
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\x8aX\xa7\xf8')  # 0x8a58a7f8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x8a58a7f8))

        data.write(b'\xa9\xac}\xed')  # 0xa9ac7ded
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa9ac7ded))

        data.write(b'\x17\xa98\x07')  # 0x17a93807
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct52_0x17a93807.to_stream(data, default_override={'distance': 4.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8c!\x992')  # 0x8c219932
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct52_0x8c219932.to_stream(data, default_override={'distance': 5.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x8a58a7f8=data['unknown_0x8a58a7f8'],
            unknown_0xa9ac7ded=data['unknown_0xa9ac7ded'],
            unknown_struct52_0x17a93807=UnknownStruct52.from_json(data['unknown_struct52_0x17a93807']),
            unknown_struct52_0x8c219932=UnknownStruct52.from_json(data['unknown_struct52_0x8c219932']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x8a58a7f8': self.unknown_0x8a58a7f8,
            'unknown_0xa9ac7ded': self.unknown_0xa9ac7ded,
            'unknown_struct52_0x17a93807': self.unknown_struct52_0x17a93807.to_json(),
            'unknown_struct52_0x8c219932': self.unknown_struct52_0x8c219932.to_json(),
        }


def _decode_unknown_0x8a58a7f8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xa9ac7ded(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_struct52_0x17a93807(data: typing.BinaryIO, property_size: int):
    return UnknownStruct52.from_stream(data, property_size, default_override={'distance': 4.0})


def _decode_unknown_struct52_0x8c219932(data: typing.BinaryIO, property_size: int):
    return UnknownStruct52.from_stream(data, property_size, default_override={'distance': 5.0})


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x8a58a7f8: ('unknown_0x8a58a7f8', _decode_unknown_0x8a58a7f8),
    0xa9ac7ded: ('unknown_0xa9ac7ded', _decode_unknown_0xa9ac7ded),
    0x17a93807: ('unknown_struct52_0x17a93807', _decode_unknown_struct52_0x17a93807),
    0x8c219932: ('unknown_struct52_0x8c219932', _decode_unknown_struct52_0x8c219932),
}
