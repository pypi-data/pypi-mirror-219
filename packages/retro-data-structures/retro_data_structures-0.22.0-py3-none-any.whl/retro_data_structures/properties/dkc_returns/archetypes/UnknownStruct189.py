# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct189(BaseProperty):
    unknown_0xe84a887b: float = dataclasses.field(default=1.0)
    unknown_0x8a58a7f8: int = dataclasses.field(default=2)
    stun_duration: float = dataclasses.field(default=2.0)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

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
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\xe8J\x88{')  # 0xe84a887b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe84a887b))

        data.write(b'\x8aX\xa7\xf8')  # 0x8a58a7f8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x8a58a7f8))

        data.write(b'-\x8d\xb3\x1d')  # 0x2d8db31d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.stun_duration))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xe84a887b=data['unknown_0xe84a887b'],
            unknown_0x8a58a7f8=data['unknown_0x8a58a7f8'],
            stun_duration=data['stun_duration'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xe84a887b': self.unknown_0xe84a887b,
            'unknown_0x8a58a7f8': self.unknown_0x8a58a7f8,
            'stun_duration': self.stun_duration,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xe84a887b, 0x8a58a7f8, 0x2d8db31d)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct189]:
    if property_count != 3:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHlLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(30))
    if (dec[0], dec[3], dec[6]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct189(
        dec[2],
        dec[5],
        dec[8],
    )


def _decode_unknown_0xe84a887b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8a58a7f8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_stun_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xe84a887b: ('unknown_0xe84a887b', _decode_unknown_0xe84a887b),
    0x8a58a7f8: ('unknown_0x8a58a7f8', _decode_unknown_0x8a58a7f8),
    0x2d8db31d: ('stun_duration', _decode_stun_duration),
}
