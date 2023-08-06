# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.SplineType import SplineType
from retro_data_structures.properties.dkc_returns.core.Spline import Spline


@dataclasses.dataclass()
class UnknownStruct32(BaseProperty):
    motion_spline_type: SplineType = dataclasses.field(default_factory=SplineType)
    motion_control_spline: Spline = dataclasses.field(default_factory=Spline)
    motion_spline_duration: float = dataclasses.field(default=10.0)
    speed_multiplier: float = dataclasses.field(default=1.0)
    initial_time: float = dataclasses.field(default=0.0)
    motion_spline_loops: bool = dataclasses.field(default=False)
    loop_forever: bool = dataclasses.field(default=False)
    auto_start: bool = dataclasses.field(default=False)

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
        data.write(b'\x00\x08')  # 8 properties

        data.write(b'I=j-')  # 0x493d6a2d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.motion_spline_type.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b"'\xe5\xf8t")  # 0x27e5f874
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.motion_control_spline.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfd\x1e/V')  # 0xfd1e2f56
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.motion_spline_duration))

        data.write(b'H\x85\xdf\xfa')  # 0x4885dffa
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.speed_multiplier))

        data.write(b'\xa5u=R')  # 0xa5753d52
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.initial_time))

        data.write(b'\x7f\xc9`\x14')  # 0x7fc96014
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.motion_spline_loops))

        data.write(b'\x08\xbbs\xc5')  # 0x8bb73c5
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.loop_forever))

        data.write(b'2\x17\xdf\xf8')  # 0x3217dff8
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.auto_start))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            motion_spline_type=SplineType.from_json(data['motion_spline_type']),
            motion_control_spline=Spline.from_json(data['motion_control_spline']),
            motion_spline_duration=data['motion_spline_duration'],
            speed_multiplier=data['speed_multiplier'],
            initial_time=data['initial_time'],
            motion_spline_loops=data['motion_spline_loops'],
            loop_forever=data['loop_forever'],
            auto_start=data['auto_start'],
        )

    def to_json(self) -> dict:
        return {
            'motion_spline_type': self.motion_spline_type.to_json(),
            'motion_control_spline': self.motion_control_spline.to_json(),
            'motion_spline_duration': self.motion_spline_duration,
            'speed_multiplier': self.speed_multiplier,
            'initial_time': self.initial_time,
            'motion_spline_loops': self.motion_spline_loops,
            'loop_forever': self.loop_forever,
            'auto_start': self.auto_start,
        }


def _decode_motion_spline_type(data: typing.BinaryIO, property_size: int):
    return SplineType.from_stream(data, property_size)


def _decode_motion_control_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_motion_spline_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_speed_multiplier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_initial_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_motion_spline_loops(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_loop_forever(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_auto_start(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x493d6a2d: ('motion_spline_type', _decode_motion_spline_type),
    0x27e5f874: ('motion_control_spline', _decode_motion_control_spline),
    0xfd1e2f56: ('motion_spline_duration', _decode_motion_spline_duration),
    0x4885dffa: ('speed_multiplier', _decode_speed_multiplier),
    0xa5753d52: ('initial_time', _decode_initial_time),
    0x7fc96014: ('motion_spline_loops', _decode_motion_spline_loops),
    0x8bb73c5: ('loop_forever', _decode_loop_forever),
    0x3217dff8: ('auto_start', _decode_auto_start),
}
