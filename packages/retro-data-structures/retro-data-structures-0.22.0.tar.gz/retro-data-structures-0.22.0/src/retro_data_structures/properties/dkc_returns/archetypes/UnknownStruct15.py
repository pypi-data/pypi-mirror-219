# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct15(BaseProperty):
    unknown_0xf38c4b4d: float = dataclasses.field(default=-1.5)
    unknown_0xcd3dd32a: float = dataclasses.field(default=2.75)
    unknown_0x8f6291d1: float = dataclasses.field(default=6.0)

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

        data.write(b'\xf3\x8cKM')  # 0xf38c4b4d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf38c4b4d))

        data.write(b'\xcd=\xd3*')  # 0xcd3dd32a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xcd3dd32a))

        data.write(b'\x8fb\x91\xd1')  # 0x8f6291d1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8f6291d1))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xf38c4b4d=data['unknown_0xf38c4b4d'],
            unknown_0xcd3dd32a=data['unknown_0xcd3dd32a'],
            unknown_0x8f6291d1=data['unknown_0x8f6291d1'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xf38c4b4d': self.unknown_0xf38c4b4d,
            'unknown_0xcd3dd32a': self.unknown_0xcd3dd32a,
            'unknown_0x8f6291d1': self.unknown_0x8f6291d1,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xf38c4b4d, 0xcd3dd32a, 0x8f6291d1)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct15]:
    if property_count != 3:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(30))
    if (dec[0], dec[3], dec[6]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct15(
        dec[2],
        dec[5],
        dec[8],
    )


def _decode_unknown_0xf38c4b4d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xcd3dd32a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8f6291d1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf38c4b4d: ('unknown_0xf38c4b4d', _decode_unknown_0xf38c4b4d),
    0xcd3dd32a: ('unknown_0xcd3dd32a', _decode_unknown_0xcd3dd32a),
    0x8f6291d1: ('unknown_0x8f6291d1', _decode_unknown_0x8f6291d1),
}
