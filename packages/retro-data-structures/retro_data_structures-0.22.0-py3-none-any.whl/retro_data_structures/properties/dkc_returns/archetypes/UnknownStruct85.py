# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct85(BaseProperty):
    start_hidden: bool = dataclasses.field(default=True)
    minimum_hide_time: float = dataclasses.field(default=0.5)
    maximum_hide_time: float = dataclasses.field(default=1.0)

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

        data.write(b'M\xef{\x9b')  # 0x4def7b9b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.start_hidden))

        data.write(b'\xcc}\x17\xd6')  # 0xcc7d17d6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.minimum_hide_time))

        data.write(b'\xe5\x03\xea\xce')  # 0xe503eace
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_hide_time))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            start_hidden=data['start_hidden'],
            minimum_hide_time=data['minimum_hide_time'],
            maximum_hide_time=data['maximum_hide_time'],
        )

    def to_json(self) -> dict:
        return {
            'start_hidden': self.start_hidden,
            'minimum_hide_time': self.minimum_hide_time,
            'maximum_hide_time': self.maximum_hide_time,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x4def7b9b, 0xcc7d17d6, 0xe503eace)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct85]:
    if property_count != 3:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LH?LHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(27))
    if (dec[0], dec[3], dec[6]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct85(
        dec[2],
        dec[5],
        dec[8],
    )


def _decode_start_hidden(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_minimum_hide_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_maximum_hide_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x4def7b9b: ('start_hidden', _decode_start_hidden),
    0xcc7d17d6: ('minimum_hide_time', _decode_minimum_hide_time),
    0xe503eace: ('maximum_hide_time', _decode_maximum_hide_time),
}
