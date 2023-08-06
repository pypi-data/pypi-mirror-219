# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct23(BaseProperty):
    unknown_0xf228ec53: float = dataclasses.field(default=3.0)
    unknown_0xd91227f1: float = dataclasses.field(default=7.0)
    unknown_0xfc764233: float = dataclasses.field(default=0.5)
    unknown_0xe29028fc: float = dataclasses.field(default=10.0)

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
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\xf2(\xecS')  # 0xf228ec53
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf228ec53))

        data.write(b"\xd9\x12'\xf1")  # 0xd91227f1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd91227f1))

        data.write(b'\xfcvB3')  # 0xfc764233
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xfc764233))

        data.write(b'\xe2\x90(\xfc')  # 0xe29028fc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe29028fc))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xf228ec53=data['unknown_0xf228ec53'],
            unknown_0xd91227f1=data['unknown_0xd91227f1'],
            unknown_0xfc764233=data['unknown_0xfc764233'],
            unknown_0xe29028fc=data['unknown_0xe29028fc'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xf228ec53': self.unknown_0xf228ec53,
            'unknown_0xd91227f1': self.unknown_0xd91227f1,
            'unknown_0xfc764233': self.unknown_0xfc764233,
            'unknown_0xe29028fc': self.unknown_0xe29028fc,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xf228ec53, 0xd91227f1, 0xfc764233, 0xe29028fc)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct23]:
    if property_count != 4:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(40))
    if (dec[0], dec[3], dec[6], dec[9]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct23(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
    )


def _decode_unknown_0xf228ec53(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd91227f1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xfc764233(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe29028fc(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf228ec53: ('unknown_0xf228ec53', _decode_unknown_0xf228ec53),
    0xd91227f1: ('unknown_0xd91227f1', _decode_unknown_0xd91227f1),
    0xfc764233: ('unknown_0xfc764233', _decode_unknown_0xfc764233),
    0xe29028fc: ('unknown_0xe29028fc', _decode_unknown_0xe29028fc),
}
