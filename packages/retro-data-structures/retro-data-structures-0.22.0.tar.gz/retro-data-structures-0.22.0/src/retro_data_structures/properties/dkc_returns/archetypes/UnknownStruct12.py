# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct12(BaseProperty):
    delay_time: float = dataclasses.field(default=0.0)
    depth: float = dataclasses.field(default=0.0)
    rate: float = dataclasses.field(default=0.0)
    feedback: float = dataclasses.field(default=0.0)

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

        data.write(b'\x8e\x16\xe0\x12')  # 0x8e16e012
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.delay_time))

        data.write(b'\xc2\x87\xb5\xaf')  # 0xc287b5af
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.depth))

        data.write(b'\x16\x8a\xe1\xdd')  # 0x168ae1dd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rate))

        data.write(b'\x1d\xa3{\r')  # 0x1da37b0d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.feedback))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            delay_time=data['delay_time'],
            depth=data['depth'],
            rate=data['rate'],
            feedback=data['feedback'],
        )

    def to_json(self) -> dict:
        return {
            'delay_time': self.delay_time,
            'depth': self.depth,
            'rate': self.rate,
            'feedback': self.feedback,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x8e16e012, 0xc287b5af, 0x168ae1dd, 0x1da37b0d)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct12]:
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

    return UnknownStruct12(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
    )


def _decode_delay_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_depth(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_feedback(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x8e16e012: ('delay_time', _decode_delay_time),
    0xc287b5af: ('depth', _decode_depth),
    0x168ae1dd: ('rate', _decode_rate),
    0x1da37b0d: ('feedback', _decode_feedback),
}
