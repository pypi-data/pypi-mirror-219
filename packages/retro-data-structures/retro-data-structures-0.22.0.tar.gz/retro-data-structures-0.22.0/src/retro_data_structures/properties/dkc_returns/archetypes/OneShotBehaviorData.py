# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class OneShotBehaviorData(BaseProperty):
    initial_delay_time: float = dataclasses.field(default=1.0)
    repeat: bool = dataclasses.field(default=True)
    delay_time: float = dataclasses.field(default=1.0)
    number_of_animations: int = dataclasses.field(default=0)
    animation01: int = dataclasses.field(default=0)
    animation02: int = dataclasses.field(default=0)

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
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'\x93"GP')  # 0x93224750
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.initial_delay_time))

        data.write(b'y\x81\x84\xbb')  # 0x798184bb
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.repeat))

        data.write(b'\x8e\x16\xe0\x12')  # 0x8e16e012
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.delay_time))

        data.write(b'h*\xa3\xc9')  # 0x682aa3c9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.number_of_animations))

        data.write(b'\x85\x14%v')  # 0x85142576
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.animation01))

        data.write(b'&B\xa3\xdf')  # 0x2642a3df
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.animation02))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            initial_delay_time=data['initial_delay_time'],
            repeat=data['repeat'],
            delay_time=data['delay_time'],
            number_of_animations=data['number_of_animations'],
            animation01=data['animation01'],
            animation02=data['animation02'],
        )

    def to_json(self) -> dict:
        return {
            'initial_delay_time': self.initial_delay_time,
            'repeat': self.repeat,
            'delay_time': self.delay_time,
            'number_of_animations': self.number_of_animations,
            'animation01': self.animation01,
            'animation02': self.animation02,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x93224750, 0x798184bb, 0x8e16e012, 0x682aa3c9, 0x85142576, 0x2642a3df)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[OneShotBehaviorData]:
    if property_count != 6:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLH?LHfLHlLHlLHl')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(57))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15]) != _FAST_IDS:
        data.seek(before)
        return None

    return OneShotBehaviorData(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
    )


def _decode_initial_delay_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_repeat(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_delay_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_number_of_animations(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_animation01(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_animation02(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x93224750: ('initial_delay_time', _decode_initial_delay_time),
    0x798184bb: ('repeat', _decode_repeat),
    0x8e16e012: ('delay_time', _decode_delay_time),
    0x682aa3c9: ('number_of_animations', _decode_number_of_animations),
    0x85142576: ('animation01', _decode_animation01),
    0x2642a3df: ('animation02', _decode_animation02),
}
