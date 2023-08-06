# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.core.Spline import Spline


@dataclasses.dataclass()
class UnknownStruct265(BaseProperty):
    dominance: enums.Dominance = dataclasses.field(default=enums.Dominance.Unknown1)
    unknown_0x60d9b1cc: bool = dataclasses.field(default=True)
    acceleration_frame: enums.AccelerationFrame = dataclasses.field(default=enums.AccelerationFrame.Unknown1)
    movement_acceleration: float = dataclasses.field(default=0.0)
    max_movement_speed: float = dataclasses.field(default=0.0)
    passive_acceleration: float = dataclasses.field(default=0.0)
    max_passive_speed: float = dataclasses.field(default=0.0)
    stopped_threshold: float = dataclasses.field(default=0.009999999776482582)
    unknown_0x91b27cb3: float = dataclasses.field(default=0.0)
    balanced_velocity_percentage: Spline = dataclasses.field(default_factory=Spline)
    unknown_0xc355fb9f: float = dataclasses.field(default=0.0)
    unknown_0x3153f656: Spline = dataclasses.field(default_factory=Spline)

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
        data.write(b'\x00\x0c')  # 12 properties

        data.write(b'\xc2\xea|\x93')  # 0xc2ea7c93
        data.write(b'\x00\x04')  # size
        self.dominance.to_stream(data)

        data.write(b'`\xd9\xb1\xcc')  # 0x60d9b1cc
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x60d9b1cc))

        data.write(b'\xe3\xa1\xbe1')  # 0xe3a1be31
        data.write(b'\x00\x04')  # size
        self.acceleration_frame.to_stream(data)

        data.write(b'\xfb\\\xf51')  # 0xfb5cf531
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.movement_acceleration))

        data.write(b'\x00L\xabd')  # 0x4cab64
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_movement_speed))

        data.write(b'&(\x88I')  # 0x26288849
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.passive_acceleration))

        data.write(b'Q\xb0="')  # 0x51b03d22
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_passive_speed))

        data.write(b'U\x05t\xf2')  # 0x550574f2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.stopped_threshold))

        data.write(b'\x91\xb2|\xb3')  # 0x91b27cb3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x91b27cb3))

        data.write(b'Y)\x9ee')  # 0x59299e65
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.balanced_velocity_percentage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc3U\xfb\x9f')  # 0xc355fb9f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc355fb9f))

        data.write(b'1S\xf6V')  # 0x3153f656
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x3153f656.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            dominance=enums.Dominance.from_json(data['dominance']),
            unknown_0x60d9b1cc=data['unknown_0x60d9b1cc'],
            acceleration_frame=enums.AccelerationFrame.from_json(data['acceleration_frame']),
            movement_acceleration=data['movement_acceleration'],
            max_movement_speed=data['max_movement_speed'],
            passive_acceleration=data['passive_acceleration'],
            max_passive_speed=data['max_passive_speed'],
            stopped_threshold=data['stopped_threshold'],
            unknown_0x91b27cb3=data['unknown_0x91b27cb3'],
            balanced_velocity_percentage=Spline.from_json(data['balanced_velocity_percentage']),
            unknown_0xc355fb9f=data['unknown_0xc355fb9f'],
            unknown_0x3153f656=Spline.from_json(data['unknown_0x3153f656']),
        )

    def to_json(self) -> dict:
        return {
            'dominance': self.dominance.to_json(),
            'unknown_0x60d9b1cc': self.unknown_0x60d9b1cc,
            'acceleration_frame': self.acceleration_frame.to_json(),
            'movement_acceleration': self.movement_acceleration,
            'max_movement_speed': self.max_movement_speed,
            'passive_acceleration': self.passive_acceleration,
            'max_passive_speed': self.max_passive_speed,
            'stopped_threshold': self.stopped_threshold,
            'unknown_0x91b27cb3': self.unknown_0x91b27cb3,
            'balanced_velocity_percentage': self.balanced_velocity_percentage.to_json(),
            'unknown_0xc355fb9f': self.unknown_0xc355fb9f,
            'unknown_0x3153f656': self.unknown_0x3153f656.to_json(),
        }


def _decode_dominance(data: typing.BinaryIO, property_size: int):
    return enums.Dominance.from_stream(data)


def _decode_unknown_0x60d9b1cc(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_acceleration_frame(data: typing.BinaryIO, property_size: int):
    return enums.AccelerationFrame.from_stream(data)


def _decode_movement_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_movement_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_passive_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_passive_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_stopped_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x91b27cb3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_balanced_velocity_percentage(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_unknown_0xc355fb9f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x3153f656(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc2ea7c93: ('dominance', _decode_dominance),
    0x60d9b1cc: ('unknown_0x60d9b1cc', _decode_unknown_0x60d9b1cc),
    0xe3a1be31: ('acceleration_frame', _decode_acceleration_frame),
    0xfb5cf531: ('movement_acceleration', _decode_movement_acceleration),
    0x4cab64: ('max_movement_speed', _decode_max_movement_speed),
    0x26288849: ('passive_acceleration', _decode_passive_acceleration),
    0x51b03d22: ('max_passive_speed', _decode_max_passive_speed),
    0x550574f2: ('stopped_threshold', _decode_stopped_threshold),
    0x91b27cb3: ('unknown_0x91b27cb3', _decode_unknown_0x91b27cb3),
    0x59299e65: ('balanced_velocity_percentage', _decode_balanced_velocity_percentage),
    0xc355fb9f: ('unknown_0xc355fb9f', _decode_unknown_0xc355fb9f),
    0x3153f656: ('unknown_0x3153f656', _decode_unknown_0x3153f656),
}
