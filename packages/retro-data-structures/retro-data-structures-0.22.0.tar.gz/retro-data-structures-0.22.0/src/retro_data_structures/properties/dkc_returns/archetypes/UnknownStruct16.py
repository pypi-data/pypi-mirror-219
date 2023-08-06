# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct16(BaseProperty):
    max_delay: float = dataclasses.field(default=0.0)
    delay: float = dataclasses.field(default=0.0)
    feedback: float = dataclasses.field(default=0.0)
    unknown: float = dataclasses.field(default=0.0)

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

        data.write(b'\xf5\xb6\xbfl')  # 0xf5b6bf6c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_delay))

        data.write(b'\x14\xff\xf3\x9c')  # 0x14fff39c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.delay))

        data.write(b'\x1d\xa3{\r')  # 0x1da37b0d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.feedback))

        data.write(b'\x11\xbc^z')  # 0x11bc5e7a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            max_delay=data['max_delay'],
            delay=data['delay'],
            feedback=data['feedback'],
            unknown=data['unknown'],
        )

    def to_json(self) -> dict:
        return {
            'max_delay': self.max_delay,
            'delay': self.delay,
            'feedback': self.feedback,
            'unknown': self.unknown,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xf5b6bf6c, 0x14fff39c, 0x1da37b0d, 0x11bc5e7a)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct16]:
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

    return UnknownStruct16(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
    )


def _decode_max_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_feedback(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf5b6bf6c: ('max_delay', _decode_max_delay),
    0x14fff39c: ('delay', _decode_delay),
    0x1da37b0d: ('feedback', _decode_feedback),
    0x11bc5e7a: ('unknown', _decode_unknown),
}
