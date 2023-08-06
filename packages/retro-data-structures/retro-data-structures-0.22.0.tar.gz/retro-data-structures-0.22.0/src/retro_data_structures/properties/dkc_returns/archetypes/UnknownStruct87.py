# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct87(BaseProperty):
    flip_duration: float = dataclasses.field(default=3.0)
    unknown_0xf5fa970d: float = dataclasses.field(default=3.0)
    unknown_0x14044489: float = dataclasses.field(default=0.33000001311302185)
    struggle_duration: float = dataclasses.field(default=2.0)

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

        data.write(b'\xf7\xf88z')  # 0xf7f8387a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.flip_duration))

        data.write(b'\xf5\xfa\x97\r')  # 0xf5fa970d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf5fa970d))

        data.write(b'\x14\x04D\x89')  # 0x14044489
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x14044489))

        data.write(b'9\x87\r5')  # 0x39870d35
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.struggle_duration))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            flip_duration=data['flip_duration'],
            unknown_0xf5fa970d=data['unknown_0xf5fa970d'],
            unknown_0x14044489=data['unknown_0x14044489'],
            struggle_duration=data['struggle_duration'],
        )

    def to_json(self) -> dict:
        return {
            'flip_duration': self.flip_duration,
            'unknown_0xf5fa970d': self.unknown_0xf5fa970d,
            'unknown_0x14044489': self.unknown_0x14044489,
            'struggle_duration': self.struggle_duration,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xf7f8387a, 0xf5fa970d, 0x14044489, 0x39870d35)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct87]:
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

    return UnknownStruct87(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
    )


def _decode_flip_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf5fa970d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x14044489(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_struggle_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf7f8387a: ('flip_duration', _decode_flip_duration),
    0xf5fa970d: ('unknown_0xf5fa970d', _decode_unknown_0xf5fa970d),
    0x14044489: ('unknown_0x14044489', _decode_unknown_0x14044489),
    0x39870d35: ('struggle_duration', _decode_struggle_duration),
}
